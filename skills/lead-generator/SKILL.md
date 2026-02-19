---
name: lead-generator
description: "Automated lead generation system for trade shows, directories, and business listings"
metadata: {
  "openclaw": {
    "requires": {
      "tools": ["browser", "write", "read", "exec"],
      "runtime": "python"
    },
    "tags": ["leads", "scraping", "automation", "outreach"]
  }
}
---

# Lead Generator Skill

## What It Is

Automated lead generation system for:
- Trade show exhibitor scraping
- Business directory extraction
- Company research and enrichment
- Lead qualification and scoring
- Outreach campaign automation

Built on existing tools:
- `trade-show-scraping/` - Trade show scrapers
- `browser-use` - Natural language browser automation
- Team conventions - Forge workflow

---

## Why It Matters

### The Problem

- Manual lead generation is time-consuming
- Trade shows have thousands of exhibitors
- Business directories require data extraction
- Outreach needs personalization and tracking

### The Solution

- Automate data collection from multiple sources
- Qualify leads automatically (business services, target market)
- Enrich data (websites, descriptions, contact info)
- Generate outreach campaigns
- Track follow-ups and responses

---

## Quick Start

```bash
cd lead-generator/

# Install dependencies
pip install -r requirements.txt

# Run generator
python run.py --source trade-show --url "https://www.expowest.com"

# Or use browser automation
python run.py --source browser --query "restaurants in Bergamo"
```

---

## Architecture

```
┌─────────────────────────────────────┐
│        Lead Generator          │
│  ┌───────────────────────┐ │
│  │     Data Sources     │ │
│  │                     │ │
│  │ ┌─────────────┐     │ │
│  │ │ Trade Shows  │     │ │
│  │ └─────────────┘     │ │
│  └───────────────────────┘ │
│                              │
│  ┌───────────────────────┐ │
│  │     Enrichment      │ │
│  │                     │ │
│  │ ┌─────────────┐     │ │
│  │ │ Browser Use  │     │ │
│  │ └─────────────┘     │ │
│  └───────────────────────┘ │
│                              │
│  ┌───────────────────────┐ │
│  │   Qualification     │ │
│  │                     │ │
│  │ Filter & Score    │ │
│  └───────────────────────┘ │
│                              │
│  ┌───────────────────────┐ │
│  │     Storage         │ │
│  │                     │ │
│  │ ┌─────────────┐     │ │
│  │ │  CSV/Excel  │     │ │
│  │ │  SQLite DB  │     │ │
│  │ └─────────────┘     │ │
│  └───────────────────────┘ │
│                              │
│  ┌───────────────────────┐ │
│  │     Outreach         │ │
│  │                     │ │
│  │ ┌─────────────┐     │ │
│  │ │  Email       │     │ │
│  │ │  LinkedIn    │     │ │
│  │ │  Templates   │     │ │
│  │ └─────────────┘     │ │
│  └───────────────────────┘ │
└─────────────────────────────────────┘
```

---

## Phase 1: Data Sources

### Trade Show Scraping

```python
from scrapers.smallworldlabs import SmallWorldLabsScraper
from scrapers.swapcard import SwapcardScraper

# Scrape trade shows
scraper = SmallWorldLabsScraper("https://www.expowest.com")
leads = scraper.scrape_all()
```

**Supported Platforms:**
- SmallWorldLabs (Expo West, SEMICON)
- Swapcard/Next.js (Winter FancyFaire)
- Map Your Show
- A2Z/Personify

### Business Directory Scraping

```python
# Use browser-use for any directory
browser_query = """
Go to https://www.yellowpages.com
Search for "restaurants" in "Bergamo, Italy"
Extract first 20 results with: name, phone, email, website
"""
leads = browser_scrape(browser_query)
```

---

## Phase 2: Lead Enrichment

```python
class LeadEnricher:
    """Enrich lead data with additional information."""

    def enrich_website(self, website: str) -> dict:
        """Extract company info from website."""
        # Use browser-use to visit website
        # Extract: description, products, contact form
        pass

    def find_email(self, company_name: str) -> str:
        """Search for company email."""
        # Use browser-use to Google search
        # Find: info@, contact@, etc.
        pass

    def classify_industry(self, description: str) -> str:
        """Classify business type."""
        keywords = {
            "restaurant": ["menu", "dining", "food", "cuisine"],
            "retail": ["store", "shop", "products", "sales"],
            "tech": ["software", "platform", "saas", "ai"],
        }
        # Match and classify
        pass
```

