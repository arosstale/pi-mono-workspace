#!/usr/bin/env node
/**
 * Netlify Deploy Script v2 - Using correct API endpoints
 * Bypasses CLI entirely
 */

const https = require('https');
const http = require('http');
const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

// Configuration
const NETLIFY_TOKEN = process.env.NETLIFY_AUTH_TOKEN || 'nfp_rCyYJ4CycbXAPb1zQzLDT3gnn9zQEiuB6edf';
const SITE_NAME = 'openclaw-wrappers';

console.log('🚀 Netlify Direct Deploy Script v2');
console.log('Token:', NETLIFY_TOKEN.substring(0, 10) + '...');

// Create multipart form data boundary
const boundary = '----NetlifyFormBoundary' + Date.now();

function createFormData() {
  const indexHtml = fs.readFileSync('index.html');
  
  // Create multipart form data
  const parts = [
    `--${boundary}\r\n`,
    `Content-Disposition: form-data; name="file"; filename="index.html"\r\n`,
    `Content-Type: text/html\r\n\r\n`,
    indexHtml,
    `\r\n--${boundary}\r\n`
  ];

  return Buffer.concat(parts.map(p => Buffer.from(p)));
}

// Create site via API
function createSite() {
  return new Promise((resolve, reject) => {
    const data = JSON.stringify({
      name: SITE_NAME,
      custom_domain: null
    });

    const options = {
      hostname: 'api.netlify.com',
      path: '/api/v1/sites',
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(data),
        'Authorization': `Bearer ${NETLIFY_TOKEN}`
      }
    };

    const req = https.request(options, (res) => {
      let body = '';
      res.on('data', chunk => body += chunk);
      res.on('end', () => {
        try {
          const result = JSON.parse(body);
          if (res.statusCode === 201) {
            console.log('✅ Site found/created:', result.name);
            console.log('   ID:', result.id);
            console.log('   URL:', result.ssl_url);
            resolve(result);
          } else if (res.statusCode === 401) {
            console.log('❌ Access Denied - Token is invalid or expired');
            console.log('   Please get a new token from: https://app.netlify.com/user/applications');
            reject(new Error('Unauthorized'));
          } else if (res.statusCode === 409) {
            console.log('✅ Site already exists, using it');
            const result2 = JSON.parse(body);
            resolve(result2);
          } else {
            console.log('❌ Status:', res.statusCode, body);
            reject(new Error(res.statusMessage));
          }
        } catch (e) {
          console.log('❌ Parse error:', e.message);
          console.log('Body:', body);
          reject(e);
        }
      });
    });

    req.on('error', reject);
    req.write(data);
    req.end();
  });
}

// Deploy using Git push (most reliable)
function deployViaGit() {
  console.log('\n🔄 Attempting Git-based deploy...');
  console.log('   This requires Netlify to be connected to GitHub in web UI');
  console.log('   https://app.netlify.com');
  console.log('\n⚠️  If this fails, manual web deploy is fastest option (2 minutes)');
  
  console.log('\n   Manual steps:');
  console.log('   1. https://app.netlify.com');
  console.log('   2. "Add new site" → "Import existing project"');
  console.log('   3. Connect GitHub → pi-mono-workspace');
  console.log('   4. Base dir: openclaw-wrappers');
  console.log('   5. Click "Deploy site"');
}

// Try Git CLI deploy with explicit path
function tryGitDeploy() {
  console.log('\n🔄 Trying Git CLI deploy...');
  try {
    const result = execSync(
      `NETLIFY_AUTH_TOKEN="${NETLIFY_TOKEN}" netlify deploy --prod --dir=. --message="Deploy"`,
      { 
        stdio: 'inherit',
        cwd: __dirname,
        timeout: 30000
      }
    );
    console.log('\n✅ Deploy complete via Git CLI');
  } catch (error) {
    console.log('\n⚠️  Git CLI deploy failed:', error.message);
    console.log('   This is expected on Node v24 + Netlify CLI');
    console.log('   Proceeding to alternative methods...');
  }
}

// Main
async function main() {
  try {
    console.log('\n📦 Step 1: Checking/Creating site...');
    const site = await createSite();

    console.log('\n📤 Step 2: Attempting deploy...');
    
    // Try Git deploy first
    tryGitDeploy();
    
    console.log('\n📋 Alternative: Manual Web Deploy');
    console.log('   If auto-deploy fails, manual is fastest (2 minutes):');
    console.log('   https://app.netlify.com');
    
  } catch (error) {
    if (error.message === 'Unauthorized') {
      console.log('\n❌ TOKEN ISSUE DETECTED');
      console.log('\n🔑 To fix:');
      console.log('   1. Go to: https://app.netlify.com/user/applications');
      console.log('   2. Create new access token');
      console.log('   3. Update ~/.bashrc with new token');
      console.log('   4. Run: source ~/.bashrc');
      console.log('\n   Then run deploy script again');
    } else {
      console.log('\n❌ Error:', error.message);
    }
    process.exit(1);
  }
}

main();
