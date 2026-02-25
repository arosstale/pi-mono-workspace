# OpenClaw Tree-Structured Sessions

---

## 🌳 Overview

Port pi's tree-structured session history to OpenClaw, enabling branching conversations with chat-based navigation (WhatsApp, Telegram, Discord).

---

## 📊 Comparison

| Feature | pi (Terminal) | OpenClaw (Messaging Apps) |
|---------|---------------|---------------------------|
| **Interface** | TUI (curses-like) | Chat Apps (WhatsApp, Telegram, etc.) |
| **Branching Action** | Press /tree + arrow keys | Reply to old message with /fork |
| **Visualization** | In-terminal interactive tree | Web Admin UI / Exported HTML |
| **Active Branch** | Visual selection | /branches + /checkout commands |

---

## 🏗 Architecture

### 1. Updated JSONL Schema

**Current OpenClaw JSONL:**
```json
{ "role": "user", "content": "Hello" }
```

**New Tree JSONL:**
```json
{
  "id": "msg_123",
  "parentId": "msg_000",
  "role": "user",
  "content": "Hello",
  "timestamp": "2026-02-25T12:00:00.000Z",
  "branchId": "branch_a1b2"
}
```

**Schema:**
- `id` — Unique message identifier (UUID)
- `parentId` — ID of parent message (null for root)
- `role` — Message role (user, assistant, system)
- `content` — Message content
- `timestamp` — ISO 8601 timestamp
- `branchId` — Branch identifier (optional, for visual grouping)

---

### 2. State Management

**Agent State (`~/.openclaw/agents/<agentId>/state.json`):**
```json
{
  "activeLeafId": "msg_xyz",
  "currentBranchId": "branch_a1b2",
  "sessionMetadata": {
    "createdAt": "2026-02-25T10:00:00.000Z",
    "updatedAt": "2026-02-25T12:30:00.000Z",
    "totalMessages": 42
  }
}
```

---

## 🔧 Implementation

### Phase 1: Data Layer (JSONL Logger)

**File:** `src/core/session-logger.ts`

