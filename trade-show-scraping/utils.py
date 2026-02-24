"""
Shared utilities for trade show scraping
"""

import pandas as pd
import json
import os
from typing import List, Dict, Optional
from pathlib import Path


BUSINESS_SERVICES_KEYWORDS = [
    "business services", "consulting", "financial services", "insurance",
    "legal services", "marketing services", "advertising services",
    "logistics", "packaging services", "printing services",
    "trade show services", "association", "media", "publication",
    "software", "technology services",
]


def is_business_services(categories: Optional[str]) -> bool:
    """Check if categories indicate business services (not product companies)"""
    if not categories:
        return False

    cats_lower = categories.lower()
    return any(kw in cats_lower for kw in BUSINESS_SERVICES_KEYWORDS)


def save_to_csv(df: pd.DataFrame, filename: str, output_dir: str = "output") -> None:
    """Save DataFrame to CSV"""
    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, filename)
    df.to_csv(path, index=False)
    print(f"✅ Saved to {path}")


def save_to_excel(df: pd.DataFrame, filename: str, output_dir: str = "output") -> None:
    """Save DataFrame to Excel"""
    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, filename)
    df.to_excel(path, index=False, engine="openpyxl")
    print(f"✅ Saved to {path}")


def filter_business_services(df: pd.DataFrame, categories_col: str = "categories") -> pd.DataFrame:
    """Filter out business service providers from exhibitors"""
    if categories_col not in df.columns:
        print(f"⚠️ Column '{categories_col}' not found - skipping filter")
        return df

    mask = df[categories_col].apply(is_business_services)
    products = df[~mask]
    services = df[mask]

    print(f"📊 Filter results:")
    print(f"  Product companies: {len(products)}")
    print(f"  Business services: {len(services)}")

    return products


def load_env() -> Dict[str, str]:
    """Load .env file"""
    env_file = Path(__file__).parent / ".env"
    if env_file.exists():
        from dotenv import load_dotenv
        load_dotenv(env_file)
        return dict(os.environ)
    return {}


def validate_url(url: str) -> bool:
    """Basic URL validation"""
    return url.startswith(("http://", "https://"))


def clean_text(text: str) -> str:
    """Clean text from HTML and extra whitespace"""
    if not text:
        return ""
    import re
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    return text
