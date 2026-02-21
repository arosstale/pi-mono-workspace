#!/usr/bin/env node
/**
 * Netlify Deploy Script v3 - Direct API upload
 * Uses deploy endpoint with site ID
 */

const https = require('https');
const http = require('http');
const fs = require('fs');
const path = require('path');

// Configuration
const NETLIFY_TOKEN = process.env.NETLIFY_AUTH_TOKEN || 'nfp_rCyYJ4CycbXAPb1zQzLDT3gnn9zQEiuB6edf';
const SITE_ID = '1f61c929-1809-4759-9366-32ab3a3f9460'; // From v2 discovery
const SITE_URL = 'https://openclaw-wrappers.netlify.app';

console.log('🚀 Netlify Direct Deploy Script v3');
console.log('Site ID:', SITE_ID);
console.log('Target:', SITE_URL);

// Read index.html
const indexHtml = fs.readFileSync('index.html');
console.log('\n📁 File size:', indexHtml.length, 'bytes');

// Create deploy payload using direct upload
function deployDirect() {
  return new Promise((resolve, reject) => {
    const formData = [
      `--NetlifyFormBoundary${Date.now()}\r\n`,
      `Content-Disposition: form-data; name="file"; filename="index.html"\r\n`,
      `Content-Type: text/html\r\n\r\n`,
      indexHtml,
      `\r\n--NetlifyFormBoundary${Date.now()}--\r\n`
    ].join('');

    const options = {
      hostname: 'api.netlify.com',
      path: `/api/v1/sites/${SITE_ID}/deploys`,
      method: 'POST',
      headers: {
        'Content-Type': `multipart/form-data; boundary=NetlifyFormBoundary${Date.now()}`,
        'Content-Length': Buffer.byteLength(formData),
        'Authorization': `Bearer ${NETLIFY_TOKEN}`
      }
    };

    const req = https.request(options, (res) => {
      let body = '';
      res.on('data', chunk => body += chunk);
      res.on('end', () => {
        console.log('Status:', res.statusCode);
        if (res.statusCode === 200 || res.statusCode === 201) {
          try {
            const result = JSON.parse(body);
            console.log('✅ Deploy complete!');
            console.log('   Deploy ID:', result.deploy_id);
            console.log('   URL:', SITE_URL);
            console.log('\n🎉 SUCCESS! Site should be live:', SITE_URL);
            resolve(result);
          } catch (e) {
            console.log('Response:', body);
            resolve({ success: true });
          }
        } else {
          console.log('❌ Deploy failed:', res.statusCode);
          console.log('Body:', body);
          reject(new Error(res.statusMessage));
        }
      });
    });

    req.on('error', reject);
    req.write(formData);
    req.end();
  });
}

// Try using files endpoint (simpler)
function uploadViaFilesEndpoint() {
  return new Promise((resolve, reject) => {
    const fileContent = fs.readFileSync('index.html');
    const fileBase64 = fileContent.toString('base64');

    const data = JSON.stringify({
      files: [
        {
          name: 'index.html',
          file_base64: fileBase64
        }
      ]
    });

    const options = {
      hostname: 'api.netlify.com',
      path: `/api/v1/sites/${SITE_ID}/files`,
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
        console.log('Files endpoint status:', res.statusCode);
        if (res.statusCode === 200) {
          console.log('✅ File uploaded via files endpoint!');
          console.log('🎉 Site should be live:', SITE_URL);
          resolve({ success: true });
        } else {
          console.log('Response:', body);
          reject(new Error(res.statusMessage));
        }
      });
    });

    req.on('error', reject);
    req.write(data);
    req.end();
  });
}

// Try deploy API
function deployViaDeployAPI() {
  return new Promise((resolve, reject) => {
    const fileContent = fs.readFileSync('index.html');
    
    // Netlify deploy API expects a different format
    const data = JSON.stringify({
      draft: false,
      files: [
        {
          name: 'index.html',
          content: fileContent.toString('base64')
        }
      ]
    });

    const options = {
      hostname: 'api.netlify.com',
      path: `/api/v1/sites/${SITE_ID}/deploys`,
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
        console.log('Deploy API status:', res.statusCode);
        if (res.statusCode === 201 || res.statusCode === 200) {
          console.log('✅ Deployed via deploy API!');
          console.log('🎉 Site should be live:', SITE_URL);
          try {
            const result = JSON.parse(body);
            console.log('   Deploy ID:', result.id);
          } catch (e) {}
          resolve({ success: true });
        } else {
          console.log('Body:', body);
          reject(new Error(res.statusMessage));
        }
      });
    });

    req.on('error', reject);
    req.write(data);
    req.end();
  });
}

// Main
async function main() {
  console.log('\n🚀 Attempting deployment methods...\n');

  // Method 1: Deploy API
  try {
    console.log('Method 1: Deploy API...');
    await deployViaDeployAPI();
    process.exit(0);
  } catch (e) {
    console.log('  ✗ Failed:', e.message);
  }

  // Method 2: Files endpoint
  try {
    console.log('\nMethod 2: Files API...');
    await uploadViaFilesEndpoint();
    process.exit(0);
  } catch (e) {
    console.log('  ✗ Failed:', e.message);
  }

  console.log('\n❌ All API methods failed');
  console.log('\n📋 MANUAL DEPLOY (2 minutes):');
  console.log('   1. https://app.netlify.com');
  console.log('   2. Find: openclaw-wrappers');
  console.log('   3. Click "Deploy site"');
  console.log('\n🎯 Already working alternative:');
  console.log('   https://openclaw-wrappers.vercel.app (LIVE!)');
  
  process.exit(1);
}

main();
