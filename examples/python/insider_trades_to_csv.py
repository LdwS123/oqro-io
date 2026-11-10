"""Download insider trades from the free OQRO REST API into a CSV file.

Usage:
    export OQRO_API_KEY=oqro_...        # free key: oqro.io, account, API keys
    python insider_trades_to_csv.py --side buy --days 30 --min-value 100000
    python insider_trades_to_csv.py --ticker NVDA --side sell --days 180

Needs Python 3.9+ and `requests` (pip install requests).
Every row keeps `source_url` (the SEC filing) and `oqro_url` (the OQRO page).
"""

import argparse
import csv
import os
import sys
import time

import requests

BASE = "https://oqro.io/api/v1"


def fetch_all(params, max_rows):
    headers = {"Authorization": f"Bearer {os.environ['OQRO_API_KEY']}"}
    rows, cursor = [], None
    while len(rows) < max_rows:
        page = dict(params, limit=100)
        if cursor:
            page["cursor"] = cursor
        r = requests.get(f"{BASE}/insider-trades", params=page, headers=headers, timeout=30)
        if r.status_code == 429:  # over the rate limit: wait as told, then retry
            time.sleep(int(r.headers.get("Retry-After", "5")))
            continue
        r.raise_for_status()
        body = r.json()
        rows.extend(body["data"])
        cursor = (body.get("pagination") or {}).get("next_cursor")
        if not cursor:
            break
    return rows[:max_rows]


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--ticker")
    ap.add_argument("--side", choices=["buy", "sell"])
    ap.add_argument("--days", type=int, default=90)
    ap.add_argument("--min-value", type=float)
    ap.add_argument("--max-rows", type=int, default=1000)
    ap.add_argument("--out", default="insider_trades.csv")
    a = ap.parse_args()

    if "OQRO_API_KEY" not in os.environ:
        sys.exit("Set OQRO_API_KEY first. Create a free key at https://oqro.io (account, API keys).")

    params = {"days": a.days}
    if a.ticker:
        params["ticker"] = a.ticker.upper()
    if a.side:
        params["side"] = a.side
    if a.min_value:
        params["min_value"] = a.min_value

    rows = fetch_all(params, a.max_rows)
    if not rows:
        print("No trades match these filters.")
        return

    fields = []
    for row in rows:  # keep every column the API returns, in first-seen order
        fields += [k for k in row if k not in fields]
    with open(a.out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)
    print(f"Wrote {len(rows)} trades to {a.out}")


if __name__ == "__main__":
    main()
