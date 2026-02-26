export interface LeadContext {
  discordHandle: string;
  content: string;
  server: string;
  channel: string;
  score: number;
}

/**
 * Generate contextual DM based on lead's original post
 * Returns: formatted DM text
 */
export function generateDM(lead: LeadContext): string {
  const text = lead.content;
  
  // Extract what they asked for
  const asks = extractAsks(text);
  const budget = extractBudget(text);
  
  return `Hey — I saw your post about ${asks.join(', ')}.

I help agencies automate their lead-gen with Discord agents. You're looking for ${budget ? `a solution within ${budget}` : 'help with automation'}. Here's what I do:

1. Find users in Discord communities who ask for help
2. Qualify them by budget/urgency  
3. Send contextual DMs
4. Hand over to you when they're ready to talk

You handle the closing. I handle the automation.

Worth setting up a call? Or want to see how this runs first?`;
}

/**
 * Generate follow-up DM (DM2 after 24h)
 * Returns: follow-up text
 */
export function generateFollowup(lead: LeadContext): string {
  return `Hey — checking in on your post about ${extractAsks(lead.content)[0] || 'automation'}.

The context I was seeing was you looking for help building or automating something. My agent finds leads in Discord, qualifies them, and I hand over when they're ready to buy.

If you want to see the results, I can walk you through the workflow — it saves you time finding clients, you just focus on closing them.

Let me know if this is still on your radar?`;
}

/**
 * Extract what they asked for from their post
 */
function extractAsks(text: string): string[] {
  const lowerText = text.toLowerCase();
  const asks: string[] = [];

  if (lowerText.includes('discord')) asks.push('Discord agents');
  if (lowerText.includes('agent')) asks.push('agent systems');
  if (lowerText.includes('automation')) asks.push('automation');
  if (lowerText.includes('lead')) asks.push('lead generation');
  if (lowerText.includes('workflow')) asks.push('workflows');
  if (lowerText.includes('bot')) asks.push('bots');
  if (lowerText.includes('typescript')) asks.push('TypeScript');

  return asks.length > 0 ? asks : ['building/automating something'];
}

/**
 * Extract budget/urgency from their post
 */
function extractBudget(text: string): string | null {
  const lowerText = text.toLowerCase();

  // Budget mentions
  const budgetMatch = text.match(/(\$[\d,]+)/);
  if (budgetMatch) return budgetMatch[0];

  // Urgency mentions
  if (lowerText.includes('budget')) return 'a defined budget';
  if (lowerText.includes('urgently') || lowerText.includes('asap')) return 'urgent needs';
  if (lowerText.includes('timeline')) return 'a timeline';

  return null;
}

/**
 * Mock DM function (for testing)
 * In production, this calls the Discord API
 */
export async function sendDiscordDM(userId: string, text: string): Promise<void> {
  // In production: send via Discord API
  console.log(`[DM SENT] To: ${userId}`);
  console.log(`[DM CONTENT] ${text}`);
  
  // Actual implementaton would be:
  // const client = new DiscordClient({ intents: GatewayIntentBits.DirectMessages });
  // await client.login(process.env.DISCORD_TOKEN!);
  // const user = await client.users.fetch(userId);
  // await user.send(text);
  // await client.destroy();
}

/**
 * Queue DM to outbox (for heartbeat to send)
 */
export function queueOutboundDM(userId: string, text: string): void {
  const outboxDir = path.join(process.cwd(), '.data', 'outbox');
  
  if (!fs.existsSync(outboxDir)) {
    fs.mkdirSync(outboxDir, { recursive: true });
  }
  
  const outFile = path.join(outboxDir, `dm_${userId}_${Date.now()}.txt`);
  fs.writeFileSync(outFile, text, 'utf8');
}