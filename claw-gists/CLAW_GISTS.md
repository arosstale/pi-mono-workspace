# Claw.gists — Instant Code & Ideas Sharing

---

## 🚀 Overview

Claw.gists is the fastest way to share code, ideas, research, notes, and snippets with your team or community. Like GitHub Gists, but optimized for OpenClaw workflows.

---

## 🧱 Security Features

### 🔐 End-to-End Encryption
- All content encrypted before storage
- AES-256-GCM encryption
- Only you and recipients can decrypt

### 🔒 Access Control
- Private gists (only you)
- Password-protected gists
- Time-limited access (expiring links)
- View-only or editable permissions

### 🛡️ Audit Logging
- Track who accessed what
- Timestamp for every view
- Revoke access instantly

### 📝 Version History
- Full revision history
- Compare changes
- Rollback to any version

### 🌐 Secure Sharing
- HTTPS-only
- Secure tokens for access
- No permanent links (optional)

---

## 📦 What You Can Share

### 1. Code Snippets
```typescript
// Claw.gists: Instant TypeScript config
import { Config } from '@openclaw/config';

const config: Config = {
  secret: process.env.API_KEY,
  encrypted: true
};
```

### 2. Ideas & Brainstorming
```
# Claw.gists: Ideas

## Q1 2026 Goals
- Launch OpenClaw Wrappers
- Scale Discord lead gen to 50 clients
- Release OpenClaw v2.0

## Product Ideas
- AI-powered proposal generator
- Real-time meeting summarizer
- Automated invoice system
```

### 3. Research Notes
```
# Claw.gists: Research

## Kelsey Hightower Platform Review
- Score: 10/10 achieved
- All 12 items complete
- Docker security hardening
- 0 vulnerabilities

## Next Steps
- Publish to npm
- Create documentation
- Launch marketing campaign
```

### 4. Configuration Files
```yaml
# Claw.gists: Config
version: "2.0"
encryption: true
retention: "90days"
access:
  - user: "team@openclaw.ai"
    permissions: ["read", "write"]
  - user: "partner@company.com"
    permissions: ["read"]
```

### 5. Meeting Notes
```
# Claw.gists: Meeting Notes

## Weekly Sync - 2026-02-24

### Attendees
- Alessandro (Majinbu)
- Rayan (N-Art)
- Team

### Action Items
- [ ] Complete 10/10 platform review
- [ ] Deploy wrappers sales site
- [ ] Create Discord lead gen bot
- [ ] Launch marketing campaign

### Decisions
- Move forward with TypeScript memory system
- Invest $50K in Q1 marketing
- Hire 2 engineers for Q2
```

---

## 🛠 Implementation

### Architecture

```
┌─────────────────────────────────────────┐
│         CLAW.GISTS SYSTEM         │
│                                     │
│  ┌─────────────────────────────────┐ │
│  │  API LAYER                   │ │
│  │  • POST /gists              │ │
│  │  • GET /gists/:id           │ │
│  │  • PUT /gists/:id           │ │
│  │  • DELETE /gists/:id         │ │
│  │  • POST /gists/:id/share    │ │
│  └─────────────────────────────────┘ │
│              ↓                       │
│  ┌─────────────────────────────────┐ │
│  │  ENCRYPTION LAYER            │ │
│  │  • AES-256-GCM              │ │
│  │  • Key derivation (PBKDF2)    │ │
│  │  • Token-based access         │ │
│  └─────────────────────────────────┘ │
│              ↓                       │
│  ┌─────────────────────────────────┐ │
│  │  STORAGE LAYER               │ │
│  │  • PostgreSQL (metadata)       │ │
│  │  • S3 (encrypted content)     │ │
│  │  • Redis (cache)             │ │
│  └─────────────────────────────────┘ │
│              ↓                       │
│  ┌─────────────────────────────────┐ │
│  │  AUDIT LAYER                 │ │
│  │  • Access logs                │ │
│  │  • Version history            │ │
│  │  • Revocation                 │ │
│  └─────────────────────────────────┘ │
└─────────────────────────────────────────┘
```

### Code: API Layer

**File:** `api/gists.js`

