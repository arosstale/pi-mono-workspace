import { SessionLogger, TreeMessage } from './session-logger';

/**
 * External message mapping (Telegram/WhatsApp message ID → internal message ID)
 */
export interface ExternalMessageMapping {
  externalId: string; // Telegram/WhatsApp message ID
  internalId: string; // OpenClaw message ID
  sessionId: string;
  timestamp: string;
}

/**
 * Reply handler options
 */
export interface ReplyHandlerOptions {
  saveMappings: boolean;
  mappingsPath?: string;
}

/**
 * Reply Fork Handler
 *
 * Handles branching by replying to old messages in chat apps.
 * Maps external message IDs (Telegram/WhatsApp) to internal message IDs.
 */
export class ReplyForkHandler {
  private messageMappings: Map<string, string> = new Map();

  constructor(
    private logger: SessionLogger,
    private sessionId: string,
    private options: ReplyHandlerOptions = { saveMappings: true }
  ) {
    this.loadMappings();
  }

  /**
   * Handle /fork command with reply context
   */
  async handleFork(
    replyToExternalId: string,
    branchName?: string
  ): Promise<{ branchId: string; message: string }> {
    // Find internal message ID
    const internalId = this.findInternalId(replyToExternalId);

    if (!internalId) {
      throw new Error(
        'Cannot find parent message. ' +
        'Make sure to reply to a message in this conversation.'
      );
    }

    // Get parent message
    const parent = await this.logger.findMessage(internalId);

    if (!parent) {
      throw new Error('Parent message not found in session history');
    }

    // Fork branch from this message
    const branchId = await this.logger.forkBranch(internalId, branchName);

    // Generate response message
    const responseMessage = this.generateForkMessage(branchId, parent, branchName);

    return { branchId, message: responseMessage };
  }

  /**
   * Handle /branches command
   */
  async handleBranches(): Promise<string> {
    const branches = await this.logger.getBranches();
    const state = this.logger.getState();

    return this.generateBranchesList(branches, state);
  }

  /**
   * Handle /checkout command
   */
  async handleCheckout(branchNumber: number): Promise<string> {
    const branches = await this.logger.getBranches();

    if (branchNumber < 1 || branchNumber > branches.length) {
      const validNumbers = branches.map((_, i) => i + 1).join(', ');
      throw new Error(
        `Invalid branch number. Valid branches: ${validNumbers || 'none'}`
      );
    }

    const branch = branches[branchNumber - 1];
    await this.logger.switchBranch(branch.leafId);

    return this.generateCheckoutMessage(branch);
  }

  /**
   * Handle /merge command
   */
  async handleMerge(branchNumber: number): Promise<string> {
    const branches = await this.logger.getBranches();

    if (branchNumber < 1 || branchNumber > branches.length) {
      throw new Error('Invalid branch number');
    }

    const branch = branches[branchNumber - 1];
    const merged = await this.logger.mergeBranch(branch.leafId);

    return this.generateMergeMessage(branch, merged);
  }

  /**
   * Handle /delete-branch command
   */
  async handleDeleteBranch(branchNumber: number, confirm = false): Promise<string> {
    const branches = await this.logger.getBranches();

    if (branchNumber < 1 || branchNumber > branches.length) {
      throw new Error('Invalid branch number');
    }

    const branch = branches[branchNumber - 1];

    if (!confirm) {
      return this.generateDeleteConfirmation(branch);
    }

    const deletedCount = await this.logger.deleteBranch(branch.id);

    return this.generateDeleteMessage(branch, deletedCount);
  }

  /**
   * Map external message ID to internal message ID
   */
  mapMessage(externalId: string, internalId: string): void {
    this.messageMappings.set(externalId, internalId);

    if (this.options.saveMappings) {
      this.saveMappings();
    }
  }

  /**
   * Find internal message ID from external ID
   */
  findInternalId(externalId: string): string | undefined {
    return this.messageMappings.get(externalId);
  }

  // Private methods

  private generateForkMessage(
    branchId: string,
    parent: TreeMessage,
    branchName?: string
  ): string {
    const name = branchName || branchId;
    const preview = (parent.content || '').substring(0, 50);

    return `🌿 **New branch created:** \`${name}\`\n\n` +
      `Branching from:\n` +
      `> "${preview}..."\n\n` +
      `Now working on this branch. All previous messages are preserved.\n\n` +
      `💡 Use \`/branches\` to see all branches\n` +
      `💡 Use \`/checkout <number>\` to switch branches`;
  }

