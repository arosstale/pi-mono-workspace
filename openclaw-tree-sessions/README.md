# @openclaw/tree-sessions

> Tree-structured session history for OpenClaw with branching conversations

---

## 🌳 Overview

OpenClaw Tree Sessions brings pi's powerful tree-structured conversations to chat-based platforms (Telegram, WhatsApp, Discord). Explore alternative conversation paths, fork branches, and merge ideas with an intuitive interface.

---

## ✨ Features

- **🌿 Branching** — Fork new branches from any message
- **📋 Branch Management** — List, switch, merge, and delete branches
- **🔍 Context Loading** — Smart tree traversal for LLM context
- **🎨 Visual Tree** — Interactive D3.js tree visualization
- **💾 Persistent State** — All branches preserved across sessions
- **🔗 Reply Integration** — Native reply-to-message forking in chat apps

---

## 🚀 Quick Start

### Installation

```bash
npm install @openclaw/tree-sessions
```

### Basic Usage

```typescript
import { createTreeSessions } from '@openclaw/tree-sessions';
import express from 'express';

const app = express();

// Create tree sessions manager
const sessions = createTreeSessions(app, {
  sessionId: 'session-123',
  sessionDir: './sessions',
  visualizer: {
    zoomable: true,
    searchable: true,
    exportable: true
  }
});

// Log a message
await sessions.logMessage('user', 'Help me fix the bug', undefined, 'telegram-msg-123');

// Fork a new branch
const branchId = await sessions.forkBranch('msg-parent-id', 'bug-fix-exploration');

// Switch branches
await sessions.switchBranch('msg-leaf-id');

// Get all branches
const branches = await sessions.getBranches();
console.log(branches);

// Export tree
const tree = await sessions.exportTree();
```

### Chat Commands

```
/fork [name]              - Create new branch from replied message
/branches                  - List all active branches
/checkout <number>          - Switch to branch
/merge <number>             - Merge branch into current
/delete-branch <number>     - Delete a branch
/tree [format]             - Export tree (json, html, text)
```

---

## 📊 Comparison

| Feature | pi (Terminal) | OpenClaw Tree Sessions |
|---------|---------------|----------------------|
| **Interface** | TUI (arrow keys) | Chat Apps (WhatsApp, Telegram) |
| **Branching** | Press /tree + navigate | Reply to message + /fork |
| **Visualization** | In-terminal tree | Web UI (D3.js) |
| **Context Loading** | Linear | Tree traversal (active branch only) |
| **Branch Switching** | Visual selection | /checkout <number> |

---

## 🏗 Architecture

### Data Structure

Each message is stored with relational IDs in JSONL format:

```json
{
  "id": "msg_a1b2c3d4",
  "parentId": "msg_x9y8z7w6",
  "role": "user",
  "content": "Help me fix the bug",
  "timestamp": "2026-02-25T12:00:00.000Z",
  "branchId": "branch_explore_oauth",
  "externalId": "telegram-msg-123"
}
```

### State Persistence

Session state stored in `.state.json`:

```json
{
  "activeLeafId": "msg_current_leaf",
  "currentBranchId": "branch_main",
  "createdAt": "2026-02-25T10:00:00.000Z",
  "updatedAt": "2026-02-25T12:30:00.000Z",
  "totalMessages": 42
}
```

### Context Loading

When loading context for the LLM:
1. Start at `activeLeafId`
2. Walk backward via `parentId` chain
3. Reverse to get chronological order
4. Ignore messages from other branches

---

## 🛠 API Reference

### SessionLogger

```typescript
import { SessionLogger } from '@openclaw/tree-sessions';

const logger = new SessionLogger('session-123', './sessions');

// Log a message
await logger.logMessage('user', 'Hello', parentId, externalId);

// Fork branch
const branchId = await logger.forkBranch(parentId, branchName);

// Switch branch
await logger.switchBranch(leafId);

// Load context
const context = await logger.loadContext(100);

// Get branches
const branches = await logger.getBranches();

// Export tree
const tree = await logger.exportTree();

// Merge branch
const merged = await logger.mergeBranch(sourceLeafId);

// Delete branch
const deleted = await logger.deleteBranch(branchId);
```

### ReplyForkHandler

```typescript
import { ReplyForkHandler } from '@openclaw/tree-sessions';

const handler = new ReplyForkHandler(logger, sessionId);

// Handle /fork
await handler.handleFork(externalId, branchName);

// Handle /branches
const branchesList = await handler.handleBranches();

// Handle /checkout
await handler.handleCheckout(1);

// Handle /merge
await handler.handleMerge(2);

// Handle /delete-branch
await handler.handleDeleteBranch(3, true);
```

### SessionTreeVisualizer

```typescript
import { SessionTreeVisualizer } from '@openclaw/tree-sessions';

const visualizer = new SessionTreeVisualizer(
  logger,
  app,
  {
    width: 1200,
    height: 800,
    zoomable: true,
    searchable: true,
    exportable: true
  }
);

// Routes automatically registered:
// GET /_admin/sessions/:id/tree.html  - Interactive tree
// GET /_admin/sessions/:id/tree.json  - JSON export
// GET /_admin/sessions/:id/tree.txt   - Text export
// POST /_admin/sessions/:id/switch  - Switch branch
```

---

## 🎯 Use Cases

### 1. Bug Fix Exploration

```
User: The login isn't working
Assistant: Let me check... Found the issue
User: [Reply] /fork fix-auth-bug
OpenClaw: 🌿 Branch created: fix-auth-bug
User: Try clearing the token
Assistant: Done
User: [Reply] /fork alternative-fix
OpenClaw: 🌿 Branch created: alternative-fix
User: Reset the session instead
Assistant: Implemented
/branches
OpenClaw: 1. fix-auth-bug
         2. main (current)
         3. alternative-fix
User: /merge 1
OpenClaw: Merged branch 1 into main
```

### 2. Feature Brainstorming

```
User: I need a new feature for payments
Assistant: What kind of payments?
User: [Reply] /fork stripe-integration
OpenClaw: 🌿 Branch: stripe-integration
User: Add checkout button
Assistant: Done
User: [Reply] /fork paypal-integration
OpenClaw: 🌿 Branch: paypal-integration
User: Add PayPal button
Assistant: Done
/tree html
OpenClaw: Exported: https://.../tree.html
```

---

## 💡 Tips

1. **Use Descriptive Branch Names** — `/fork bug-fix-2` vs `/fork branch_abc123`
2. **Name Your Alternatives** — Try different approaches, keep them accessible
3. **Review with /branches** — See what you're working on, switch contexts
4. **Export for Documentation** — `/tree html` → Save for team review
5. **Merge the Best** — Keep exploring, then merge the winner

---

## 🔒 Security

- **No Data Loss** — All branches preserved until explicitly deleted
- **Reversible Operations** — Delete requires confirmation
- **State Persistence** — Sessions survive restarts
- **Message Mapping** — External IDs stored securely for reply forking

---

## 📦 Files

| File | Description |
|------|-------------|
| `session-logger.ts` | Core tree logging logic |
| `reply-handler.ts` | Chat command handlers |
| `tree-visualizer.ts` | Web UI with D3.js |
| `index.ts` | Main exports |
| `TREE_SESSIONS.md` | Full documentation |

---

## 🚦 License

MIT

---

## 🤝 Contributing

Contributions welcome! Please open an issue or PR.

---

**Start branching your conversations!** 🌳
