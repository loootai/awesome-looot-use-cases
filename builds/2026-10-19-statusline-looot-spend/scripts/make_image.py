#!/usr/bin/env python3
"""Write image.html from data/test-results.json (the lines are what the script printed; the balance is masked as $NN.NN)."""
import json, html
R = json.load(open("data/test-results.json"))
L = [("first call, no cache yet", R["cold_first_call"][0]), ("same session, 4 s later", R["after_refresh"][0]),
     ("LOOOT_STATUS_HIDE_BALANCE=1", R["hide_balance"][0]),
     ("spend since 2026-10-09, 37 real runs", R["since_test"]["script_printed"]), ("API unreachable", R["api_unreachable"][0]), ("no LOOOT_TOKEN", R["no_token"][0])]
lines = "".join(f'<div class="ln"><span class="c">{html.escape(a)}</span><span class="o">{html.escape(b)}</span></div>' for a, b in L)
st = R["since_test"]
page = f'''<!doctype html><meta charset="utf-8"><title>looot status line</title>
<style>:root{{--ink:#0B2E22;--deep:#0B4A35;--green:#12A06A;--paper:#F7F8F5}}
*{{box-sizing:border-box}}body{{margin:0;width:1600px;height:900px;background:var(--paper);color:var(--ink);font-family:Inter,-apple-system,"Helvetica Neue",Arial,sans-serif;padding:48px 72px;position:relative}}
h1{{font-size:42px;margin:0 0 8px;color:var(--deep);letter-spacing:-.5px}}.sub{{font-size:20px;color:#35574a;margin:0 0 28px;max-width:1450px;line-height:1.4}}
.cols{{display:grid;grid-template-columns:900px 1fr;gap:44px}}h2{{font-size:18px;margin:0 0 10px;color:var(--deep)}}
.term{{background:var(--ink);border-radius:8px;padding:18px 22px;font:23px/1 ui-monospace,Menlo,monospace}}.ln{{display:grid;grid-template-columns:330px 1fr;gap:16px;padding:26px 0;border-bottom:1px solid #1d4a39}}.ln:last-child{{border:0}}.c{{color:#8fb5a4;font-size:16px;font-family:Inter,Arial,sans-serif;align-self:center}}.o{{color:#e6f2ec}}
.stat{{background:#fff;border:1px solid #dfe5dc;border-radius:6px;padding:14px 18px;margin-bottom:14px}}.stat b{{display:block;font-size:34px;color:var(--deep)}}.stat span{{font-size:16px;color:#4d6b5f}}
.foot{{position:absolute;left:72px;right:72px;bottom:28px;font-size:15px;color:#4d6b5f;display:flex;justify-content:space-between;align-items:flex-end;gap:36px}}.foot p{{margin:0;max-width:1300px;line-height:1.4}}img{{height:40px}}</style>
<h1>A Claude Code status line that shows what looot has spent this session</h1>
<p class="sub">It prints from a cache in about {int(R["cached_call_ms"]["median"])} ms and refreshes in the background with two free reads, GET /v1/balance and GET /v1/runs. Real output below from {R["meta"]["date"]}. No looot run was made.</p>
<div class="cols"><div><h2>What the script printed</h2><div class="term">{lines}</div></div>
<div><div class="stat"><b>{int(R["cached_call_ms"]["median"])} ms</b><span>median time to print from cache, {R["cached_call_ms"]["n"]} calls, max {int(R["cached_call_ms"]["max"])} ms</span></div>
<div class="stat"><b>{R["refresh_ms_measured_by_script"] / 1000:.1f} s</b><span>one background refresh, balance plus run list</span></div>
<div class="stat"><b>${st["independent_sum_usd"]:.4f}, {st["independent_runs"]} runs</b><span>an independent sum from looot runs list --limit 50 over the same window. The script printed ${st["script_state"]["spend"]:.4f}, {st["script_state"]["runs"]} runs</span></div></div></div>
<div class="foot"><p>looot made this. The balance is masked as $NN.NN here. The session total counts runs created after the script first saw the session, from any tool using the same workspace. Script and tests: github.com/loootai/awesome-looot-use-cases</p><img src="wordmark.svg" alt="looot"></div>
'''
open("image.html", "w").write(page)
