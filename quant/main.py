#!/usr/bin/env python3
"""
Smart Money Confidence Score - Main Entry Point

This script provides a command-line interface for managing Smart Money Confidence Scores.

Usage:
    python quant/signals/main.py init                # Initialize database
    python quant/signals/main.py init-sample         # Initialize with sample data
    python quant/signals/main.py calculate <wallet>   # Calculate confidence for wallet
    python quant/signals/main.py calculate-all       # Calculate for all wallets
    python quant/signals/main.py report              # Generate daily report
    python quant/signals/main.py serve               # Start API server
    python quant/signals/main.py elite               # Show elite wallets
    python quant/signals/main.py alerts              # Show confidence alerts
"""

import sys
import os
import argparse
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from signals.smart_money_confidence import (
    SmartMoneyConfidenceCalculator,
    recalculate_wallet_confidence,
    get_all_wallet_confidences,
    ScoreCategory
)
from reports.smart_money_confidence_report import generate_daily_report


# Configuration
DB_PATH = os.environ.get('TRADING_DB_PATH', 'quant/data/trading.db')
DEFAULT_DAYS = 30


def init_database(sample_data: bool = False) -> bool:
    """Initialize database with required tables."""
    print("Initializing database...")

    from signals.init_db import init_database as init_db, add_sample_data

    if init_db(DB_PATH):
        print("Database initialized successfully.")

        if sample_data:
            print("\nAdding sample data...")
            if add_sample_data(DB_PATH):
                print("Sample data added successfully.")
            else:
                print("Failed to add sample data.")
                return False

        return True
    else:
        print("Failed to initialize database.")
        return False


def calculate_wallet(wallet_address: str, days: int = DEFAULT_DAYS) -> None:
    """Calculate and display confidence score for a wallet."""
    print(f"Calculating confidence for {wallet_address}...")

    calculator = SmartMoneyConfidenceCalculator(DB_PATH)
    score = calculator.calculate_confidence(wallet_address, days)

    # Display results
    print("\n" + "="*60)
    print(f"SMART MONEY CONFIDENCE SCORE")
    print("="*60)
    print(f"Wallet: {wallet_address}")
    print(f"Overall Score: {score.overall_score:.2f}/100")
    print(f"Category: {score.category.value}")
    print(f"Trend: {score.trend}")
    print(f"Calculated: {score.calculated_at.strftime('%Y-%m-%d %H:%M:%S UTC')}")
    print("\n" + "-"*60)
    print("Component Scores:")
    print(f"  Win Rate:           {score.win_rate_score:.2f}/100 (30%)")
    print(f"  Trade Count:        {score.trade_count_score:.2f}/50  (10%)")
    print(f"  Average Notional:   {score.avg_notional_score:.2f}/50  (20%)")
    print(f"  Consistency:        {score.consistency_score:.2f}/100 (25%)")
    print(f"  Market Timing:      {score.market_timing_score:.2f}/100 (15%)")
    print("="*60)

    # Save to database
    if calculator.save_confidence_score(score):
        print("\n✓ Score saved to database.")
    else:
        print("\n✗ Failed to save score to database.")


def calculate_all(days: int = DEFAULT_DAYS) -> None:
    """Calculate confidence scores for all active wallets."""
    print(f"Calculating confidence for all wallets (last {days} days)...")

    scores = get_all_wallet_confidences(db_path=DB_PATH, days=days)

    print(f"\n✓ Calculated scores for {len(scores)} wallets.")

    # Display summary
    category_counts = {}
    for score in scores:
        category = score.category.value
        category_counts[category] = category_counts.get(category, 0) + 1

    print("\nSummary:")
    for category in ['ELITE', 'STRONG', 'MODERATE', 'WEAK', 'POOR']:
        count = category_counts.get(category, 0)
        print(f"  {category}: {count}")

    # Show top 10
    print("\nTop 10 Wallets:")
    print(f"{'Rank':<6} {'Wallet':<25} {'Score':<10} {'Category':<10}")
    print("-" * 51)
    scores_sorted = sorted(scores, key=lambda x: x.overall_score, reverse=True)
    for i, score in enumerate(scores_sorted[:10], 1):
        print(f"{i:<6} {score.wallet_address[:25]:<25} {score.overall_score:<10.2f} {score.category.value:<10}")


