"""
Smart Money Confidence Report Generator

Generates daily markdown reports on Smart Money Confidence Scores.

Report Contents:
- Summary statistics
- Elite wallet rankings
- Category breakdown
- Recent score changes
- Confidence trends
- Alerts for declining elite wallets
"""

from datetime import datetime, timedelta
import os
from typing import List, Dict
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from signals.smart_money_confidence import (
    SmartMoneyConfidenceCalculator,
    ConfidenceScore,
    ScoreCategory
)


class ConfidenceReportGenerator:
    """Generate markdown reports for Smart Money Confidence Scores."""

    def __init__(self, db_path: str = 'quant/data/trading.db'):
        """
        Initialize report generator.

        Args:
            db_path: Path to SQLite database
        """
        self.db_path = db_path
        self.calculator = SmartMoneyConfidenceCalculator(db_path)
        self.report_date = datetime.utcnow()

    def generate_report(self, output_path: str = None) -> str:
        """
        Generate full confidence report.

        Args:
            output_path: Path to save report (optional)

        Returns:
            Markdown report content
        """
        # Get latest scores
        all_scores = self.calculator.get_latest_confidence_scores(limit=1000)

        if not all_scores:
            return "# Smart Money Confidence Report\n\nNo data available."

        # Generate report sections
        markdown = []

        # Title and metadata
        markdown.append(self._generate_header())

        # Summary statistics
        markdown.append(self._generate_summary(all_scores))

        # Category breakdown
        markdown.append(self._generate_category_breakdown(all_scores))

        # Elite wallet rankings
        markdown.append(self._generate_elite_rankings(all_scores))

        # Top performers by component
        markdown.append(self._generate_top_performers(all_scores))

        # Recent score changes
        markdown.append(self._generate_recent_changes(all_scores))

        # Confidence trends
        markdown.append(self._generate_trends(all_scores))

        # Alerts
        markdown.append(self._generate_alerts(all_scores))

        # Methodology
        markdown.append(self._generate_methodology())

        # Combine all sections
        report = '\n\n'.join(markdown)

        # Save to file if path provided
        if output_path:
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            with open(output_path, 'w') as f:
                f.write(report)
            print(f"Report saved to: {output_path}")

        return report

    def _generate_header(self) -> str:
        """Generate report header."""
        return f"""# Smart Money Confidence Report

**Generated:** {self.report_date.strftime('%Y-%m-%d %H:%M:%S UTC')}
**Analysis Period:** Last 30 days

---

## Overview

This report provides a comprehensive analysis of Smart Money Confidence Scores across all tracked wallets. Confidence scores measure the quality and reliability of wallet behavior, not just the quantity of activity.

**Score Categories:**
- **ELITE (90-100)**: Top 1% - Exceptional smart money
- **STRONG (75-89)**: Top 5% - Very reliable smart money
- **MODERATE (60-74)**: Top 20% - Above average
- **WEAK (40-59)**: Below average
- **POOR (0-39)**: Unreliable

---

## Scoring Methodology

The confidence score combines five weighted factors:

| Factor | Weight | Description |
|--------|--------|-------------|
| Win Rate | 30% | Percentage of profitable trades |
| Trade Count | 10% | Number of trades (more data = higher confidence) |
| Average Notional | 20% | Average trade size (skin in the game) |
| Consistency | 25% | Stability of win rate over time |
| Market Timing | 15% | Tendency to buy low and sell high |

---

"""

    def _generate_summary(self, scores: List[ConfidenceScore]) -> str:
        """Generate summary statistics section."""
        total_wallets = len(scores)

        # Count by category
        category_counts = {}
        for score in scores:
            category = score.category.value
            category_counts[category] = category_counts.get(category, 0) + 1

        # Calculate average scores
        avg_overall = sum(s.overall_score for s in scores) / total_wallets
        avg_win_rate = sum(s.win_rate_score for s in scores) / total_wallets
        avg_consistency = sum(s.consistency_score for s in scores) / total_wallets

        # Trend distribution
        trend_counts = {'up': 0, 'down': 0, 'neutral': 0}
        for score in scores:
            trend_counts[score.trend] += 1

        return f"""## Summary Statistics

**Total Wallets Analyzed:** {total_wallets}

### Category Distribution

| Category | Count | Percentage |
|----------|-------|------------|
| ELITE (90-100) | {category_counts.get('ELITE', 0)} | {category_counts.get('ELITE', 0) / total_wallets * 100:.1f}% |
| STRONG (75-89) | {category_counts.get('STRONG', 0)} | {category_counts.get('STRONG', 0) / total_wallets * 100:.1f}% |
| MODERATE (60-74) | {category_counts.get('MODERATE', 0)} | {category_counts.get('MODERATE', 0) / total_wallets * 100:.1f}% |
| WEAK (40-59) | {category_counts.get('WEAK', 0)} | {category_counts.get('WEAK', 0) / total_wallets * 100:.1f}% |
| POOR (0-39) | {category_counts.get('POOR', 0)} | {category_counts.get('POOR', 0) / total_wallets * 100:.1f}% |

### Average Scores

- **Overall Confidence:** {avg_overall:.2f}
- **Win Rate Score:** {avg_win_rate:.2f}
- **Consistency Score:** {avg_consistency:.2f}

### Trend Distribution

| Trend | Count | Percentage |
|-------|-------|------------|
| Improving (↑) | {trend_counts['up']} | {trend_counts['up'] / total_wallets * 100:.1f}% |
| Declining (↓) | {trend_counts['down']} | {trend_counts['down'] / total_wallets * 100:.1f}% |
| Stable (→) | {trend_counts['neutral']} | {trend_counts['neutral'] / total_wallets * 100:.1f}% |

---

"""

    def _generate_category_breakdown(self, scores: List[ConfidenceScore]) -> str:
        """Generate category breakdown section."""
        categories = {
            ScoreCategory.ELITE: [],
            ScoreCategory.STRONG: [],
            ScoreCategory.MODERATE: [],
            ScoreCategory.WEAK: [],
            ScoreCategory.POOR: []
        }

        for score in scores:
            categories[score.category].append(score)

        markdown = ["## Category Breakdown\n"]

        for category, cat_scores in categories.items():
            if not cat_scores:
                continue

            cat_scores.sort(key=lambda x: x.overall_score, reverse=True)

            avg_score = sum(s.overall_score for s in cat_scores) / len(cat_scores)
            avg_trades = sum(s.trade_count_score for s in cat_scores) / len(cat_scores) / 2  # Convert to 0-100 scale

            markdown.append(f"### {category.value} ({len(cat_scores)} wallets)")
            markdown.append(f"**Average Score:** {avg_score:.2f}")
            markdown.append(f"**Average Trade Activity:** {avg_trades:.1f}/100\n")

            # Show top 5 in this category
            markdown.append("**Top Performers:**")
            markdown.append("| Rank | Wallet | Score | Trend |")
            markdown.append("|------|--------|-------|-------|")

            for i, score in enumerate(cat_scores[:5], 1):
                trend_emoji = {'up': '↑', 'down': '↓', 'neutral': '→'}
                markdown.append(
                    f"| {i} | `{score.wallet_address[:10]}...` | {score.overall_score:.1f} | {trend_emoji[score.trend]} |"
                )

            markdown.append("\n---\n")

        return '\n'.join(markdown)

    def _generate_elite_rankings(self, scores: List[ConfidenceScore]) -> str:
        """Generate elite wallet rankings section."""
        elite = [s for s in scores if s.category == ScoreCategory.ELITE]
        elite.sort(key=lambda x: x.overall_score, reverse=True)

        if not elite:
            return "## Elite Wallet Rankings\n\nNo elite wallets found.\n\n---\n"

        markdown = ["## Elite Wallet Rankings (Top 1%)\n"]
        markdown.append(f"**Total Elite Wallets:** {len(elite)}\n")
        markdown.append("| Rank | Wallet | Score | Win Rate | Consistency | Market Timing | Trend |")
        markdown.append("|------|--------|-------|----------|-------------|---------------|-------|")

        for i, score in enumerate(elite, 1):
            trend_emoji = {'up': '↑', 'down': '↓', 'neutral': '→'}
            markdown.append(
                f"| {i} | `{score.wallet_address[:10]}...` | {score.overall_score:.1f} | {score.win_rate_score:.1f} | {score.consistency_score:.1f} | {score.market_timing_score:.1f} | {trend_emoji[score.trend]} |"
            )

        markdown.append("\n---\n")

        return '\n'.join(markdown)

    def _generate_top_performers(self, scores: List[ConfidenceScore]) -> str:
        """Generate top performers by component section."""
        if not scores:
            return ""

        markdown = ["## Top Performers by Component\n"]

        # Top win rate
        sorted_win_rate = sorted(scores, key=lambda x: x.win_rate_score, reverse=True)
        markdown.append("### 🎯 Highest Win Rate")
        markdown.append("| Rank | Wallet | Score |")
        markdown.append("|------|--------|------|")
        for i, score in enumerate(sorted_win_rate[:5], 1):
            markdown.append(f"| {i} | `{score.wallet_address[:10]}...` | {score.win_rate_score:.1f} |")

        # Top consistency
        sorted_consistency = sorted(scores, key=lambda x: x.consistency_score, reverse=True)
        markdown.append("\n### 📊 Most Consistent")
        markdown.append("| Rank | Wallet | Score |")
        markdown.append("|------|--------|------|")
        for i, score in enumerate(sorted_consistency[:5], 1):
            markdown.append(f"| {i} | `{score.wallet_address[:10]}...` | {score.consistency_score:.1f} |")

        # Top market timing
        sorted_timing = sorted(scores, key=lambda x: x.market_timing_score, reverse=True)
        markdown.append("\n### ⏰ Best Market Timing")
        markdown.append("| Rank | Wallet | Score |")
        markdown.append("|------|--------|------|")
        for i, score in enumerate(sorted_timing[:5], 1):
            markdown.append(f"| {i} | `{score.wallet_address[:10]}...` | {score.market_timing_score:.1f} |")

        # Most active (highest trade count)
        sorted_activity = sorted(scores, key=lambda x: x.trade_count_score, reverse=True)
        markdown.append("\n### 🔥 Most Active")
        markdown.append("| Rank | Wallet | Score |")
        markdown.append("|------|--------|------|")
        for i, score in enumerate(sorted_activity[:5], 1):
            markdown.append(f"| {i} | `{score.wallet_address[:10]}...` | {score.trade_count_score:.1f} |")

        markdown.append("\n---\n")

        return '\n'.join(markdown)

    def _generate_recent_changes(self, scores: List[ConfidenceScore]) -> str:
        """Generate recent score changes section."""
        trending_up = [s for s in scores if s.trend == 'up']
        trending_down = [s for s in scores if s.trend == 'down']

        trending_up.sort(key=lambda x: x.overall_score, reverse=True)
        trending_down.sort(key=lambda x: x.overall_score, reverse=True)

        markdown = ["## Recent Score Changes\n"]

        if trending_up:
            markdown.append(f"### 📈 Improving ({len(trending_up)} wallets)")
            markdown.append("| Wallet | Score | Category |")
            markdown.append("|--------|-------|----------|")
            for score in trending_up[:10]:
                markdown.append(f"| `{score.wallet_address[:10]}...` | {score.overall_score:.1f} | {score.category.value} |")

        if trending_down:
            markdown.append(f"\n### 📉 Declining ({len(trending_down)} wallets)")
            markdown.append("| Wallet | Score | Category |")
            markdown.append("|--------|-------|----------|")
            for score in trending_down[:10]:
                markdown.append(f"| `{score.wallet_address[:10]}...` | {score.overall_score:.1f} | {score.category.value} |")

        markdown.append("\n---\n")

        return '\n'.join(markdown)

    def _generate_trends(self, scores: List[ConfidenceScore]) -> str:
        """Generate confidence trends section."""
        markdown = ["## Confidence Trends Analysis\n"]

        # Wallets approaching elite status
        near_elite = [
            s for s in scores
            if 85 <= s.overall_score < 90 and s.trend == 'up'
        ]
        near_elite.sort(key=lambda x: x.overall_score, reverse=True)

        if near_elite:
            markdown.append(f"### 🚀 Approaching Elite Status ({len(near_elite)} wallets)")
            markdown.append("These wallets are trending up and approaching elite status:")
            markdown.append("| Wallet | Score | Trend |")
            markdown.append("|--------|-------|-------|")
            for score in near_elite[:5]:
                markdown.append(f"| `{score.wallet_address[:10]}...` | {score.overall_score:.1f} | ↑ |")

        # Wallets at risk of dropping categories
        at_risk = []
        for score in scores:
            if score.category == ScoreCategory.ELITE and score.trend == 'down':
                at_risk.append(('Elite', score))
            elif score.category == ScoreCategory.STRONG and score.trend == 'down':
                at_risk.append(('Strong', score))

        if at_risk:
            markdown.append(f"\n### ⚠️ At Risk of Downgrade ({len(at_risk)} wallets)")
            markdown.append("These top wallets are declining and at risk of dropping category:")
            markdown.append("| Wallet | Category | Score | Trend |")
            markdown.append("|--------|----------|-------|-------|")
            for category, score in at_risk[:5]:
                markdown.append(f"| `{score.wallet_address[:10]}...` | {category} | {score.overall_score:.1f} | ↓ |")

        markdown.append("\n---\n")

        return '\n'.join(markdown)

    def _generate_alerts(self, scores: List[ConfidenceScore]) -> str:
        """Generate alerts section."""
        alerts = []

        # Elite wallets with significant decline
        for score in scores:
            if score.category == ScoreCategory.ELITE and score.trend == 'down':
                # Get recent history to check for significant drop
                history = self.calculator.get_wallet_history(score.wallet_address, days=7)

                if len(history) >= 2:
                    previous_score = history[-2].overall_score
                    current_score = score.overall_score
                    drop = previous_score - current_score

                    if drop >= 10:  # Significant drop
                        alerts.append({
                            'type': 'CRITICAL' if drop >= 20 else 'WARNING',
                            'wallet': score.wallet_address,
                            'previous': previous_score,
                            'current': current_score,
                            'drop': drop
                        })

        markdown = ["## 🚨 Alerts\n"]

        if not alerts:
            markdown.append("**No alerts at this time.** All elite wallets are stable or improving.")
        else:
            critical = [a for a in alerts if a['type'] == 'CRITICAL']
            warnings = [a for a in alerts if a['type'] == 'WARNING']

            if critical:
                markdown.append(f"### CRITICAL Alerts ({len(critical)})")
                markdown.append("Elite wallets experiencing significant decline (>20 points):")
                markdown.append("| Wallet | Previous | Current | Drop |")
                markdown.append("|--------|----------|---------|------|")
                for alert in critical:
                    markdown.append(
                        f"| `{alert['wallet'][:10]}...` | {alert['previous']:.1f} | {alert['current']:.1f} | -{alert['drop']:.1f} |"
                    )

            if warnings:
                markdown.append(f"\n### WARNING Alerts ({len(warnings)})")
                markdown.append("Elite wallets experiencing moderate decline (10-20 points):")
                markdown.append("| Wallet | Previous | Current | Drop |")
                markdown.append("|--------|----------|---------|------|")
                for alert in warnings[:5]:  # Limit warnings
                    markdown.append(
                        f"| `{alert['wallet'][:10]}...` | {alert['previous']:.1f} | {alert['current']:.1f} | -{alert['drop']:.1f} |"
                    )

        markdown.append("\n---\n")

        return '\n'.join(markdown)

    def _generate_methodology(self) -> str:
        """Generate methodology section."""
        return """## Methodology Notes

### Data Quality
- Only closed trades are included in calculations
- Minimum 3 trades per day for daily consistency metrics
- Minimum 3 days of trading activity required for consistency score

### Score Interpretation
- **Scores above 90** represent exceptional traders with proven track records
- **Scores between 75-89** indicate strong, reliable performance
- **Scores between 60-74** show above-average but inconsistent results
- **Scores below 60** suggest unreliable or novice trading behavior

### Limitations
- Market timing analysis is simplified (compares entry/exit prices)
- Short trading history may lead to inflated or deflated scores
- Sudden market events may temporarily affect scores
- Scores should be considered alongside other metrics for complete analysis

### Recommendations
- Follow ELITE wallets for high-conviction trade ideas
- Monitor STRONG wallets for additional alpha opportunities
- Use trend information to identify improving or deteriorating performance
- Set alerts for elite wallet score declines to catch deteriorating performance early

---

*Report generated by Smart Money Confidence System*
*For questions or feedback, refer to the system documentation*
"""


def generate_daily_report(output_dir: str = 'quant/reports',
                         db_path: str = 'quant/data/trading.db') -> str:
    """
    Generate daily confidence report.

    Args:
        output_dir: Directory to save reports
        db_path: Path to database

    Returns:
        Path to generated report
    """
    # Create output directory if needed
    os.makedirs(output_dir, exist_ok=True)

    # Generate filename with date
    date_str = datetime.utcnow().strftime('%Y%m%d')
    report_path = os.path.join(output_dir, f'smart_money_confidence_{date_str}.md')

    # Generate report
    generator = ConfidenceReportGenerator(db_path)
    generator.generate_report(report_path)

    return report_path


if __name__ == '__main__':
    # Generate daily report
    report_path = generate_daily_report()
    print(f"Report generated: {report_path}")
