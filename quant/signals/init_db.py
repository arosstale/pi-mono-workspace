"""
Smart Money Confidence Database Initialization

Creates and initializes the smart_money_confidence table and related structures.
"""

import sqlite3
import os
from datetime import datetime


def init_database(db_path: str = 'quant/data/trading.db') -> bool:
    """
    Initialize database with required tables for Smart Money Confidence.

    Args:
        db_path: Path to SQLite database

    Returns:
        True if successful, False otherwise
    """
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        # Create agent_trades table (if not exists)
        # This table stores trade data used for confidence calculations
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
                is_paper_trade INTEGER DEFAULT 1,
                created_at INTEGER DEFAULT (strftime('%s', 'now'))
            )
        ''')

        # Create smart_money_confidence table
        # This table stores confidence score history
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS smart_money_confidence (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                wallet_address TEXT NOT NULL,
                overall_score REAL NOT NULL,
                win_rate_score REAL NOT NULL,
                trade_count_score REAL NOT NULL,
                avg_notional_score REAL NOT NULL,
                consistency_score REAL NOT NULL,
                market_timing_score REAL NOT NULL,
                category TEXT NOT NULL,
                trend TEXT DEFAULT 'neutral',
                calculated_at INTEGER NOT NULL,
                created_at INTEGER DEFAULT (strftime('%s', 'now'))
            )
        ''')

        # Create indexes for performance
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_agent_trades_agent
            ON agent_trades(agent_id)
        ''')

        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_agent_trades_symbol
            ON agent_trades(symbol)
        ''')

        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_agent_trades_status
            ON agent_trades(status)
        ''')

        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_agent_trades_timestamp
            ON agent_trades(entry_timestamp DESC)
        ''')

        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_smart_money_confidence_wallet
            ON smart_money_confidence(wallet_address)
        ''')

        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_smart_money_confidence_timestamp
            ON smart_money_confidence(calculated_at DESC)
        ''')

        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_smart_money_confidence_score
            ON smart_money_confidence(overall_score DESC)
        ''')

        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_smart_money_confidence_category
            ON smart_money_confidence(category)
        ''')

        conn.commit()

        print("Database initialized successfully.")
        print(f"Database path: {db_path}")
        print("\nTables created:")
        print("  - agent_trades")
        print("  - smart_money_confidence")
        print("\nIndexes created for performance optimization.")

        return True

    except Exception as e:
        print(f"Error initializing database: {e}")
        conn.rollback()
        return False

    finally:
        conn.close()


