import { v4 as uuidv4 } from 'uuid';
import { promises as fs } from 'fs';
import { join } from 'path';

/**
 * Tree-structured message with relational IDs
 */
export interface TreeMessage {
  id: string;
  parentId: string | null;
  role: 'user' | 'assistant' | 'system';
  content: string;
  timestamp: string;
  branchId?: string;
  externalId?: string; // Telegram/WhatsApp message ID mapping
}

/**
 * Branch information
 */
export interface BranchInfo {
  id: string;
  name?: string;
  leafId: string;
  messageCount: number;
  lastActive: string;
}

/**
 * Tree node for visualization
 */
export interface TreeNode {
  id: string;
  role?: string;
  content?: string;
  timestamp?: string;
  branchId?: string;
  children?: TreeNode[];
}

/**
 * Session state
 */
export interface SessionState {
  activeLeafId: string | null;
  currentBranchId: string | null;
  createdAt: string;
  updatedAt: string;
  totalMessages: number;
}

/**
 * Session Logger with Tree-Structured History
 *
 * Enables branching conversations like pi, but adapted for chat interfaces.
 */
export class SessionLogger {
  private currentLeafId: string | null = null;
  private currentBranchId: string | null = null;
  private messageCount: number = 0;
  private createdAt: string = new Date().toISOString();

  constructor(
    private sessionId: string,
    private sessionDir: string = '.'
  ) {
    this.loadState();
  }

  /**
   * Log a new message with tree structure
   */
  async logMessage(
    role: 'user' | 'assistant' | 'system',
    content: string,
    parentId?: string,
    externalId?: string
  ): Promise<TreeMessage> {
    const message: TreeMessage = {
      id: uuidv4(),
      parentId: parentId || this.currentLeafId || null,
      role,
      content,
      timestamp: new Date().toISOString(),
      branchId: this.currentBranchId || undefined,
      externalId
    };

    // Append to JSONL
    await this.appendMessage(message);

    // Update state
    this.currentLeafId = message.id;
    this.messageCount++;

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
    const branchId = branchName || `branch_${uuidv4().slice(0, 8)}`;

    // Update state
    this.currentBranchId = branchId;
    this.currentLeafId = parentId;

    await this.saveState();

    return branchId;
  }

  /**
   * Switch to a different branch (by leaf message ID)
   */
  async switchBranch(leafId: string): Promise<void> {
    const message = await this.findMessage(leafId);

    if (!message) {
      throw new Error(`Message ${leafId} not found`);
    }

    this.currentLeafId = leafId;
    this.currentBranchId = message.branchId || null;

    await this.saveState();
  }

  /**
   * Load context for LLM (active branch only, chronological)
   */
  async loadContext(limit = 100): Promise<TreeMessage[]> {
    if (!this.currentLeafId) {
      return [];
    }

    // Start at current leaf and walk backward
    const context: TreeMessage[] = [];
    let currentId: string | null = this.currentLeafId;

    while (currentId && context.length < limit) {
      const message = await this.findMessage(currentId);

      if (!message) {
        break;
      }

      context.unshift(message);
      currentId = message.parentId || null;
    }

    return context;
  }

