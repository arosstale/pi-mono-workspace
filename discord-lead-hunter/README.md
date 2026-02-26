# Discord Lead Hunter Agent

**What it does:**
- Scans Discord servers for users asking for help/agency/dev
- Qualifies leads by fit/budget/urgency
- Sends contextual DMs
- Hands over to [Artale] when they're ready to close
- Never mass-DMs, never cold-contacts, respects stop signals

**What it doesn't do:**
- Cold DM random users
- Mass DM
- Ignore "stop" or "not interested"
- Pitch without solving their problem first

---

## Tech Stack

- TypeScript/Node.js
- Discord.js (`discord.js` library)
- SQLite (`better-sqlite3` for lead tracking)
- YAML (heartbeat configuration)

---

## Setup

```bash
# Clone or copy this directory
cd discord-lead-hunter

# Install dependencies
npm install

# Copy .env.example to .env
cp .env.example .env

# Edit .env with:
# - DISCORD_TOKEN=your_bot_token
# - OPENCLAW_API_KEY=your_openclaw_key
```

---

## Run the Agent

**Option 1: Test single run**
```bash
# Discover, score, save, queue, send
npx ts-node-scan  # Step-by-step through the pipeline
```

**Option 2: Enable heartbeat (continuous)**
```bash
# Start the heartbeat loop
npm run heartbeat
```

**This happens every 30 min:**
1. Scan 10 Discord servers
2. Score new leads (threshold: 0.6)
3. Save to SQLite database
4. Generate contextual DMs
5. Queue and send (respecting rate limits)

---

## Guardrails

- Max 3 DMs per day per user
- Max 20 DMs total per day
- Never DM users who didn't ask for help
- Stop immediately if they say "not interested"
- No mass DM, no cold outreach

---

## Data Flow

```
Discord Servers
  ↓
[scan-discord.ts] → Lead candidates
  ↓
[score-lead.ts] → Qualified leads (score > 0.6)
  ↓
[save-lead.ts] → SQLite DB (leads.db)
  ↓
[queue-outbound-dm.ts] → .data/outbox/
  ↓
[heartbeat.yaml] → Discord adapter drains and sends
  ↓
Handover to [Artale] when they're ready to buy
```

---

## Launch Checklist

- [ ] `.env` set with Discord token + OpenClaw key
- [ ] Dependencies installed
- [ ] Heartbeat configured (heartbeat.yaml)
- [ ] Database initialized (leads.db)
- [ ] AGENTS.md sets expectations (lead hunter identity)
- [ ] SOUL.md sets guardrails (tone, boundaries, anti-spam)
- [ ] Test single run: `npm run scan`
- [ ] Enable heartbeat: `npm run heartbeat`
- [ ] Verify: check leads.db, check .data/outbox/
- [ ] Add 10 Discord servers to config
- [ ] Monitor for 24 hours (check DM logs)
- [ ] Adjust guardrails if needed
- [ ] Scale to 20 servers when stable

---

## What You Need

**Discord:** Bot token
`.env` file set properly (don't hardcode keys)

**OpenClaw:** API key
Gateway running on port 18789

**10 Servers:** Add to `heartbeat.yaml` config
Start with:
- OpenClaw Discord
- AI research communities
- Developer help servers

---

## Monitoring

```bash
# Check leads status
cat leads.db  # Or use SQLite browser

# Check outbox
ls .data/outbox/

# Check heartbeat logs
tail -f logs/heartbeat.log
```

---

## If You Break Something

**Problem:** Rate limit from Discord
**Fix:** Reduce maxDMsPerDay in `heartbeat.yaml`

**Problem:** Leads are all garbage
**Fix:** Raise score threshold to 0.7

**Problem:** Handover not pinging you
**Fix:** Check triggers in `heartbeat.yaml`

**Problem:** Agent won't stop
**Fix:** Re-read SOUL.md → add "stop" triggers

---

## Support

This is a solo project. If it breaks, fix it.

---

**Built for:** Artale
**Purpose:** Automate lead-gen, help him close deals.
**Rule:** Never mass-DM. Never cold-contact. Always solve first.