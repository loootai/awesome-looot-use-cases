#!/usr/bin/env python3
"""Fetch tools/list from a remote MCP server (Streamable HTTP) and save the raw JSON.
Usage: mcp_tools_list.py <url> <out.json> [header=value ...]
No credentials are sent unless you pass a header. Standard library only."""
import json, sys, urllib.request

def post(url, body, headers, sid=None):
    h = {"user-agent": "curl/8.7.1", "content-type": "application/json", "accept": "application/json, text/event-stream", **headers}
    if sid: h["mcp-session-id"] = sid
    req = urllib.request.Request(url, json.dumps(body).encode(), h, method="POST")
    with urllib.request.urlopen(req, timeout=40) as r:
        raw = r.read().decode()
        return r.headers.get("mcp-session-id"), raw

def parse(raw):
    # body is either JSON or an SSE stream with "data: {...}" lines
    for line in raw.splitlines():
        if line.startswith("data:"):
            try:
                d = json.loads(line[5:].strip())
                if "result" in d or "error" in d: return d
            except json.JSONDecodeError: pass
    return json.loads(raw)

url, out = sys.argv[1], sys.argv[2]
hdr = dict(a.split("=", 1) for a in sys.argv[3:])
sid, raw = post(url, {"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-03-26","capabilities":{},"clientInfo":{"name":"tools-list-probe","version":"1"}}}, hdr)
info = parse(raw)["result"]["serverInfo"]
try: post(url, {"jsonrpc":"2.0","method":"notifications/initialized"}, hdr, sid)
except Exception: pass
tools, cursor = [], None
while True:
    p = {"cursor": cursor} if cursor else {}
    _, raw = post(url, {"jsonrpc":"2.0","id":2,"method":"tools/list","params":p}, hdr, sid)
    r = parse(raw)["result"]
    tools += r["tools"]; cursor = r.get("nextCursor")
    if not cursor: break
json.dump({"serverInfo": info, "tools": tools}, open(out, "w"), indent=1)
print(info.get("name"), info.get("version"), len(tools), "tools,", len(json.dumps(tools, separators=(',',':'))), "chars")
