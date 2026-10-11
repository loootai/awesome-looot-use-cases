#!/usr/bin/env python3
"""Print every provider and its price for a task, from looot's free public catalog.

Usage: looot_price.py "find a work email" [--limit 25] [--all] [--json]

The best-matching job gets a full table. Other matches get one line each, or a full table with --all.

It sends one GET to https://api.looot.ai/v1/public-catalog. It needs no token, runs no
endpoint and spends nothing. Standard library only."""
import json, sys, urllib.parse, urllib.request

BASE = "https://api.looot.ai/v1/public-catalog"


def fetch(task, limit):
    url = BASE + "?" + urllib.parse.urlencode({"q": task, "limit": limit})
    req = urllib.request.Request(url, headers={"user-agent": "looot-price/1", "accept": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def money(micros):
    return f"${micros / 1e6:.6f}".rstrip("0").rstrip(".")


def main(argv):
    limit, as_json, show_all, words = 25, False, False, []
    it = iter(argv)
    for a in it:
        if a == "--limit":
            limit = int(next(it))
        elif a == "--all":
            show_all = True
        elif a == "--json":
            as_json = True
        else:
            words.append(a)
    task = " ".join(words).strip()
    if not task:
        print('Usage: looot_price.py "what you want done" [--limit N] [--all] [--json]')
        return 2
    try:
        data = fetch(task, limit)
    except Exception as e:  # network, DNS, HTTP error
        print(f"Could not read the looot catalog: {e}")
        return 1
    items = data.get("items", [])
    if as_json:
        print(json.dumps(items, indent=1))
        return 0
    if not items:
        print(f'No catalog match for "{task}". Try other words, or the job name such as google.serp.organic.')
        return 0
    jobs = {}
    for i in items:  # keep the catalog's ranking: first job seen is the best match
        jobs.setdefault((i.get("capabilities") or ["(no job)"])[0], []).append(i)
    print(f'Task: "{task}". looot public catalog, free read, nothing was run.')
    print(f"{len(items)} endpoints in {len(jobs)} job{'s' if len(jobs) != 1 else ''}, best match first. Prices are looot list prices in USD.\n")
    for n, (job, rows) in enumerate(jobs.items()):
        priced = [r for r in rows if r["price"].get("state") == "known" and r["price"].get("amountMicros") is not None]
        priced.sort(key=lambda r: r["price"]["amountMicros"])
        n_p = len({r['providerId'] for r in rows})
        line = f"Capability {job}: {len(rows)} endpoint{'s' if len(rows) != 1 else ''}, {n_p} provider{'s' if n_p != 1 else ''}"
        if len(priced) > 1 and priced[0]["price"]["amountMicros"] > 0 and priced[0]["price"]["amountMicros"] != priced[-1]["price"]["amountMicros"]:
            lo, hi = priced[0]["price"]["amountMicros"], priced[-1]["price"]["amountMicros"]
            line += f", {money(lo)} to {money(hi)} per call ({hi / lo:.1f}x)"
        print(line)
        if n > 0 and not show_all:
            continue
        print("| Provider | Endpoint | Price | Unit | Verified |")
        print("| --- | --- | --- | --- | --- |")
        unpriced = [r for r in rows if r not in priced]
        for r in priced + unpriced:
            p = r["price"]
            price = money(p["amountMicros"]) if r in priced else "unknown"
            print(f"| {r['providerId']} | {r['operationId']} | {price} | {p.get('unit') or '-'} | {r['verification']['state']} |")
        print()
    print("A price is per call at the listed unit. What a call returns differs by provider, so read the endpoint before you pick on price alone.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
