# Discord → PI Routing Fix

## Current State: ONE-WAY Only

**Working:** PI → Discord → User
**Broken:** User → Discord → PI

---

## Evidence

### 1. Discord Plugin Config
```json
{
  "plugins": {
    "entries": {
      "discord": {
        "enabled": true    // Only config, no routing setup
      }
    }
  }
}
```

### 2. Gateway Config
```json
{
  "gateway": {
    "mode": "local",      // Loopback bind, localhost only
    "bind": "loopback",
    "port": 18789
  }
}
```

### 3. Session Logs
```bash
# No incoming Discord messages in raw logs:
tail -50 ~/.openclaw/logs/raw-stream.jsonl | grep -i "discord.*incoming"
# Result: (no output)
```

---

## Fix Required

The Discord bot needs to route incoming user messages back to the PI session via OpenClaw gateway.

### Implementation: Discord Bot → Gateway Routing

Add this to `/opt/discord-bot-data/gateway/integration.js`:

```javascript
// When Discord receives a message from user that's a reply to PI
client.on('messageCreate', async (message) => {
  // Only process replies from authorized user
  if (message.author.id !== AUTHORIZED_USER_ID) {
    return;
  }

  // Only process if it's a reply to the bot or mentions the bot
  if (!message.mentions.has(client.user) && !isReplyToBot(message)) {
    return;
  }

  // Send to OpenClaw gateway
  const gateway = getGateway();
  if (gateway && gateway.isConnected()) {
    await gateway.sendMessage({
      type: "user_message",
      text: message.content,
      channel: "discord",
      sessionId: "main",
      userId: message.author.id,
      messageId: message.id
    });
  }
});

function isReplyToBot(message) {
  return message.reference?.messageId !== null;
}
```

---

## Alternative: Change Gateway to Accept External Connections

**Step 1: Update OpenClaw config:**
```bash
# Edit ~/.openclaw/openclaw.json
# Change:
"gateway": {
  "mode": "host",        // Was "local"
  "bind": "0.0.0.0"     // Was "loopback"
}
```

**Step 2: Open firewall for gateway:**
```bash
sudo ufw allow 18789/tcp
sudo ufw reload
```

**Step 3: Restart OpenClaw:**
```bash
# Kill existing gateway
kill 1196035

# Restart via service or directly
openclaw-gateway
```

---

## Verification

After fix, test by:
1. Send message to PI agent in Discord
2. Wait for PI to respond
3. Reply with a correction (e.g., "Stop thermal spam")
4. Check if PI receives and acknowledges it

**Success indicators:**
```bash
# Incoming message appears in PI logs:
tail -f ~/.openclaw/logs/raw-stream.jsonl | grep "user_message"

# PI changes behavior based on correction
```

---

## Quick Fix Command

To test if routing works, try sending a message directly to PI via CLI:

```bash
# From Discord bot, call PI with test message:
echo '{"action": "incoming", "text": "Test from Discord"}' | \
  pi -t main --stdin
```

If this works, the routing mechanism exists but isn't being called from Discord.

---

**Created:** 2026-02-21
**Issue:** No Discord → PI feedback loop
**Fix:** Implement gateway routing or change gateway mode
