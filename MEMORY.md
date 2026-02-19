
---

## 👥 **Team & Contacts (2026-02-18)**

### N-Art Team
- **Rayan** - CEO & Founder
  - Email: rayan@n-art.io
  - Telegram ID: 5264265623
  - Role: Full Admin, Trading System Access
  - Config: `/home/majinbu/pi-mono-workspace/n-art/RAYAN_USER_CONFIG.md`

### OpenClaw Team
- **Alessandro (Majinbu)** - Founder & Owner
  - Email: ciao@openclaw.ai
  - WhatsApp: +39 329 348 4956
  - Location: Bergamo, Italia
  - GitHub: https://github.com/arosstale

---

## 🚀 **Sales Sites (2026-02-17)**

### OpenClaw - AI Automation Platform
- **Live:** https://openclaw-sales.netlify.app
- **GitHub:** https://github.com/arosstale/openclaw-sales-site
- **Pricing:** €299-€1,999/mo (50% OFF launch)
- **Target:** Italian SMBs (restaurants, retail, services)
- **Features:** Multi-agent AI, 24/7 automation, sales, support, content
- **Contact:** ciao@openclaw.ai, +39 329 348 4956

### N-Art - AI Trading Agents
- **Live:** https://n-art-sales.netlify.app
- **GitHub:** https://github.com/arosstale/n-art-sales-site
- **Pricing:** $199-1,999/mo
- **Target:** Crypto traders, quant firms, DeFi users
- **Features:** Multi-agent trading, 24/7 operation, risk management
- **CEO & Founder:** Rayan
- **Contact:** rayan@n-art.io

### Revenue Potential (Year 1)
- **OpenClaw:** €490K-€1.7M (120-400 clients)
- **N-Art:** $599K-$3M (100-500 clients)
- **TOTAL:** $1.1M-$4.7M

### Deployment Commands
```bash
# Update OpenClaw
cd ~/pi-mono-workspace/openclaw-sales-site
git add . && git commit -m "Update" && git push

# Update N-Art
cd ~/pi-mono-workspace/n-art-sales
git add . && git commit -m "Update" && git push
```

### Netlify Token
- **Location:** `~/.bashrc` (NETLIFY_AUTH_TOKEN)
- **Team:** Fdsa
- **Email:** adedararosstale@gmail.com

---

## 🧠 Wisdom

### T013: Graceful Degradation > Brittle Perfection
**Confidence:** 1.0 (Technical)
**Source:** Dual Wallet Deployment (Feb 15, 2026)

> "Resilience is the ability to operate while wounded."

In high-availability systems (Trading), a missing configuration (e.g., Wallet 2 Key) must trigger a "Degraded Mode" (Single Wallet) rather than a System Crash.

**Application:** Always wrap critical init logic in try/except blocks that allow the system to proceed with partial resources.

### T014: The RSI Veto Protocol
**Confidence:** 1.0 (Technical)
**Source:** Operation Green Candle

> "Discipline > Activity"

Trading Agents often mistake "Momentum" for "Signal." Adding a hard RSI filter (Veto if > 70 for Longs) acts as a "Prefrontal Cortex" inhibition, preventing impulsive entries at local tops.

**Application:** Apply "Veto Logic" to all impulse-based strategies.

### T015: The Falling Knife Paradox (RSI Trap)
**Confidence:** 1.0 (Technical)
**Source:** Operation Green Candle / Time Machine

> "Oversold RSI in a downturn trend is a trap, not an opportunity."

Low RSI (<30) is NOT always a buy signal. In a macro downtrend (Price < 200MA), oversold RSI indicates momentum failure, not mean reversion. Buying here is "Catching a Falling Knife."

**Application:** VETO BUY if (RSI_Daily < 40) AND (Price < 200_MA). Only buy dips in Uptrends.

---

## 🌐 **Subdomains & DNS (2026-02-19)**

### OpenClaw Subdomains
- **openclaw.n-art.io** → http://host.docker.internal:18789
- **openclaw.fdsa.agency** → http://host.docker.internal:18789
- **openclaw.fdsa.ai** → http://host.docker.internal:18789

### Configuration
- **Coolify Proxy:** `/traefik/dynamic/openclaw.yaml` (configured)
- **Cloudflare DNS:** All 3 subdomains added via API
- **Status:** ⏸️ DNS propagating (up to 24 hours)

