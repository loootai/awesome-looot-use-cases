# Find and verify a work email

![Find and verify a work email](../../assets/cases/01.jpg)

**The job.** Given a first name, last name and company domain, find a work email, then check it is deliverable before you send.

## What you get

A work email address and a deliverability verdict. Email status values the gateway documents for verify runs: valid, invalid, catch_all, risky, unknown.

## Price

Read from the free public catalog, as of 2026-10-08.

| Job | Cheapest per call |
| --- | --- |
| `people.email.find` | $0.003598 |
| `people.email.verify` | $0.00145 |

Cheapest listed endpoint per job. A provider that bills a not-found is charged; a failed call is free. Prices change; re-read them before a large batch with `curl -s 'https://api.looot.ai/v1/catalog/overview?depth=jobs'` (field `cheapestPerCall`, in USD).

## Paste this into an agent

```text
Find the work email of Jane Doe at example.com. Then verify it. Report the address and the verify status. If the verify status is not valid, say so and do not suggest sending to it.
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
  -d '{"endpointId": "job:people.email.find", "input": {"first_name": "Jane", "last_name": "Doe", "domain": "example.com"}, "idempotencyKey": "<unique-key>"}'

curl -s -X POST 'https://api.looot.ai/v1/runs?wait=30' \
  -H "Authorization: Bearer $LOOOT_TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{"endpointId": "job:people.email.verify", "input": {"email": "jane.doe@example.com"}, "idempotencyKey": "<unique-key>"}'
```

Use a new `idempotencyKey` for each logical call. Reusing a key with the same body returns the original run and charges nothing again.

The response has `runId`, `status`, `result`, `actualCost` and `error`. A run can answer HTTP 201 with `status: "failed"`, so check `status` and `error`, not the HTTP code. Past the wait window the run comes back queued; poll `GET /v1/runs/{runId}`.

Pass `"fallback": true` in the body (CLI: `--fallback`) to let looot try the next provider of the same job on a miss. Only attempts that ran are charged, inside one hold.

## Notes

- The example values (`example.com`, Jane Doe) are placeholders. Swap in your own.
- `job:<id>` lets looot pick a provider of that job. To pin one provider, search the catalog and use its operation id instead.
- A miss is a normal answer, not an error, and a failed call costs nothing.
- Back to the [use case list](../../README.md).
