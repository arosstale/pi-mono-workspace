"""
Smart Money Confidence Score Module

Calculates a unified confidence score (0-100) for wallet behavior quality.
Focuses on measuring the quality of smart money, not just quantity.

Score Factors:
- Win Rate (30% weight): Higher = more reliable
- Trade Count (10% weight): More = more data
- Average Notional (20% weight): Larger = more skin in game
- Consistency (25% weight): Stable win rate over time
- Market Timing (15% weight): Do they buy low/sell high?

Score Categories:
- 90-100: ELITE (Top 1%)
- 75-89: STRONG (Top 5%)
- 60-74: MODERATE (Top 20%)
- 40-59: WEAK (Below average)
- 0-39: POOR (Unreliable)
"""

import sqlite3
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import statistics


class ScoreCategory(Enum):
    ELITE = "ELITE"      # 90-100 (Top 1%)
    STRONG = "STRONG"    # 75-89 (Top 5%)
    MODERATE = "MODERATE" # 60-74 (Top 20%)
    WEAK = "WEAK"        # 40-59 (Below average)
    POOR = "POOR"        # 0-39 (Unreliable)


@dataclass
class ConfidenceScore:
    wallet_address: str
    overall_score: float
    win_rate_score: float
    trade_count_score: float
    avg_notional_score: float
    consistency_score: float
    market_timing_score: float
    category: ScoreCategory
    calculated_at: datetime
    trend: str = "neutral"  # up, down, neutral


