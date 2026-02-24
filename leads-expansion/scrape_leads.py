#!/usr/bin/env python3
"""
Business Leads Scraper — PagineGialle (Italian Yellow Pages)
Target: 1,500+ leads across multiple cities and sectors
"""

import sys
import time
import random
import json
from datetime import datetime
from urllib.parse import urljoin, quote
import re

# Try to import requests, fall back to urllib if not available
try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    import urllib.request
    import urllib.parse
    HAS_REQUESTS = False

def get_page(url, retries=3):
    """Fetch a page with retries and rate limiting"""
    headers = {
        'User-Agent': random.choice([
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        ])
    }

    for attempt in range(retries):
        try:
            if HAS_REQUESTS:
                response = requests.get(url, headers=headers, timeout=30)
                response.raise_for_status()
                return response.text
            else:
                req = urllib.request.Request(url, headers=headers)
                with urllib.request.urlopen(req, timeout=30) as response:
                    return response.read().decode('utf-8')
        except Exception as e:
            if attempt < retries - 1:
                wait_time = random.uniform(2, 5)
                print(f"  ⚠️  Error: {e}, retrying in {wait_time:.1f}s...")
                time.sleep(wait_time)
            else:
                print(f"  ❌ Failed after {retries} attempts: {e}")
                return None

    return None

def extract_business_info(html, city, sector):
    """Extract business information from HTML"""
    leads = []

    # This is a template - actual parsing depends on PagineGialle's HTML structure
    # Common patterns to look for:
    # - Business names in <h2>, <h3>, or specific classes
    # - Phone numbers with various formats
    # - Addresses
    # - Websites

    # Pattern for Italian phone numbers
    phone_pattern = r'[\+0-9\s\(\)\-]{8,20}'
    phones = re.findall(phone_pattern, html)

    # Pattern for addresses (basic)
    address_pattern = r'(Via|Corso|Piazza|Largo|Viale|Piazzale)\s+[^\.,]+[\d\s,]+'
    addresses = re.findall(address_pattern, html)

    # Pattern for websites
    website_pattern = r'(https?://[^\s<>"\']+)'
    websites = re.findall(website_pattern, html)

    # Extract business names (this is highly site-dependent)
    name_pattern = r'<h[1-6][^>]*>([^<]+)</h[1-6]>'
    names = re.findall(name_pattern, html)

    # Combine and deduplicate
    for i in range(min(len(names), len(phones))):
        lead = {
            'name': names[i].strip() if i < len(names) else f"{city} {sector} business {i+1}",
            'phone': phones[i].strip() if i < len(phones) else '',
            'website': websites[i] if i < len(websites) else '',
            'address': addresses[i] if i < len(addresses) else '',
            'city': city,
            'sector': sector,
            'source': 'PagineGialle',
            'discovered_at': datetime.now().isoformat(),
            'status': 'new',
            'score': 0,
            'email_sent': False,
            'responded': False,
            'priority': False
        }
        leads.append(lead)

    return leads

def scrape_sector_in_city(city, sector, pages=5):
    """Scrape multiple pages of a sector in a city"""
    all_leads = []

    print(f"\n📍 Scraping {sector} in {city}...")

    for page in range(1, pages + 1):
        print(f"  📄 Page {page}/{pages}...")

        # Construct URL (template for PagineGialle)
        url = f"{BASE_URL}/{quote(city)}/{quote(sector)}/p-{page}"
        print(f"    URL: {url}")

        html = get_page(url)
        if html:
            leads = extract_business_info(html, city, sector)
            all_leads.extend(leads)
            print(f"    ✅ Found {len(leads)} leads")
        else:
            print(f"    ❌ Failed to fetch page")

        # Rate limiting
        time.sleep(random.uniform(3, 6))

    return all_leads

def save_leads(leads, filename):
    """Save leads to JSON file"""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(leads, f, ensure_ascii=False, indent=2)
    print(f"\n💾 Saved {len(leads)} leads to {filename}")

def main():
    """Main execution"""
    if len(sys.argv) < 3:
        print("Usage: python3 scrape_leads.py <city> <sector> [pages]")
        sys.exit(1)

    city = sys.argv[1]
    sector = sys.argv[2]
    pages = int(sys.argv[3]) if len(sys.argv) > 3 else 5

    print(f"🚀 Starting scrape: {sector} in {city}")
    print(f"📊 Pages: {pages}")
    print(f"📅 Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

    leads = scrape_sector_in_city(city, sector, pages)

    # Save to file
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"{OUTPUT_DIR}/leads_{city}_{sector}_{timestamp}.json"
    save_leads(leads, filename)

    print("\n✅ SCRAPE COMPLETE!")
    print(f"📊 Total leads: {len(leads)}")
    print(f"📅 Finished: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == '__main__':
    main()

