"""
Database utilities for cross-chain whale monitoring
"""

import sqlite3
import os
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import json

# Database path
DB_PATH = Path(__file__).parent.parent.parent / "smart_money.db"

class WhaleDatabase:
    """Database manager for whale monitoring system"""

    def __init__(self, db_path: str = str(DB_PATH)):
        self.db_path = db_path
        self.conn = None
        self.connect()
        self._ensure_schema()

    def connect(self):
        """Create database connection"""
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row  # Enable dict-like access
        self.conn.execute("PRAGMA journal_mode=WAL")  # Better concurrency
        self.conn.execute("PRAGMA foreign_keys=ON")

    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()

    def _ensure_schema(self):
        """Ensure schema is loaded"""
        schema_path = Path(__file__).parent / "schema.sql"
        if schema_path.exists():
            with open(schema_path, 'r') as f:
                schema = f.read()
            self.conn.executescript(schema)
            self.conn.commit()

    def insert_whale_wallet(self, address: str, chain: str, tx_value: float = 0):
        """Insert or update whale wallet"""
        now = int(datetime.now().timestamp())
        self.conn.execute("""
            INSERT INTO whale_wallets (address, chain, first_seen, last_seen, total_tx_value, tx_count)
            VALUES (?, ?, ?, ?, ?, 1)
            ON CONFLICT(address, chain) DO UPDATE SET
                last_seen = excluded.last_seen,
                total_tx_value = total_tx_value + excluded.total_tx_value,
                tx_count = tx_count + 1,
                updated_at = excluded.updated_at
        """, (address.lower(), chain, now, now, tx_value))
        self.conn.commit()

    def insert_eth_tx(self, tx_data: Dict[str, Any]) -> int:
        """Insert Ethereum transaction"""
        cursor = self.conn.execute("""
            INSERT INTO eth_whale_txs (
                tx_hash, from_address, to_address, value_eth, value_usd,
                gas_used, gas_price, tx_type, protocol, block_number, timestamp
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            tx_data.get('tx_hash'),
            tx_data.get('from_address', '').lower(),
            tx_data.get('to_address', '').lower(),
            tx_data.get('value_eth', 0),
            tx_data.get('value_usd', 0),
            tx_data.get('gas_used'),
            tx_data.get('gas_price'),
            tx_data.get('tx_type', 'transfer'),
            tx_data.get('protocol'),
            tx_data.get('block_number'),
            tx_data.get('timestamp', int(datetime.now().timestamp()))
        ))
        self.conn.commit()
        return cursor.lastrowid

    def insert_sol_tx(self, tx_data: Dict[str, Any]) -> int:
        """Insert Solana transaction"""
        cursor = self.conn.execute("""
            INSERT INTO sol_whale_txs (
                tx_sig, from_address, to_address, amount_sol, amount_usd,
                fee_lamports, tx_type, protocol, slot, timestamp
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            tx_data.get('tx_sig'),
            tx_data.get('from_address', '').lower(),
            tx_data.get('to_address', '').lower(),
            tx_data.get('amount_sol', 0),
            tx_data.get('amount_usd', 0),
            tx_data.get('fee_lamports'),
            tx_data.get('tx_type', 'transfer'),
            tx_data.get('protocol'),
            tx_data.get('slot'),
            tx_data.get('timestamp', int(datetime.now().timestamp()))
        ))
        self.conn.commit()
        return cursor.lastrowid

    def insert_cross_chain_event(self, event_data: Dict[str, Any]) -> int:
        """Insert cross-chain correlation event"""
        cursor = self.conn.execute("""
            INSERT INTO cross_chain_events (
                eth_tx_id, sol_tx_id, correlation_type, correlation_score,
                time_diff_hours, description
            ) VALUES (?, ?, ?, ?, ?, ?)
        """, (
            event_data.get('eth_tx_id'),
            event_data.get('sol_tx_id'),
            event_data.get('correlation_type'),
            event_data.get('correlation_score', 0),
            event_data.get('time_diff_hours'),
            event_data.get('description')
        ))
        self.conn.commit()
        return cursor.lastrowid

    def insert_whale_alert(self, alert_data: Dict[str, Any]) -> int:
        """Insert whale alert"""
        cursor = self.conn.execute("""
            INSERT INTO whale_alerts (
                alert_type, chain, address, amount, currency,
                description, correlation_id
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            alert_data.get('alert_type'),
            alert_data.get('chain'),
            alert_data.get('address', '').lower(),
            alert_data.get('amount'),
            alert_data.get('currency'),
            alert_data.get('description'),
            alert_data.get('correlation_id')
        ))
        self.conn.commit()
        return cursor.lastrowid

    def get_whale_wallets(self, chain: str = None, hours: int = 24) -> List[Dict[str, Any]]:
        """Get whale wallets from last N hours"""
        since = int((datetime.now() - timedelta(hours=hours)).timestamp())
        query = "SELECT * FROM whale_wallets WHERE last_seen > ?"
        params = [since]
        if chain:
            query += " AND chain = ?"
            params.append(chain)
        query += " ORDER BY last_seen DESC"

        cursor = self.conn.execute(query, params)
        return [dict(row) for row in cursor.fetchall()]

    def get_recent_eth_txs(self, hours: int = 24, limit: int = 100) -> List[Dict[str, Any]]:
        """Get recent ETH transactions"""
        since = int((datetime.now() - timedelta(hours=hours)).timestamp())
        cursor = self.conn.execute("""
            SELECT * FROM eth_whale_txs
            WHERE timestamp > ?
            ORDER BY timestamp DESC
            LIMIT ?
        """, (since, limit))
        return [dict(row) for row in cursor.fetchall()]

    def get_recent_sol_txs(self, hours: int = 24, limit: int = 100) -> List[Dict[str, Any]]:
        """Get recent SOL transactions"""
        since = int((datetime.now() - timedelta(hours=hours)).timestamp())
        cursor = self.conn.execute("""
            SELECT * FROM sol_whale_txs
            WHERE timestamp > ?
            ORDER BY timestamp DESC
            LIMIT ?
        """, (since, limit))
        return [dict(row) for row in cursor.fetchall()]

    def get_cross_chain_events(self, hours: int = 24, min_score: float = 0.5) -> List[Dict[str, Any]]:
        """Get cross-chain correlation events"""
        since = int((datetime.now() - timedelta(hours=hours)).timestamp())
        cursor = self.conn.execute("""
            SELECT cce.*, e.tx_hash as eth_tx_hash, s.tx_sig as sol_tx_sig
            FROM cross_chain_events cce
            LEFT JOIN eth_whale_txs e ON cce.eth_tx_id = e.id
            LEFT JOIN sol_whale_txs s ON cce.sol_tx_id = s.id
            WHERE cce.created_at > ? AND cce.correlation_score >= ?
            ORDER BY cce.correlation_score DESC
        """, (since, min_score))
        return [dict(row) for row in cursor.fetchall()]

    def get_stats(self) -> Dict[str, Any]:
        """Get database statistics"""
        stats = {}
        for table in ['whale_wallets', 'eth_whale_txs', 'sol_whale_txs', 'cross_chain_events', 'whale_alerts']:
            cursor = self.conn.execute(f"SELECT COUNT(*) as count FROM {table}")
            stats[table] = cursor.fetchone()['count']

        # Chain breakdown
        cursor = self.conn.execute("SELECT chain, COUNT(*) as count FROM whale_wallets GROUP BY chain")
        stats['by_chain'] = {row['chain']: row['count'] for row in cursor.fetchall()}

        # Recent activity
        last_24h = int((datetime.now() - timedelta(hours=24)).timestamp())
        for table in ['eth_whale_txs', 'sol_whale_txs']:
            cursor = self.conn.execute(f"SELECT COUNT(*) as count FROM {table} WHERE timestamp > ?", (last_24h,))
            stats[f'{table}_24h'] = cursor.fetchone()['count']

        return stats

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