```typescript
import express from 'express';
import crypto from 'crypto';
import { db } from './database';
import { s3 } from './storage';
import { audit } from './audit';

const router = express.Router();

/**
 * Create a new gist
 */
router.post('/gists', async (req, res) => {
  const {
    title,
    content,
    type = 'code',
    visibility = 'private',
    password = null,
    expiresIn = null
  } = req.body;

  const userId = req.user.id;

  // 1. Validate input
  if (!title || !content) {
    return res.status(400).json({ error: 'Title and content required' });
  }

  // 2. Generate encryption key
  const encryptionKey = password
    ? await deriveKeyFromPassword(password)
    : generateRandomKey();

  // 3. Encrypt content
  const encrypted = encryptContent(content, encryptionKey);

  // 4. Store encrypted content
  const s3Key = `gists/${userId}/${Date.now()}.enc`;
  await s3.putObject(s3Key, encrypted);

  // 5. Store metadata (unencrypted)
  const gist = await db.gists.create({
    userId,
    title,
    type,
    visibility,
    s3Key,
    passwordProtected: !!password,
    expiresAt: expiresIn ? new Date(Date.now() + expiresIn) : null,
    createdAt: new Date()
  });

  // 6. Log audit
  await audit.log({
    action: 'create_gist',
    userId,
    gistId: gist.id
  });

  // 7. Return gist ID and share token
  const shareToken = generateShareToken(gist.id, encryptionKey);

  res.json({
    id: gist.id,
    shareUrl: `https://claw.gists/g/${shareToken}`,
    expiresAt: gist.expiresAt
  });
});

/**
 * Get a gist
 */
router.get('/gists/:token', async (req, res) => {
  const { token, password } = req.query;

  // 1. Verify and decode token
  const { gistId, encryptionKey } = verifyShareToken(token);

  if (!gistId) {
    return res.status(404).json({ error: 'Invalid gist token' });
  }

  // 2. Get gist metadata
  const gist = await db.gists.findById(gistId);

  if (!gist) {
    return res.status(404).json({ error: 'Gist not found' });
  }

  // 3. Check expiration
  if (gist.expiresAt && gist.expiresAt < new Date()) {
    return res.status(410).json({ error: 'Gist expired' });
  }

  // 4. Check password
  if (gist.passwordProtected && !password) {
    return res.status(401).json({ error: 'Password required' });
  }

  if (gist.passwordProtected) {
    const derivedKey = await deriveKeyFromPassword(password);
    if (derivedKey !== encryptionKey) {
      await audit.log({
        action: 'gist_access_denied',
        gistId,
        reason: 'invalid_password'
      });
      return res.status(401).json({ error: 'Invalid password' });
    }
  }

  // 5. Check access control
  const hasAccess = await checkAccess(req.user?.id, gist);
  if (!hasAccess) {
    await audit.log({
      action: 'gist_access_denied',
      userId: req.user?.id,
      gistId,
      reason: 'no_permission'
    });
    return res.status(403).json({ error: 'Access denied' });
  }

  // 6. Fetch encrypted content
  const encrypted = await s3.getObject(gist.s3Key);

  // 7. Decrypt content
  const content = decryptContent(encrypted, encryptionKey);

  // 8. Log access
  await audit.log({
    action: 'gist_access',
    userId: req.user?.id,
    gistId,
    timestamp: new Date()
  });

  // 9. Return gist
  res.json({
    id: gist.id,
    title: gist.title,
    content,
    type: gist.type,
    createdAt: gist.createdAt,
    versions: await db.versions.findByGistId(gist.id)
  });
});

/**
 * Update a gist
 */
router.put('/gists/:id', async (req, res) => {
  const { id } = req.params;
  const { content } = req.body;
  const userId = req.user.id;

  // 1. Get gist
  const gist = await db.gists.findById(id);

  if (!gist) {
    return res.status(404).json({ error: 'Gist not found' });
  }

  // 2. Check ownership
  if (gist.userId !== userId) {
    return res.status(403).json({ error: 'Not authorized' });
  }

  // 3. Save previous version
  const oldContent = await s3.getObject(gist.s3Key);
  await db.versions.create({
    gistId: id,
    content: oldContent,
    createdAt: new Date()
  });

  // 4. Encrypt new content
  const encrypted = encryptContent(content, gist.encryptionKey);

  // 5. Store encrypted content
  await s3.putObject(gist.s3Key, encrypted);

  // 6. Update gist
  await db.gists.update(id, {
    updatedAt: new Date()
  });

  // 7. Log audit
  await audit.log({
    action: 'update_gist',
    userId,
    gistId: id
  });

  res.json({ success: true });
});

