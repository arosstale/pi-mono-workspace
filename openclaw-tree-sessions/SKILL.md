---
name: tree-sessions
description: Tree-structured session history for OpenClaw. Branch conversations, merge contexts, visualize with D3.js, and manage multiple conversation paths.
version: 1.0.0
---

# OpenClaw Tree-Structured Sessions

Tree-structured session history for OpenClaw, inspired by pi's TUI tree but adapted for chat platforms (Telegram, WhatsApp, Discord).

## Features

- 🌳 **Branching**: Create branches from any message in the conversation
- 🔄 **Context Loading**: Load only the active branch into LLM context
- 🎨 **Visualization**: Interactive D3.js tree visualization
- 📊 **Export**: Export trees as JSON, HTML, or text
- 🔀 **Merge**: Merge branches back into main conversation
- 🗑️ **Delete**: Remove unwanted branches

## Quick Start

### Installation

```bash
cd /home/majinbu/pi-mono-workspace/openclaw-tree-sessions
npm install
npm run build
```

### Chat Commands

```
/fork [name]              - Create branch from replied message
/branches                  - List all active branches
/checkout <number>         - Switch to branch
/merge <number>            - Merge branch into current
/delete-branch <number>    - Delete a branch
/tree [format]            - Export tree (json, html, text)
```

## How It Works

### JSONL Format

Each message is stored with metadata:

```json
{
  "id": "msg_a1b2c3d4",
  "parentId": "msg_x9y8z7w6",
  "role": "user",
  "content": "Hello",
  "timestamp": "2026-02-25T12:00:00.000Z",
  "branchId": "branch_explore_oauth",
  "externalId": "telegram-msg-123"
}
```

### Context Loading

1. Start at `activeLeafId`
2. Walk backward via `parentId` chain
3. Reverse for chronological order
4. Ignore messages from other branches

### Branching Workflow

1. **Reply to a message** in the conversation
2. **Send** `/fork explore-option-b`
3. **New branch** is created from that message
4. **Switch** `/checkout 2` to work on branch
5. **Merge** `/merge 2` when done, or `/delete-branch 2` to discard

## API Usage

```typescript
import { SessionLogger, SessionTreeVisualizer } from '@openclaw/tree-sessions';

// Initialize
const logger = new SessionLogger('/path/to/sessions.jsonl');
const visualizer = new SessionTreeVisualizer();

// Log a message
await logger.logMessage({
  role: 'user',
  content: 'Hello',
  externalId: 'telegram-msg-123'
});

// Create a branch
const branchId = await logger.forkBranch('msg_a1b2c3d4', 'explore-option-b');

// Switch branches
await logger.switchBranch(branchId);

// Load context for LLM
const context = await logger.loadContext();

// Visualize tree
const html = await visualizer.exportHTML(logger.exportTree());
```

## Visualization

The web UI includes:

- 🖱️ **Interactive tree** with zoom/pan
- 🔍 **Search functionality** across all messages
- 📝 **Click-to-view** message details panel
- 📤 **Export** as SVG or PDF

## Comparison: pi vs OpenClaw

| Feature | pi (Terminal) | OpenClaw |
|---------|---------------|----------|
| Interface | TUI (arrow keys) | Chat Apps |
| Branching | `/tree` + navigate | Reply + `/fork` |
| Visualization | In-terminal | Web UI (D3.js) |
| Context Loading | Linear | Tree traversal |

## Example Use Cases

### 1. Explore Multiple Solutions

```
User: How should we authenticate users?

You: [Option A: JWT]
User: Let's explore that
You: /fork jwt-approach

[Later switch branches]
User: Let's see Option B
You: /checkout 2
You: [Option B: OAuth2]
```

### 2. Parallel Work

```
User: I need to fix a bug and add a feature

You: /fork bug-fix
[Later switch back]
You: /checkout 2
You: [Working on feature]
```

### 3. Safe Experimentation

```
User: Try this risky approach

You: /fork experiment
[Try experimental approach]
If it fails: /delete-branch 2
If it works: /merge 2
```

## Files

- `session-logger.ts` — Core logging logic (10,679 bytes)
- `reply-handler.ts` — Chat command handlers (9,853 bytes)
- `tree-visualizer.ts` — D3.js web UI (12,925 bytes)
- `index.ts` — Main exports (3,289 bytes)
- `TREE_SESSIONS.md` — Complete documentation (18,378 bytes)

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `TREE_SESSIONS_PATH` | ~/.openclaw/sessions.jsonl | Session data file |
| `TREE_EXPORT_DIR` | ~/.openclaw/exports | Export output directory |

## Configuration

```typescript
const config = {
  sessionPath: '/path/to/sessions.jsonl',
  exportDir: '/path/to/exports',
  maxTreeDepth: 50,
  enableAutoSave: true
};
```

## Support

- **Discord:** https://discord.gg/clawd
- **Docs:** https://docs.openclaw.ai
