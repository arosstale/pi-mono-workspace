# N-Art User Configuration - Rayan

---

## User Profile

- **Name:** Rayan
- **Role:** CEO & Founder
- **Company:** N-Art
- **Email:** rayan@n-art.io
- **Telegram ID:** 5264265623
- **Status:** Active
- **Created:** 2026-02-18

---

## Access Permissions

### OpenClaw Gateway
- **Status:** Pending approval
- **Pairing Code:** Z8Q4M2UQ
- **Telegram ID:** 5264265623
- **Command to approve:** `openclaw pairing approve telegram Z8Q4M2UQ`

### Trading System Access
- **Account:** rayan_nart
- **Role:** Full Admin
- **Permissions:**
  - ✅ View all trading strategies
  - ✅ Execute trades (with confirmation)
  - ✅ Modify strategy parameters
  - ✅ View performance reports
  - ✅ Manage API keys
  - ✅ Access real-time dashboard
  - ✅ Configure alerts/notifications
  - ❌ Cannot delete critical data (safety)

### Database Access
- **swarm_pg:** Read/Write (trading data)
- **pgvector:** Read/Write (memory/history)
- **Analytics:** Read only

---

## Trading Configuration

### Default Settings
- **Risk Tolerance:** Medium-High
- **Max Position Size:** 5% portfolio per trade
- **Stop Loss:** Automatic -2%
- **Take Profit:** Automatic +5%
- **Daily Loss Limit:** -$5,000
- **Daily Profit Target:** +$10,000

### AI Agent Permissions
- **SuperQuant:** Full control
- **Nano-Agent:** Full control
- **AutoMaker:** Full control
- **Borg Memory:** Read/Write

### Notification Settings
- **Telegram:** Enabled (all alerts)
- **Email:** Enabled (daily summary)
- **SMS:** Disabled

---

## API Keys Configuration

### Exchange API Keys
```bash
# Binance (if applicable)
RAYAN_BINANCE_API_KEY=XXXXXXXXXXXXXX
RAYAN_BINANCE_API_SECRET=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

# Other exchanges as needed
RAYAN_KRAKEN_API_KEY=XXXXXXXXXXXXXX
RAYAN_KRAKEN_API_SECRET=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
```

### OpenAI API (for AI agents)
```bash
RAYAN_OPENAI_API_KEY=sk-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
```

**Security:** All API keys stored in environment variables, never committed to git.

---

## SSH Access (if needed)

```bash
# SSH connection
ssh rayan@144.76.30.176

# Or via Majinbu's server with user switch
ssh majinbu@144.76.30.176
su - rayan
```

---

## Dashboard Access

### Web Interfaces
- **Automaker UI:** http://144.76.30.176:3007
- **Grafana:** http://144.76.30.176:3002 (if available)
- **N-Art Sales:** https://n-art-sales.netlify.app

### Authentication
- **Username:** rayan@n-art.io
- **Password:** (to be set on first login)
- **2FA:** Recommended (enable in settings)

---

## Quick Start Commands

### View Trading Status
```bash
docker ps | grep -E "superquant|nano-agent|automaker"
```

### Check Recent Trades
```bash
docker logs superquant --tail 50
```

### View Performance
```bash
cd ~/hl-trading-agent-private/hl-trading-agent
python check_position.py
```

### Restart Trading Bot
```bash
docker restart superquant
```

---

## Support & Contacts

### Technical Support
- **Primary:** Alessandro (Majinbu) - majinbu@openclaw.ai
- **WhatsApp:** +39 329 348 4956
- **Telegram:** Direct message

### Emergency Contacts
- **Server Issues:** Contact Alessandro immediately
- **Trading Issues:** Stop all bots first, then contact support
- **Security Issues:** Report immediately

---

## Onboarding Checklist

### Week 1
- [ ] Telegram pairing approved
- [ ] SSH access configured
- [ ] Dashboard access tested
- [ ] Trading system reviewed
- [ ] API keys configured
- [ ] Notification settings set

### Week 2
- [ ] Execute first test trade
- [ ] Review performance reports
- [ ] Configure alerts
- [ ] Set up daily monitoring routine

### Week 3-4
- [ ] Customize strategy parameters
- [ ] Enable additional agents (if needed)
- [ ] Set up backup/restore procedures
- [ ] Document personal workflows

---

## Notes

- Rayan has full admin access to N-Art trading systems
- All trades require confirmation until safety is established
- Daily loss limits in place for risk management
- 24/7 monitoring active on all trading bots
- Automatic alerts configured for all significant events

---

**Last Updated:** 2026-02-18
**Status:** Active - Pending Telegram approval
