#!/usr/bin/env python3
"""
Main runner for cross-chain whale monitoring
"""

import argparse
import sys
from datetime import datetime
from eth_monitor import EthereumWhaleMonitor
from sol_monitor import SolanaWhaleMonitor
from cross_chain_correlation import CrossChainCorrelation


def run_eth_monitoring(hours: int = 24):
    """Run Ethereum whale monitoring"""
    print("\n" + "=" * 60)
    print("ETHEREUM WHALE MONITORING")
    print("=" * 60)

    monitor = EthereumWhaleMonitor()
    results = monitor.monitor_whales(lookback_hours=hours)

    # Also scan recent blocks
    print("\nScanning recent blocks...")
    block_txs = monitor.scan_large_blocks(num_blocks=100)

    monitor.db.close()

    return {
        'wallet_transactions': len(results.get('transactions', [])),
        'block_transactions': len(block_txs),
    }


def run_sol_monitoring(limit: int = 500):
    """Run Solana whale monitoring"""
    print("\n" + "=" * 60)
    print("SOLANA WHALE MONITORING")
    print("=" * 60)

    monitor = SolanaWhaleMonitor()
    results = monitor.monitor_whales(limit=limit)

    # Also scan recent blocks
    print("\nScanning recent slots...")
    block_txs = monitor.scan_recent_blocks(num_blocks=100)

    monitor.db.close()

    return {
        'wallet_transactions': len(results.get('transactions', [])),
        'block_transactions': len(block_txs),
    }


def run_cross_chain_analysis(hours: int = 24):
    """Run cross-chain correlation analysis"""
    print("\n" + "=" * 60)
    print("CROSS-CHAIN CORRELATION ANALYSIS")
    print("=" * 60)

    analyzer = CrossChainCorrelation()
    results = analyzer.analyze_patterns(hours=hours)

    analyzer.db.close()

    return results


def run_full_pipeline(hours: int = 24, sol_limit: int = 500):
    """Run complete monitoring pipeline"""
    print("\n" + "=" * 60)
    print("CROSS-CHAIN WHALE MONITORING PIPELINE")
    print(f"Time window: Last {hours} hours")
    print(f"Started: {datetime.now().isoformat()}")
    print("=" * 60)

    # Phase 1: Collect ETH data
    eth_results = run_eth_monitoring(hours=hours)

    # Phase 2: Collect SOL data
    sol_results = run_sol_monitoring(limit=sol_limit)

    # Phase 3: Cross-chain correlation
    cross_results = run_cross_chain_analysis(hours=hours)

    # Summary
    print("\n" + "=" * 60)
    print("PIPELINE SUMMARY")
    print("=" * 60)
    print(f"Ethereum:")
    print(f"  Wallet transactions: {eth_results['wallet_transactions']}")
    print(f"  Block scan transactions: {eth_results['block_transactions']}")
    print(f"\nSolana:")
    print(f"  Wallet transactions: {sol_results['wallet_transactions']}")
    print(f"  Block scan transactions: {sol_results['block_transactions']}")
    print(f"\nCross-Chain:")
    print(f"  Address correlations: {cross_results['address_correlations']}")
    print(f"  Bridge movements: {cross_results['bridge_correlations']}")
    print(f"  High-confidence events: {cross_results['high_confidence_events']}")

    # Database stats
    print(f"\nDatabase Statistics:")
    stats = cross_results['stats']
    print(f"  ETH whale wallets: {stats.get('whale_wallets', {}).get('eth', 0)}")
    print(f"  SOL whale wallets: {stats.get('whale_wallets', {}).get('sol', 0)}")
    print(f"  ETH transactions (24h): {stats.get('eth_whale_txs_24h', 0)}")
    print(f"  SOL transactions (24h): {stats.get('sol_whale_txs_24h', 0)}")
    print(f"  Cross-chain events: {stats.get('cross_chain_events', 0)}")
    print(f"  Whale alerts: {stats.get('whale_alerts', 0)}")

    print(f"\nCompleted: {datetime.now().isoformat()}")
    print("=" * 60)

    return {
        'eth': eth_results,
        'sol': sol_results,
        'cross_chain': cross_results,
    }


def main():
    parser = argparse.ArgumentParser(description='Cross-chain whale monitoring system')
    parser.add_argument('--mode', choices=['eth', 'sol', 'cross', 'full'], default='full',
                       help='Monitoring mode to run')
    parser.add_argument('--hours', type=int, default=24,
                       help='Hours of data to collect (default: 24)')
    parser.add_argument('--sol-limit', type=int, default=500,
                       help='Transaction limit for Solana (default: 500)')

    args = parser.parse_args()

    try:
        if args.mode == 'eth':
            run_eth_monitoring(hours=args.hours)
        elif args.mode == 'sol':
            run_sol_monitoring(limit=args.sol_limit)
        elif args.mode == 'cross':
            run_cross_chain_analysis(hours=args.hours)
        else:
            run_full_pipeline(hours=args.hours, sol_limit=args.sol_limit)

        return 0
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
        return 130
    except Exception as e:
        print(f"\n\nError: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
