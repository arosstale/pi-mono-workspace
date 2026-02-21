
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

## 🤖 **Agentic Engineering (2026-02-19)**

### Key Insights from "Forging a Workflow: Agentic Engineering in Practice"

**Source:** Martin Gratzer - Article on shifting from manual coding to agentic workflows

### From Assistant to Agent

**The Real Shift:**
Stop using AI for one-off prompts → Start encoding team conventions into reusable "skills"

**Key Principle:**
- Agent is only as effective as the workflow and codebase it's given to work within
- Structure amplifies capability

### The "Colorburst" Experiment

**What:**
AI-powered coloring page generator (planning → production)

**Finding:**
Agents excel when project has:
- ✅ Well-defined structure
- ✅ Clear documentation to ground them

### Process as a Tool, Not a Tax

**Traditional Overhead:**
- Tickets
- PR templates
- Changelogs

**Agentic Engineering:**
- Automates these tasks
- Ensures high-quality documentation and testing maintained effortlessly

### The "Forge" Workflow

**Open-standard skills for project pipeline:**

1. **Setting Foundations** - Project structure, conventions
2. **Planning** - Requirements, architecture
3. **Implementing** - Coding with patterns
4. **Self-Reviewing** - Code quality, testing
5. **Documenting** - Auto-generated docs

### Human's Evolving Role

**From:** Writing code manually
**To:**
- High-level architecture
- Orchestration
- Quality gate (Pull Request)

### Why PRs Remain Essential

**Human Review Catches:**
- ✅ Cross-cutting concerns (security)
- ✅ Shared team knowledge
- ✅ Architectural alignment

### Application to OpenClaw ✅

**Completed:**

1. **TEAM_CONVENTIONS.md Created**
   - Coding conventions (file naming, style)
   - Project structure standards
   - Git workflow and PR templates
   - Error handling patterns
   - Security conventions
   - Quality gates

2. **Forge Workflow Skill Created**
   - `skills/forge-workflow/SKILL.md` (7.2KB)
   - `skills/forge-workflow/README.md` (3.4KB)
   - `skills/forge-workflow/EXAMPLES.md` (7.7KB)

### Forge Workflow: 5 Phases

1. **Setting Foundations** - Create project structure, SKILL.md
2. **Planning** - Define requirements, architecture
3. **Implementing** - Write code following conventions
4. **Self-Reviewing** - Quality check before commit
5. **Documenting** - Auto-generate docs (README, EXAMPLES.md)

### What We Have Now
- Skills system with SKILL.md files ✅
- Team conventions encoded ✅
- Forge workflow skill ready ✅
- Multiple agents (Rayan, trading, etc.) ✅
- Clear documentation (AGENTS.md, SOUL.md, USER.md, MEMORY.md) ✅
- Git-based workflow ✅

**Result:** Structure amplifies capability. Skills compound in value over time.

---

## 🔐 **Security - Singularity Attack Defense (2026-02-19)**

### What It Is

The "Singularity Attack" (prompt injection/jailbreaking) attempts to make AI systems break out of constraints and follow attacker-provided instructions.

### Defense Strategies

| Layer | Technique |
|--------|-----------|
| **1. Input Validation** | Check for override patterns |
| **2. Context Isolation** | Separate system vs user (delimiters) |
| **3. Capability Control** | Whitelist allowed actions |
| **4. Output Filtering** | Strip injected commands |
| **5. Human-in-the-Loop** | Destructive actions need approval |

### OpenClaw Defenses

| Mechanism | Status |
|------------|--------|
| External content delimiters | ✅ `<<<EXTERNAL_UNTRUSTED_CONTENT>>>` |
| Separated system/user context | ✅ Implemented |
| Destructive action blocking | ✅ Implemented |
| External request warnings | ✅ Implemented |

### Key Principles

