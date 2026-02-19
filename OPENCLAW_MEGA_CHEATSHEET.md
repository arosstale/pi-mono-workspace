# OpenClaw Mega Cheatsheet 2026 - Complete CLI Reference & Developer Guide

---

## Quick Start & Installation

### Global Install
```bash
npm install -g openclaw@latest
```

### Onboarding

1. Guided Setup
```bash
openclaw onboard --install-daemon
```

2. Channel Link
```bash
openclaw channels login
```

3. Start Gateway
```bash
openclaw gateway --port 18789
```

### Onboard Flags

- `--mode local` - Local gateway mode
- `--mode remote` - Connect to remote gateway
- `--flow quickstart` - Minimal setup
- `--skip-channels` - Skip channel setup

---

## Channel Setup

| Channel | Method | Command |
|---------|--------|--------|
| 📱 WhatsApp | QR Scan | `openclaw channels login` |
| ✈️ Telegram | Bot Token | `channels add --channel telegram --token $TOKEN` |
| 🎮 Discord | Bot Token | `channels add --channel discord --token $TOKEN` |
| 💬 iMessage | macOS Native | macOS bridge |
| 🏢 Slack | Bot Token | `channels add --channel slack` |
| 💬 Google Chat | Service Account | `channels add --channel googlechat` |
| 🔒 Signal | Linked Device | `channels add --channel signal` |
| 📎 MS Teams | Bot Registration | `channels add --channel msteams` |

### Quick Diagnostics

```bash
# Status
openclaw channels status --probe

# Logs
openclaw channels logs --channel [id]
```

---

## Workspace Files

| File | Purpose |
|------|---------|
| 🤖 `AGENTS.md` | Operating instructions for agent |
| ✨ `SOUL.md` | Persona, tone, boundaries |
| 👤 `USER.md` | User info & preferences |
| 🆔 `IDENTITY.md` | Agent name, emoji, theme |
| 🧠 `MEMORY.md` | Curated long-term memory (DM only) |
| 📅 `memory/YYYY-MM-DD.md` | Daily append-only log |
| 🔧 `TOOLS.md` | Local tool notes |
| 💓 `HEARTBEAT.md` | Heartbeat checklist |
| 🚀 `BOOT.md` | Startup checklist |

⚠️ **Root:** `~/.openclaw/workspace`

---

## Memory System

### Daily Logs
`memory/YYYY-MM-DD.md`
- Append-only
- Read today + yesterday at session start

### Long-Term Memory
`MEMORY.md`
- Curated facts
- Only loaded in main DM session

### Vector Search
```bash
memory_search tool
# Semantic search over memory chunks (~400 tokens)
```

### Providers
`memorySearch.provider`
- Auto-select: local GGUF → OpenAI → Gemini → Voyage

### QMD Backend
```yaml
memory.backend = "qmd"
# BM25 + vectors + reranking (experimental)
```

### Hybrid Search
- 0.7/0.3 default weights
- Vector similarity + BM25 keyword relevance

```bash
openclaw memory index --all
openclaw memory search "X"
```

---

## Models & Auth

```bash
openclaw models list --all               # View all available models
openclaw models set <model>              # Set agents.defaults.model.primary
openclaw models set-image <model>        # Set default image model
openclaw models fallbacks add <model>    # Add to fallback chain
openclaw models auth setup-token         # Preferred Anthropic auth (setup-token)
openclaw models auth add --provider <p>   # Add provider API key
openclaw models status --probe           # Live probe configured auth profiles
openclaw models aliases add <a> <m>      # Create model alias
```

### Failover & Cooldowns

- 1 min
- 5 min
- 1 hour

---

## Sessions

```yaml
session.dmScope          # main (default) | per-peer | per-channel-peer | per-account-channel-peer
session.reset.mode       # daily (default, 4am local) | idle
session.reset.idleMinutes  # Sliding idle window (whichever expires first wins)
session.resetByType      # Override policy for dm, group, thread sessions
session.resetByChannel   # Per-channel override (takes precedence)
session.identityLinks    # Map provider:id → canonical identity for cross-channel
session.sendPolicy       # Block delivery for specific session types
session.store            # ~/.openclaw/agents/{agentId}/sessions/sessions.json
```

⚠️ **SECURITY:** Use `per-channel-peer` for multi-user inboxes to prevent context leakage.

---

## Slash Commands

| Command | Description |
|---------|-------------|
| `/status` | Session health + context usage + WhatsApp cred status |
| `/context list` | What's in context window (biggest contributors) |
| `/context detail` | Full system prompt + injected workspace files |
| `/model <model>` | Switch model for this session (or `/model list`) |
| `/compact [instructions]` | Summarize older context, free up window space |
| `/new [model]` | Start fresh session (optional: set model) |
| `/reset` | Alias for `/new` |
| `/stop` | Abort current run + clear queued followups |
| `/send on|off|inherit` | Override delivery for this session |
| `/tts on|off` | Toggle text-to-speech |
| `/think`|`/verbose` | Toggle reasoning/verbose mode |
| `/config` | Persisted config changes |
| `/debug` | Runtime-only config overrides (requires `commands.debug: true`) |

