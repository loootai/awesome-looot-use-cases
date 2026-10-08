<p align="center"><img src="assets/banner.jpg" alt="awesome-looot-use-cases" width="100%"></p>

# awesome-looot-use-cases

Copy-paste recipes for what an agent can do with [looot](https://looot.ai). looot gives an agent one token and one prepaid balance for 2,500+ data API endpoints from 90+ providers. The agent searches the catalog, sees the price before it runs, and pays per call. A failed call costs nothing. No subscription, top up from $5.

Each recipe has the job in one sentence, a prompt to paste, and three ways to run it: an MCP client, the CLI and plain REST.

## Use cases

Prices are the cheapest listed endpoint per job in the free public catalog, as of 2026-10-08.

| Use case | What you get | Price per call | Recipe |
| --- | --- | --- | --- |
| Find and verify a work email | A work email address and a deliverability verdict | $0.0036 find + $0.00145 verify | [recipe](use-cases/find-and-verify-work-email/README.md) |
| Enrich a company from its domain | Company facts as the chosen provider returns them | $0.0019 | [recipe](use-cases/enrich-company-from-domain/README.md) |
| Build a lead list as a CSV | A CSV with name, title, email and verify status per person | $0 to ~$0.0054 per search, then $0.0036 + $0.00145 per person | [recipe](use-cases/build-a-lead-list/README.md) |
| Track Google rankings for a keyword list | The organic Google results for each keyword | $0.0009 per keyword | [recipe](use-cases/track-google-rankings/README.md) |
| Read any web page as Markdown | The page content as Markdown | $0.0002 | [recipe](use-cases/read-a-web-page-as-markdown/README.md) |
| Monitor news about a company | Recent news articles for the query | $0.00099 | [recipe](use-cases/monitor-company-news/README.md) |
| Local business list for a city | Local businesses from the map | $0.001 | [recipe](use-cases/local-business-list-for-a-city/README.md) |
| Look up a LinkedIn profile | Public profile details | $0.0012 | [recipe](use-cases/linkedin-profile-lookup/README.md) |
| Find the tech stack of a domain | Technology detections for the domain | $0 to $0.0089 | [recipe](use-cases/tech-stack-of-a-domain/README.md) |
| Find a phone number | A phone number if a provider has one | $0.00483 | [recipe](use-cases/phone-number-lookup/README.md) |
| Competitor SERP snapshot | The organic Google results for each query, saved with a date | $0.0009 per query | [recipe](use-cases/competitor-serp-snapshot/README.md) |
| Research a prospect before a call | A short brief: company facts, the person's role, recent news and what the company's site says | about $0.0043 for the four calls | [recipe](use-cases/research-a-prospect-before-a-call/README.md) |

## Quick start

```bash
claude mcp add --transport http looot https://api.looot.ai/mcp   # sign in in the browser
npm install -g looot && looot login                              # or use the CLI
```

Browsing the catalog needs no token and is free:

```bash
curl -s 'https://api.looot.ai/v1/catalog/overview?depth=jobs'
curl -s 'https://api.looot.ai/v1/public-catalog?q=find+work+email&limit=10'
```

A paid REST run looks like this:

```bash
curl -s -X POST 'https://api.looot.ai/v1/runs?wait=30' \
  -H "Authorization: Bearer $LOOOT_TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{"endpointId":"job:people.email.verify","input":{"email":"jane.doe@example.com"},"idempotencyKey":"<unique-key>"}'
```

## Related

- [loootai/looot-mcp](https://github.com/loootai/looot-mcp), install steps for the MCP server.
- [loootai/looot-js](https://github.com/loootai/looot-js), a typed client for the REST API.
- [loootai/looot-skills](https://github.com/loootai/looot-skills), agent skills for 20 data jobs.
- [loootai/n8n-nodes-looot](https://github.com/loootai/n8n-nodes-looot), the n8n node.
- [loootai/awesome-gtm](https://github.com/loootai/awesome-gtm), a list of open-source GTM tools, with and without looot.

Docs: https://docs.looot.ai. Support: https://looot.ai/contact. Privacy: https://looot.ai/privacy. Terms: https://looot.ai/terms.

## Contributing

Open an issue or a pull request with a new recipe. Read prices from the public catalog only, write the date next to each price, and do not paste result bodies you have not seen.

## License

MIT. See [LICENSE](LICENSE).
