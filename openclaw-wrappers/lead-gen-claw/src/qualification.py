"""
Lead qualification: score leads 0-100 based on criteria
"""

import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)


class LeadQualifier:
    """Score and qualify leads"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.min_score = config.get('min_score', 50)
        self.criteria = config.get('criteria', {})
    
    def score(self, lead: Dict[str, Any]) -> int:
        """Calculate qualification score (0-100)"""
        score = 0
        
        # Website validity (20 points)
        if lead.get('website_valid', False):
            score += 20
        elif lead.get('website_status_code') == 404:
            score -= 10
        
        # Email deliverability (25 points)
        if lead.get('email_valid', False):
            score += 10
        if lead.get('email_deliverable', False):
            score += 15
        elif lead.get('email_deliverable') is False:
            score -= 10
        
        # Company size (20 points)
        company_size = lead.get('company_size', 'unknown').lower()
        size_scores = {
            'large': 20,
            'medium': 15,
            'small': 10,
            'unknown': 5
        }
        score += size_scores.get(company_size, 5)
        
        # Industry relevance (20 points)
        target_industries = self.criteria.get('industries', [])
        lead_industry = lead.get('industry', '').lower()
        if any(target.lower() in lead_industry for target in target_industries):
            score += 20
        elif 'unknown' in lead_industry or not lead_industry:
            score += 5
        
        # Social media presence (10 points)
        if lead.get('linkedin'):
            score += 5
        if lead.get('twitter') or lead.get('instagram'):
            score += 5
        
        # Geographic fit (5 points)
        target_regions = self.criteria.get('regions', [])
        lead_region = lead.get('region', '').lower()
        if any(target.lower() in lead_region for target in target_regions):
            score += 5
        elif 'unknown' in lead_region or not lead_region:
            score += 2
        
        # Bonus: booth info (10 points)
        if lead.get('booth'):
            score += 10
        
        # Clamp to 0-100
        score = max(0, min(100, score))
        
        logger.debug(f"Scored {lead.get('company_name', 'Unknown')}: {score}")
        
        return score
