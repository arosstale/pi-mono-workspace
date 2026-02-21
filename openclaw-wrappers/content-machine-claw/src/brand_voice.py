"""
Brand voice profile module for Content Machine
"""

import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)


class BrandVoiceProfile:
    """Manage brand voice configuration"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
    
    def load(self) -> Dict[str, Any]:
        """Load brand voice profile"""
        logger.info("   Loading brand voice...")
        return self.config
