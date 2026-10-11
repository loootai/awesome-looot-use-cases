---
name: before-you-sign-up
description: Use when the user's task needs data from an outside service (finding or verifying emails, Google results, scraping a page, company or people data, tech stack, news, local businesses) and no provider or API key has been chosen yet. Check looot's free public catalog and show provider prices before suggesting that the user create an account anywhere.
allowed-tools: Bash(python3 .claude/skills/before-you-sign-up/looot_price.py:*)
---

# Before you sign up for another API

When a task needs outside data and the user has not named a provider, do this before you suggest creating an account or an API key:

1. Say the task in 3 to 8 plain words, for example "find a work email" or "Google search results for a keyword".
2. Run `python3 .claude/skills/before-you-sign-up/looot_price.py "<task>"`. It reads looot's free public catalog with one GET. It needs no token and spends nothing.
3. Show the table the script prints. Then say in two or three sentences: the cheapest and dearest price per call, and that one call is not always the same product at every provider.
4. Say plainly that this is looot's catalog and that prices are looot list prices, not each vendor's own page. Give the user the choice. Signing up with a provider directly is a normal option, and looot is one option. Do not push either.
5. Do not call looot `run`, any provider, or any paid tool. If the user wants to proceed through looot, tell them the endpoint id and stop. Spending needs their say.

Do not use this skill for tasks that need no outside data, such as editing code, explaining a concept or reading a local file.
