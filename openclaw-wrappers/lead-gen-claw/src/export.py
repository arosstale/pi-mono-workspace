"""
Export leads to CSV, Excel, SQLite
"""

import logging
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any
import pandas as pd

logger = logging.getLogger(__name__)


class LeadExporter:
    """Export leads to multiple formats"""
    
    def __init__(self, output_dir: str = 'output'):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
    
    def export(self, leads: List[Dict], format_type: str, timestamp: str) -> str:
        """Export leads to specified format"""
        if not leads:
            logger.warning("No leads to export")
            return None
        
        df = pd.DataFrame(leads)
        
        # Reorder columns
        columns_order = [
            'company_name', 'email', 'website', 'booth', 'description',
            'industry', 'subindustry', 'company_size', 'region',
            'linkedin', 'twitter', 'instagram',
            'website_valid', 'email_valid', 'email_deliverable',
            'qualification_score', 'source'
        ]
        
        # Only include columns that exist
        existing_columns = [col for col in columns_order if col in df.columns]
        df = df[existing_columns]
        
        # Sort by qualification score
        df = df.sort_values('qualification_score', ascending=False)
        
        if format_type == 'csv':
            return self._export_csv(df, timestamp)
        elif format_type == 'excel':
            return self._export_excel(df, timestamp)
        elif format_type == 'sqlite':
            return self._export_sqlite(df, timestamp)
        else:
            raise ValueError(f"Unsupported format: {format_type}")
    
    def _export_csv(self, df: pd.DataFrame, timestamp: str) -> str:
        """Export to CSV"""
        filename = self.output_dir / f"leads_{timestamp}.csv"
        df.to_csv(filename, index=False, encoding='utf-8')
        logger.info(f"   Exported CSV: {filename}")
        return str(filename)
    
    def _export_excel(self, df: pd.DataFrame, timestamp: str) -> str:
        """Export to Excel"""
        filename = self.output_dir / f"leads_{timestamp}.xlsx"
        df.to_excel(filename, index=False, engine='openpyxl')
        logger.info(f"   Exported Excel: {filename}")
        return str(filename)
    
    def _export_sqlite(self, df: pd.DataFrame, timestamp: str) -> str:
        """Export to SQLite"""
        filename = self.output_dir / f"leads_{timestamp}.db"
        
        import sqlite3
        conn = sqlite3.connect(filename)
        df.to_sql('leads', conn, if_exists='replace', index=False)
        conn.close()
        
        logger.info(f"   Exported SQLite: {filename}")
        return str(filename)
