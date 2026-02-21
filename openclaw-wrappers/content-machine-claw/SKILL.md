# Content Machine Claw

Automated content creation pipeline for creators and solopreneurs.

---

## 🎯 What It Does

The Content Machine Claw automates the entire content production workflow:

1. **Monitors trends** (X, Reddit, RSS, YouTube transcripts)
2. **Identifies viral topics** in your niche
3. **Generates content** in your brand voice
4. **Creates visuals** (thumbnails, graphics)
5. **Schedules everything** across platforms

**Daily message:**
> "📝 Content Machine Claw — Weekly Batch
> 
> Here's your content for next 7 days:
> 
> 📱 Twitter: 14 posts (short, punchy)
> 📰 Newsletter: 2 editions (deep dives)
> 🎬 YouTube: 3 scripts (9-minute each)
> 📸 Instagram: 7 graphics (carousel posts)
> 
> 📅 All scheduled. Review and hit publish!
> 
> 💡 Trending topic this week: [topic]"

---

## 💡 Pain Points Solved

| Pain | Traditional | Content Machine |
|-------|-------------|-----------------|
| 80% production time | Manual writing, designing, scheduling | **Auto-generated in your voice** |
| Inconsistent voice | Mixed styles, tone drift | **Brand voice locked in** |
 Miss trends | Too busy creating | **Scrapes trends automatically** |
| No visuals | Canva, Figma manual | **Auto-generates graphics** |
| Manual scheduling | Post-by-post | **Batch schedules all platforms** |

---

## 🛠 Features

### Trend Monitoring
- **X/Twitter** — Trending hashtags, viral posts
- **Reddit** — Hot posts in subreddits
- **RSS Feeds** — Your niche's top blogs
- **YouTube** — Transcripts of top channels
- **News APIs** — Real-time trends

### Brand Voice Profile
- **Writing style** (formal, casual, witty, professional)
- **Vocabulary** (preferred words, phrases)
- **Tone** (optimistic, direct, inspiring)
- **Structure** (hooks, CTA patterns)
- **Avoid** (overused phrases, competitor language)

### Content Generation
- **Twitter/X** — Short, punchy, hashtags
- **LinkedIn** — Professional, thought leadership
- **Newsletter** — Deep dives, actionable insights
- **YouTube** — Scripts (intro, hook, content, outro)
- **Instagram** — Captions, carousel posts, stories
- **TikTok** — Short scripts, trending hooks

### Visual Creation
- **Thumbnails** — Click-worthy, brand-aligned
- **Social graphics** — Instagram posts, quote cards
- **Templates** — Consistent visual identity
- **A/B variants** — Multiple options per post

### Scheduling
- **Multi-platform** — Twitter, LinkedIn, YouTube, Instagram
- **Optimal times** — Based on your audience analytics
- **Batch upload** — Queue everything for the week
- **Auto-repost** — Evergreen content recycling

---

## 📊 Target Buyers

| Segment | Price | Why Buy |
|----------|--------|----------|
| Content creators | $99/mo | Get 80% of time back |
| Solopreneurs | $99/mo | Scale content without hiring |
| Agencies | $149/mo | Client content on autopilot |
| Course creators | $199/mo | Daily engagement, course promotion |

---

## ⚙️ Configuration

### config.json

```json
{
  "brand_voice": {
    "style": "casual",
    "tone": "optimistic",
    "vocabulary": ["shipping", "shipping fast", "builders"],
    "avoid": ["guys", "please", "super"],
    "examples": [
      "Ship it or shut up.",
      "Done is better than perfect."
    ]
  },
  "sources": [
    {
      "platform": "reddit",
      "subreddits": ["openclaw", "AI", "indiehackers"],
      "enabled": true
    },
    {
      "platform": "x",
      "keywords": ["openclaw", "AI agents", "automation"],
      "enabled": true
    }
  ],
  "content_plan": {
    "twitter": {
      "posts_per_week": 14,
      "hashtags": ["#openclaw", "#AI", "#automation"],
      "length": "short"
    },
    "newsletter": {
      "editions_per_week": 2,
      "word_count": 1500
    },
    "youtube": {
      "scripts_per_week": 3,
      "duration_minutes": 9
    },
    "instagram": {
      "posts_per_week": 7,
      "format": "carousel"
    }
  },
  "visuals": {
    "thumbnails": {
      "style": "minimalist",
      "brand_colors": ["#1a1a1a", "#00d4aa"]
    },
    "graphics": {
      "templates": ["quote", "stat", "announcement"]
    }
  },
  "scheduling": {
    "platforms": ["twitter", "linkedin", "youtube", "instagram"],
    "optimal_times": {
      "twitter": ["09:00", "14:00", "19:00"],
      "linkedin": ["09:00", "17:00"],
      "youtube": ["10:00", "18:00"],
      "instagram": ["11:00", "20:00"]
    }
  },
  "delivery": {
    "channel": "whatsapp",
    "schedule": "08:00",
    "frequency": "weekly"
  }
}
```

---

## 🚀 Quick Start

### 1. Install Dependencies

```bash
cd ~/pi-mono-workspace/openclaw-wrappers/content-machine-claw
pip install -r requirements.txt
```

### 2. Create Brand Voice Profile

Edit `config/brand_voice.json` with your style, tone, and examples.

### 3. Configure Sources

Add your niche's subreddits, X keywords, RSS feeds in `config.json`.

### 4. Run First Batch

```bash
python src/content_machine.py --config config.json
```

### 5. Review and Publish

Receive weekly batch via WhatsApp/Telegram. Review, hit publish, and grow.

---

## 💰 Pricing

| Plan | Price | Features |
|-------|--------|-----------|
| **Starter** | $49/mo | 2 platforms, 7 posts/week, basic visuals |
| **Creator** | $99/mo | 4 platforms, 20 posts/week, full visuals |
| **Agency** | $199/mo | Unlimited platforms, unlimited content, client branding |

---

## 📈 Battle-Tested

- ✅ 14 Twitter posts generated in brand voice
- ✅ 2 newsletter drafts (1,500 words each)
- ✅ 3 YouTube scripts (9-minute videos)
- ✅ 7 Instagram graphics (carousel posts)
- ✅ Weekly delivery via WhatsApp

---

## 🦞 Why Buy This Wrapper?

1. **Get 80% of your time back** — Review instead of create
2. **Consistent brand voice** — Locked in via JSON profile
3. **Never miss trends** — Scrapes automatically 24/7
4. **Batch scheduling** — Queue a week in 5 minutes
5. **Visuals included** — Thumbnails, graphics, templates

**Stop creating content manually. Start publishing consistently.** 📝
