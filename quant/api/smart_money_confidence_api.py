"""
Smart Money Confidence API

REST API endpoint for querying and managing Smart Money Confidence Scores.

Endpoints:
- GET /api/v1/smart-money-confidence - Get all latest confidence scores
- GET /api/v1/smart-money-confidence/{wallet} - Get confidence for specific wallet
- GET /api/v1/smart-money-confidence/elite - Get elite wallets
- GET /api/v1/smart-money-confidence/{wallet}/history - Get wallet score history
- POST /api/v1/smart-money-confidence/recalculate - Recalculate specific wallet
"""

from flask import Flask, jsonify, request
from datetime import datetime
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from signals.smart_money_confidence import (
    SmartMoneyConfidenceCalculator,
    recalculate_wallet_confidence,
    get_all_wallet_confidences,
    ScoreCategory
)

app = Flask(__name__)

# Configuration
DB_PATH = os.environ.get('TRADING_DB_PATH', 'quant/data/trading.db')
DEFAULT_DAYS = 30


def make_cors_response(data=None, status=200):
    """Make response with CORS headers."""
    response = jsonify(data) if data is not None else jsonify({})
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST,OPTIONS')
    response.status_code = status
    return response


@app.route('/api/v1/smart-money-confidence', methods=['GET', 'OPTIONS'])
def get_all_confidence_scores():
    """
    Get latest confidence scores for all wallets.

    Query Parameters:
    - limit: Maximum number of wallets to return (default: 100)
    - category: Filter by category (ELITE, STRONG, MODERATE, WEAK, POOR)
    """
    if request.method == 'OPTIONS':
        return make_cors_response()

    try:
        limit = request.args.get('limit', 100, type=int)
        category_filter = request.args.get('category')

        calculator = SmartMoneyConfidenceCalculator(DB_PATH)
        scores = calculator.get_latest_confidence_scores(limit=limit)

        # Filter by category if specified
        if category_filter:
            try:
                category = ScoreCategory[category_filter.upper()]
                scores = [s for s in scores if s.category == category]
            except KeyError:
                return make_cors_response(
                    {'error': f'Invalid category: {category_filter}'},
                    400
                )

        # Convert to dict format
        result = {
            'count': len(scores),
            'scores': [
                {
                    'wallet_address': score.wallet_address,
                    'overall_score': score.overall_score,
                    'category': score.category.value,
                    'trend': score.trend,
                    'calculated_at': score.calculated_at.isoformat(),
                    'components': {
                        'win_rate_score': score.win_rate_score,
                        'trade_count_score': score.trade_count_score,
                        'avg_notional_score': score.avg_notional_score,
                        'consistency_score': score.consistency_score,
                        'market_timing_score': score.market_timing_score
                    }
                }
                for score in scores
            ]
        }

        return make_cors_response(result)

    except Exception as e:
        return make_cors_response(
            {'error': str(e)},
            500
        )


@app.route('/api/v1/smart-money-confidence/<wallet_address>', methods=['GET', 'OPTIONS'])
def get_wallet_confidence(wallet_address: str):
    """
    Get latest confidence score for a specific wallet.

    Path Parameters:
    - wallet_address: Wallet address

    Query Parameters:
    - days: Number of days to analyze (default: 30)
    """
    if request.method == 'OPTIONS':
        return make_cors_response()

    try:
        days = request.args.get('days', DEFAULT_DAYS, type=int)

        calculator = SmartMoneyConfidenceCalculator(DB_PATH)
        score = calculator.calculate_confidence(wallet_address, days)

        result = {
            'wallet_address': score.wallet_address,
            'overall_score': score.overall_score,
            'category': score.category.value,
            'trend': score.trend,
            'calculated_at': score.calculated_at.isoformat(),
            'components': {
                'win_rate_score': score.win_rate_score,
                'trade_count_score': score.trade_count_score,
                'avg_notional_score': score.avg_notional_score,
                'consistency_score': score.consistency_score,
                'market_timing_score': score.market_timing_score
            },
            'statistics': calculator.get_wallet_statistics(wallet_address, days)
        }

        return make_cors_response(result)

    except Exception as e:
        return make_cors_response(
            {'error': str(e)},
            500
        )


