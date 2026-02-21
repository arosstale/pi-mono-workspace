"""
Configuration management for Content Machine
"""

import json
from pathlib import Path
from typing import Dict, Any


class Config:
    """Load and validate content machine configuration"""
    
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
        required_keys = ['brand_voice', 'sources', 'content_plan', 'visuals', 'scheduling', 'delivery']
        for key in required_keys:
            if key not in self._data:
                raise ValueError(f"Missing required config key: {key}")
    
    @property
    def brand_voice(self) -> Dict[str, Any]:
        """Get brand voice configuration"""
        return self._data.get('brand_voice', {})
    
    @property
    def sources(self) -> Dict[str, Any]:
        """Get trend sources configuration"""
        return self._data.get('sources', [])
    
    @property
    def content_plan(self) -> Dict[str, Any]:
        """Get content plan configuration"""
        return self._data.get('content_plan', {})
    
    @property
    def visuals(self) -> Dict[str, Any]:
        """Get visual creation configuration"""
        return self._data.get('visuals', {})
    
    @property
    def scheduling(self) -> Dict[str, Any]:
        """Get scheduling configuration"""
        return self._data.get('scheduling', {})
    
    @property
    def delivery(self) -> Dict[str, Any]:
        """Get delivery configuration"""
        return self._data.get('delivery', {})
