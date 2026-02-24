"""
Trade Show Scraping - Main Runner
"""

import argparse
import sys
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description="Scrape exhibitors from trade show websites")
    parser.add_argument("platform", choices=["smallworldlabs", "swapcard"], help="Platform type")
    parser.add_argument("--url", help="Base URL for the trade show")
    parser.add_argument("--output", help="Output filename prefix")
    parser.add_argument("--filter-services", action="store_true", help="Filter out business services")

    args = parser.parse_args()

    if args.platform == "smallworldlabs":
        from smallworldlabs_scraper import SmallWorldLabsScraper

        if not args.url:
            print("❌ Error: --url required for SmallWorldLabs")
            print("   Example: --url https://www.expowest.com")
            sys.exit(1)

        scraper = SmallWorldLabsScraper(args.url, args.output or "exhibitors")
        scraper.scrape_all()
        df = scraper.to_dataframe()

    elif args.platform == "swapcard":
        from swapcard_scraper import SwapcardScraper

        if not args.url:
            print("❌ Error: --url required for Swapcard")
            print("   Example: --url https://events.example.com/winter-fancyfaire-2026")
            sys.exit(1)

        # Parse URL for GraphQL endpoint
        from urllib.parse import urlparse
        parsed = urlparse(args.url)
        graphql_url = f"{parsed.scheme}://{parsed.netloc}/api/graphql"

        scraper = SwapcardScraper(graphql_url, args.url, args.output or "exhibitors")
        scraper.scrape_all()
        df = scraper.to_dataframe()

    # Save results
    from utils import filter_business_services, save_to_csv, save_to_excel

    if args.filter_services:
        df = filter_business_services(df)

    output_name = args.output or "exhibitors"
    save_to_csv(df, f"{output_name}.csv")
    save_to_excel(df, f"{output_name}.xlsx")


if __name__ == "__main__":
    main()
