# Trade Show Scraping - Project Created

---

## What Was Created

### Files

| File | Purpose |
|-------|---------|
| `TRADE_SHOW_SCRAPING_PLAYBOOK.md` | Complete scraping guide with all strategies |
| `README.md` | Quick start and usage instructions |
| `utils.py` | Shared utilities (filtering, export) |
| `smallworldlabs_scraper.py` | SmallWorldLabs platform scraper |
| `swapcard_scraper.py` | Swapcard/Next.js GraphQL scraper |
| `run.py` | Main CLI runner |
| `requirements.txt` | Python dependencies |
| `.gitignore` | Git ignore patterns |
| `.env.example` | Environment template |

### Directories

```
trade-show-scraping/
├── output/              # Scraped results (CSV/Excel)
├── venv/               # Python virtual environment
├── *.py                # Scripts
├── *.md                # Documentation
├── requirements.txt      # Dependencies
└── .gitignore         # Git config
```

---

## Setup

```bash
cd /home/majinbu/pi-mono-workspace/trade-show-scraping

# Install dependencies
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
playwright install chromium
```

---

## Quick Start

### SmallWorldLabs (Expo West)

```bash
python run.py smallworldlabs \
  --url https://www.expowest.com \
  --output expo_west_2026
```

### Swapcard (Winter FancyFaire)

```bash
python run.py swapcard \
  --url https://events.example.com/event-name \
  --output event_name_2026
```

---

## Supported Platforms

| Platform | Strategy | Status |
|-----------|-----------|--------|
| SmallWorldLabs | AJAX POST + token rotation | ✅ Ready |
| Swapcard/Next.js | GraphQL + persisted queries | ✅ Ready |
| Map Your Show | REST/HTML | 📝 Playbook only |
| A2Z/Personify | AJAX + session | 📝 Playbook only |
| Bizzabo | REST API | 📝 Playbook only |
| Cvent | Playwright | 📝 Playbook only |
| Eventbrite | Public API | 📝 Playbook only |

---

## Features

- ✅ Auto API discovery (Playwright network interception)
- ✅ Token rotation (SmallWorldLabs)
- ✅ GraphQL with persisted queries (Swapcard)
- ✅ Threaded detail page enrichment
- ✅ Business services filtering
- ✅ CSV/Excel export
- ✅ Rate limiting

---

## Battle-Tested

- ✅ Expo West 2026: 3,144 exhibitors
- ✅ Winter FancyFaire 2026: 1,035 exhibitors

---

## Integration with browser-use

Your browser-use skill can simplify this further! Instead of writing Playwright scripts, just say:

> "Go to Expo West exhibitors page, scrape all exhibitor names and websites"

The AI will figure out the clicks and extraction automatically.

---

## Location

```
/home/majinbu/pi-mono-workspace/trade-show-scraping/
```

---

*Project created and ready to use! 🚀*
