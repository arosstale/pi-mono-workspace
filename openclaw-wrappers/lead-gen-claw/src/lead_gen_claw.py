#!/usr/bin/env python3
"""
Lead Generation Claw — Automated lead generation system
"""

import asyncio
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any
import pandas as pd

from src.scrapers import ScraperFactory
from src.enrichment import LeadEnricher
from src.qualification import LeadQualifier
from src.export import LeadExporter
from src.delivery import LeadDelivery
from src.config import Config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler('lead_gen_claw.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class LeadGenerationClaw:
    """Main orchestrator for lead generation pipeline"""
    
    def __init__(self, config_path: str):
        self.config = Config(config_path)
        self.scraper_factory = ScraperFactory()
        self.enricher = LeadEnricher()
        self.qualifier = LeadQualifier(self.config.qualification)
        self.exporter = LeadExporter()
        self.delivery = LeadDelivery(self.config.delivery)
    
    async def run(self, verbose: bool = False):
        """Run the full lead generation pipeline"""
        
        logger.info("=" * 60)
        logger.info("Lead Generation Claw — Starting")
        logger.info("=" * 60)
        
        # Phase 1: Scrape
        logger.info("\n📥 Phase 1: Scraping sources...")
        all_leads = await self._scrape_sources(verbose)
        logger.info(f"   Total leads scraped: {len(all_leads)}")
        
        # Phase 2: Enrich
        logger.info("\n🔍 Phase 2: Enriching leads...")
        enriched_leads = await self._enrich_leads(all_leads, verbose)
        logger.info(f"   Leads enriched: {len(enriched_leads)}")
        
        # Phase 3: Qualify
        logger.info("\n📊 Phase 3: Qualifying leads...")
        qualified_leads = self._qualify_leads(enriched_leads)
        logger.info(f"   Qualified leads: {len(qualified_leads)}")
        logger.info(f"   Qualified rate: {len(qualified_leads)/len(all_leads)*100:.1f}%")
        
        # Phase 4: Export
        logger.info("\n💾 Phase 4: Exporting leads...")
        export_paths = self._export_leads(qualified_leads)
        for path in export_paths:
            logger.info(f"   Exported: {path}")
        
        # Phase 5: Deliver
        logger.info("\n📤 Phase 5: Delivering batch...")
        await self._deliver_batch(qualified_leads, export_paths)
        logger.info("   Daily batch sent!")
        
        # Summary
        self._print_summary(qualified_leads)
        
        logger.info("\n✅ Lead Generation Claw — Complete!")
        return qualified_leads
    
    async def _scrape_sources(self, verbose: bool) -> List[Dict[str, Any]]:
        """Scrape all configured sources"""
        all_leads = []
        
        for source in self.config.sources:
            if not source.get('enabled', True):
                logger.info(f"   Skipping disabled source: {source['name']}")
                continue
            
            logger.info(f"\n   Scraping: {source['name']}")
            scraper = self.scraper_factory.create(source['platform'])
            
            try:
                leads = await scraper.scrape(source)
                all_leads.extend(leads)
                logger.info(f"   ✓ {source['name']}: {len(leads)} leads")
            except Exception as e:
                logger.error(f"   ✗ {source['name']}: {e}")
        
        return all_leads
    
    async def _enrich_leads(self, leads: List[Dict], verbose: bool) -> List[Dict]:
        """Enrich all leads with additional data"""
        enrichment_tasks = []
        
        if self.config.enrichment.get('verify_websites'):
            enrichment_tasks.append(self.enricher.verify_websites(leads))
        
        if self.config.enrichment.get('validate_emails'):
            enrichment_tasks.append(self.enricher.validate_emails(leads))
        
        if self.config.enrichment.get('classify_industry'):
            enrichment_tasks.append(self.enricher.classify_industry(leads))
        
        if self.config.enrichment.get('find_social_media'):
            enrichment_tasks.append(self.enricher.find_social_media(leads))
        
        # Run all enrichment tasks in parallel
        await asyncio.gather(*enrichment_tasks)
        
        return leads
    
    def _qualify_leads(self, leads: List[Dict]) -> List[Dict]:
        """Score and filter leads based on criteria"""
        qualified = []
        
        for lead in leads:
            score = self.qualifier.score(lead)
            lead['qualification_score'] = score
            
            if score >= self.config.qualification.get('min_score', 50):
                qualified.append(lead)
        
        return qualified
    
    def _export_leads(self, leads: List[Dict]) -> List[str]:
        """Export leads to configured formats"""
        formats = self.config.delivery.get('formats', ['csv'])
        export_paths = []
        timestamp = datetime.now().strftime('%Y-%m-%d')
        
        for fmt in formats:
            path = self.exporter.export(leads, fmt, timestamp)
            export_paths.append(path)
        
        return export_paths
    
    async def _deliver_batch(self, leads: List[Dict], export_paths: List[str]):
        """Send batch to configured channel"""
        message = self._format_message(leads, export_paths)
        await self.delivery.send(message, export_paths)
    
    def _format_message(self, leads: List[Dict], export_paths: List[str]) -> str:
        """Format delivery message"""
        timestamp = datetime.now().strftime('%A, %B %d, %Y')
        
        message = f"""📊 Lead Generation Claw — Daily Batch

📅 {timestamp}

Sources scraped:
• Total leads: {len(leads)}
• Qualified (50+ score): {len(leads)}

📈 Top qualified (score 90+):
"""

        # Top 5 leads
        top_leads = sorted(leads, key=lambda x: x.get('qualification_score', 0), reverse=True)[:5]
        for i, lead in enumerate(top_leads, 1):
            status = "✓" if lead.get('email_valid', False) else "⚠"
            message += f"{i}. {lead.get('company_name', 'Unknown')} — Score: {lead.get('qualification_score', 0)} — Email: {status}\n"
        
        message += "\n📥 Download links:\n"
        for path in export_paths:
            filename = Path(path).name
            message += f"• {filename}\n"
        
        message += "\n💡 Tip: Contact high-score leads first!"
        
        return message
    
    def _print_summary(self, leads: List[Dict]):
        """Print summary statistics"""
        print("\n" + "=" * 60)
        print("📊 SUMMARY")
        print("=" * 60)
        print(f"Total qualified leads: {len(leads)}")
        
        if leads:
            avg_score = sum(l.get('qualification_score', 0) for l in leads) / len(leads)
            print(f"Average qualification score: {avg_score:.1f}")
            
            score_distribution = {
                '90+': len([l for l in leads if l.get('qualification_score', 0) >= 90]),
                '70-89': len([l for l in leads if 70 <= l.get('qualification_score', 0) < 90]),
                '50-69': len([l for l in leads if 50 <= l.get('qualification_score', 0) < 70]),
            }
            
            print("\nScore distribution:")
            for range_str, count in score_distribution.items():
                print(f"  {range_str}: {count}")
        
        print("=" * 60)


async def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Lead Generation Claw')
    parser.add_argument('--config', default='config/config.json', help='Config file path')
    parser.add_argument('--verbose', action='store_true', help='Verbose output')
    
    args = parser.parse_args()
    
    claw = LeadGenerationClaw(args.config)
    await claw.run(verbose=args.verbose)


if __name__ == '__main__':
    asyncio.run(main())
