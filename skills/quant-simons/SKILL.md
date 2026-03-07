---
name: quant-simons
description: 14-model Simons RBI scoring engine for the live trading system. Use when asked to check signal scores, analyze why a trade didn't fire, tune model weights, debug scoring logic, or understand what's blocking a paper trade. Covers rbi_agent_simons.py, model weights, Hurst regime filter, and polypigeon integration.
triggers:
  - "simons score"
  - "why didn't it fire"
  - "signal score"
  - "model weights"
  - "hurst"
  - "edge score"
  - "rbi simons"
  - "scoring"
---

# Quant Simons Skill

## System Location
```
/home/majinbu/organized/active-projects/trading-system/quant/
├── rbi_agent_simons.py          # 14-model ensemble (1400+ lines)
├── cmlkevin_polypigeon_integration.py  # Hurst/VPIN/variance ratio
├── realtime_trades.db           # trade_buckets, large_trades (WS feed)
├── whale_deltas.db              # snapshots, deltas (hourly)
├── funding_oi.db                # snapshots, regime_signals
└── logs/no_hands_live.log       # live scoring output
```

## 14-Model Ensemble Weights

| # | Model | Weight | Source |
|---|-------|--------|--------|
| 1 | z_score | 13% | realtime_trades.db / price history |
| 2 | momentum | 10% | EMA9/EMA21/ROC from candles |
| 3 | microstructure | 8% | hl_websocket_collector → trade_buckets |
| 4 | funding_divergence | 11% | HL vs Binance/Bybit/OKX |
| 5 | whale_delta | 10% | whale_deltas.db (28 tracked whales) |
| 6 | liquidation_dir | 9% | Binance liq WebSocket |
| 7 | imbalance_mtf | 8% | MoonDev API → local trade_buckets fallback |
| 8 | volume | 5% | trade_buckets |
| 9 | volatility | 3% | ATR from candles |
| 10 | oi_divergence | 5% | funding_oi.db |
| 11 | hlp_liquidator | 5% | HL clearinghouseState (3 addresses) |
| 12 | gj_macro | 5% | Polymarket + ORACLE forecaster |
| 13 | on_chain_flow | 5% | HL bridge transfers |
| 14 | hurst_mr | 3% | polypigeon Hurst exponent |

**Total: 100%**

## Firing Thresholds
```python
SIMONS_THRESHOLD = 70.0   # score must exceed this
SPREAD_MINIMUM   = 10.0   # LONG_score - SHORT_score gap
MAX_TRADES_PER_DAY = 2
MAX_POSITIONS    = 1
```

## Hurst Regime Filter (Model 14)
- H < 0.45 → MEAN_REVERTING → score 70-85%
- H 0.45-0.55 → RANDOM_WALK → score ~37-50% (penalized)
- H > 0.55 → TRENDING → score ~50-60%
- **Key insight**: BTC/ETH in random walk regime = mean-reversion fails

## Check Current Scores
```bash
cd /home/majinbu/organized/active-projects/trading-system/quant
tail -100 logs/no_hands_live.log | grep -E "(BTC:|ETH:|SOL:).*(spread|LONG|SHORT)"
```

## Full Breakdown for One Asset
```bash
tail -300 logs/no_hands_live.log | grep -A 45 "SIMONS ANALYSIS: SOL LONG"
```

## Why Didn't It Fire — Diagnosis
```bash
# Get scores and compute gap
python3 -c "
import re
lines = open('logs/no_hands_live.log').readlines()[-200:]
for line in lines:
    if 'contrib:' in line:
        print(line.rstrip())
"
```

## MoonDev Key Update (rotates daily)
```bash
# Update key in .env
sed -i 's/MOONDEV_API_KEY=.*/MOONDEV_API_KEY=moonstream_NEWKEY/' .env
# All 4 usages auto-read via _load_moondev_key()
```

## Data Feed Health Check
```bash
python3 -c "
import sqlite3
from datetime import datetime
for db, table in [('realtime_trades.db','trade_buckets'),
                  ('whale_deltas.db','snapshots'),
                  ('funding_oi.db','snapshots')]:
    conn = sqlite3.connect(db)
    last = conn.execute(f'SELECT MAX(timestamp) FROM {table}').fetchone()[0]
    print(f'{db}: last={str(last)[:16]}')
    conn.close()
"
```

## Common Issues

| Issue | Cause | Fix |
|-------|-------|-----|
| imbalance_mtf stuck at 50% | MoonDev 401 + local DB stale | Restart hl_websocket_collector.py |
| hurst_mr returning 37% | BTC/ETH in random walk | Correct — don't trade those assets |
| microstructure 35% | Bearish order flow | Real signal — wait for reversal |
| whale_delta stuck at 50% | No delta events in 24h | Normal when market quiet |
| Score 63% but spread 15% | Score gate, not spread gate | Need more model alignment |