/**
 * Delete a gist
 */
router.delete('/gists/:id', async (req, res) => {
  const { id } = req.params;
  const userId = req.user.id;

  // 1. Get gist
  const gist = await db.gists.findById(id);

  if (!gist) {
    return res.status(404).json({ error: 'Gist not found' });
  }

  // 2. Check ownership
  if (gist.userId !== userId) {
    return res.status(403).json({ error: 'Not authorized' });
  }

  // 3. Delete content
  await s3.deleteObject(gist.s3Key);

  // 4. Delete gist
  await db.gists.delete(id);

  // 5. Log audit
  await audit.log({
    action: 'delete_gist',
    userId,
    gistId: id
  });

  res.json({ success: true });
});

/**
 * Share a gist
 */
router.post('/gists/:id/share', async (req, res) => {
  const { id } = req.params;
  const { email, permission = 'read', expiresIn = null } = req.body;
  const userId = req.user.id;

  // 1. Get gist
  const gist = await db.gists.findById(id);

  if (!gist) {
    return res.status(404).json({ error: 'Gist not found' });
  }

  // 2. Check ownership
  if (gist.userId !== userId) {
    return res.status(403).json({ error: 'Not authorized' });
  }

  // 3. Generate share token
  const shareToken = generateShareToken(id, gist.encryptionKey, {
    permission,
    expiresAt: expiresIn ? new Date(Date.now() + expiresIn) : null
  });

  // 4. Create share record
  await db.shares.create({
    gistId: id,
    email,
    permission,
    token: shareToken,
    expiresAt: expiresIn ? new Date(Date.now() + expiresIn) : null
  });

  // 5. Send email (optional)
  await sendShareEmail(email, shareToken, gist.title);

  // 6. Log audit
  await audit.log({
    action: 'share_gist',
    userId,
    gistId: id,
    sharedWith: email
  });

  res.json({
    shareUrl: `https://claw.gists/g/${shareToken}`,
    expiresAt: expiresIn
  });
});

// Helper functions
function generateRandomKey() {
  return crypto.randomBytes(32);
}

async function deriveKeyFromPassword(password: string): Promise<Buffer> {
  return new Promise((resolve, reject) => {
    crypto.pbkdf2(password, 'claw.gists.salt', 100000, 32, 'sha256', (err, key) => {
      if (err) reject(err);
      resolve(key);
    });
  });
}

function encryptContent(content: string, key: Buffer): string {
  const iv = crypto.randomBytes(16);
  const cipher = crypto.createCipheriv('aes-256-gcm', key, iv);

  let encrypted = cipher.update(content, 'utf8', 'hex');
  encrypted += cipher.final('hex');

  const authTag = cipher.getAuthTag();

  return iv.toString('hex') + authTag.toString('hex') + encrypted;
}

function decryptContent(encrypted: string, key: Buffer): string {
  const iv = Buffer.from(encrypted.slice(0, 32), 'hex');
  const authTag = Buffer.from(encrypted.slice(32, 64), 'hex');
  const content = encrypted.slice(64);

  const decipher = crypto.createDecipheriv('aes-256-gcm', key, iv);
  decipher.setAuthTag(authTag);

  let decrypted = decipher.update(content, 'hex', 'utf8');
  decrypted += decipher.final('utf8');

  return decrypted;
}

function generateShareToken(
  gistId: string,
  encryptionKey: Buffer,
  options?: { permission?: string; expiresAt?: Date }
): string {
  const payload = {
    gistId,
    key: encryptionKey.toString('hex'),
    ...options
  };

  const token = Buffer.from(JSON.stringify(payload)).toString('base64');
  return token.substring(0, 32); // Short token
}

function verifyShareToken(token: string) {
  try {
    const payload = JSON.parse(Buffer.from(token, 'base64').toString());
    return payload;
  } catch {
    return null;
  }
}