def add_sample_data(db_path: str = 'quant/data/trading.db') -> bool:
    """
    Add sample trade data for testing purposes.

    Args:
        db_path: Path to SQLite database

    Returns:
        True if successful, False otherwise
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        # Sample wallet addresses
        wallets = [
            '0xelite_trader_001',  # Elite performer
            '0xstrong_trader_002',  # Strong performer
            '0xmoderate_trader_003',  # Moderate performer
            '0xweak_trader_004',  # Weak performer
            '0xpoor_trader_005',  # Poor performer
        ]

        # Generate sample trades for each wallet
        import random
        from datetime import datetime, timedelta

        base_time = int((datetime.now() - timedelta(days=30)).timestamp())

        for wallet in wallets:
            # Determine performance characteristics
            if 'elite' in wallet:
                win_rate = 0.75
                avg_trades = 50
                avg_notional = 100000
            elif 'strong' in wallet:
                win_rate = 0.65
                avg_trades = 30
                avg_notional = 50000
            elif 'moderate' in wallet:
                win_rate = 0.55
                avg_trades = 20
                avg_notional = 20000
            elif 'weak' in wallet:
                win_rate = 0.45
                avg_trades = 10
                avg_notional = 5000
            else:  # poor
                win_rate = 0.35
                avg_trades = 5
                avg_notional = 1000

            # Generate trades
            num_trades = random.randint(int(avg_trades * 0.8), int(avg_trades * 1.2))

            for i in range(num_trades):
                # Determine if trade is a win
                is_win = random.random() < win_rate

                # Trade parameters
                entry_price = random.uniform(100, 200)
                quantity = random.uniform(0.5, 2.0)
                entry_timestamp = base_time + random.randint(0, 30 * 24 * 3600)

                # Calculate exit price and PnL
                if is_win:
                    exit_price = entry_price * random.uniform(1.02, 1.15)
                    pnl = (exit_price - entry_price) * quantity
                else:
                    exit_price = entry_price * random.uniform(0.85, 0.98)
                    pnl = (exit_price - entry_price) * quantity

                pnl_percent = ((exit_price - entry_price) / entry_price) * 100

                # Insert trade
                cursor.execute('''
                    INSERT INTO agent_trades (
                        agent_id, model, symbol, side, order_type,
                        quantity, entry_price, exit_price, pnl, pnl_percent,
                        status, entry_timestamp, exit_timestamp, is_paper_trade
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    wallet,
                    'gpt-4',
                    'BTC/USDT' if random.random() > 0.5 else 'ETH/USDT',
                    'buy',
                    'market',
                    quantity,
                    entry_price,
                    exit_price,
                    pnl,
                    pnl_percent,
                    'closed',
                    entry_timestamp,
                    entry_timestamp + random.randint(3600, 24 * 3600),
                    1
                ))

        conn.commit()

        print("\nSample data added successfully.")
        print(f"Sample wallets created: {len(wallets)}")

        # Count trades
        cursor.execute('SELECT COUNT(*) FROM agent_trades')
        trade_count = cursor.fetchone()[0]
        print(f"Total sample trades: {trade_count}")

        return True

    except Exception as e:
        print(f"Error adding sample data: {e}")
        conn.rollback()
        return False

    finally:
        conn.close()


def verify_database(db_path: str = 'quant/data/trading.db') -> bool:
    """
    Verify database structure and content.

    Args:
        db_path: Path to SQLite database

    Returns:
        True if verification successful, False otherwise
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        print("\n" + "="*60)
        print("DATABASE VERIFICATION")
        print("="*60)

        # Check tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]

        print(f"\nTables found: {len(tables)}")
        for table in tables:
            print(f"  - {table}")

        # Check agent_trades table
        cursor.execute("SELECT COUNT(*) FROM agent_trades")
        trade_count = cursor.fetchone()[0]
        print(f"\nagent_trades: {trade_count} records")

        if trade_count > 0:
            cursor.execute('''
                SELECT
                    agent_id,
                    COUNT(*) as trade_count,
                    SUM(CASE WHEN pnl > 0 THEN 1 ELSE 0 END) as wins,
                    AVG(pnl) as avg_pnl
                FROM agent_trades
                GROUP BY agent_id
            ''')

            print("\nTrade summary by wallet:")
            print(f"{'Wallet':<25} {'Trades':<10} {'Wins':<10} {'Avg PnL':<15}")
            print("-" * 60)
            for row in cursor.fetchall():
                print(f"{row[0]:<25} {row[1]:<10} {row[2]:<10} ${row[3]:<14.2f}")

        # Check smart_money_confidence table
        cursor.execute("SELECT COUNT(*) FROM smart_money_confidence")
        confidence_count = cursor.fetchone()[0]
        print(f"\nsmart_money_confidence: {confidence_count} records")

        if confidence_count > 0:
            cursor.execute('''
                SELECT
                    wallet_address,
                    overall_score,
                    category,
                    trend
                FROM smart_money_confidence
                ORDER BY overall_score DESC
                LIMIT 10
            ''')

            print("\nTop 10 confidence scores:")
            print(f"{'Wallet':<25} {'Score':<10} {'Category':<10} {'Trend':<10}")
            print("-" * 55)
            for row in cursor.fetchall():
                trend_emoji = {'up': '↑', 'down': '↓', 'neutral': '→'}
                print(f"{row[0]:<25} {row[1]:<10.2f} {row[2]:<10} {trend_emoji[row[3]]:<10}")

        print("\n" + "="*60)
        print("Verification complete.")
        print("="*60)

        return True

    except Exception as e:
        print(f"Error verifying database: {e}")
        return False

    finally:
        conn.close()


def reset_database(db_path: str = 'quant/data/trading.db') -> bool:
    """
    Reset database by dropping and recreating tables.

    Args:
        db_path: Path to SQLite database

    Returns:
        True if successful, False otherwise
    """
    response = input(f"Are you sure you want to reset the database at {db_path}? (yes/no): ")

    if response.lower() != 'yes':
        print("Database reset cancelled.")
        return False

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        # Drop tables
        cursor.execute('DROP TABLE IF EXISTS smart_money_confidence')
        cursor.execute('DROP TABLE IF EXISTS agent_trades')

        conn.commit()
        print("Database tables dropped successfully.")

        # Reinitialize
        conn.close()
        return init_database(db_path)

    except Exception as e:
        print(f"Error resetting database: {e}")
        conn.rollback()
        return False

    finally:
        conn.close()


if __name__ == '__main__':
    import sys

    db_path = 'quant/data/trading.db'

    if len(sys.argv) > 1:
        db_path = sys.argv[1]

    print("Smart Money Confidence Database Initialization")
    print(f"Database path: {db_path}\n")

    # Initialize database
    if init_database(db_path):
        print("\n" + "="*60)

        # Ask if sample data should be added
        response = input("\nAdd sample data for testing? (yes/no): ")

        if response.lower() == 'yes':
            add_sample_data(db_path)

        # Verify database
        verify_database(db_path)

        print("\nDatabase is ready to use!")