@app.route('/api/v1/smart-money-confidence/elite', methods=['GET', 'OPTIONS'])
def get_elite_wallets():
    """
    Get wallets with elite confidence scores.

    Query Parameters:
    - threshold: Minimum score to be considered elite (default: 90.0)
    - check_decline: If true, exclude wallets in decline (default: true)
    """
    if request.method == 'OPTIONS':
        return make_cors_response()

    try:
        threshold = request.args.get('threshold', 90.0, type=float)
        check_decline = request.args.get('check_decline', True, type=bool)

        calculator = SmartMoneyConfidenceCalculator(DB_PATH)
        scores = calculator.get_elite_wallets(threshold=threshold, check_decline=check_decline)

        result = {
            'count': len(scores),
            'threshold': threshold,
            'wallets': [
                {
                    'wallet_address': score.wallet_address,
                    'overall_score': score.overall_score,
                    'trend': score.trend,
                    'calculated_at': score.calculated_at.isoformat()
                }
                for score in scores
            ]
        }

        return make_cors_response(result)

    except Exception as e:
        return make_cors_response(
            {'error': str(e)},
            500
        )


@app.route('/api/v1/smart-money-confidence/<wallet_address>/history', methods=['GET', 'OPTIONS'])
def get_wallet_history(wallet_address: str):
    """
    Get confidence score history for a specific wallet.

    Path Parameters:
    - wallet_address: Wallet address

    Query Parameters:
    - days: Number of days of history to retrieve (default: 30)
    """
    if request.method == 'OPTIONS':
        return make_cors_response()

    try:
        days = request.args.get('days', 30, type=int)

        calculator = SmartMoneyConfidenceCalculator(DB_PATH)
        scores = calculator.get_wallet_history(wallet_address, days)

        result = {
            'wallet_address': wallet_address,
            'period_days': days,
            'data_points': len(scores),
            'history': [
                {
                    'overall_score': score.overall_score,
                    'category': score.category.value,
                    'trend': score.trend,
                    'calculated_at': score.calculated_at.isoformat(),
                    'components': {
                        'win_rate_score': score.win_rate_score,
                        'trade_count_score': score.trade_count_score,
                        'avg_notional_score': score.avg_notional_score,
                        'consistency_score': score.consistency_score,
                        'market_timing_score': score.market_timing_score
                    }
                }
                for score in scores
            ]
        }

        return make_cors_response(result)

    except Exception as e:
        return make_cors_response(
            {'error': str(e)},
            500
        )


@app.route('/api/v1/smart-money-confidence/recalculate', methods=['POST', 'OPTIONS'])
def recalculate_confidence():
    """
    Recalculate confidence score for a wallet or all wallets.

    Request Body:
    {
        "wallet_address": "0x123...",  // Optional - if omitted, recalculate all
        "days": 30,                     // Optional - analysis period
        "save": true                    // Optional - save to database
    }
    """
    if request.method == 'OPTIONS':
        return make_cors_response()

    try:
        data = request.get_json() or {}
        wallet_address = data.get('wallet_address')
        days = data.get('days', DEFAULT_DAYS)
        save_to_db = data.get('save', True)

        if wallet_address:
            # Recalculate specific wallet
            score = recalculate_wallet_confidence(
                wallet_address,
                db_path=DB_PATH,
                days=days
            )

            if not score:
                return make_cors_response(
                    {'error': 'Failed to calculate confidence score'},
                    500
                )

            result = {
                'wallet_address': score.wallet_address,
                'overall_score': score.overall_score,
                'category': score.category.value,
                'trend': score.trend,
                'calculated_at': score.calculated_at.isoformat(),
                'saved': save_to_db
            }
        else:
            # Recalculate all wallets
            scores = get_all_wallet_confidences(
                db_path=DB_PATH,
                days=days
            )

            result = {
                'count': len(scores),
                'saved': save_to_db,
                'wallets': [
                    {
                        'wallet_address': score.wallet_address,
                        'overall_score': score.overall_score,
                        'category': score.category.value
                    }
                    for score in scores
                ]
            }

        return make_cors_response(result)

    except Exception as e:
        return make_cors_response(
            {'error': str(e)},
            500
        )