  private generateBranchesList(
    branches: any[],
    state: any
  ): string {
    if (branches.length === 0) {
      return '🌳 No branches yet. Use `/fork` to create a new branch.';
    }

    let message = '🌳 **Active Branches:**\n\n';

    branches.forEach((branch, index) => {
      const number = index + 1;
      const isCurrent = branch.leafId === state.activeLeafId;
      const icon = isCurrent ? '🔵' : '⚪';
      const timeAgo = this.getTimeAgo(branch.lastActive);

      message += `${number}. ${icon} \`${branch.id}\`\n` +
        `   Messages: ${branch.messageCount}\n` +
        `   Last active: ${timeAgo}\n` +
        `${isCurrent ? '   *(current branch)*\n' : ''}\n`;
    });

    message += `💡 Use \`/checkout <number>\` to switch branches`;

    return message;
  }

  private generateCheckoutMessage(branch: any): string {
    return `🌿 **Switched to branch:** \`${branch.id}\`\n\n` +
      `Context loaded from this branch. Previous work is preserved.\n\n` +
      `💡 Use \`/branches\` to see all branches`;
  }

  private generateMergeMessage(branch: any, merged: TreeMessage[]): string {
    const mergedCount = merged.length;
    const mergedList = merged
      .map(m => `✅ "${(m.content || '').substring(0, 40)}..."`)
      .join('\n');

    return `🌿 **Merged branch:** \`${branch.id}\`\n\n` +
      `${mergedCount} messages merged:\n${mergedList}\n\n` +
      `Current branch updated.`;
  }

  private generateDeleteConfirmation(branch: any): string {
    return `⚠️ **Delete branch:** \`${branch.id}\`?\n\n` +
      `This will delete ${branch.messageCount} messages and cannot be undone.\n\n` +
      `Type \`/confirm-delete-branch ${branch.id}\` to proceed.`;
  }

  private generateDeleteMessage(branch: any, deletedCount: number): string {
    return `🗑️ **Branch deleted:** \`${branch.id}\`\n\n` +
      `${deletedCount} messages removed from history.`;
  }

  private getTimeAgo(timestamp: string): string {
    const now = new Date();
    const then = new Date(timestamp);
    const diffMs = now.getTime() - then.getTime();
    const diffMins = Math.floor(diffMs / 60000);
    const diffHours = Math.floor(diffMs / 3600000);
    const diffDays = Math.floor(diffMs / 86400000);

    if (diffMins < 1) return 'just now';
    if (diffMins < 60) return `${diffMins} minutes ago`;
    if (diffHours < 24) return `${diffHours} hours ago`;
    return `${diffDays} days ago`;
  }

  private async loadMappings(): Promise<void> {
    if (!this.options.saveMappings) return;

    const fs = require('fs').promises;
    const path = require('path');

    try {
      const mappingsPath = this.getMappingsPath();
      const content = await fs.readFile(mappingsPath, 'utf-8');
      const mappings: ExternalMessageMapping[] = JSON.parse(content);

      this.messageMappings.clear();
      for (const mapping of mappings) {
        if (mapping.sessionId === this.sessionId) {
          this.messageMappings.set(mapping.externalId, mapping.internalId);
        }
      }
    } catch (error) {
      // No mappings file, start fresh
      this.messageMappings = new Map();
    }
  }

  private async saveMappings(): Promise<void> {
    if (!this.options.saveMappings) return;

    const fs = require('fs').promises;
    const path = require('path');

    // Load existing mappings
    let allMappings: ExternalMessageMapping[] = [];
    const mappingsPath = this.getMappingsPath();

    try {
      const content = await fs.readFile(mappingsPath, 'utf-8');
      allMappings = JSON.parse(content);
    } catch {
      // No file, start fresh
    }

    // Update or add new mapping
    for (const [externalId, internalId] of this.messageMappings.entries()) {
      const existing = allMappings.find(m => m.externalId === externalId);

      if (existing) {
        existing.internalId = internalId;
        existing.timestamp = new Date().toISOString();
      } else {
        allMappings.push({
          externalId,
          internalId,
          sessionId: this.sessionId,
          timestamp: new Date().toISOString()
        });
      }
    }

    // Save
    const dir = path.dirname(mappingsPath);
    await fs.mkdir(dir, { recursive: true });
    await fs.writeFile(mappingsPath, JSON.stringify(allMappings, null, 2));
  }

  private getMappingsPath(): string {
    const path = require('path');
    const mappingsPath = this.options.mappingsPath || path.join(
      process.env.HOME || '.',
      '.openclaw',
      'message-mappings.json'
    );
    return mappingsPath;
  }
}

/**
 * Create reply handler for a session
 */
export function createReplyHandler(
  logger: SessionLogger,
  sessionId: string,
  options?: ReplyHandlerOptions
): ReplyForkHandler {
  return new ReplyForkHandler(logger, sessionId, options);
}

/**
 * Handle incoming message with reply context
 */
export async function handleIncomingMessage(
  handler: ReplyForkHandler,
  externalMessageId: string,
  externalReplyToId?: string
): Promise<void> {
  // If this is a reply to an existing message, map it
  if (externalReplyToId) {
    // When the message is logged, we'll get the internal ID
    // For now, just record the mapping for future /fork commands
  }
}
