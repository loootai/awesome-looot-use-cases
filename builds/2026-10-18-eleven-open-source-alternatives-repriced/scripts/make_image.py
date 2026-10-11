#!/usr/bin/env python3
"""Write image.html from data/repos.json (check_repos.py) and data/vendor-prices.csv (typed by hand from the saved page excerpts)."""
import csv, json, html
V = list(csv.DictReader(open("data/vendor-prices.csv")))
D = json.load(open("data/repos.json"))["repos"]
ok = sum(v["price_lines_matching_today"] for v in D.values()); bad = sum(v["price_lines_differing"] for v in D.values())
uniq = len({e for v in D.values() for e in v["endpoints_in_code"]})
rows = ""
for r in V:
    d = D[r["repo"]]; rd = r["vendor_public_price_read_2026-10-11"]
    cls = "nr" if rd.startswith(("not", "no price")) else ""
    rows += f'<tr><td class="rp">{r["repo"]}<small>{d["n_endpoints"]} endpoints, {d["price_lines_matching_today"]} price lines match</small></td><td>{html.escape(r["replaces"])}</td><td class="{cls}">{html.escape(rd)}</td><td>{html.escape(r["repo_typical_run_per_its_readme"])}</td></tr>'
page = f'''<!doctype html><meta charset="utf-8"><title>eleven alternatives re-priced</title>
<style>:root{{--ink:#0B2E22;--deep:#0B4A35;--green:#12A06A;--paper:#F7F8F5}}
*{{box-sizing:border-box}}body{{margin:0;width:1600px;height:900px;background:var(--paper);color:var(--ink);font-family:Inter,-apple-system,"Helvetica Neue",Arial,sans-serif;padding:36px 64px;position:relative;overflow:hidden}}
h1{{font-size:36px;margin:0 0 6px;color:var(--deep);letter-spacing:-.5px}}.sub{{font-size:17px;color:#35574a;margin:0 0 12px;max-width:1450px;line-height:1.35}}
table{{border-collapse:collapse;width:100%;font-size:15px}}th{{text-align:left;font-size:12px;color:#4d6b5f;padding:5px 8px;border-bottom:2px solid #dfe5dc;text-transform:uppercase;letter-spacing:.04em}}
td{{padding:6px 8px;border-bottom:1px solid #dfe5dc;vertical-align:top;line-height:1.2}}td.rp{{font-weight:700;color:var(--deep);white-space:nowrap}}td.rp small{{display:block;font-weight:400;color:#4d6b5f;font-size:11.5px}}td.nr{{color:#7a8f86;font-style:italic}}
.foot{{position:absolute;left:64px;right:64px;bottom:18px;font-size:12.5px;color:#4d6b5f;display:flex;justify-content:space-between;align-items:flex-end;gap:36px}}.foot p{{margin:0;max-width:1350px;line-height:1.4}}img{{height:36px}}</style>
<h1>Eleven open-source alternatives, checked against today's catalog and vendor pages</h1>
<p class="sub">The code references {uniq} distinct looot endpoint ids. None points at an endpoint missing from today's catalog. {ok} of {ok + bad} price lines in the READMEs match its prices. The other {bad} quote a per-run total. Vendor prices come from the vendors' own pages, read 2026-10-11. No paid looot run has been made for any repo.</p>
<table><tr><th>Repo</th><th>Replaces</th><th>Vendor's own public price</th><th>Typical run, from the repo's README</th></tr>{rows}</table>
<div class="foot"><p>looot made these repos and this check. A repo is not the same product as the paid tool: the vendors have their own data, support and a hosted app. Prices are list prices and every endpoint is marked unverified. Steps: github.com/loootai/awesome-looot-use-cases</p><img src="wordmark.svg" alt="looot"></div>
'''
open("image.html", "w").write(page)
