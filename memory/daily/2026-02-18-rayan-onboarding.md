# 2026-02-18 - N-Art CEO Onboarding: Rayan

---

## 👤 New User: Rayan - CEO & Founder of N-Art

**Status:** Active Setup
**Telegram ID:** 5264265623
**Pairing Code:** Z8Q4M2UQ
**Email:** rayan@n-art.io

---

## Actions Completed

1. ✅ **Updated MEMORY.md**
   - Added Rayan as CEO & Founder of N-Art
   - Updated contact information

2. ✅ **Updated USER.md**
   - Added Rayan to N-Art section
   - Documented CEO role

3. ✅ **Created User Configuration**
   - File: `/home/majinbu/pi-mono-workspace/n-art/RAYAN_USER_CONFIG.md`
   - Full access permissions documented
   - Trading configuration specified
   - API key setup guide included

---

## Access Details

### Telegram Pairing (Pending)
- **Pairing Code:** Z8Q4M2UQ
- **Command to approve:** `openclaw pairing approve telegram Z8Q4M2UQ`
- **Status:** Waiting for bot owner approval

### Trading System Access
- **Role:** Full Admin
- **Permissions:** View, Execute, Modify, Reports, API Keys, Dashboard, Alerts
- **Risk Tolerance:** Medium-High
- **Max Position:** 5% portfolio per trade
- **Stop Loss:** -2%
- **Take Profit:** +5%
- **Daily Loss Limit:** -$5,000
- **Daily Profit Target:** +$10,000

---

## What Rayan Can Do

### Trading
- ✅ View all trading strategies
- ✅ Execute trades (with confirmation)
- ✅ Modify strategy parameters
- ✅ View performance reports
- ✅ Manage API keys
- ✅ Access real-time dashboard
- ✅ Configure alerts/notifications

### AI Agents
- ✅ SuperQuant: Full control
- ✅ Nano-Agent: Full control
- ✅ AutoMaker: Full control
- ✅ Borg Memory: Read/Write

### Database
- ✅ swarm_pg: Read/Write
- ✅ pgvector: Read/Write
- ✅ Analytics: Read only

---

## Dashboard URLs

- **Automaker UI:** http://144.76.30.176:3007
- **Grafana:** http://144.76.30.176:3002
- **N-Art Sales:** https://n-art-sales.netlify.app

---

## Quick Commands

```bash
# Check trading status
docker ps | grep -E "superquant|nano-agent|automaker"

# Check recent trades
docker logs superquant --tail 50

# View performance
cd ~/hl-trading-agent-private/hl-trading-agent
python check_position.py

# Restart bot
docker restart superquant
```

---

## Next Steps

1. **Approve Telegram Pairing**
   ```bash
   openclaw pairing approve telegram Z8Q4M2UQ
   ```

2. **Rayan to Complete:**
   - [ ] Set dashboard password
   - [ ] Configure exchange API keys
   - [ ] Enable 2FA
   - [ ] Review trading configuration
   - [ ] Execute first test trade

---

## Support

- **Technical:** Alessandro (Majinbu) - majinbu@openclaw.ai
- **WhatsApp:** +39 329 348 4956
- **Telegram:** Direct message

---

**Created:** 2026-02-18 20:45 UTC
**Status:** Rayan configured, pending Telegram approval
