# MSAM REST API Test - TypeScript

## Quick Start

```bash
cd ~/pi-mono-workspace/scripts

# Install dependencies
npm install

# Run tests
npm test
```

## Requirements

- Node.js v18+
- TypeScript v5+
- ts-node

## Script Details

**File:** `test-msam-api.ts`
**Purpose:** Test MSAM REST API endpoints (TypeScript)

## Endpoints Tested

| Method | Endpoint | Description |
|--------|-----------|-------------|
| POST | `/v1/store` | Store memory atom |
| POST | `/v1/query` | Query memories |
| POST | `/v1/context` | Get session context |
| GET | `/v1/stats` | Get database statistics |

## Example Output

```
🧪 MSAM REST API Integration Test (TypeScript)

API URL: http://localhost:3001
==================================================
📤 Testing POST /store...
  Status: 200
  Response: { "stored": true, "atom_id": "...", ... }
📥 Testing POST /query...
  Status: 200
  Confidence Tier: high
  Total Tokens: 289
  Items Returned: 11
  Latency: 552.68ms
📋 Testing POST /context...
  Status: 200
  Total Tokens: 228
  Method: shannon_optimized
📊 Testing GET /stats...
  Status: 200
  Total Atoms: 75
  Active Atoms: 75
  Est Tokens: 1333

==================================================
📋 Test Results:
  ✅ PASS POST /store
  ✅ PASS POST /query
  ✅ PASS POST /context
  ✅ PASS GET /stats

✅ All tests passed!
```

## Error Handling

If MSAM server is not running:

```
❌ ERROR: connect ECONNREFUSED 127.0.0.1:3001
   MSAM server not running
   Start it with: cd ~/msam && python -m msam.server
```

## Integration Example

```typescript
import { request } from 'http';

async function queryMSAM(query: string) {
  const result = await httpRequest('POST', '/v1/query', { query });

  if (result.status === 200) {
    const { confidence_tier, atoms, total_tokens } = result.data;

    if (confidence_tier === 'high') {
      const memories = atoms.map(a => a.content).join('\n');
      return `Context:\n${memories}\n\n`;
    } else if (confidence_tier === 'none') {
      return ''; // No relevant memories
    } else {
      return `Context (low confidence):\n${atoms[0].content}\n\n`;
    }
  }

  return '';
}
```

## Python vs TypeScript

| Feature | Python | TypeScript |
|---------|--------|------------|
| Dependencies | requests | native http |
| Runtime | CPython | Node.js |
| Type Safety | No | Yes |
| Compilation | No | ts-node |
| Line Count | 115 | 150 |

Both scripts are functionally equivalent. Use TypeScript for pi-agent ecosystem compatibility.
