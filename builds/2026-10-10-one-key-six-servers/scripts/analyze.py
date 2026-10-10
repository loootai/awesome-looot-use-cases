#!/usr/bin/env python3
"""Read data/*.tools.json, count tools and characters of the minified tool definitions,
build the config entries, and write results.json. Standard library only.
Run from the folder root: python3 -I scripts/analyze.py"""
import json
RATIO = 4  # rough characters per token; NOT Claude's tokenizer. Treat tokens as an estimate.
servers = [
 # key, label, data file, config entry as the server's own README shows it (versions pinned here), keys needed
 ("firecrawl","Firecrawl","firecrawl.tools.json",{"command":"npx","args":["-y","firecrawl-mcp@3.27.3"],"env":{"FIRECRAWL_API_KEY":"<key>"}},1),
 ("tavily","Tavily","tavily.tools.json",{"command":"npx","args":["-y","tavily-mcp@0.2.22"],"env":{"TAVILY_API_KEY":"<key>"}},1),
 ("exa","Exa","exa.tools.json",{"type":"http","url":"https://mcp.exa.ai/mcp"},0),
 ("brave","Brave Search","brave.tools.json",{"command":"npx","args":["-y","@brave/brave-search-mcp-server@2.1.4"],"env":{"BRAVE_API_KEY":"<key>"}},1),
 ("serper","Serper","serper.tools.json",{"command":"npx","args":["-y","serper-search-scrape-mcp-server@0.1.2"],"env":{"SERPER_API_KEY":"<key>"}},1),
 ("hunter","Hunter","",{"type":"http","url":"https://mcp.hunter.io/mcp","headers":{"X-API-KEY":"<key>"}},1),
 ("looot","looot","looot.tools.json",{"type":"http","url":"https://api.looot.ai/mcp"},0),
]
out=[]
for k,label,f,entry,keys in servers:
    block = json.dumps({"mcpServers":{k:entry}}, indent=2)
    r={"key":k,"label":label,"config_lines":block.count("\n")+1,"keys":keys,"config":entry}
    if f:
        d=json.load(open("data/"+f)); ts=d["tools"]
        chars=len(json.dumps(ts,separators=(",",":")))
        r.update(tools=len(ts),chars=chars,tokens_est=round(chars/RATIO),version=d["serverInfo"].get("version"),
                 per_tool=sorted(((t["name"],len(json.dumps(t,separators=(",",":")))) for t in ts),key=lambda x:-x[1]))
    else:
        r.update(tools=None,chars=None,tokens_est=None,version=None,per_tool=[])
    out.append(r)
six=[r for r in out if r["key"]!="looot"]
meas=[r for r in six if r["tools"] is not None]
tot={"six_config_lines_one_file":json.dumps({"mcpServers":{r["key"]:r["config"] for r in six}},indent=2).count("\n")+1,
     "looot_config_lines":json.dumps({"mcpServers":{"looot":out[-1]["config"]}},indent=2).count("\n")+1,"six_keys":sum(r["keys"] for r in six),
     "measured_servers":len(meas),"measured_tools":sum(r["tools"] for r in meas),
     "measured_chars":sum(r["chars"] for r in meas),"measured_tokens_est":sum(r["tokens_est"] for r in meas),
     "ratio_chars_per_token":RATIO}
json.dump({"servers":out,"totals":tot},open("results.json","w"),indent=1)
for r in out: print(f'{r["label"]:14} lines={r["config_lines"]:2} keys={r["keys"]} tools={r["tools"]} chars={r["chars"]} tok~{r["tokens_est"]}')
print(tot)
