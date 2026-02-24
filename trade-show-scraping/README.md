# Trade Show Exhibitor Scraping

Battle-tested scrapers for extracting exhibitor lists from trade show websites.

---

## Supported Platforms

| Platform | Examples | Strategy |
|-----------|------------|-----------|
| **SmallWorldLabs** | Expo West, SEMICON, Informa events | AJAX POST pagination + token rotation |
| **Swapcard/Next.js** | Winter FancyFaire, SFA events | GraphQL API with persisted queries |

---

## Installation

```bash
cd trade-show-scraping

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install Playwright browser (for API discovery)
playwright install chromium
```

---

## Usage

### SmallWorldLabs (e.g., Expo West)

```bash
python run.py smallworldlabs \
  --url https://www.expowest.com \
  --output expo_west_2026 \
  --filter-services
```

### Swapcard/Next.js (e.g., Winter FancyFaire)

```bash
python run.py swapcard \
  --url https://events.example.com/winter-fancyfaire-2026 \
  --output winter_fancyfaire_2026 \
  --filter-services
```

---

## Output

Results are saved to the `output/` directory:
- `exhibitors.csv` - CSV format
- `exhibitors.xlsx` - Excel format

---

## Filtering

Use `--filter-services` to remove business service providers (consulting, marketing, etc.) and keep only product companies.

---

## API Discovery

For Swapcard sites, the script auto-discovers GraphQL parameters using Playwright network interception.

---

## Rate Limiting

- Default: 1 second delay between requests
- Adjust in scraper scripts if needed

---

## Troubleshooting

### Token Errors (SmallWorldLabs)
- The server issues new tokens with each response
- Make sure token rotation is working

### GraphQL Query Hash (Swapcard)
- Query hashes can change when the site deploys new code
- Re-run discovery if scraping fails

### Missing Data
- Not all exhibitors fill in every field
- Typical fill rates: Name 100%, Website 70-99%, Description 30-60%

---

## Battle-Tested

- ✅ Expo West 2026: 3,144 exhibitors
- ✅ Winter FancyFaire 2026: 1,035 exhibitors

---

*Built for lead generation and business intelligence* 📊
