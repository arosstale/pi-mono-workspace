# Claw.gists Skill

---

## 🧱 Overview

Claw.gists is the fastest way to share code, ideas, research, notes, and snippets with your team or community. Think GitHub Gists, but with:

- **End-to-end encryption** (AES-256-GCM)
- **Access control** (private, password-protected, time-limited)
- **Audit logging** (full tracking, revoke anytime)
- **Version history** (rollback to any version)
- **OpenClaw integration** (seamless CLI and API)

---

## 📦 Installation

### Option 1: Install as OpenClaw Skill

```bash
# Install the skill
mkdir -p ~/.local/lib/node_modules/openclaw/skills
cd ~/.local/lib/node_modules/openclaw/skills
git clone https://github.com/arosstale/claw-gists.git

# Set up environment
export CLAW_GISTS_API_URL="https://claw-gists.your-domain.com/api"
export CLAW_GISTS_TOKEN="your-api-token"
```

### Option 2: Install as NPM Package

```bash
npm install -g @arosstale/claw-gists
```

### Option 3: Use Directly

```bash
git clone https://github.com/arosstale/claw-gists.git
cd claw-gists
npm install
npm link
```

---

## 🚀 Usage

### In OpenClaw Chat

```
You: Create a gist for my OpenClaw config
Claw: Sure! Please provide:
- Title: The gist title
- Content: The code/content to share
- Type: code, text, idea, research
- Visibility: private, password, timed

You: Title: OpenClaw Config
Content: export const config = { secret: '...' }
Type: code
Visibility: private
Claw: ✅ Gist created!
ID: abc123
Share URL: https://claw.gists/g/xyz789
```

```
You: Get gist abc123
Claw: 🧱 Fetching encrypted gist...
━━━ OpenClaw Config ━━━
export const config = { secret: '...' }
────────────────────────
✅ Decrypted with AES-256-GCM
Created: Feb 25, 2026
Versions: 3
```

```
You: List my gists
Claw: 📋 Your Gists (5 total):

1. 🧱 OpenClaw Config
   ID: abc123
   Type: code
   Created: Feb 25, 2026

2. 🧱 Platform Research
   ID: def456
   Type: research
   Created: Feb 24, 2026

3. 🧱 Meeting Notes - Weekly Sync
   ID: ghi789
   Type: text
   Created: Feb 22, 2026
   ⏰ Expires: Mar 1, 2026

4. 🧱 AI Idea - Proposal Generator
   ID: jkl012
   Type: idea
   Created: Feb 20, 2026
   🔒 Password protected

5. 🧱 Bug Fix #123
   ID: mno345
   Type: code
   Created: Feb 18, 2026
```

---

## 🎯 Commands

### `gist create`

Create a new gist.

**Arguments:**
- `title` — Gist title
- `content` — Content to share
- `type` — Type: `code`, `text`, `idea`, `research` (default: `code`)
- `visibility` — Visibility: `private`, `password`, `timed` (default: `private`)
- `password` — Password (if visibility=`password`)
- `expiresIn` — Expiration time in ms (if visibility=`timed`)

**Examples:**
```
# Basic gist
gist create "My snippet" "const x = 42;"

# Password-protected
gist create "Secret config" "API_KEY=..." \
  --visibility password \
  --password mysecretpass

# Time-limited (1 hour)
gist create "Emergency fix" "patch code here" \
  --visibility timed \
  --expiresIn 3600000

# Research note
gist create "Platform review" "Score: 10/10 achieved" \
  --type research
```

**Returns:**
```
{
  "id": "abc123",
  "shareUrl": "https://claw.gists/g/xyz789",
  "expiresAt": "2026-03-01T00:00:00.000Z"
}
```

---

### `gist get`

Retrieve and decrypt a gist.

**Arguments:**
- `id` — Gist ID or share token
- `password` — Password (if gist is password-protected)

**Examples:**
```
# Get by ID
gist get abc123

# Get with password
gist get abc123 --password mysecretpass
```

**Returns:**
```
{
  "id": "abc123",
  "title": "OpenClaw Config",
  "content": "export const config = { ... }",
  "type": "code",
  "createdAt": "2026-02-25T10:30:00.000Z",
  "versions": [
    { "version": 1, "createdAt": "2026-02-25T10:30:00.000Z" },
    { "version": 2, "createdAt": "2026-02-25T11:00:00.000Z" }
  ]
}
```

---

### `gist list`

List all your gists.

**Arguments:**
- `type` — Filter by type (optional)
- `limit` — Maximum number to return (default: 50)

**Examples:**
```
# List all gists
gist list

# Filter by type
gist list --type code

# Limit results
gist list --limit 10
```

**Returns:**
```
[
  {
    "id": "abc123",
    "title": "OpenClaw Config",
    "type": "code",
    "createdAt": "2026-02-25T10:30:00.000Z",
    "visibility": "private"
  },
  ...
]
```

