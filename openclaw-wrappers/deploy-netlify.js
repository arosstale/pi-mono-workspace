#!/usr/bin/env node
/**
 * Netlify Deploy Script - Bypasses CLI entirely
 * Uses Netlify REST API directly
 */

const https = require('https');
const fs = require('fs');
const path = require('path');

// Configuration
const NETLIFY_TOKEN = process.env.NETLIFY_AUTH_TOKEN || 'nfp_rCyYJ4CycbXAPb1zQzLDT3gnn9zQEiuB6edf';
const SITE_NAME = 'openclaw-wrappers-deploy-test-' + Date.now();

// Files to deploy
const files = [
  { name: 'index.html', path: path.join(__dirname, 'index.html') }
];

console.log('🚀 Netlify Direct Deploy Script');
console.log('Token:', NETLIFY_TOKEN.substring(0, 10) + '...');
console.log('Site:', SITE_NAME);

// Step 1: Create site
function createSite() {
  return new Promise((resolve, reject) => {
    const data = JSON.stringify({
      name: SITE_NAME,
      ssl: true
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
            console.log('✅ Site created:', result.ssl_url);
            resolve(result);
          } else {
            console.log('❌ Failed to create site:', res.statusCode, body);
            reject(new Error(res.statusMessage));
          }
        } catch (e) {
          console.log('❌ Parse error:', e.message);
          console.log('Response:', body);
          reject(e);
        }
      });
    });

    req.on('error', reject);
    req.write(data);
    req.end();
  });
}

// Step 2: Upload file
function uploadFile(site, file) {
  return new Promise((resolve, reject) => {
    const fileData = fs.readFileSync(file.path);

    const options = {
      hostname: 'api.netlify.com',
      path: `/api/v1/sites/${site.id}/files/${file.name}`,
      method: 'PUT',
      headers: {
        'Content-Type': 'application/octet-stream',
        'Content-Length': Buffer.byteLength(fileData),
        'Authorization': `Bearer ${NETLIFY_TOKEN}`
      }
    };

    const req = https.request(options, (res) => {
      if (res.statusCode === 200) {
        console.log(`✅ Uploaded: ${file.name}`);
        resolve();
      } else {
        console.log(`❌ Upload failed: ${file.name}`, res.statusCode);
        reject(new Error(res.statusMessage));
      }
    });

    req.on('error', reject);
    req.write(fileData);
    req.end();
  });
}

// Main
async function main() {
  try {
    console.log('\n📦 Step 1: Creating site...');
    const site = await createSite();

    console.log('\n📤 Step 2: Uploading files...');
    for (const file of files) {
      await uploadFile(site, file);
    }

    console.log('\n🎉 Deploy complete!');
    console.log('URL:', site.ssl_url);

  } catch (error) {
    console.error('\n❌ Deploy failed:', error.message);
    process.exit(1);
  }
}

main();
