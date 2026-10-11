<p align="center"><img src="assets/banner.jpg" alt="awesome-looot-use-cases" width="100%"></p>

# awesome-looot-use-cases

**[Showcase](https://loootai.github.io/showcase/)**: every repo built on looot in one gallery, with prices.

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

## Open-source alternatives built on looot

Each repo rebuilds a paid product on one looot key, with a demo mode, a headless CLI and the price shown before every run. No paid looot run was made for any of them yet, so parsers come from docs and fixtures. Costs are list prices from each README.

| Repo | Replaces | What it does | Typical run at list price |
| --- | --- | --- | --- |
| [looot-intent](https://github.com/loootai/looot-intent) | 6sense | Scores company domains from ten public signals, with the provider and cost behind each point. | $0.18 per account |
| [looot-score](https://github.com/loootai/looot-score) | MadKudu | CSV of leads in, grade A to D out, against an ICP you edit. | $0.83 to $1.67 per 100 leads |
| [looot-reveal](https://github.com/loootai/looot-reveal) | RB2B, Clearbit Reveal | Turns visitor IPs into companies with an ICP flag. Company level only. | about $0.08 per 100 new IPs |
| [looot-techstack](https://github.com/loootai/looot-techstack) | BuiltWith, Wappalyzer | Website technologies from several providers side by side, plus companies using a technology. | $1.89 per 100 domains |
| [looot-signals](https://github.com/loootai/looot-signals) | TheirStack, Harmonic | Hiring, funding, news and leadership triggers as a dated feed with an evidence link. | up to $0.53 per run of five triggers |
| [looot-lookalike](https://github.com/loootai/looot-lookalike) | Ocean.io | 3 to 20 seed domains in, a ranked list of similar companies out. | up to $0.21 for 6 seeds |
| [looot-ads](https://github.com/loootai/looot-ads) | Foreplay | Competitor ads from the Meta, Google, LinkedIn and TikTok libraries on one board. | about $0.11 for 5 competitors |
| [looot-reviews](https://github.com/loootai/looot-reviews) | ReviewTrackers | Google Maps, App Store, Google Play and Tripadvisor reviews grouped into themes. | up to $0.015 for 5 companies on Google Maps |
| [looot-battlecards](https://github.com/loootai/looot-battlecards) | Klue, Crayon | Competitor battlecards with a source link and date on every claim. | $0.076 for 5 competitors |
| [looot-mentions](https://github.com/loootai/looot-mentions) | Brand24, Mention | Brand and keyword mentions from six sources, with sentiment and a daily digest. | $0.0066 per keyword per run |
| [looot-warm-leads](https://github.com/loootai/looot-warm-leads) | Gojiberry | Warm leads from LinkedIn intent signals, scored against your ICP with each point itemised, verified emails, drafted messages, CSV and Instantly export. LinkedIn sending is optional, off by default, through your own Unipile account. | up to $0.25 per run (new role only), $0.65 with hiring and funding triggers |

## Builds

One dated build a day, each with its data and the steps to reproduce it. looot made these comparisons.

| Date | Build | Result |
| --- | --- | --- |
| 2026-10-10 | [One looot entry vs six MCP servers](builds/2026-10-10-one-key-six-servers/README.md) | Tool-definition size read from each server's tools/list |
| 2026-10-11 | [One Google search at 7 providers](builds/2026-10-11-google-search-price-spread/README.md) | $0.0009 to $0.025 a call, read from the free catalog |
| 2026-10-12 | [/looot-price slash command](builds/2026-10-12-looot-price-command/README.md) | Every provider and price for a task, nothing run |
| 2026-10-13 | [Budget guard hook for Claude Code](builds/2026-10-13-budget-guard-hook/README.md) | Blocked a $0.025 run at a $0.01 limit in a real session, 23 payloads checked |
| 2026-10-14 | [Catalog map](builds/2026-10-14-catalog-map/README.md) | 2,590 endpoints, 94 providers. 119 jobs have 2 or more providers, median price spread 6.9x |
| 2026-10-15 | [before-you-sign-up skill](builds/2026-10-15-before-you-sign-up-skill/README.md) | Skill used on 6 of 6 data prompts and 0 of 2 others, 8 prompts, small test |
| 2026-10-16 | [Subscription vs per-call](builds/2026-10-16-subscription-vs-per-call/README.md) | looot's list price equals the vendor's entry price for 4 of 5 vendors, bigger vendor plans are 2 to 7.5x cheaper per unit |
| 2026-10-17 | [What an IP-to-company lookup returns](builds/2026-10-17-ip-to-company-what-it-tells-you/README.md) | Owner lookups $0.03 to $2 per 1,000, a company profile $280 per 1,000 matches, 14 IPs checked at two free services |

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
- [loootai/reverse-engineer](https://github.com/loootai/reverse-engineer), skills that take a product apart from public evidence, rebuild it on looot and request missing data sources.
- [loootai/n8n-nodes-looot](https://github.com/loootai/n8n-nodes-looot), the n8n node.
- [loootai/awesome-gtm](https://github.com/loootai/awesome-gtm), a list of open-source GTM tools, with and without looot.

Docs: https://docs.looot.ai. Support: https://looot.ai/contact. Privacy: https://looot.ai/privacy. Terms: https://looot.ai/terms.

## Contributing

Open an issue or a pull request with a new recipe. Read prices from the public catalog only, write the date next to each price, and do not paste result bodies you have not seen.

## License

MIT. See [LICENSE](LICENSE).
