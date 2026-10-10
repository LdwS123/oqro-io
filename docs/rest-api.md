# OQRO REST API

Read-only JSON for insider trades, politician trades (Congress), 13F fund moves, federal contracts, lobbying, prices and a screener. Every row carries `source_url` (the official record) and `oqro_url` (the matching OQRO page). It is the same data as the [MCP server](https://github.com/LdwS123/oqro-mcp), for your own code.

- **Base URL:** `https://oqro.io/api/v1`
- **Access:** part of OQRO Pro. Every request needs an API key from a member account with an active subscription. Full, current reference: <https://oqro.io/docs/api>.

## Authentication

Create a key in your account (API keys), name it and copy it: it is shown once. Send it as `Authorization: Bearer oqro_...` or in an `X-API-Key` header (if both are present, `Authorization` wins). Keys are personal and act for your account; the API stops answering if the subscription ends. You can hold 5 active keys. Call the API from servers or notebooks, never from a web page or distributed app: CORS headers are not sent, on purpose.

```bash
export OQRO_API_KEY=oqro_...
curl "https://oqro.io/api/v1/insider-trades?ticker=NVDA&side=sell&days=180&limit=5" \
  -H "Authorization: Bearer $OQRO_API_KEY"
```

```python
import os, requests

r = requests.get(
    "https://oqro.io/api/v1/insider-trades",
    params={"ticker": "NVDA", "side": "sell", "days": 180, "limit": 5},
    headers={"Authorization": f"Bearer {os.environ['OQRO_API_KEY']}"},
    timeout=30,
)
r.raise_for_status()
for row in r.json()["data"]:
    print(row)
```

All endpoints are `GET`. Responses are JSON and are never cached. Lists are paginated: send the previous page's `pagination.next_cursor` back as `cursor`, unchanged, with the same filters.

## Endpoints

| Endpoint | What it returns |
|---|---|
| `GET /companies/search?q=` | Covered companies by ticker or part of a name (up to 20). |
| `GET /companies/{ticker}` | Profile, latest close and 12-month change next to the S&P 500, annual revenue and net income from SEC filings, latest FINRA short interest, counts of recent disclosures. |
| `GET /insider-trades` | SEC Form 4 trades (open-market purchases and sales by default) or Form 144 notices. Filters: `ticker`, `side`, `kind`, `days`, `min_value`, `limit`, `cursor`. |
| `GET /congress-trades` | Trades disclosed by members of Congress, official amount ranges. Filters: `ticker`, `member`, `side`, `days`, `limit`, `cursor`. |
| `GET /fund-moves` | Position changes in SEC Form 13F. Filters: `ticker`, `fund`, `change` (new, increased, reduced, exited), `limit`, `cursor`. |
| `GET /contracts` | Prime federal contract awards (USAspending.gov). Filters: `ticker`, `days`, `min_amount`, `limit`, `cursor`. |
| `GET /lobbying?ticker=` | Federal lobbying spend from LDA reports; quarter totals in `meta.quarter_totals`. |
| `GET /prices/{ticker}` | Daily, weekly or monthly closes next to the S&P 500 (`days`, `interval`, `include_sp500`). |
| `GET /screen` | Filter and sort about 850 covered companies on published numbers (price change, distance from the 12-month high, market value, revenue, profit, free cash flow, net debt, short interest, disclosed buying). |
| `GET /export` | Events as CSV (UTF-8 with BOM), up to 1,000 rows a page and 10,000 per query. |

The exact parameters, limits and examples of each endpoint are in the live reference: <https://oqro.io/docs/api>.

OQRO reports public filings and is not investment advice.