### DNS Records Verified
| Domain | Type | Value | Proxied | Status |
|--------|------|--------|---------|--------|
| openclaw.n-art.io | A | 144.76.30.176 | Yes | ✅ Active |
| openclaw.fdsa.agency | A | 144.76.30.176 | Yes | ✅ Active |
| openclaw.fdsa.ai | A | 144.76.30.176 | Yes | ✅ Active |

---

## 📊 **RBI System Completion (2026-02-19)**

### New Agents Created
- **Execution Agent:** `rbi_execution_agent.py`
  - Runs backtests in isolated subprocess
  - Code validation and safety checks
  - Timeout protection (300 seconds)
  - Result parsing and logging

- **Optimization Agent:** `rbi_optimization_agent.py`
  - Analyzes backtest results
  - Identifies performance issues
  - Generates improvements
  - Parameter tuning and code modification

### RBI Pipeline (Complete)
```
Research → Backtest → Package → Debug → Execute → Optimize (feedback loop)
```

### Safety Features
- ✅ Code validation (blocks dangerous imports)
- ✅ Resource limits (2GB memory, 1 CPU core)
- ✅ Timeout protection
- ✅ Graceful error handling

### Documentation
- **File:** `RBI_FIX_COMPLETE.md` - Complete system summary
- **Location:** `/home/majinbu/organized/active-projects/trading-system/quant/core/agents/external/`

---

## 📈 **Trade Show Scraping (2026-02-19)**

### Project Created
- **Location:** `/home/majinbu/pi-mono-workspace/trade-show-scraping/`
- **Playbook:** `TRADE_SHOW_SCRAPING_PLAYBOOK.md` (14KB, comprehensive guide)

### Supported Platforms
| Platform | Strategy | Status |
|-----------|-----------|--------|
| SmallWorldLabs | AJAX POST + token rotation | ✅ Ready |
| Swapcard/Next.js | GraphQL + persisted queries | ✅ Ready |
| Map Your Show | REST/HTML | 📝 In playbook |
| A2Z/Personify | AJAX + session | 📝 In playbook |
| Bizzabo | REST API | 📝 In playbook |
| Cvent | Playwright | 📝 In playbook |
| Eventbrite | Public API | 📝 In playbook |

### Battle-Tested
- ✅ Expo West 2026: 3,144 exhibitors
- ✅ Winter FancyFaire 2026: 1,035 exhibitors

### Features
- ✅ Auto API discovery (Playwright network interception)
- ✅ Token rotation (SmallWorldLabs)
- ✅ GraphQL with persisted queries (Swapcard)
- ✅ Threaded detail page enrichment
- ✅ Business services filtering
- ✅ CSV/Excel export
- ✅ Rate limiting

---

## 🔐 **Security Updates (2026-02-18)**

### PostgreSQL Passwords Changed
| Database | New Password |
|----------|---------------|
| swarm_pg | `kv0xMkzdz6vp9SsByuSc1BmSehmvOfoF` |
| pgvector | `hJfVIpVaoJA85dVhEZxivRKG4mXtbSjL` |

### Security Status
- ✅ No public port exposure (internal Docker network only)
- ✅ SSH brute force attack blocked: 14.211.253.127
- ✅ PostgreSQL restarted securely

---

## 📁 **Git Repository (2026-02-19)**

### Working Repository
- **URL:** https://github.com/arosstale/pi-mono-workspace
- **Status:** Public & Working
- **Remote:** origin (configured)
- **Commits:** 4 commits pushed

---

## 🌐 **browser-use Skill (2026-02-19)**

### Natural Language Browser Automation

No Playwright scripts needed - just describe what you want in plain English.

**Location:** `~/pi-mono-workspace/skills/browser-use/`

### Files
- `SKILL.md` - Complete skill documentation
- `README.md` - Quick start guide
- `EXAMPLES.md` - Ready-to-use prompt examples

### Why It Matters

| Traditional | browser-use |
|-------------|--------------|
| Hours of coding | Minutes |
| Fragile (breaks on updates) | Adapts to changes |
| Debug DOM selectors | Natural language |
| Requires coding skill | Anyone can use |

### Example

Instead of this:
```javascript
await page.goto('https://reddit.com/r/openclaw');
await page.click('[data-click-id="text"]');
// ... more Playwright code
```

Just say:
> "Go to r/openclaw on Reddit and extract the title, author, and upvote count from the top post"

### Use Cases

- **Lead Generation** - Scrape trade show directories
- **Job Hunting** - Aggregate job postings
- **Price Monitoring** - Compare competitor prices
- **Market Research** - Extract product info
- **Testing** - Walk through user flows

---

*Last updated: 2026-02-19*