---

### `gist update`

Update an existing gist.

**Arguments:**
- `id` — Gist ID
- `content` — New content

**Examples:**
```
gist update abc123 "export const config = { ... }"
```

**Returns:**
```
{
  "success": true,
  "version": 3
}
```

---

### `gist delete`

Delete a gist.

**Arguments:**
- `id` — Gist ID
- `force` — Skip confirmation (default: `false`)

**Examples:**
```
# With confirmation
gist delete abc123

# Force delete
gist delete abc123 --force
```

**Returns:**
```
{
  "success": true
}
```

---

### `gist share`

Share a gist with someone.

**Arguments:**
- `id` — Gist ID
- `email` — Recipient email
- `permission` — Permission: `read`, `write` (default: `read`)
- `expiresIn` — Expiration time in ms (optional)

**Examples:**
```
# Share with read access
gist share abc123 team@openclaw.ai

# Share with write access
gist share abc123 partner@company.com --permission write

# Time-limited share (1 day)
gist share abc123 temp@company.com --expiresIn 86400000
```

**Returns:**
```
{
  "shareUrl": "https://claw.gists/g/xyz789",
  "expiresAt": "2026-02-26T10:30:00.000Z"
}
```

---

### `gist search`

Search your gists.

**Arguments:**
- `query` — Search query
- `type` — Filter by type (optional)
- `limit` — Maximum results (default: 20)

**Examples:**
```
# Search by keyword
gist search "openclaw"

# Search by type
gist search --type research

# Combined
gist search "platform review" --type research --limit 5
```

**Returns:**
```
[
  {
    "id": "ghi789",
    "title": "Platform Review",
    "type": "research",
    "snippet": "Score: 10/10 achieved..."
  },
  ...
]
```

---

### `gist versions`

View version history of a gist.

**Arguments:**
- `id` — Gist ID

**Examples:**
```
gist versions abc123
```

**Returns:**
```
[
  {
    "version": 1,
    "content": "Old content...",
    "createdAt": "2026-02-25T10:30:00.000Z"
  },
  {
    "version": 2,
    "content": "New content...",
    "createdAt": "2026-02-25T11:00:00.000Z"
  }
]
```

---

### `gist rollback`

Rollback a gist to a previous version.

**Arguments:**
- `id` — Gist ID
- `version` — Version number to rollback to

**Examples:**
```
gist rollback abc123 --version 1
```

**Returns:**
```
{
  "success": true,
  "currentVersion": 1
}
```

---

## 🔒 Security Best Practices

### 1. Always Use Encryption
All content is encrypted with AES-256-GCM before storage. This means:
- Even if the database is compromised, content remains encrypted
- Encryption keys are never stored with content
- Each gist has a unique encryption key

### 2. Use Password Protection
For sensitive content, always set a password:
```bash
gist create "Secret" "sensitive content" --visibility password --password strongpass
```

### 3. Set Time Limits
For temporary sharing, use time-limited gists:
```bash
# 1 hour
gist create "Emergency" "fix code" --visibility timed --expiresIn 3600000

# 1 day
gist create "Temp" "temp content" --visibility timed --expiresIn 86400000
```

### 4. Review Audit Logs
Check who accessed your gists:
```bash
# (This would be a separate command)
gist audit abc123
```

### 5. Revoke Access
Immediately revoke access when no longer needed:
```bash
# (This would be a separate command)
gist revoke abc123 partner@company.com
```

---

## 💡 Use Cases

### Pair Programming

Share code with a pair programming partner:

```bash
# Create gist with code
gist create "Pair session - Bug #123" "function fix() { ... }" \
  --visibility password --password pairsession

# Share URL with partner
# Partner accesses with password
# Both can view and edit
# Version history tracks all changes
```

**Time saved:** 30 minutes vs email back-and-forth

---

### Meeting Notes

Capture and share meeting notes:

```bash
# Create gist with notes
gist create "Weekly Sync - 2026-02-25" \
  "## Action Items\n- [ ] Fix bug\n- [ ] Deploy feature" \
  --type text \
  --visibility timed \
  --expiresIn 604800000
```

**Benefits:**
- Everyone can view and add notes
- Auto-expires in 1 week
- Full version history

---

### Code Review

Share code for review:

```bash
# Create gist with code
gist create "PR #456 - Feature X" \
  "function featureX() { ... }" \
  --type code \
  --visibility password --password review
```

**Benefits:**
- Reviewers can comment
- Password protects pre-review
- Version history for changes

---

### Research Sharing

Share research findings securely:

```bash
# Create gist with research
gist create "Platform Engineering Review" \
  "## Score: 10/10\n\n### Items:\n1. Docker security\n2. CI/CD" \
  --type research \
  --visibility password --password secret
```

**Benefits:**
- End-to-end encrypted
- Password protection
- Full audit trail

---

### Emergency Fixes

