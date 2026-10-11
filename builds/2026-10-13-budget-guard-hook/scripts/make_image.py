#!/usr/bin/env python3
"""Write image.html from data/test-results.json and data/e2e-claude-p-output.txt. Render with Playwright (see README)."""
import json, html
D = json.load(open("data/test-results.json")); R = D["results"]
e2e = open("data/e2e-claude-p-output.txt").read().strip().split("\n\n")[0:3]
CH = {"deny": ("deny", "#0B2E22", "#F7F8F5"), "ask": ("ask", "#12A06A", "#0B2E22"), "pass (message only)": ("within limit", "#e1efe7", "#0B4A35"),
      "no opinion (exit 0, no output)": ("ignore", "#eef0ea", "#4d6b5f")}
pick = [0, 1, 3, 4, 5, 6, 7, 8, 11, 13]   # rows shown
rows = ""
for i in pick:
    r = R[i]; lab, bg, fg = CH[r["decision"]]
    rows += f'<div class="r"><span class="chip" style="background:{bg};color:{fg}">{lab}</span><span class="c">{html.escape(r["case"])}</span><span class="ms">{r["ms"]} ms</span></div>'
cap = [r["decision"] for r in R if r["case"].startswith("cap test")]
ncap_ok = sum(1 for c in cap if c.startswith("pass")); 
cap_line = f'Session cap $0.005, runs of $0.001: {ncap_ok} pass, then {len(cap) - ncap_ok} denied'
page = f'''<!doctype html><meta charset="utf-8"><title>budget guard</title>
<style>:root{{--ink:#0B2E22;--deep:#0B4A35;--green:#12A06A;--paper:#F7F8F5}}
*{{box-sizing:border-box}}body{{margin:0;width:1600px;height:900px;background:var(--paper);color:var(--ink);font-family:Inter,-apple-system,"Helvetica Neue",Arial,sans-serif;padding:48px 72px;position:relative}}
h1{{font-size:42px;margin:0 0 8px;color:var(--deep);letter-spacing:-.5px}}.sub{{font-size:20px;color:#35574a;margin:0 0 26px;max-width:1400px}}
.grid{{display:grid;grid-template-columns:780px 1fr;gap:36px}}
.r{{display:grid;grid-template-columns:132px 1fr 84px;align-items:center;gap:12px;height:50px;border-bottom:1px solid #dfe5dc;font-size:19px}}
.chip{{font-size:15px;font-weight:700;text-align:center;border-radius:4px;padding:5px 0}}.ms{{text-align:right;color:#4d6b5f;font-size:16px}}
.note{{font-size:17px;color:#35574a;margin-top:14px}}
pre{{background:var(--ink);color:#e6f2ec;font:16px/1.45 ui-monospace,Menlo,monospace;padding:22px 26px;border-radius:8px;margin:0;white-space:pre-wrap;height:560px;overflow:hidden}}
.cmd{{color:var(--green)}}h2{{font-size:20px;margin:0 0 10px;color:var(--deep)}}
.foot{{position:absolute;left:72px;right:72px;bottom:28px;font-size:15px;color:#4d6b5f;display:flex;justify-content:space-between;align-items:center}}img{{height:40px}}</style>
<h1>A price limit for looot runs, checked before the run</h1>
<p class="sub">A Claude Code PreToolUse hook reads the endpoint's list price from the free catalog and answers deny, ask or stays silent inside the limits. Limits here: $0.01 a call, $0.25 a session. No looot run was made.</p>
<div class="grid"><div><h2>Decision per case, {D["meta"]["date"]}</h2>{rows}<div class="note">{cap_line}.</div></div>
<div><h2>Real claude -p session with the hook installed</h2><pre><span class="cmd">&gt; Run exactly this shell command: looot run serpapi-google --input '{{"q":"test"}}'</span>

{html.escape(chr(10).join(e2e))}</pre></div></div>
<div class="foot"><span>looot made this. Prices are looot list prices read from its public catalog. Hook and tests: github.com/loootai/awesome-looot-use-cases</span><img src="wordmark.svg" alt="looot"></div>
'''
open("image.html", "w").write(page)
