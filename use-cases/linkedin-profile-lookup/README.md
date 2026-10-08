# Look up a LinkedIn profile

![Look up a LinkedIn profile](../../assets/cases/08.jpg)

**The job.** Read the public details of one LinkedIn profile from its URL.

## What you get

Public profile details. The MCP tool describes headline, role, company and location.

## Price

Read from the free public catalog, as of 2026-10-08.

| Job | Cheapest per call |
| --- | --- |
| `linkedin.person.profile` | $0.0012 |

Cheapest listed endpoint for the job. Prices change; re-read them before a large batch with `curl -s 'https://api.looot.ai/v1/catalog/overview?depth=jobs'` (field `cheapestPerCall`, in USD).

## Paste this into an agent

```text
Look up the LinkedIn profile at https://www.linkedin.com/in/example-person. Give me the current role, company and location. If the profile is not found, say so instead of guessing.
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
looot run job:linkedin.person.profile --input '{"linkedin_url": "https://www.linkedin.com/in/example-person"}' --wait
```

`looot balance` shows the minimum top-up. `looot help --all` lists every flag.

### 3. REST

```bash
export LOOOT_TOKEN=...   # an agent token from looot.ai
curl -s -X POST 'https://api.looot.ai/v1/runs?wait=30' \
  -H "Authorization: Bearer $LOOOT_TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{"endpointId": "job:linkedin.person.profile", "input": {"linkedin_url": "https://www.linkedin.com/in/example-person"}, "idempotencyKey": "<unique-key>"}'
```

Use a new `idempotencyKey` for each logical call. Reusing a key with the same body returns the original run and charges nothing again.

The response has `runId`, `status`, `result`, `actualCost` and `error`. A run can answer HTTP 201 with `status: "failed"`, so check `status` and `error`, not the HTTP code. Past the wait window the run comes back queued; poll `GET /v1/runs/{runId}`.

## Notes

- The example values (`example.com`, Jane Doe) are placeholders. Swap in your own.
- `job:<id>` lets looot pick a provider of that job. To pin one provider, search the catalog and use its operation id instead.
- A miss is a normal answer, not an error, and a failed call costs nothing.
- Back to the [use case list](../../README.md).
