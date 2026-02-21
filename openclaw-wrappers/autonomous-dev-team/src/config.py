"""
Configuration management for Autonomous Dev Team
"""

import json
from pathlib import Path
from typing import Dict, Any


class Config:
    """Load and validate dev team configuration"""
    
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
        required_keys = ['preferences', 'boilerplates', 'testing', 'deployment', 'delivery']
        for key in required_keys:
            if key not in self._data:
                raise ValueError(f"Missing required config key: {key}")
    
    @property
    def preferences(self) -> Dict[str, Any]:
        """Get development preferences"""
        return self._data.get('preferences', {})
    
    @property
    def boilerplates(self) -> Dict[str, Any]:
        """Get boilerplate configuration"""
        return self._data.get('boilerplates', {})
    
    @property
    def testing(self) -> Dict[str, Any]:
        """Get testing configuration"""
        return self._data.get('testing', {})
    
    @property
    def deployment(self) -> Dict[str, Any]:
        """Get deployment configuration"""
        return self._data.get('deployment', {})
    
    @property
    def delivery(self) -> Dict[str, Any]:
        """Get delivery configuration"""
        return self._data.get('delivery', {})
