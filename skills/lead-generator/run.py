#!/usr/bin/env python3
"""
Lead Generator - Automated lead generation for trade shows, directories, and business listings.

Phase 1: Data Sources (trade shows, directories, websites)
Phase 2: Enrichment (website scraping, email discovery)
Phase 3: Qualification (scoring, filtering)
Phase 4: Storage (CSV, Excel, SQLite)
Phase 5: Outreach (emails, LinkedIn messages)
"""

import argparse
import logging
import sys
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('lead_generator.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class LeadGenerator:
    """Main lead generation orchestrator."""

    def __init__(self, config_path: str = "config.json"):
        self.config_path = config_path
        self.config = self._load_config()
        self.leads: List[Dict] = []

    def _load_config(self) -> Dict:
        """Load configuration from config.json."""
        import json
        try:
            with open(self.config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.warning(f"Config file not found: {self.config_path}. Using defaults.")
            return self._default_config()

    def _default_config(self) -> Dict:
        """Default configuration."""
        return {
            "sender": {
                "name": "Alessandro",
                "title": "Founder & CEO",
                "company": "OpenClaw",
                "email": "ciao@openclaw.ai",
                "phone": "+39 329 348 4956",
            },
            "filters": {
                "exclude_business_services": True,
                "min_score": 50,
                "industries": [],
            }
        }

    def scrape_trade_show(self, url: str, filter_services: bool = True) -> List[Dict]:
        """Scrape trade show exhibitors."""
        logger.info(f"Scraping trade show: {url}")

        # Import trade show scrapers
        sys.path.insert(0, str(Path(__file__).parent.parent.parent / "trade-show-scraping"))

        try:
            from smallworldlabs_scraper import SmallWorldLabsScraper
        except ImportError:
            logger.error("SmallWorldLabs scraper not found. Is trade-show-scraping in parent directory?")
            return []

        try:
            from utils import filter_business_services
        except ImportError:
            logger.error("Utils module not found")
            return []

        scraper = SmallWorldLabsScraper(url, "trade_show_scraper")
        scraper.scrape_all()

        # Filter business services if enabled
        if filter_services:
            logger.info("Filtering out business services (consulting, agencies, etc.)")
            leads = filter_business_services(scraper.exhibitors)
        else:
            leads = scraper.exhibitors

        logger.info(f"Scraped {len(leads)} leads")
        return leads

    def scrape_browser_query(self, query: str, limit: int = 50) -> List[Dict]:
        """Scrape using browser automation (placeholder - needs browser tool)."""
        logger.info(f"Browser scraping query: {query}")
        logger.info("Note: Browser scraping requires browser tool integration.")

        # Placeholder for browser scraping
        # In production, this would use the browser tool
        leads = [{
            "id": f"browser_{i}",
            "source": "browser_search",
            "source_url": f"search?q={query}",
            "name": f"Result {i+1}",
            "description": f"Search result for: {query}",
            "website": "",
            "email": "",
            "phone": "",
            "industry": "",
            "category": "",
            "score": 50,
            "status": "new",
            "notes": "",
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
        } for i in range(limit)]

        return leads

    def qualify_leads(self, leads: List[Dict]) -> List[Dict]:
        """Score and qualify leads."""
        logger.info(f"Qualifying {len(leads)} leads")

        BUSINESS_SERVICES = [
            "consulting", "marketing", "agency", "services",
            "outsourcing", "freelance", "contractor",
        ]

        qualified = []
        for lead in leads:
            score = 50  # Base score

            # Has website
            if lead.get("website"):
                score += 15

            # Has email
            if lead.get("email"):
                score += 20

            # Has phone
            if lead.get("phone"):
                score += 10

            # Check if business service
            if self.config["filters"]["exclude_business_services"]:
                name = lead.get("name", "").lower()
                description = lead.get("description", "").lower()
                if any(service in f"{name} {description}" for service in BUSINESS_SERVICES):
                    score = 0
                    lead["notes"] = "Excluded: Business service"
                    logger.debug(f"Excluded business service: {lead.get('name')}")

            # Check industry filter
            industries = self.config["filters"]["industries"]
            if industries and lead.get("industry") not in industries:
                score -= 20

            # Apply min score filter
            if score < self.config["filters"]["min_score"]:
                lead["status"] = "filtered"
                logger.debug(f"Lead filtered by score: {lead.get('name')}")
            else:
                lead["status"] = "qualified"
                lead["score"] = score
                qualified.append(lead)

        logger.info(f"Qualified {len(qualified)} leads")
        return qualified

    def enrich_leads(self, leads: List[Dict]) -> List[Dict]:
        """Enrich leads with additional information."""
        logger.info(f"Enriching {len(leads)} leads")
        logger.info("Note: Enrichment requires browser tool integration.")

        # Placeholder for enrichment
        # In production, this would:
        # 1. Visit each website using browser tool
        # 2. Extract company description
        # 3. Find email addresses
        # 4. Classify industry

        for lead in leads:
            if not lead.get("description"):
                lead["description"] = "Description not yet enriched"
            if not lead.get("industry"):
                lead["industry"] = "Unknown"

        return leads

    def save_leads(self, leads: List[Dict], output_name: str, formats: List[str]):
        """Save leads to multiple formats."""
        logger.info(f"Saving {len(leads)} leads as {output_name}")

        # Add metadata
        for lead in leads:
            lead["created_at"] = datetime.now().isoformat()
            lead["updated_at"] = datetime.now().isoformat()

        if not any(lead.get("id") for lead in leads):
            # Generate IDs
            for i, lead in enumerate(leads):
                lead["id"] = f"lead_{i+1}"

        # CSV
        if "csv" in formats:
            self._save_csv(leads, f"{output_name}.csv")

        # Excel
        if "excel" in formats or "xlsx" in formats:
            self._save_excel(leads, f"{output_name}.xlsx")

        # SQLite
        if "db" in formats:
            self._save_db(leads, f"{output_name}.db")

    def _save_csv(self, leads: List[Dict], filepath: str):
        """Save to CSV."""
        import pandas as pd
        df = pd.DataFrame(leads)
        df.to_csv(filepath, index=False)
        logger.info(f"Saved to CSV: {filepath}")

    def _save_excel(self, leads: List[Dict], filepath: str):
        """Save to Excel."""
        import pandas as pd
        df = pd.DataFrame(leads)
        df.to_excel(filepath, index=False)
        logger.info(f"Saved to Excel: {filepath}")

    def _save_db(self, leads: List[Dict], filepath: str):
        """Save to SQLite."""
        from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, DateTime
        from sqlalchemy.ext.declarative import declarative_base

        Base = declarative_base()

        class Lead(Base):
            __tablename__ = 'leads'
            id = Column(Integer, primary_key=True)
            source = Column(String)
            name = Column(String)
            description = Column(String)
            website = Column(String)
            email = Column(String)
            phone = Column(String)
            booth = Column(String)
            industry = Column(String)
            category = Column(String)
            score = Column(Integer)
            status = Column(String)
            notes = Column(String)
            created_at = Column(DateTime)
            updated_at = Column(DateTime)

        engine = create_engine(f'sqlite:///{filepath}')
        Base.metadata.create_all(engine)

        from sqlalchemy.orm import sessionmaker
        Session = sessionmaker(bind=engine)
        session = Session()

        # Clear existing data
        session.query(Lead).delete()

        # Insert leads
        for lead_data in leads:
            lead = Lead(**lead_data)
            session.add(lead)

        session.commit()
        session.close()
        logger.info(f"Saved to SQLite: {filepath}")

    def generate_outreach(self, leads: List[Dict], campaign_type: str = "intro") -> Dict[str, str]:
        """Generate outreach content for leads."""
        logger.info(f"Generating {campaign_type} outreach for {len(leads)} leads")

        sender = self.config["sender"]
        templates = {
            "intro": """
Hi {name},

I came across {company} at {source} and was impressed by your work in {industry}.

I'd love to learn more about your offerings. Are you open to a brief call this week?

Best regards,
{my_name}
{my_title}
{my_company}
Email: {my_email}
Phone: {my_phone}
""",
            "followup": """
Hi {name},

Just following up on my previous note. Would love to connect and explore how we might collaborate.

Best regards,
{my_name}
{my_title}
{my_company}
""",
        }

        outreach = {}
        template = templates.get(campaign_type, templates["intro"])

        for lead in leads:
            # Skip filtered leads
            if lead.get("status") == "filtered":
                continue

            # Personalize template
            message = template.format(
                name=lead.get("name", "there"),
                company=lead.get("name", "their company"),
                source=lead.get("source", "various sources"),
                industry=lead.get("industry", "their industry"),
                **sender
            )

            outreach[lead["id"]] = message

        logger.info(f"Generated outreach for {len(outreach)} leads")
        return outreach

    def run(self):
        """Main entry point."""
        args = self._parse_args()
        logger.info(f"Lead Generator started: {args}")

        # Load or scrape leads
        if args.source == "trade-show":
            leads = self.scrape_trade_show(args.url, args.filter_services)
        elif args.source == "browser":
            leads = self.scrape_browser_query(args.query, args.limit)
        elif args.source == "file" and args.input:
            leads = self._load_leads(args.input)
        else:
            logger.error("Invalid source. Use --source trade-show|browser|file")
            sys.exit(1)

        # Process leads
        if args.enrich:
            leads = self.enrich_leads(leads)

        if args.qualify:
            leads = self.qualify_leads(leads)

        # Save leads
        if args.output:
            formats = [fmt.lower() for fmt in (args.format or "csv,excel,db").split(",")]
            self.save_leads(leads, args.output, formats)

        # Generate outreach
        if args.campaign:
            outreach = self.generate_outreach(leads, args.campaign)

            # Save outreach
            output_dir = Path(f"{args.output}_outreach")
            output_dir.mkdir(exist_ok=True)

            for lead_id, message in outreach.items():
                file_path = output_dir / f"{lead_id}.txt"
                with open(file_path, 'w') as f:
                    f.write(message)

            logger.info(f"Saved outreach to: {output_dir}")

        logger.info(f"Lead generator complete! Processed {len(leads)} leads")

    def _parse_args(self):
        """Parse command line arguments."""
        parser = argparse.ArgumentParser(
            description="Lead Generator - Automated lead generation for trade shows, directories, and business listings"
        )

        parser.add_argument("--source", choices=["trade-show", "browser", "file"],
                            required=True, help="Data source")
        parser.add_argument("--url", help="URL for trade show scraping")
        parser.add_argument("--query", help="Query for browser scraping")
        parser.add_argument("--input", help="Input file (CSV, Excel, or DB)")
        parser.add_argument("--output", default="leads", help="Output file prefix")
        parser.add_argument("--format", default="csv,excel,db",
                           help="Output formats: csv, excel, db (comma-separated)")
        parser.add_argument("--limit", type=int, default=100, help="Limit number of results")
        parser.add_argument("--filter-services", action="store_true",
                           help="Exclude business services (consultants, agencies)")
        parser.add_argument("--enrich", action="store_true", help="Enrich leads with website data")
        parser.add_argument("--qualify", action="store_true", help="Score and qualify leads")
        parser.add_argument("--campaign", help="Generate outreach campaign (intro, followup)")

        return parser.parse_args()

    def _load_leads(self, input_file: str) -> List[Dict]:
        """Load leads from file."""
        import pandas as pd

        # Detect file type
        if input_file.endswith('.csv'):
            df = pd.read_csv(input_file)
        elif input_file.endswith('.xlsx'):
            df = pd.read_excel(input_file)
        elif input_file.endswith('.db'):
            from sqlalchemy import create_engine
            engine = create_engine(f'sqlite:///{input_file}')
            df = pd.read_sql("SELECT * FROM leads", engine)
        else:
            logger.error(f"Unsupported file type: {input_file}")
            return []

        leads = df.to_dict('records')
        logger.info(f"Loaded {len(leads)} leads from {input_file}")
        return leads


def main():
    """Main entry point."""
    generator = LeadGenerator()
    generator.run()


if __name__ == "__main__":
    main()