---

## Phase 3: Qualification

```python
class LeadQualifier:
    """Score and qualify leads."""

    BUSINESS_SERVICES = [
        "consulting", "marketing", "agency", "services",
        "outsourcing", "freelance", "contractor",
    ]

    def score_lead(self, lead: dict) -> int:
        """Calculate lead quality score (0-100)."""
        score = 50  # Base score

        # Has website
        if lead.get("website"):
            score += 15

        # Has email
        if lead.get("email"):
            score += 20

        # Not a business service
        if not self._is_business_service(lead.get("name", "")):
            score += 15

        return min(score, 100)

    def _is_business_service(self, name: str, description: str = "") -> bool:
        """Check if this is a business service (should exclude)."""
        combined = f"{name} {description}".lower()
        return any(service in combined for service in self.BUSINESS_SERVICES)
```

---

## Phase 4: Storage

```python
class LeadStorage:
    """Store leads in multiple formats."""

    def __init__(self, db_path: str = "leads.db"):
        self.db_path = db_path
        self.csv_path = "leads.csv"
        self.xlsx_path = "leads.xlsx"

    def save_to_db(self, leads: list[dict]):
        """Save to SQLite database."""
        import sqlite3
        conn = sqlite3.connect(self.db_path)
        # Create table if not exists
        # Insert leads
        conn.close()

    def save_to_csv(self, leads: list[dict]):
        """Save to CSV file."""
        import pandas as pd
        df = pd.DataFrame(leads)
        df.to_csv(self.csv_path, index=False)

    def save_to_excel(self, leads: list[dict]):
        """Save to Excel file."""
        import pandas as pd
        df = pd.DataFrame(leads)
        df.to_excel(self.xlsx_path, index=False)
```

---

## Phase 5: Outreach

```python
class OutreachGenerator:
    """Generate personalized outreach campaigns."""

    EMAIL_TEMPLATES = {
        "intro": """
Hi {name},

I came across {company} at {source} and was impressed by your work in {industry}.

I'd love to learn more about your offerings. Are you open to a brief call this week?

Best,
{my_name}
{my_title}
{my_company}
        """,
        "followup": """
Hi {name},

Just following up on my previous note. Would love to connect and explore how we might collaborate.

Best,
{my_name}
        """,
    }

    LINKEDIN_TEMPLATES = {
        "connection_request": """
Hi {name},

I came across your profile and was impressed by your work at {company} in {industry}.

I'd love to connect and explore potential collaboration opportunities.

Best,
{my_name}
        """,
    }

    def generate_email(self, lead: dict, template_name: str = "intro") -> str:
        """Generate personalized email."""
        template = self.EMAIL_TEMPLATES[template_name]
        return template.format(**lead, **self.get_sender_info())

    def generate_linkedin_message(self, lead: dict, template_name: str = "connection_request") -> str:
        """Generate personalized LinkedIn message."""
        template = self.LINKEDIN_TEMPLATES[template_name]
        return template.format(**lead, **self.get_sender_info())

    def get_sender_info(self) -> dict:
        """Get sender information from config."""
        return {
            "my_name": "Alessandro",
            "my_title": "Founder & CEO",
            "my_company": "OpenClaw",
        }
```

---

## Usage Examples

### Example 1: Scrape Trade Show

```bash
python run.py \
  --source trade-show \
  --url https://www.expowest.com \
  --output expo_west_2026 \
  --filter-services
```

**Output:**
- `expo_west_2026.csv` - All exhibitors
- `expo_west_2026.xlsx` - Excel format
- `expo_west_2026.db` - SQLite database

### Example 2: Scrape Business Directory

```bash
python run.py \
  --source browser \
  --query "AI automation companies in Italy" \
  --output ai_italy_leads \
  --limit 50
```

### Example 3: Generate Outreach Campaign

```bash
python run.py \
  --source file \
  --input expo_west_2026.csv \
  --campaign intro \
  --output outreach_campaign
```

---

## CLI Interface

```bash
# Data Sources
python run.py --source trade-show --url <URL>           # Scrape trade show
python run.py --source browser --query "<query>"         # Browser scraping

# Processing
python run.py --source file --input <file>             # Load from file
python run.py --enrich                           # Enrich existing leads
python run.py --qualify                          # Qualify and score
python run.py --filter-business-services             # Remove consultants/agencies

# Outreach
python run.py --campaign <template>                 # Generate outreach
python run.py --outreach-email --test                # Test email (dry run)

# Output
--output <name>                                  # Output file prefix
--format csv|excel|db                          # Output format
--limit <number>                                  # Limit results
```

