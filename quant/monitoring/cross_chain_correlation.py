"""
Cross-chain whale correlation analyzer
"""

import time
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from database import WhaleDatabase
from eth_monitor import EthereumWhaleMonitor
from sol_monitor import SolanaWhaleMonitor


class CrossChainCorrelation:
    """Analyze whale movements across Ethereum and Solana"""

    def __init__(self):
        self.db = WhaleDatabase()
        self.eth_monitor = EthereumWhaleMonitor()
        self.sol_monitor = SolanaWhaleMonitor()

    def correlate_by_address_patterns(self, hours: int = 24) -> List[Dict[str, Any]]:
        """
        Find potential cross-chain wallet mappings using address patterns.
        This is a heuristic approach since ETH and SOL addresses are different formats.
        """
        print("Correlating addresses by patterns...")

        # Get whale wallets from both chains
        eth_wallets = self.db.get_whale_wallets(chain='eth', hours=hours)
        sol_wallets = self.db.get_whale_wallets(chain='sol', hours=hours)

        correlations = []

        # This is a simplified correlation - in reality, you'd need:
        # 1. Bridge transactions (e.g., Portal, Wormhole)
        # 2. Social media links (Twitter, etc.)
        # 3. Known mappings from on-chain analysis
        # 4. Subgraph queries

        # For now, we'll look for wallets with similar activity patterns
        # and similar transaction volumes

        eth_by_volume = sorted(eth_wallets, key=lambda x: x['total_tx_value'], reverse=True)
        sol_by_volume = sorted(sol_wallets, key=lambda x: x['total_tx_value'], reverse=True)

        # Look for wallets with similar volume ranks (heuristic)
        for i, eth_wallet in enumerate(eth_by_volume[:20]):  # Top 20
            # Find SOL wallet with similar volume
            for sol_wallet in sol_by_volume[:20]:
                volume_diff_pct = abs(
                    eth_wallet['total_tx_value'] - sol_wallet['total_tx_value']
                ) / max(eth_wallet['total_tx_value'], sol_wallet['total_tx_value'])

                # If volumes are within 20%, consider it a potential correlation
                if volume_diff_pct < 0.2:
                    correlation_score = 1.0 - volume_diff_pct

                    # Check for timing correlation
                    eth_txs = self._get_wallet_txs(eth_wallet['address'], 'eth')
                    sol_txs = self._get_wallet_txs(sol_wallet['address'], 'sol')

                    timing_score = self._calculate_timing_correlation(eth_txs, sol_txs)

                    combined_score = (correlation_score + timing_score) / 2

                    if combined_score > 0.3:  # Minimum threshold
                        correlations.append({
                            'eth_address': eth_wallet['address'],
                            'sol_address': sol_wallet['address'],
                            'correlation_score': combined_score,
                            'volume_correlation': correlation_score,
                            'timing_correlation': timing_score,
                            'evidence': f'Similar volume rank and activity timing',
                        })

        # Remove duplicates and store
        unique_correlations = self._deduplicate_correlations(correlations)

        for corr in unique_correlations:
            # Store mapping
            self._store_mapping(corr)

        print(f"  Found {len(unique_correlations)} potential correlations")
        return unique_correlations

    def correlate_by_bridge_activity(self, hours: int = 24) -> List[Dict[str, Any]]:
        """
        Find cross-chain movements through bridge analysis.
        This would require bridge-specific analysis in production.
        """
        print("Analyzing bridge activity...")

        # In a production system, you would:
        # 1. Query bridge contracts (Portal, Wormhole, Allbridge)
        # 2. Track deposit/withdrawal pairs
        # 3. Match timestamps and amounts

        # For this POC, we'll use a simplified approach:
        # Look for large transfers with similar timing across chains

        correlations = []

        # Get recent large ETH transactions
        recent_eth = self.db.get_recent_eth_txs(hours=hours, limit=100)

        # Get recent large SOL transactions
        recent_sol = self.db.get_recent_sol_txs(hours=hours, limit=100)

        # Look for potential bridges (timing + amount)
        for eth_tx in recent_eth:
            if eth_tx['value_usd'] < 50_000:  # Only large transactions
                continue

            for sol_tx in recent_sol:
                if sol_tx['amount_usd'] < 50_000:
                    continue

                # Check timing (within 30 minutes)
                time_diff = abs(eth_tx['timestamp'] - sol_tx['timestamp'])
                if time_diff > 1800:  # 30 minutes
                    continue

                # Check amount similarity (within 50%)
                amount_diff_pct = abs(eth_tx['value_usd'] - sol_tx['amount_usd']) / max(
                    eth_tx['value_usd'], sol_tx['amount_usd']
                )

                if amount_diff_pct < 0.5:
                    correlation_score = 1.0 - (amount_diff_pct / 2)

                    correlation = {
                        'eth_tx': eth_tx,
                        'sol_tx': sol_tx,
                        'correlation_score': correlation_score,
                        'time_diff_hours': time_diff / 3600,
                        'amount_diff_pct': amount_diff_pct,
                        'type': 'bridge',
                    }

                    correlations.append(correlation)

                    # Store as cross-chain event
                    self._store_cross_chain_event(correlation)

                    # Generate alert if high correlation
                    if correlation_score > 0.7:
                        self._generate_bridge_alert(correlation)

        print(f"  Found {len(correlations)} potential bridge movements")
        return correlations

    def _get_wallet_txs(self, address: str, chain: str, hours: int = 24) -> List[Dict[str, Any]]:
        """Get transactions for a wallet"""
        if chain == 'eth':
            # Get ETH transactions
            cursor = self.db.conn.execute("""
                SELECT * FROM eth_whale_txs
                WHERE from_address = ? OR to_address = ?
                ORDER BY timestamp DESC
            """, (address.lower(), address.lower()))
            return [dict(row) for row in cursor.fetchall()]
        else:
            # Get SOL transactions
            cursor = self.db.conn.execute("""
                SELECT * FROM sol_whale_txs
                WHERE from_address = ? OR to_address = ?
                ORDER BY timestamp DESC
            """, (address.lower(), address.lower()))
            return [dict(row) for row in cursor.fetchall()]

    def _calculate_timing_correlation(self, eth_txs: List[Dict], sol_txs: List[Dict]) -> float:
        """Calculate timing correlation between two sets of transactions"""
        if not eth_txs or not sol_txs:
            return 0.0

        # Get timestamps
        eth_times = [tx['timestamp'] for tx in eth_txs]
        sol_times = [tx['timestamp'] for tx in sol_txs]

        # Calculate pairwise differences
        min_diff = float('inf')

        for et in eth_times:
            for st in sol_times:
                diff = abs(et - st)
                if diff < min_diff:
                    min_diff = diff

        # Convert to hours and calculate score
        diff_hours = min_diff / 3600

        # Score decreases with time difference
        # 0-1 hours: 1.0, 1-6 hours: 0.8, 6-24 hours: 0.5, >24: 0.2
        if diff_hours < 1:
            return 1.0
        elif diff_hours < 6:
            return 0.8
        elif diff_hours < 24:
            return 0.5
        else:
            return 0.2

    def _deduplicate_correlations(self, correlations: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Remove duplicate correlations"""
        seen = set()
        unique = []

        for corr in correlations:
            key = (corr['eth_address'], corr['sol_address'])
            if key not in seen:
                seen.add(key)
                unique.append(corr)

        return unique

    def _store_mapping(self, correlation: Dict[str, Any]):
        """Store cross-chain wallet mapping"""
        try:
            self.db.conn.execute("""
                INSERT INTO cross_chain_mappings (
                    eth_address, sol_address, correlation_score,
                    confidence, evidence
                ) VALUES (?, ?, ?, ?, ?)
                ON CONFLICT(eth_address, sol_address) DO UPDATE SET
                    correlation_score = excluded.correlation_score,
                    confidence = excluded.confidence,
                    updated_at = ?
            """, (
                correlation['eth_address'].lower(),
                correlation['sol_address'].lower(),
                correlation['correlation_score'],
                correlation.get('timing_correlation', 0),
                correlation['evidence'],
                int(time.time())
            ))
            self.db.conn.commit()
        except Exception as e:
            print(f"Error storing mapping: {e}")

    def _store_cross_chain_event(self, correlation: Dict[str, Any]):
        """Store cross-chain correlation event"""
        try:
            eth_tx_id = correlation.get('eth_tx', {}).get('id')
            sol_tx_id = correlation.get('sol_tx', {}).get('id')

            self.db.insert_cross_chain_event({
                'eth_tx_id': eth_tx_id,
                'sol_tx_id': sol_tx_id,
                'correlation_type': 'timing',
                'correlation_score': correlation['correlation_score'],
                'time_diff_hours': correlation['time_diff_hours'],
                'description': f'Potential bridge movement: ${correlation["eth_tx"]["value_usd"]:,.0f} vs ${correlation["sol_tx"]["amount_usd"]:,.0f}',
            })
        except Exception as e:
            print(f"Error storing cross-chain event: {e}")

    def _generate_bridge_alert(self, correlation: Dict[str, Any]):
        """Generate alert for high-confidence bridge movement"""
        try:
            eth_tx = correlation['eth_tx']
            sol_tx = correlation['sol_tx']

            self.db.insert_whale_alert({
                'alert_type': 'cross_chain_move',
                'chain': 'cross',
                'address': f"{eth_tx['from_address']} -> {sol_tx['from_address']}",
                'amount': (eth_tx['value_usd'] + sol_tx['amount_usd']) / 2,
                'currency': 'USD',
                'description': (
                    f"HIGH CONFIDENCE: Potential cross-chain whale movement\n"
                    f"ETH: {eth_tx['value_eth']:.2f} ETH (${eth_tx['value_usd']:,.0f})\n"
                    f"SOL: {sol_tx['amount_sol']:.2f} SOL (${sol_tx['amount_usd']:,.0f})\n"
                    f"Time diff: {correlation['time_diff_hours']:.2f} hours\n"
                    f"Confidence: {correlation['correlation_score']:.2f}"
                ),
            })
        except Exception as e:
            print(f"Error generating bridge alert: {e}")

    def analyze_patterns(self, hours: int = 24) -> Dict[str, Any]:
        """Run full cross-chain analysis"""
        print(f"\n=== Cross-Chain Analysis ({hours} hours) ===\n")

        # Collect fresh data
        print("Collecting fresh ETH data...")
        eth_monitor = EthereumWhaleMonitor()
        eth_monitor.monitor_whales(lookback_hours=hours)

        print("\nCollecting fresh SOL data...")
        sol_monitor = SolanaWhaleMonitor()
        sol_monitor.monitor_whales(limit=300)

        # Analyze correlations
        print("\nRunning correlation analysis...")

        address_correlations = self.correlate_by_address_patterns(hours=hours)
        bridge_correlations = self.correlate_by_bridge_activity(hours=hours)

        # Get stats
        stats = self.db.get_stats()

        # Get high-confidence events
        high_confidence_events = self.db.get_cross_chain_events(hours=hours, min_score=0.7)

        result = {
            'address_correlations': len(address_correlations),
            'bridge_correlations': len(bridge_correlations),
            'high_confidence_events': len(high_confidence_events),
            'stats': stats,
            'events': high_confidence_events,
            'bridge_movements': bridge_correlations,
        }

        # Print summary
        print(f"\n=== Analysis Results ===")
        print(f"Address pattern correlations: {len(address_correlations)}")
        print(f"Potential bridge movements: {len(bridge_correlations)}")
        print(f"High-confidence events: {len(high_confidence_events)}")

        print(f"\n=== Database Stats ===")
        print(f"ETH whale wallets: {stats.get('whale_wallets', {}).get('eth', 0)}")
        print(f"SOL whale wallets: {stats.get('whale_wallets', {}).get('sol', 0)}")
        print(f"ETH transactions (24h): {stats.get('eth_whale_txs_24h', 0)}")
        print(f"SOL transactions (24h): {stats.get('sol_whale_txs_24h', 0)}")
        print(f"Cross-chain events: {stats.get('cross_chain_events', 0)}")

        return result

    def get_top_whales(self, chain: str = None, limit: int = 10) -> List[Dict[str, Any]]:
        """Get top whale wallets by transaction volume"""
        query = """
            SELECT * FROM whale_wallets
            WHERE is_active = 1
        """
        params = []

        if chain:
            query += " AND chain = ?"
            params.append(chain)

        query += " ORDER BY total_tx_value DESC LIMIT ?"
        params.append(limit)

        cursor = self.db.conn.execute(query, params)
        return [dict(row) for row in cursor.fetchall()]

    def get_cross_chain_alerts(self, hours: int = 24, unresolved: bool = True) -> List[Dict[str, Any]]:
        """Get cross-chain alerts"""
        since = int((datetime.now() - timedelta(hours=hours)).timestamp())
        query = """
            SELECT * FROM whale_alerts
            WHERE alert_type = 'cross_chain_move'
            AND created_at > ?
        """
        params = [since]

        if unresolved:
            query += " AND is_resolved = 0"

        query += " ORDER BY created_at DESC"

        cursor = self.db.conn.execute(query, params)
        return [dict(row) for row in cursor.fetchall()]


if __name__ == '__main__':
    # Run cross-chain analysis
    analyzer = CrossChainCorrelation()

    print("=" * 60)
    print("CROSS-CHAIN WHALE CORRELATION ANALYZER")
    print("=" * 60)

    # Analyze last 24 hours
    results = analyzer.analyze_patterns(hours=24)

    # Print top whales
    print(f"\n=== Top ETH Whales ===")
    for whale in analyzer.get_top_whales(chain='eth', limit=5):
        print(f"  {whale['address']}: ${whale['total_tx_value']:,.0f} ({whale['tx_count']} txs)")

    print(f"\n=== Top SOL Whales ===")
    for whale in analyzer.get_top_whales(chain='sol', limit=5):
        print(f"  {whale['address']}: ${whale['total_tx_value']:,.0f} ({whale['tx_count']} txs)")

    # Print cross-chain alerts
    print(f"\n=== Cross-Chain Alerts ===")
    alerts = analyzer.get_cross_chain_alerts(hours=24)
    if alerts:
        for alert in alerts[:3]:
            print(f"  [{alert['created_at']}] {alert['description'][:100]}...")
    else:
        print("  No cross-chain alerts in last 24 hours")

    print(f"\n=== High-Confidence Events ===")
    for event in results['events'][:5]:
        print(f"  Score: {event['correlation_score']:.2f} | {event['description'][:80]}...")

    analyzer.db.close()
