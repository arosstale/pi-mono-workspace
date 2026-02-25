#!/usr/bin/env node

/**
 * Claw.gists CLI — OpenClaw Integration
 *
 * Commands:
 *   gist create [title] [content] - Create a new gist
 *   gist create --file [path]    - Create gist from file
 *   gist get [id]                 - Get a gist
 *   gist list                      - List all gists
 *   gist share [id] [email]       - Share a gist
 *   gist delete [id]               - Delete a gist
 */

import { Command } from 'commander';
import { readFile } from 'fs/promises';
import { homedir } from 'os';
import { join } from 'path';

const program = new Command();

// API endpoint (adjust to your deployment)
const API_URL = process.env.CLAW_GISTS_API_URL || 'http://localhost:3000/api';

// Auth token (read from ~/.claw-gists/token)
const getToken = () => {
  const tokenPath = join(homedir(), '.claw-gists', 'token');
  try {
    return require(tokenPath).token;
  } catch {
    return process.env.CLAW_GISTS_TOKEN;
  }
};

/**
 * Create a new gist
 */
program
  .command('create')
  .argument('[title]', 'Gist title')
  .argument('[content]', 'Gist content')
  .option('-f, --file <path>', 'Create from file')
  .option('-t, --type <type>', 'Gist type (code, text, idea, research)', 'code')
  .option('-v, --visibility <visibility>', 'Visibility (private, password, timed)', 'private')
  .option('-p, --password <password>', 'Password protection')
  .option('-e, --expires <ms>', 'Expiration time in milliseconds')
  .action(async (title, content, options) => {
    try {
      let gistContent = content;

      // Read from file if specified
      if (options.file) {
        console.log(`Reading file: ${options.file}`);
        gistContent = await readFile(options.file, 'utf-8');
      }

      if (!title && options.file) {
        title = options.file.split('/').pop();
      }

      if (!title) {
        title = 'Untitled Gist';
      }

      // Prepare request body
      const body = {
        title,
        content: gistContent,
        type: options.type,
        visibility: options.visibility,
        password: options.visibility === 'password' ? options.password : null,
        expiresIn: options.visibility === 'timed' ? parseInt(options.expires) : null
      };

      // Create gist
      console.log('Creating gist...');
      const response = await fetch(`${API_URL}/gists`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${getToken()}`
        },
        body: JSON.stringify(body)
      });

      const result = await response.json();

      if (result.shareUrl) {
        console.log('\n✅ Gist created!');
        console.log(`\nTitle: ${title}`);
        console.log(`Type: ${options.type}`);
        console.log(`Share URL: ${result.shareUrl}`);
        if (result.expiresAt) {
          console.log(`Expires: ${new Date(result.expiresAt).toLocaleString()}`);
        }
        console.log(`\n🔒 Content is AES-256-GCM encrypted`);
      } else {
        console.error('❌ Error creating gist:', result.error);
        process.exit(1);
      }

    } catch (error) {
      console.error('❌ Error:', error.message);
      process.exit(1);
    }
  });

/**
 * Get a gist
 */
program
  .command('get')
  .argument('<id>', 'Gist ID or token')
  .option('-p, --password <password>', 'Password if protected')
  .action(async (id, options) => {
    try {
      const url = new URL(`${API_URL}/gists/${id}`);
      if (options.password) {
        url.searchParams.set('password', options.password);
      }

      console.log('Fetching gist...');
      const response = await fetch(url.toString());
      const gist = await response.json();

      if (gist.content) {
        console.log(`\n━━━ ${gist.title} ━━━`);
        console.log(`\nType: ${gist.type}`);
        console.log(`Created: ${new Date(gist.createdAt).toLocaleString()}`);
        if (gist.versions?.length > 0) {
          console.log(`Versions: ${gist.versions.length}`);
        }
        console.log(`\n${'─'.repeat(50)}`);
        console.log(`\n${gist.content}\n`);
        console.log(`\n${'─'.repeat(50)}`);
        console.log(`\n✅ Decrypted with AES-256-GCM`);
      } else {
        console.error('❌ Error:', gist.error || 'Gist not found');
        process.exit(1);
      }

    } catch (error) {
      console.error('❌ Error:', error.message);
      process.exit(1);
    }
  });

/**
 * List all gists
 */
program
  .command('list')
  .action(async () => {
    try {
      console.log('Fetching gists...\n');

      const response = await fetch(`${API_URL}/gists`, {
        headers: {
          'Authorization': `Bearer ${getToken()}`
        }
      });

      const gists = await response.json();

      if (gists.length === 0) {
        console.log('No gists found. Create one with `gist create`');
        return;
      }

      console.log(gists.map((gist, index) => {
        const secure = gist.passwordProtected ? '🔒' : '🔓';
        const expires = gist.expiresAt ? `⏰ ${new Date(gist.expiresAt).toLocaleDateString()}` : '';
        return [
          `${index + 1}. ${secure} ${gist.title}`,
          `   ID: ${gist.id}`,
          `   Type: ${gist.type}`,
          `   Created: ${new Date(gist.createdAt).toLocaleDateString()}`,
          `   ${expires}`
        ].filter(Boolean).join('\n');
      }).join('\n\n'));

      console.log(`\nTotal: ${gists.length} gist(s)`);
      console.log('🧱 All content encrypted with AES-256-GCM\n');

    } catch (error) {
      console.error('❌ Error:', error.message);
      process.exit(1);
    }
  });

/**
 * Share a gist
 */
program
  .command('share')
  .argument('<id>', 'Gist ID')
  .argument('<email>', 'Recipient email')
  .option('-p, --permission <permission>', 'Permission (read, write)', 'read')
  .option('-e, --expires <ms>', 'Expiration time in milliseconds')
  .action(async (id, email, options) => {
    try {
      console.log(`Sharing gist ${id} with ${email}...`);

      const body = {
        email,
        permission: options.permission,
        expiresIn: parseInt(options.expires)
      };

      const response = await fetch(`${API_URL}/gists/${id}/share`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${getToken()}`
        },
        body: JSON.stringify(body)
      });

      const result = await response.json();

      if (result.shareUrl) {
        console.log('\n✅ Gist shared!');
        console.log(`\nRecipient: ${email}`);
        console.log(`Permission: ${options.permission}`);
        console.log(`Share URL: ${result.shareUrl}`);
        if (result.expiresAt) {
          console.log(`Expires: ${new Date(result.expiresAt).toLocaleString()}`);
        }
        console.log(`\n🔒 Secure link sent via email`);
      } else {
        console.error('❌ Error sharing gist:', result.error);
        process.exit(1);
      }

    } catch (error) {
      console.error('❌ Error:', error.message);
      process.exit(1);
    }
  });

