"""
Configuration management for SEO Empire Builder
"""

import json
from pathlib import Path
from typing import Dict, Any


class Config:
    """Load and validate SEO configuration"""
    
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
        required_keys = [
            'keyword_research', 'programmatic_seo', 'content_generation',
            'cms', 'backlink_acquisition', 'search_console', 'delivery'
        ]
        for key in required_keys:
            if key not in self._data:
                raise ValueError(f"Missing required config key: {key}")
    
    @property
    def keyword_research(self) -> Dict[str, Any]:
        """Get keyword research configuration"""
        return self._data.get('keyword_research', {})
    
    @property
    def programmatic_seo(self) -> Dict[str, Any]:
        """Get programmatic SEO configuration"""
        return self._data.get('programmatic_seo', {})
    
    @property
    def content_generation(self) -> Dict[str, Any]:
        """Get content generation configuration"""
        return self._data.get('content_generation', {})
    
    @property
    def cms(self) -> Dict[str, Any]:
        """Get CMS configuration"""
        return self._data.get('cms', {})
    
    @property
    def backlink_acquisition(self) -> Dict[str, Any]:
        """Get backlink acquisition configuration"""
        return self._data.get('backlink_acquisition', {})
    
    @property
    def search_console(self) -> Dict[str, Any]:
        """Get Search Console configuration"""
        return self._data.get('search_console', {})
    
    @property
    def delivery(self) -> Dict[str, Any]:
        """Get delivery configuration"""
        return self._data.get('delivery', {})
