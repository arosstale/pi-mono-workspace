import Database from 'better-sqlite3';
import path from 'path';

export interface LeadData {
  id: string;
  discordHandle: string;
  userId: string;
  content: string;
  serverName: string;
  channelName: string;
  timestamp: string;
  score: number;
  reason: string;
  confidence: string;
  dm1Sent?: string;
  dm1Response?: string;
  dm2Sent?: string;
  dm2Response?: string;
  status: 'new' | 'contacted1' | 'contacted2' | 'handover' | 'won' | 'lost' | 'blocked';
}

const dbPath = path.join(process.cwd(), 'leads.db');
const db = new Database(dbPath);

// Initialize database
db.exec(`
  CREATE TABLE IF NOT EXISTS leads (
    id TEXT PRIMARY KEY,
    discordHandle TEXT,
    userId TEXT,
    content TEXT,
    serverName TEXT,
    channelName TEXT,
    timestamp TEXT,
    score INTEGER,
    reason TEXT,
    confidence TEXT,
    dm1Sent TEXT,
    dm1Response TEXT,
    dm2Sent TEXT,
    dm2Response TEXT,
    status TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
  )
`);

/**
 * Save a lead to the database
 * Returns: created lead data
 */
export function saveLead(lead: Omit<LeadData, 'id' | 'created_at'>): LeadData {
  const id = `lead_${Date.now()}_${lead.userId}`;
  
  const stmt = db.prepare(`
    INSERT INTO leads (
      id, discordHandle, userId, content, serverName, channelName,
      timestamp, score, reason, confidence, dm1Sent, dm1Response,
      dm2Sent, dm2Response, status
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
  `).run(
    id,
    lead.discordHandle,
    lead.userId,
    lead.content,
    lead.serverName,
    lead.channelName,
    lead.timestamp,
    lead.score,
    lead.reason,
    lead.confidence,
    lead.dm1Sent || null,
    lead.dm1Response || null,
    lead.dm2Sent || null,
    lead.dm2Response || null,
    lead.status
  );

  return {
    ...lead,
    id,
    created_at: new Date().toISOString()
  };
}

/**
 * Get all leads filtered by status
 */
export function getLeadsByStatus(status: string): LeadData[] {
  const stmt = db.prepare('SELECT * FROM leads WHERE status = ? ORDER BY created_at DESC');
  return stmt.all(status);
}

/**
 * Get a specific lead by Discord user ID
 */
export function getLeadByUserId(userId: string): LeadData | undefined {
  const stmt = db.prepare('SELECT * FROM leads WHERE userId = ?');
  return stmt.get(userId);
}

/**
 * Update lead DM1 response
 */
export function updateLeadDM1Response(userId: string, response: string): void {
  const stmt = db.prepare('UPDATE leads SET dm1Response = ?, status = ? WHERE userId = ?');
  stmt.run(response, 'contacted1', userId);
}

/**
 * Update lead DM2 response
 */
export function updateLeadDM2Response(userId: string, response: string): void {
  const stmt = db.prepare('UPDATE leads SET dm2Response = ?, status = ? WHERE userId = ?');
  stmt.run(response, 'contacted2', userId);
}

/**
 * Mark lead as blocked (user said not interested/stop)
 */
export function blockLead(userId: string, reason: string = 'not interested'): void {
  const stmt = db.prepare('UPDATE leads SET status = ? WHERE userId = ?');
  stmt.run('blocked', userId);
}

/**
 * Get lead statistics
 */
export function getStats() {
  const stmt = db.prepare(`
    SELECT 
      status,
      COUNT(*) as count 
    FROM leads 
    GROUP BY status
  `);
  return stmt.all();
}