Share emergency fix quickly:

```bash
# Create gist with fix
gist create "Hotfix - Production Incident" \
  "PATCH: Update dependency to fix security issue" \
  --type code \
  --visibility timed \
  --expiresIn 3600000
```

**Benefits:**
- Instant sharing
- Auto-expires in 1 hour
- Secure link

---

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|----------|
| `CLAW_GISTS_API_URL` | API endpoint URL | `http://localhost:3000/api` |
| `CLAW_GISTS_TOKEN` | API authentication token | - |
| `CLAW_GISTS_ENCRYPTION_KEY` | Default encryption key (optional) | - |
| `CLAW_GISTS_TIMEOUT` | Request timeout in ms | `30000` |

### Setting Environment Variables

```bash
# Set for current session
export CLAW_GISTS_API_URL="https://claw-gists.your-domain.com/api"
export CLAW_GISTS_TOKEN="your-api-token"

# Set permanently
echo 'export CLAW_GISTS_API_URL="https://claw-gists.your-domain.com/api"' >> ~/.bashrc
echo 'export CLAW_GISTS_TOKEN="your-api-token"' >> ~/.bashrc
```

---

## 🐛 Troubleshooting

### Issue: Authentication Failed

**Error:** `401 Unauthorized`

**Solution:**
```bash
# Check your token
echo $CLAW_GISTS_TOKEN

# Re-login if needed
gist login <new-token>
```

---

### Issue: Gist Not Found

**Error:** `404 Gist not found`

**Solution:**
- Verify gist ID is correct
- Check if gist was deleted
- If password-protected, ensure password is correct

---

### Issue: Decryption Failed

**Error:** `Failed to decrypt content`

**Solution:**
- Verify password is correct
- Check if gist was corrupted
- Try retrieving a previous version

---

### Issue: Access Denied

**Error:** `403 Access denied`

**Solution:**
- Verify you have permission
- Check if access was revoked
- Contact gist owner if needed

---

## 📞 Support

- **Documentation:** https://docs.claw.gists
- **API Reference:** https://api.claw.gists
- **Issues:** https://github.com/arosstale/claw-gists/issues
- **Community:** https://discord.gg/clawgists

---

## 📝 Examples

### Example 1: Daily Notes

```bash
# Create daily notes gist
gist create "Daily Notes - 2026-02-25" \
  "## Accomplishments\n- Deployed feature X\n- Fixed bug Y\n\n## Tomorrow\n- Start feature Z" \
  --type text

# Share with team
gist share abc123 team@openclaw.ai
```

### Example 2: Code Snippets Library

```bash
# Create snippets for reuse
gist create "Auth Utils" \
  "function hashPassword(password) { return bcrypt.hash(password); }
function verifyPassword(password, hash) { return bcrypt.compare(password, hash); }" \
  --type code

# Search snippets later
gist search "auth utils"
```

### Example 3: Research Repository

```bash
# Create research gist
gist create "Kelsey Hightower Review" \
  "## Platform Engineering Review\n\nScore: 10/10\n\n### Complete Items:\n- Docker security\n- CI/CD pipeline\n- Health checks" \
  --type research \
  --visibility password --password secret
```

### Example 4: Quick Ideas

```bash
# Capture idea instantly
gist create "AI Feature Idea" \
  "Build AI-powered proposal generator that:\n1. Analyzes requirements\n2. Generates proposal text\n3. Includes pricing estimates" \
  --type idea
```

---

## 🎯 Best Practices

1. **Use descriptive titles** — Makes searching easier
2. **Choose the right type** — code, text, idea, research
3. **Set appropriate visibility** — private for secrets, password for sharing
4. **Use time limits** — For temporary content
5. **Review audit logs** — Check who accessed what
6. **Keep versions clean** — Delete old versions if needed
7. **Share selectively** — Only with trusted recipients
8. **Revoke access** — When collaboration ends

---

## 🚦 OpenClaw Integration

### Using in Workflows

Claw.gists integrates seamlessly with OpenClaw workflows:

```yaml
workflow:
  name: "Share Code Snippet"

  triggers:
    - type: "message"
      pattern: "create gist"

  actions:
    - name: "Create Gist"
      action: "gist.create"
      inputs:
        title: "${workflow.title}"
        content: "${workflow.content}"
        type: "code"

    - name: "Share URL"
      action: "reply"
      template: "Gist created: ${gist.shareUrl}"
```

### Using in Agents

Agents can use Claw.gists for sharing code:

```python
# In Python agents
import requests

def share_code(title, content):
    response = requests.post(
        f"{API_URL}/gists",
        json={
            "title": title,
            "content": content,
            "type": "code"
        },
        headers={"Authorization": f"Bearer {TOKEN}"}
    )
    return response.json()
```

---

**Start sharing securely with Claw.gists!** 🧱🔒

---

*Version: 1.0.0*
*Last Updated: 2026-02-25*
