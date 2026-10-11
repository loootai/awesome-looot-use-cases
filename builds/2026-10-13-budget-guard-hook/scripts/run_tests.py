#!/usr/bin/env python3
"""Replay hook payloads against hook/looot_budget_guard.py and record the decision and wall time of each.
These are payloads shaped like Claude Code's PreToolUse input. The price lookups are real reads of the
free public catalog. No looot run is made. Output: data/test-results.json
Usage (from this folder): python3 -I scripts/run_tests.py"""
import json, os, subprocess, sys, tempfile, time, datetime

HOOK = os.path.join("hook", "looot_budget_guard.py")
state = tempfile.mkdtemp(prefix="guard-state-", dir=os.environ.get("GUARD_TMP", "."))

def call(name, payload, env=None):
    e = dict(os.environ, LOOOT_GUARD_STATE=state, **(env or {}))
    t = time.perf_counter()
    p = subprocess.run([sys.executable, "-I", HOOK], input=json.dumps(payload), capture_output=True, text=True, env=e)
    ms = round((time.perf_counter() - t) * 1000)
    out = p.stdout.strip()
    dec, reason = "no opinion (exit 0, no output)", ""
    if out:
        j = json.loads(out)
        h = j.get("hookSpecificOutput")
        if h:
            dec, reason = h["permissionDecision"], h["permissionDecisionReason"]
        else:
            dec, reason = "pass (message only)", j.get("systemMessage", "")
    return {"case": name, "decision": dec, "reason": reason, "ms": ms, "exit": p.returncode}

mcp = lambda eid, inp=None, **kw: {"session_id": kw.pop("s", "s1"), "hook_event_name": "PreToolUse",
    "tool_name": "mcp__looot__run", "tool_input": dict({"endpointId": eid, "input": inp or {}, "idempotencyKey": "k"}, **kw)}
bash = lambda cmd, s="s1": {"session_id": s, "hook_event_name": "PreToolUse", "tool_name": "Bash", "tool_input": {"command": cmd}}

R = []
R.append(call("MCP run, serper-search ($0.001)", mcp("serper-search", {"q": "x"})))
R.append(call("MCP run, serpapi-google ($0.025)", mcp("serpapi-google", {"q": "x"})))
R.append(call("MCP run, free endpoint ($0)", mcp("ai-ark-lists")))
R.append(call("Bash: looot run serper-search", bash("looot run serper-search --input '{\"q\":\"x\"}' --wait")))
R.append(call("Bash: looot run serpapi-google", bash("cd x && looot run serpapi-google --input '{\"q\":\"x\"}'")))
R.append(call("MCP run, job:people.email.find", mcp("job:people.email.find", {"domain": "a.com"})))
R.append(call("MCP run, per-result price (ai-ark-people)", mcp("ai-ark-people")))
R.append(call("MCP run, fallback true", mcp("serper-search", fallback=True)))
R.append(call("MCP run, fallback maxCostUsd 0.5", mcp("serper-search", fallback={"maxCostUsd": 0.5})))
R.append(call("MCP run, fallback maxCostUsd 0.005", mcp("serper-search", fallback={"maxCostUsd": 0.005})))
R.append(call("MCP run, endpoint that does not exist", mcp("no-such-endpoint")))
R.append(call("catalog unreachable", mcp("serper-search"), {"LOOOT_CATALOG_URL": "http://127.0.0.1:9"}))
R.append(call("LOOOT_UNKNOWN_PRICE=deny, job id", mcp("job:people.email.find"), {"LOOOT_UNKNOWN_PRICE": "deny"}))
R.append(call("not a looot run: Bash ls", bash("ls -la")))
R.append(call("not a looot run: Edit", {"session_id": "s1", "tool_name": "Edit", "tool_input": {"file_path": "a"}}))
R.append(call("MCP inspect (free tool)", dict(mcp("serper-search"), tool_name="mcp__looot__inspect")))
# session cap: cap $0.005, serper-search $0.001 each, 7 runs in one session
seq = [call(f"cap test run {n} (cap $0.005)", mcp("serper-search", s="cap"), {"LOOOT_SESSION_CAP": "0.005"}) for n in range(1, 8)]
R += seq
meta = {"date": datetime.date.today().isoformat(), "python": sys.version.split()[0], "cases": len(R)}
json.dump({"meta": meta, "results": R}, open("data/test-results.json", "w"), indent=1)
for r in R:
    print(f'{r["ms"]:5d} ms  {r["decision"]:32s} {r["case"]}')
