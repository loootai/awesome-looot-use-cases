#!/usr/bin/env python3
"""Shallow-clone the 11 repos (default branch), then
 1. list every catalog endpoint id that appears as a quoted string in src/, config/, scripts/ or a json/yaml file, and check it exists in today's catalog;
 (also lists quoted strings that start with a provider id and a hyphen but are not catalog ids, to be read by hand)
 2. in README.md and docs/*.md find lines that hold an endpoint id and a dollar price, and compare the price with today's catalog price.
Reads data/catalog-slim-*.json. Writes data/repos.json. The clone folder is the first argument (outside this repo). Usage: python3 -I scripts/check_repos.py <clone-dir>"""
import json, re, os, sys, glob, subprocess, collections, datetime
CL = sys.argv[1]
REPOS = ["looot-intent", "looot-score", "looot-reveal", "looot-techstack", "looot-signals", "looot-lookalike", "looot-ads", "looot-reviews", "looot-battlecards", "looot-mentions", "looot-warm-leads"]
cat = json.load(open(sorted(glob.glob("data/catalog-slim-*.json"))[-1]))["items"]
P = {e["op"]: (e["micros"] / 1e6, e["unit"]) for e in cat}
provs = {e["provider"] for e in cat}
tok = re.compile(r"[\"'`]([a-z0-9][a-z0-9._:-]{3,80})[\"'`]")
money = re.compile(r"\$\s?(\d+(?:\.\d+)?)")
out = {}
for r in REPOS:
    d = os.path.join(CL, r)
    if not os.path.isdir(d):
        subprocess.run(["git", "clone", "-q", "--depth", "1", f"https://github.com/loootai/{r}.git", d], check=True)
    sha = subprocess.run(["git", "-C", d, "log", "-1", "--format=%h %cI"], capture_output=True, text=True).stdout.strip()
    used = collections.Counter(); unknown = collections.Counter()
    for f in glob.glob(d + "/**/*", recursive=True):
        rel = f[len(d) + 1:]
        if os.path.isdir(f) or rel.startswith(("node_modules/", ".git/")) or rel.endswith(("package-lock.json", ".png", ".jpg", ".svg", ".gif", ".webm", ".ico")): continue
        if not (rel.startswith(("src/", "config/", "scripts/")) or rel.endswith((".json", ".yaml", ".yml"))): continue
        for m in tok.finditer(open(f, errors="ignore").read()):
            x = m.group(1)
            if x in P: used[x] += 1
            elif re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)+", x) and x.split("-")[0] in provs: unknown[x] += 1
    match = drift = 0; drifts = []
    for f in [os.path.join(d, "README.md")] + glob.glob(d + "/docs/*.md"):
        if not os.path.exists(f): continue
        for ln in open(f, errors="ignore"):
            ids = [t for t in re.findall(r"[a-z0-9][a-z0-9-]{3,80}", ln) if t in P]
            ms = money.findall(ln)
            if len(ids) == 1 and len(ms) == 1:
                live = P[ids[0]][0]
                if abs(float(ms[0]) - live) < 1e-9 or abs(round(float(ms[0]), 4) - round(live, 4)) < 1e-9: match += 1
                else: drift += 1; drifts.append({"endpoint": ids[0], "doc_says": float(ms[0]), "catalog_today": live, "file": os.path.relpath(f, d), "line": ln.strip()[:160]})
    out[r] = {"commit": sha, "endpoints_in_code": sorted(used), "n_endpoints": len(used), "looks_like_endpoint_id_but_not_in_catalog": sorted(unknown), "unit_result": [e for e in used if P[e][1] != "call"],
              "price_lines_matching_today": match, "price_lines_differing": drift, "differences": drifts,
              "cheapest_endpoint_usd": min((P[e][0] for e in used), default=None), "dearest_endpoint_usd": max((P[e][0] for e in used), default=None),
              "all_endpoints_one_call_each_usd": round(sum(P[e][0] for e in used), 5)}
json.dump({"read_on": datetime.date.today().isoformat(), "repos": out}, open("data/repos.json", "w"), indent=1)
for r, v in out.items():
    print(f'{r:18s} {v["commit"][:7]} endpoints {v["n_endpoints"]:2d}  price lines ok {v["price_lines_matching_today"]:3d} differ {v["price_lines_differing"]:2d}  one call each ${v["all_endpoints_one_call_each_usd"]}')
