# Cross-Chain Whale Monitoring System

A proof-of-concept system for tracking whale movements across Ethereum and Solana blockchains.

## Features

### Ethereum Monitoring
- Tracks wallets with >$100K ETH transactions
- Monitors large transfers (>10 ETH)
- Detects DEX swaps (Uniswap, 1inch)
- Tracks smart contract interactions
- Uses Etherscan free tier API (5 calls/second)

### Solana Monitoring
- Tracks wallets with >$50K SOL transactions
- Monitors large transfers (>1,000 SOL)
- Detects DEX swaps (Jupiter, Raydium, Orca)
- Tracks program interactions
- Uses public RPC endpoints (no API key required)

### Cross-Chain Correlation
- Identifies potential wallet mappings across chains
- Detects bridge-like movements via timing and amount analysis
- Calculates correlation scores between chain activities
- Generates alerts for high-confidence cross-chain movements

## Installation

1. Install dependencies:
```bash
cd /home/majinbu/pi-mono-workspace/quant/monitoring
pip install -r requirements.txt
```

2. (Optional) Set Etherscan API key:
```bash
export ETHERSCAN_API_KEY=your_api_key_here
```
Without an API key, Etherscan free tier is used with limited rate limits.

## Usage

### Run full monitoring pipeline (recommended):
```bash
python run_monitor.py
```

### Run specific chain monitors:
```bash
# Ethereum only
python run_monitor.py --mode eth

# Solana only
python run_monitor.py --mode sol

# Cross-chain analysis only
python run_monitor.py --mode cross
```

### Adjust time window:
```bash
# Last 7 days
python run_monitor.py --hours 168

# Last 12 hours
python run_monitor.py --hours 12
```

## Database Schema

### Tables

**whale_wallets**
- Tracks addresses across ETH and SOL chains
- Includes transaction volume, count, and activity status

**cross_chain_mappings**
- Maps ETH addresses to SOL addresses
- Stores correlation scores and confidence levels

**eth_whale_txs**
- Ethereum whale transactions
- Includes transaction type, protocol, and USD values

**sol_whale_txs**
- Solana whale transactions
- Includes transaction type, protocol, and USD values

**cross_chain_events**
- Cross-chain correlation events
- Links ETH and SOL transactions

**whale_alerts**
- Alerts for significant whale activity
- Includes large transfers, cross-chain moves, unusual patterns

## Database Location

Database is stored at: `/home/majinbu/pi-mono-workspace/smart_money.db`

## Individual Scripts

### eth_monitor.py
```bash
python eth_monitor.py
```
Monitors Ethereum whale transactions using Etherscan API.

### sol_monitor.py
```bash
python sol_monitor.py
```
Monitors Solana whale transactions using public RPC.

### cross_chain_correlation.py
```bash
python cross_chain_correlation.py
```
Analyzes cross-chain correlations and generates alerts.

## Limitations

### Known Whale Wallets
The system starts with a small seed list of whale wallets. In production, you would:
1. Add more known whale addresses
2. Continuously discover new whales from large transactions
3. Maintain a curated whale list

### Cross-Chain Mapping
True cross-chain wallet mapping requires:
1. Bridge transaction analysis (Portal, Wormhole, etc.)
2. Social media link scraping
3. Subgraph queries for on-chain attestations
4. ENS + domain name correlation

The current implementation uses heuristics (timing, volume, activity patterns).

### Rate Limiting
- Etherscan: 5 calls/second (free tier)
- CoinGecko (SOL price): ~10-30 calls/minute
- Solana RPCs: Varies by endpoint

The monitors include rate limiting to avoid hitting these limits.

## API Keys

### Etherscan (Optional)
Get free API key: https://etherscan.io/apis
Free tier: 5 calls/second, 100,000 calls/day

Set via environment variable:
```bash
export ETHERSCAN_API_KEY=your_key_here
```

Without API key, the system uses the public endpoint with stricter rate limits.

## Future Enhancements

1. **Real-time monitoring**: Run monitors as daemon processes with cron
2. **Webhook alerts**: Send alerts to Telegram, Discord, or Slack
3. **Bridge integration**: Direct integration with Portal, Wormhole, Allbridge
4. **ML-based correlation**: Use machine learning for better cross-chain mapping
5. **Dashboard**: Web interface for visualizing whale movements
6. **Historical backfill**: Archive historical data for trend analysis
7. **Multi-chain expansion**: Add BSC, Polygon, Arbitrum, Optimism

## Example Output

```
============================================================
CROSS-CHAIN WHALE MONITORING PIPELINE
Time window: Last 24 hours
Started: 2026-02-16T18:00:00
============================================================

============================================================
ETHEREUM WHALE MONITORING
============================================================
Monitoring ETH wallet: 0x47ac0Fb4F2D84898e4D9E7b4DaB3C24507a6D503
  Found 15 whale transactions
...

============================================================
SOLANA WHALE MONITORING
============================================================
Monitoring SOL wallet: 7RCz8Z1QDgkzF7yVz5pC2B9p8G3qL4wX6Y9nN1vM2PjK
  Found 8 whale transactions
...

============================================================
CROSS-CHAIN CORRELATION ANALYSIS
============================================================
...

============================================================
PIPELINE SUMMARY
============================================================
Ethereum:
  Wallet transactions: 45
  Block scan transactions: 28

Solana:
  Wallet transactions: 32
  Block scan transactions: 19

Cross-Chain:
  Address correlations: 3
  Bridge movements: 2
  High-confidence events: 1

Database Statistics:
  ETH whale wallets: 52
  SOL whale wallets: 38
  ETH transactions (24h): 73
  SOL transactions (24h): 51
  Cross-chain events: 5
  Whale alerts: 8
```

## Support

For issues or questions, check the individual script docstrings or database schema.
