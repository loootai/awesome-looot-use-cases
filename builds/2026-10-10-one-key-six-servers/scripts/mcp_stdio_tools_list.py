#!/usr/bin/env python3
"""Start a stdio MCP server with a fake key and no network credentials, ask tools/list, save JSON.
Usage: mcp_stdio_tools_list.py <out.json> <ENV_NAME=fake> -- <command> [args...]"""
import json, subprocess, sys, os
out = sys.argv[1]; i = sys.argv.index("--"); envs = sys.argv[2:i]; cmd = sys.argv[i+1:]
env = {**os.environ, **dict(e.split("=",1) for e in envs)}
p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True, env=env)
def send(m): p.stdin.write(json.dumps(m)+"\n"); p.stdin.flush()
def recv(id_):
    while True:
        l = p.stdout.readline()
        if not l: raise SystemExit("server closed")
        try: d = json.loads(l)
        except ValueError: continue
        if d.get("id") == id_: return d
send({"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-03-26","capabilities":{},"clientInfo":{"name":"tools-list-probe","version":"1"}}})
info = recv(1)["result"]["serverInfo"]
send({"jsonrpc":"2.0","method":"notifications/initialized"})
tools, cur, n = [], None, 2
while True:
    send({"jsonrpc":"2.0","id":n,"method":"tools/list","params":({"cursor":cur} if cur else {})})
    r = recv(n)["result"]; tools += r["tools"]; cur = r.get("nextCursor"); n += 1
    if not cur: break
p.terminate()
json.dump({"serverInfo":info,"tools":tools}, open(out,"w"), indent=1)
print(info.get("name"), info.get("version"), len(tools), "tools,", len(json.dumps(tools,separators=(',',':'))), "chars")
