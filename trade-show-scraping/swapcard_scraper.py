"""
Swapcard/Next.js GraphQL Exhibitor Scraper
Used for: Winter FancyFaire, various SFA events, modern conference sites
Strategy: GraphQL API with persisted queries and cursor pagination
"""

import requests
import base64
import pandas as pd
from typing import List, Dict, Optional
import time


class SwapcardScraper:
    """Scrape exhibitors from Swapcard/Next.js-based sites"""

    def __init__(self, graphql_url: str, event_url: str, output_name: str):
        self.graphql_url = graphql_url
        self.event_url = event_url
        self.output_name = output_name
        self.session = requests.Session()
        self.exhibitors: List[Dict] = []

        # GraphQL params (found via network interception)
        self.view_id = ""  # base64-encoded view ID
        self.event_id = ""  # base64-encoded event ID
        self.query_hash = ""  # sha256 of persisted query
        self.cursor = None

    def discover_params(self):
        """
        Run Playwright to discover GraphQL parameters
        This captures the view ID, event ID, and query hash from network calls
        """
        print(f"🔍 Discovering GraphQL parameters from {self.event_url}...")

        from playwright.sync_api import sync_playwright

        api_calls = []

        def on_response(response):
            req = response.request
            ct = response.headers.get("content-type", "")

            if req.resource_type in ["xhr", "fetch"] or "json" in ct:
                if "/graphql" in response.url:
                    try:
                        api_calls.append({
                            "url": response.url,
                            "method": req.method,
                            "post_data": req.post_data[:1000] if req.post_data else None,
                        })
                    except:
                        pass

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.on("response", on_response)
            page.goto(self.event_url, wait_until="networkidle", timeout=45000)
            time.sleep(3)
            browser.close()

        # Parse captured GraphQL calls
        for call in api_calls:
            if call["post_data"]:
                try:
                    data = json.loads(call["post_data"])
                    for item in data:
                        if item.get("extensions", {}).get("persistedQuery"):
                            self.query_hash = item["extensions"]["persistedQuery"]["sha256Hash"]
                            vars = item.get("variables", {})
                            self.view_id = vars.get("viewId", "")
                            self.event_id = vars.get("eventId", "")
                            print(f"✅ Discovered params:")
                            print(f"  View ID: {self.view_id}")
                            print(f"  Event ID: {self.event_id}")
                            print(f"  Query Hash: {self.query_hash[:20]}...")
                            return
                except:
                    continue

        if not self.query_hash:
            raise ValueError("Could not discover GraphQL parameters")

    def scrape_page(self) -> Optional[List[Dict]]:
        """Scrape one page using GraphQL cursor"""
        variables = {
            "withEvent": True,
            "viewId": self.view_id,
            "eventId": self.event_id
        }

        if self.cursor:
            variables["endCursor"] = self.cursor

        payload = [{
            "operationName": "EventExhibitorListViewConnectionQuery",
            "variables": variables,
            "extensions": {
                "persistedQuery": {
                    "version": 1,
                    "sha256Hash": self.query_hash
                }
            }
        }]

        print(f"📄 Fetching page with cursor: {self.cursor}")
        resp = self.session.post(self.graphql_url, json=payload)

        if resp.status_code != 200:
            print(f"❌ Failed: {resp.status_code}")
            return None

        data = resp.json()

        try:
            nodes = data[0]["data"]["view"]["exhibitors"]["nodes"]
            page_info = data[0]["data"]["view"]["exhibitors"]["pageInfo"]
        except (KeyError, IndexError) as e:
            print(f"❌ Error parsing response: {e}")
            print(f"Response: {json.dumps(data, indent=2)[:500]}")
            return None

        exhibitors = []
        for node in nodes:
            exhibitor = {
                "name": node.get("name", ""),
                "website": node.get("websiteUrl", ""),
            }

            # Add booth info if available
            with_event = node.get("withEvent", {})
            if with_event:
                exhibitor["booth"] = with_event.get("booth", "")
                exhibitor["description"] = with_event.get("htmlDescription", "")

            exhibitors.append(exhibitor)

        # Update cursor for next page
        if page_info.get("hasNextPage"):
            self.cursor = page_info.get("endCursor")
        else:
            self.cursor = None

        return exhibitors

    def scrape_all(self):
        """Scrape all exhibitors"""
        print(f"🚀 Starting scrape of {self.output_name}...")

        # Auto-discover params
        self.discover_params()

        # Paginate through all results
        while self.cursor is not None:
            exhibitors = self.scrape_page()
            if exhibitors:
                self.exhibitors.extend(exhibitors)
                print(f"  ✅ Found {len(exhibitors)} exhibitors")
            else:
                break

            time.sleep(1)  # Rate limiting

        # Fetch first page (cursor=None is initial)
        exhibitors = self.scrape_page()
        if exhibitors:
            self.exhibitors.extend(exhibitors)

        print(f"🎉 Total exhibitors scraped: {len(self.exhibitors)}")

    def to_dataframe(self) -> pd.DataFrame:
        """Convert to pandas DataFrame"""
        return pd.DataFrame(self.exhibitors)


def main():
    """Main runner"""
    # Example: Winter FancyFaire 2026
    GRAPHQL_URL = "https://events.example.com/api/graphql"
    EVENT_URL = "https://events.example.com/winter-fancyfaire-2026"
    OUTPUT_NAME = "winter_fancyfaire_2026"

    scraper = SwapcardScraper(GRAPHQL_URL, EVENT_URL, OUTPUT_NAME)
    scraper.scrape_all()

    # Save results
    df = scraper.to_dataframe()

    from utils import save_to_csv, save_to_excel

    save_to_csv(df, f"{OUTPUT_NAME}.csv")
    save_to_excel(df, f"{OUTPUT_NAME}.xlsx")


if __name__ == "__main__":
    main()
