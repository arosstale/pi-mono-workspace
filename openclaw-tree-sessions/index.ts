/**
 * OpenClaw Tree-Structured Sessions
 *
 * Enables branching conversations with tree-structured history,
 * adapted from pi's TUI tree for chat-based interfaces.
 *
 * @module @openclaw/tree-sessions
 */

export * from './session-logger';
export * from './tree-visualizer';
export * from './reply-handler';

import { SessionLogger } from './session-logger';
import { SessionTreeVisualizer, VisualizationOptions } from './tree-visualizer';
import { ReplyForkHandler } from './reply-handler';

/**
 * Tree sessions configuration
 */
export interface TreeSessionsConfig {
  sessionId: string;
  sessionDir?: string;
  visualizer?: VisualizationOptions;
}

/**
 * Tree sessions manager
 */
export class TreeSessions {
  private logger: SessionLogger;
  private visualizer: SessionTreeVisualizer | null = null;
  private replyHandler: ReplyForkHandler;

  constructor(private app: any, private config: TreeSessionsConfig) {
    this.logger = new SessionLogger(
      config.sessionId,
      config.sessionDir
    );
    this.replyHandler = new ReplyForkHandler(
      this.logger,
      config.sessionId
    );

    // Setup visualizer if Express app provided
    if (app && config.visualizer !== false) {
      this.visualizer = new SessionTreeVisualizer(
        this.logger,
        app,
        config.visualizer
      );
    }
  }

  /**
   * Get the session logger
   */
  getLogger(): SessionLogger {
    return this.logger;
  }

  /**
   * Get the reply handler
   */
  getReplyHandler(): ReplyForkHandler {
    return this.replyHandler;
  }

  /**
   * Log a message
   */
  async logMessage(
    role: 'user' | 'assistant' | 'system',
    content: string,
    parentId?: string,
    externalId?: string
  ) {
    return this.logger.logMessage(role, content, parentId, externalId);
  }

  /**
   * Fork a new branch
   */
  async forkBranch(parentId: string, branchName?: string): Promise<string> {
    return this.logger.forkBranch(parentId, branchName);
  }

  /**
   * Switch to a different branch
   */
  async switchBranch(leafId: string): Promise<void> {
    return this.logger.switchBranch(leafId);
  }

  /**
   * Get all branches
   */
  async getBranches() {
    return this.logger.getBranches();
  }

  /**
   * Export tree
   */
  async exportTree() {
    return this.logger.exportTree();
  }

  /**
   * Handle /fork command
   */
  async handleFork(replyToExternalId: string, branchName?: string) {
    return this.replyHandler.handleFork(replyToExternalId, branchName);
  }

  /**
   * Handle /branches command
   */
  async handleBranches() {
    return this.replyHandler.handleBranches();
  }

  /**
   * Handle /checkout command
   */
  async handleCheckout(branchNumber: number) {
    return this.replyHandler.handleCheckout(branchNumber);
  }

  /**
   * Handle /merge command
   */
  async handleMerge(branchNumber: number) {
    return this.replyHandler.handleMerge(branchNumber);
  }

  /**
   * Handle /delete-branch command
   */
  async handleDeleteBranch(branchNumber: number, confirm?: boolean) {
    return this.replyHandler.handleDeleteBranch(branchNumber, confirm);
  }
}

/**
 * Create tree sessions manager
 */
export function createTreeSessions(
  app: any,
  config: TreeSessionsConfig
): TreeSessions {
  return new TreeSessions(app, config);
}
