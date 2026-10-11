#!/usr/bin/env python3
"""Price per 1,000 lookups. Vendor rows come from data/vendor-prices.csv (typed from the saved page excerpts). looot rows are read live from the public catalog.
Writes data/looot-prices-<date>.json, data/prices-per-1000.csv and data/summary.json. Run from this folder: python3 -I scripts/analyze.py"""
import csv, json, urllib.request, datetime
T = datetime.date.today().isoformat()
G = lambda u: json.load(urllib.request.urlopen(urllib.request.Request("https://api.looot.ai" + u, headers={"User-Agent": "curl/8"}), timeout=60))
L = {}
for e in ("ipinfo-lite", "ipinfo--2", "people-data-labs-ip-enrich"):
    d = G("/v1/public-catalog/" + e); p = d["price"]
    L[e] = {"usd": p["amountMicros"] / 1e6, "unit": p["unit"], "price_set": p["effectiveAt"][:10], "verification": d["verification"]["state"], "read_on": T}
json.dump(L, open(f"data/looot-prices-{T}.json", "w"), indent=1)
rows = []
for r in csv.DictReader(open("data/vendor-prices.csv")):
    rows.append({"who": r["vendor"], "product": r["product"], "usd_per_1000": float(r["usd"]) / float(r["per_n_lookups"]) * 1000, "kind": "network owner or location", "source": r["source_file"], "note": r["note"]})
rows.append({"who": "looot", "product": "ipinfo-lite (free)", "usd_per_1000": L["ipinfo-lite"]["usd"] * 1000, "kind": "network owner or location", "source": "catalog", "note": "country and ASN name only"})
rows.append({"who": "looot", "product": "ipinfo--2 (IPinfo)", "usd_per_1000": L["ipinfo--2"]["usd"] * 1000, "kind": "network owner or location", "source": "catalog", "note": "city, region, country; ASN, company and privacy fields depend on the IPinfo plan, not tested"})
rows.append({"who": "looot", "product": "people-data-labs-ip-enrich (PDL)", "usd_per_1000": L["people-data-labs-ip-enrich"]["usd"] * 1000, "kind": "company profile", "source": "catalog", "note": "charged only on a match, per 1,000 matches"})
rows.sort(key=lambda r: r["usd_per_1000"])
with open("data/prices-per-1000.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)
org = [r for r in rows if r["kind"] == "network owner or location" and r["usd_per_1000"] > 0 and "Country" not in r["product"]]
pdl = [r for r in rows if r["kind"] == "company profile"][0]
S = {"read_on": T, "owner_lookup_min": min(r["usd_per_1000"] for r in org), "owner_lookup_max": max(r["usd_per_1000"] for r in org),
     "pdl_per_1000_matches": pdl["usd_per_1000"], "pdl_over_cheapest_owner": round(pdl["usd_per_1000"] / min(r["usd_per_1000"] for r in org)),
     "pdl_over_looot_ipinfo": round(pdl["usd_per_1000"] / L["ipinfo--2"]["usd"] / 1000)}
json.dump(S, open("data/summary.json", "w"), indent=1)
for r in rows: print(f'{r["usd_per_1000"]:9.3f}  {r["who"]:18s} {r["product"]}')
print(S)
