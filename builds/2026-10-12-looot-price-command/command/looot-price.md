---
description: List every provider and price for a task from the free looot catalog. Runs nothing, spends nothing.
argument-hint: <what you want done, in plain words>
allowed-tools: Bash(python3 .claude/commands/looot_price.py:*)
---

Price check for: $ARGUMENTS

Catalog result, read just now from https://api.looot.ai/v1/public-catalog (free, no sign-in):

!`python3 .claude/commands/looot_price.py "$ARGUMENTS"`

Show this to me as it is, then add at most three sentences: the cheapest and the most expensive provider and the multiple between them, and one thing to check before choosing on price alone. Do not call looot `run`, do not call any provider, and do not spend anything. If I want to go ahead, tell me the endpoint id and stop.
