import { Client, GatewayIntentBits, Partials } from 'discord.js';
import { Pool } from 'pg';
import { logAuditEvent } from '../lib/audit';

interface Lead {
  id: string;
  source: 'discord';
  guildId: string;
  channelId: string;
  userId: string;
  username: string;
  content: string;
  score: number;
  signals: string[];
  timestamp: Date;
  status: 'new' | 'qualified' | 'rejected';
}

// Scoring weights
const SCORE_WEIGHTS = {
  bydMention: 0.4,
  fleetSize: 0.3,
  automationKeyword: 0.15,
  italianLanguage: 0.1,
  urgencySignal: 0.2,
  budgetMention: 0.25
};

// Keywords to track
const KEYWORDS = {
  byd: ['byd', 'byd auto', 'byd italia', 'byd dealer'],
  automation: ['automazione', 'automazione industriale', 'fleet management', 
               'gestione flotta', 'industria 4.0', 'iot', 'operations ai'],
  urgency: ['urgente', 'asap', 'immediato', 'subito', 'cerco', 'serve'],
  budget: ['budget', 'preventivo', 'costo', 'investimento', '€', 'euro'],
  fleet: ['flotta', 'veicoli', 'auto elettriche', 'fleet', 'vehicles']
};

export class ProspectorAgent {
  private client: Client;
  private db: Pool;
  private monitoredGuilds: string[];

  constructor(config: { 
    discordToken: string;
    databaseUrl: string;
    guildIds: string[];
  }) {
    this.client = new Client({
      intents: [
        GatewayIntentBits.Guilds,
        GatewayIntentBits.GuildMessages,
        GatewayIntentBits.MessageContent,
        GatewayIntentBits.GuildMembers
      ],
      partials: [Partials.Channel]
    });

    this.db = new Pool({ connectionString: config.databaseUrl });
    this.monitoredGuilds = config.guildIds;
  }

  async start(): Promise<void> {
    this.client.on('messageCreate', this.handleMessage.bind(this));
    
    this.client.on('ready', () => {
      console.log(`✅ Prospector Agent logged in as ${this.client.user?.tag}`);
      console.log(`📡 Monitoring ${this.monitoredGuilds.length} guilds`);
    });

    await this.client.login(process.env.DISCORD_TOKEN);
  }

  private async handleMessage(message: any): Promise<void> {
    // Skip if not in monitored guilds
    if (!this.monitoredGuilds.includes(message.guildId)) return;
    
    // Skip bot messages
    if (message.author.bot) return;
    
    // Skip if not in relevant channels (optional filter)
    const relevantChannels = ['general', 'jobs', 'opportunities', 'automazione'];
    if (!relevantChannels.some(c => message.channel.name.includes(c))) return;

    const content = message.content.toLowerCase();
    
    // Score the message
    const score = this.calculateScore(content, message);
    
    if (score >= 0.7) {
      const lead: Lead = {
        id: `discord-${message.id}`,
        source: 'discord',
        guildId: message.guildId,
        channelId: message.channelId,
        userId: message.author.id,
        username: message.author.username,
        content: message.content,
        score,
        signals: this.extractSignals(content),
        timestamp: new Date(),
        status: 'qualified'
      };

      // Save to database
      await this.saveLead(lead);
      
      // Trigger Strategist Agent
      await this.triggerStrategist(lead);
      
      // Log
      await logAuditEvent({
        agent: 'prospector',
        action: 'lead_qualified',
        leadId: lead.id,
        score,
        user: message.author.username
      });

      console.log(`🎯 Qualified lead: ${message.author.username} (score: ${score.toFixed(2)})`);
    }
  }

  private calculateScore(content: string, message: any): number {
    let score = 0;
    const signals: string[] = [];

    // BYD mention
    if (KEYWORDS.byd.some(k => content.includes(k))) {
      score += SCORE_WEIGHTS.bydMention;
      signals.push('byd_mention');
    }

    // Automation keywords
    if (KEYWORDWORDS.automation.some(k => content.includes(k))) {
      score += SCORE_WEIGHTS.automationKeyword;
      signals.push('automation_keyword');
    }

    // Fleet reference
    if (KEYWORDS.fleet.some(k => content.includes(k))) {
      score += SCORE_WEIGHTS.fleetSize;
      signals.push('fleet_reference');
    }

    // Urgency
    if (KEYWORDS.urgency.some(k => content.includes(k))) {
      score += SCORE_WEIGHTS.urgencySignal;
      signals.push('urgency_signal');
    }

    // Budget mention
    if (KEYWORDS.budget.some(k => content.includes(k))) {
      score += SCORE_WEIGHTS.budgetMention;
      signals.push('budget_mentioned');
    }

    // Italian language (simple heuristic)
    const italianWords = ['cerco', 'automazione', 'flotta', 'gestione', 'preventivo'];
    if (italianWords.some(w => content.includes(w))) {
      score += SCORE_WEIGHTS.italianLanguage;
      signals.push('italian_language');
    }

    return Math.min(score, 1.0); // Cap at 1.0
  }

  private extractSignals(content: string): string[] {
    const signals: string[] = [];
    
    Object.entries(KEYWORDS).forEach(([category, keywords]) => {
      if (keywords.some(k => content.includes(k))) {
        signals.push(category);
      }
    });
    
    return signals;
  }

  private async saveLead(lead: Lead): Promise<void> {
    const query = `
      INSERT INTO leads (id, source, guild_id, channel_id, user_id, username, 
                        content, score, signals, timestamp, status)
      VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11)
      ON CONFLICT (id) DO NOTHING
    `;
    
    await this.db.query(query, [
      lead.id, lead.source, lead.guildId, lead.channelId,
      lead.userId, lead.username, lead.content, lead.score,
      JSON.stringify(lead.signals), lead.timestamp, lead.status
    ]);
  }

  private async triggerStrategist(lead: Lead): Promise<void> {
    // Queue message for Strategist Agent
    const query = `
      INSERT INTO strategist_queue (lead_id, status, created_at)
      VALUES ($1, 'pending', NOW())
    `;
    await this.db.query(query, [lead.id]);
    
    // Could also use Redis, RabbitMQ, or direct IPC
    console.log(`📤 Queued lead ${lead.id} for Strategist Agent`);
  }

  async stop(): Promise<void> {
    await this.client.destroy();
    await this.db.end();
  }
}

// Main execution
if (require.main === module) {
  const agent = new ProspectorAgent({
    discordToken: process.env.DISCORD_TOKEN!,
    databaseUrl: process.env.DATABASE_URL!,
    guildIds: process.env.DISCORD_GUILD_IDS?.split(',') || []
  });

  agent.start().catch(console.error);
  
  // Graceful shutdown
  process.on('SIGINT', () => {
    console.log('\n🛑 Shutting down Prospector Agent...');
    agent.stop().then(() => process.exit(0));
  });
}