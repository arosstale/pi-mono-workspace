# Lead Generator

Automated lead generation for trade shows, directories, and business listings.

---

## What It Is

Scrape, qualify, enrich, and generate outreach for business leads from multiple sources.

**Data Sources:**
- Trade show exhibitors (Expo West, Winter FancyFaire, etc.)
- Business directories
- Company websites
- LinkedIn profiles

**Capabilities:**
- Automatic scraping (SmallWorldLabs, Swapcard platforms)
- Browser automation (any website)
- Lead qualification (scoring, filtering)
- Outreach generation (emails, LinkedIn messages)
- Multi-format output (CSV, Excel, SQLite)

---

## Quick Start

```bash
cd skills/lead-generator/

# Install
pip install -r requirements.txt

# Scrape a trade show
python run.py --source trade-show --url https://www.expowest.com

# Generate outreach
python run.py --source file --input expo_leads.csv --campaign intro
```

---

## Usage

### Trade Show Scraping

```bash
python run.py \
  --source trade-show \
  --url <URL> \
  --output <name> \
  --filter-services
```

**Supported:**
- SmallWorldLabs (Expo West, SEMICON)
- Swapcard/Next.js (Winter FancyFaire)
- Map Your Show
- A2Z/Personify

### Business Directory Scraping

```bash
python run.py \
  --source browser \
  --query "<search query>" \
  --output <name> \
  --limit <number>
```

### Lead Processing

```bash
# Enrich existing leads
python run.py --source file --input leads.csv --enrich

# Qualify and score
python run.py --source file --input leads.csv --qualify

# Generate outreach
python run.py --source file --input leads.csv --campaign intro
```

---

## Lead Schema

| Field | Type | Description |
|--------|--------|-------------|
| id | str | Unique identifier |
| source | str | Trade show, directory, etc. |
| source_url | str | URL where found |
| name | str | Company name |
| description | str | Company description |
| website | str | Company website |
| email | str | Contact email |
| phone | str | Contact phone |
| booth | str | Trade show booth # |
| industry | str | Classified industry |
| category | str | SaaS, Retail, etc. |
| score | int | Quality score (0-100) |
| status | str | new, contacted, qualified, closed |
| notes | str | Notes/interaction history |
| created_at | datetime | When generated |
| updated_at | datetime | Last update |

---

## Output Formats

- **CSV** - `leads.csv` - Importable to Excel
- **Excel** - `leads.xlsx` - Multiple sheets, formulas
- **SQLite** - `leads.db` - Queryable database

---

## Configuration

Create `config.json`:

```json
{
  "sender": {
    "name": "Your Name",
    "title": "Your Title",
    "company": "Your Company",
    "email": "your@email.com",
    "phone": "+1 555 123 4567"
  },
  "filters": {
    "exclude_business_services": true,
    "min_score": 50,
    "industries": ["SaaS", "Retail", "Hospitality"]
  }
}
```

---

## Integration

### Trade Show Scraping

Uses existing `trade-show-scraping/` project:
- `smallworldlabs_scraper.py`
- `swapcard_scraper.py`

### Browser Automation

Uses `browser-use` skill for:
- Website enrichment
- Email discovery
- Company research

---

## Best Practices

- **Quality > Quantity** - Score and qualify leads
- **Personalize** - Customize outreach per lead
- **Track** - Log all interactions in notes
- **Follow Up** - Don't spam, timely follow-ups
- **Respect Privacy** - Follow robots.txt, rate limits

---

## Location

```
/home/majinbu/pi-mono-workspace/skills/lead-generator/
```

---

*Automated lead generation - from scraping to outreach* 🎯
