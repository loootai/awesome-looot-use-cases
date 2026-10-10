# Take the real /context screenshots

The chart estimates tokens from characters. `/context` in Claude Code shows the real number for each setup. Three steps, about 5 minutes.

1. Make a scratch folder and add the six servers with the entries in `results.json` (or `claude mcp add` for each, with the keys you have). Open Claude Code there, run `/context`, and screenshot the MCP tools section. Note the "MCP tools" total. If you have no Hunter key, say so in the post and leave Hunter out.
2. Remove them (`claude mcp remove <name>` for each), run `claude mcp add --transport http looot https://api.looot.ai/mcp`, start a new session, sign in with `/mcp`, run `/context` again and screenshot it.
3. Save both screenshots in this folder as `context-six.png` and `context-looot.png`, write the two totals under the table in `README.md`, and quote the `/context` number instead of the estimate. If it differs much from the chart, trust `/context`.