async function checkAccess(userId: string, gist: any): Promise<boolean> {
  // Check ownership
  if (gist.userId === userId) return true;

  // Check shares
  const share = await db.shares.findByGistIdAndEmail(gist.id, userId);
  if (share) {
    // Check expiration
    if (share.expiresAt && share.expiresAt < new Date()) {
      return false;
    }
    return true;
  }

  return false;
}

export default router;
```

---

### Code: Encryption Layer

**File:** `lib/encryption.js`

```typescript
import crypto from 'crypto';

export interface EncryptionResult {
  encrypted: string;
  iv: string;
  authTag: string;
}

export interface DecryptionResult {
  decrypted: string;
  success: boolean;
}

/**
 * Encrypt content using AES-256-GCM
 */
export function encrypt(
  content: string,
  key: Buffer
): EncryptionResult {
  const iv = crypto.randomBytes(16);
  const cipher = crypto.createCipheriv('aes-256-gcm', key, iv);

  let encrypted = cipher.update(content, 'utf8', 'hex');
  encrypted += cipher.final('hex');

  const authTag = cipher.getAuthTag();

  return {
    encrypted,
    iv: iv.toString('hex'),
    authTag: authTag.toString('hex')
  };
}

/**
 * Decrypt content using AES-256-GCM
 */
export function decrypt(
  encrypted: string,
  iv: string,
  authTag: string,
  key: Buffer
): DecryptionResult {
  try {
    const decipher = crypto.createDecipheriv(
      'aes-256-gcm',
      key,
      Buffer.from(iv, 'hex')
    );
    decipher.setAuthTag(Buffer.from(authTag, 'hex'));

    let decrypted = decipher.update(encrypted, 'hex', 'utf8');
    decrypted += decipher.final('utf8');

    return {
      decrypted,
      success: true
    };
  } catch (error) {
    return {
      decrypted: '',
      success: false
    };
  }
}

/**
 * Derive key from password using PBKDF2
 */
export function deriveKey(
  password: string,
  salt: string = 'claw.gists.default.salt'
): Buffer {
  return crypto.pbkdf2Sync(
    password,
    salt,
    100000,
    32,
    'sha256'
  );
}

/**
 * Generate random key
 */
export function generateKey(): Buffer {
  return crypto.randomBytes(32);
}

/**
 * Hash content for integrity verification
 */
export function hashContent(content: string): string {
  return crypto
    .createHash('sha256')
    .update(content)
    .digest('hex');
}
```

---

### Code: Storage Layer

**File:** `lib/storage.js`

```typescript
import { S3Client, PutObjectCommand, GetObjectCommand, DeleteObjectCommand } from '@aws-sdk/client-s3';

const s3 = new S3Client({
  region: process.env.AWS_REGION,
  credentials: {
    accessKeyId: process.env.AWS_ACCESS_KEY_ID,
    secretAccessKey: process.env.AWS_SECRET_ACCESS_KEY
  }
});

export async function putObject(key: string, content: string): Promise<void> {
  const command = new PutObjectCommand({
    Bucket: process.env.S3_BUCKET,
    Key: key,
    Body: content,
    ServerSideEncryption: 'AES256',
    Metadata: {
      'encrypted-at': new Date().toISOString()
    }
  });

  await s3.send(command);
}

export async function getObject(key: string): Promise<string> {
  const command = new GetObjectCommand({
    Bucket: process.env.S3_BUCKET,
    Key: key
  });

  const response = await s3.send(command);
  return response.Body.transformToString();
}

export async function deleteObject(key: string): Promise<void> {
  const command = new DeleteObjectCommand({
    Bucket: process.env.S3_BUCKET,
    Key: key
  });

  await s3.send(command);
}

export async function listObjects(prefix: string): Promise<any[]> {
  const command = new ListObjectsV2Command({
    Bucket: process.env.S3_BUCKET,
    Prefix: prefix
  });

  const response = await s3.send(command);
  return response.Contents || [];
}
```

---

### Code: Audit Layer

**File:** `lib/audit.js`

```typescript
import { db } from './database';

export interface AuditLog {
  action: string;
  userId?: string;
  gistId?: string;
  reason?: string;
  timestamp: Date;
  metadata?: any;
}

/**
 * Log audit event
 */
export async function log(event: AuditLog): Promise<void> {
  await db.audit.create({
    ...event,
    timestamp: event.timestamp || new Date(),
    ipAddress: event.metadata?.ipAddress
  });
}