---

## Text-to-Speech

| Provider | Type | Description |
|-----------|------|-------------|
| ElevenLabs | Premium | Ultra-realistic, higher latency |
| OpenAI | Standard | Fast, high-quality voices |
| Edge TTS | Free | No API key, multi-language support |

### Enable Auto-TTS

```yaml
messages.tts.auto: "always"
```

---

## Logging & Diagnostics

```bash
openclaw logs --follow                    # Tail Gateway file logs (colorized in TTY)
openclaw logs --json                      # Line-delimited JSON (one event per line)
openclaw logs --limit 200                 # Limit number of log lines
openclaw channels logs --channel whatsapp   # Channel-specific logs
```

### OTel Export Config

```yaml
"diagnostics": {
  "otel": {
    "enabled": true
  }
}
```

---

## Browser & Cron

### Browser Ops

```bash
openclaw browser start|stop               # Start/stop headless instance
openclaw browser tabs                     # List all open pages
openclaw browser open <url>               # Open URL in new tab
openclaw browser screenshot                # Capture active view
openclaw browser navigate <url>           # Navigate current tab
openclaw browser click|type|press         # DOM interactions
openclaw browser evaluate <js>            # Run JavaScript in page
openclaw browser pdf                     # Export page as PDF
```

### Cron Jobs

```bash
openclaw cron list                        # View scheduled jobs
openclaw cron add                         # Create new scheduled job
openclaw cron edit <id>                   # Edit existing job
openclaw cron enable|disable <id>         # Toggle job
openclaw cron run <id>                    # Manual trigger
openclaw cron runs                        # View run history
```

---

## Hooks & Automation

### Bundled Hooks

| Name | Type | Description |
|------|------|-------------|
| 💾 `session-memory` | `command:new` | Save session context to memory on `/new` |
| 📝 `command-logger` | `command` | Log all commands to audit file |
| 🚀 `boot-md` | `gateway:startup` | Run BOOT.md on gateway start |
| 😈 `soul-evil` | `agent:bootstrap` | Swap SOUL.md during purge window |

```bash
openclaw hooks list                       # List all discovered hooks
openclaw hooks enable <name>              # Enable a hook
openclaw hooks disable <name>             # Disable a hook
openclaw hooks info <name>                # Show hook details
openclaw hooks check                      # Check eligibility
```

### Event Types

- `command:new` - When `/new` is issued
- `command:reset` - When `/reset` is issued
- `command:stop` - When `/stop` is issued
- `gateway:startup` - After channels start
- `agent:bootstrap` - Before workspace files injected

---

## Skills System

### Skill Precedence