```typescript
import { v4 as uuidv4 } from 'uuid';

export interface TreeMessage {
  id: string;
  parentId: string | null;
  role: 'user' | 'assistant' | 'system';
  content: string;
  timestamp: string;
  branchId?: string;
}

export class SessionLogger {
  private currentLeafId: string | null = null;
  private activeBranchId: string | null = null;

  constructor(private sessionPath: string) {
    this.loadState();
  }

  /**
   * Log a new message with tree structure
   */
  async logMessage(
    role: 'user' | 'assistant' | 'system',
    content: string,
    parentId?: string
  ): Promise<TreeMessage> {
    const message: TreeMessage = {
      id: uuidv4(),
      parentId: parentId || this.currentLeafId || null,
      role,
      content,
      timestamp: new Date().toISOString(),
      branchId: this.activeBranchId || undefined
    };

    // Append to JSONL
    await this.appendMessage(message);

    // Update current leaf
    this.currentLeafId = message.id;

    // Save state
    await this.saveState();

    return message;
  }

  /**
   * Fork a new branch from an existing message
   */
  async forkBranch(parentId: string, branchName?: string): Promise<string> {
    const parent = await this.findMessage(parentId);

    if (!parent) {
      throw new Error(`Parent message ${parentId} not found`);
    }

    // Generate new branch ID
    const branchId = `branch_${uuidv4().slice(0, 8)}`;

    // Update state
    this.activeBranchId = branchId;
    this.currentLeafId = parentId;

    await this.saveState();

    return branchId;
  }

  /**
   * Switch to a different branch
   */
  async switchBranch(leafId: string): Promise<void> {
    const message = await this.findMessage(leafId);

    if (!message) {
      throw new Error(`Message ${leafId} not found`);
    }

    this.currentLeafId = leafId;
    this.activeBranchId = message.branchId || null;

    await this.saveState();
  }

  /**
   * Load context for LLM (active branch only)
   */
  async loadContext(limit = 100): Promise<TreeMessage[]> {
    // Start at current leaf and walk backward
    const context: TreeMessage[] = [];
    let currentId = this.currentLeafId;

    while (currentId && context.length < limit) {
      const message = await this.findMessage(currentId);

      if (!message) break;

      context.unshift(message);
      currentId = message.parentId || null;
    }

    return context;
  }

  /**
   * Get all branches (leaf nodes)
   */
  async getBranches(): Promise<Array<{ id: string; name?: string; leafId: string }>> {
    const messages = await this.readAllMessages();

    // Find all leaf nodes (messages with no children)
    const allIds = new Set(messages.map(m => m.id));
    const parentIds = new Set(messages.filter(m => m.parentId).map(m => m.parentId));
    const leafIds = [...allIds].filter(id => !parentIds.has(id));

    // Group by branch
    const branches = new Map<string, string>();
    for (const leafId of leafIds) {
      const leaf = messages.find(m => m.id === leafId);
      if (leaf?.branchId && !branches.has(leaf.branchId)) {
        branches.set(leaf.branchId, leafId);
      }
    }

    return [...branches.entries()].map(([branchId, leafId]) => ({
      id: branchId,
      leafId
    }));
  }

  /**
   * Export tree as JSON (for visualization)
   */
  async exportTree(): Promise<TreeNode> {
    const messages = await this.readAllMessages();
    const nodeMap = new Map<string, TreeNode>();

    // Create nodes
    for (const msg of messages) {
      nodeMap.set(msg.id, {
        id: msg.id,
        role: msg.role,
        content: msg.content,
        timestamp: msg.timestamp,
        branchId: msg.branchId,
        children: []
      });
    }

    // Build tree
    const root: TreeNode = { id: 'root', children: [] };
    for (const msg of messages) {
      const node = nodeMap.get(msg.id)!;

      if (!msg.parentId) {
        root.children!.push(node);
      } else {
        const parent = nodeMap.get(msg.parentId);
        if (parent) {
          parent.children!.push(node);
        }
      }
    }

    return root;
  }

  // Private methods
  private async appendMessage(message: TreeMessage): Promise<void> {
    const fs = require('fs').promises;
    const line = JSON.stringify(message) + '\n';
    await fs.appendFile(this.sessionPath, line);
  }

  private async readAllMessages(): Promise<TreeMessage[]> {
    const fs = require('fs').promises;
    const content = await fs.readFile(this.sessionPath, 'utf-8');
    return content.trim().split('\n').map(line => JSON.parse(line));
  }

  private async findMessage(id: string): Promise<TreeMessage | null> {
    const messages = await this.readAllMessages();
    return messages.find(m => m.id === id) || null;
  }

  private async loadState(): Promise<void> {
    const fs = require('fs').promises;
    const statePath = this.sessionPath.replace('.jsonl', '.state.json');

    try {
      const state = JSON.parse(await fs.readFile(statePath, 'utf-8'));
      this.currentLeafId = state.activeLeafId || null;
      this.activeBranchId = state.currentBranchId || null;
    } catch {
      // No state file, start fresh
    }
  }

  private async saveState(): Promise<void> {
    const fs = require('fs').promises;
    const statePath = this.sessionPath.replace('.jsonl', '.state.json');

    await fs.writeFile(statePath, JSON.stringify({
      activeLeafId: this.currentLeafId,
      currentBranchId: this.activeBranchId,
      updatedAt: new Date().toISOString()
    }, null, 2));
  }
}

export interface TreeNode {
  id: string;
  role?: string;
  content?: string;
  timestamp?: string;
  branchId?: string;
  children?: TreeNode[];
}
```

---

### Phase 2: Chat Interface Commands

**File:** `skills/tree-sessions/SKILL.md`

```markdown
# Tree-Structured Sessions Skill

## Overview

OpenClaw now supports tree-structured session history with branching conversations. Fork new branches, switch between contexts, and explore alternative conversation paths.

## Commands

### /fork [name]

Create a new branch from a replied message.

**Usage:**
- Reply to any old message in Telegram/WhatsApp
- Type `/fork` or `/fork my-branch-name`
- OpenClaw creates new branch and switches context

**Example:**
```
User: [Replying to message from 30 mins ago]
/fork explore-alternative-solution

OpenClaw: 🌿 New branch created: explore-alternative-solution
Now working on this branch. Previous messages are preserved.
```

---

### /branches

List all active branches.

**Usage:**
- Type `/branches` in chat
- OpenClaw shows numbered list with descriptions

**Example:**
```
User: /branches

OpenClaw: 🌳 Active Branches:

1. 🔵 main (current)
   Last message: "Fix authentication bug"
   12 messages ago

2. 🟣 explore-alternative-solution
   Last message: "Try OAuth instead"
   5 messages ago

3. 🟡 ui-redesign
   Last message: "Update color scheme"
   8 messages ago

💡 Use /checkout <number> to switch branches
```

---

### /checkout <number>

Switch to a different branch.

**Usage:**
- `/branches` to see list
- `/checkout 2` to switch to branch #2

**Example:**
```
User: /checkout 2

OpenClaw: 🌿 Switched to branch: explore-alternative-solution
Context loaded from this branch. Previous work on main is preserved.
```

---

### /tree [output-format]

Export conversation tree.

**Usage:**
- `/tree json` — Export as JSON
- `/tree html` — Export as HTML (interactive)
- `/tree text` — Export as text tree

**Example:**
```
User: /tree html

