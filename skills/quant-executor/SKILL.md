---
name: quant-executor
description: No-hands autonomous executor for the live trading system. Use when asked about live vs paper mode, trade execution, position management, PAPER_MODE flag, keepalive cron, enabling live trading, checking open positions, or executor logs.
triggers:
  - "executor"
  - "paper mode"
  - "live trading"
  - "no hands"
  - "open position"
  - "trade fired"
  - "keepalive"
  - "flip to live"
  - "enable trading"
---

# Quant Executor Skill

## Key Files
```
no_hands_executor.py     # v3 — main executor (paper mode)
cft_paper.db             # paper trades table: paper_trades
logs/no_hands_live.log   # live output
no_hands_keepalive.sh    # cron restarter (every 1 min)
```

## Critical Constants (top of no_hands_executor.py)
```python
PAPER_MODE        = True    # ← FLIP TO FALSE only after 55% WR / 50 trades
SIMONS_THRESHOLD  = 70.0    # minimum edge score
SPREAD_MINIMUM    = 10.0    # LONG - SHORT gap
MAX_TRADES_PER_DAY = 2
MAX_POSITIONS     = 1
POSITION_SIZE     = 10.0    # $10 per trade
DAILY_LOSS_LIMIT  = 5.0     # $5 max daily loss
PAPER_SL_PCT      = 0.02    # 2% stop loss
PAPER_TP_PCT      = 0.05    # 5% take profit (2.5:1 R:R)
```

## Paper Trade Progress
```bash
cd /home/majinbu/organized/active-projects/trading-system/quant
python3 -c "
import sqlite3
conn = sqlite3.connect('cft_paper.db')
rows = conn.execute('SELECT symbol, direction, entry_price, exit_price, pnl, outcome, timestamp FROM paper_trades ORDER BY id').fetchall()
closed = [r for r in rows if r[4] is not None]
wins = sum(1 for r in closed if r[4] > 0)
wr = wins/len(closed)*100 if closed else 0
print(f'Trades: {len(closed)}/50 | WR: {wr:.0f}% | Need: 55%')
print(f'PnL: {sum(r[4] for r in closed):+.4f}')
"
```

## Enable Live Trading (when ready)
**Only flip after 50 paper trades at ≥55% WR:**
```bash
sed -i 's/PAPER_MODE = True/PAPER_MODE = False/' no_hands_executor.py
pkill -f no_hands_executor.py
bash no_hands_keepalive.sh
```

## Check Executor Status
```bash
ps aux | grep no_hands_executor | grep -v grep
tail -20 logs/no_hands_live.log | grep -E "SCANNING|SKIP|FIRE|PAPER|ERROR"
```

## Check Live Account
```bash
python3 -c "
import requests
r = requests.post('https://api.hyperliquid.xyz/info',
    json={'type':'clearinghouseState','user':'0xed63Aab89f2Eaf03998E66ABf90B3588F201d948'}, timeout=10)
d = r.json()
print(f'Balance: \${float(d[\"marginSummary\"][\"accountValue\"]):.4f}')
pos = [p for p in d.get('assetPositions',[]) if float(p['position']['szi']) != 0]
print(f'Open: {len(pos)} positions')
for p in pos:
    pi = p['position']
    print(f'  {pi[\"coin\"]} szi={pi[\"szi\"]} upnl={pi[\"unrealizedPnl\"]}')
"
```

## Force Restart Executor
```bash
pkill -f no_hands_executor.py
sleep 2
cd /home/majinbu/organized/active-projects/trading-system/quant
source .env
nohup python3 -u no_hands_executor.py >> logs/no_hands_live.log 2>&1 &
```

## Emergency Stop
```bash
pkill -f no_hands_executor.py
# Disable keepalive temporarily:
crontab -l | grep -v no_hands_keepalive | crontab -
```

## Keepalive Cron
```
* * * * *  /home/majinbu/.../no_hands_keepalive.sh >> /tmp/keepalive.log 2>&1
```
Checks every minute, restarts executor + hl_websocket_collector if dead.

## Live → Paper Mode Breakeven Math
- Current R:R = 2.5:1 (2% SL, 5% TP)
- Breakeven WR = 1/(1+2.5) = 28.6%
- Target WR = 55% for live trading
- **Previous system failure**: 39% WR + 1.1:1 R:R = guaranteed loss

## Account
- Address: `0xed63Aab89f2Eaf03998E66ABf90B3588F201d948`
- Balance: ~$39.47
- Mode: PAPER until 55% WR / 50 trades confirmed
