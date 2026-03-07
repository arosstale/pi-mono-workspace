---
name: quant-data-infra
description: Data collection infrastructure for the quant trading system. Use when asked about data collectors, websocket feeds, database health, MoonDev API, whale tracking, funding rates, liquidation data, or the realtime_trades/whale_deltas/funding_oi databases.
triggers:
  - "data collector"
  - "websocket collector"
  - "realtime trades"
  - "whale delta"
  - "funding oi"
  - "moondev api"
  - "binance liquidation"
  - "data health"
  - "collector dead"
  - "stale data"
---

# Quant Data Infrastructure Skill

## Collector Processes

| Process | DB | Table | Keepalive |
|---------|-----|-------|-----------|
| `hl_websocket_collector.py` | realtime_trades.db | trade_buckets, large_trades | ws_keepalive.sh (*/5 cron) |
| `own_data_infra/whale_collector.py` | whale_deltas.db | snapshots, deltas | systemd |
| `own_data_infra/binance_liq_collector.py` | binance_liquidations.db | liquidations | systemd |
| `polymarket_poller.py` | gj_signals.db | polymarket_events | cron */30 |
| `funding_oi_tracker.py` | funding_oi.db | snapshots, regime_signals | cron :05 |
| `moondev_snapshot_collector.py` | moondev_history.db | snapshots | cron :10 |

## Data Health Check (all at once)
```bash
cd /home/majinbu/organized/active-projects/trading-system/quant
python3 -c "
import sqlite3, os
from datetime import datetime
checks = [
    ('realtime_trades.db', 'trade_buckets', 'bucket_start'),
    ('whale_deltas.db', 'snapshots', 'timestamp'),
    ('funding_oi.db', 'snapshots', 'timestamp'),
    ('binance_liquidations.db', 'liquidations', 'timestamp'),
    ('gj_signals.db', 'polymarket_events', 'timestamp'),
]
for db, table, ts_col in checks:
    if not os.path.exists(db):
        print(f'MISSING: {db}')
        continue
    conn = sqlite3.connect(db)
    try:
        n = conn.execute(f'SELECT COUNT(*) FROM {table}').fetchone()[0]
        last = conn.execute(f'SELECT MAX({ts_col}) FROM {table}').fetchone()[0]
        age_mins = (datetime.utcnow() - datetime.fromisoformat(str(last)[:19])).seconds//60 if last else 9999
        status = '✅' if age_mins < 10 else '⚠️' if age_mins < 60 else '❌'
        print(f'{status} {db}: {n} rows, {age_mins}m ago')
    except Exception as e:
        print(f'ERR {db}: {e}')
    conn.close()
"
```

## Start hl_websocket_collector
```bash
cd /home/majinbu/organized/active-projects/trading-system/quant
nohup python3 -u hl_websocket_collector.py >> logs/ws_collector.log 2>&1 &
# Tracks: BTC, ETH, SOL, HYPE, XRP
# Writes: 1-min trade buckets + large trades (>$100K)
# Safety: 7-day retention, 100MB max
```

## realtime_trades.db Schema
```sql
trade_buckets(id, timestamp, coin, bucket_start,
              buy_volume, sell_volume, buy_count, sell_count,
              net_delta, vwap, high, low, trade_count)
large_trades(id, timestamp, coin, side, size, price, notional)
```

## SOL Imbalance (own data, no MoonDev needed)
```bash
python3 -c "
import sqlite3
from datetime import datetime, timedelta
conn = sqlite3.connect('realtime_trades.db')
for mins, label in [(5,'5m'),(15,'15m'),(60,'1h'),(240,'4h')]:
    since = (datetime.utcnow()-timedelta(minutes=mins)).isoformat()
    r = conn.execute('SELECT SUM(buy_volume),SUM(sell_volume) FROM trade_buckets WHERE coin=? AND bucket_start>=?',('SOL',since)).fetchone()
    if r[0]:
        ratio = (r[0]-r[1])/(r[0]+r[1])
        print(f'{label}: {ratio:+.3f} (buy={r[0]:,.0f} sell={r[1]:,.0f})')
conn.close()
"
```

## MoonDev API Key
- **Rotates daily** — get from https://moondev.com/quantapp
- After Thursday: Discord/email
- Update: `sed -i 's/MOONDEV_API_KEY=.*/MOONDEV_API_KEY=moonstream_NEWKEY/' .env`
- All simons models read via `_load_moondev_key()` — no hardcodes

## whale_deltas.db — Whale Signal
```bash
python3 -c "
import sqlite3
conn = sqlite3.connect('whale_deltas.db')
# Recent covering events (shorts closing = bullish)
rows = conn.execute('''SELECT coin, delta_type, delta_size, timestamp
    FROM deltas WHERE timestamp > datetime('now','-24 hours')
    AND delta_type='covering' ORDER BY timestamp DESC LIMIT 10''').fetchall()
for r in rows: print(r)
conn.close()
"
```

## Binance Liquidations (own WebSocket, no API key)
```bash
# Collector: own_data_infra/binance_liq_collector.py
python3 -c "
import sqlite3
conn = sqlite3.connect('binance_liquidations.db')
rows = conn.execute('''SELECT symbol, side, quantity, price, timestamp
    FROM liquidations ORDER BY id DESC LIMIT 10''').fetchall()
for r in rows: print(r)
conn.close()
"
```

## ORACLE Forecaster
```bash
# Manual run (uses MiniMax M2.5 coding plan — free)
cd /home/majinbu/organized/active-projects/trading-system/quant
python3 run_oracle_forecast.py
# Nightly cron: 23:00 UTC
# DB: oracle_forecasts.db
```

## Cron Schedule
```
* * * * *    no_hands_keepalive.sh
*/5 * * * *  ws_keepalive.sh
*/30 * * * * polymarket_poller.py
0 * * * *    whale_delta_tracker.py
5 * * * *    funding_oi_tracker.py
10 * * * *   moondev_snapshot_collector.py
0 23 * * *   run_oracle_forecast.py
```