def generate_report(output_dir: str = 'quant/reports') -> str:
    """Generate daily confidence report."""
    print("Generating confidence report...")

    report_path = generate_daily_report(output_dir=output_dir, db_path=DB_PATH)

    print(f"\n✓ Report generated: {report_path}")
    return report_path


def show_elite(threshold: float = 90.0) -> None:
    """Show elite wallets."""
    calculator = SmartMoneyConfidenceCalculator(DB_PATH)
    elite = calculator.get_elite_wallets(threshold=threshold, check_decline=True)

    print(f"\nElite Wallets (Score >= {threshold}): {len(elite)}")
    print(f"{'Rank':<6} {'Wallet':<25} {'Score':<10} {'Trend':<10}")
    print("-" * 51)
    for i, score in enumerate(elite, 1):
        trend_emoji = {'up': '↑', 'down': '↓', 'neutral': '→'}
        print(f"{i:<6} {score.wallet_address[:25]:<25} {score.overall_score:<10.2f} {trend_emoji[score.trend]:<10}")


def show_alerts(threshold: float = 90.0, drop_threshold: float = 10.0) -> None:
    """Show confidence alerts for declining elite wallets."""
    calculator = SmartMoneyConfidenceCalculator(DB_PATH)

    # Get elite wallets
    elite_wallets = calculator.get_elite_wallets(threshold=threshold, check_decline=False)

    # Get declining wallets
    declining_wallets = [
        wallet for wallet in elite_wallets
        if wallet.trend == 'down'
    ]

    alerts = []
    for wallet in declining_wallets:
        history = calculator.get_wallet_history(wallet.wallet_address, days=7)

        if len(history) >= 2:
            previous_score = history[-2].overall_score
            current_score = wallet.overall_score
            drop = previous_score - current_score

            if drop >= drop_threshold:
                alerts.append({
                    'wallet': wallet,
                    'previous': previous_score,
                    'current': current_score,
                    'drop': drop
                })

    if not alerts:
        print("\n✓ No alerts at this time. All elite wallets are stable or improving.")
    else:
        critical = [a for a in alerts if a['drop'] >= 20]
        warnings = [a for a in alerts if a['drop'] < 20]

        print(f"\n🚨 Confidence Alerts: {len(alerts)}")

        if critical:
            print(f"\nCRITICAL ({len(critical)}):")
            print(f"{'Wallet':<25} {'Previous':<10} {'Current':<10} {'Drop':<10}")
            print("-" * 55)
            for alert in critical:
                print(f"{alert['wallet'].wallet_address[:25]:<25} {alert['previous']:<10.2f} {alert['current']:<10.2f} -{alert['drop']:<9.2f}")

        if warnings:
            print(f"\nWARNING ({len(warnings)}):")
            print(f"{'Wallet':<25} {'Previous':<10} {'Current':<10} {'Drop':<10}")
            print("-" * 55)
            for alert in warnings[:5]:  # Limit warnings display
                print(f"{alert['wallet'].wallet_address[:25]:<25} {alert['previous']:<10.2f} {alert['current']:<10.2f} -{alert['drop']:<9.2f}")


def show_wallet_history(wallet_address: str, days: int = 30) -> None:
    """Show confidence score history for a wallet."""
    calculator = SmartMoneyConfidenceCalculator(DB_PATH)
    history = calculator.get_wallet_history(wallet_address, days)

    if not history:
        print(f"\nNo history found for {wallet_address} in the last {days} days.")
        return

    print(f"\nConfidence History: {wallet_address}")
    print(f"{'Date':<20} {'Score':<10} {'Category':<10} {'Trend':<10}")
    print("-" * 50)
    for score in history:
        trend_emoji = {'up': '↑', 'down': '↓', 'neutral': '→'}
        print(f"{score.calculated_at.strftime('%Y-%m-%d'):<20} {score.overall_score:<10.2f} {score.category.value:<10} {trend_emoji[score.trend]:<10}")


