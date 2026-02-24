# OpenClaw Memory TypeScript Skill

This skill allows OpenClaw agents to interface with the enterprise-grade TypeScript memory system.

## Usage

```javascript
const { loadConfig, getLogger, getSecretsManager, BackupManager } = require('/home/majinbu/pi-mono-workspace/openclaw-memory-ts/dist/index.js');

// 1. Load config
const config = await loadConfig();

// 2. Get secrets
const secrets = getSecretsManager(config);
const apiKey = secrets.get('MY_API_KEY');

// 3. Backup memory
const backup = new BackupManager(config, getLogger('backup', config));
await backup.backup();
```

## MSAM Integration

```javascript
const { MSAMClient } = require('/home/majinbu/pi-mono-workspace/openclaw-memory-ts/dist/index.js');
const client = new MSAMClient(config);

// Store memory
await client.store("Project X deadline is Friday", "episodic");

// Recall
const context = await client.getContext("When is the deadline?");
console.log(context.synthesis);
```
