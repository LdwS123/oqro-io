# OQRO examples (free)

Small, copyable examples for the free OQRO REST API and MCP server. Both need a free OQRO account; nothing here costs money.

## REST API

| Example | What it does |
|---|---|
| [python/insider_trades_to_csv.py](python/insider_trades_to_csv.py) | Pages through `GET /insider-trades` and writes every row to a CSV, with the SEC filing link kept on each row. Handles `429` by waiting for `Retry-After`. |

```bash
pip install requests
export OQRO_API_KEY=oqro_...   # oqro.io, account, API keys
python examples/python/insider_trades_to_csv.py --side buy --days 30 --min-value 100000
```

No key yet? The rare insider trades list is free without any account, as [JSON](https://oqro.io/rare-insider-trades/data.json), [CSV](https://oqro.io/rare-insider-trades/data.csv) or [RSS](https://oqro.io/rare-insider-trades/feed.xml):

```bash
curl -s https://oqro.io/rare-insider-trades/data.json | python3 -c "
import json, sys
for t in json.load(sys.stdin)['items'][:10]:
    print(t['ticker'], t['side'], round(t['amount_usd']), t['person'], '-', t['signals'][0]['text'])
"
```

API reference: [docs/rest-api.md](../docs/rest-api.md), <https://oqro.io/docs/api> and the OpenAPI file <https://oqro.io/openapi.json> (import it into Postman or a code generator).

## MCP server

The server is remote: `https://oqro.io/api/mcp`. Your client opens the OQRO sign-in the first time.

**Claude Code**

```bash
claude mcp add --transport http oqro https://oqro.io/api/mcp
```

**Cursor** (`~/.cursor/mcp.json`)

```json
{ "mcpServers": { "oqro": { "url": "https://oqro.io/api/mcp" } } }
```

**VS Code** (`.vscode/mcp.json`)

```json
{ "servers": { "oqro": { "type": "http", "url": "https://oqro.io/api/mcp" } } }
```

**Claude and ChatGPT (web and desktop):** add a custom connector with the URL above. Screens: <https://oqro.io/mcp>.

Then ask, for example: *"Which insider purchases this week stand out against that company's last 20 years of filings? Link each filing."* The 22 tools are listed in [LdwS123/oqro-mcp](https://github.com/LdwS123/oqro-mcp).

OQRO reports public filings. It is not investment advice.
