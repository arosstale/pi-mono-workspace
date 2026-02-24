#!/usr/bin/env python3
"""
research_daemon.py - Research Engine Daemon
Part of Research Engine - arXiv Paper Discovery System

Purpose:
  - Periodically fetches arXiv papers based on configured domains
  - Stores metadata in SQLite database for searchability
  - Generates daily markdown reports
  - Logs to journalctl for systemd compatibility

Usage:
  - Direct: python3 research_daemon.py
  - Cron: Run every 6 hours (00:00, 06:00, 12:00, 18:00)
  - systemd: research_daemon.service

Author: OpenClaw Research Engine
Version: 1.0
"""

import sys
import os
import logging
import sqlite3
import json
import subprocess
from datetime import datetime, date
from pathlib import Path
from typing import List, Dict, Optional
import argparse

# Configure logging for journalctl compatibility
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger('research_daemon')

# Paths
RESEARCH_DIR = Path(__file__).parent
RESEARCH_DB = RESEARCH_DIR / "research.db"
FETCHER_SCRIPT = Path(__file__).parent.parent / "openclaw-memory-template" / "scripts" / "arxiv_fetcher.py"
DOMAINS_FILE = RESEARCH_DIR / "domains.json"
PAPERS_DIR = RESEARCH_DIR / "papers"
DAILY_REPORTS_DIR = RESEARCH_DIR / "research" / "daily"
STATUS_FILE = RESEARCH_DIR / "status.json"


class ResearchDaemon:
    """Research engine daemon for periodic paper discovery."""

    def __init__(self, dry_run: bool = False):
        self.dry_run = dry_run
        self.research_dir = RESEARCH_DIR
        self.db_path = RESEARCH_DB
        self.fetcher_script = FETCHER_SCRIPT
        self.domains_file = DOMAINS_FILE
        self.papers_dir = PAPERS_DIR

        # Ensure directories exist
        self.papers_dir.mkdir(exist_ok=True)
        DAILY_REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    def load_domains(self) -> List[Dict]:
        """Load domain configuration from domains.json."""
        try:
            with open(self.domains_file, 'r') as f:
                data = json.load(f)
                # Handle format where domains are key-value pairs
                if isinstance(data, dict):
                    domains = []
                    for key, value in data.items():
                        domain = value.copy()
                        domain['key'] = key
                        domains.append(domain)
                    return domains
                return data.get('domains', [])
        except FileNotFoundError:
            logger.error(f"Domains file not found: {self.domains_file}")
            return []
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in domains file: {e}")
            return []

    def run_fetcher(self, domains: List[str] = None) -> Dict:
        """Run the arXiv fetcher and return results."""
        if self.dry_run:
            logger.info("DRY RUN: Would run fetcher")
            return {"status": "dry_run", "papers_fetched": 0}

        if not self.fetcher_script.exists():
            logger.error(f"Fetcher script not found: {self.fetcher_script}")
            return {"status": "error", "message": "Fetcher not found"}

        cmd = [sys.executable, str(self.fetcher_script)]
        if domains:
            cmd.extend(domains)

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )

            if result.returncode != 0:
                logger.error(f"Fetcher failed: {result.stderr}")
                return {
                    "status": "error",
                    "message": result.stderr,
                    "papers_fetched": 0
                }

            # Parse output for stats
            papers_fetched = 0
            for line in result.stdout.split('\n'):
                if 'Total:' in line and 'papers' in line:
                    try:
                        papers_fetched = int(line.split('(')[0].split(':')[-1].strip())
                    except (IndexError, ValueError):
                        pass

            logger.info(f"Fetcher completed: {papers_fetched} papers")
            return {
                "status": "success",
                "papers_fetched": papers_fetched,
                "output": result.stdout
            }

        except subprocess.TimeoutExpired:
            logger.error("Fetcher timeout after 5 minutes")
            return {"status": "error", "message": "Timeout", "papers_fetched": 0}
        except Exception as e:
            logger.error(f"Fetcher error: {e}")
            return {"status": "error", "message": str(e), "papers_fetched": 0}

    def get_db_stats(self) -> Dict:
        """Get statistics from the database."""
        try:
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()

            # Paper counts
            cursor.execute("SELECT COUNT(*) FROM papers")
            total_papers = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM authors")
            total_authors = cursor.fetchone()[0]

            # Recent papers (last 7 days)
            cursor.execute("""
                SELECT COUNT(*) FROM papers
                WHERE published >= date('now', '-7 days')
            """)
            recent_papers = cursor.fetchone()[0]

            # Papers by domain
            cursor.execute("""
                SELECT domain, COUNT(*) as count
                FROM papers
                GROUP BY domain
                ORDER BY count DESC
            """)
            by_domain = {row[0]: row[1] for row in cursor.fetchall()}

            conn.close()

            return {
                "total_papers": total_papers,
                "total_authors": total_authors,
                "recent_papers": recent_papers,
                "by_domain": by_domain
            }

        except Exception as e:
            logger.error(f"Database error: {e}")
            return {}

    def log_scan(self, papers_found: int, new_papers: int) -> None:
        """Log a scan to the database."""
        try:
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO scan_logs (scan_date, papers_found, new_papers)
                VALUES (?, ?, ?)
            """, (date.today(), papers_found, new_papers))

            conn.commit()
            conn.close()

            logger.info(f"Scan logged: {papers_found} found, {new_papers} new")

        except Exception as e:
            logger.error(f"Failed to log scan: {e}")

    def generate_daily_report(self) -> str:
        """Generate daily markdown report."""
        today = date.today()
        report_file = DAILY_REPORTS_DIR / f"DAILY_RESEARCH_{today}.md"

        if self.dry_run:
            logger.info(f"DRY RUN: Would generate {report_file.name}")
            return str(report_file)

        try:
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()

            # Get today's papers
            cursor.execute("""
                SELECT p.id, p.title, p.published, p.link, p.domain
                FROM papers p
                WHERE p.published = ?
                ORDER BY p.published DESC
                LIMIT 50
            """, (today,))

            papers = cursor.fetchall()
            conn.close()

            # Build markdown report
            report = f"""# Daily Research Report - {today}