1. **Never Trust User Text Implicitly** - Always validate
2. **Isolate System Instructions** - Use delimiters
3. **Require Explicit Privilege** - Dangerous actions need approval
4. **Log Security Events** - Track and learn
5. **Maintain Human-in-the-Loop** - Safety requires oversight

**Documentation:** `SINGULARITY_ATTACK_DEFENSE.md` (9.1KB)

---

## 🎯 **Lead Generator System (2026-02-19)**

### System Complete ✅

**Location:** `skills/lead-generator/`

**Built:**
- Complete lead generation system (5 phases)
- Scraping (trade shows, directories, browser)
- Enrichment (website, email, industry)
- Qualification (scoring 0-100, filtering)
- Storage (CSV, Excel, SQLite)
- Outreach (emails, LinkedIn templates)

**Files:**
- `SKILL.md` (13.8KB) - Complete documentation
- `README.md` (3.5KB) - Quick start
- `run.py` (14.8KB) - Main Python implementation
- `requirements.txt` - Python dependencies
- `config.json` - Configuration template

**Features:**
- Trade show scraping (SmallWorldLabs, Swapcard)
- Browser automation integration
- Lead qualification and scoring
- Multi-format output (CSV, Excel, DB)
- Outreach templates (intro, followup, LinkedIn)

**Architecture:**
```
Data Sources → Enrichment → Qualification → Storage → Outreach
```

---

---

## 🦀 **VibeClaw - Browser-Based OpenClaw (2026-02-21)**

### Overview
OpenClaw sandbox that runs entirely in your browser — no server, no Docker, no install required.

**Live:** https://vibeclaw-openclaw.netlify.app
**Local:** `~/pi-mono-workspace/vibeclaw/`
**GitHub:** https://github.com/arosstale/vibeclaw (forked from jasonkneen/vibeclaw)

### Features
- 🌐 **Sandbox Mode** - Boot OpenClaw agents directly in browser (almostnode runtime)
- 🔴 **Live Gateway** - Connect to your running OpenClaw instance via WebSocket
- 🎨 **6 Flavours** - Swap personalities (OpenClaw, TinyClaw, ShipIt, R00t, Pixie, Professor)
- 📊 **Full Dashboard** - Sessions, agents, files, skills, cron jobs, metrics, logs
- 🔌 **8 Netlify Functions** - `/api/chat`, `/api/articles`, `/api/gateway-live`, etc.

### Flavours Available
| Emoji | Name | Focus | Agents | Skills |
|-------|------|-------|--------|--------|
| 🦀 | OpenClaw | Coding assistant | 4 | 3 |
| 🦞 | TinyClaw | Multi-agent orchestrator | 5 | 4 |
| 🚀 | ShipIt | DevOps | 5 | 5 |
| 💀 | R00t | Security/pen-testing | 5 | 5 |
| ✨ | Pixie | Creative studio | 5 | 5 |
| 🎓 | Professor | Education | 4 | 4 |

### Deployment
- **Platform:** Netlify (Free plan)
- **Account:** Fdsa (arosstale)
- **Build:** Vite + Netlify Functions
- **Auto-deploy:** Manual (via `netlify deploy --prod`)

### Update Commands
```bash
# Build and deploy
cd ~/pi-mono-workspace/vibeclaw
npm run flavours:build && npm run build
NETLIFY_AUTH_TOKEN="nfp_rCyYJ4CycbXAPb1zQzLDT3gnn9zQEiuB6edf" netlify deploy --prod --dir=dist-site --functions=netlify/functions
```

### Netlify API
- **Site ID:** 81c6fa40-191a-4df7-a61b-afd36232a5ac
- **Admin URL:** https://app.netlify.com/projects/vibeclaw-openclaw
- **Build Logs:** https://app.netlify.com/projects/vibeclaw-openclaw/deploys
- **Function Logs:** https://app.netlify.com/projects/vibeclaw-openclaw/functions