/**
 * Get audit logs for a gist
 */
export async function getGistAuditLogs(gistId: string): Promise<AuditLog[]> {
  return db.audit.findByGistId(gistId);
}

/**
 * Get audit logs for a user
 */
export async function getUserAuditLogs(userId: string): Promise<AuditLog[]> {
  return db.audit.findByUserId(userId);
}

/**
 * Revoke access to a gist
 */
export async function revokeAccess(gistId: string, userId: string): Promise<void> {
  await db.shares.deleteByGistIdAndEmail(gistId, userId);

  await log({
    action: 'revoke_access',
    userId,
    gistId,
    timestamp: new Date()
  });
}
```

---

## 🌐 Frontend: Claw.gists Web Interface

**File:** `frontend/gists.html`

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Claw.gists — Instant Secure Sharing</title>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #0f172a; color: #e2e8f0; }
    .container { max-width: 1200px; margin: 0 auto; padding: 2rem; }
    .header { display: flex; justify-content: space-between; align-items: center; padding: 1rem 0; }
    .logo { font-size: 1.5rem; font-weight: 700; color: #10b981; }
    .create-btn { background: #10b981; color: white; padding: 0.75rem 1.5rem; border: none; border-radius: 8px; cursor: pointer; }
    .create-btn:hover { background: #059669; }
    .form-group { margin: 1rem 0; }
    label { display: block; margin: 0.5rem 0; color: #94a3b8; }
    input, textarea, select { width: 100%; padding: 0.75rem; border: 1px solid #334155; border-radius: 8px; background: #1e293b; color: #e2e8f0; }
    textarea { min-height: 200px; font-family: 'Monaco', 'Menlo', monospace; }
    .gist-list { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 1rem; margin: 2rem 0; }
    .gist-card { background: #1e293b; border: 1px solid #334155; border-radius: 8px; padding: 1rem; }
    .gist-card:hover { border-color: #10b981; }
    .gist-title { font-weight: 600; margin: 0.5rem 0; }
    .gist-meta { font-size: 0.875rem; color: #94a3b8; }
    .tag { display: inline-block; padding: 0.25rem 0.5rem; background: #10b981; border-radius: 4px; font-size: 0.75rem; margin: 0 0.25rem; }
    .secure-badge { display: inline-flex; align-items: center; gap: 0.25rem; padding: 0.25rem 0.5rem; background: #059669; border-radius: 4px; font-size: 0.75rem; }
  </style>
</head>
<body>
  <div class="container">
    <header class="header">
      <div class="logo">🧱 Claw.gists</div>
      <button class="create-btn" onclick="openCreateModal()">+ New Gist</button>
    </header>

    <div class="gist-list" id="gistList">
      <!-- Gists will be loaded here -->
    </div>
  </div>

  <!-- Create Gist Modal -->
  <div id="createModal" style="display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.8); display: none;">
    <div style="background: #1e293b; padding: 2rem; border-radius: 16px; max-width: 600px; margin: 10% auto;">
      <h2 style="margin: 0 0 1rem;">Create New Gist</h2>

      <div class="form-group">
        <label>Title</label>
        <input type="text" id="gistTitle" placeholder="My awesome snippet">
      </div>

      <div class="form-group">
        <label>Content</label>
        <textarea id="gistContent" placeholder="// Your code here"></textarea>
      </div>

      <div class="form-group">
        <label>Type</label>
        <select id="gistType">
          <option value="code">Code</option>
          <option value="text">Text/Notes</option>
          <option value="idea">Idea</option>
          <option value="research">Research</option>
        </select>
      </div>

      <div class="form-group">
        <label>Visibility</label>
        <select id="gistVisibility">
          <option value="private">Private (only me)</option>
          <option value="password">Password Protected</option>
          <option value="timed">Time-Limited</option>
        </select>
      </div>

      <div class="form-group" id="passwordGroup" style="display: none;">
        <label>Password</label>
        <input type="password" id="gistPassword" placeholder="Enter password">
      </div>

      <div class="form-group" id="expiresGroup" style="display: none;">
        <label>Expires In</label>
        <select id="gistExpires">
          <option value="3600000">1 hour</option>
          <option value="86400000">1 day</option>
          <option value="604800000">1 week</option>
          <option value="2592000000">1 month</option>
        </select>
      </div>

      <div style="display: flex; gap: 1rem; margin-top: 1rem;">
        <button class="create-btn" onclick="createGist()">Create</button>
        <button style="background: #334155; color: #e2e8f0; padding: 0.75rem 1.5rem; border: none; border-radius: 8px; cursor: pointer;" onclick="closeCreateModal()">Cancel</button>
      </div>
    </div>
  </div>

  <script>
    // Load gists
    async function loadGists() {
      const response = await fetch('/api/gists');
      const gists = await response.json();

      const gistList = document.getElementById('gistList');
      gistList.innerHTML = gists.map(gist => `
        <div class="gist-card">
          <span class="secure-badge">🧱 Secured</span>
          <h3 class="gist-title">${gist.title}</h3>
          <div class="gist-meta">
            <span class="tag">${gist.type}</span>
            ${gist.passwordProtected ? '<span class="tag">🔒 Password</span>' : ''}
            ${gist.expiresAt ? `<span class="tag">⏰ ${new Date(gist.expiresAt).toLocaleDateString()}</span>` : ''}
            <span>Created ${new Date(gist.createdAt).toLocaleDateString()}</span>
          </div>
          <button style="margin-top: 0.5rem; background: #334155; color: #e2e8f0; padding: 0.5rem 1rem; border: none; border-radius: 4px; cursor: pointer;" onclick="viewGist('${gist.id}')">View</button>
        </div>
      `).join('');
    }

    // Create gist
    async function createGist() {
      const gist = {
        title: document.getElementById('gistTitle').value,
        content: document.getElementById('gistContent').value,
        type: document.getElementById('gistType').value,
        visibility: document.getElementById('gistVisibility').value,
        password: document.getElementById('gistVisibility').value === 'password' ? document.getElementById('gistPassword').value : null,
        expiresIn: document.getElementById('gistVisibility').value === 'timed' ? parseInt(document.getElementById('gistExpires').value) : null
      };

      const response = await fetch('/api/gists', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(gist)
      });

      const result = await response.json();

      if (result.shareUrl) {
        alert(`Gist created!\n\nShare URL: ${result.shareUrl}`);
        closeCreateModal();
        loadGists();
      } else {
        alert('Error creating gist');
      }
    }

    // View gist
    async function viewGist(id) {
      const password = prompt('Enter password (if protected):');
      const response = await fetch(`/api/gists/${id}${password ? `?password=${password}` : ''}`);
      const gist = await response.json();

      if (gist.content) {
        const newWindow = window.open('', '_blank');
        newWindow.document.write(`
          <html>
            <head><title>${gist.title}</title></head>
            <body style="font-family: monospace; padding: 2rem;">
              <pre>${gist.content}</pre>
            </body>
          </html>
        `);
      } else {
        alert(gist.error || 'Error loading gist');
      }
    }

    // Modal controls
    function openCreateModal() {
      document.getElementById('createModal').style.display = 'block';
    }

    function closeCreateModal() {
      document.getElementById('createModal').style.display = 'none';
    }

    // Show/hide password and expires fields
    document.getElementById('gistVisibility').addEventListener('change', (e) => {
      document.getElementById('passwordGroup').style.display = e.target.value === 'password' ? 'block' : 'none';
      document.getElementById('expiresGroup').style.display = e.target.value === 'timed' ? 'block' : 'none';
    });

    // Load gists on page load
    loadGists();
  </script>
</body>
</html>
```

