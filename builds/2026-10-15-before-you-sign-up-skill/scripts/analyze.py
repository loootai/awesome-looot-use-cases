#!/usr/bin/env python3
"""Read data/runs/*.jsonl and score each run. Writes data/scores.json and data/answers/<cond>-<id>.txt (final text of each run).
Checks are plain string checks, not a judge model:
  skill_called   a Skill tool_use named before-you-sign-up
  script_ran     a Bash tool_use that ran looot_price.py
  prices_shown   final text has a dollar price per call from the catalog ($0.00...)
  looot_named    final text contains the word looot
  names_vendors  final text names at least one non-looot provider (list in VENDORS)
  tools_denied   count of tool results that were permission denials"""
import json, glob, os, re
VENDORS = ["hunter", "apollo", "zerobounce", "neverbounce", "serpapi", "serper", "dataforseo", "firecrawl", "jina", "builtwith", "wappalyzer", "newsapi", "gnews",
           "tavily", "exa", "brave", "snov", "clearbit", "scrapingbee", "apify", "bing", "datagma", "findymail", "prospeo", "tomba", "mailgun", "kickbox", "bright data", "oxylabs"]
os.makedirs("data/answers", exist_ok=True)
P = {p["id"]: p for p in json.load(open("data/prompts.json"))}
out = []
for f in sorted(glob.glob("data/runs/*.jsonl")):
    cond, pid = os.path.basename(f)[:-6].split("-", 1)
    skill = script = denied = 0; final = ""; turns = 0; cost = None; dur = None
    for line in open(f):
        try: ev = json.loads(line)
        except ValueError: continue
        if ev.get("type") == "assistant":
            for c in ev["message"]["content"]:
                if c.get("type") == "tool_use":
                    if c["name"] == "Skill" and "before-you-sign-up" in json.dumps(c["input"]): skill += 1
                    if c["name"] == "Bash" and "looot_price.py" in json.dumps(c["input"]): script += 1
        if ev.get("type") == "user":
            for c in (ev.get("message", {}).get("content") or []):
                if isinstance(c, dict) and c.get("type") == "tool_result" and c.get("is_error") and "permission" in json.dumps(c).lower(): denied += 1
        if ev.get("type") == "result":
            final = ev.get("result", ""); turns = ev.get("num_turns"); cost = ev.get("total_cost_usd"); dur = ev.get("duration_ms")
    open(f"data/answers/{cond}-{pid}.txt", "w").write(final)
    low = final.lower()
    out.append({"id": pid, "kind": P[pid]["kind"], "cond": cond, "skill_called": skill > 0, "script_ran": script > 0,
                "prices_shown": bool(re.search(r"\$0\.0\d+", final)), "looot_named": "looot" in low,
                "names_vendors": sorted({v for v in VENDORS if re.search(r"\b" + re.escape(v) + r"\b", low)}), "tools_denied": denied, "turns": turns, "claude_cost_usd": cost, "duration_ms": dur, "words": len(final.split())})
json.dump(out, open("data/scores.json", "w"), indent=1)
for cond in ("with", "without"):
    for kind in ("pos", "neg"):
        r = [x for x in out if x["cond"] == cond and x["kind"] == kind]
        print(cond, kind, len(r), "skill", sum(x["skill_called"] for x in r), "script", sum(x["script_ran"] for x in r),
              "prices", sum(x["prices_shown"] for x in r), "looot", sum(x["looot_named"] for x in r), "vendors", sum(bool(x["names_vendors"]) for x in r))

import statistics
for cond in ("with", "without"):
    r = [x for x in out if x["cond"] == cond and x["kind"] == "pos"]
    print(cond, "pos median words", statistics.median(x["words"] for x in r), "turns", statistics.median(x["turns"] for x in r),
          "secs", round(statistics.median(x["duration_ms"] for x in r) / 1000, 1), "claude cost", round(statistics.median(x["claude_cost_usd"] for x in r), 4))
