# OpenClaw Wrappers

Pre-configured AI agents for lead generation, content creation, trading automation, and more.

---

## 🎯 What Are Wrappers?

OpenClaw is open-source and free. But setup takes hours:

- **Learn the platform** — 3-5 hours
- **Configure skills** — 2-4 hours  
- **Integrate APIs** — 1-3 hours
- **Test & debug** — 2-4 hours

**Total:** 8-16 hours per project

**Wrappers skip all that.** Pre-configured, battle-tested, ready in 10 minutes.

---

## 📦 Available Wrappers

| Wrapper | Price | What It Does | Setup Time |
|----------|--------|-------------|-------------|
| **Lead Generation Claw** | $99/mo | Automated lead scraping, enrichment, qualification | 5 min |
| **Content Machine Claw** | $99/mo | Social content pipeline (Twitter, Newsletter, YouTube) | 10 min |
| **Trading Automation Claw** | $399/mo | Crypto trading automation with RBI system | 10 min |
| **Brand Voice Claw** | $149/mo | Consistent brand voice across platforms | 5 min |
| **Research Assistant Claw** | $199/mo | Academic research automation (ArX, citations) | 10 min |

---

## 🚀 Quick Start

### 1. Choose a Wrapper

Browse the wrappers above or visit `index.html`.

### 2. Install Dependencies

```bash
cd ~/pi-mono-workspace/openclaw-wrappers/[wrapper-name]
pip install -r requirements.txt
```

### 3. Configure

Edit `config/config.json` with your credentials and settings.

### 4. Run

```bash
python src/[wrapper-name].py --config config/config.json
```

### 5. Schedule (Optional)

Edit your OpenClaw cron job for automation:

```yaml
# ~/.openclaw/cron.yaml
wrapper_name:
  schedule: "0 9 * * *"
  command: "python ~/pi-mono-workspace/openclaw-wrappers/[wrapper-name]/src/[wrapper-name].py --config ~/pi-mono-workspace/openclaw-wrappers/[wrapper-name]/config/config.json"
  enabled: true
```

Restart OpenClaw:

```bash
openclaw restart
```

---

## 📊 Who Should Use Wrappers?

| Buyer | Pain | Wrapper Solution |
|--------|-------|----------------|
| **Agencies** | Scale without hiring | Lead Gen Claw, Content Machine |
| **Content Creators** | 80% production time | Content Machine, Brand Voice |
| **Crypto Traders** | 24/7 monitoring | Trading Automation Claw |
| **Researchers** | Manual paper tracking | Research Assistant Claw |
| **Founders** | Need MVP fast | All wrappers |

---

## 💰 Pricing

All wrappers include:

- ✅ **Full automation** — No manual work
- ✅ **Battle-tested code** — Used in production
- ✅ **Documentation** — Setup guides, troubleshooting
- ✅ **Weekly updates** — New features, bug fixes
- ✅ **Priority support** — Discord community

---

## 📚 Documentation

Each wrapper includes:

- **SKILL.md** — Complete feature list
- **README.md** — 10-minute setup guide
- **config/config.json** — Template configuration
- **TROUBLESHOOTING.md** — Common issues

---

## 🚀 Deploy Sales Site

```bash
cd ~/pi-mono-workspace/openclaw-wrappers
netlify deploy --prod --dir=. --site=openclaw-wrappers
```

---

## 📞 Support

- **Email:** contact@openclaw.ai
- **Discord:** Invite-only (wrapper buyers)
- **Issues:** https://github.com/your-repo/openclaw-wrappers/issues

---

## 🦞 Why Buy?

1. **Setup in 10 minutes** — Copy-paste credentials
2. **Fully automated** — Wake up to results
3. **Brand-ready** — Professional, tested code
4. **Weekly updates** — New features, bug fixes
5. **Community access** — Learn from other wrapper users

**Stop configuring. Start automating.** 🚀
