# Trade Show Exhibitor Scraping Playbook

Step-by-step methodology for scraping exhibitor lists from any trade show / expo website.
Battle-tested on Expo West 2026 (3,144 exhibitors) and Winter FancyFaire 2026 (1,035 exhibitors).

---

## Phase 1: Recon — Identify the Platform

Every trade show site uses one of a handful of platforms under the hood. The platform determines your scraping strategy.

### How to Identify

1. **View Page Source** — look for platform fingerprints in script tags, CSS, meta tags
2. **Check Network Tab** — load exhibitor page with DevTools open, watch XHR/Fetch calls
3. **Check subdomains** — exhibitor directories often live on a subdomain powered by a vendor

### Common Platforms

| Platform | Fingerprint | Strategy |
|-----------|-------------|-----------|
| **SmallWorldLabs** | `*.smallworldlabs.com`, `JSPaginator`, `swl_*_sess` cookie | AJAX POST pagination |
| **Swapcard** | `events.*.com`, `__NEXT_DATA__`, `swapcard` in scripts, GraphQL `/api/graphql` | GraphQL API with cursor pagination |
| **Map Your Show** | `*.mapyourshow.com`, `/8_0/exhview/`, `MYSFloorplan` | REST API or HTML scrape |
| **A2Z / Personify** | `*.a2zinc.net`, `a2z` in scripts | AJAX with session tokens |
| **Gripeo / Swapcard** | Next.js + Apollo cache in `__NEXT_DATA__` | Parse Apollo state or use GraphQL |
| **Bizzabo** | `*.bizzabo.com` | REST API |
| **Cvent** | `*.cvent.com` | Usually requires Playwright |
| **Eventbrite** | `*.eventbrite.com` | Public API available |

---

## Phase 2: API Discovery with Playwright

When you can't figure out the API from source alone, use **Playwright network interception** to capture every XHR/Fetch call the page makes.

### The Discovery Script Pattern

```python
from playwright.sync_api import sync_playwright
import json
import time

api_calls = []

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    def on_response(response):
        req = response.request
        ct = response.headers.get("content-type", "")

        if req.resource_type in ["xhr", "fetch"] or "json" in ct:
            try:
                body = response.text()
                api_calls.append({
                    "method": req.method,
                    "url": response.url,
                    "status": response.status,
                    "size": len(body),
                    "body_preview": body[:2000],
                    "post_data": req.post_data[:500] if req.post_data else None,
                })
            except:
                pass

    page.on("response", on_response)
    page.goto(TARGET_URL, wait_until="networkidle", timeout=45000)
    time.sleep(3)

    # Trigger pagination to capture data-loading calls
    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    time.sleep(2)

    # Click "next page" or "load more" to see paginated API calls
    next_btn = page.query_selector("a[rel='next'], .pager-right-next, button:has-text('More')")
    if next_btn:
        next_btn.click()
        time.sleep(3)

    browser.close()

# The gold is here — inspect what the site fetches
for call in api_calls:
    print(f"{call['method']} {call['url'][:120]}")
    if call['post_data']:
        print(f"  POST: {call['post_data'][:300]}")
    print(f"  Body: {call['body_preview'][:300]}")
```

### What You're Looking For

- **POST to `/index.php` or `/api/`** — AJAX pagination endpoints
- **POST to `/api/graphql`** — GraphQL APIs (Swapcard, Bizzabo, etc.)
- **GET to `/api/exhibitors`** — REST APIs
- **Response with `"total"` field** — pagination metadata
- **URL-encoded HTML in response `"data"` field** — SmallWorldLabs pattern
- **`nodes` array in response** — GraphQL relay-style pagination

---

## Phase 3: Platform-Specific Scraping Strategies

### Strategy A: SmallWorldLabs (AJAX POST + Token Rotation)

**Used for:** Expo West, SEMICON, various Informa events

**How it works:**
1. GET exhibitor page → grab session cookie + `tk`/`tm` CSRF tokens from inline JS
2. POST to `/index.php` with pagination params → get URL-encoded HTML + new tokens
3. Rotate tokens each request (server gives you fresh `formToken`/`formTime` in each response)
4. Parse HTML table rows for company data

```python
# Step 1: Get session + tokens
session = requests.Session()
resp = session.get(f"{BASE_URL}/exhibitors")

tk = re.search(r'tk\s*=\s*["\']([^"\']{10,})["\']', resp.text).group(1)
tm = re.search(r'tm\s*=\s*["\']([^"\']{10,})["\']', resp.text).group(1)

# Step 2: Paginate
for offset in range(0, total, LIMIT):
    data = {
        "limit": LIMIT,
        "offset": offset,
        "module": "organizations_organization_list",  # <-- found in page JS
        "site_page_id": "3000",  # <-- found in page JS
        "method": "paginationHandler",
        "template": "generic_items",
        "mCell": "0",
        "mId": "1",
        "page_id": "openAjax",
        "ajaxType": "paginate",
        "tk": tk,
        "tm": tm,
    }

    result = session.post(f"{BASE_URL}/index.php", data=data).json()

    # Step 3: Rotate tokens
    tk = result.get("formToken", tk)
    tm = result.get("formTime", tm)
    total = result["total"]  # e.g. 3444

    # Step 4: Parse URL-encoded HTML
    html = unquote(result["data"])
    soup = BeautifulSoup(html, "lxml")

    for row in soup.find_all("tr"):
        link = row.find("a", href=re.compile(r"^/co/"))
        if link:
            name = link.get_text(strip=True)
            profile_url = BASE_URL + link["href"]
```