1. **<workspace>/skills/** - Per-agent, highest precedence
2. **~/.openclaw/skills/** - Managed/local, shared across workspaces
3. **Bundled skills** - Shipped with OpenClaw (lowest)

### ClawHub Registry

```bash
clawhub install <slug>   # Install skill from ClawHub
clawhub update --all      # Update all installed skills
clawhub sync --all        # Scan and publish updates
```

### SKILL.md Format

```yaml
---
name: my-skill
description: "What this skill does"
metadata: {
  "openclaw": {
    "requires": {...}
  }
}
---
```

---

## Multi-Agent Routing

### Isolated Workspaces
- Each agent has own `AGENTS.md`, `SOUL.md`, `USER.md`
- Per-Agent Auth
- Separate auth profiles per agent `Dir`
- Session Store
- Chat history under `~/.openclaw/agents/<id>/sessions`

### Bindings
Route messages by channel, accountId, peer

### Routing Precedence

1. **peer** (exact DM/group id) - Highest precedence
2. **guildId** (Discord) - Guild-level routing
3. **teamId** (Slack) - Team-level routing
4. **accountId** - Account-level routing
5. **channel** - Channel-wide fallback
6. **default agent** - Final fallback

```bash
openclaw agents add <name>
openclaw agents list --bindings
```

---

## Heartbeat System

```yaml
heartbeat.every          # Interval (default: 30m, 1h for Anthropic OAuth)
heartbeat.target        # last | none | <channel id>
heartbeat.to           # Optional recipient override
heartbeat.model        # Model override for heartbeat runs
heartbeat.prompt       # Custom prompt body
heartbeat.activeHours  # Restrict to time window (start/end/timezone)
```

⚠️ **CONTRACT:** Reply `HEARTBEAT_OK` if nothing needs attention. Agent strips and drops OK-only replies.

### HEARTBEAT.md Example

```markdown
# Heartbeat checklist
- Quick scan: anything urgent?
- Daytime: lightweight check-in
- Blocked? Note what's missing
```

---

## Sandboxing

```yaml
sandbox.mode          # "off" (no sandboxing), "non-main" (default), "all"
sandbox.scope        # "session" (default), "agent", "shared"
workspaceAccess      # "none" (default), "ro", "rw"
```

### sandbox.mode

- `"off"` - No sandboxing, tools run on host
- `"non-main"` - Sandbox only non-main sessions (default)
- `"all"` - Every session runs in sandbox

### sandbox.scope

- `"session"` - One container per session (default)
- `"agent"` - One container per agent
- `"shared"` - One container for all sandboxed sessions

### workspaceAccess

- `"none"` - Tools see sandbox workspace only (default)
- `"ro"` - Read-only mount at `/agent`
- `"rw"` - Read/write mount at `/workspace`

### Setup Image

```bash
scripts/sandbox-setup.sh
# Default image: openclaw-sandbox:bookworm-slim
```

---

## Sub-Agents

- **Parallel Work** - Run research/long tasks without blocking
- **Session Isolation** - Own session key + optional sandbox
- **Auto-Announce** - Results posted to requester chat channel
- **Auto-Archive** - Sessions archived after 60m (configurable)

```bash
/subagents list                       # List active sub-agents
/subagents stop <id|#|all>            # Stop sub-agent runs
/subagents log <id|#>                 # View sub-agent logs
/subagents info <id|#>                # Show run metadata
/subagents send <id|#> <msg>          # Send message to sub-agent
```

### sessions_spawn Tool

```json
{
  "task",
  "label?",
  "model?",
  "thinking?",
  "runTimeoutSeconds?",
  "cleanup?"
}
```

Returns:
```json
{
  "status",
  "runId",
  "childSessionKey"
}
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| No DM Reply | `openclaw pairing list` → approve pending requests |
| Silent in Group | Check `mentionPatterns` config (agent needs @mention) |
| Auth Expired | `openclaw models auth setup-token --provider anthropic` |
| Gateway Down | `openclaw doctor --deep` (scans for extra installs) |
| Memory Not Indexing | `openclaw memory index` (reindex memory files) |
| Context Full | `/compact` or `/new` (start fresh session) |
| Channel Disconnected | `openclaw channels status --probe` |
| Session Issues | `openclaw reset --scope sessions` |

### Universal Fix Command

```bash
openclaw doctor --deep --yes
```

Health checks + quick fixes + system service scans.

---

## Key Paths

| Path | Description |
|------|-------------|
| `~/.openclaw/openclaw.json` | Main configuration file |
| `~/.openclaw/workspace/` | Default agent workspace |
| `~/.openclaw/agents/<id>/` | Per-agent state directory |
| `~/.openclaw/agents/<id>/sessions/` | Session store + transcripts |
| `~/.openclaw/credentials/` | OAuth/API keys |
| `~/.openclaw/memory/<agentId>.sqlite` | Vector index store |
| `/tmp/openclaw/openclaw-YYYY-MM-DD.log` | Gateway log file |

> **Tip:** Use `--dev` or `--profile <name>` to isolate state under different directories.

---

## Model Aliases

| Alias | Model |
|-------|--------|
| `cerebras` | `cerebras/gpt-oss-120b` |
| `cerebras-glm` | `cerebras/zai-glm-4.7` |
| `cerebras-llama` | `cerebras/llama-3.3-70b` |
| `cerebras-qwen` | `cerebras/qwen-3-235b-a22b-instruct-2507` |
| `cerebras-qwen32` | `cerebras/qwen-3-32b` |
| `flash` | `zai/glm-4.5-air` |
| `gemini` | `google-gemini-cli/gemini-3-flash` |
| `gemini-pro` | `google-gemini-cli/gemini-3-pro` |
| `glm` | `zai/glm-4.7` |
| `glm5` | `zai/glm-4.5` |
| `glm6` | `zai/glm-4.6` |
| `groq` | `groq/openai/gpt-oss-120b` |
| `groq-8b` | `groq/llama-3.1-8b-instant` |
| `groq-gpt20` | `groq/openai/gpt-oss-20b` |
| `groq-kimi` | `groq/moonshotai/kimi-k2-instruct` |
| `groq-llama` | `groq/llama-3.3-70b-versatile` |
| `groq-qwen` | `groq/qwen/qwen3-32b` |
| `groq-scout` | `groq/meta-llama/llama-4-scout-17b-16e-instruct` |
| `minimax` | `minimax/MiniMax-M2.5` |
| `opus` | `anthropic/claude-opus-4-5` |
| `zen-glm` | `opencode-zen/glm-4.7-free` |
| `zen-kimi` | `opencode-zen/kimi-k2.5-free` |
| `zen-minimax` | `opencode-zen/minimax-m2.5-free` |
| `zen-trinity` | `opencode-zen/trinity-large-preview-free` |

---

*Source: https://moltfounders.com/openclaw-mega-cheatsheet*
*Cloned: 2026-02-19*