@app.route('/api/v1/smart-money-confidence/categories', methods=['GET', 'OPTIONS'])
def get_categories():
    """
    Get available score categories and their descriptions.
    """
    if request.method == 'OPTIONS':
        return make_cors_response()

    categories = {
        'ELITE': {
            'range': '90-100',
            'description': 'Top 1% - Exceptional smart money',
            'characteristics': 'High win rate, consistent performance, excellent market timing'
        },
        'STRONG': {
            'range': '75-89',
            'description': 'Top 5% - Very reliable smart money',
            'characteristics': 'Good win rate, decent consistency, solid market timing'
        },
        'MODERATE': {
            'range': '60-74',
            'description': 'Top 20% - Above average',
            'characteristics': 'Moderate win rate, some consistency, average market timing'
        },
        'WEAK': {
            'range': '40-59',
            'description': 'Below average',
            'characteristics': 'Low win rate, inconsistent, poor market timing'
        },
        'POOR': {
            'range': '0-39',
            'description': 'Unreliable',
            'characteristics': 'Very low win rate, highly inconsistent, poor decisions'
        }
    }

    return make_cors_response(categories)


@app.route('/api/v1/smart-money-confidence/alerts', methods=['GET', 'OPTIONS'])
def get_confidence_alerts():
    """
    Get alerts for elite wallets whose confidence has dropped significantly.

    Query Parameters:
    - threshold: Minimum score to check (default: 90.0)
    - drop_threshold: Minimum drop to trigger alert (default: 10.0)
    """
    if request.method == 'OPTIONS':
        return make_cors_response()

    try:
        threshold = request.args.get('threshold', 90.0, type=float)
        drop_threshold = request.args.get('drop_threshold', 10.0, type=float)

        calculator = SmartMoneyConfidenceCalculator(DB_PATH)

        # Get elite wallets with downward trend
        elite_wallets = calculator.get_elite_wallets(
            threshold=threshold,
            check_decline=False  # Include declining wallets
        )

        # Get declining wallets
        declining_wallets = [
            wallet for wallet in elite_wallets
            if wallet.trend == 'down'
        ]

        # Check for significant drops
        alerts = []
        for wallet in declining_wallets:
            # Get history to calculate actual drop
            history = calculator.get_wallet_history(wallet.wallet_address, days=7)

            if len(history) >= 2:
                previous_score = history[-2].overall_score
                current_score = history[-1].overall_score
                drop = previous_score - current_score

                if drop >= drop_threshold:
                    alerts.append({
                        'wallet_address': wallet.wallet_address,
                        'previous_score': previous_score,
                        'current_score': current_score,
                        'drop': round(drop, 2),
                        'drop_percentage': round((drop / previous_score) * 100, 2),
                        'alert_level': 'CRITICAL' if drop >= 20 else 'WARNING'
                    })

        result = {
            'alert_count': len(alerts),
            'thresholds': {
                'elite_threshold': threshold,
                'drop_threshold': drop_threshold
            },
            'alerts': alerts
        }

        return make_cors_response(result)

    except Exception as e:
        return make_cors_response(
            {'error': str(e)},
            500
        )


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return make_cors_response({
        'status': 'healthy',
        'service': 'smart-money-confidence-api',
        'timestamp': datetime.utcnow().isoformat()
    })


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    print(f"Starting Smart Money Confidence API on port {port}")
    print(f"Database: {DB_PATH}")
    app.run(host='0.0.0.0', port=port, debug=True)