**Detail page structure** (for enrichment):
- Fields are in `div.row > div.col-4` (label) + sibling div (value)
- Labels: `Name`, `What We Do`, `Website`, `Categories`, `Founded`, `Address`
- Website link is an `<a>` tag inside the value div

```python
for row in soup.find_all("div", class_="row"):
    label_div = row.find("div", class_="text-secondary")
    if not label_div:
        continue

    label = label_div.get_text(strip=True)
    cols = row.find_all("div", recursive=False)
    value_div = cols[-1]

    if label == "Website":
        value = value_div.find("a", href=True)["href"]
    else:
        value = value_div.get_text(strip=True)
```

---

### Strategy B: Swapcard / Next.js (GraphQL with Persisted Queries)

**Used for:** Winter FancyFaire, various SFA events, many modern conference sites

**How it works:**
1. The site is Next.js — server-side rendered with `__NEXT_DATA__` containing Apollo cache
2. The exhibitor list loads via GraphQL POST to `/api/graphql`
3. Uses **persisted queries** (sha256 hash instead of full query text)
4. Cursor-based pagination with `endCursor` param

```python
# Key constants (found via network interception)
GRAPHQL_URL = "https://events.example.com/api/graphql"
VIEW_ID = "RXZlbnRWaWV3XzEyMTQzMDM="  # base64-encoded ID from URL
EVENT_ID = "RXZlbnRfMjc2NjU0MQ=="  # found in network calls
QUERY_HASH = "b3cb76208b6de3d9..."  # sha256 of persisted query

cursor = None
while True:
    variables = {
        "withEvent": True,
        "viewId": VIEW_ID,
        "eventId": EVENT_ID
    }

    if cursor:
        variables["endCursor"] = cursor

    payload = [{
        "operationName": "EventExhibitorListViewConnectionQuery",
        "variables": variables,
        "extensions": {
            "persistedQuery": {
                "version": 1,
                "sha256Hash": QUERY_HASH
            }
        }
    }]

    data = session.post(GRAPHQL_URL, json=payload).json()
    nodes = data[0]["data"]["view"]["exhibitors"]["nodes"]

    for node in nodes:
        name = node["name"]
        booth = node["withEvent"]["booth"]
        description = node.get("htmlDescription", "")

    # Cursor pagination
    page_info = data[0]["data"]["view"]["exhibitors"]["pageInfo"]
    if not page_info["hasNextPage"]:
        break

    cursor = page_info["endCursor"]
```

**Detail page enrichment** — parse `__NEXT_DATA__` Apollo cache:

```python
resp = session.get(detail_url)
soup = BeautifulSoup(resp.text, "lxml")

nd = soup.find("script", id="__NEXT_DATA__")
apollo = json.loads(nd.string)["props"]["apolloState"]

for key, val in apollo.items():
    if key.startswith("Core_Exhibitor:"):
        website = val.get("websiteUrl", "")

        # Custom fields are in withEvent -> fields array
        we = val["withEvent({...})"]
        for field in we["fields"]:
            if field["name"] == "Brands":
                brands = [resolve_ref(v, apollo) for v in field["values"]]
```

---

### Strategy C: Map Your Show (REST or HTML)

**Used for:** AAPEX, RE+, CES floor plans, many Informa floor plans

**How it works:**
- Floor plan viewer at `*.mapyourshow.com/8_0/exhview/index.cfm`
- May have REST API at `api.mapyourshow.com/mysRest/v2/`
- API requires Bearer token (GUID) from page source
- Exhibitor list at `/8_0/exhlist/index.cfm`

```python
# Try REST API if available
headers = {"Authorization": f"Bearer {MYS_GUID}"}
resp = requests.get(f"{MYS_BASE}/mysRest/v2/Exhibitors", headers=headers)

# Or scrape HTML list view
resp = requests.get(f"{MYS_BASE}/8_0/exhlist/index.cfm")
soup = BeautifulSoup(resp.text, "lxml")
```

---

## Phase 4: Detail Page Enrichment (Threaded)

Once you have the exhibitor list, enrich each with detail page data. Use **ThreadPoolExecutor** for 5-10x speedup.

