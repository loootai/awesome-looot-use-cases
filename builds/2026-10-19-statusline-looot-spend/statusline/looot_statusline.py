#!/usr/bin/env python3
"""Claude Code status line: what this session has spent through looot, and the balance.

Claude Code runs this command, writes a JSON object on stdin (session_id, model, cwd, cost...) and shows the first line of stdout.
Output looks like:   looot session $0.0012 (3 runs) | balance $25.51

How it stays fast: it prints from a small cache file at once. When the cache is older than LOOOT_STATUS_TTL seconds
(default 30) it starts a detached background refresh and still prints the old numbers. The refresh makes two free reads,
GET /v1/balance and GET /v1/runs?limit=50, with your token. Nothing is ever run or charged.

Environment:
  LOOOT_TOKEN                  required, the same token the looot SDKs use
  LOOOT_STATUS_HIDE_BALANCE=1  print spend only
  LOOOT_STATUS_TTL             cache seconds, default 30
  LOOOT_STATUS_SINCE           ISO time that replaces "first time this session was seen" (used for testing)
  LOOOT_STATUS_STATE           state folder, default ~/.local/state/looot-statusline
  LOOOT_API                    base URL, default https://api.looot.ai
Session start is the first time this script saw the session id, so spend before that moment is not counted.
A run created by another tool on the same workspace during the session is counted too, and a run started in the last 30 seconds may not show yet.
Python 3 standard library only."""
import datetime as dt, json, os, re, subprocess, sys, time, urllib.request

API = os.environ.get("LOOOT_API", "https://api.looot.ai").rstrip("/")
TTL = float(os.environ.get("LOOOT_STATUS_TTL", "30"))
STATE = os.environ.get("LOOOT_STATUS_STATE", os.path.expanduser("~/.local/state/looot-statusline"))
NOW = lambda: dt.datetime.now(dt.timezone.utc)


def parse_iso(s):
    return dt.datetime.fromisoformat(s.replace("Z", "+00:00"))


def get(path, token):
    req = urllib.request.Request(API + path, headers={"Authorization": "Bearer " + token, "User-Agent": "looot-statusline/0.1"})
    with urllib.request.urlopen(req, timeout=8) as r:
        return json.load(r)


def refresh(sf, since_iso):
    """Read balance and recent runs, add up this session's actualCost, write the cache."""
    token = os.environ.get("LOOOT_TOKEN", "")
    st = json.load(open(sf))
    t0 = time.time()
    try:
        bal = get("/v1/balance", token)
        runs = get("/v1/runs?limit=50", token).get("runs", [])
        since = parse_iso(since_iso)
        mine = [r for r in runs if parse_iso(r["createdAt"]) >= since]
        st["cache"] = {"at": time.time(), "available": bal.get("available"), "reserved": bal.get("reserved"),
                       "spend": round(sum(float(r.get("actualCost") or 0) for r in mine), 6), "runs": len(mine),
                       "window_full": len(runs) == 50 and parse_iso(runs[-1]["createdAt"]) >= since, "ms": round((time.time() - t0) * 1000), "error": None}
    except Exception as e:
        st.setdefault("cache", {})["error"] = type(e).__name__
        st["cache"]["at"] = time.time() - TTL + 10   # retry in 10 s
    json.dump(st, open(sf, "w"))


def main():
    if len(sys.argv) > 2 and sys.argv[1] == "--refresh":
        return refresh(sys.argv[2], sys.argv[3])
    try:
        payload = json.load(sys.stdin)
    except Exception:
        payload = {}
    if not os.environ.get("LOOOT_TOKEN"):
        print("looot: set LOOOT_TOKEN")
        return
    os.makedirs(STATE, exist_ok=True)
    sid = re.sub(r"[^A-Za-z0-9_-]", "_", str(payload.get("session_id") or "nosession"))
    sf = os.path.join(STATE, sid + ".json")
    if not os.path.exists(sf):
        json.dump({"first_seen": NOW().isoformat()}, open(sf, "w"))
    st = json.load(open(sf))
    since = os.environ.get("LOOOT_STATUS_SINCE") or st["first_seen"]
    c = st.get("cache")
    if c is None or time.time() - c.get("at", 0) > TTL:
        subprocess.Popen([sys.executable, "-I", os.path.abspath(__file__), "--refresh", sf, since],
                         stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True,
                         env=dict(os.environ))
    if not c or c.get("available") is None:
        print("looot session $0 | reading..." if not (c and c.get("error")) else "looot: cannot read (%s)" % c["error"])
        return
    s = f"looot session ${c['spend']:.4f} ({c['runs']} run{'' if c['runs'] == 1 else 's'}{'+' if c.get('window_full') else ''})"
    if os.environ.get("LOOOT_STATUS_HIDE_BALANCE") != "1":
        s += f" | balance ${float(c['available']):.2f}" + (" LOW" if float(c["available"]) < 1 else "")
    if c.get("error"):
        s += " (stale)"
    print(s)


if __name__ == "__main__":
    main()