Generated by research_daemon.py at {datetime.now().strftime('%H:%M:%S')} UTC

---

## 📊 Today's Statistics

- **Papers found:** {len(papers)}
- **Database total:** {self.get_db_stats().get('total_papers', 0)}

---

## 📚 Papers from {today}

"""

            for paper in papers:
                paper_id, title, published, link, domain = paper
                report += f"""
### [{title}]({link})

- **ID:** {paper_id}
- **Domain:** {domain}
- **Published:** {published}

"""

            # Write report
            with open(report_file, 'w') as f:
                f.write(report)

            logger.info(f"Daily report generated: {report_file}")
            return str(report_file)

        except Exception as e:
            logger.error(f"Failed to generate report: {e}")
            return ""

    def run(self, domains: List[str] = None) -> bool:
        """Main daemon execution."""
        logger.info("=" * 60)
        logger.info("📚 Research Engine Daemon - Starting")
        logger.info(f"📅 Scan date: {date.today()}")
        logger.info("=" * 60)

        # Load domains
        domain_configs = self.load_domains()
        if not domain_configs:
            logger.warning("No domains configured, will use fetcher defaults")

        # Run fetcher
        logger.info("🔍 Running arXiv fetcher...")
        fetcher_result = self.run_fetcher(domains)

        if fetcher_result["status"] == "error":
            logger.error(f"❌ Fetcher failed: {fetcher_result.get('message', 'Unknown error')}")
            self.log_scan(0, 0)
            return False

        papers_fetched = fetcher_result.get("papers_fetched", 0)

        # Get database stats
        stats = self.get_db_stats()
        logger.info(f"📊 Database: {stats.get('total_papers', 0)} papers, {stats.get('total_authors', 0)} authors")

        # Log scan
        self.log_scan(papers_fetched, 0)  # Simplified new paper tracking

        # Generate daily report
        logger.info("📝 Generating daily report...")
        report_file = self.generate_daily_report()

        # Update status file
        status = {
            "last_run": datetime.now().isoformat(),
            "last_scan": date.today().isoformat(),
            "papers_fetched": papers_fetched,
            "db_stats": stats,
            "report_file": str(report_file) if report_file else None
        }

        with open(STATUS_FILE, 'w') as f:
            json.dump(status, f, indent=2)

        logger.info("=" * 60)
        logger.info("✅ Research Engine Daemon - Complete")
        logger.info("=" * 60)

        return True


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description='Research Engine Daemon')
    parser.add_argument('--dry-run', action='store_true',
                       help='Run in dry-run mode (no changes)')
    parser.add_argument('--domains', nargs='+', help='Specific domains to fetch')

    args = parser.parse_args()

    daemon = ResearchDaemon(dry_run=args.dry_run)
    success = daemon.run(domains=args.domains)

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
