#!/usr/bin/env python3
"""Monthly cost of N calls: the vendor's own cheapest listed plan that covers N, against N x looot's list price.
Reads data/vendors.csv (typed from each vendor's pricing page, 2026-10-11) and data/looot-prices-*.json (read from the catalog the same day).
Rules, applied as written:
  monthly plans (serpapi, hunter, firecrawl): the cheapest plan whose monthly allowance covers N. Free plan counts up to its allowance.
  serper sells packs of credits valid 6 months: I assume you use N a month for 6 months and must buy the smallest pack that covers 6N, so the monthly cost is pack price / 6. Unused credits are lost.
  tavily: free 1,000 credits a month, above that pay as you go at the listed price per credit.
  Every call is assumed to return a billable result. The vendors' own plans bundle other features that this ignores.
Writes data/results.csv, data/summary.json."""
import csv, json, glob
V = list(csv.DictReader(open("data/vendors.csv")))
L = json.load(open(sorted(glob.glob("data/looot-prices-*.json"))[-1]))
GRID = [100, 500, 1000, 2000, 5000, 10000, 25000, 50000, 100000, 300000]
def direct(vendor, n):
    P = [r for r in V if r["vendor"] == vendor]
    if vendor == "tavily":
        return 0.0 if n <= 1000 else n * float([r for r in P if r["plan"] == "Pay as you go"][0]["price_usd"])
    if vendor == "serper":
        packs = [r for r in P if "pack" in r["billing"]]
        for r in sorted(packs, key=lambda r: float(r["price_usd"])):
            if float(r["included_units"]) >= 6 * n:
                return float(r["price_usd"]) / 6
        return None
    for r in sorted(P, key=lambda r: float(r["price_usd"])):
        if float(r["included_units"]) >= n:
            return float(r["price_usd"])
    return None
vendors = []
for r in V:
    if r["vendor"] not in [x[0] for x in vendors]:
        vendors.append((r["vendor"], r["looot_endpoint"]))
rows, summ = [], {}
for v, ep in vendors:
    p = L[ep]["usd"]
    seg, prev = [], None
    for n in range(1, 300001):
        d = direct(v, n); lo = n * p
        s = "beyond listed plans" if d is None else ("looot cheaper" if lo < d - 1e-9 else ("same" if abs(lo - d) <= 1e-9 else "direct cheaper"))
        if s != prev:
            seg.append({"from_calls_per_month": n, "result": s}); prev = s
    summ[v] = {"looot_endpoint": ep, "looot_usd_per_call": p, "price_set": L[ep]["price_set"], "segments": seg}
    for n in GRID:
        d = direct(v, n)
        rows.append({"vendor": v, "calls_per_month": n, "looot_usd": round(n * p, 4), "direct_usd": None if d is None else round(d, 4),
                     "looot_minus_direct": None if d is None else round(n * p - d, 4)})
w = csv.DictWriter(open("data/results.csv", "w", newline=""), fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)
json.dump(summ, open("data/summary.json", "w"), indent=1)
for v, s in summ.items():
    print(v, s["looot_usd_per_call"], [(x["from_calls_per_month"], x["result"]) for x in s["segments"]])
