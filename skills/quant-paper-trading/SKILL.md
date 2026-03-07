---
name: quant-paper-trading
description: Paper trading validation system for the quant trading system. Use when asked about paper trade results, WR progress toward live trading, paper bot performance, strategy validation, or comparing strategies. Covers cft_paper.db, 26 systemd paper bots, and the 55% WR gate.
triggers:
  - "paper trade"
  - "paper results"
  - "win rate"
  - "paper bot"
  - "WR progress"
  - "strategy performance"
  - "55% WR"
  - "ready to go live"
  - "paper stats"
---

# Quant Paper Trading Skill

## The 55% WR Gate
**Live trading is DISABLED until:**
- ≥50 paper trades completed (in `cft_paper.db → paper_trades`)
- ≥55% win rate over those 50 trades
- **Why 55%**: at 2.5:1 R:R, breakeven is 28.6%. 55% = strong edge confirmation.

**Previous system failure**: 39% WR + 1.1:1 R:R = -$20 in 7 days (553 trades)

## Check no_hands Paper Progress
```bash
cd /home/majinbu/organized/active-projects/trading-system/quant
python3 -c "
import sqlite3
conn = sqlite3.connect('cft_paper.db')
rows = conn.execute('''SELECT symbol, direction, entry_price, exit_price, pnl, outcome, timestamp
                       FROM paper_trades ORDER BY id''').fetchall()
closed = [r for r in rows if r[4] is not None]
open_pos = [r for r in rows if r[4] is None]
wins = sum(1 for r in closed if r[4] > 0)
wr = wins/len(closed)*100 if closed else 0
total_pnl = sum(r[4] for r in closed)
print(f'Closed: {len(closed)}/50 | WR: {wr:.0f}% | PnL: {total_pnl:+.4f}')
print(f'Open: {len(open_pos)}')
for r in closed[-10:]:
    icon = 'W' if r[4]>0 else 'L'
    print(f'  [{icon}] {r[6][:16]} {r[0]} {r[1]} e={r[2]:.2f} x={r[3]:.2f} {r[4]:+.4f}')
conn.close()
"
```

## All Paper Bot P&L (systemd bots)
```bash
for svc in paper-megacombo-scalp paper-megacombo-sol paper-mr-bb-eth \
           paper-original-mega paper-parabolic-liq paper-rbi-cluster-fader \
           paper-rbi-divergence paper-rbi-vol-accel paper-regime-liq \
           paper-rsi-accel-liq paper-smart-divergence paper-stochastic-liq \
           paper-vpin-fade paper-liq-cascade paper-liq-cascade-timing \
           paper-mean-reversion paper-elite-cluster paper-elite-copybot \
           paper-funding-regime paper-hlp-flip paper-bbpctb-liq \
           paper-composite-signal paper-donchian-liq paper-volume-profile \
           paper-rbi-dynamic-accel; do
    line=$(journalctl -u $svc --no-pager -n 1 2>/dev/null | grep -oE "PnL=\\\$[+\-][0-9.]+ \| W/L=[0-9]+/[0-9]+ \| trades=[0-9]+" | tail -1)
    [ -n "$line" ] && echo "$svc: $line"
done
```

## Active Paper Bots
| Bot | Status | Notes |
|-----|--------|-------|
| paper-rbi-divergence | ✅ running | Best: +$2.26, 47% WR, 32t |
| paper-rbi-cluster-fader | ✅ running | -$1.25, 47% WR, 38t |
| paper-rbi-dynamic-accel | ❌ stopped | 28% WR, 190t — killed |
| paper-vpin-fade | ✅ running | 0 trades yet |
| paper-megacombo-* | ✅ running | Checking |

## Strategy Kill Criteria
Stop any paper bot that hits:
- WR < 40% over ≥50 trades
- Total loss > $10 paper
- Trade rate > 20/day (overtrading signal)

```bash
systemctl stop paper-BOT-NAME
systemctl disable paper-BOT-NAME
```

## New Paper Strategy Template
```bash
# 1. Create strategy file
# 2. Add systemd service to /etc/systemd/system/paper-STRATEGY.service
# 3. systemctl daemon-reload && systemctl enable --now paper-STRATEGY
# 4. Monitor for 50 trades before any conclusions
```

## Systemd Service Template
```ini
[Unit]
Description=Paper Trading - STRATEGY_NAME
After=network.target

[Service]
Type=simple
User=majinbu
WorkingDirectory=/home/majinbu/organized/active-projects/trading-system/quant
ExecStart=/usr/bin/python3 paper_STRATEGY.py
Restart=always
RestartSec=30

[Install]
WantedBy=multi-user.target
```

## Promotion to Live
When no_hands paper hits 55% WR / 50 trades:
```bash
# 1. Verify stats
python3 -c "import sqlite3; ..."  # confirm numbers

# 2. Flip the flag
sed -i 's/PAPER_MODE = True/PAPER_MODE = False/' no_hands_executor.py

# 3. Set conservative live size
sed -i 's/POSITION_SIZE = 10.0/POSITION_SIZE = 10.0/' no_hands_executor.py  # keep $10

# 4. Restart
pkill -f no_hands_executor.py
bash no_hands_keepalive.sh
```
