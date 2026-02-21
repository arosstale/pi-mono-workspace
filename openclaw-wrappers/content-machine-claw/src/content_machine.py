#!/usr/bin/env python3
"""
Content Machine Claw — Automated content creation pipeline
"""

import asyncio
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any

from src.config import Config
from src.trend_monitor import TrendMonitor
from src.brand_voice import BrandVoiceProfile
from src.content_generator import ContentGenerator
from src.visual_creator import VisualCreator
from src.scheduler import ContentScheduler
from src.delivery import ContentDelivery

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler('content_machine.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class ContentMachineClaw:
    """Main orchestrator for content creation"""
    
    def __init__(self, config_path: str):
        self.config = Config(config_path)
        self.trend_monitor = TrendMonitor(self.config.sources)
        self.brand_voice = BrandVoiceProfile(self.config.brand_voice)
        self.content_generator = ContentGenerator(self.config.content_plan)
        self.visual_creator = VisualCreator(self.config.visuals)
        self.scheduler = ContentScheduler(self.config.scheduling)
        self.delivery = ContentDelivery(self.config.delivery)
    
    async def run(self, verbose: bool = False):
        """Run full content creation pipeline"""
        
        logger.info("=" * 70)
        logger.info("Content Machine Claw — Starting")
        logger.info("=" * 70)
        
        # Phase 1: Monitor Trends
        logger.info("\n📱 Phase 1: Monitoring Trends...")
        trends = await self._monitor_trends(verbose)
        logger.info(f"   {len(trends)} trends identified")
        
        # Phase 2: Load Brand Voice
        logger.info("\n🎭 Phase 2: Loading Brand Voice...")
        brand_voice = self._load_brand_voice(verbose)
        logger.info(f"   Style: {brand_voice.get('style', 'casual')}")
        
        # Phase 3: Generate Content
        logger.info("\n✍️ Phase 3: Generating Content...")
        content = await self._generate_content(trends, brand_voice, verbose)
        logger.info(f"   {len(content)} pieces created")
        
        # Phase 4: Create Visuals
        logger.info("\n📸 Phase 4: Creating Visuals...")
        visuals = await self._create_visuals(content, verbose)
        logger.info(f"   {len(visuals)} visual assets created")
        
        # Phase 5: Schedule
        logger.info("\n📅 Phase 5: Scheduling Content...")
        scheduled = await self._schedule_content(content, visuals, verbose)
        logger.info(f"   {len(scheduled)} items scheduled")
        
        # Phase 6: Delivery
        logger.info("\n📤 Phase 6: Sending Delivery...")
        await self._send_delivery(content, scheduled, verbose)
        logger.info("   Weekly batch sent!")
        
        # Summary
        self._print_summary(content, visuals)
        
        logger.info("\n✅ Content Machine Claw — Complete!")
        return content
    
    async def _monitor_trends(self, verbose: bool) -> List[Dict[str, Any]]:
        """Monitor trends across platforms"""
        return await self.trend_monitor.scan()
    
    def _load_brand_voice(self, verbose: bool) -> Dict[str, Any]:
        """Load brand voice profile"""
        return self.brand_voice.load()
    
    async def _generate_content(self, trends: List, voice: Dict, verbose: bool) -> List[Dict]:
        """Generate content in brand voice"""
        return await self.content_generator.generate(trends, voice)
    
    async def _create_visuals(self, content: List, verbose: bool) -> List[Dict]:
        """Create thumbnails and graphics"""
        return await self.visual_creator.create(content)
    
    async def _schedule_content(self, content: List, visuals: List, verbose: bool) -> List[Dict]:
        """Schedule content across platforms"""
        return await self.scheduler.schedule(content, visuals)
    
    async def _send_delivery(self, content: List, scheduled: List, verbose: bool):
        """Send weekly content batch"""
        message = self._format_message(content, scheduled)
        await self.delivery.send(message)
    
    def _format_message(self, content: List, scheduled: List) -> str:
        """Format delivery message"""
        timestamp = datetime.now().strftime('%A, %B %d, %Y')
        
        message = f"""📝 Content Machine Claw — Weekly Batch

📅 {timestamp}

Here's your content for next 7 days:

📱 Twitter: 14 posts (short, punchy)
📰 Newsletter: 2 editions (deep dives)
🎬 YouTube: 3 scripts (9-minute each)
📸 Instagram: 7 graphics (carousel posts)

📅 All scheduled. Review and hit publish!

💡 Trending topic this week: {content[0].get('topic', 'N/A')}
"""
        
        return message
    
    def _print_summary(self, content: List, visuals: List):
        """Print content summary"""
        print("\n" + "=" * 70)
        print("📊 WEEKLY CONTENT SUMMARY")
        print("=" * 70)
        print(f"Twitter posts: {sum(1 for c in content if c.get('platform') == 'twitter')}")
        print(f"Newsletter editions: {sum(1 for c in content if c.get('platform') == 'newsletter')}")
        print(f"YouTube scripts: {sum(1 for c in content if c.get('platform') == 'youtube')}")
        print(f"Instagram graphics: {len(visuals)}")
        print("=" * 70)


async def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Content Machine Claw')
    parser.add_argument('--config', default='config/config.json', help='Config file path')
    parser.add_argument('--verbose', action='store_true', help='Verbose output')
    
    args = parser.parse_args()
    
    content_machine = ContentMachineClaw(args.config)
    await content_machine.run(verbose=args.verbose)


if __name__ == '__main__':
    asyncio.run(main())
