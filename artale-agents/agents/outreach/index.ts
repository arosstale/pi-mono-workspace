import { Pool } from 'pg';
import { Client as DiscordClient } from 'discord.js';
import nodemailer from 'nodemailer';
import TelegramBot from 'node-telegram-bot-api';

interface Lead {
  id: string;
  username: string;
  userId: string;
  email?: string;
  linkedinUrl?: string;
  telegramUsername?: string;
}

interface Templates {
  discord: string;
  linkedin: string;
  email: {
    subject: string;
    body: string;
  };
}

interface PipelineDeal {
  leadId: string;
  status: 'new' | 'contacted' | 'replied' | 'meeting_booked' | 'proposal_sent' | 'negotiating' | 'closed_won' | 'closed_lost' | 'dead';
  channel: 'discord' | 'linkedin' | 'email' | 'telegram';
  lastContact: Date;
  replyScore: number;
  value: number;
}

export class OutreachAgent {
  private db: Pool;
  private discord: DiscordClient;
  private email: nodemailer.Transporter;
  private telegram: TelegramBot;
  private telegramChatId: string;

  constructor(config: {
    databaseUrl: string;
    discordToken: string;
    smtpConfig: {
      host: string;
      port: number;
      user: string;
      pass: string;
    };
    telegramToken: string;
    telegramChatId: string;
  }) {
    this.db = new Pool({ connectionString: config.databaseUrl });
    
    this.discord = new DiscordClient({ intents: [] });
    this.discord.login(config.discordToken);
    
    this.email = nodemailer.createTransport({
      host: config.smtpConfig.host,
      port: config.smtpConfig.port,
      auth: {
        user: config.smtpConfig.user,
        pass: config.smtpConfig.pass
      }
    });
    
    this.telegram = new TelegramBot(config.telegramToken, { polling: false });
    this.telegramChatId = config.telegramChatId;
  }

  async start(): Promise<void> {
    console.log('✅ Outreach Agent started');
    console.log('📤 Multi-channel: Discord, LinkedIn, Email, Telegram');
    
    // Process queue every 60 seconds (rate limiting)
    setInterval(() => this.processQueue(), 60000);
    
    // Check for replies every 30 seconds
    setInterval(() => this.checkReplies(), 30000);
    
    this.processQueue();
    this.checkReplies();
  }

  private async processQueue(): Promise<void> {
    // Rate limits
    const limits = {
      discord: { perHour: 10, perDay: 50 },
      linkedin: { perHour: 5, perDay: 20 },
      email: { perHour: 20, perDay: 100 }
    };
    
    // Check current counts
    const counts = await this.getTodayCounts();
    
    const query = `
      SELECT q.*, l.username, l.user_id, l.email, l.linkedin_url, l.telegram_username
      FROM outreach_queue q
      JOIN leads l ON q.lead_id = l.id
      WHERE q.status = 'pending'
      ORDER BY q.created_at ASC
      LIMIT 10
    `;
    
    const result = await this.db.query(query);
    
    for (const row of result.rows) {
      const lead: Lead = {
        id: row.lead_id,
        username: row.username,
        userId: row.user_id,
        email: row.email,
        linkedinUrl: row.linkedin_url,
        telegramUsername: row.telegram_username
      };
      
      const templates: Templates = JSON.parse(row.templates);
      
      // Choose channel based on available contact info
      const channel = this.chooseChannel(lead);
      
      // Check rate limit
      if (counts[channel] >= limits[channel].perHour) {
        console.log(`⏸️ Rate limit hit for ${channel}, skipping`);
        continue;
      }
      
      try {
        // Send message
        await this.sendMessage(lead, templates, channel);
        
        // Update pipeline
        await this.updatePipeline({
          leadId: lead.id,
          status: 'contacted',
          channel,
          lastContact: new Date(),
          replyScore: 0,
          value: this.estimateValue(lead)
        });
        
        // Mark as sent
        await this.db.query(
          'UPDATE outreach_queue SET status = 'sent', sent_at = NOW(), channel = $2 WHERE lead_id = $1',
          [lead.id, channel]
        );
        
        counts[channel]++;
        
        console.log(`📤 Sent ${channel} message to ${lead.username}`);
        
      } catch (error) {
        console.error(`❌ Failed to send to ${lead.username}:`, error);
        await this.db.query(
          'UPDATE outreach_queue SET status = 'error', error_message = $2 WHERE lead_id = $1',
          [lead.id, error.message]
        );
      }
    }
  }

  private chooseChannel(lead: Lead): 'discord' | 'linkedin' | 'email' | 'telegram' {
    // Priority: Discord (for tech) → LinkedIn (for enterprise) → Email (formal) → Telegram
    if (lead.userId) return 'discord';
    if (lead.linkedinUrl) return 'linkedin';
    if (lead.email) return 'email';
    if (lead.telegramUsername) return 'telegram';
    return 'discord'; // Default
  }

