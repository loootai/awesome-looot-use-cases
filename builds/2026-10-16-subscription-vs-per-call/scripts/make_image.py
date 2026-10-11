#!/usr/bin/env python3
"""Write image.html: a table of looot cost against the vendor's own cheapest covering plan, at 8 monthly volumes. Reads data/results.csv, data/vendors.csv, data/looot-prices-*.json."""
import csv, json, glob
R = list(csv.DictReader(open("data/results.csv"))); L = json.load(open(sorted(glob.glob("data/looot-prices-*.json"))[-1]))
V = list(csv.DictReader(open("data/vendors.csv")))
NAMES = {"serper": "Serper", "serpapi": "SerpApi", "hunter": "Hunter", "firecrawl": "Firecrawl", "tavily": "Tavily"}
WHAT = {"serper": "Google search", "serpapi": "Google search", "hunter": "email finder", "firecrawl": "page scrape", "tavily": "web search"}
EP = {}
for r in V: EP[r["vendor"]] = r["looot_endpoint"]
cols = [100, 500, 1000, 2000, 5000, 10000, 25000, 100000]
fmt = lambda x: f"${x:,.0f}" if x >= 100 else (f"${x:,.2f}" if x >= 1 else f"${x:.2f}")
head = "".join(f"<th>{c:,}</th>" for c in cols)
body = ""
for v in EP:
    p = L[EP[v]]["usd"]
    cells = ""
    for c in cols:
        r = [x for x in R if x["vendor"] == v and int(x["calls_per_month"]) == c]
        if not r:
            r = [x for x in R if x["vendor"] == v and int(x["calls_per_month"]) == c] or [{"looot_usd": str(c * p), "direct_usd": ""}]
        lo = c * p; d = r[0]["direct_usd"]
        if d == "": cells += f'<td class="n"><b>{fmt(lo)}</b><i>no listed plan</i></td>'; continue
        d = float(d)
        cls = "free" if d == 0 else ("lo" if lo < d - 1e-9 else ("eq" if abs(lo - d) < 1e-9 else "hi"))
        cells += f'<td class="{cls}"><b>{fmt(lo)}</b><i>{"free tier" if d == 0 else "direct " + fmt(d)}</i></td>'
    body += f'<tr><th class="v">{NAMES[v]}<small>{WHAT[v]}, looot ${p:g} a call</small></th>{cells}</tr>'
page = f'''<!doctype html><meta charset="utf-8"><title>subscription vs per call</title>
<style>:root{{--ink:#0B2E22;--deep:#0B4A35;--green:#12A06A;--paper:#F7F8F5}}
*{{box-sizing:border-box}}body{{margin:0;width:1600px;height:900px;background:var(--paper);color:var(--ink);font-family:Inter,-apple-system,"Helvetica Neue",Arial,sans-serif;padding:44px 72px;position:relative}}
h1{{font-size:40px;margin:0 0 8px;color:var(--deep);letter-spacing:-.5px}}.sub{{font-size:19px;color:#35574a;margin:0 0 22px;max-width:1450px}}
table{{border-collapse:separate;border-spacing:6px;width:100%}}th{{font-size:16px;color:#4d6b5f;font-weight:600;padding:4px}}
th.v{{text-align:left;font-size:24px;color:var(--ink);width:290px}}th.v small{{display:block;font-size:14px;color:#4d6b5f;font-weight:400}}
td{{text-align:center;padding:12px 4px;border-radius:5px;height:92px;vertical-align:middle}}td b{{display:block;font-size:26px}}td i{{display:block;font-style:normal;font-size:15px;margin-top:3px}}
td.lo{{background:#cfeadb;color:var(--deep)}}td.hi{{background:var(--ink);color:#F7F8F5}}td.eq{{background:#e8ece6}}td.free{{background:#fff;border:2px solid var(--green);color:var(--deep)}}td.n{{background:#e8ece6;color:#4d6b5f}}
.key{{display:flex;gap:22px;font-size:16px;margin:12px 0 0;color:#35574a}}.key span::before{{content:"";display:inline-block;width:16px;height:16px;border-radius:3px;margin-right:7px;vertical-align:-3px}}
.k1::before{{background:#cfeadb}}.k2::before{{background:var(--ink)}}.k3::before{{background:#fff;border:2px solid var(--green)}}.k4::before{{background:#e8ece6}}
.foot{{position:absolute;left:72px;right:72px;bottom:26px;font-size:14px;color:#4d6b5f;display:flex;justify-content:space-between;align-items:flex-end;gap:40px}}.foot p{{margin:0;max-width:1300px;line-height:1.45}}img{{height:40px}}</style>
<h1>looot's list price against each vendor's own plan, by calls a month</h1>
<p class="sub">Big number is what N calls cost at looot's per-call list price. Small number is the vendor's cheapest listed plan that covers N. Vendor prices read from their pricing pages on 2026-10-11, looot prices from its catalog the same day.</p>
<table><tr><th></th>{head}</tr>{body}</table>
<div class="key"><span class="k1">looot cheaper</span><span class="k2">vendor plan cheaper</span><span class="k3">vendor free tier covers it</span><span class="k4">same price, or no listed plan covers N</span></div>
<div class="foot"><p>looot made this comparison and sells these providers. Plans bundle other features that this table ignores. Serper sells 6-month credit packs, shown as pack price / 6 for N a month. Firecrawl prices are per month billed yearly. Assumes every call returns a billable result. Sources and steps: github.com/loootai/awesome-looot-use-cases</p><img src="wordmark.svg" alt="looot"></div>
'''
open("image.html", "w").write(page)
