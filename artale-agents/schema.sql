-- Artale 3-Agent System Database Schema

-- Leads table (from Prospector)
CREATE TABLE IF NOT EXISTS leads (
  id VARCHAR(255) PRIMARY KEY,
  source VARCHAR(50) NOT NULL, -- 'discord', 'linkedin', 'email'
  guild_id VARCHAR(255),
  channel_id VARCHAR(255),
  user_id VARCHAR(255),
  username VARCHAR(255) NOT NULL,
  email VARCHAR(255),
  linkedin_url VARCHAR(500),
  telegram_username VARCHAR(255),
  content TEXT NOT NULL,
  score DECIMAL(3,2) NOT NULL,
  signals JSONB,
  timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  status VARCHAR(50) DEFAULT 'new' -- 'new', 'qualified', 'rejected'
);

-- Strategist queue
CREATE TABLE IF NOT EXISTS strategist_queue (
  lead_id VARCHAR(255) PRIMARY KEY REFERENCES leads(id),
  status VARCHAR(50) DEFAULT 'pending', -- 'pending', 'completed', 'error'
  processed_at TIMESTAMP,
  error_message TEXT
);

-- Outreach queue
CREATE TABLE IF NOT EXISTS outreach_queue (
  lead_id VARCHAR(255) PRIMARY KEY REFERENCES leads(id),
  offer_data JSONB,
  templates JSONB,
  status VARCHAR(50) DEFAULT 'pending', -- 'pending', 'sent', 'error'
  channel VARCHAR(50), -- 'discord', 'linkedin', 'email', 'telegram'
  sent_at TIMESTAMP,
  error_message TEXT
);

-- Pipeline (deals)
CREATE TABLE IF NOT EXISTS pipeline (
  lead_id VARCHAR(255) PRIMARY KEY REFERENCES leads(id),
  status VARCHAR(50) DEFAULT 'new', -- 'new', 'contacted', 'replied', 'meeting_booked', 'proposal_sent', 'negotiating', 'closed_won', 'closed_lost', 'dead'
  channel VARCHAR(50),
  last_contact TIMESTAMP,
  reply_score DECIMAL(3,2) DEFAULT 0,
  value INTEGER DEFAULT 0,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Audit log
CREATE TABLE IF NOT EXISTS audit_logs (
  id SERIAL PRIMARY KEY,
  agent VARCHAR(50) NOT NULL,
  action VARCHAR(100) NOT NULL,
  lead_id VARCHAR(255),
  score DECIMAL(3,2),
  user_data JSONB,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for performance
CREATE INDEX idx_leads_status ON leads(status);
CREATE INDEX idx_leads_score ON leads(score);
CREATE INDEX idx_leads_timestamp ON leads(timestamp);
CREATE INDEX idx_strategist_queue_status ON strategist_queue(status);
CREATE INDEX idx_outreach_queue_status ON outreach_queue(status);
CREATE INDEX idx_pipeline_status ON pipeline(status);
CREATE INDEX idx_audit_logs_agent ON audit_logs(agent);
CREATE INDEX idx_audit_logs_created ON audit_logs(created_at);

-- Daily metrics view
CREATE OR REPLACE VIEW daily_metrics AS
SELECT 
  DATE(created_at) as date,
  COUNT(*) as leads_generated,
  COUNT(CASE WHEN status = 'qualified' THEN 1 END) as qualified_leads,
  COUNT(CASE WHEN status = 'contacted' THEN 1 END) as contacted,
  COUNT(CASE WHEN status = 'replied' THEN 1 END) as replies,
  AVG(score) as avg_score
FROM leads
GROUP BY DATE(created_at)
ORDER BY date DESC;

-- Sample data for testing (optional)
-- INSERT INTO leads (id, source, username, content, score, signals) VALUES
-- ('test-1', 'discord', 'testuser', 'cerco automazione BYD', 0.85, '["byd", "italian"]');