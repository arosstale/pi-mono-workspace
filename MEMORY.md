## System Status (2026-02-26)

| Metric | Value |
|--------|-------|
| Disk | 48% (healthy) |
| OpenClaw | 2026.2.25 |
| Pi-mono | v0.55.1 (pi-claw synced) |
| Primary Model | opencode-zen/glm-4.7 (free) |
| Node | v24.13.1 |
| Python | 3.10.12 |
| Bun | 1.3.7 |

### Running Services
- OpenClaw Gateway (PID active, port 18789)
- CF Tunnel → https://openclaw.fdsa.agency/
- Channels: Telegram ✅ Discord ✅ Slack ✅ WhatsApp ✅
- 27 paper trading strategies (systemd)
- SuperQuant (systemd)

### Model Providers (openclaw)
| Provider | Status | Models |
|---|---|---|
| opencode-zen | ✅ PRIMARY (free) | GLM 4.7/5, MiniMax M2.5, Kimi K2.5, Gemini 3 Flash/Pro |
| cerebras | ✅ fallback (free) | GPT-OSS 120B, GLM 4.7, Qwen3 235B |
| groq | ✅ fallback (free) | Llama 3.3 70B, Llama 3.1 8B |
| nvidia | ✅ paid | Kimi K2 Instruct/Thinking, DeepSeek V3.2, Seed OSS 36B |
| zai | ⚠️ empty balance | GLM 4.7, GLM 5 (recharge to restore) |
| gemini | ✅ OAuth | Gemini 2.5 Pro/Flash, 2.0 Flash |

---

## Team & Contacts

- **Owner:** Majinbu / Artale
- **Telegram:** @majinbu (ID: 8270920648)
- **Capital:** Artale $39.72 (Hyperliquid)

---

## MSAM Integration

- **Server:** http://127.0.0.1:3001/v1 (OpenAI-compatible)
- **Start:** `cd /home/majinbu/pi-mono-workspace && node msam-server.js`
- **Hook:** `/home/majinbu/.openclaw/hooks/msam-memory/` (ESM fixed 2026-02-26)

---

## Infrastructure

- **OpenClaw config:** `~/.openclaw/openclaw.json`
- **Gateway env:** `~/.openclaw/gateway.env` (channel tokens + GROQ_API_KEY)
- **CF Tunnel:** `~/.cloudflared/config.yml` (tunnel: f39b7ee1)
- **Pi-mono:** `/home/majinbu/organized/active-projects/pi-mono` (branch: pi-claw)
- **PAI:** `packages/pi-mono-pai/` (v2.0.0)
- **Loom:** `/home/majinbu/loom/` (v0.1.0, port 8080)
- **Workspace:** `/home/majinbu/pi-mono-workspace/`

---

## Active Paper Trading Strategies
- MegaCombo (ETH, SOL, scalp, original)
- RBI suite (cluster-fader, divergence, dynamic-accel, vol-accel)
- Liquidation suite (cascade, parabolic, stochastic, regime, rsi-accel, bbpctb, donchian)
- Signal strategies (composite-signal, funding-regime, hlp-flip, mean-reversion, smart-divergence, volume-profile, vpin-fade)
- Elite (cluster-momentum, wallet-copybot)
- Monitors (large-trade-detector, whale-monitor, sltp-monitor, trading-health)

---

## Key Commands

```bash
# OpenClaw
openclaw gateway start
openclaw channels status
openclaw doctor

# Pi-mono sync
cd /home/majinbu/organized/active-projects/pi-mono
git fetch upstream && git merge upstream/main --no-edit

# Update openclaw
npm install -g openclaw@latest

# Disk check
df -h / | tail -1
```

---

## Wisdom
- ZAI credits drain fast — always have cerebras/groq as fallback
- openclaw config `models.providers.*` requires: `baseUrl` + `apiKey` + `models: [{id, name}]`
- gateway.env needs LLM API keys explicitly (not inherited from shell)
- MEMORY.md limit: 20,000 chars — keep trimmed
- `openclaw doctor --fix` removes unknown keys but can't fix missing required fields
- Discord/WhatsApp bots cannot initiate — user must message first