---

## Lead Schema

```python
{
    "id": str,                    # Unique identifier
    "source": str,                 # Trade show, directory, etc.
    "source_url": str,             # URL where found
    "name": str,                  # Company/Exhibitor name
    "description": str,            # Company description
    "website": str,                # Company website
    "email": str,                  # Contact email
    "phone": str,                  # Contact phone
    "booth": str,                  # Trade show booth #
    "industry": str,               # Classified industry
    "category": str,                # Category (SaaS, Retail, etc.)
    "score": int,                  # Lead quality score (0-100)
    "status": str,                 # new, contacted, qualified, closed
    "notes": str,                  # Notes/interaction history
    "created_at": datetime,          # When lead was generated
    "updated_at": datetime,           # Last update
}
```

---

## Best Practices

### Data Collection

- Always verify data accuracy
- Check for duplicates (company name + website)
- Normalize phone numbers and emails
- Classify industry/category

### Qualification

- Exclude business services (consultants, agencies)
- Score leads based on available data
- Prioritize high-quality leads first
- Track lead sources for ROI

### Outreach

- Personalize based on company/industry
- Use multiple channels (email, LinkedIn)
- Track all interactions in lead notes
- Follow up appropriately (not spam)
- A/B test subject lines

### Privacy

- Respect website terms of service
- Don't scrape behind login walls
- Comply with robots.txt
- Use rate limiting

---

## Integration with Existing Tools

### Trade Show Scraping

```python
from trade_show_scraping.smallworldlabs import SmallWorldLabsScraper

# Use existing scraper
scraper = SmallWorldLabsScraper(url)
leads = scraper.scrape_all()
```

### Browser-Use

```python
# Use browser tool for custom queries
browser_result = browser.run("""
Go to {website}
Extract company description and contact information
""")
```

---

## Configuration

### Config File (`config.json`)

```json
{
  "sender": {
    "name": "Alessandro",
    "title": "Founder & CEO",
    "company": "OpenClaw",
    "email": "alessandro@openclaw.ai",
    "phone": "+39 329 348 4956"
  },
  "smtp": {
    "host": "smtp.gmail.com",
    "port": 587,
    "use_tls": true
  },
  "linkedin": {
    "session_cookie": "",
    "user_agent": ""
  },
  "filters": {
    "exclude_business_services": true,
    "min_score": 50,
    "industries": ["SaaS", "Retail", "Hospitality"]
  }
}
```

---

## Error Handling

```python
try:
    leads = scrape_tradeshow(url)
except ScrapingError as e:
    logger.error(f"Scraping failed: {e}")
    # Fallback to browser-use
    leads = browser_scrape_fallback(url)
except Exception as e:
    logger.error(f"Unexpected error: {e}")
    # Save partial results
    save_partial_results(leads[:current_index])
```

---

## Output Formats

### CSV

```csv
id,name,description,website,email,phone,booth,industry,category,score,status,notes,created_at,updated_at
1,Company A,Description,https://companya.com,,555-1234,A-101,Technology,SaaS,75,new,,2026-02-19,2026-02-19
```

### Excel

- Multiple sheets: All Leads, Qualified, Contacted
- Formatted for easy filtering
- Include charts for lead distribution

### SQLite

```sql
CREATE TABLE leads (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source TEXT,
    name TEXT,
    description TEXT,
    website TEXT,
    email TEXT,
    phone TEXT,
    booth TEXT,
    industry TEXT,
    category TEXT,
    score INTEGER,
    status TEXT DEFAULT 'new',
    notes TEXT,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);
```

---

## Success Criteria

Lead generator is complete when:

- [ ] Data source scrapers working
- [ ] Enrichment extracting additional info
- [ ] Qualification scoring leads
- [ ] Storage in multiple formats (CSV, Excel, DB)
- [ ] Outreach templates generated
- [ ] CLI interface functional
- [ ] Documentation complete

---

## Next Steps

After basic lead generator:

1. **Email Integration** - Send emails via SMTP
2. **LinkedIn Automation** - Send connection requests via API
3. **CRM Integration** - Export to HubSpot/Salesforce
4. **Analytics** - Track campaign performance
5. **Follow-up Automation** - Auto-schedule follow-ups

---

*Lead generation automation - from scraping to outreach* 🎯
