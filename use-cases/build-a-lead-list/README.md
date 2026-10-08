# Build a lead list as a CSV

![Build a lead list as a CSV](../../assets/cases/03.jpg)

**The job.** Search people by title at a company, find a work email for each, verify it, and write a CSV.

## What you get

A CSV with name, title, email and verify status per person. Start with a handful of people to check the cost.

## Price

Read from the free public catalog, as of 2026-10-08.

| Job | Cheapest per call |
| --- | --- |
| `people.search` | $0 (cheapest listed endpoint returns masked results; paid providers in a catalog search run from $0.00036 to $0.0054 and up) |
| `people.email.find` | $0.003598 |
| `people.email.verify` | $0.00145 |

Search prices differ a lot between providers. Run `looot search "search people by title"` first and read the price before you pick. Prices change; re-read them before a large batch with `curl -s 'https://api.looot.ai/v1/catalog/overview?depth=jobs'` (field `cheapestPerCall`, in USD).

## Paste this into an agent

```text
For the domain example.com, find up to 5 people whose title matches Head of Marketing. For each one, find a work email, then verify it. Write leads.csv with name, title, email, verify_status. Stop and ask me before spending more than $0.10. Skip anyone whose email is not valid.
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
looot run job:people.search --input '{"job_title": "Head of Marketing", "domain": "example.com", "limit": 5}' --wait
looot run job:people.email.find --input '{"first_name": "Jane", "last_name": "Doe", "domain": "example.com"}' --wait
looot run job:people.email.verify --input '{"email": "jane.doe@example.com"}' --wait
```

`looot balance` shows the minimum top-up. `looot help --all` lists every flag.

### 3. REST

```bash
export LOOOT_TOKEN=...   # an agent token from looot.ai
curl -s -X POST 'https://api.looot.ai/v1/runs?wait=30' \
  -H "Authorization: Bearer $LOOOT_TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{"endpointId": "job:people.search", "input": {"job_title": "Head of Marketing", "domain": "example.com", "limit": 5}, "idempotencyKey": "<unique-key>"}'

curl -s -X POST 'https://api.looot.ai/v1/runs?wait=30' \
  -H "Authorization: Bearer $LOOOT_TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{"endpointId": "job:people.email.find", "input": {"first_name": "Jane", "last_name": "Doe", "domain": "example.com"}, "idempotencyKey": "<unique-key>"}'

curl -s -X POST 'https://api.looot.ai/v1/runs?wait=30' \
  -H "Authorization: Bearer $LOOOT_TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{"endpointId": "job:people.email.verify", "input": {"email": "jane.doe@example.com"}, "idempotencyKey": "<unique-key>"}'
```

Use a new `idempotencyKey` for each logical call. Reusing a key with the same body returns the original run and charges nothing again.

The response has `runId`, `status`, `result`, `actualCost` and `error`. A run can answer HTTP 201 with `status: "failed"`, so check `status` and `error`, not the HTTP code. Past the wait window the run comes back queued; poll `GET /v1/runs/{runId}`.

## Notes

- The example values (`example.com`, Jane Doe) are placeholders. Swap in your own.
- `job:<id>` lets looot pick a provider of that job. To pin one provider, search the catalog and use its operation id instead.
- A miss is a normal answer, not an error, and a failed call costs nothing.
- Back to the [use case list](../../README.md).