class SmartMoneyConfidenceCalculator:
    """
    Calculates Smart Money Confidence Scores based on multiple factors.
    """

    # Factor weights (must sum to 1.0)
    WEIGHTS = {
        'win_rate': 0.30,
        'trade_count': 0.10,
        'avg_notional': 0.20,
        'consistency': 0.25,
        'market_timing': 0.15
    }

    def __init__(self, db_path: str = 'quant/data/trading.db'):
        """
        Initialize the confidence calculator.

        Args:
            db_path: Path to SQLite database containing trade data
        """
        self.db_path = db_path

    def get_db_connection(self) -> sqlite3.Connection:
        """Get database connection."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def calculate_win_rate_score(self, win_rate: float) -> float:
        """
        Calculate win rate score (0-100 points).

        Args:
            win_rate: Win rate as percentage (0-100)

        Returns:
            Score from 0-100
        """
        # Direct mapping: win_rate percentage to score
        return min(max(win_rate, 0), 100)

    def calculate_trade_count_score(self, trade_count: int) -> float:
        """
        Calculate trade count score (0-50 points).

        More trades = more data points = higher confidence (up to 50).

        Args:
            trade_count: Number of trades

        Returns:
            Score from 0-50
        """
        # Logarithmic scale: diminishing returns after many trades
        # 0 trades = 0, 10 trades = 25, 100 trades = 50
        if trade_count == 0:
            return 0

        import math
        score = 50 * (math.log10(trade_count + 1) / math.log10(101))
        return min(score, 50)

    def calculate_avg_notional_score(self, avg_notional: float) -> float:
        """
        Calculate average notional score (0-50 points).

        Larger average notional = more skin in game = higher confidence (up to 50).

        Args:
            avg_notional: Average trade notional value

        Returns:
            Score from 0-50
        """
        # Threshold-based scoring
        # $0 = 0 points
        # $10k = 20 points
        # $100k = 35 points
        # $1M+ = 50 points

        if avg_notional <= 0:
            return 0

        import math
        score = 50 * (math.log10(avg_notional + 1) / math.log10(1000001))
        return min(score, 50)

    def calculate_consistency_score(self, wallet_address: str,
                                   days: int = 30) -> float:
        """
        Calculate consistency score (0-100 points).

        Measures stability of win rate over time. Lower variance = higher score.

        Args:
            wallet_address: Wallet address
            days: Number of days to analyze

        Returns:
            Score from 0-100
        """
        conn = self.get_db_connection()
        cursor = conn.cursor()

        try:
            # Get daily win rates over the period
            cursor.execute("""
                SELECT
                    DATE(entry_timestamp, 'unixepoch') as trade_date,
                    SUM(CASE WHEN pnl > 0 THEN 1 ELSE 0 END) * 100.0 / COUNT(*) as daily_win_rate
                FROM agent_trades
                WHERE agent_id = ?
                  AND entry_timestamp >= strftime('%s', 'now', '-{} days')
                  AND status = 'closed'
                GROUP BY trade_date
                HAVING COUNT(*) >= 3  -- Only include days with sufficient trades
            """.format(days), (wallet_address,))

            rows = cursor.fetchall()

            if len(rows) < 3:  # Need at least 3 days of data
                return 0

            daily_win_rates = [row['daily_win_rate'] for row in rows]

            # Calculate coefficient of variation (CV)
            # Lower CV = more consistent = higher score
            mean_win_rate = statistics.mean(daily_win_rate)
            if mean_win_rate == 0:
                return 0

            std_dev = statistics.stdev(daily_win_rates) if len(daily_win_rates) > 1 else 0
            cv = (std_dev / mean_win_rate) * 100  # Coefficient of variation as percentage

            # CV to score mapping
            # CV < 10 = 100 points
            # CV < 20 = 80 points
            # CV < 30 = 60 points
            # CV < 50 = 40 points
            # CV >= 50 = 20 points
            if cv < 10:
                score = 100
            elif cv < 20:
                score = 100 - (cv - 10) * 2  # 100 -> 80
            elif cv < 30:
                score = 80 - (cv - 20) * 2  # 80 -> 60
            elif cv < 50:
                score = 60 - (cv - 30) * 1  # 60 -> 40
            else:
                score = max(40 - (cv - 50) * 0.5, 20)  # 40 -> 20

            return score

        finally:
            conn.close()

    def calculate_market_timing_score(self, wallet_address: str,
                                      days: int = 30) -> float:
        """
        Calculate market timing score (0-100 points).

        Measures if wallet tends to buy low and sell high.
        Compares entry/exit prices with average price over holding period.

        Args:
            wallet_address: Wallet address
            days: Number of days to analyze

        Returns:
            Score from 0-100
        """
        conn = self.get_db_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                SELECT
                    symbol,
                    side,
                    entry_price,
                    exit_price,
                    entry_timestamp,
                    exit_timestamp
                FROM agent_trades
                WHERE agent_id = ?
                  AND entry_timestamp >= strftime('%s', 'now', '-{} days')
                  AND status = 'closed'
                  AND exit_price IS NOT NULL
                  AND exit_price > 0
            """.format(days), (wallet_address,))

            rows = cursor.fetchall()

            if len(rows) == 0:
                return 0

            timing_scores = []

            for trade in rows:
                # Calculate average price during holding period
                # This is a simplified version - in production, you'd use OHLCV data
                holding_period = trade['exit_timestamp'] - trade['entry_timestamp']

                # Normalize timing score based on PnL percentage
                if trade['side'].lower() == 'buy':
                    # Long: buy low, sell high
                    if trade['exit_price'] > trade['entry_price']:
                        # Good timing - calculate score based on how much profit
                        pct_gain = ((trade['exit_price'] - trade['entry_price']) / trade['entry_price']) * 100
                        score = min(100, 50 + pct_gain / 2)  # Base 50, bonus for gains
                    else:
                        # Bad timing
                        pct_loss = ((trade['entry_price'] - trade['exit_price']) / trade['entry_price']) * 100
                        score = max(0, 50 - pct_loss)  # Penalize losses
                else:  # sell / short
                    # Short: sell high, buy low
                    if trade['entry_price'] > trade['exit_price']:
                        # Good timing
                        pct_gain = ((trade['entry_price'] - trade['exit_price']) / trade['entry_price']) * 100
                        score = min(100, 50 + pct_gain / 2)
                    else:
                        # Bad timing
                        pct_loss = ((trade['exit_price'] - trade['entry_price']) / trade['entry_price']) * 100
                        score = max(0, 50 - pct_loss)

                timing_scores.append(score)

            # Average timing score
            return statistics.mean(timing_scores) if timing_scores else 0

        finally:
            conn.close()

    def get_wallet_statistics(self, wallet_address: str, days: int = 30) -> Dict:
        """
        Get basic statistics for a wallet.

        Args:
            wallet_address: Wallet address
            days: Number of days to analyze

        Returns:
            Dictionary with win_rate, trade_count, avg_notional
        """
        conn = self.get_db_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                SELECT
                    COUNT(*) as total_trades,
                    SUM(CASE WHEN pnl > 0 THEN 1 ELSE 0 END) as winning_trades,
                    AVG(ABS(entry_price * quantity)) as avg_notional,
                    SUM(pnl) as total_pnl,
                    AVG(pnl) as avg_pnl
                FROM agent_trades
                WHERE agent_id = ?
                  AND entry_timestamp >= strftime('%s', 'now', '-{} days')
                  AND status = 'closed'
            """.format(days), (wallet_address,))

            row = cursor.fetchone()

            if not row or row['total_trades'] == 0:
                return {
                    'win_rate': 0,
                    'trade_count': 0,
                    'avg_notional': 0,
                    'total_pnl': 0,
                    'avg_pnl': 0
                }

            win_rate = (row['winning_trades'] / row['total_trades']) * 100

            return {
                'win_rate': win_rate,
                'trade_count': row['total_trades'],
                'avg_notional': row['avg_notional'] or 0,
                'total_pnl': row['total_pnl'] or 0,
                'avg_pnl': row['avg_pnl'] or 0
            }

        finally:
            conn.close()

    def calculate_overall_score(self, win_rate_score: float,
                                trade_count_score: float,
                                avg_notional_score: float,
                                consistency_score: float,
                                market_timing_score: float) -> float:
        """
        Calculate overall confidence score using weighted average.

        Note: trade_count_score and avg_notional_score are on 0-50 scale,
        other scores are on 0-100 scale. We normalize everything to 0-100.

        Args:
            win_rate_score: Win rate score (0-100)
            trade_count_score: Trade count score (0-50)
            avg_notional_score: Average notional score (0-50)
            consistency_score: Consistency score (0-100)
            market_timing_score: Market timing score (0-100)

        Returns:
            Overall confidence score (0-100)
        """
        # Normalize trade_count and avg_notional to 0-100 scale
        trade_count_normalized = trade_count_score * 2  # 0-50 -> 0-100
        avg_notional_normalized = avg_notional_score * 2  # 0-50 -> 0-100

        # Calculate weighted average
        overall = (
            win_rate_score * self.WEIGHTS['win_rate'] +
            trade_count_normalized * self.WEIGHTS['trade_count'] +
            avg_notional_normalized * self.WEIGHTS['avg_notional'] +
            consistency_score * self.WEIGHTS['consistency'] +
            market_timing_score * self.WEIGHTS['market_timing']
        )

        return min(max(overall, 0), 100)

    def get_category(self, score: float) -> ScoreCategory:
        """
        Get score category based on confidence score.

        Args:
            score: Confidence score (0-100)

        Returns:
            ScoreCategory enum
        """
        if score >= 90:
            return ScoreCategory.ELITE
        elif score >= 75:
            return ScoreCategory.STRONG
        elif score >= 60:
            return ScoreCategory.MODERATE
        elif score >= 40:
            return ScoreCategory.WEAK
        else:
            return ScoreCategory.POOR

    def calculate_confidence(self, wallet_address: str,
                            days: int = 30) -> ConfidenceScore:
        """
        Calculate full confidence score for a wallet.

        Args:
            wallet_address: Wallet address
            days: Number of days to analyze

        Returns:
            ConfidenceScore object
        """
        # Get basic statistics
        stats = self.get_wallet_statistics(wallet_address, days)

        # Calculate individual scores
        win_rate_score = self.calculate_win_rate_score(stats['win_rate'])
        trade_count_score = self.calculate_trade_count_score(stats['trade_count'])
        avg_notional_score = self.calculate_avg_notional_score(stats['avg_notional'])
        consistency_score = self.calculate_consistency_score(wallet_address, days)
        market_timing_score = self.calculate_market_timing_score(wallet_address, days)

        # Calculate overall score
        overall_score = self.calculate_overall_score(
            win_rate_score,
            trade_count_score,
            avg_notional_score,
            consistency_score,
            market_timing_score
        )

        # Get category
        category = self.get_category(overall_score)

        # Calculate trend (compare with previous score)
        trend = self.calculate_trend(wallet_address, overall_score)

        return ConfidenceScore(
            wallet_address=wallet_address,
            overall_score=round(overall_score, 2),
            win_rate_score=round(win_rate_score, 2),
            trade_count_score=round(trade_count_score, 2),
            avg_notional_score=round(avg_notional_score, 2),
            consistency_score=round(consistency_score, 2),
            market_timing_score=round(market_timing_score, 2),
            category=category,
            calculated_at=datetime.utcnow(),
            trend=trend
        )

    def calculate_trend(self, wallet_address: str, current_score: float) -> str:
        """
        Calculate trend by comparing current score with previous score.

        Args:
            wallet_address: Wallet address
            current_score: Current confidence score

        Returns:
            Trend: 'up', 'down', or 'neutral'
        """
        conn = self.get_db_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                SELECT overall_score
                FROM smart_money_confidence
                WHERE wallet_address = ?
                ORDER BY calculated_at DESC
                LIMIT 1
            """, (wallet_address,))

            row = cursor.fetchone()

            if not row:
                return 'neutral'

            previous_score = row['overall_score']
            delta = current_score - previous_score

            if delta > 5:  # Significant improvement
                return 'up'
            elif delta < -5:  # Significant decline
                return 'down'
            else:
                return 'neutral'

        finally:
            conn.close()

    def save_confidence_score(self, score: ConfidenceScore) -> bool:
        """
        Save confidence score to database.

        Args:
            score: ConfidenceScore object

        Returns:
            True if successful, False otherwise
        """
        conn = self.get_db_connection()
        cursor = conn.cursor()

        try:
            # Create table if it doesn't exist
            cursor.execute("""
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
            """)

            # Insert score
            cursor.execute("""
                INSERT INTO smart_money_confidence (
                    wallet_address, overall_score, win_rate_score,
                    trade_count_score, avg_notional_score,
                    consistency_score, market_timing_score,
                    category, trend, calculated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                score.wallet_address,
                score.overall_score,
                score.win_rate_score,
                score.trade_count_score,
                score.avg_notional_score,
                score.consistency_score,
                score.market_timing_score,
                score.category.value,
                score.trend,
                int(score.calculated_at.timestamp())
            ))

            conn.commit()
            return True

        except Exception as e:
            print(f"Error saving confidence score: {e}")
            conn.rollback()
            return False

        finally:
            conn.close()

    def get_latest_confidence_scores(self, limit: int = 100) -> List[ConfidenceScore]:
        """
        Get latest confidence scores for all wallets.

        Args:
            limit: Maximum number of wallets to return

        Returns:
            List of ConfidenceScore objects
        """
        conn = self.get_db_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                SELECT
                    wallet_address, overall_score, win_rate_score,
                    trade_count_score, avg_notional_score,
                    consistency_score, market_timing_score,
                    category, trend, calculated_at
                FROM smart_money_confidence
                WHERE id IN (
                    SELECT MAX(id)
                    FROM smart_money_confidence
                    GROUP BY wallet_address
                )
                ORDER BY overall_score DESC
                LIMIT ?
            """, (limit,))

            rows = cursor.fetchall()

            scores = []
            for row in rows:
                scores.append(ConfidenceScore(
                    wallet_address=row['wallet_address'],
                    overall_score=row['overall_score'],
                    win_rate_score=row['win_rate_score'],
                    trade_count_score=row['trade_count_score'],
                    avg_notional_score=row['avg_notional_score'],
                    consistency_score=row['consistency_score'],
                    market_timing_score=row['market_timing_score'],
                    category=ScoreCategory(row['category']),
                    calculated_at=datetime.fromtimestamp(row['calculated_at']),
                    trend=row['trend']
                ))

            return scores

        finally:
            conn.close()

    def get_wallet_history(self, wallet_address: str,
                          days: int = 30) -> List[ConfidenceScore]:
        """
        Get confidence score history for a specific wallet.

        Args:
            wallet_address: Wallet address
            days: Number of days of history to retrieve

        Returns:
            List of ConfidenceScore objects
        """
        conn = self.get_db_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                SELECT
                    wallet_address, overall_score, win_rate_score,
                    trade_count_score, avg_notional_score,
                    consistency_score, market_timing_score,
                    category, trend, calculated_at
                FROM smart_money_confidence
                WHERE wallet_address = ?
                  AND calculated_at >= strftime('%s', 'now', '-{} days')
                ORDER BY calculated_at ASC
            """.format(days), (wallet_address,))

            rows = cursor.fetchall()

            scores = []
            for row in rows:
                scores.append(ConfidenceScore(
                    wallet_address=row['wallet_address'],
                    overall_score=row['overall_score'],
                    win_rate_score=row['win_rate_score'],
                    trade_count_score=row['trade_count_score'],
                    avg_notional_score=row['avg_notional_score'],
                    consistency_score=row['consistency_score'],
                    market_timing_score=row['market_timing_score'],
                    category=ScoreCategory(row['category']),
                    calculated_at=datetime.fromtimestamp(row['calculated_at']),
                    trend=row['trend']
                ))

            return scores

        finally:
            conn.close()

    def get_elite_wallets(self, threshold: float = 90.0,
                         check_decline: bool = True) -> List[ConfidenceScore]:
        """
        Get wallets with elite confidence scores.

        Args:
            threshold: Minimum score to be considered elite
            check_decline: If True, only include wallets not in decline

        Returns:
            List of elite ConfidenceScore objects
        """
        scores = self.get_latest_confidence_scores(limit=1000)

        elite = [
            score for score in scores
            if score.overall_score >= threshold
            and (not check_decline or score.trend != 'down')
        ]

        return elite


def recalculate_wallet_confidence(wallet_address: str,
                                   db_path: str = 'quant/data/trading.db',
                                   days: int = 30) -> Optional[ConfidenceScore]:
    """
    Recalculate confidence for a specific wallet and save to database.

    This function is intended to be called after each trade fill.

    Args:
        wallet_address: Wallet address
        db_path: Path to database
        days: Number of days to analyze

    Returns:
        ConfidenceScore if successful, None otherwise
    """
    calculator = SmartMoneyConfidenceCalculator(db_path)
    score = calculator.calculate_confidence(wallet_address, days)
    calculator.save_confidence_score(score)
    return score


def get_all_wallet_confidences(db_path: str = 'quant/data/trading.db',
                               days: int = 30) -> List[ConfidenceScore]:
    """
    Calculate and save confidence scores for all active wallets.

    Args:
        db_path: Path to database
        days: Number of days to analyze

    Returns:
        List of ConfidenceScore objects
    """
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    try:
        # Get all unique wallets with recent activity
        cursor.execute("""
            SELECT DISTINCT agent_id
            FROM agent_trades
            WHERE entry_timestamp >= strftime('%s', 'now', '-{} days')
        """.format(days))

        rows = cursor.fetchall()
        wallet_addresses = [row['agent_id'] for row in rows]

        calculator = SmartMoneyConfidenceCalculator(db_path)
        scores = []

        for wallet_address in wallet_addresses:
            score = calculator.calculate_confidence(wallet_address, days)
            calculator.save_confidence_score(score)
            scores.append(score)

        return scores

    finally:
        conn.close()


if __name__ == '__main__':
    # Example usage
    calculator = SmartMoneyConfidenceCalculator('quant/data/trading.db')

    # Calculate confidence for a specific wallet
    score = calculator.calculate_confidence('0x1234567890abcdef', days=30)
    print(f"Confidence Score: {score.overall_score}")
    print(f"Category: {score.category.value}")
    print(f"Trend: {score.trend}")

    # Save to database
    calculator.save_confidence_score(score)

    # Get latest scores for all wallets
    latest_scores = calculator.get_latest_confidence_scores(limit=10)
    for s in latest_scores:
        print(f"{s.wallet_address}: {s.overall_score} ({s.category.value})")

    # Get elite wallets
    elite_wallets = calculator.get_elite_wallets()
    print(f"\nElite Wallets: {len(elite_wallets)}")