  private async sendMessage(lead: Lead, templates: Templates, channel: string): Promise<void> {
    switch (channel) {
      case 'discord':
        await this.sendDiscordDM(lead.userId!, templates.discord);
        break;
      case 'linkedin':
        // Would need LinkedIn API integration
        console.log(`[LinkedIn] Would send to ${lead.linkedinUrl}: ${templates.linkedin}`);
        break;
      case 'email':
        await this.sendEmail(lead.email!, templates.email);
        break;
      case 'telegram':
        await this.sendTelegram(lead.telegramUsername!, templates.discord); // Use Discord template
        break;
    }
  }

  private async sendDiscordDM(userId: string, message: string): Promise<void> {
    try {
      const user = await this.discord.users.fetch(userId);
      await user.send(message);
    } catch (error) {
      throw new Error(`Discord DM failed: ${error.message}`);
    }
  }

  private async sendEmail(to: string, template: { subject: string; body: string }): Promise<void> {
    await this.email.sendMail({
      from: process.env.EMAIL_FROM,
      to,
      subject: template.subject,
      text: template.body
    });
  }

  private async sendTelegram(username: string, message: string): Promise<void> {
    // Would need to resolve username to chat ID
    console.log(`[Telegram] Would send to @${username}: ${message}`);
  }

  private async checkReplies(): Promise<void> {
    // Poll Discord DMs for replies
    // This would need a more sophisticated implementation with message history
    
    // For now, placeholder: check if any leads have been manually marked as replied
    const query = `
      SELECT * FROM pipeline 
      WHERE status = 'contacted' 
      AND last_contact < NOW() - INTERVAL '3 days'
    `;
    
    const result = await this.db.query(query);
    
    for (const row of result.rows) {
      // Send follow-up
      await this.sendFollowUp(row.lead_id);
    }
  }

  private async sendFollowUp(leadId: string): Promise<void> {
    const followUpTemplates = {
      day3: 'Hey, following up on my previous message. Worth a quick chat?',
      day7: 'Quick check-in — still exploring automation solutions?',
      day14: 'Last follow-up from me. If timing isn\'t right, no worries!'
    };
    
    console.log(`📤 Would send follow-up to ${leadId}`);
  }

  private async updatePipeline(deal: PipelineDeal): Promise<void> {
    const query = `
      INSERT INTO pipeline (lead_id, status, channel, last_contact, reply_score, value)
      VALUES ($1, $2, $3, $4, $5, $6)
      ON CONFLICT (lead_id) DO UPDATE SET
        status = EXCLUDED.status,
        channel = EXCLUDED.channel,
        last_contact = EXCLUDED.last_contact,
        reply_score = EXCLUDED.reply_score
    `;
    
    await this.db.query(query, [
      deal.leadId, deal.status, deal.channel, 
      deal.lastContact, deal.replyScore, deal.value
    ]);
    
    // Check for high-signal
    if (deal.replyScore >= 0.7) {
      await this.alertHighSignal(deal);
    }
  }

  private async alertHighSignal(deal: PipelineDeal): Promise<void> {
    const message = `🎯 HIGH-SIGNAL LEAD

Lead: ${deal.leadId}
Status: ${deal.status}
Estimated Value: €${deal.value}

Next: Respond immediately
    `;
    
    await this.telegram.sendMessage(this.telegramChatId, message);
    console.log('🔔 High-signal alert sent to Telegram');
  }

  private async getTodayCounts(): Promise<Record<string, number>> {
    const query = `
      SELECT channel, COUNT(*) as count
      FROM outreach_queue
      WHERE sent_at >= CURRENT_DATE
      GROUP BY channel
    `;
    
    const result = await this.db.query(query);
    const counts: Record<string, number> = {};
    
    for (const row of result.rows) {
      counts[row.channel] = parseInt(row.count);
    }
    
    return counts;
  }

  private estimateValue(lead: Lead): number {
    // Simple estimation based on signals
    // Would use actual scoring in production
    return 50000; // €50k default
  }

  async stop(): Promise<void> {
    await this.discord.destroy();
    await this.db.end();
  }
}

// Main execution
if (require.main === module) {
  const agent = new OutreachAgent({
    databaseUrl: process.env.DATABASE_URL!,
    discordToken: process.env.DISCORD_TOKEN!,
    smtpConfig: {
      host: process.env.SMTP_HOST!,
      port: parseInt(process.env.SMTP_PORT!),
      user: process.env.SMTP_USER!,
      pass: process.env.SMTP_PASS!
    },
    telegramToken: process.env.TELEGRAM_BOT_TOKEN!,
    telegramChatId: process.env.TELEGRAM_CHAT_ID!
  });

  agent.start().catch(console.error);
  
  process.on('SIGINT', () => {
    console.log('\n🛑 Shutting down Outreach Agent...');
    agent.stop().then(() => process.exit(0));
  });
}