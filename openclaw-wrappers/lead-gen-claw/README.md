# Lead Generation Claw — Setup Guide

Automated lead generation in 10 minutes.

---

## ⚡ 10-Minute Setup

### Prerequisites

- ✅ OpenClaw installed and running
- ✅ Python 3.10+
- ✅ WhatsApp Business / Telegram Bot / Slack Workspace
- ✅ Trade show accounts (optional, some work without login)

---

## Step 1: Install Dependencies

```bash
cd ~/pi-mono-workspace/openclaw-wrappers/lead-gen-claw
pip install -r requirements.txt
```

**What this installs:**
- `requests` — HTTP requests
- `beautifulsoup4` — HTML parsing
- `playwright` — JavaScript-heavy sites
- `pandas` — Data export (CSV, Excel)
- `aioboto3` — AWS SES (email validation)
- `openclaw-python` — OpenClaw SDK

---

## Step 2: Configure Your Sources

Edit `config/config.json`:

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

### Sources Available

| Platform | Setup Required |
|-----------|---------------|
| SmallWorldLabs | API token (optional) |
| Swapcard | GraphQL endpoint |
| Map Your Show | None |
| A2Z/Personify | Session cookie (optional) |
| Bizzabo | API key |
| Cvent | Login credentials |
| Eventbrite | API key |

---

## Step 3: Connect Your Delivery Channel

### WhatsApp

```bash
# Configure OpenClaw WhatsApp integration
openclaw channel connect whatsapp
```

Follow QR code instructions.

### Telegram

```bash
# Create bot via BotFather
openclaw channel connect telegram
```

Paste bot token.

### Slack

```bash
# Add bot to workspace
openclaw channel connect slack
```

---

## Step 4: Run First Scrape

```bash
python src/lead_gen_claw.py --config config.json --verbose
```

**Expected output:**

```
[INFO] Starting Lead Generation Claw...
[INFO] Loading sources...
[INFO] Scraping Expo West 2026...
[INFO] Found 3,144 exhibitors
[INFO] Enriching leads...
[INFO] Verifying websites... (90% success)
[INFO] Validating emails... (88% deliverable)
[INFO] Classifying industries...
[INFO] Scoring leads...
[INFO] Qualified: 2,847 leads (score 50+)
[INFO] Exporting to CSV, Excel, SQLite...
[INFO] Sending via WhatsApp...
[INFO] Daily batch sent!
```

---

## Step 5: Schedule Daily Batches

Edit your OpenClaw cron job:

```yaml
# ~/.openclaw/cron.yaml
lead_gen_claw:
  schedule: "0 9 * * *"  # 9:00 AM daily
  command: "python ~/pi-mono-workspace/openclaw-wrappers/lead-gen-claw/src/lead_gen_claw.py --config ~/pi-mono-workspace/openclaw-wrappers/lead-gen-claw/config/config.json"
  enabled: true
```

Restart OpenClaw:

```bash
openclaw restart
```

---

## 📊 Daily Message Example

**WhatsApp/Telegram/Slack:**

```
📊 Lead Generation Claw — Daily Batch

📅 Friday, February 21, 2026

Sources scraped:
• Expo West 2026 — 3,144 total → 2,847 qualified
• Winter FancyFaire — 1,035 total → 890 qualified

📈 Top qualified (score 90+):
1. Organic Valley Co. — Score: 97 — Email: confirmed
2. Whole Foods Market — Score: 95 — Email: confirmed
3. Trader Joe's — Score: 94 — Email: confirmed

📥 Download links:
• CSV: https://your-domain.com/leads/2026-02-21.csv
• Excel: https://your-domain.com/leads/2026-02-21.xlsx
• SQLite: https://your-domain.com/leads/2026-02-21.db

💡 Tip: Contact high-score leads first!
```

---

## 🛠 Troubleshooting

### Scraping Returns 0 Results

**Problem:** Site requires login or blocked by rate limiting.

**Solution:**
1. Check if platform requires API key/token
2. Add rate limiting delay in `config.json`
3. Use different user agent

### Email Validation Fails

**Problem:** SMTP check blocked by ISP.

**Solution:**
```json
{
  "enrichment": {
    "validate_emails": "format_only"  // Skip SMTP check
  }
}
```

### WhatsApp Message Not Sent

**Problem:** Channel not connected.

**Solution:**
```bash
openclaw channel status
# Reconnect if needed
openclaw channel connect whatsapp
```

---

## 💡 Pro Tips

1. **Schedule for 9:00 AM** — Review leads before starting your day
2. **Export all formats** — CSV for CRM, Excel for filtering, SQLite for apps
3. **Set min_score to 50** — Balances quality vs quantity
4. **Filter by industry** — Only get relevant leads for your business
5. **Add multiple sources** — Diversify your pipeline

---

## 📞 Support

- **Documentation:** `TROUBLESHOOTING.md`
- **Issues:** https://github.com/your-repo/lead-gen-claw/issues
- **Community:** Discord (invite only)

---

**Ready to automate your lead generation?** 📊

Setup time: **10 minutes**

Time saved per week: **8+ hours**

Leads generated: **2,000+ per month** (professional plan)
