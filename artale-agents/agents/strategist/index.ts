import { Pool } from 'pg';
import { OpenAI } from 'openai';
import fs from 'fs';
import path from 'path';

interface Lead {
  id: string;
  username: string;
  content: string;
  score: number;
  signals: string[];
}

interface Offer {
  vertical: string;
  valueProp: string;
  differentiators: string[];
  pricing: string;
  nextSteps: string;
}

interface MessageTemplate {
  discord: string;
  linkedin: string;
  email: {
    subject: string;
    body: string;
  };
}

export class StrategistAgent {
  private db: Pool;
  private openai: OpenAI;
  private kbPath: string;

  constructor(config: {
    databaseUrl: string;
    openaiApiKey: string;
    kbPath: string;
  }) {
    this.db = new Pool({ connectionString: config.databaseUrl });
    this.openai = new OpenAI({ apiKey: config.openaiApiKey });
    this.kbPath = config.kbPath;
  }

  async start(): Promise<void> {
    console.log('✅ Strategist Agent started');
    console.log('📚 KB Path:', this.kbPath);
    
    // Poll for new leads every 30 seconds
    setInterval(() => this.processQueue(), 30000);
    
    // Initial check
    this.processQueue();
  }

  private async processQueue(): Promise<void> {
    const query = `
      SELECT l.* FROM strategist_queue q
      JOIN leads l ON q.lead_id = l.id
      WHERE q.status = 'pending'
      ORDER BY l.score DESC
      LIMIT 5
    `;
    
    const result = await this.db.query(query);
    
    for (const row of result.rows) {
      const lead: Lead = {
        id: row.id,
        username: row.username,
        content: row.content,
        score: row.score,
        signals: JSON.parse(row.signals)
      };
      
      console.log(`🧠 Processing lead: ${lead.username} (score: ${lead.score})`);
      
      try {
        // 1. Determine vertical
        const vertical = this.determineVertical(lead);
        
        // 2. Query KB for relevant context
        const context = await this.queryKB(vertical, lead);
        
        // 3. Craft offer
        const offer = await this.craftOffer(lead, vertical, context);
        
        // 4. Generate message templates
        const templates = await this.generateTemplates(lead, offer, vertical);
        
        // 5. Queue for Outreach Agent
        await this.queueOutreach(lead, offer, templates);
        
        // 6. Mark as processed
        await this.db.query(
          'UPDATE strategist_queue SET status = 'completed', processed_at = NOW() WHERE lead_id = $1',
          [lead.id]
        );
        
        console.log(`✅ Offer crafted for ${lead.username}`);
        
      } catch (error) {
        console.error(`❌ Error processing lead ${lead.id}:`, error);
        await this.db.query(
          'UPDATE strategist_queue SET status = 'error', error_message = $2 WHERE lead_id = $1',
          [lead.id, error.message]
        );
      }
    }
  }

  private determineVertical(lead: Lead): string {
    const signals = lead.signals;
    
    if (signals.includes('byd') || signals.includes('fleet')) {
      return 'automotive';
    }
    if (signals.includes('industria') || signals.includes('factory')) {
      return 'industrial';
    }
    if (signals.includes('security') || signals.includes('sicurezza')) {
      return 'security';
    }
    if (signals.includes('firefighter') || signals.includes('vigili')) {
      return 'firefighter';
    }
    
    return 'automotive'; // Default
  }

  private async queryKB(vertical: string, lead: Lead): Promise<string> {
    // Simple file-based KB query (replace with vector DB for production)
    const kbFiles = {
      automotive: ['byd-australia-case-study.md', 'automotive-automation-playbook.md'],
      industrial: ['industrial-iot-operations.md', 'factory-optimization.md'],
      security: ['security-systems-integration.md'],
      firefighter: ['firefighter-ems-dispatch.md']
    };
    
    const files = kbFiles[vertical] || kbFiles.automotive;
    let context = '';
    
    for (const file of files) {
      const filePath = path.join(this.kbPath, '03-verticals', file);
      if (fs.existsSync(filePath)) {
        context += fs.readFileSync(filePath, 'utf8') + '\n\n';
      }
    }
    
    // Also check case studies
    const caseStudyPath = path.join(this.kbPath, '02-case-studies', 'byd-australia-case-study.md');
    if (fs.existsSync(caseStudyPath)) {
      context += fs.readFileSync(caseStudyPath, 'utf8') + '\n\n';
    }
    
    return context || 'No KB context available';
  }

