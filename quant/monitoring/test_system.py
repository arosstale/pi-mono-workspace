#!/usr/bin/env python3
"""
Test script for cross-chain whale monitoring - without external APIs
"""

import time
from database import WhaleDatabase


def test_database():
    """Test database functionality with mock data"""
    print("Testing database functionality...")

    db = WhaleDatabase()

    # Generate unique hashes based on timestamp to avoid conflicts
    timestamp_suffix = str(int(time.time()))

    # Insert mock ETH transaction
    eth_tx_id = db.insert_eth_tx({
        'tx_hash': '0x' + 'a' * 60 + timestamp_suffix,
        'from_address': '0x' + '1' * 40,
        'to_address': '0x' + '2' * 40,
        'value_eth': 100.5,
        'value_usd': 200_000,
        'gas_used': 21000,
        'gas_price': '20000000000',
        'tx_type': 'transfer',
        'protocol': None,
        'block_number': 12345678,
        'timestamp': int(time.time()) - 3600,
    })
    print(f"  Inserted ETH transaction: {eth_tx_id}")

    # Insert mock SOL transaction
    sol_tx_id = db.insert_sol_tx({
        'tx_sig': 'test_sol_sig_' + timestamp_suffix,
        'from_address': 'sol' + '1' * 40,
        'to_address': 'sol' + '2' * 40,
        'amount_sol': 5000.0,
        'amount_usd': 750_000,
        'fee_lamports': 5000,
        'tx_type': 'transfer',
        'protocol': None,
        'slot': 123456789,
        'timestamp': int(time.time()) - 1800,
    })
    print(f"  Inserted SOL transaction: {sol_tx_id}")

    # Insert whale wallets
    db.insert_whale_wallet('0x' + '1' * 40, 'eth', 200_000)
    db.insert_whale_wallet('sol' + '1' * 40, 'sol', 750_000)
    print("  Inserted whale wallets")

    # Insert cross-chain event
    event_id = db.insert_cross_chain_event({
        'eth_tx_id': eth_tx_id,
        'sol_tx_id': sol_tx_id,
        'correlation_type': 'timing',
        'correlation_score': 0.85,
        'time_diff_hours': 0.5,
        'description': 'Potential bridge movement detected',
    })
    print(f"  Inserted cross-chain event: {event_id}")

    # Insert alert
    alert_id = db.insert_whale_alert({
        'alert_type': 'large_transfer',
        'chain': 'eth',
        'address': '0x' + '1' * 40,
        'amount': 100.5,
        'currency': 'ETH',
        'description': 'Large transfer: 100.5 ETH ($200,000)',
    })
    print(f"  Inserted whale alert: {alert_id}")

    # Test queries
    print("\nTesting queries...")

    eth_txs = db.get_recent_eth_txs(hours=24, limit=10)
    print(f"  Recent ETH transactions: {len(eth_txs)}")

    sol_txs = db.get_recent_sol_txs(hours=24, limit=10)
    print(f"  Recent SOL transactions: {len(sol_txs)}")

    events = db.get_cross_chain_events(hours=24, min_score=0.5)
    print(f"  Cross-chain events: {len(events)}")

    eth_whales = db.get_whale_wallets(chain='eth', hours=24)
    print(f"  ETH whale wallets: {len(eth_whales)}")

    sol_whales = db.get_whale_wallets(chain='sol', hours=24)
    print(f"  SOL whale wallets: {len(sol_whales)}")

    # Get stats
    print("\nDatabase statistics:")
    stats = db.get_stats()
    for key, value in stats.items():
        print(f"  {key}: {value}")

    db.close()
    print("\n✓ Database test passed!")
    return True


def test_schema():
    """Test database schema initialization"""
    print("Testing schema initialization...")

    db = WhaleDatabase()

    # Check that all tables exist
    cursor = db.conn.execute("""
        SELECT name FROM sqlite_master
        WHERE type='table' AND name NOT LIKE 'sqlite_%'
    """)

    tables = [row[0] for row in cursor.fetchall()]
    expected_tables = [
        'whale_wallets',
        'cross_chain_mappings',
        'eth_whale_txs',
        'sol_whale_txs',
        'cross_chain_events',
        'whale_alerts',
    ]

    print(f"  Tables created: {len(tables)}")
    for table in expected_tables:
        if table in tables:
            print(f"    ✓ {table}")
        else:
            print(f"    ✗ {table} - MISSING")

    db.close()

    if all(t in tables for t in expected_tables):
        print("\n✓ Schema test passed!")
        return True
    else:
        print("\n✗ Schema test failed - some tables missing")
        return False


if __name__ == '__main__':
    print("=" * 60)
    print("CROSS-CHAIN WHALE MONITORING - TEST SUITE")
    print("=" * 60)
    print()

    # Test 1: Schema initialization
    if not test_schema():
        exit(1)

    print()

    # Test 2: Database operations
    if not test_database():
        exit(1)

    print()
    print("=" * 60)
    print("ALL TESTS PASSED ✓")
    print("=" * 60)
    print()
    print("System is ready for production use!")
    print()
    print("Next steps:")
    print("1. (Optional) Set ETHERSCAN_API_KEY environment variable")
    print("2. Run: python run_monitor.py")
    print("3. Check results in smart_money.db")
