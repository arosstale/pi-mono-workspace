# Smart Money Confidence Score

A unified confidence score system for measuring wallet behavior quality. Focuses on the quality of smart money, not just quantity.

## Overview

The Smart Money Confidence Score (0-100) evaluates wallet performance across five weighted factors:

1. **Win Rate (30%)** - Percentage of profitable trades
2. **Trade Count (10%)** - Number of trades (more data = higher confidence)
3. **Average Notional (20%)** - Average trade size (skin in the game)
4. **Consistency (25%)** - Stability of win rate over time
5. **Market Timing (15%)** - Tendency to buy low and sell high

## Score Categories

| Category | Range | Description |
|----------|-------|-------------|
| ELITE | 90-100 | Top 1% - Exceptional smart money |
| STRONG | 75-89 | Top 5% - Very reliable smart money |
| MODERATE | 60-74 | Top 20% - Above average |
| WEAK | 40-59 | Below average |
| POOR | 0-39 | Unreliable |

## Installation

```bash
cd /home/majinbu/pi-mono-workspace/quant
```

## Database Setup

Ensure your database has the required tables:

```bash
# Create database and tables
python -c "
import sqlite3
conn = sqlite3.connect('data/trading.db')
cursor = conn.cursor()

# Create agent_trades table (if not exists)
cursor.execute('''
CREATE TABLE IF NOT EXISTS agent_trades (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    agent_id TEXT NOT NULL,
    model TEXT NOT NULL,
    symbol TEXT NOT NULL,
    side TEXT NOT NULL,
    order_type TEXT NOT NULL,
    quantity REAL NOT NULL,
    entry_price REAL NOT NULL,
    exit_price REAL,
    stop_loss REAL,
    take_profit REAL,
    pnl REAL DEFAULT 0,
    pnl_percent REAL DEFAULT 0,
    status TEXT DEFAULT 'open',
    entry_timestamp INTEGER NOT NULL,
    exit_timestamp INTEGER,
    reasoning TEXT,
    metadata TEXT,
    execution_time_ms INTEGER,
    is_paper_trade BOOLEAN DEFAULT 1,
    created_at INTEGER DEFAULT (strftime('%s', 'now'))
)
''')

conn.commit()
conn.close()
print('Database initialized successfully.')
"
```

## Usage

### 1. Calculate Confidence for a Single Wallet

```python
from signals.smart_money_confidence import (
    SmartMoneyConfidenceCalculator,
    recalculate_wallet_confidence
)

# Initialize calculator
calculator = SmartMoneyConfidenceCalculator('data/trading.db')

# Calculate confidence for a wallet
score = calculator.calculate_confidence('0x1234567890abcdef', days=30)

print(f"Overall Score: {score.overall_score}")
print(f"Category: {score.category.value}")
print(f"Trend: {score.trend}")

# Save to database
calculator.save_confidence_score(score)
```

### 2. Recalculate After Trade Fill (Real-time)

```python
# Call this function after each trade fill
from signals.smart_money_confidence import recalculate_wallet_confidence

score = recalculate_wallet_confidence(
    wallet_address='0x1234567890abcdef',
    db_path='data/trading.db',
    days=30
)
```

### 3. Get Latest Scores for All Wallets

```python
calculator = SmartMoneyConfidenceCalculator('data/trading.db')

# Get top 100 wallets by confidence score
latest_scores = calculator.get_latest_confidence_scores(limit=100)

for score in latest_scores:
    print(f"{score.wallet_address}: {score.overall_score} ({score.category.value})")
```

### 4. Get Elite Wallets

```python
# Get elite wallets (score >= 90) not in decline
elite_wallets = calculator.get_elite_wallets(threshold=90.0, check_decline=True)

print(f"Elite Wallets: {len(elite_wallets)}")
for wallet in elite_wallets:
    print(f"{wallet.wallet_address}: {wallet.overall_score}")
```

### 5. Get Wallet History

```python
# Get 30-day confidence history for a wallet
history = calculator.get_wallet_history('0x1234567890abcdef', days=30)

for score in history:
    print(f"{score.calculated_at}: {score.overall_score}")
```

## API Server

Start the API server:

```bash
export TRADING_DB_PATH='quant/data/trading.db'
python api/smart_money_confidence_api.py
```

The API will be available at `http://localhost:5001`

### API Endpoints

#### Get All Confidence Scores
```
GET /api/v1/smart-money-confidence?limit=100&category=ELITE
```

#### Get Specific Wallet Confidence
```
GET /api/v1/smart-money-confidence/{wallet_address}?days=30
```

#### Get Elite Wallets
```
GET /api/v1/smart-money-confidence/elite?threshold=90.0&check_decline=true
```