  /**
   * Get all active branches (leaf nodes)
   */
  async getBranches(): Promise<BranchInfo[]> {
    const messages = await this.readAllMessages();

    // Find all leaf nodes (messages with no children)
    const allIds = new Set(messages.map(m => m.id));
    const parentIds = new Set(
      messages.filter(m => m.parentId).map(m => m.parentId!)
    );
    const leafIds = [...allIds].filter(id => !parentIds.has(id));

    // Group by branch and count messages
    const branchMap = new Map<string, { leafId: string; lastActive: string; messages: TreeMessage[] }>();

    for (const leafId of leafIds) {
      const leaf = messages.find(m => m.id === leafId);
      if (!leaf) continue;

      const branchId = leaf.branchId || 'main';
      if (!branchMap.has(branchId)) {
        branchMap.set(branchId, { leafId, lastActive: leaf.timestamp, messages: [] });
      }
      branchMap.get(branchId)!.messages.push(leaf);
    }

    // Count messages per branch
    return [...branchMap.entries()].map(([id, data]) => ({
      id,
      leafId: data.leafId,
      messageCount: data.messages.length,
      lastActive: data.lastActive
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
        if (parent && parent.children) {
          parent.children.push(node);
        }
      }
    }

    return root;
  }

  /**
   * Merge branch into current branch
   */
  async mergeBranch(sourceLeafId: string): Promise<TreeMessage[]> {
    const sourceMessage = await this.findMessage(sourceLeafId);
    if (!sourceMessage) {
      throw new Error(`Source message ${sourceLeafId} not found`);
    }

    // Load branch context
    const merged: TreeMessage[] = [];
    let currentId: string | null = sourceLeafId;

    while (currentId) {
      const message = await this.findMessage(currentId);
      if (!message) break;

      // Skip if already in current branch
      if (message.id !== this.currentLeafId) {
        merged.unshift(message);
      }

      currentId = message.parentId || null;
    }

    // Append merged messages to current branch
    for (const msg of merged) {
      await this.logMessage(msg.role, msg.content, this.currentLeafId || undefined);
    }

    return merged;
  }

  /**
   * Delete a branch and its messages
   */
  async deleteBranch(branchId: string): Promise<number> {
    const messages = await this.readAllMessages();
    const toDelete = messages.filter(m => m.branchId === branchId);

    // Rewrite file without deleted messages
    const remaining = messages.filter(m => m.branchId !== branchId);
    await this.writeFile(remaining);

    // Update state if deleting current branch
    if (this.currentBranchId === branchId) {
      const mainBranch = await this.getMainBranch();
      if (mainBranch) {
        await this.switchBranch(mainBranch);
      }
    }

    return toDelete.length;
  }

  /**
   * Find message by external ID (Telegram/WhatsApp message ID)
   */
  async findByExternalId(externalId: string): Promise<TreeMessage | null> {
    const messages = await this.readAllMessages();
    return messages.find(m => m.externalId === externalId) || null;
  }

  /**
   * Get session state
   */
  getState(): SessionState {
    return {
      activeLeafId: this.currentLeafId,
      currentBranchId: this.currentBranchId,
      createdAt: this.createdAt,
      updatedAt: new Date().toISOString(),
      totalMessages: this.messageCount
    };
  }

  // Private methods

  private async appendMessage(message: TreeMessage): Promise<void> {
    const line = JSON.stringify(message) + '\n';
    const sessionPath = this.getSessionPath();
    await fs.appendFile(sessionPath, line);
  }

  private async readFile(): Promise<TreeMessage[]> {
    const sessionPath = this.getSessionPath();
    try {
      const content = await fs.readFile(sessionPath, 'utf-8');
      return content.trim().split('\n')
        .filter(line => line.trim())
        .map(line => JSON.parse(line));
    } catch (error) {
      if ((error as any).code === 'ENOENT') {
        return [];
      }
      throw error;
    }
  }

  private async writeFile(messages: TreeMessage[]): Promise<void> {
    const sessionPath = this.getSessionPath();
    const content = messages.map(m => JSON.stringify(m)).join('\n') + '\n';
    await fs.writeFile(sessionPath, content);
  }

  private async readAllMessages(): Promise<TreeMessage[]> {
    return this.readFile();
  }

  public async findMessage(id: string): Promise<TreeMessage | null> {
    const messages = await this.readAllMessages();
    return messages.find(m => m.id === id) || null;
  }

  private async getMainBranch(): Promise<string | null> {
    const branches = await this.getBranches();
    const main = branches.find(b => b.id === 'main');
    return main ? main.leafId : null;
  }

  private async loadState(): Promise<void> {
    const statePath = this.getStatePath();

    try {
      const content = await fs.readFile(statePath, 'utf-8');
      const state = JSON.parse(content);

      this.currentLeafId = state.activeLeafId || null;
      this.currentBranchId = state.currentBranchId || null;
      this.messageCount = state.totalMessages || 0;
      this.createdAt = state.createdAt || this.createdAt;
    } catch (error) {
      // No state file, start fresh
      this.messageCount = 0;
    }
  }

  private async saveState(): Promise<void> {
    const state: SessionState = {
      activeLeafId: this.currentLeafId,
      currentBranchId: this.currentBranchId,
      createdAt: this.createdAt,
      updatedAt: new Date().toISOString(),
      totalMessages: this.messageCount
    };

    const statePath = this.getStatePath();
    await fs.mkdir(this.sessionDir, { recursive: true });
    await fs.writeFile(statePath, JSON.stringify(state, null, 2));
  }

  private getSessionPath(): string {
    return join(this.sessionDir, `${this.sessionId}.jsonl`);
  }

  private getStatePath(): string {
    return join(this.sessionDir, `${this.sessionId}.state.json`);
  }
}

/**
 * Create a new session logger
 */
export function createSessionLogger(
  sessionId: string,
  sessionDir?: string
): SessionLogger {
  return new SessionLogger(sessionId, sessionDir);
}

/**
 * Load existing session
 */
export async function loadSession(
  sessionId: string,
  sessionDir?: string
): Promise<SessionLogger> {
  const logger = new SessionLogger(sessionId, sessionDir);
  const state = logger.getState();
  return logger;
}
