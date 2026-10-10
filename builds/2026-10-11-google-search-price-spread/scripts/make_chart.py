#!/usr/bin/env python3
"""Write chart.html from summary.json. Render with headless Chrome (see README)."""
import json
S=json.load(open("summary.json")); P=S["providers"]; mx=max(p["max"] for p in P)
rows=""
for k,p in enumerate(P):
    w=max(p["min"]/mx*100,1.0); cls="lo" if k==0 else ("hi" if k==len(P)-1 else "mid")
    mult=p["min"]/P[0]["min"]; lab=f'x{mult:.1f}' if k else "cheapest"
    ep=f'{p["endpoints"]} endpoints' if p["endpoints"]>1 else "1 endpoint"
    rows+=f'<div class="row"><div class="lab"><b>{p["provider"]}</b><span>{ep}, price set {p["price_effective"]}</span></div><div class="track"><div class="bar {cls}" style="width:{w:.1f}%"></div></div><div class="val">${p["min"]:.5g}<small>{lab}</small></div></div>\n'
html=f'''<!doctype html><meta charset="utf-8"><title>Google search price spread</title>
<style>
:root{{--ink:#0B2E22;--deep:#0B4A35;--green:#12A06A;--paper:#F7F8F5}}
*{{box-sizing:border-box}}body{{margin:0;width:1600px;height:900px;background:var(--paper);color:var(--ink);font-family:Inter,-apple-system,"Helvetica Neue",Arial,sans-serif;padding:56px 72px;position:relative}}
h1{{font-size:44px;line-height:1.1;margin:0 0 10px;color:var(--deep);letter-spacing:-.5px}}
.sub{{font-size:21px;margin:0 0 34px;max-width:1350px;color:#35574a}}
.row{{display:grid;grid-template-columns:330px 1fr 190px;align-items:center;gap:20px;height:66px}}
.lab b{{display:block;font-size:24px}}.lab span{{font-size:15px;color:#4d6b5f}}
.track{{background:#e8ece6;height:34px;border-radius:4px}}
.bar{{height:100%;border-radius:4px}}.bar.lo{{background:var(--green)}}.bar.mid{{background:var(--deep)}}.bar.hi{{background:var(--ink)}}
.val{{font-size:26px;font-weight:700;text-align:right}}.val small{{display:block;font-size:15px;font-weight:500;color:#4d6b5f}}
.foot{{position:absolute;left:72px;right:72px;bottom:40px;font-size:15px;color:#4d6b5f;display:flex;justify-content:space-between;align-items:flex-end;gap:40px}}
.foot p{{margin:0;max-width:1180px;line-height:1.45}}img{{height:44px}}
</style>
<h1>One Google search, {S["spread_x"]}x between cheapest and dearest</h1>
<p class="sub">looot list price per call for the job google.serp.organic, {len(P)} providers, {S["endpoints"]} endpoints, read from the free catalog on 2026-10-10 (revision {S["catalog_revision"]}). Nothing was run. A call is not always the same product, see the README.</p>
{rows}
<div class="foot"><p>looot made this comparison from its own catalog. Prices are looot list prices, not each vendor's own pricing page. Providers differ in what one call returns, in rate limits and in plans. Data and steps: github.com/loootai/awesome-looot-use-cases</p><img src="wordmark.svg" alt="looot"></div>
'''
open("chart.html","w").write(html)