#### Get Wallet History
```
GET /api/v1/smart-money-confidence/{wallet_address}/history?days=30
```

#### Recalculate Confidence
```
POST /api/v1/smart-money-confidence/recalculate
Content-Type: application/json

{
  "wallet_address": "0x123...",
  "days": 30,
  "save": true
}
```

#### Get Alerts
```
GET /api/v1/smart-money-confidence/alerts?threshold=90.0&drop_threshold=10.0
```

#### Health Check
```
GET /health
```

## Report Generation

Generate daily confidence report:

```python
from reports.smart_money_confidence_report import generate_daily_report

report_path = generate_daily_report(
    output_dir='reports',
    db_path='data/trading.db'
)

print(f"Report generated: {report_path}")
```

Or run directly:

```bash
python reports/smart_money_confidence_report.py
```

The report will be saved as `reports/smart_money_confidence_YYYYMMDD.md`

## Report Contents

Each report includes:

- **Summary Statistics** - Total wallets, category distribution, average scores
- **Category Breakdown** - Detailed breakdown by score category
- **Elite Rankings** - Top 1% elite wallets ranked by score
- **Top Performers** - Best wallets by component (win rate, consistency, timing, activity)
- **Recent Changes** - Wallets with significant score changes
- **Trends Analysis** - Wallets approaching elite status, at-risk wallets
- **Alerts** - Elite wallets with significant confidence declines

## Integration with Trading System

### Real-time Updates

After each trade fill, call the recalculation function:

```python
# In your trade execution system
def on_trade_filled(wallet_address, trade_details):
    # Save trade to database
    save_trade_to_database(wallet_address, trade_details)

    # Recalculate confidence score
    recalculate_wallet_confidence(
        wallet_address=wallet_address,
        db_path='data/trading.db',
        days=30
    )

    # Check for elite wallet decline alerts
    check_elite_wallet_alerts()
```

### Alert System

```python
from signals.smart_money_confidence import SmartMoneyConfidenceCalculator

def check_elite_wallet_alerts():
    calculator = SmartMoneyConfidenceCalculator('data/trading.db')
    elite_wallets = calculator.get_elite_wallets(threshold=90.0, check_decline=False)

    declining_elite = [w for w in elite_wallets if w.trend == 'down']

    for wallet in declining_elite:
        # Get recent history to check for significant drop
        history = calculator.get_wallet_history(wallet.wallet_address, days=7)

        if len(history) >= 2:
            previous = history[-2].overall_score
            current = wallet.overall_score
            drop = previous - current

            if drop >= 10:  # Significant decline
                send_alert(
                    wallet_address=wallet.wallet_address,
                    previous_score=previous,
                    current_score=current,
                    drop=drop
                )
```

## Monitoring and Automation

### Daily Cron Job

Add to crontab to generate daily reports:

```bash
# Run at 8:00 AM UTC every day
0 8 * * * cd /home/majinbu/pi-mono-workspace/quant && python reports/smart_money_confidence_report.py
```

### Batch Recalculation

Recalculate all wallets periodically:

```python
from signals.smart_money_confidence import get_all_wallet_confidences

# Recalculate confidence for all active wallets
scores = get_all_wallet_confidences(
    db_path='data/trading.db',
    days=30
)

print(f"Updated {len(scores)} wallet confidence scores")
```

## Key Features

1. **Multi-factor Scoring** - Combines 5 weighted factors for comprehensive evaluation
2. **Real-time Updates** - Recalculates after each trade fill
3. **Trend Tracking** - Monitors if wallets are improving or declining
4. **Category Classification** - Simple 5-tier classification system
5. **Alert System** - Notifies when elite wallets decline significantly
6. **Historical Analysis** - Tracks confidence over time
7. **REST API** - Easy integration with external systems
8. **Daily Reports** - Automated markdown reports for analysis

## Data Requirements

The system requires the following data in your database:

- `agent_trades` table with columns:
  - `agent_id` - Wallet address
  - `symbol` - Trading pair
  - `side` - 'buy' or 'sell'
  - `quantity` - Trade quantity
  - `entry_price` - Entry price
  - `exit_price` - Exit price (for closed trades)
  - `pnl` - Profit/loss
  - `status` - 'open' or 'closed'
  - `entry_timestamp` - Unix timestamp of entry
  - `exit_timestamp` - Unix timestamp of exit (optional)

## Notes

- Minimum 3 days of trading activity required for consistency score
- Minimum 3 trades per day for daily consistency metrics
- Scores are more reliable with longer trading history
- Market timing analysis is simplified and may not capture all nuances
- Consider scores alongside other metrics for complete analysis

## Support

For issues or questions, refer to the main documentation or contact the development team.
