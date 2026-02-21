#!/usr/bin/env python3
"""
Autonomous Dev Team — Multi-agent build pipeline
"""

import asyncio
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any
import subprocess

from src.config import Config
from src.requirement_parser import RequirementParser
from src.agent_selector import AgentSelector
from src.boilerplate_manager import BoilerplateManager
from src.builder import Builder
from src.tester import Tester
from src.deployer import Deployer
from src.self_healer import SelfHealer
from src.delivery import DevDelivery

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler('dev_team.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class AutonomousDevTeam:
    """Main orchestrator for autonomous development"""
    
    def __init__(self, config_path: str):
        self.config = Config(config_path)
        self.parser = RequirementParser()
        self.agent_selector = AgentSelector(self.config.preferences)
        self.boilerplate = BoilerplateManager(self.config.boilerplates)
        self.builder = Builder(self.config.testing)
        self.tester = Tester(self.config.testing)
        self.deployer = Deployer(self.config.deployment)
        self.healer = SelfHealer()
        self.delivery = DevDelivery(self.config.delivery)
    
    async def build_project(self, project_description: str, verbose: bool = False):
        """Build project from idea to deployed product"""
        
        logger.info("=" * 70)
        logger.info("Autonomous Dev Team — Starting")
        logger.info("=" * 70)
        
        # Phase 1: Parse Requirements
        logger.info("\n📝 Phase 1: Parsing Requirements...")
        requirements = await self._parse_requirements(project_description, verbose)
        logger.info(f"   {len(requirements.get('features', []))} features identified")
        
        # Phase 2: Select Sub-Agent
        logger.info("\n🤖 Phase 2: Selecting Sub-Agent...")
        selected_agent = await self._select_agent(requirements, verbose)
        logger.info(f"   Agent: {selected_agent['name']}")
        
        # Phase 3: Pull Boilerplate
        logger.info("\n📂 Phase 3: Pulling Boilerplate...")
        boilerplate = await self._get_boilerplate(selected_agent, verbose)
        logger.info(f"   Boilerplate: {boilerplate['name']}")
        
        # Phase 4: Build Features
        logger.info("\n🔨 Phase 4: Building Features...")
        build_result = await self._build_features(requirements, boilerplate, verbose)
        logger.info(f"   Features built: {build_result.get('features_count', 0)}")
        
        # Phase 5: Run Tests
        logger.info("\n✅ Phase 5: Running Tests...")
        test_results = await self._run_tests(build_result, verbose)
        logger.info(f"   Tests: {test_results.get('passed', 0)}/{test_results.get('total', 0)} passed")
        
        # Phase 6: Deploy
        logger.info("\n🚀 Phase 6: Deploying...")
        deploy_result = await self._deploy(build_result, verbose)
        logger.info(f"   Deployed: {deploy_result.get('url', 'unknown')}")
        
        # Phase 7: Send Notification
        logger.info("\n📤 Phase 7: Sending Notification...")
        await self._notify_completion(deploy_result, verbose)
        
        # Summary
        self._print_summary(deploy_result)
        
        logger.info("\n✅ Autonomous Dev Team — Complete!")
        return deploy_result
    
    async def _parse_requirements(self, description: str, verbose: bool) -> Dict[str, Any]:
        """Parse plain English project description"""
        return await self.parser.parse(description)
    
    async def _select_agent(self, requirements: Dict, verbose: bool) -> Dict[str, Any]:
        """Select appropriate development agent"""
        return await self.agent_selector.select(requirements)
    
    async def _get_boilerplate(self, agent: Dict, verbose: bool) -> Dict[str, Any]:
        """Pull and prepare boilerplate"""
        return await self.boilerplate.get(agent['boilerplate'])
    
    async def _build_features(self, requirements: Dict, boilerplate: Dict, verbose: bool) -> Dict[str, Any]:
        """Implement features"""
        return await self.builder.build(requirements, boilerplate)
    
    async def _run_tests(self, build_result: Dict, verbose: bool) -> Dict[str, Any]:
        """Run automated tests"""
        return await self.tester.run(build_result)
    
    async def _deploy(self, build_result: Dict, verbose: bool) -> Dict[str, Any]:
        """Deploy to production"""
        return await self.deployer.deploy(build_result)
    
    async def _notify_completion(self, deploy_result: Dict, verbose: bool):
        """Send live URL notification"""
        message = self._format_message(deploy_result)
        await self.delivery.send(message)
    
    def _format_message(self, deploy_result: Dict) -> str:
        """Format deployment notification"""
        url = deploy_result.get('url', 'Deploying...')
        return f"""🚀 Your Project is Live!

URL: {url}
Build time: {deploy_result.get('build_time', 'N/A')}
Deployed: {deploy_result.get('deployed_at', 'N/A')}
"""
    
    def _print_summary(self, deploy_result: Dict):
        """Print build summary"""
        print("\n" + "=" * 70)
        print("🎉 DEPLOYMENT SUMMARY")
        print("=" * 70)
        print(f"URL: {deploy_result.get('url', 'unknown')}")
        print(f"Features: {deploy_result.get('features_count', 0)}")
        print(f"Tests: {deploy_result.get('tests_passed', 0)}/{deploy_result.get('tests_total', 0)}")
        print(f"Deployed at: {deploy_result.get('deployed_at', 'N/A')}")
        print("=" * 70)


async def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Autonomous Dev Team')
    parser.add_argument('--project', required=True, help='Project description (plain English)')
    parser.add_argument('--config', default='config/config.json', help='Config file path')
    parser.add_argument('--verbose', action='store_true', help='Verbose output')
    
    args = parser.parse_args()
    
    dev_team = AutonomousDevTeam(args.config)
    await dev_team.build_project(args.project, verbose=args.verbose)


if __name__ == '__main__':
    asyncio.run(main())
