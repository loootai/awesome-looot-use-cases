#!/usr/bin/env python3
"""Read today's looot list price for the endpoints in data/vendors.csv (one free GET each), and the whole catalog price list for calculator.html.
Writes data/looot-prices-<date>.json and data/catalog-prices-<date>.json. No token."""
import csv, json, urllib.request, urllib.parse, datetime
T = datetime.date.today().isoformat()
G = lambda u: json.load(urllib.request.urlopen(urllib.request.Request("https://api.looot.ai" + u, headers={"User-Agent": "curl/8"}), timeout=60))
ids = sorted({r["looot_endpoint"] for r in csv.DictReader(open("data/vendors.csv"))})
out = {}
for i in ids:
    d = G("/v1/public-catalog/" + urllib.parse.quote(i, safe=""))
    p = d["price"]
    out[i] = {"provider": d["providerId"], "usd": p["amountMicros"] / 1e6, "unit": p["unit"], "price_set": p["effectiveAt"][:10],
              "verification": d["verification"]["state"], "read_on": T}
json.dump(out, open(f"data/looot-prices-{T}.json", "w"), indent=1)
items, cur = [], None
while True:
    d = G("/v1/public-catalog?limit=50" + (("&cursor=" + urllib.parse.quote(cur)) if cur else ""))
    items += d["items"]; cur = d.get("nextCursor")
    if not cur: break
json.dump({"read_on": T, "n": len(items), "prices": {i["operationId"]: [i["providerId"], i["price"]["amountMicros"], i["price"]["unit"]] for i in items}},
          open(f"data/catalog-prices-{T}.json", "w"), separators=(",", ":"))
print(json.dumps(out, indent=1), len(items))
