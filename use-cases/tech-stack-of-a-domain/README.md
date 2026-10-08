# Find the tech stack of a domain

![Find the tech stack of a domain](../../assets/cases/09.jpg)

**The job.** List the technologies a company's website runs on.

## What you get

Technology detections for the domain.

## Price

Read from the free public catalog, as of 2026-10-08.

| Job | Cheapest per call |
| --- | --- |
| `company.technographics` | $0 (cheapest listed endpoint returns technology group counts only) |
| `full technology list, Tomba endpoint `tomba-technology`` | $0.0089 |

Read the price of the endpoint you pick. In a catalog search, full-list providers ran from $0.0089 to $0.0981. Prices change; re-read them before a large batch with `curl -s 'https://api.looot.ai/v1/catalog/overview?depth=jobs'` (field `cheapestPerCall`, in USD).

## Paste this into an agent

```text
Which technologies does example.com use? Group them by category and flag any CRM, analytics or marketing automation tool.
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
looot run job:company.technographics --input '{"domain": "example.com"}' --wait
```

`looot balance` shows the minimum top-up. `looot help --all` lists every flag.

### 3. REST

```bash
export LOOOT_TOKEN=...   # an agent token from looot.ai
curl -s -X POST 'https://api.looot.ai/v1/runs?wait=30' \
  -H "Authorization: Bearer $LOOOT_TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{"endpointId": "job:company.technographics", "input": {"domain": "example.com"}, "idempotencyKey": "<unique-key>"}'
```

Use a new `idempotencyKey` for each logical call. Reusing a key with the same body returns the original run and charges nothing again.

The response has `runId`, `status`, `result`, `actualCost` and `error`. A run can answer HTTP 201 with `status: "failed"`, so check `status` and `error`, not the HTTP code. Past the wait window the run comes back queued; poll `GET /v1/runs/{runId}`.

## Notes

- The example values (`example.com`, Jane Doe) are placeholders. Swap in your own.
- `job:<id>` lets looot pick a provider of that job. To pin one provider, search the catalog and use its operation id instead.
- A miss is a normal answer, not an error, and a failed call costs nothing.
- Back to the [use case list](../../README.md).
