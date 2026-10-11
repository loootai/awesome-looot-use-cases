#!/usr/bin/env python3
"""Write image.html from data/prices-per-1000.csv and data/ip-samples-*.json. Bars use a log scale."""
import csv, json, glob, math, html
P = list(csv.DictReader(open("data/prices-per-1000.csv")))
IP = json.load(open(sorted(glob.glob("data/ip-samples-*.json"))[-1]))
lo, hi = 0.02, 400.0
bars = ""
for r in P:
    v = float(r["usd_per_1000"])
    w = 0 if v == 0 else max(2, 100 * (math.log10(v) - math.log10(lo)) / (math.log10(hi) - math.log10(lo)))
    cls = "pdl" if r["kind"] == "company profile" else ("lo" if r["who"] == "looot" else "mid")
    lab = "$0" if v == 0 else (f"${v:,.0f}" if v >= 10 else f"${v:.3g}")
    bars += f'<div class="r"><div class="l"><b>{r["who"]}</b> {html.escape(r["product"])}</div><div class="tr"><div class="b {cls}" style="width:{w:.1f}%"></div></div><div class="v">{lab}</div></div>'
ips = ""
for o in IP["ips"]:
    ips += f'<tr><td class="ip">{o["ip"]}</td><td>{html.escape(o["role_my_label"])}</td><td>{html.escape(o["ipapi_is_company"] or "")}</td><td>{html.escape((o["ipinfo_org"] or "").split(" ",1)[-1])}</td></tr>'
page = f'''<!doctype html><meta charset="utf-8"><title>IP to company</title>
<style>:root{{--ink:#0B2E22;--deep:#0B4A35;--green:#12A06A;--paper:#F7F8F5}}
*{{box-sizing:border-box}}body{{margin:0;width:1600px;height:900px;background:var(--paper);color:var(--ink);font-family:Inter,-apple-system,"Helvetica Neue",Arial,sans-serif;padding:40px 64px;position:relative}}
h1{{font-size:38px;margin:0 0 6px;color:var(--deep);letter-spacing:-.5px}}.sub{{font-size:18px;color:#35574a;margin:0 0 20px;max-width:1450px}}
.cols{{display:grid;grid-template-columns:720px 1fr;gap:40px}}h2{{font-size:17px;margin:0 0 8px;color:var(--deep)}}
.r{{display:grid;grid-template-columns:262px 1fr 62px;gap:10px;align-items:center;height:42px}}.l{{font-size:15px;line-height:1.15}}.l b{{display:block}}
.tr{{background:#e8ece6;height:20px;border-radius:3px}}.b{{height:100%;border-radius:3px}}.b.mid{{background:var(--deep)}}.b.lo{{background:var(--green)}}.b.pdl{{background:var(--ink)}}.v{{text-align:right;font-weight:700;font-size:18px}}
table{{border-collapse:collapse;width:100%;font-size:14px}}th{{text-align:left;font-size:12px;color:#4d6b5f;padding:5px 6px;border-bottom:2px solid #dfe5dc}}td{{padding:6px;border-bottom:1px solid #dfe5dc;vertical-align:top}}td.ip{{font-family:ui-monospace,Menlo,monospace;font-size:13px}}
.note{{font-size:14px;color:#35574a;margin:6px 0 0;line-height:1.4}}
.foot{{position:absolute;left:64px;right:64px;bottom:24px;font-size:13px;color:#4d6b5f;display:flex;justify-content:space-between;align-items:flex-end;gap:36px}}.foot p{{margin:0;max-width:1350px;line-height:1.4}}img{{height:38px}}</style>
<h1>IP lookups return a network owner for $0.03 to $2 per 1,000. A company profile is $280.</h1>
<p class="sub">Left, price per 1,000 lookups from each vendor's own pricing page and looot's catalog, read 2026-10-11, log scale. Right, what two free services returned for 14 well-known public IPs. Nothing here identifies a visitor.</p>
<div class="cols"><div><h2>Price per 1,000 lookups (PDL is per 1,000 matches)</h2>{bars}</div>
<div><h2>Company or organisation returned for 14 infrastructure IPs</h2><table><tr><th>IP</th><th>What I know it is</th><th>ipapi.is company</th><th>ipinfo.io org</th></tr>{ips}</table>
<p class="note">Both services return the owner of the network block. For cloud, CDN and ISP addresses that is the provider, not whoever is using the connection. The two agree on the organisation for 13 of 14. On 1.1.1.1 one says APNIC, the other Cloudflare.</p></div></div>
<div class="foot"><p>looot made this and sells IPinfo and People Data Labs lookups. Cheap rows return an owner or location, PDL returns a company profile, so they are different products. Plan tiers, free allowances and which plan carries the company field are in the README. Data and steps: github.com/loootai/awesome-looot-use-cases</p><img src="wordmark.svg" alt="looot"></div>
'''
open("image.html", "w").write(page)
