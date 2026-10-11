#!/usr/bin/env python3
"""Run the status line script against the real looot API (free reads only) and record what it prints and how long it takes.
Needs the looot CLI logged in (the token is read with `looot token --reveal`, kept in memory, passed to the script through the environment, never written down).
The balance figure is replaced with $NN.NN in everything this script saves. Output: data/test-results.json
Usage (from this folder): python3 -I scripts/run_tests.py"""
import json, os, re, subprocess, sys, tempfile, time, datetime, statistics, urllib.request

SCRIPT = os.path.join("statusline", "looot_statusline.py")
tok = re.search(r"([A-Za-z0-9_\-\.]{30,})", subprocess.run(["looot", "token", "--reveal"], capture_output=True, text=True).stdout).group(1)
state = tempfile.mkdtemp(prefix="statusline-state-", dir=os.environ.get("TEST_TMP", "."))
mask = lambda s: re.sub(r"balance \$[0-9.]+", "balance $NN.NN", s)
PAY = json.dumps({"session_id": "test-1", "model": {"display_name": "Claude"}, "cost": {"total_cost_usd": 0.1}})
def call(env_extra=None, payload=PAY, token=True, sid=None):
    env = {k: v for k, v in os.environ.items() if k != "LOOOT_TOKEN"}
    env.update(LOOOT_STATUS_STATE=state, **(env_extra or {}))
    if token: env["LOOOT_TOKEN"] = tok
    p = payload if sid is None else json.dumps(dict(json.loads(payload), session_id=sid))
    t = time.perf_counter()
    r = subprocess.run([sys.executable, "-I", SCRIPT], input=p, capture_output=True, text=True, env=env)
    return mask(r.stdout.strip()), round((time.perf_counter() - t) * 1000), r.returncode
R = {}
R["no_token"] = call(token=False)
R["cold_first_call"] = call(sid="cold")
time.sleep(4)
R["after_refresh"] = call(sid="cold")
cached = [call(sid="cold")[1] for _ in range(20)]
R["cached_call_ms"] = {"n": 20, "median": statistics.median(cached), "max": max(cached), "min": min(cached)}
cache = json.load(open(os.path.join(state, "cold.json")))["cache"]
R["refresh_ms_measured_by_script"] = cache["ms"]
R["hide_balance"] = call({"LOOOT_STATUS_HIDE_BALANCE": "1"}, sid="cold")
# correctness: spend since a fixed time against an independent sum from `looot runs list`
SINCE = "2026-10-09T00:00:00Z"
call({"LOOOT_STATUS_SINCE": SINCE, "LOOOT_STATUS_HIDE_BALANCE": "1"}, sid="since"); time.sleep(4)
out_since = call({"LOOOT_STATUS_SINCE": SINCE, "LOOOT_STATUS_HIDE_BALANCE": "1"}, sid="since")
cli = subprocess.run(["looot", "runs", "list", "--limit", "50"], capture_output=True, text=True, env={**os.environ, "LOOOT_TOKEN": tok}).stdout
runs = json.loads(cli[cli.index("{"):])["runs"]
sf = datetime.datetime.fromisoformat(SINCE.replace("Z", "+00:00"))
mine = [r for r in runs if datetime.datetime.fromisoformat(r["createdAt"].replace("Z", "+00:00")) >= sf]
R["since_test"] = {"since": SINCE, "script_printed": out_since[0], "independent_sum_usd": round(sum(float(r.get("actualCost") or 0) for r in mine), 6),
                   "independent_runs": len(mine), "independent_source": "looot runs list --limit 50 (CLI, own date filter and sum)", "script_state": json.load(open(os.path.join(state, "since.json")))["cache"]}
R["since_test"]["script_state"].pop("available", None); R["since_test"]["script_state"].pop("reserved", None)
# failure: API unreachable
call({"LOOOT_API": "http://127.0.0.1:9"}, sid="dead"); time.sleep(2)
R["api_unreachable"] = call({"LOOOT_API": "http://127.0.0.1:9"}, sid="dead")
R["meta"] = {"date": datetime.date.today().isoformat(), "python": sys.version.split()[0]}
json.dump(R, open("data/test-results.json", "w"), indent=1)
print(json.dumps(R, indent=1))