```python
from concurrent.futures import ThreadPoolExecutor, as_completed

def scrape_detail(args):
    idx, url = args
    try:
        resp = requests.get(url, timeout=15)
        # ... parse fields ...
        return idx, {
            "website": ...,
            "categories": ...,
            "description": ...
        }
    except:
        return idx, {}

tasks = [(i, row["profile_url"]) for i, row in df.iterrows()]

with ThreadPoolExecutor(max_workers=8) as executor:
    futures = {executor.submit(scrape_detail, t): t[0] for t in tasks}

    for future in as_completed(futures):
        idx, data = future.result()

        for col, val in data.items():
            df.at[idx, col] = val
```

### Rate Limiting Guidelines

| Threads | Delay | Use Case |
|---------|--------|----------|
| 1 | 1-2s | Conservative / rate-limited sites |
| 4-8 | 0s | Most trade show sites (they handle traffic well) |
| 8-12 | 0s | Large lists (3000+), watch for 429s |

---

## Phase 5: Filtering & Output

### Business Services Filter

Trade shows mix food/product companies with service providers. Filter by category keywords:

```python
BUSINESS_SERVICES_KEYWORDS = [
    "business services", "consulting", "financial services", "insurance",
    "legal services", "marketing services", "advertising services",
    "logistics", "packaging services", "printing services",
    "trade show services", "association", "media", "publication",
    "software", "technology services",
]

def is_business_services(categories: str) -> bool:
    if not categories:
        return False

    cats_lower = categories.lower()
    return any(kw in cats_lower for kw in BUSINESS_SERVICES_KEYWORDS)
```

### Output Format

```python
import pandas as pd

df.to_csv("output/show_name_2026.csv", index=False)
df.to_excel("output/show_name_2026.xlsx", index=False, engine="openpyxl")
```

---

## Quick Reference: New Site Checklist

1. [ ] Open exhibitor page in browser
2. [ ] Open DevTools Network tab, filter by XHR/Fetch
3. [ ] Identify platform (check subdomain, scripts, network calls)
4. [ ] If unclear, run Playwright discovery script
5. [ ] Find: pagination endpoint, auth/tokens, total count
6. [ ] Build list scraper (requests + BeautifulSoup)
7. [ ] Test on first 2-3 pages
8. [ ] Run full pagination
9. [ ] Sample 5 detail pages to find available fields
10. [ ] Build threaded enrichment scraper
11. [ ] Filter out unwanted categories
12. [ ] Export to CSV/Excel

---

## Tech Stack

| Tool | Purpose |
|------|---------|
| `requests` | HTTP calls, session/cookie management |
| `beautifulsoup4` + `lxml` | HTML parsing |
| `playwright` | JS-rendered pages, API discovery via network interception |
| `pandas` + `openpyxl` | Data manipulation, CSV/Excel export |
| `concurrent.futures` | Threaded detail page scraping |

### Install

```bash
python3 -m venv venv
source venv/bin/activate
pip install requests beautifulsoup4 pandas openpyxl lxml playwright
playwright install chromium
```

---

## Gotchas & Lessons Learned

### Token Rotation (SmallWorldLabs)

The server issues new CSRF tokens (`formToken`/`formTime`) with every AJAX response. You **must** use fresh tokens for the next request or you'll get 403s. This is the most common failure point.

### Persisted Queries (Swapcard/GraphQL)

Swapcard doesn't accept raw GraphQL queries — only persisted query hashes. You **must** capture the exact `sha256Hash` from network traffic. These hashes change when the site deploys new code, so they may break over time.

### Base64 IDs

Both Swapcard and some A2Z sites use base64-encoded IDs in URLs. Decode them to understand the data model:
- `RXZlbnRWaWV3XzEyMTQzMDM=` → `EventView_1214303`
- `RXhoaWJpdG9yXzIzMjE1NDg=` → `Exhibitor_2321548`

### Page 1 vs AJAX Pages

SmallWorldLabs renders the first page server-side in HTML. Subsequent pages come from AJAX. Your parser needs to handle **both** formats (full page HTML vs URL-encoded HTML fragment).

### Missing Data is Normal

Not all exhibitors fill in every field. Expect fill rates of:
- Company name: 100%
- Booth: 95-100%
- Website: 70-99% (depends on the show)
- Description/What We Do: 30-60%
- Categories: 40-80%

### Thread Safety

When using ThreadPoolExecutor, create a **new `requests.Session()`** inside each thread function. Don't share sessions across threads — cookie jars aren't thread-safe.

---

## File Structure

```
project/
├── expo_west.py          # SmallWorldLabs list scraper
├── winter_fancyfaire.py  # Swapcard/GraphQL list scraper
├── enrich.py             # Threaded detail page enrichment
├── utils.py              # Shared helpers (filtering, CSV export)
├── run.py               # Main runner
├── requirements.txt
├── venv/
└── output/
    ├── expo_west_2026.csv
    ├── expo_west_2026.xlsx
    ├── winter_fancyfaire_2026.csv
    └── winter_fancyfaire_2026.xlsx
```

---

*Battle-tested strategies for 4,000+ exhibitors across multiple platforms*
