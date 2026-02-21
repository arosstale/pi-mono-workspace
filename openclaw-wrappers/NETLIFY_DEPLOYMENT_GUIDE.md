# Netlify Deployment Guide — OpenClaw Wrappers

**Issue:** Netlify CLI is incompatible with Node.js v24 (unsettled top-level await error)
**Solution:** Git-based deployment (better anyway — auto-deploys on push!)

---

## 🚀 Quick Deploy (Git Method — Recommended)

### Why This is Better Than CLI

| CLI Method | Git Method |
|------------|------------|
| Manual deploy each time | Auto-deploy on push |
| Netlify CLI required | No CLI needed |
| Local Node version issues | Runs on Netlify's build |
| Forget to deploy? | Never forgets |

---

## Step-by-Step Instructions

### Step 1: Go to Netlify Dashboard

1. Visit: https://app.netlify.com
2. Click **"Add new site"** → **"Import an existing project"**
3. Click **"GitHub"** to connect

### Step 2: Connect GitHub Repository

1. Authorize Netlify to access your GitHub
2. Search for: `pi-mono-workspace`
3. **Click the repository**

### Step 3: Configure Build Settings

```
Base directory: openclaw-wrappers
Build command: echo 'Static site ready'
Publish directory: . (or leave empty)
```

### Step 4: Deploy!

Click **"Deploy site"** — done!

Netlify will:
- Pull from GitHub
- Run the `netlify.toml` config
- Deploy your static HTML site
- Give you a URL like: `https://openclaw-wrappers.netlify.app`

---

## ⚙️ Netlify.toml Explained

```toml
[build]
  publish = "."              # Current directory (where index.html lives)
  command = "echo 'Static site ready'"  # No build needed (static HTML)

[dev]
  command = "echo 'Dev server ready'"
  port = 3000

[[headers]]
  for = "/*"               # Apply to all files
  [headers.values]
    X-Frame-Options = "DENY"
    X-XSS-Protection = "1; mode=block"
    X-Content-Type-Options = "nosniff"
    Referrer-Policy = "strict-origin-when-cross-origin"

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200            # SPA-friendly redirect (if we add JS later)
```

---

## 🔄 How Auto-Deploy Works

After Git setup:

1. You make changes locally
2. Run: `git commit -m "Update" && git push`
3. **Netlify auto-detects push**
4. **Auto-redeploys** in ~30 seconds
5. **Done!**

No CLI needed ever again.

---

## 🐛 Node v24 Issue Research

### The Problem

```
Uncaught SyntaxError: Cannot use import statement outside a module
netlify-cli has terminated unexpectedly
```

**Root Cause:** Netlify CLI uses ESM (ECMAScript Modules) with top-level `await`, but:
- Node v18+ requires explicit ESM mode (`"type": "module"` in package.json)
- Or CLI must use `.mjs` extension
- Netlify CLI may not be fully updated for v24

### Why This Matters

| Node Version | ESM Support | Netlify CLI Status |
|--------------|--------------|-------------------|
| v16.x | Partial | ✅ Works |
| v18.x | Better | ⚠️ May work |
| v20.x | Good | ⚠️ May work |
| v24.x | Native | ❌ **Broken** |

### Workaround Options

1. **Git Deploy (Recommended)** — No CLI needed
2. **Downgrade Node** — Use v18 or v20 with `nvm`
3. **Use Vercel** — Vercel CLI works with v24
4. **Wait for Fix** — Netlify CLI update (unknown timeline)

---

## 🌐 Vercel Alternative

If you prefer Vercel:

```bash
cd openclaw-wrappers
npx vercel --prod
```

Vercel CLI works with Node v24!

---

## ✅ Verify Deployment

After deploying:

1. Visit your Netlify URL
2. Check: `openclaw-wrappers.netlify.app`
3. Verify:
   - ✅ 5 wrapper cards visible
   - ✅ Pricing correct
   - ✅ Buy buttons clickable
   - ✅ Mobile responsive

---

## 📝 Post-Deploy Checklist

- [ ] Update buy buttons with payment links (Stripe/LemonSqueezy)
- [ ] Test checkout flow
- [ ] Add Google Analytics
- [ ] Set up custom domain (if desired)
- [ ] Enable HTTPS (automatic on Netlify)

---

## 🔗 Helpful Links

- **Netlify Git Deploy Guide:** https://docs.netlify.com/configure-builds/file-based-configuration/
- **Netlify.toml Reference:** https://docs.netlify.com/netlify-toml-reference/
- **Vercel CLI:** https://vercel.com/docs/cli

---

**Done!** 🚀

Your site is now connected to GitHub and will auto-deploy on every push.
