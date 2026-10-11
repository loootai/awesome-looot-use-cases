#!/usr/bin/env python3
"""Claude Code PreToolUse hook: cap what an agent can spend through looot runs.

Reads the hook payload on stdin. For a looot `run` (the MCP tool, or `looot run` in Bash) it looks up
the endpoint's list price in the free public catalog and answers allow, ask or deny.

Settings, all environment variables:
  LOOOT_MAX_PRICE_PER_CALL   deny a run whose list price is above this many USD (default 0.01)
  LOOOT_SESSION_CAP          deny once allowed runs in this session add up to this many USD (default 0.25)
  LOOOT_UNKNOWN_PRICE        what to do when the price cannot be known: ask (default) or deny
  LOOOT_AUTO_ALLOW           set to 1 to approve runs inside the limits without a prompt (default: leave the prompt rules alone)
  LOOOT_CATALOG_URL          catalog base URL (default https://api.looot.ai)

The session total counts the list price of every run this hook allowed. Failed runs are free at looot,
so the real bill can be lower. It is never higher for a plain `unit: call` endpoint.
Python 3 standard library only. No token is read or sent.
"""
import fcntl, json, os, re, shlex, sys, time, urllib.error, urllib.request

BASE = os.environ.get("LOOOT_CATALOG_URL", "https://api.looot.ai").rstrip("/")
MAX_CALL = float(os.environ.get("LOOOT_MAX_PRICE_PER_CALL", "0.01"))
CAP = float(os.environ.get("LOOOT_SESSION_CAP", "0.25"))
UNKNOWN = os.environ.get("LOOOT_UNKNOWN_PRICE", "ask")
AUTO_ALLOW = os.environ.get("LOOOT_AUTO_ALLOW") == "1"
STATE_DIR = os.environ.get("LOOOT_GUARD_STATE", os.path.expanduser("~/.local/state/looot-budget-guard"))


def answer(decision, reason):
    print(json.dumps({"hookSpecificOutput": {"hookEventName": "PreToolUse",
                                              "permissionDecision": decision,
                                              "permissionDecisionReason": reason}}))
    sys.exit(0)


def parse_run(payload):
    """Return (endpoint_id, input_dict) when this tool call is a looot run, None when it is not.
    Return ("?", {}) when it looks like a run but cannot be parsed."""
    name = payload.get("tool_name", "")
    ti = payload.get("tool_input") or {}
    if name.startswith("mcp__") and "looot" in name.lower() and name.endswith("__run"):
        return str(ti.get("endpointId") or "?"), ti
    if name == "Bash":
        cmd = ti.get("command", "")
        if not re.search(r"\blooot\s+run\b", cmd):
            return None
        try:
            toks = shlex.split(cmd)
        except ValueError:
            return "?", {}
        for i, t in enumerate(toks[:-1]):
            if t == "looot" and toks[i + 1] == "run":
                rest = toks[i + 2:]
                eid = next((x for x in rest if not x.startswith("-")), "?")
                body = {}
                if "--input" in rest:
                    try:
                        body = {"input": json.loads(rest[rest.index("--input") + 1])}
                    except (ValueError, IndexError):
                        pass
                return eid, body
        return "?", {}
    return None


def list_price(endpoint_id):
    """USD list price of one call, or (None, why)."""
    if endpoint_id == "?" or endpoint_id.startswith(("job:", "workflow:")):
        return None, f"the endpoint '{endpoint_id}' has no single list price"
    url = f"{BASE}/v1/public-catalog/{urllib.request.quote(endpoint_id, safe='')}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "looot-budget-guard/0.1"})
        with urllib.request.urlopen(req, timeout=5) as r:
            item = json.load(r)
    except urllib.error.HTTPError as e:
        return None, f"catalog answered HTTP {e.code} for '{endpoint_id}'"
    except Exception as e:  # network down, bad JSON
        return None, f"could not read the catalog ({type(e).__name__})"
    p = item.get("price") or {}
    if p.get("state") != "known":
        return None, f"'{endpoint_id}' has no known price"
    if p.get("unit") != "call":
        return None, (f"'{endpoint_id}' is priced per {p.get('unit')} "
                      f"(${p['amountMicros'] / 1e6:g} each), so the total depends on how many come back")
    return p["amountMicros"] / 1e6, None


def add_to_session(session, usd):
    os.makedirs(STATE_DIR, exist_ok=True)
    path = os.path.join(STATE_DIR, re.sub(r"[^A-Za-z0-9_-]", "_", session or "nosession") + ".json")
    with open(path, "a+") as f:
        fcntl.flock(f, fcntl.LOCK_EX)
        f.seek(0)
        raw = f.read()
        st = json.loads(raw) if raw else {"spent": 0.0, "runs": 0}
        before = st["spent"]
        if before + usd > CAP + 1e-12:
            return False, before
        st["spent"] = round(before + usd, 9)
        st["runs"] += 1
        f.seek(0); f.truncate(); f.write(json.dumps(st))
        return True, st["spent"]


def main():
    try:
        payload = json.load(sys.stdin)
        run = parse_run(payload)
        if run is None:
            sys.exit(0)  # not a looot run: say nothing, let other rules decide
        eid, body = run
        fb = body.get("fallback")
        usd, why = list_price(eid)
        if usd is None:
            answer(UNKNOWN, f"looot budget guard: {why}. Price not known, so the limit cannot be checked.")
        if fb:
            ceiling = fb.get("maxCostUsd") if isinstance(fb, dict) else None
            if ceiling is None:
                answer(UNKNOWN, "looot budget guard: this run uses fallback with no maxCostUsd, so "
                                "other providers may be tried at other prices. Set fallback.maxCostUsd.")
            usd = max(usd, float(ceiling))
        if usd > MAX_CALL + 1e-12:
            answer("deny", f"looot budget guard: '{eid}' lists at ${usd:g} a call, above the per-call limit "
                           f"${MAX_CALL:g} (LOOOT_MAX_PRICE_PER_CALL). Pick a cheaper endpoint or ask the user.")
        ok, total = add_to_session(payload.get("session_id"), usd)
        if not ok:
            answer("deny", f"looot budget guard: this run (${usd:g}) would take the session past the cap "
                           f"${CAP:g} (LOOOT_SESSION_CAP). Spent so far ${total:g}. Ask the user to raise it.")
        if AUTO_ALLOW:
            answer("allow", f"looot budget guard: '{eid}' ${usd:g}, session total ${total:g} of ${CAP:g}")
        # Within limits: stay silent so Claude Code's own permission rules decide whether to prompt.
        print(json.dumps({"systemMessage": f"looot budget guard: '{eid}' ${usd:g}, session total ${total:g} of ${CAP:g}"}))
        sys.exit(0)
    except SystemExit:
        raise
    except Exception as e:
        # Fail closed for anything that might be a run. A hook crash would otherwise let the run through.
        answer("ask", f"looot budget guard: internal error ({type(e).__name__}); asking instead of guessing")


if __name__ == "__main__":
    main()
