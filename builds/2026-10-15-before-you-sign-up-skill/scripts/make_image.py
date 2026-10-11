#!/usr/bin/env python3
"""Write image.html from data/scores.json and two saved answers (prompt p2, with and without the skill). Excerpts are cut by line count only."""
import json, html
S = json.load(open("data/scores.json"))
n = lambda cond, kind, k: sum(1 for x in S if x["cond"] == cond and x["kind"] == kind and x[k])
tot = lambda kind: sum(1 for x in S if x["cond"] == "with" and x["kind"] == kind)
prompt = [p for p in json.load(open("data/prompts.json")) if p["id"] == "p2"][0]["prompt"]
wo = open("data/answers/without-p2.txt").read().split("\n")
wi = open("data/answers/with-p2.txt").read().split("\n")
cut = lambda L, a, b: html.escape("\n".join(L[a:b]).replace("**", ""))
page = f'''<!doctype html><meta charset="utf-8"><title>before-you-sign-up</title>
<style>:root{{--ink:#0B2E22;--deep:#0B4A35;--green:#12A06A;--paper:#F7F8F5}}
*{{box-sizing:border-box}}body{{margin:0;width:1600px;height:900px;background:var(--paper);color:var(--ink);font-family:Inter,-apple-system,"Helvetica Neue",Arial,sans-serif;padding:44px 72px;position:relative}}
h1{{font-size:40px;margin:0 0 6px;color:var(--deep);letter-spacing:-.5px}}.sub{{font-size:19px;color:#35574a;margin:0 0 18px}}
.stats{{display:flex;gap:18px;margin-bottom:18px}}.st{{background:#fff;border:1px solid #dfe5dc;border-radius:6px;padding:10px 16px;font-size:16px;color:#4d6b5f}}.st b{{display:block;font-size:30px;color:var(--deep)}}
.q{{font:15px ui-monospace,Menlo,monospace;color:var(--deep);margin:0 0 10px}}
.cols{{display:grid;grid-template-columns:1fr 1fr;gap:26px}}h2{{font-size:17px;margin:0 0 8px;color:var(--deep)}}
pre{{background:var(--ink);color:#e6f2ec;font:14.5px/1.4 ui-monospace,Menlo,monospace;padding:16px 20px;border-radius:8px;margin:0;white-space:pre-wrap;height:430px;overflow:hidden}}
.foot{{position:absolute;left:72px;right:72px;bottom:24px;font-size:14px;color:#4d6b5f;display:flex;justify-content:space-between;align-items:center;gap:30px}}img{{height:38px}}</style>
<h1>Claude Code checked a price list before suggesting an account</h1>
<p class="sub">A skill that reads looot's free catalog when a task needs outside data. 8 prompts through claude -p with and without it, 2026-10-11. looot made the skill.</p>
<div class="stats"><div class="st"><b>{n("with","pos","skill_called")} of {tot("pos")}</b>data tasks: skill used, catalog prices shown</div>
<div class="st"><b>{n("without","pos","prices_shown")} of {tot("pos")}</b>same tasks without the skill: catalog prices shown</div>
<div class="st"><b>{n("with","neg","skill_called")} of {tot("neg")}</b>prompts needing no outside data: skill used</div>
<div class="st"><b>{sum(1 for x in S if x["cond"]=="with" and x["kind"]=="pos" and x["names_vendors"])} of {tot("pos")}</b>with the skill, still names providers to sign up with directly</div></div>
<p class="q">&gt; {html.escape(prompt)}</p>
<div class="cols"><div><h2>Without the skill (first lines of the answer)</h2><pre>{cut(wo, 0, 16)}</pre></div>
<div><h2>With the skill (first lines of the answer)</h2><pre>{cut(wi, 0, 15)}</pre></div></div>
<div class="foot"><span>Prices are looot list prices from its public catalog. Small test, 8 prompts. Skill and raw runs: github.com/loootai/awesome-looot-use-cases</span><img src="wordmark.svg" alt="looot"></div>
'''
open("image.html", "w").write(page)
