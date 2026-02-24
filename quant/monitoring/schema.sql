-- Cross-chain whale monitoring database schema

-- Whale wallets table (tracks addresses across chains)
CREATE TABLE IF NOT EXISTS whale_wallets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    address TEXT NOT NULL,
    chain TEXT NOT NULL CHECK(chain IN ('eth', 'sol')),
    first_seen INTEGER NOT NULL,
    last_seen INTEGER NOT NULL,
    total_tx_value REAL DEFAULT 0,
    tx_count INTEGER DEFAULT 0,
    is_active INTEGER DEFAULT 1,
    created_at INTEGER DEFAULT (strftime('%s', 'now')),
    updated_at INTEGER DEFAULT (strftime('%s', 'now')),
    UNIQUE(address, chain)
);

-- Cross-chain wallet mappings (links same wallet across chains)
CREATE TABLE IF NOT EXISTS cross_chain_mappings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    eth_address TEXT,
    sol_address TEXT,
    correlation_score REAL DEFAULT 0,
    confidence REAL DEFAULT 0,
    evidence TEXT,
    created_at INTEGER DEFAULT (strftime('%s', 'now')),
    updated_at INTEGER DEFAULT (strftime('%s', 'now')),
    UNIQUE(eth_address, sol_address)
);

-- Ethereum whale transactions
CREATE TABLE IF NOT EXISTS eth_whale_txs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tx_hash TEXT NOT NULL UNIQUE,
    from_address TEXT NOT NULL,
    to_address TEXT NOT NULL,
    value_eth REAL NOT NULL,
    value_usd REAL,
    gas_used INTEGER,
    gas_price TEXT,
    tx_type TEXT CHECK(tx_type IN ('transfer', 'swap', 'contract', 'approval')),
    protocol TEXT, -- uniswap, 1inch, etc.
    block_number INTEGER,
    timestamp INTEGER NOT NULL,
    created_at INTEGER DEFAULT (strftime('%s', 'now'))
);

-- Solana whale transactions
CREATE TABLE IF NOT EXISTS sol_whale_txs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tx_sig TEXT NOT NULL UNIQUE,
    from_address TEXT NOT NULL,
    to_address TEXT NOT NULL,
    amount_sol REAL NOT NULL,
    amount_usd REAL,
    fee_lamports INTEGER,
    tx_type TEXT CHECK(tx_type IN ('transfer', 'swap', 'program', 'approval')),
    protocol TEXT, -- jupiter, raydium, etc.
    slot INTEGER,
    timestamp INTEGER NOT NULL,
    created_at INTEGER DEFAULT (strftime('%s', 'now'))
);

-- Cross-chain correlation events
CREATE TABLE IF NOT EXISTS cross_chain_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    eth_tx_id INTEGER,
    sol_tx_id INTEGER,
    correlation_type TEXT CHECK(correlation_type IN ('same_wallet', 'timing', 'pattern')),
    correlation_score REAL NOT NULL,
    time_diff_hours REAL,
    description TEXT,
    created_at INTEGER DEFAULT (strftime('%s', 'now')),
    FOREIGN KEY (eth_tx_id) REFERENCES eth_whale_txs(id),
    FOREIGN KEY (sol_tx_id) REFERENCES sol_whale_txs(id)
);

-- Whale alerts (generated for significant cross-chain activity)
CREATE TABLE IF NOT EXISTS whale_alerts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    alert_type TEXT NOT NULL CHECK(alert_type IN ('large_transfer', 'cross_chain_move', 'unusual_pattern')),
    chain TEXT NOT NULL,
    address TEXT NOT NULL,
    amount REAL,
    currency TEXT,
    description TEXT,
    correlation_id INTEGER,
    is_resolved INTEGER DEFAULT 0,
    created_at INTEGER DEFAULT (strftime('%s', 'now')),
    FOREIGN KEY (correlation_id) REFERENCES cross_chain_events(id)
);

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_whale_wallets_address ON whale_wallets(address);
CREATE INDEX IF NOT EXISTS idx_whale_wallets_chain ON whale_wallets(chain);
CREATE INDEX IF NOT EXISTS idx_whale_wallets_active ON whale_wallets(is_active);
CREATE INDEX IF NOT EXISTS idx_whale_wallets_last_seen ON whale_wallets(last_seen);

CREATE INDEX IF NOT EXISTS idx_cross_chain_mappings_eth ON cross_chain_mappings(eth_address);
CREATE INDEX IF NOT EXISTS idx_cross_chain_mappings_sol ON cross_chain_mappings(sol_address);
CREATE INDEX IF NOT EXISTS idx_cross_chain_mappings_score ON cross_chain_mappings(correlation_score);

CREATE INDEX IF NOT EXISTS idx_eth_whale_txs_from ON eth_whale_txs(from_address);
CREATE INDEX IF NOT EXISTS idx_eth_whale_txs_to ON eth_whale_txs(to_address);
CREATE INDEX IF NOT EXISTS idx_eth_whale_txs_type ON eth_whale_txs(tx_type);
CREATE INDEX IF NOT EXISTS idx_eth_whale_txs_timestamp ON eth_whale_txs(timestamp);

CREATE INDEX IF NOT EXISTS idx_sol_whale_txs_from ON sol_whale_txs(from_address);
CREATE INDEX IF NOT EXISTS idx_sol_whale_txs_to ON sol_whale_txs(to_address);
CREATE INDEX IF NOT EXISTS idx_sol_whale_txs_type ON sol_whale_txs(tx_type);
CREATE INDEX IF NOT EXISTS idx_sol_whale_txs_timestamp ON sol_whale_txs(timestamp);

CREATE INDEX IF NOT EXISTS idx_cross_chain_events_type ON cross_chain_events(correlation_type);
CREATE INDEX IF NOT EXISTS idx_cross_chain_events_score ON cross_chain_events(correlation_score);
CREATE INDEX IF NOT EXISTS idx_cross_chain_events_created ON cross_chain_events(created_at);

CREATE INDEX IF NOT EXISTS idx_whale_alerts_chain ON whale_alerts(chain);
CREATE INDEX IF NOT EXISTS idx_whale_alerts_type ON whale_alerts(alert_type);
CREATE INDEX IF NOT EXISTS idx_whale_alerts_resolved ON whale_alerts(is_resolved);
CREATE INDEX IF NOT EXISTS idx_whale_alerts_created ON whale_alerts(created_at);