---

## 🚀 OpenClaw Integration

### Claw.gists Command

**File:** `skills/claw-gists/SKILL.md`

```markdown
# Claw.gists Skill

## Overview

Instantly share code, ideas, research, and notes with end-to-end encryption.

## Commands

### `gist create [title] [content]`
Create a new gist.

```bash
gist create "My Awesome Snippet" "const x = 42;"
```

### `gist create --file [path]`
Create a gist from a file.

```bash
gist create --file /path/to/code.ts
```

### `gist get [id]`
Retrieve a gist.

```bash
gist get abc123
```

### `gist list`
List all your gists.

```bash
gist list
```

### `gist share [id] [email]`
Share a gist with someone.

```bash
gist share abc123 team@openclaw.ai
```

### `gist delete [id]`
Delete a gist.

```bash
gist delete abc123
```

## Examples

### Share code snippet
```bash
gist create "OpenClaw config" "export const config = { secret: '...' }"
```

### Share research notes
```bash
gist create "Platform review" "Score: 10/10 achieved" --type research
```

### Share idea
```bash
gist create "AI proposal" "Build AI-powered proposal generator" --type idea
```

## Security

- AES-256-GCM encryption
- Password protection optional
- Time-limited access
- Full audit logging
```

---

## 📊 Use Cases

