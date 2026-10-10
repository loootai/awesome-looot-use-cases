#!/usr/bin/env python3
"""Render a captured command output (data/sample-claude-code-output-google-search.txt) as image.html.
The text is the real output of `claude -p "/looot-price ..."`, trimmed to the lines shown. Nothing is typed by hand."""
import html
L = open("data/sample-claude-code-output-google-search.txt").read().splitlines()
# drop the table of the other jobs, keep header, the main table, one-line job list head and Claude's closing note
keep = []
for l in L:
    if l.startswith("Capability ") and "google_serp_organic" not in l and len([k for k in keep if k.startswith("Capability ")]) >= 3:
        continue
    keep.append(l)
text = "\n".join(l for l in keep if not l.startswith("| ---"))
body = html.escape(text)
page = f'''<!doctype html><meta charset="utf-8"><title>looot-price</title>
<style>:root{{--ink:#0B2E22;--deep:#0B4A35;--green:#12A06A;--paper:#F7F8F5}}
*{{box-sizing:border-box}}body{{margin:0;width:1600px;height:900px;background:var(--paper);color:var(--ink);font-family:Inter,-apple-system,"Helvetica Neue",Arial,sans-serif;padding:44px 72px;position:relative}}
h1{{font-size:40px;margin:0 0 6px;color:var(--deep);letter-spacing:-.5px}}.sub{{font-size:20px;color:#35574a;margin:0 0 20px}}
pre{{background:var(--ink);color:#e6f2ec;font:15.5px/1.38 ui-monospace,Menlo,monospace;padding:20px 26px;border-radius:8px;margin:0;white-space:pre-wrap;height:640px;overflow:hidden}}
.cmd{{color:var(--green)}}
.foot{{position:absolute;left:72px;right:72px;bottom:28px;font-size:15px;color:#4d6b5f;display:flex;justify-content:space-between;align-items:center}}img{{height:40px}}</style>
<h1>/looot-price: the price of a task, before anything runs</h1>
<p class="sub">Real output from Claude Code, 2026-10-10, with the list of lower-ranked matches trimmed. One free read of the looot catalog. No sign-in, no run, $0 spent.</p>
<pre><span class="cmd">&gt; /looot-price Google search results for a keyword</span>

{body}</pre>
<div class="foot"><span>looot made this. Prices are looot list prices. Command and script: github.com/loootai/awesome-looot-use-cases</span><img src="wordmark.svg" alt="looot"></div>
'''
open("image.html","w").write(page)
