# Quick Reference - Cross-Chain Whale Monitoring

## Quick Start

```bash
# Navigate to monitoring directory
cd /home/majinbu/pi-mono-workspace/quant/monitoring

# Run tests (verify everything works)
python3 test_system.py

# Run full monitoring pipeline
python3 run_monitor.py

# Or run specific components
python3 run_monitor.py --mode eth    # Ethereum only
python3 run_monitor.py --mode sol    # Solana only
python3 run_monitor.py --mode cross  # Cross-chain analysis only
```

## Optional API Key

For better Ethereum monitoring, set Etherscan API key:

```bash
export ETHERSCAN_API_KEY=your_key_here
```

Get free API key: https://etherscan.io/apis

## Database Location

```
/home/majinbu/pi-mono-workspace/smart_money.db
```

## Files

| File | Purpose |
|------|---------|
| `database.py` | Database operations |
| `eth_monitor.py` | Ethereum whale tracker |
| `sol_monitor.py` | Solana whale tracker |
| `cross_chain_correlation.py` | Cross-chain analysis |
| `run_monitor.py` | Main execution script |
| `test_system.py` | Test suite |
| `schema.sql` | Database schema |
| `requirements.txt` | Dependencies |

## Thresholds

### Ethereum
- Minimum ETH: 10 ETH
- Minimum USD: $100,000

### Solana
- Minimum SOL: 1,000 SOL
- Minimum USD: $50,000

## Protocols Tracked

### Ethereum DEX
- Uniswap V2
- Uniswap V3
- 1inch
- Sushiswap
- Curve

### Solana DEX
- Jupiter
- Raydium
- Orca
- Serum

## Command Options

```bash
python3 run_monitor.py [OPTIONS]

Options:
  --mode {eth,sol,cross,full}  Monitoring mode (default: full)
  --hours INT                   Time window in hours (default: 24)
  --sol-limit INT              Transaction limit for Solana (default: 500)
```

## Examples

```bash
# Monitor last 7 days
python3 run_monitor.py --hours 168

# Monitor last 12 hours
python3 run_monitor.py --hours 12

# ETH monitoring with more transactions
python3 run_monitor.py --mode eth --hours 48

# Quick test with 1 hour window
python3 run_monitor.py --hours 1
```

## Database Queries

You can query the database directly:

```bash
sqlite3 /home/majinbu/pi-mono-workspace/smart_money.db

# Example queries:
.tables                              # List all tables
SELECT * FROM whale_wallets LIMIT 10;
SELECT * FROM eth_whale_txs ORDER BY timestamp DESC LIMIT 10;
SELECT * FROM sol_whale_txs ORDER BY timestamp DESC LIMIT 10;
SELECT * FROM cross_chain_events WHERE correlation_score > 0.7;
SELECT * FROM whale_alerts WHERE is_resolved = 0;
```

## Troubleshooting

### Etherscan API Errors
- Set API key: `export ETHERSCAN_API_KEY=your_key`
- Without key, rate limits are stricter

### Solana RPC Issues
- System uses multiple RPC endpoints with automatic failover
- If all fail, try again later

### Database Issues
- Database auto-initializes on first run
- Check permissions: `ls -la smart_money.db`
- Reset database: `rm smart_money.db` (will recreate on next run)

## Getting Help

- Check README.md for detailed documentation
- Check IMPLEMENTATION_SUMMARY.md for architecture details
- Run `test_system.py` to verify installation

## Key Metrics

After running, check these in the output:
- ETH whale wallets discovered
- SOL whale wallets discovered
- ETH transactions collected
- SOL transactions collected
- Cross-chain events detected
- Whale alerts generated

## Next Steps

1. Set up cron job for regular monitoring:
   ```bash
   # Run every 6 hours
   0 */6 * * * cd /home/majinbu/pi-mono-workspace/quant/monitoring && /usr/bin/python3 run_monitor.py >> /var/log/whale_monitor.log 2>&1
   ```

2. Set up alerts (extend the code to send to Telegram/Discord/Slack)

3. Add more whale addresses to seed lists in `eth_monitor.py` and `sol_monitor.py`

4. Monitor the database growth and consider backup strategy
