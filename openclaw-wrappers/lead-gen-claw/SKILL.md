# Lead Generation Claw

Automated lead generation system for agencies and B2B sales teams.

---

## 🎯 What It Does

The Lead Generation Claw automates the entire lead generation workflow:

1. **Scrapes trade shows and directories** (Expo West, Winter FancyFaire, etc.)
2. **Enriches leads** (website verification, email validation, industry classification)
3. **Qualifies leads** (scoring 0-100 based on criteria)
4. **Exports in multiple formats** (CSV, Excel, SQLite)
5. **Delivers daily batches** via WhatsApp/Telegram/Slack

**Daily message:**
> "📊 New leads batch ready:
> 
> • 47 qualified leads from Expo West
> • 23 leads from Winter FancyFaire
> • 12 high-priority (score 90+)
> 
> 📥 Export: CSV, Excel, SQLite
> 📈 Click to view dashboard"

---

## 💡 Pain Points Solved

| Pain | Traditional | Lead Gen Claw |
|-------|-------------|----------------|
| Manual scraping | Hours of copy-paste | Automatic API discovery |
| Email verification | One-by-one check | Batch verification in seconds |
| Qualification | Spreadsheet filtering | AI-powered scoring (0-100) |
| Daily delivery | Manual export | Automated via message |
| Multiple formats | One export choice | CSV + Excel + SQLite |

---

## 🛠 Features

### Scraping
- **SmallWorldLabs** — AJAX POST + token rotation
- **Swapcard/Next.js** — GraphQL + persisted queries
- **Map Your Show** — REST/HTML parsing
- **A2Z/Personify** — AJAX + session management
- **Bizzabo** — REST API integration
- **Cvent** — Playwright automation
- **Eventbrite** — Public API

### Enrichment
- Website verification (HTTP 200 check)
- Email validation (format + SMTP check)
- Industry classification (AI-based)
- Social media links (LinkedIn, Twitter)

### Qualification
- **Score 0-100** based on:
  - Company size (employee count, revenue)
  - Industry relevance
  - Email deliverability
  - Social media presence
  - Geographic fit
- **Custom filters** (minimum score, regions, industries)

### Storage
- **CSV** — Excel-compatible
- **Excel** — Pivot tables, filtering
- **SQLite** — Queries, joins, app integration

### Delivery
- **WhatsApp** — Direct message with download links
- **Telegram** — File upload to chat
- **Slack** — Channel notification
- **Email** — CSV attachment

---

## 📊 Target Buyers

| Segment | Price | Why Buy |
|----------|--------|----------|
| Agencies | $249/mo | Scale without hiring |
| B2B sales teams | $249/mo | More leads, faster |
| Event marketers | $199/mo | Pre-show preparation |
| Business development | $199/mo | Continuous pipeline |

---

## ⚙️ Configuration

### config.json

```json
{
  "sources": [
    {
      "name": "Expo West 2026",
      "url": "https://smallworldlabs.com/events/expo-west-2026",
      "platform": "smallworldlabs",
      "enabled": true
    }
  ],
  "enrichment": {
    "verify_websites": true,
    "validate_emails": true,
    "classify_industry": true,
    "find_social_media": true
  },
  "qualification": {
    "min_score": 50,
    "criteria": {
      "company_size": ["small", "medium", "large"],
      "industries": ["food", "beverage", "retail"],
      "regions": ["US", "Canada", "Europe"]
    }
  },
  "delivery": {
    "channel": "whatsapp",
    "schedule": "09:00",
    "formats": ["csv", "excel", "sqlite"]
  }
}
```

---

## 🚀 Quick Start

### 1. Install Dependencies

```bash
cd ~/pi-mono-workspace/openclaw-wrappers/lead-gen-claw
pip install -r requirements.txt
```

### 2. Configure Your Sources

Edit `config.json` with your target events/directories.

### 3. Run First Scrape

```bash
python src/lead_gen_claw.py --config config.json
```

### 4. Receive Daily Batches

The claw automatically sends qualified leads via your chosen channel (WhatsApp/Telegram/Slack).

---

## 💰 Pricing

| Plan | Price | Features |
|-------|--------|-----------|
| **Starter** | $99/mo | 1 source, 500 leads/month, CSV only |
| **Professional** | $249/mo | 5 sources, 2,000 leads/month, all formats |
| **Enterprise** | $499/mo | Unlimited sources, unlimited leads, custom filters, priority support |

---

## 📈 Battle-Tested

- ✅ Expo West 2026 — 3,144 exhibitors scraped
- ✅ Winter FancyFaire 2026 — 1,035 exhibitors scraped
- ✅ Daily delivery via WhatsApp (tested)
- ✅ Email verification (90%+ accuracy)
- ✅ Export to CSV, Excel, SQLite

---

## 📚 Documentation

- **Setup Guide** — `README.md`
- **Configuration Templates** — `templates/config-*.json`
- **Troubleshooting** — `TROUBLESHOOTING.md`
- **API Reference** — `API.md`

---

## 🦞 Why Buy This Wrapper?

1. **Setup in 10 minutes** — Copy-paste credentials, go live
2. **Fully automated** — No manual scraping or verification
3. **Daily delivery** — Wake up to new leads every morning
4. **Multiple formats** — Import into any CRM or spreadsheet
5. **Battle-tested** — Used to scrape 4,000+ exhibitors

**Stop scraping manually. Start growing your pipeline.** 📊