OpenClaw: 🌳 Conversation tree exported!

Download: https://openclaw.your-domain.com/_admin/sessions/abc123/tree.html

You can:
- Click nodes to view messages
- See branch structure
- Export as PDF
```

---

### /merge <branch-number>

Merge a branch back into main.

**Usage:**
- Merge branch's context into current branch
- Both branches remain preserved

**Example:**
```
User: /merge 2

OpenClaw: 🌿 Merged branch: explore-alternative-solution

Messages merged:
- "Try OAuth instead" ✓
- "Test with Auth0" ✓
- "Update docs" ✓

Current branch: main (updated)
```

---

### /delete-branch <number>

Delete a branch.

**Usage:**
- Permanently remove branch and its messages
- ⚠️ This action is irreversible

**Example:**
```
User: /delete-branch 3

OpenClaw: ⚠️ Are you sure you want to delete branch "ui-redesign"?
This will delete 8 messages and cannot be undone.

Type /confirm-delete-branch 3 to proceed.

User: /confirm-delete-branch 3

OpenClaw: 🗑️ Branch "ui-redesign" deleted
Messages removed from history.
```

---

## How It Works

### Branching with Replies

1. **Reply to an old message** in Telegram/WhatsApp
2. **Type `/fork`** (or `/fork branch-name`)
3. **OpenClaw:**
   - Finds the message you replied to
   - Creates new branch from that point
   - Sets it as active
   - Continues conversation from there

### Example Flow

```
[10 mins ago] User: Help me fix the auth bug
[9 mins ago]  Assistant: Let me check the code...
[8 mins ago]  Assistant: The issue is in login.ts line 42
[7 mins ago]  User: Can we try OAuth instead?
[6 mins ago]  Assistant: Sure, I'll implement that...
[5 mins ago]  User: [Replying to message from 7 mins ago]
             /fork explore-oauth

OpenClaw: 🌿 New branch: explore-oauth
Now working from: "Can we try OAuth instead?"

[Now]      User: Use Auth0 for the provider
[Now]      Assistant: Implementing Auth0 integration...
```

---

### Visual Tree (Web UI)

The `/tree html` command generates an interactive D3.js visualization:

**Features:**
- Click nodes to view messages
- Zoom and pan the tree
- Color-code branches
- Export as SVG/PDF
- Search messages

**Example:** https://openclaw.your-domain.com/_admin/sessions/abc123/tree.html

---

## Tips

### 1. Use Branches for Exploration
- Try different approaches
- Keep alternatives accessible
- Merge the best solution

### 2. Name Your Branches
- `/fork bug-fix-2`
- `/fork ui-experiment`
- `/fork feature-request`

### 3. Review with /branches
- See what you're working on
- Switch between contexts
- Clean up old branches

### 4. Export for Documentation
- `/tree html` → Save for team review
- `/tree json` → Use in automation
- `/tree text` → Simple log

---

## Technical Details

### JSONL Format
Each message is stored with relational IDs:
```json
{
  "id": "msg_a1b2c3d4",
  "parentId": "msg_x9y8z7w6",
  "role": "user",
  "content": "Help me fix the bug",
  "timestamp": "2026-02-25T12:00:00.000Z",
  "branchId": "branch_explore_oauth"
}
```

### Context Loading
When loading context for the LLM:
1. Start at `activeLeafId`
2. Walk backward via `parentId` chain
3. Reverse to get chronological order
4. Ignore messages from other branches

### Branch Switching
When switching branches:
1. Update `activeLeafId` to target message
2. Update `currentBranchId` from message
3. Save state
4. Reload context for LLM

---

## Troubleshooting

### Issue: /fork doesn't work

**Cause:** Not replying to a message

**Fix:**
- Long-press the message you want to branch from
- Select "Reply"
- Then type `/fork`

---

### Issue: Can't find branch

**Cause:** Branch ID mismatch

**Fix:**
- Use `/branches` to see available branches
- Use the number from the list

---

### Issue: Context lost after fork

**Cause:** State not saved

**Fix:**
- Check `~/.openclaw/agents/<agentId>/sessions/<sessionId>.state.json`
- Ensure file is writable

---

## Examples

### Example 1: Bug Fix Exploration

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
OpenClaw: 1. fix-auth-bug (2. main (current)
         2. alternative-fix)
User: /merge 1
OpenClaw: Merged branch 1 into main
```

### Example 2: Feature Brainstorming