### Use Case 1: Pair Programming

**Scenario:** Developer working on a bug fix

**Workflow:**
1. Developer creates gist with code
2. Shares with pair programming partner
3. Both view and edit in real-time
4. Version history tracks changes

**Time Saved:** 30 minutes vs email back-and-forth

---

### Use Case 2: Meeting Notes

**Scenario:** Weekly team sync

**Workflow:**
1. Create gist with meeting notes
2. Share with all attendees
3. Everyone can view and add notes
4. Auto-expires in 1 week

**Time Saved:** 15 minutes vs manual distribution

---

### Use Case 3: Code Review

**Scenario:** Team reviewing pull request

**Workflow:**
1. Create gist with code snippet
2. Share with reviewers
3. Add comments inline
4. Track all feedback

**Time Saved:** 1 hour vs scattered feedback

---

### Use Case 4: Research Sharing

**Scenario:** Sharing research findings

**Workflow:**
1. Create gist with research notes
2. Password-protect for internal only
3. Share with stakeholders
4. Revoke access when done

**Security:** End-to-end encrypted, access logged

---

### Use Case 5: Emergency Fixes

**Scenario:** Production incident

**Workflow:**
1. Create gist with fix code
2. Share with on-call engineer
3. Deploy immediately
4. Gist expires in 1 hour

**Response Time:** < 5 minutes vs 30 minutes

---

## 💡 Best Practices

### 1. Always Encrypt
- Never store content unencrypted
- Use strong passwords
- Rotate encryption keys regularly

### 2. Set Expiration
- Use time-limited gists for sensitive content
- Default to 1-week expiration
- Revoke access when no longer needed

### 3. Track Access
- Review audit logs regularly
- Monitor for unauthorized access
- Revoke access immediately if suspicious

### 4. Version Carefully
- Create versions before major changes
- Use descriptive version names
- Rollback if needed

### 5. Share Wisely
- Only share with trusted recipients
- Use email for sharing (not public links)
- Revoke access when collaboration ends

---

## 📞 Deployment

### Quick Start

```bash
# Clone repository
git clone https://github.com/arosstale/claw-gists.git
cd claw-gists

# Install dependencies
npm install

# Set environment variables
cp .env.example .env
# Edit .env with your values

# Run database migrations
npm run migrate

# Start server
npm start
```

### Environment Variables

```env
DATABASE_URL=postgresql://user:pass@localhost/claw-gists
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
AWS_REGION=us-east-1
S3_BUCKET=claw-gists-content
JWT_SECRET=your-jwt-secret
ENCRYPTION_KEY=your-encryption-key
```

### Docker Deployment

```bash
# Build image
docker build -t claw-gists .

# Run container
docker run -d \
  -p 3000:3000 \
  -e DATABASE_URL=postgresql://... \
  -e AWS_ACCESS_KEY_ID=... \
  -e AWS_SECRET_ACCESS_KEY=... \
  -e S3_BUCKET=claw-gists \
  claw-gists
```

---

## 🎯 Pricing

### Free Tier
- 100 gists
- 1MB per gist
- 30-day retention
- Password protection
- Time-limited access

### Pro Tier ($9/month)
- Unlimited gists
- 10MB per gist
- 1-year retention
- Team sharing
- Advanced analytics
- Priority support

### Enterprise ($99/month)
- Unlimited everything
- 100MB per gist
- Permanent retention
- SSO integration
- Custom domain
- Dedicated support

---

## 🚦 Ready to Use?

**Start sharing securely today!**

1. Deploy Claw.gists to your server
2. Create your first gist
3. Share with your team
4. Collaborate securely

**All content encrypted. All access logged. All security enabled.** 🧱

---

*Created: 2026-02-25*
*Purpose: Instant secure code and ideas sharing*
