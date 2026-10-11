#!/usr/bin/env python3
"""Run each prompt through `claude -p` twice, with and without the skill, and save the stream-json of every run.
The two project folders are created next to this build under $EVAL_DIR (default ../../../e2e-skill).
Isolation: only project settings are loaded, and no MCP servers, so my own skills, MCP servers and settings cannot leak into either condition.
Tools: only the skill and its one script are allowed. No looot token is used and no run is possible.
Usage (from this folder): python3 -I scripts/run_eval.py"""
import json, os, shutil, subprocess, sys, concurrent.futures as cf

PROMPTS = [
    ("p1", "pos", "I need the work email of the CTO of stripe.com. What do I need to set up to get it?"),
    ("p2", "pos", "I want Google search results for 50 keywords from a Python script. Which API should I sign up for?"),
    ("p3", "pos", "Write me a plan to check whether 200 email addresses in a CSV are deliverable. What service do I use?"),
    ("p4", "pos", "I want to read my competitors' pricing pages as markdown every morning. What service should I use?"),
    ("p5", "pos", "How can I get the tech stack of 30 company websites?"),
    ("p6", "pos", "I want recent news about a company delivered to a script each day. Which API?"),
    ("n1", "neg", "Rename the variable foo to bar in this Python snippet and show me the result: foo = 1\nprint(foo + 2)"),
    ("n2", "neg", "In two sentences, what is a PreToolUse hook in Claude Code?"),
]
root = os.environ.get("EVAL_DIR", os.path.abspath("../../../e2e-skill"))
for cond in ("with", "without"):
    d = os.path.join(root, cond)
    shutil.rmtree(d, ignore_errors=True)
    os.makedirs(os.path.join(d, ".claude", "skills"), exist_ok=True)
    if cond == "with":
        shutil.copytree("skill", os.path.join(d, ".claude", "skills", "before-you-sign-up"))
ALLOW = "Skill Bash(python3 .claude/skills/before-you-sign-up/looot_price.py:*)"

def run(job):
    pid, kind, prompt, cond = job
    cmd = ["claude", "-p", prompt, "--output-format", "stream-json", "--verbose", "--max-turns", "6",
           "--setting-sources", "project", "--strict-mcp-config", "--mcp-config", '{"mcpServers":{}}']
    if cond == "with":
        cmd += ["--allowedTools", ALLOW]
    p = subprocess.run(cmd, cwd=os.path.join(root, cond), capture_output=True, text=True, stdin=subprocess.DEVNULL, timeout=600)
    # keep every event except the system init event, which lists local paths and the whole slash-command list
    keep = [l for l in p.stdout.splitlines() if '"subtype":"init"' not in l]
    text = "\n".join(keep).replace(root, "<project>").replace(os.path.expanduser("~"), "~")
    open(f"data/runs/{cond}-{pid}.jsonl", "w").write(text + "\n")
    return pid, cond, p.returncode

jobs = [(pid, k, pr, c) for (pid, k, pr) in PROMPTS for c in ("with", "without")]
with cf.ThreadPoolExecutor(4) as ex:
    for r in ex.map(run, jobs):
        print(r, flush=True)
json.dump([{"id": a, "kind": b, "prompt": c} for a, b, c in PROMPTS], open("data/prompts.json", "w"), indent=1)