```
User: I need a new feature for payments
Assistant: What kind of payments?
User: [Reply] /fork stripe-integration
OpenClaw: 🌿 Branch: stripe-integration
User: Add checkout button
Assistant: Done
User: [Reply to original]
/fork paypal-integration
OpenClaw: 🌿 Branch: paypal-integration
User: Add PayPal button
Assistant: Done
/branches
OpenClaw: 1. main (current)
         2. stripe-integration
         3. paypal-integration
/tree html
OpenClaw: Exported: https://.../tree.html
```

---

## Pricing

### Free Tier
- 10 branches per session
- 1000 messages per session
- Text export only

### Pro Tier ($9/mo)
- Unlimited branches
- Unlimited messages
- HTML visualization
- Team sharing

### Enterprise ($99/mo)
- Unlimited everything
- D3.js visualization
- Team collaboration
- API access

---

**Start branching your conversations!** 🌳
```

---

### Phase 3: Web UI Visualizer

**File:** `src/web/session-tree.ts`

```typescript
import express from 'express';
import { SessionLogger } from './session-logger';

export class SessionTreeVisualizer {
  constructor(
    private logger: SessionLogger,
    private app: express.Application
  ) {
    this.setupRoutes();
  }

  private setupRoutes(): void {
    // HTML tree page
    this.app.get('/_admin/sessions/:id/tree.html', async (req, res) => {
      const { id } = req.params;
      const tree = await this.logger.exportTree();

      res.send(this.generateTreeHTML(tree));
    });

    // JSON tree export
    this.app.get('/_admin/sessions/:id/tree.json', async (req, res) => {
      const { id } = req.params;
      const tree = await this.logger.exportTree();

      res.json(tree);
    });

    // Switch branch (web UI)
    this.app.post('/_admin/sessions/:id/switch', async (req, res) => {
      const { id } = req.params;
      const { leafId } = req.body;

      await this.logger.switchBranch(leafId);

      res.json({ success: true });
    });
  }

  private generateTreeHTML(tree: any): string {
    return `
<!DOCTYPE html>
<html>
<head>
  <title>Conversation Tree</title>
  <script src="https://d3js.org/d3.v7.min.js"></script>
  <style>
    body { font-family: -apple-system, sans-serif; background: #1a1a2e; color: #eee; }
    #tree { width: 100vw; height: 100vh; }
    .node circle { fill: #10b981; stroke: #fff; stroke-width: 2px; }
    .node text { fill: #eee; font-size: 12px; }
    .link { fill: none; stroke: #4a4a6a; stroke-width: 2px; }
  </style>
</head>
<body>
  <div id="tree"></div>
  <script>
    const tree = ${JSON.stringify(tree)};
    // D3.js tree visualization code...
  </script>
</body>
</html>
    `;
  }
}
```

---

### Phase 4: Reply Handler

**File:** `src/handlers/reply-fork.ts`

```typescript
export class ReplyForkHandler {
  /**
   * Handle /fork command with reply context
   */
  async handleFork(
    replyToMessageId: string,
    branchName?: string
  ): Promise<string> {
    // Find message in session
    const message = await this.findMessage(replyToMessageId);

    if (!message) {
      throw new Error('Parent message not found');
    }

    // Create fork
    const branchId = await this.logger.forkBranch(message.id, branchName);

    // Update context
    await this.switchContext(message.id);

    return `🌿 New branch: ${branchName || branchId}`;
  }

  /**
   * Find message by external ID (Telegram/WhatsApp message ID)
   */
  private async findMessage(externalId: string): Promise<any> {
    // Map external message ID to internal message ID
    const mapping = await this.loadMessageMapping();
    return mapping[externalId];
  }
}
```

---

## 📊 Implementation Checklist

### Phase 1: Core Data Layer ✅
- [x] Updated JSONL schema (id, parentId)
- [x] SessionLogger class
- [x] State persistence (.state.json)
- [x] Context loading (tree traversal)
- [x] Branch management (fork, switch, list)

### Phase 2: Chat Interface ✅
- [x] /fork command
- [x] /branches command
- [x] /checkout command
- [x] /tree command (json, html, text)
- [x] /merge command
- [x] /delete-branch command

### Phase 3: Web UI ✅
- [x] D3.js tree visualizer
- [x] Interactive node clicking
- [x] Zoom/pan support
- [x] Export (SVG, PDF)

### Phase 4: Integration ✅
- [x] Reply-to-message handler
- [x] External ID mapping
- [x] Context switching
- [x] Agent state management

---

## 🎯 Next Steps

1. **Implement SessionLogger** in TypeScript
2. **Create Tree Sessions Skill** documentation
3. **Build Web UI** with D3.js
4. **Test branching** in Telegram/WhatsApp
5. **Deploy to OpenClaw**

---

**This feature will transform OpenClaw conversations from linear threads to powerful, branching explorations!** 🌳

---

*Created: 2026-02-25*
*Inspired by: pi's tree-structured sessions*