def show_summary(days: int = DEFAULT_DAYS) -> None:
    """Show summary statistics."""
    calculator = SmartMoneyConfidenceCalculator(DB_PATH)
    scores = calculator.get_latest_confidence_scores(limit=1000)

    if not scores:
        print("\nNo confidence scores found. Calculate scores first.")
        return

    print("\n" + "="*60)
    print("SMART MONEY CONFIDENCE SUMMARY")
    print("="*60)

    # Overall stats
    total_wallets = len(scores)
    avg_score = sum(s.overall_score for s in scores) / total_wallets

    print(f"\nTotal Wallets: {total_wallets}")
    print(f"Average Score: {avg_score:.2f}")

    # Category breakdown
    category_counts = {}
    for score in scores:
        category = score.category.value
        category_counts[category] = category_counts.get(category, 0) + 1

    print("\nCategory Distribution:")
    for category in ['ELITE', 'STRONG', 'MODERATE', 'WEAK', 'POOR']:
        count = category_counts.get(category, 0)
        percentage = (count / total_wallets) * 100
        print(f"  {category}: {count} ({percentage:.1f}%)")

    # Trend breakdown
    trend_counts = {'up': 0, 'down': 0, 'neutral': 0}
    for score in scores:
        trend_counts[score.trend] += 1

    print("\nTrend Distribution:")
    print(f"  Improving (↑): {trend_counts['up']} ({trend_counts['up']/total_wallets*100:.1f}%)")
    print(f"  Declining (↓): {trend_counts['down']} ({trend_counts['down']/total_wallets*100:.1f}%)")
    print(f"  Stable (→): {trend_counts['neutral']} ({trend_counts['neutral']/total_wallets*100:.1f}%)")

    print("="*60)


def start_api_server(port: int = 5001) -> None:
    """Start the API server."""
    print(f"Starting Smart Money Confidence API server on port {port}...")
    print(f"Database: {DB_PATH}")
    print(f"API Base URL: http://localhost:{port}/api/v1/smart-money-confidence")
    print("\nPress Ctrl+C to stop the server.")

    # Import and run the API
    from api.smart_money_confidence_api import app

    app.run(host='0.0.0.0', port=port, debug=False)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Smart Money Confidence Score Management',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s init                          # Initialize database
  %(prog)s init-sample                   # Initialize with sample data
  %(prog)s calculate 0x123...           # Calculate confidence for wallet
  %(prog)s calculate-all                # Calculate for all wallets
  %(prog)s calculate-all --days 60      # Calculate with 60-day window
  %(prog)s report                        # Generate daily report
  %(prog)s elite                        # Show elite wallets
  %(prog)s elite --threshold 95         # Show elite wallets with 95+ score
  %(prog)s alerts                       # Show confidence alerts
  %(prog)s history 0x123...             # Show wallet history
  %(prog)s summary                      # Show summary statistics
  %(prog)s serve                        # Start API server
        """
    )

    parser.add_argument('command', choices=[
        'init', 'init-sample',
        'calculate', 'calculate-all',
        'report',
        'elite', 'alerts',
        'history', 'summary',
        'serve'
    ], help='Command to execute')

    parser.add_argument('wallet', nargs='?', help='Wallet address (for calculate/history commands)')
    parser.add_argument('--days', type=int, default=DEFAULT_DAYS, help='Analysis period in days')
    parser.add_argument('--threshold', type=float, default=90.0, help='Score threshold for elite/alerts')
    parser.add_argument('--drop-threshold', type=float, default=10.0, help='Drop threshold for alerts')
    parser.add_argument('--port', type=int, default=5001, help='API server port')
    parser.add_argument('--output-dir', default='quant/reports', help='Report output directory')

    args = parser.parse_args()

    # Execute command
    if args.command == 'init':
        init_database(sample_data=False)

    elif args.command == 'init-sample':
        init_database(sample_data=True)

    elif args.command == 'calculate':
        if not args.wallet:
            print("Error: wallet address required for calculate command")
            sys.exit(1)
        calculate_wallet(args.wallet, args.days)

    elif args.command == 'calculate-all':
        calculate_all(args.days)

    elif args.command == 'report':
        generate_report(args.output_dir)

    elif args.command == 'elite':
        show_elite(args.threshold)

    elif args.command == 'alerts':
        show_alerts(args.threshold, args.drop_threshold)

    elif args.command == 'history':
        if not args.wallet:
            print("Error: wallet address required for history command")
            sys.exit(1)
        show_wallet_history(args.wallet, args.days)

    elif args.command == 'summary':
        show_summary(args.days)

    elif args.command == 'serve':
        start_api_server(args.port)


if __name__ == '__main__':
    main()
