#!/usr/bin/env python3
"""Read the saved public-catalog response for the job google.serp.organic and write
prices.csv, summary.json. No provider is called. Run from the folder root: python3 -I scripts/analyze.py"""
import json, csv, statistics
d = json.load(open("data/public-catalog-capability-google_serp_organic-2026-10-10.json"))
ov = json.load(open("data/catalog-overview-jobs-google.serp.organic-2026-10-10.json"))
rows = []
for i in d["items"]:
    p = i["price"]
    assert p["state"] == "known" and p["unit"] == "call" and p["currency"] == "USD"
    rows.append({"provider": i["providerId"], "endpoint": i["operationId"], "price_usd_per_call": p["amountMicros"]/1e6,
                 "price_effective": p["effectiveAt"][:10], "verification": i["verification"]["state"]})
rows.sort(key=lambda r: (r["price_usd_per_call"], r["provider"], r["endpoint"]))
with open("prices.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
prov = {}
for r in rows:
    prov.setdefault(r["provider"], []).append(r)
P = []
for k, v in prov.items():
    ps = [x["price_usd_per_call"] for x in v]
    P.append({"provider": k, "endpoints": len(v), "min": min(ps), "max": max(ps), "price_effective": max(x["price_effective"] for x in v)})
P.sort(key=lambda p: p["min"])
lo, hi = P[0], P[-1]
allp = [r["price_usd_per_call"] for r in rows]
S = {"catalog_revision": ov["revision"], "catalog_built_at": ov["builtAt"], "endpoints": len(rows), "provider_count": len(P),
     "cheapest": lo, "dearest": hi, "spread_x": round(hi["min"]/lo["min"], 1),
     "median_provider_min": statistics.median(p["min"] for p in P),
     "per_1000_calls_usd": {p["provider"]: round(p["min"]*1000, 2) for p in P},
     "per_10000_calls_usd": {p["provider"]: round(p["min"]*10000, 2) for p in P},
     "providers": P}
json.dump(S, open("summary.json", "w"), indent=1)
print(json.dumps({k: S[k] for k in ("catalog_revision","endpoints","provider_count","spread_x","median_provider_min")}), "\n", *[f'{p["provider"]:15} {p["min"]:.5f} x{p["endpoints"]}\n' for p in P])
