#!/usr/bin/env python3
"""Write map.html (one self-contained page, data embedded, no network) from data/catalog-slim-*.json, data/overview-full-*.json, data/summary.json."""
import json, glob, collections
cat = json.load(open(sorted(glob.glob("data/catalog-slim-*.json"))[-1]))
ov = json.load(open(sorted(glob.glob("data/overview-full-*.json"))[-1]))
S = json.load(open("data/summary.json"))
ctitle = {c["id"]: c["title"] for c in ov["categories"]}
jtitle = {j["id"]: j["title"] for c in ov["categories"] for j in c["jobs"]}
jcat = {j["id"]: c["id"] for c in ov["categories"] for j in c["jobs"]}
jobs = collections.defaultdict(list)
for e in cat["items"]:
    for c in e["caps"]:
        jobs[c.replace("_", ".")].append([e["provider"], e["op"], e["micros"], e["unit"], e["priceSet"]])
J = [{"id": k, "t": jtitle.get(k, k), "c": jcat.get(k, "other"), "e": sorted(v, key=lambda x: x[2])} for k, v in jobs.items()]
# treemap data: category -> provider -> endpoints
tm = collections.defaultdict(collections.Counter)
for e in cat["items"]:
    tm[(e["cats"] or ["other"])[0]][e["provider"]] += 1
TM = [{"c": c, "t": ctitle.get(c, c), "p": dict(v)} for c, v in tm.items()]
D = {"readOn": S["read_on"], "revision": S["revision"], "endpoints": S["endpoints"], "providers": S["providers"], "jobs": J, "tm": TM, "ctitle": ctitle}
page = open("scripts/map_template.html").read().replace("/*DATA*/null", json.dumps(D, separators=(",", ":")))
open("map.html", "w").write(page)
print(len(page) // 1024, "KB")
