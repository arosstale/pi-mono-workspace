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

---

## AgentOS Expansion (2026-02-26)

**Architecting AgentOS: From Token-Level to Emergent System-Level Intelligence**

Research Source: "Architecture AGENTOS: From Token-Level Context to Emergent System-Level Intelligence" by ChengYou LI, XiaoDong Liu, XiangBao Meng, XinYu Zhao (Yishu Research, Fukuoka Institute, National University of Singapore)

**AgentOS Primitives (OpenClaw Implementation):**

1. **Process Management (30-120 Days)**
   - Agent lifecycle: spawn, monitor, kill, auto-restart
   - Resource constraints: token limits, CPU, memory, timeout
   - Failure recovery: auto-restart, crash handling

2. **Memory Systems (Next 30 Days)**
   - Context windows, long-term memory, knowledge retrieval
   - Cross-agent shared memory
   - Token-aware compression (preserve reasoning, prune noise)

3. **Communication / IPC (30-60 Days)**
   - Message passing between agents
   - Pub/Sub patterns, negotiation protocols
   - Event-driven architecture

4. **Scheduling & Execution (60-120 Days)**
   - Multi-agent coordination, priority queuing
   - Task queues: urgency, budget, cost models
   - Multi-agent parallelism, load balancing

5. **Tool Access (In Progress)**
   - Permission systems, sandboxing
   - Role-based permissions (multi-user)
   - Tool discoverability

**Why AgentOS Matters:**

- Not just a platform (collection of features) → Not a product (acquired/cloned) → BUT AgentOS (manages agent lives)
- Competitive vs AutoGen/LangGraph: Community-owned, multi-provider LLM, white-label, real-time coordination
- Thesis: We're the OS that manages autonomous agents. Can't acquire 100 contributors. Can't kill kernel.

**AgentOS vs. AutoGen/LangGraph:**

| Feature | OpenClaw AgentOS | AutoGen | LangGraph |
|---------|-----------------|---------|-----------|
| Multi-Provider LLM | 100+ providers | Claude-only | Multi-provider support |
| Messenger Layer | Native (Telegram/Discord/Slack/WhatsApp) | External | External |
| Memory System | MSAM (semantic+episodic+procedural) | Local | LangChain memory |
| Agent Lifecycle | Roadmap (30-120d) | Yes | Yes |
| Communication IPC | Roadmap (30-60d) | Yes | Yes |
| Real-time Coordination | Roadmap (60-90d) | Yes | Yes |
| Community-Owned | 100 contributors, impossible to kill | Microsoft owned | LangChain owned |
| White-Label | $299/mo, brandable | No | No |

**AgentOS Architecture Committed:**
- Repo: `kelsey-hightowel-platform/AgentOS_Architecture.md`
- Commit: `564c5ad feat(agentos)`
- GitHub: https://github.com/arosstale/kelsey-hightowel-platform

---

## Platform Strategy (2026-02-26)

**The Linux Play — Multi-Provider vs. Lock-In:**

- **Narrative:** OpenClaw is the platform that runs everything (100+ providers), not a product locked into one vendor
- **Risk:** Not acquisition — irrelevance. If DX gets so good nobody uses the open alternative, community dies
- **Community ownership:** 100 contributors, 4000+ PRs, impossible to acquire/kill
- **Position:** Infrastructure layer, not product. Platform engineer Kelsey Hightowel leads platform team

**Deliverables Built:**

1. **Manifesto:** The_Linux_Play_Manifesto.md
   - Acquisition game: indie tools → labs clone → startups die
   - OpenClaw exception: run everything, community-owned
   - Mission: Build moats, make OpenClaw indispensable

2. **Landing Page:** Run_Everything copy
   - Agencies: "Run everything, not just one. Your agents are safer."
   - Enterprises: "Infra that scales, not a product to acquire."
   - Pricing: Free, Professional ($299/mo), Enterprise (custom) tiers

3. **Sales Framework:** Multi-Provider vs. Lock-In
   - Email sequences for agencies (3-step pipeline)
   - LinkedIn posts for lead generation
   - Closing script: Platform vs. Product distinction
   - Objection handling: lock-in, security, pricing

4. **Platform Expansion:** White-Label + Enterprise Ready
   - Roadmap: Multi-user (30d), White-label (60d), SSO (90d), On-prem (120d)
   - Security & compliance: GDPR, SOC 2, ISO 27001
   - Enterprise pitch + objection handling

**Repo Status:** Local git repo at `~/pi-mono-workspace/toplevel/strategy/platform-engineer-kelsey-hightowel/`. GitHub repo not created yet — awaiting user to paste URL for push.

**Next Steps for Launch:**
1. Create private GitHub repo for platform strategy
2. Implement Phase 1: Multi-User Permissions (30 days)
3. Build Phase 2: White-Label branding (60 days)
4. Release Phase 3: SSO integration (90 days)
5. Launch Enterprise tier with SLA and custom pricing

**Core Thesis:** We're not the product. We're the platform that makes LLMs work together. Can't kill 100 contributors. We're the Linux playbook: be the infrastructure, not the tool.
