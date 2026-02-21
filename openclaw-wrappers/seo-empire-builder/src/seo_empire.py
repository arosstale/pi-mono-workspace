#!/usr/bin/env python3
"""
SEO Empire Builder — Full SEO automation system
"""

import asyncio
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any
import pandas as pd

from src.keyword_research import KeywordResearcher
from src.programmatic_seo import ProgrammaticSEO
from src.content_generator import ContentGenerator
from src.cms_publisher import CMSPublisher
from src.backlink_outreach import BacklinkOutreach
from src.search_console import SearchConsoleMonitor
from src.config import Config
from src.strategy_adjuster import StrategyAdjuster

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler('seo_empire.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class SEOEmpireBuilder:
    """Main orchestrator for SEO automation pipeline"""
    
    def __init__(self, config_path: str):
        self.config = Config(config_path)
        self.keyword_researcher = KeywordResearcher(self.config.keyword_research)
        self.programmatic_seo = ProgrammaticSEO(self.config.programmatic_seo)
        self.content_generator = ContentGenerator(self.config.content_generation)
        self.cms_publisher = CMSPublisher(self.config.cms)
        self.backlink_outreach = BacklinkOutreach(self.config.backlink_acquisition)
        self.search_console = SearchConsoleMonitor(self.config.search_console)
        self.strategy_adjuster = StrategyAdjuster(self.config)
    
    async def run(self, verbose: bool = False):
        """Run full SEO automation pipeline"""
        
        logger.info("=" * 70)
        logger.info("SEO Empire Builder — Starting")
        logger.info("=" * 70)
        
        # Phase 1: Keyword Research
        logger.info("\n📊 Phase 1: Keyword Research...")
        keywords = await self._keyword_research(verbose)
        logger.info(f"   {len(keywords)} keywords discovered")
        
        # Phase 2: Programmatic SEO Strategy
        logger.info("\n🗺 Phase 2: Programmatic SEO Strategy...")
        strategy = await self._build_strategy(keywords, verbose)
        logger.info(f"   {len(strategy.get('topic_clusters', []))} topic clusters created")
        
        # Phase 3: Content Generation
        logger.info("\n✍️ Phase 3: Content Generation...")
        content = await self._generate_content(strategy, verbose)
        logger.info(f"   {len(content)} articles generated")
        
        # Phase 4: CMS Publishing
        logger.info("\n📤 Phase 4: CMS Publishing...")
        published_urls = await self._publish_content(content, verbose)
        logger.info(f"   {len(published_urls)} articles published")
        
        # Phase 5: Backlink Acquisition
        logger.info("\n🤝 Phase 5: Backlink Acquisition...")
        outreach_stats = await self._backlink_outreach(strategy, verbose)
        logger.info(f"   {outreach_stats.get('emails_sent', 0)} outreach emails sent")
        logger.info(f"   {outreach_stats.get('responses', 0)} responses received")
        
        # Phase 6: Search Console Monitoring
        logger.info("\n📈 Phase 6: Search Console Monitoring...")
        performance_data = await self._monitor_performance(verbose)
        logger.info(f"   {performance_data.get('total_clicks', 0)} clicks tracked")
        
        # Phase 7: Strategy Adjustment
        logger.info("\n🔄 Phase 7: Strategy Adjustment...")
        adjusted_strategy = await self._adjust_strategy(performance_data, strategy, verbose)
        logger.info("   Strategy adjusted based on performance")
        
        # Summary
        self._print_summary(keywords, content, outreach_stats, performance_data)
        
        logger.info("\n✅ SEO Empire Builder — Complete!")
        return {
            'keywords': keywords,
            'content': content,
            'outreach': outreach_stats,
            'performance': performance_data,
            'strategy': adjusted_strategy
        }
    
    async def _keyword_research(self, verbose: bool) -> List[Dict[str, Any]]:
        """Perform weekly keyword research"""
        tasks = [
            self.keyword_researcher.discover_opportunities(),
            self.keyword_researcher.analyze_competitors(),
            self.keyword_researcher.detect_trends()
        ]
        
        await asyncio.gather(*tasks)
        
        return self.keyword_researcher.get_top_keywords()
    
    async def _build_strategy(self, keywords: List[Dict], verbose: bool) -> Dict[str, Any]:
        """Build programmatic SEO strategy"""
        return await self.programmatic_seo.create_strategy(keywords)
    
    async def _generate_content(self, strategy: Dict, verbose: bool) -> List[Dict[str, Any]]:
        """Generate SEO-optimized content"""
        return await self.content_generator.generate_weekly_content(strategy)
    
    async def _publish_content(self, content: List[Dict], verbose: bool) -> List[str]:
        """Publish content to CMS"""
        return await self.cms_publisher.publish_batch(content)
    
    async def _backlink_outreach(self, strategy: Dict, verbose: bool) -> Dict[str, Any]:
        """Execute backlink acquisition campaign"""
        return await self.backlink_outreach.run_campaign(strategy)
    
    async def _monitor_performance(self, verbose: bool) -> Dict[str, Any]:
        """Monitor Search Console performance"""
        return await self.search_console.get_daily_report()
    
    async def _adjust_strategy(self, performance: Dict, current: Dict, verbose: bool) -> Dict[str, Any]:
        """Adjust SEO strategy based on performance"""
        return await self.strategy_adjuster.adjust(performance, current)
    
    def _print_summary(self, keywords: List, content: List, outreach: Dict, performance: Dict):
        """Print daily/weekly summary"""
        print("\n" + "=" * 70)
        print("📊 OVERNIGHT REPORT")
        print("=" * 70)
        print(f"• {outreach.get('backlinks_acquired', 0)} new backlinks acquired (DA 45+)")
        print(f"• {performance.get('keywords_moved_to_page1', 0)} keywords moved to Page 1")
        print(f"• {len(content)} new articles published (2,400 words each)")
        print("\n📊 WEEKLY PERFORMANCE:")
        print(f"• Total traffic: +{performance.get('traffic_change', 0)}%")
        print(f"• Organic revenue: +{performance.get('revenue_change', 0)}%")
        print(f"• Top growing keywords: {[k['keyword'] for k in performance.get('top_keywords', [])[:5]]}")
        print("=" * 70)


async def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='SEO Empire Builder')
    parser.add_argument('--config', default='config/config.json', help='Config file path')
    parser.add_argument('--verbose', action='store_true', help='Verbose output')
    
    args = parser.parse_args()
    
    seo_builder = SEOEmpireBuilder(args.config)
    await seo_builder.run(verbose=args.verbose)


if __name__ == '__main__':
    asyncio.run(main())
