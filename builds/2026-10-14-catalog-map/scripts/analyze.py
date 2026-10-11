#!/usr/bin/env python3
"""Group the slim catalog by job (capability with _ turned into .), find jobs several providers sell, and measure the price spread.
Reads data/catalog-slim-*.json and data/overview-full-*.json (newest). Writes data/summary.json and data/jobs.json."""
import json, glob, collections, statistics
cat = json.load(open(sorted(glob.glob("data/catalog-slim-*.json"))[-1]))
ov = json.load(open(sorted(glob.glob("data/overview-full-*.json"))[-1]))
jobs = {j["id"]: dict(j, category=c["id"]) for c in ov["categories"] for j in c["jobs"]}
byjob = collections.defaultdict(list)
for e in cat["items"]:
    for c in e["caps"]:
        byjob[c.replace("_", ".")].append(e)
rows = []
for jid, es in byjob.items():
    prov = collections.defaultdict(list)
    for e in es:
        if e["unit"] == "call" and e["micros"] > 0:
            prov[e["provider"]].append(e["micros"])
    best = {p: min(v) for p, v in prov.items()}      # cheapest endpoint per provider, per call
    allp = {e["provider"] for e in es}
    r = {"job": jid, "title": jobs.get(jid, {}).get("title", jid), "category": jobs.get(jid, {}).get("category"),
         "endpoints": len(es), "providers": len(allp), "priced_providers": len(best)}
    if len(best) >= 2:
        lo, hi = min(best.values()), max(best.values())
        r.update(min_usd=lo / 1e6, max_usd=hi / 1e6, spread=round(hi / lo, 2),
                 cheapest=min(best, key=best.get), dearest=max(best, key=best.get))
    rows.append(r)
multi = [r for r in rows if r["providers"] >= 2]
spread = [r for r in rows if "spread" in r]
pe = collections.Counter(e["provider"] for e in cat["items"])
tot = len(cat["items"])
cum, top = 0, []
for p, n in pe.most_common():
    cum += n; top.append((p, n, round(100 * cum / tot, 1)))
half = next(i + 1 for i, (_, _, c) in enumerate(top) if c >= 50)
cats = collections.Counter(e["cats"][0] if e["cats"] else "none" for e in cat["items"])
S = {"read_on": cat["readOn"], "revision": ov["revision"], "built_at": ov["builtAt"], "digest": cat["catalogDigest"],
     "endpoints": tot, "providers": len(pe), "jobs_in_overview": len(jobs), "jobs_with_endpoints": len(byjob),
     "unverified_endpoints": sum(1 for e in cat["items"] if e["verification"] == "unverified"),
     "unit_call": sum(1 for e in cat["items"] if e["unit"] == "call"), "unit_result": sum(1 for e in cat["items"] if e["unit"] == "result"),
     "free_endpoints": sum(1 for e in cat["items"] if e["micros"] == 0),
     "jobs_with_2plus_providers": len(multi), "jobs_with_3plus": sum(1 for r in rows if r["providers"] >= 3),
     "jobs_with_5plus": sum(1 for r in rows if r["providers"] >= 5), "jobs_with_one_provider": sum(1 for r in rows if r["providers"] == 1),
     "jobs_with_price_spread": len(spread), "median_spread": statistics.median(r["spread"] for r in spread),
     "spread_ge_2": sum(1 for r in spread if r["spread"] >= 2), "spread_ge_10": sum(1 for r in spread if r["spread"] >= 10),
     "spread_ge_100": sum(1 for r in spread if r["spread"] >= 100),
     "providers_for_half_of_endpoints": half, "top_providers": top[:10],
     "categories": cats.most_common(),
     "most_contested": sorted(multi, key=lambda r: -r["providers"])[:12],
     "widest_spread_5plus": sorted([r for r in spread if r["providers"] >= 5], key=lambda r: -r["spread"])[:12],
     "overview_totals": ov["totals"]}
json.dump(S, open("data/summary.json", "w"), indent=1)
json.dump(rows, open("data/jobs.json", "w"))
for k, v in S.items():
    if k not in ("most_contested", "widest_spread_5plus", "top_providers", "categories", "overview_totals", "digest"):
        print(k, v)
print("top providers", S["top_providers"][:6])
for r in S["widest_spread_5plus"]: print(r["spread"], r["providers"], r["job"], r["min_usd"], r["max_usd"], r["cheapest"], r["dearest"])
print([ (r["job"], r["providers"]) for r in S["most_contested"][:6]])