### Skills Repository
- **Location:** `~/pi-mono-workspace/awesome-openclaw-skills/`
- **GitHub:** https://github.com/VoltAgent/awesome-openclaw-skills
- **Skills:** 3,002 curated skills (30+ categories)
- **Excluded:** Spam, crypto, duplicates, flagged malicious content

### Top Skill Categories
- 🤖 AI & LLMs (287)
- 🔍 Search & Research (253)
- ⚙️ DevOps & Cloud (212)
- 🌐 Web & Frontend (202)
- 🛒 Marketing & Sales (143)
- 💻 Coding Agents (133)
- 🌍 Browser & Automation (139)

### Security Sanitization (2026-02-21)
**Status:** ✅ Completed and Deployed
**Fork:** https://github.com/arosstale/awesome-openclaw-skills

**Scan Results:**
- **Total Skills:** 3,020
- **Suspicious:** 9 (0.3%)
- **Removed (High Risk):** 4 skills
- **Flagged (Medium Risk):** 5 skills
- **Clean:** 3,011 skills (99.87%)

**High-Risk Skills Removed:**
1. camoufox - Anti-detect browser automation
2. stealthy-auto-browse - Evades bot detection
3. aluvia-web-proxy - Bypass CAPTCHAs
4. aluvia-web-unblock - Bypass CAPTCHAs

**Sanitization Files:**
- `SANITIZATION_REPORT.md` - Full security report
- `SUSPICIOUS_SKILLS.json` - Detailed skill analysis
- `README_CLEAN.md` - Sanitized skill list
- `sanitize.py` - Basic sanitization script
- `comprehensive_sanitize.py` - Full scanner
- `full_sanitize.py` - Creates clean README

**Original Exclusions (by curator):**
- Spam/bulk accounts: 1,180
- Crypto/blockchain: 672
- Duplicates: 492
- Malicious (audited): 396
- Non-English: 8

**Total Filtered:** 2,748 skills excluded from original 5,705

---

## 🔒 **GitHub OpenClaw Skills - Full Security Scan (2026-02-21)**

### Scan Results
- **Total Skills Analyzed:** 8,221
- **Suspicious:** 4 (0.05%)
- **Clean:** 8,217 (99.95%)
- **Critical/High Risk:** 0 (0.00%)

### Suspicious Skills (Medium Risk)
All are "stealth browser" skills that evade bot detection:

| Skill | Path | URL |
|-------|------|-----|
| b0tresch-stealth-browser | skills/b0tresch/b0tresch-stealth-browser | [View](https://github.com/openclaw/skills/tree/main/skills/b0tresch/b0tresch-stealth-browser) |
| camoufox-stealth-browser | skills/kesslerio/camoufox-stealth-browser | [View](https://github.com/openclaw/skills/tree/main/skills/kesslerio/camoufox-stealth-browser) |
| kesslerio-stealth-browser | skills/kesslerio/kesslerio-stealth-browser | [View](https://github.com/openclaw/skills/tree/main/skills/kesslerio/kesslerio-stealth-browser) |
| stealth-browser | skills/mayuqi-crypto/stealth-browser | [View](https://github.com/openclaw/skills/tree/main/skills/mayuqi-crypto/stealth-browser) |

### Files Created
- `GITHUB_SECURITY_REPORT.md` - Full security report
- `GITHUB_REFINED_SCAN_REPORT.json` - JSON report with all skills
- `GITHUB_SUSPICIOUS_REFINED.json` - Suspicious skills list
- `GITHUB_TREE_FULL.json` - Raw GitHub tree data (67,647 entries)
- `refined_scan.py` - Python scanner script

### Location
- `~/pi-mono-workspace/awesome-openclaw-skills/`

### Key Finding
The OpenClaw skills repository is **overwhelmingly safe** with 99.95% clean rate. Only 4 stealth browser skills (0.05%) require security review before use.

---

*Last updated: 2026-02-21*