  private async craftOffer(lead: Lead, vertical: string, context: string): Promise<Offer> {
    const verticalValueProps = {
      automotive: 'BYD-certified fleet automation — real-time tracking, predictive maintenance, automated reporting.',
      industrial: 'Industria 4.0 AI automation — factory floor optimization, predictive maintenance, quality control.',
      security: 'Smart security automation — surveillance, access control, incident response AI.',
      firefighter: 'Emergency dispatch AI — resource optimization, route planning, automated reporting.'
    };

    const differentiators = [
      'BYD-certified partner (Australia case study completed)',
      'Local Italy presence (not offshore)',
      'Multi-provider AI (not locked to single vendor)',
      'Operations focus (not just chatbots)',
      'Measurable ROI (€100k+ savings typical)'
    ];

    const pricingTiers = {
      audit: '€2,500',
      pilot: '€15,000',
      platform: '€50,000/year'
    };

    return {
      vertical,
      valueProp: verticalValueProps[vertical],
      differentiators,
      pricing: `Audit: ${pricingTiers.audit} | Pilot: ${pricingTiers.pilot} | Platform: ${pricingTiers.platform}`,
      nextSteps: '15-min call to assess fit'
    };
  }

  private async generateTemplates(lead: Lead, offer: Offer, vertical: string): Promise<MessageTemplate> {
    const isItalian = lead.content.match(/cerco|automazione|flotta|gestione/i);
    
    if (isItalian) {
      return {
        discord: `Ciao ${lead.username}, ho visto il tuo messaggio su ${vertical}. 

Abbiamo appena consegnato un sistema simile per BYD in Australia — ${offer.valueProp}

Risultato: 30% riduzione costi operativi.

Possiamo fare una call veloce di 15 min per vedere se ha senso anche per voi?`,

        linkedin: `Ciao ${lead.username},

Ho notato il tuo interesse per ${vertical}. 

Come partner certificato BYD, abbiamo implementato automazione operations in Australia con risultati misurabili.

${offer.valueProp}

Vale una breve call per esplorare il potenziale?

Artale`,

        email: {
          subject: `Automazione ${vertical} — caso studio BYD Australia`,
          body: `Ciao ${lead.username},

Ho seguito con interesse la conversazione su ${vertical}.

Voglio condividere un caso recente: BYD Australia, automazione flotta con AI operations.

${offer.valueProp}

Risultati:
• 30% riduzione costi gestionali
• Zero downtime operativo
• Reporting automatizzato compliance

Offriamo:
${offer.pricing}

Vale una call esplorativa di 15 minuti?

Cordiali saluti,
Artale
[Calendar link]`
        }
      };
    } else {
      // English templates
      return {
        discord: `Hey ${lead.username}, saw your post about ${vertical}.

We just delivered a similar system for BYD in Australia — ${offer.valueProp}

Result: 30% ops cost reduction.

Worth a 15-min call to see if it applies to your setup?`,

        linkedin: `Hi ${lead.username},

Noticed your interest in ${vertical}.

As a BYD-certified partner, we've implemented operations automation in Australia with measurable results.

${offer.valueProp}

Worth a brief call to explore the potential?

Artale`,

        email: {
          subject: `${vertical} Automation — BYD Australia Case Study`,
          body: `Hi ${lead.username},

Following the conversation about ${vertical}.

Wanted to share a recent case: BYD Australia, fleet automation with AI operations.

${offer.valueProp}

Results:
• 30% reduction in operational costs
• Zero operational downtime
• Automated compliance reporting

We offer:
${offer.pricing}

Worth an exploratory 15-minute call?

Best,
Artale
[Calendar link]`
        }
      };
    }
  }

  private async queueOutreach(lead: Lead, offer: Offer, templates: MessageTemplate): Promise<void> {
    const query = `
      INSERT INTO outreach_queue (lead_id, offer_data, templates, status, created_at)
      VALUES ($1, $2, $3, 'pending', NOW())
    `;
    
    await this.db.query(query, [
      lead.id,
      JSON.stringify(offer),
      JSON.stringify(templates)
    ]);
    
    console.log(`📤 Queued ${lead.username} for Outreach Agent`);
  }

  async stop(): Promise<void> {
    await this.db.end();
  }
}

// Main execution
if (require.main === module) {
  const agent = new StrategistAgent({
    databaseUrl: process.env.DATABASE_URL!,
    openaiApiKey: process.env.OPENAI_API_KEY!,
    kbPath: process.env.KB_PATH || './kb'
  });

  agent.start().catch(console.error);
  
  process.on('SIGINT', () => {
    console.log('\n🛑 Shutting down Strategist Agent...');
    agent.stop().then(() => process.exit(0));
  });
}