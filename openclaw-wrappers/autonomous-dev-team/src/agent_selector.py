"""
Agent selector module for Autonomous Dev Team
"""

import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)


class AgentSelector:
    """Select appropriate development agent"""
    
    def __init__(self, preferences: Dict[str, Any]):
        self.preferences = preferences
        self.default_stack = preferences.get('default_stack', 'nextjs')
    
    async def select(self, requirements: Dict) -> Dict[str, Any]:
        """Select development agent based on requirements"""
        logger.info("   Selecting agent...")
        
        stack = requirements.get('stack', self.default_stack)
        
        agents = {
            'nextjs': {
                'name': 'Next.js Dashboard Agent',
                'boilerplate': 'nextjs_dashboard',
                'skills': ['react', 'typescript', 'tailwind']
            },
            'react': {
                'name': 'React App Agent',
                'boilerplate': 'react_saas',
                'skills': ['react', 'vite', 'routing']
            },
            'python': {
                'name': 'Python API Agent',
                'boilerplate': 'python_api',
                'skills': ['fastapi', 'sqlalchemy', 'pytest']
            }
        }
        
        selected = agents.get(stack, agents['nextjs'])
        return selected
