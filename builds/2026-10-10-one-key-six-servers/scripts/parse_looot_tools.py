#!/usr/bin/env python3
"""Build raw/looot.tools.json from https://api.looot.ai/llms-full.txt (the public tool docs).
Each tool = name + description (text between the heading and 'Input schema:') + minified inputSchema.
Operator-only tools (register_endpoint, verify_endpoint) are left out: a customer sign-in does not see them."""
import re, json, sys
txt = open(sys.argv[1]).read()
body = txt.split("## MCP tools",1)[1].split("\n## CLI",1)[0]
parts = re.split(r"\n### (\w+) -- [^\n]*\n", "\n"+body)
tools=[]
for name, sec in zip(parts[1::2], parts[2::2]):
    if name in ("register_endpoint","verify_endpoint"): continue
    desc = sec.split("Input schema:")[0].strip()
    m = re.search(r"Input schema:\s*```json\n(.*?)\n```", sec, re.S)
    schema = json.loads(m.group(1)) if m else {}
    tools.append({"name":name,"description":desc,"inputSchema":schema})
json.dump({"serverInfo":{"name":"looot","source":"llms-full.txt"},"tools":tools}, open(sys.argv[2],"w"), indent=1)
print(len(tools), "tools", len(json.dumps(tools,separators=(',',':'))), "chars")
