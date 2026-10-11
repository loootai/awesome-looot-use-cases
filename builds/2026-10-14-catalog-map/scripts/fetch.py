#!/usr/bin/env python3
"""Download the whole public catalog (52 pages of 50) and the job overview, keep only the fields the analysis needs.
Writes data/catalog-slim-<date>.json and data/overview-full-<date>.json. No token. Run from this folder."""
import json, urllib.request, urllib.parse, datetime
T = datetime.date.today().isoformat()
G = lambda u: json.load(urllib.request.urlopen(urllib.request.Request("https://api.looot.ai" + u, headers={"User-Agent": "curl/8"}), timeout=60))
items, cur, pages = [], None, 0
while True:
    d = G("/v1/public-catalog?limit=50" + (("&cursor=" + urllib.parse.quote(cur)) if cur else ""))
    items += d["items"]; pages += 1; cur = d.get("nextCursor")
    if not cur: break
slim = [{"op": i["operationId"], "provider": i["providerId"], "caps": i["capabilities"], "cats": i["categories"],
         "micros": i["price"]["amountMicros"], "unit": i["price"]["unit"], "priceSet": i["price"]["effectiveAt"][:10],
         "verification": i["verification"]["state"]} for i in items]
ov = G("/v1/catalog/overview?depth=full")
json.dump({"readOn": T, "pages": pages, "catalogDigest": d.get("catalogDigest"), "items": slim}, open(f"data/catalog-slim-{T}.json", "w"))
json.dump(ov, open(f"data/overview-full-{T}.json", "w"))
print(len(slim), "endpoints,", pages, "pages, revision", ov["revision"])
