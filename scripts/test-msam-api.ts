#!/usr/bin/env node

/**
 * MSAM REST API Integration Test
 * TypeScript version for pi-agent ecosystem
 */

import { request } from 'http';

const API_URL = 'http://localhost:3001';
const API_BASE = '/v1';

interface Response {
  status: number;
  data: any;
}

function httpRequest(
  method: string,
  endpoint: string,
  data?: any
): Promise<Response> {
  return new Promise((resolve, reject) => {
    const url = new URL(API_URL + API_BASE + endpoint);
    const options: any = {
      hostname: url.hostname,
      port: url.port || 8000,
      path: url.pathname,
      method,
      headers: {
        'Content-Type': 'application/json',
      },
    };

    const req = request(options, (res) => {
      let body = '';
      res.on('data', chunk => body += chunk);
      res.on('end', () => {
        try {
          const responseData = body ? JSON.parse(body) : {};
          resolve({ status: res.statusCode || 500, data: responseData });
        } catch (e) {
          resolve({ status: res.statusCode || 500, data: body });
        }
      });
    });

    req.on('error', reject);

    if (data) {
      req.write(JSON.stringify(data));
    }
    req.end();
  });
}

async function testStore(): Promise<boolean> {
  console.log('📤 Testing POST /store...');
  try {
    const result = await httpRequest('POST', '/store', {
      content: 'User tested MSAM REST API successfully (TypeScript)',
      stream: 'episodic',
      arousal: 0.6,
      valence: 0.7,
      encoding_confidence: 0.9,
    });
    console.log(`  Status: ${result.status}`);
    console.log(`  Response: ${JSON.stringify(result.data, null, 2).substring(0, 200)}...`);
    return result.status === 200;
  } catch (error: any) {
    console.log(`  Error: ${error.message}`);
    return false;
  }
}

async function testQuery(): Promise<boolean> {
  console.log('\n📥 Testing POST /query...');
  try {
    const result = await httpRequest('POST', '/query', {
      query: 'What do you know about MSAM REST API TypeScript?'
    });
    console.log(`  Status: ${result.status}`);
    if (result.status === 200) {
      const data = result.data;
      console.log(`  Confidence Tier: ${data.confidence_tier}`);
      console.log(`  Total Tokens: ${data.total_tokens}`);
      console.log(`  Items Returned: ${data.items_returned}`);
      console.log(`  Latency: ${data.latency_ms}ms`);
      if (data.atoms && data.atoms.length > 0) {
        console.log(`  First Atom: ${data.atoms[0].content.substring(0, 80)}...`);
      }
    }
    return result.status === 200;
  } catch (error: any) {
    console.log(`  Error: ${error.message}`);
    return false;
  }
}

async function testContext(): Promise<boolean> {
  console.log('\n📋 Testing POST /context...');
  try {
    const result = await httpRequest('POST', '/context', {});
    console.log(`  Status: ${result.status}`);
    if (result.status === 200) {
      const data = result.data;
      console.log(`  Total Tokens: ${data.total_tokens}`);
      console.log(`  Method: ${data.method}`);
    }
    return result.status === 200;
  } catch (error: any) {
    console.log(`  Error: ${error.message}`);
    return false;
  }
}

async function testStats(): Promise<boolean> {
  console.log('\n📊 Testing GET /stats...');
  try {
    const result = await httpRequest('GET', '/stats');
    console.log(`  Status: ${result.status}`);
    if (result.status === 200) {
      const data = result.data;
      console.log(`  Total Atoms: ${data.total_atoms}`);
      console.log(`  Active Atoms: ${data.active_atoms}`);
      console.log(`  Est Tokens: ${data.est_active_tokens}`);
    }
    return result.status === 200;
  } catch (error: any) {
    console.log(`  Error: ${error.message}`);
    return false;
  }
}

async function main(): Promise<number> {
  console.log('🧪 MSAM REST API Integration Test (TypeScript)\n');
  console.log(`API URL: ${API_URL}`);
  console.log('='.repeat(50));

  const results: [string, boolean][] = [
    ['POST /store', await testStore()],
    ['POST /query', await testQuery()],
    ['POST /context', await testContext()],
    ['GET /stats', await testStats()],
  ];

  console.log('\n' + '='.repeat(50));
  console.log('📋 Test Results:');
  for (const [endpoint, success] of results) {
    const status = success ? '✅ PASS' : '❌ FAIL';
    console.log(`  ${status} ${endpoint}`);
  }

  const allPass = results.every(([, success]) => success);
  if (allPass) {
    console.log('\n✅ All tests passed!');
  } else {
    console.log('\n❌ Some tests failed');
  }

  return allPass ? 0 : 1;
}

main().catch((error: any) => {
  console.log(`\n❌ ERROR: ${error.message}`);
  if (error.code === 'ECONNREFUSED') {
    console.log('   MSAM server not running');
    console.log('   Start it with: cd ~/msam && python -m msam.server');
  }
  process.exit(1);
});
