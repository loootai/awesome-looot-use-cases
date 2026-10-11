#!/usr/bin/env python3
"""Look up 14 well-known public infrastructure IPs at two free services and keep the organisation fields. Without a key ipapi.is returns only a company string and an ASN string.
ipapi.is (https://api.ipapi.is/?q=IP, no key) and ipinfo.io (https://ipinfo.io/IP/json, no token). One request per IP per service. No looot call.
The role of each IP (my label) is what I know about the address, not something either service says.
Writes data/ip-samples-<date>.json. Run from this folder: python3 -I scripts/sample_ips.py"""
import json, urllib.request, datetime, time
T = datetime.date.today().isoformat()
IPS = [("8.8.8.8", "public DNS resolver, Google"), ("1.1.1.1", "public DNS resolver, Cloudflare"), ("9.9.9.9", "public DNS resolver, Quad9"),
       ("75.75.75.75", "ISP DNS resolver, Comcast"), ("208.67.222.222", "public DNS resolver, OpenDNS"),
       ("140.82.112.3", "github.com web server"), ("17.253.144.10", "apple.com web server, inside Apple's own range"),
       ("18.9.22.69", "inside MIT's own range"), ("13.107.42.14", "Microsoft web server"), ("157.240.1.35", "facebook.com web server"),
       ("3.5.140.2", "AWS S3, cloud hosting"), ("52.95.110.1", "AWS, cloud hosting"), ("104.16.132.229", "Cloudflare CDN edge"), ("142.250.80.46", "Google web server")]
G = lambda u: json.load(urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "curl/8"}), timeout=30))
out = []
for ip, role in IPS:
    a = G("https://api.ipapi.is/?q=" + ip); i = G("https://ipinfo.io/" + ip + "/json")
    out.append({"ip": ip, "role_my_label": role,
                "ipapi_is_company": a.get("company"), "ipapi_is_asn": a.get("asn"),
                "ipinfo_org": i.get("org"), "ipinfo_hostname": i.get("hostname")})
    time.sleep(0.5)
json.dump({"read_on": T, "ips": out}, open(f"data/ip-samples-{T}.json", "w"), indent=1)
for o in out:
    print(o["ip"], "|", o["ipapi_is_company"], "|", o["ipapi_is_asn"], "|", o["ipinfo_org"])
