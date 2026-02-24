"""
SmallWorldLabs Exhibitor Scraper
Used for: Expo West, SEMICON, various Informa events
Strategy: AJAX POST pagination with token rotation
"""

import requests
import re
import json
from urllib.parse import unquote
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
import time
import pandas as pd


class SmallWorldLabsScraper:
    """Scrape exhibitors from SmallWorldLabs-based trade show sites"""

    def __init__(self, base_url: str, output_name: str):
        self.base_url = base_url
        self.output_name = output_name
        self.session = requests.Session()
        self.exhibitors: List[Dict] = []

        # Pagination params
        self.limit = 50
        self.total = 0
        self.tk = ""
        self.tm = ""

    def get_session_tokens(self):
        """Get session cookie and CSRF tokens from initial page"""
        print(f"🔍 Getting session tokens from {self.base_url}/exhibitors...")
        resp = self.session.get(f"{self.base_url}/exhibitors")

        # Extract CSRF tokens from inline JS
        tk_match = re.search(r'tk\s*=\s*["\']([^"\']{10,})["\']', resp.text)
        tm_match = re.search(r'tm\s*=\s*["\']([^"\']{10,})["\']', resp.text)

        if tk_match and tm_match:
            self.tk = tk_match.group(1)
            self.tm = tm_match.group(1)
            print(f"✅ Got tokens: tk={self.tk[:10]}..., tm={self.tm[:10]}...")
        else:
            raise ValueError("Could not find CSRF tokens in page")

    def scrape_page(self, offset: int) -> Optional[List[Dict]]:
        """Scrape one page of exhibitors"""
        data = {
            "limit": self.limit,
            "offset": offset,
            "module": "organizations_organization_list",
            "site_page_id": "3000",
            "method": "paginationHandler",
            "template": "generic_items",
            "mCell": "0",
            "mId": "1",
            "page_id": "openAjax",
            "ajaxType": "paginate",
            "tk": self.tk,
            "tm": self.tm,
        }

        print(f"📄 Fetching page {offset//self.limit + 1} (offset={offset})...")
        resp = self.session.post(f"{self.base_url}/index.php", data=data)

        if resp.status_code != 200:
            print(f"❌ Failed: {resp.status_code}")
            return None

        result = resp.json()

        # Rotate tokens for next request
        self.tk = result.get("formToken", self.tk)
        self.tm = result.get("formTime", self.tm)

        if "total" in result:
            self.total = result["total"]

        # Parse URL-encoded HTML
        html = unquote(result.get("data", ""))
        soup = BeautifulSoup(html, "lxml")

        exhibitors = []
        for row in soup.find_all("tr"):
            link = row.find("a", href=re.compile(r"^/co/"))
            if link:
                name = link.get_text(strip=True)
                profile_url = f"{self.base_url}{link['href']}"
                exhibitors.append({
                    "name": name,
                    "profile_url": profile_url,
                })

        return exhibitors

    def scrape_all(self):
        """Scrape all exhibitors"""
        self.get_session_tokens()

        print(f"📊 Total exhibitors: {self.total}")
        print(f"📄 Pages to scrape: {(self.total // self.limit) + 1}")

        for offset in range(0, self.total, self.limit):
            exhibitors = self.scrape_page(offset)
            if exhibitors:
                self.exhibitors.extend(exhibitors)
                print(f"  ✅ Found {len(exhibitors)} exhibitors")
            else:
                print(f"  ⚠️ No exhibitors found on page")
                break

            time.sleep(1)  # Rate limiting

        print(f"🎉 Total exhibitors scraped: {len(self.exhibitors)}")

    def to_dataframe(self) -> pd.DataFrame:
        """Convert to pandas DataFrame"""
        return pd.DataFrame(self.exhibitors)


def main():
    """Main runner"""
    # Example: Expo West 2026
    BASE_URL = "https://www.expowest.com"
    OUTPUT_NAME = "expo_west_2026"

    scraper = SmallWorldLabsScraper(BASE_URL, OUTPUT_NAME)
    scraper.scrape_all()

    # Save results
    df = scraper.to_dataframe()

    # Filter out business services
    from utils import filter_business_services, save_to_csv, save_to_excel

    df_filtered = filter_business_services(df)

    save_to_csv(df_filtered, f"{OUTPUT_NAME}.csv")
    save_to_excel(df_filtered, f"{OUTPUT_NAME}.xlsx")


if __name__ == "__main__":
    main()
