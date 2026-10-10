#!/usr/bin/env python3
"""Write chart.html from results.json. Render with headless Chrome (see README)."""
import json
R=json.load(open("results.json")); S=R["servers"]; T=R["totals"]
mx=max(r["tokens_est"] or 0 for r in S)
rows=""
for r in sorted(S,key=lambda r:(r["key"]=="looot", -(r["tokens_est"] or -1))):
    cls="looot" if r["key"]=="looot" else "other"
    if r["tokens_est"] is None:
        bar='<div class="nm">not measured: tool list needs a Hunter API key</div>'; val="n/a"; meta=f'{r["config_lines"]} config lines, {r["keys"]} key'
    else:
        w=max(r["tokens_est"]/mx*100,0.8); bar=f'<div class="bar {cls}" style="width:{w:.1f}%"></div>'
        val=f'{r["tokens_est"]:,}'; meta=f'{r["tools"]} tools, {r["config_lines"]} config lines, {r["keys"]} key'
    rows+=f'<div class="row"><div class="lab"><b>{r["label"]}</b><span>{meta}</span></div><div class="track">{bar}</div><div class="val">{val}</div></div>\n'
html=f'''<!doctype html><meta charset="utf-8"><title>Tool-definition size</title>
<style>
:root{{--ink:#0B2E22;--deep:#0B4A35;--green:#12A06A;--paper:#F7F8F5}}
*{{box-sizing:border-box}}body{{margin:0;width:1600px;height:900px;background:var(--paper);color:var(--ink);font-family:Inter,-apple-system,"Helvetica Neue",Arial,sans-serif;padding:56px 72px;position:relative}}
h1{{font-size:44px;line-height:1.1;margin:0 0 10px;color:var(--deep);letter-spacing:-.5px}}
.sub{{font-size:21px;margin:0 0 34px;max-width:1300px;color:#35574a}}
.row{{display:grid;grid-template-columns:330px 1fr 120px;align-items:center;gap:20px;height:62px}}
.lab b{{display:block;font-size:24px}}.lab span{{font-size:15px;color:#4d6b5f}}
.track{{background:#e8ece6;height:34px;border-radius:4px;position:relative}}
.bar{{height:100%;border-radius:4px}}.bar.other{{background:var(--deep)}}.bar.looot{{background:var(--green)}}
.nm{{font-size:16px;color:#4d6b5f;padding:8px 12px;font-style:italic}}
.val{{font-size:26px;font-weight:700;text-align:right}}
.foot{{position:absolute;left:72px;right:72px;bottom:40px;font-size:15px;color:#4d6b5f;display:flex;justify-content:space-between;align-items:flex-end;gap:40px}}
.foot p{{margin:0;max-width:1180px;line-height:1.45}}
img{{height:44px}}
.sum{{font-size:22px;margin:14px 0 0;color:var(--ink)}}
</style>
<h1>Tool definitions the model has to carry</h1>
<p class="sub">Estimated tokens from each server's own tools/list, measured 2026-10-10 (characters of minified JSON / 4). Five of six servers measured: {T["measured_tools"]} tools, about {T["measured_tokens_est"]:,} tokens. looot alone: 17 tools, about {S[-1]["tokens_est"]:,}.</p>
{rows}
<div class="foot"><p>Estimate, not Claude's tokenizer. Exact figures need /context. looot made this comparison and publishes it. The bars say nothing about result quality, and a smaller tool list is not better: Exa's 2 tools do web search and fetch well, Firecrawl has dedicated crawl and monitor tools that looot only reaches through run. Data and steps: github.com/loootai/awesome-looot-use-cases</p><img src="wordmark.svg" alt="looot"></div>
'''
open("chart.html","w").write(html)
