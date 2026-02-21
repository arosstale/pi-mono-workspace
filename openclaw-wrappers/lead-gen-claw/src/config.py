"""
Configuration management for Lead Generation Claw
"""

import json
from pathlib import Path
from typing import List, Dict, Any


class Config:
    """Load and validate configuration"""
    
    def __init__(self, config_path: str):
        self.path = Path(config_path)
        self._data = self._load()
        self._validate()
    
    def _load(self) -> Dict[str, Any]:
        """Load configuration from JSON file"""
        if not self.path.exists():
            raise FileNotFoundError(f"Config file not found: {self.path}")
        
        with open(self.path, 'r') as f:
            return json.load(f)
    
    def _validate(self):
        """Validate required configuration keys"""
        required_keys = ['sources', 'enrichment', 'qualification', 'delivery']
        for key in required_keys:
            if key not in self._data:
                raise ValueError(f"Missing required config key: {key}")
    
    @property
    def sources(self) -> List[Dict[str, Any]]:
        """Get scraping sources configuration"""
        return self._data.get('sources', [])
    
    @property
    def enrichment(self) -> Dict[str, Any]:
        """Get enrichment configuration"""
        return self._data.get('enrichment', {})
    
    @property
    def qualification(self) -> Dict[str, Any]:
        """Get qualification configuration"""
        return self._data.get('qualification', {})
    
    @property
    def delivery(self) -> Dict[str, Any]:
        """Get delivery configuration"""
        return self._data.get('delivery', {})
