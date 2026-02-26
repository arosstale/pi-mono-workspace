# Discord Lead Hunter — Launch Checklist

## ✅ What's Working

- Node.js v24.13.1
- Package.json configured
- All 4 skill files present and syntactically valid
- Heartbeat configuration written
- Guardrails defined in SOUL.md
- README.md with instructions

## ⏳ What You Need to Provide

### 1. Discord Bot Token

Get it from:
1. Go to Discord Developer Portal: https://discord.com/developers/applications
2. Create application → Bot
3. Copy the token
4. Add to `.env` file:
```bash
DISCORD_TOKEN=your_bot_token_here
```

### 2. Server IDs to Scan

Add 10 server IDs to `heartbeat.yaml`:

```yaml
workflow:
  - step: scan
    config:
      servers:
        - "Your-Server-ID-1"
        - "Your-Server-ID-2"
        - "Your-Server-ID-3"
        # ... add more (total 10 recommended)
      channels:
        - "looking-for-help"
        - "questions"
        - "help"
        - "support"
      keywords:
        - "looking for"
        - "need help with"
        - "agency"
        - "developer"
        - "agent"
      limit: 10
```

---

## 🔧 Steps for You to Run Locally (or on VPS)

```bash
# 1. Navigate to the project
cd discord-lead-hunter

# 2. Copy and edit .env
cp .env.example .env
nano .env  # Add your DISCORD_TOKEN

# 3. Edit heartbeat.yaml (add server IDs)
nano heartbeat.yaml

# 4. Install dependencies
npm install

# 5. Test a single scan run (optional)
npm run scan

# 6. Initialize the database (auto-creates)
node run.js

# 7. Start the heartbeat (continuous)
npm run heartbeat
```

---

## 📊 What Happens When Running

**Every 30 minutes, the system:**

1. **Scans** Discord servers for posts asking: "looking for help", "need agency/dev"
2. **Scores** users 0-1 on:
   - Budget mentioned (+0.3)
   - Payment ready (+0.2)
   - Urgency (+0.2)
   - Niche fit (+0.15)
   - Explicit ask (+0.1)
   - Looking for agency (+0.1)
3. **Saves** qualified leads (score > 0.6) to SQLite database
4. **Generates** contextual DMs referencing their problem
5. **Queues** DMs (max 3/day per user, 20/day total)
6. **Sends** DMs in batches (5 every 30 sec to rate limit)
7. **Hands over** to you when they say "Yes, I'm interested" or "Worth a call"

---

## 🛡 Guardrails in Place

- **Never** mass-DM random users
- **Never** cold-DM without an explicit ask for help
- **Never** send more than 3 DMs/day to the same user
- **Never** DM users who said "not interested" or "stop"
- **Never** ignore "stop" or "not interested"

If you break these, the system stops.

---

## 💰 Monetization Flow

1. **System finds** users asking for help
2. **System qualifies** them by budget/urgency
3. **System DMs** with contextual help
4. **User responds** positively → System hands over to you
5. **You close** → Users pay you

The system does the hunting. You do the closing.

---

## 🚫 What I Can't Do For You

- ❌ Access your Discord account to get the token
- ❌ Know which servers you want to scan
- ❌ Run the actual heartbeat without Discord token

---

## 🎯 Next Moves

**Option A: You're ready now**
1. Go to Discord → Create bot → Get token
2. Add token to `.env`
3. 10 server IDs → edit `heartbeat.yaml`
4. Run: `npm run heartbeat`
5. Monitor logs for 24h

**Option B: You want to test first**
1. Get token and server IDs
2. Add to `.env` and `heartbeat.yaml`
3. Run: `npm run build`
4. Run: `npm run heartbeat`
5. Check logs, adjust score threshold if too many/too few leads

---

**Your move:** give me Discord token + 10 server IDs, I'll validate the whole system is ready. Or you provide them and run locally.

Either way, I'm ready when you are.