/**
 * Delete a gist
 */
program
  .command('delete')
  .argument('<id>', 'Gist ID')
  .option('-f, --force', 'Skip confirmation')
  .action(async (id, options) => {
    try {
      if (!options.force) {
        const readline = require('readline');
        const rl = readline.createInterface({
          input: process.stdin,
          output: process.stdout
        });

        const answer = await new Promise(resolve => {
          rl.question('Are you sure you want to delete this gist? (y/N) ', resolve);
        });

        rl.close();

        if (answer.toLowerCase() !== 'y') {
          console.log('Cancelled');
          return;
        }
      }

      console.log(`Deleting gist ${id}...`);

      const response = await fetch(`${API_URL}/gists/${id}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${getToken()}`
        }
      });

      const result = await response.json();

      if (result.success) {
        console.log('\n✅ Gist deleted');
        console.log('🧱 Encrypted content removed from storage');
      } else {
        console.error('❌ Error:', result.error);
        process.exit(1);
      }

    } catch (error) {
      console.error('❌ Error:', error.message);
      process.exit(1);
    }
  });

/**
 * Login
 */
program
  .command('login')
  .argument('<token>', 'API token')
  .action(async (token) => {
    try {
      const tokenPath = join(homedir(), '.claw-gists');
      const fs = require('fs');
      fs.mkdirSync(tokenPath, { recursive: true });

      fs.writeFileSync(
        join(tokenPath, 'token'),
        JSON.stringify({ token })
      );

      console.log('✅ Logged in successfully');
      console.log('Token saved to ~/.claw-gists/token\n');

    } catch (error) {
      console.error('❌ Error:', error.message);
      process.exit(1);
    }
  });

/**
 * Logout
 */
program
  .command('logout')
  .action(async () => {
    try {
      const tokenPath = join(homedir(), '.claw-gists', 'token');
      const fs = require('fs');

      if (fs.existsSync(tokenPath)) {
        fs.unlinkSync(tokenPath);
        console.log('✅ Logged out successfully');
      } else {
        console.log('Not logged in');
      }

    } catch (error) {
      console.error('❌ Error:', error.message);
      process.exit(1);
    }
  });

/**
 * Help
 */
program.on('--help', () => {
  console.log('\n🧱 Claw.gists — Instant Secure Sharing\n');
  console.log('\nAll content encrypted with AES-256-GCM\n');
  console.log('\nExamples:\n');
  console.log('  gist create "My snippet" "const x = 42;"');
  console.log('  gist create --file code.ts --type code');
  console.log('  gist get abc123');
  console.log('  gist list');
  console.log('  gist share abc123 team@example.com');
  console.log('  gist delete abc123 --force\n');
  console.log('Environment variables:\n');
  console.log('  CLAW_GISTS_API_URL   API endpoint (default: http://localhost:3000/api)');
  console.log('  CLAW_GISTS_TOKEN       API token (or use `gist login`)\n');
});

// Parse and execute
program.parse();
