# Research a prospect before a call

![Research a prospect before a call](../../assets/cases/12.jpg)

**The job.** Build a one-page brief on a person and their company from four cheap lookups.

## What you get

A short brief: company facts, the person's role, recent news and what the company's site says.

## Price

Read from the free public catalog, as of 2026-10-08.

| Job | Cheapest per call |
| --- | --- |
| `company.enrich` | $0.0019 |
| `linkedin.person.profile` | $0.0012 |
| `news.search` | $0.00099 |
| `web.scrape.markdown` | $0.0002 |

Sum of the four cheapest listed endpoints is $0.00429. Prices change; re-read them before a large batch with `curl -s 'https://api.looot.ai/v1/catalog/overview?depth=jobs'` (field `cheapestPerCall`, in USD).

## Paste this into an agent

```text
I have a call with the person at https://www.linkedin.com/in/example-person, who works at example.com. Enrich the company, read the profile, search recent news about the company, and read the company homepage. Write a brief of at most 200 words with three questions I could ask. Mark every fact with the lookup it came from.
```

## Three ways to run it

### 1. Claude Code or any MCP client

```bash
claude mcp add --transport http looot https://api.looot.ai/mcp
```

Sign in in the browser when the client asks. Then paste the prompt above.

### 2. CLI

```bash
npm install -g looot
looot login
looot run job:company.enrich --input '{"domain": "example.com"}' --wait
looot run job:linkedin.person.profile --input '{"linkedin_url": "https://www.linkedin.com/in/example-person"}' --wait
looot run job:news.search --input '{"query": "Example Corp", "limit": 5}' --wait
looot run job:web.scrape.markdown --input '{"url": "https://example.com"}' --wait
```

`looot balance` shows the minimum top-up. `looot help --all` lists every flag.

### 3. REST

```bash
export LOOOT_TOKEN=...   # an agent token from looot.ai
curl -s -X POST 'https://api.looot.ai/v1/runs?wait=30' \
  -H "Authorization: Bearer $LOOOT_TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{"endpointId": "job:company.enrich", "input": {"domain": "example.com"}, "idempotencyKey": "<unique-key>"}'

curl -s -X POST 'https://api.looot.ai/v1/runs?wait=30' \
  -H "Authorization: Bearer $LOOOT_TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{"endpointId": "job:linkedin.person.profile", "input": {"linkedin_url": "https://www.linkedin.com/in/example-person"}, "idempotencyKey": "<unique-key>"}'

curl -s -X POST 'https://api.looot.ai/v1/runs?wait=30' \
  -H "Authorization: Bearer $LOOOT_TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{"endpointId": "job:news.search", "input": {"query": "Example Corp", "limit": 5}, "idempotencyKey": "<unique-key>"}'

curl -s -X POST 'https://api.looot.ai/v1/runs?wait=30' \
  -H "Authorization: Bearer $LOOOT_TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{"endpointId": "job:web.scrape.markdown", "input": {"url": "https://example.com"}, "idempotencyKey": "<unique-key>"}'
```

Use a new `idempotencyKey` for each logical call. Reusing a key with the same body returns the original run and charges nothing again.

The response has `runId`, `status`, `result`, `actualCost` and `error`. A run can answer HTTP 201 with `status: "failed"`, so check `status` and `error`, not the HTTP code. Past the wait window the run comes back queued; poll `GET /v1/runs/{runId}`.

## Notes

- The example values (`example.com`, Jane Doe) are placeholders. Swap in your own.
- `job:<id>` lets looot pick a provider of that job. To pin one provider, search the catalog and use its operation id instead.
- A miss is a normal answer, not an error, and a failed call costs nothing.
- Back to the [use case list](../../README.md).
