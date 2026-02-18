
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
