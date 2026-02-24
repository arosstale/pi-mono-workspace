# Ground News Content Structure Report

**Date:** February 15, 2026  
**Report Type:** Site Structure & Content Organization Analysis  
**URL:** https://ground.news/

---

## Executive Summary

Ground News is a news aggregation platform designed to counteract media bias by displaying news events with sources from across the political spectrum. The platform aggregates stories from **50,000+ news sources** globally and presents them through a unique bias-aware interface that allows users to compare how different outlets frame the same story.

**Key Differentiators:**
- Multi-perspective comparison (Left, Center, Right bias ratings)
- Blindspot detection for underreported stories
- AI-powered Ground Summary for neutral content overview
- Comprehensive rating system (Bias, Factuality, Ownership)
- Personalized feeds with algorithmic curation

---

## 1. Complete Site Map and Page Tree

### Core News Pages

```
ground.news/
├── / (Homepage)
│   ├── Top Stories (Main feed)
│   ├── Local News
│   ├── Blindspot Feed
│   └── International
├── /my (My Feed - Personalized)
├── /blindspot (Blindspot Feed)
│   ├── ?filter=left (Left blindspots)
│   ├── ?filter=right (Right blindspots)
│   └── /today's-blindspot-topics
├── /interest/{topic} (Topic-specific pages)
│   ├── /interest/politics
│   ├── /interest/sports
│   ├── /interest/business
│   └── Custom interest pages
└── /article/{story_id} (Article story pages)
```

### Bias & Ratings Pages

```
├── /bias-bar (Bias distribution visualization)
├── /rating-system (Rating methodology)
├── /media-bias (Media bias information)
└── /bias-comparison (Story bias comparison)
```

### Subscription & Account Pages

```
├── /subscribe (Subscription tiers)
├── /my-news-bias-vantage (Personal bias insights - Vantage feature)
├── /my-news-bias (Personal bias insights - Free)
├── /group-subscriptions (Educational/institutional)
└── /gift (Gift subscriptions)
```

### Company Pages

```
├── /about (About Us)
├── /history (Company history)
├── /mission (Mission statement)
├── /blog (Blog)
├── /testimonials (User testimonials)
├── /careers (Job opportunities)
└── /contact-us (Contact form)
```

### Tools & Resources

```
├── /app (Mobile app download)
├── /tools (Tool section)
├── /app-store-links (iOS/Android)
├── /daily-newsletter (Newsletter signup)
├── /newsletters/
│   ├── /blindspot-report (Blindspot Report newsletter)
│   └── /burst-your-bubble (Burst Your Bubble newsletter)
├── /timelines (Story timelines)
└── /browser-extension (Chrome extension)
```

### Help & Support

```
├── /frequently-asked-questions (FAQ)
├── /help/ (Help Center)
│   ├── Media Bias Ratings
│   ├── Ownership and Factuality Ratings
│   ├── News Sources
│   ├── Topics
│   └── Referral Code
└── /ground-rebrand (Rebrand announcement)
```

### Specialized Tools

```
├── /blindspotter/
│   ├── /reddit/{subreddit} (Reddit community analysis)
│   └── /reddit-methodology (Blindspotter methodology)
└── /landingV*/ (Landing pages for campaigns)
    ├── /landingV8/fridaycheckout
    ├── /landingV5/welcome
    └── Other campaign pages
```

---

## 2. Content Categories and Niches

### Primary News Categories

#### Geographic Categories
- **International**
  - North America
  - South America
  - Europe
  - Asia
  - Australia
  - Africa
- **Local News** (Location-based)

#### Trending Categories
- **Trending Internationally**
- **Trending in U.S.**
- **Trending in U.K.**

#### Topic-Based Categories
- **Politics**
- **Elections**
- **Israel-Gaza Conflict**
- **Trump Administration**
- **Immigration and Customs Enforcement**
- **Business & Markets**
- **Sports**
  - Basketball
  - Hockey
  - Olympics
  - Super Bowl
- **Entertainment**
  - Valentine's Day
  - Bad Bunny
- **Social Media**
- **Technology**
- **Science**
- **Health**
- **Education**
- **Environment**
- **Jobs/Employment**

### Political Bias Categories

**7-Point Bias Spectrum:**
1. Far Left
2. Left
3. Leans Left
4. Center
5. Leans Right
6. Right
7. Far Right

### Factuality Ratings

- **Very High** - Most reliable, fact-based sources
- **High** - Well-researched, accurate with minimal bias
- **Mixed** - Some factual issues or moderate bias
- **Low** - Poor factuality, significant bias
- **Very Low** - Highly unreliable, often factually incorrect

### Ownership Categories

- **Corporate** - Large media conglomerates
- **Government-funded** - State-sponsored outlets
- **Independently Owned** - Free from corporate/government influence
- **Untracked** - Sources not yet classified
- **Unclassified** - Sources that don't fit existing categories

### Special Niches

- **Blindspot Stories** - Stories disproportionately covered by one political side
- **Alternative Media** - Non-mainstream sources
- **Local/Community News** - Regional and local coverage
- **Academic/Educational** - Educational institution-focused content
- **Reddit Community Analysis** - Subreddit news consumption patterns

---

## 3. Media Types Used

### Text Content
- **Article Headlines** - Primary story titles
- **Ground Summary** - AI-generated neutral story summaries
- **Source Excerpts** - Brief article snippets from sources
- **Bias Labels** - Text-based bias indicators (Left/Center/Right)
- **Publication Names** - Source outlet names
- **Timestamps** - Publication dates and times
- **Topic Tags** - Category and topic labels
- **Source Ratings** - Factuality and ownership text ratings

### Visual Elements
- **Bias Bar** - Visual representation of bias distribution (colored bar showing Left/Center/Right proportions)
- **Factuality Icons** - Visual indicators of source reliability
- **Ownership Badges** - Ownership type visual markers
- **Source Logos** - News outlet brand logos
- **Topic Pills** - Clickable topic/category pills
- **Trending Indicators** - Visual markers for trending stories

### Interactive Components
- **Bias Comparison Slider** - Interactive tool to compare coverage
- **Political Spectrum Visualization** - 7-point bias spectrum display
- **Blindspot Filters** - Filter by left/right blindspots
- **Source Sorting/Filtering** - Sort by bias, factuality, ownership
- **Feed Customization** - Pin/remove feeds, reorder navigation
- **Follow/Unfollow Controls** - Topic and source following
- **Search Interface** - Search for stories, topics, sources

### External Links
- **Source Article Links** - Links to original articles on publisher sites
- **Source Pages** - Individual news source profile pages
- **Social Media Links** - Links to Ground News social profiles

### Multimedia (Limited)
- **Source Thumbnails** - Source outlet images/logos
- **Note:** Ground News does not host full article images or videos - links to external sources
- **No embedded videos** - Platform is text/link-focused
- **No image galleries** - Minimal media hosting

---

## 4. Content Layout Patterns

### Homepage Layout (Desktop/Web)

```
┌─────────────────────────────────────────────────────────────┐
│ HEADER: Logo | Search | Login/Subscribe | Menu               │
├─────────────────────────────────────────────────────────────┤
│ NAVIGATION: Home | My Feed | Blindspot | Discover | Local   │
├───────────────────┬───────────────────────────────────────────┤
│                   │                                           │
│ TOPIC PILLS       │  MAIN FEED AREA                          │
│ (Trending topics) │  - Story Cards with bias bars             │
│                   │  - Ground Summary for top stories        │
│ SIDEBAR (Left)    │  - Blindspot indicator                   │
│                   │                                           │
│ - My Feed         │                                           │
│ - Blindspot       │                                           │
│ - Local News      │                                           │
│ - International    │                                           │
│ - Following       │                                           │
│                   │                                           │
└───────────────────┴───────────────────────────────────────────┘
```

### Story Card Layout

```
┌─────────────────────────────────────────────────────────┐
│ STORY HEADLINE                                        │
├─────────────────────────────────────────────────────────┤
│ BIAs BAR: [████████░░] Left ████████░░░░ Center       │
├─────────────────────────────────────────────────────────┤
│ Source 1 (Left)    | Source 2 (Center) | Source 3 (Right)
│ CNN                | Reuters           | Fox News
│ Factuality: High   | Factuality: Very  | Factuality: Mixed
│                    | High              │
├─────────────────────────────────────────────────────────┤
│ [Ground Summary - AI Generated Neutral Summary]        │
│ Brief overview of key points from all perspectives...   │
└─────────────────────────────────────────────────────────┘
```

### Article Detail Page Layout

```
┌─────────────────────────────────────────────────────────────┐
│ BACK | STORY HEADLINE                                       │
├─────────────────────────────────────────────────────────────┤
│ TABS: Coverage | Bias Comparison | Timeline | Sources      │
├─────────────────────────────────────────────────────────────┤
│ BIAS BAR: [████████░░] Left ████████░░░░ Center             │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│ COVERAGE TAB:                                                │
│ ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│ │ Left Side    │  │ Center Side  │  │ Right Side   │     │
│ │              │  │              │  │              │     │
│ │ - Source A   │  │ - Source X   │  │ - Source 1   │     │
│ │ - Source B   │  │ - Source Y   │  │ - Source 2   │     │
│ │              │  │              │  │              │     │
│ └──────────────┘  └──────────────┘  └──────────────┘     │
│                                                              │
│ BIAS COMPARISON TAB:                                         │
│ Side-by-side comparison of how Left/Center/Right cover      │
│ the same story with framing analysis                        │
│                                                              │
│ TIMELINE TAB:                                                │
│ Chronological view of coverage across all sources           │
│                                                              │
│ GROUND SUMMARY:                                              │
│ AI-generated neutral summary of all perspectives             │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Blindspot Feed Layout

```
┌─────────────────────────────────────────────────────────┐
│ BLINDSPOT FEED                                          │
├─────────────────────────────────────────────────────────┤
│ FILTER: [All] [Left Blindspots] [Right Blindspots]     │
├─────────────────────────────────────────────────────────┤
│                                                          │
│ 🔴 LEFT BLINDSPOT STORY                                 │
│ Story mostly covered by Right sources                    │
│ [Bias Bar showing Right dominance]                      │
│                                                          │
│ 🔵 RIGHT BLINDSPOT STORY                                │
│ Story mostly covered by Left sources                     │
│ [Bias Bar showing Left dominance]                       │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

### My Feed Layout

```
┌─────────────────────────────────────────────────────────┐
│ MY FEED (Personalized)                                   │
├─────────────────────────────────────────────────────────┤
│ Customize: [Edit Topics] [Edit Sources]                  │
├─────────────────────────────────────────────────────────┤
│                                                          │
│ PERSONALIZED STORY CARDS                                 │
│ Based on:                                                │
│ - Followed topics                                        │
│ - Followed sources                                       │
│ - Reading behavior                                       │
│ - Location                                               │
│                                                          │
│ [Standard story card layout with bias info]              │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

### Mobile App Layout

```
┌───────────────────┐
│ [≡]  Ground News  │
├───────────────────┤
│ [Search bar]      │
├───────────────────┤
│                   │
│ Scrollable Feed   │
│                   │
│ Story Cards       │
│ with compact      │
│ bias indicators   │
│                   │
├───────────────────┤
│ [Home] [Discover] │
│ [My Feed] [Blindspot] │
└───────────────────┘
```

---

## 5. Article/Card Components

### Story Card Components

#### Primary Elements
1. **Headline** - Main story title (clickable)
2. **Bias Bar** - Visual representation of source distribution
   - Color-coded sections (Red/Left, Gray/Center, Blue/Right)
   - Proportional width based on source count
3. **Source Count** - Number of sources covering the story
4. **Timestamp** - When the story was first published/updated

#### Secondary Elements
5. **Topic Tags** - Pills showing relevant categories (e.g., Politics, Sports)
6. **Blindspot Indicator** - Badge if story is a blindspot
   - "Left Blindspot" - Underreported by Left media
   - "Right Blindspot" - Underreported by Right media
7. **Ground Summary Preview** - Brief AI-generated snippet (premium)
8. **Factuality Score** - Average factuality of covering sources

#### Interactive Elements
9. **Expand/Collapse** - Toggle full story details
10. **Save/Bookmark** - Add to saved stories
11. **Share** - Share via social/email
12. **Hide Story** - Remove from feed
13. **More Options** - Three-dot menu (report, mute source, etc.)

### Source List Components (Within Story Card)

1. **Source Name** - Outlet name (e.g., CNN, Fox News)
2. **Bias Rating** - Text label (Left/Center/Right with granularity)
3. **Factuality Rating** - High/Mixed/Low rating
4. **Ownership Badge** - Corporate/Independent/Government
5. **Publication Time** - When source published the story
6. **External Link** - Link to original article (opens new tab)
7. **Source Logo** - Outlet brand image

### Ground Summary Components (Premium)

1. **Summary Header** - "Ground Summary" label
2. **AI-Generated Text** - Neutral summary of all perspectives
3. **Key Points** - Bullet points highlighting main issues
4. **Perspective Breakdown** - How different sides frame the story
5. **Neutral Language Indicator** - Note about AI neutrality

### Bias Comparison Components

1. **Left Column** - Left-leaning source coverage
2. **Center Column** - Center-leaning source coverage
3. **Right Column** - Right-leaning source coverage
4. **Framing Analysis** - How each side frames the issue
5. **Key Differences** - Highlighted contrasts in coverage
6. **Common Ground** - Points of agreement across spectrum

### Timeline Components

1. **Chronological List** - Stories ordered by publication time
2. **Source Indicator** - Which source published when
3. **Coverage Evolution** - How coverage developed over time
4. **First Report** - Who broke the story
5. **Follow-up Coverage** - Subsequent reporting

---

## 6. Header and Footer Elements

### Header Elements

#### Desktop Header
```
┌──────────────────────────────────────────────────────────────────┐
│ [Ground News Logo]       [Search Bar 🔍]    [Login] [Subscribe]  │
│                      Top Stories | My Feed | Blindspot | Local  │
└──────────────────────────────────────────────────────────────────┘
```

#### Components:
1. **Logo** - Ground News branding (clickable to homepage)
2. **Search Bar** - Search stories, topics, sources
3. **Login Button** - Sign in to account
4. **Subscribe Button** - CTA for subscription (prominent)
5. **Main Navigation** - Top-level navigation tabs
   - Home / Top Stories
   - My Feed (personalized)
   - Blindspot (underreported stories)
   - Discover (topics and sources)
   - Local (location-based news)

#### Mobile Header
```
┌──────────────────┐
│ [≡]  Ground News  │
├──────────────────┤
│ [Search 🔍]       │
└──────────────────┘
```

#### Components:
1. **Hamburger Menu** - Navigation drawer
2. **Logo** - Ground News branding
3. **Search Icon** - Opens search interface

### Navigation Menu (Hamburger/Full)

#### Primary Navigation
- **Home** - Top stories feed
- **My Feed** - Personalized news
- **Blindspot** - Bias blindspot stories
- **Local News** - Location-based
- **International** - Global news
- **Discover** - Browse topics and sources

#### Secondary Navigation
- **My News Bias** - Personal bias insights (Vantage)
- **Timelines** - Story timeline view
- **News Sources** - Browse all sources
- **Topics** - Browse all topics
- **Saved Stories** - Bookmarked articles

#### Account Navigation
- **Settings** - Account preferences
- **Subscription** - Manage subscription
- **Help Center** - Support and FAQs
- **Log Out** - Sign out

### Footer Elements

#### Desktop Footer
```
┌──────────────────────────────────────────────────────────────────────┐
│                                                                      │
│  Company                                                             │
│  • About • History • Mission • Blog • Testimonials • Careers         │
│                                                                      │
│  Product                                                             │
│  • App • Browser Extension • Daily Newsletter • Timelines             │
│                                                                      │
│  Resources                                                           │
│  • Help Center • FAQ • Rating System • Media Bias Ratings           │
│  • Ownership & Factuality • Referral Code • News Sources • Topics    │
│                                                                      │
│  Newsletters                                                         │
│  • Daily Newsletter • Blindspot Report • Burst Your Bubble           │
│                                                                      │
│  Legal                                                               │
│  • Privacy Policy • Terms & Conditions • Refund & Cancellation      │
│                                                                      │
│  Social                                                              │
│  • Twitter • LinkedIn • Instagram                                    │
│                                                                      │
│  Contact                                                             │
│  • Email: feedback@ground.news                                      │
│                                                                      │
│  © 2026 Ground News. All rights reserved.                           │
└──────────────────────────────────────────────────────────────────────┘
```

#### Footer Sections:

**1. Company Section**
- About Us
- History
- Mission
- Blog
- Testimonials
- Careers
- Contact Us

**2. Product Section**
- Mobile App (iOS/Android)
- Browser Extension
- Daily Newsletter
- Timelines
- Blindspotter Tool

**3. Resources Section**
- Help Center
- FAQ
- Rating System
- Media Bias Ratings
- Ownership & Factuality Ratings
- Referral Code
- News Sources Directory
- Topics Directory

**4. Newsletters Section**
- Daily Newsletter
- Blindspot Report
- Burst Your Bubble

**5. Subscription Section**
- Subscribe Now
- Gift Subscriptions
- Group Subscriptions (Educational)
- Free Trial

**6. Legal Section**
- Privacy Policy
- Terms & Conditions
- Refund & Cancellation Policy
- Cookie Preferences

**7. Social Links**
- Twitter: @Ground_app
- LinkedIn
- Instagram

**8. Contact Information**
- Email: feedback@ground.news
- Support form

**9. Copyright**
- © 2026 Ground News
- All rights reserved

#### Mobile Footer
```
┌─────────────────────┐
│ [Home] [Discover]   │
│ [My Feed] [Settings]│
└─────────────────────┘
```

#### Bottom Navigation Bar (Mobile App):
1. **Home** - Top stories
2. **Discover** - Topics and sources
3. **My Feed** - Personalized feed
4. **Settings/Profile** - Account settings

---

## 7. Sidebar Widgets or Sections

### Left Sidebar (Desktop)

#### Feed Navigation Widget
```
┌──────────────────────┐
│ NEWS FEEDS           │
├──────────────────────┤
│ • Home               │
│ • My Feed            │
│ • Blindspot          │
│ • Local News         │
│ • International      │
│ • Following          │
└──────────────────────┘
```

#### Following Widget
```
┌──────────────────────┐
│ FOLLOWING            │
├──────────────────────┤
│ Topics:              │
│ • Politics           │
│ • Technology         │
│ • Sports             │
│                      │
│ Sources:             │
│ • CNN                │
│ • BBC News           │
│ • Reuters            │
└──────────────────────┘
```

#### Trending Topics Widget
```
┌──────────────────────┐
│ TRENDING TOPICS      │
├──────────────────────┤
│ • Israel-Gaza        │
│ • Olympics           │
│ • Trump Admin        │
│ • Super Bowl         │
│ • Business & Markets │
│ • Immigration        │
└──────────────────────┘
```

#### Geographic Editions Widget
```
┌──────────────────────┐
│ EDITIONS             │
├──────────────────────┤
│ • North America      │
│ • Europe             │
│ • Asia               │
│ • UK                 │
│ • Australia          │
└──────────────────────┘
```

### Right Sidebar (Article Detail Page)

#### Bias Distribution Widget
```
┌──────────────────────┐
│ BIAS DISTRIBUTION    │
├──────────────────────┤
│ Left:    ██████ 40%  │
│ Center:  ████  25%  │
│ Right:   ████  35%  │
│                      │
│ Total Sources: 23    │
└──────────────────────┘
```

#### Factuality Distribution Widget
```
┌──────────────────────┐
│ FACTUALITY RATING    │
├──────────────────────┤
│ Very High:  ████  2  │
│ High:       ██████ 6  │
│ Mixed:      ████  4  │
│ Low:        ██     1  │
└──────────────────────┘
```

#### Ownership Distribution Widget
```
┌──────────────────────┐
│ OWNERSHIP BREAKDOWN  │
├──────────────────────┤
│ Corporate:   ██████  8  │
│ Independent: ████    5  │
│ Government:  ██      1  │
└──────────────────────┘
```

#### Related Stories Widget
```
┌──────────────────────┐
│ RELATED STORIES      │
├──────────────────────┤
│ • [Story 1 title]    │
│ • [Story 2 title]    │
│ • [Story 3 title]    │
│ • [Story 4 title]    │
└──────────────────────┘
```

#### Source List Widget
```
┌──────────────────────┐
│ SOURCES (23)         │
├──────────────────────┤
│ [L] CNN              │
│ [C] Reuters          │
│ [R] Fox News         │
│ [L] MSNBC            │
│ [C] AP News          │
│ [R] Breitbart        │
│ ...                  │
│ [Show all] [Filter]  │
└──────────────────────┘
```

#### My News Bias Widget (Vantage)
```
┌──────────────────────┐
│ MY NEWS BIAS         │
├──────────────────────┤
│ Your reading habits: │
│                      │
│ Bias:                │
│ Left:  ████  35%     │
│ Center: ██████ 50%   │
│ Right: ██    15%     │
│                      │
│ Factuality:          │
│ High: ██████  80%    │
│ Mixed: ██    20%     │
│                      │
│ [View Full Report]   │
└──────────────────────┘
```

#### Blindspot Alert Widget
```
┌──────────────────────┐
│ YOUR BLINDSPOTS      │
├──────────────────────┤
│ ⚠️ You may be       │
│    missing:          │
│                      │
│ • 12 Right-bias      │
│   stories            │
│                      │
│ • 8 stories about    │
│   [Topic X]          │
│                      │
│ [View Blindspots]    │
└──────────────────────┘
```

### Discover Sidebar

#### Topic Categories Widget
```
┌──────────────────────┐
│ BROWSE TOPICS        │
├──────────────────────┤
│ • Politics           │
│ • Business           │
│ • Technology         │
│ • Sports             │
│ • Entertainment      │
│ • Health             │
│ • Science            │
│ • Environment        │
│ • Education          │
│ [Show all topics]    │
└──────────────────────┘
```

#### Recommended Topics Widget
```
┌──────────────────────┐
│ RECOMMENDED FOR YOU  │
├──────────────────────┤
│ Based on your        │
│ reading history:      │
│                      │
│ • [Topic A] [+]      │
│ • [Topic B] [+]      │
│ • [Topic C] [+]      │
│ • [Topic D] [+]      │
└──────────────────────┘
```

---

## 8. Dynamic Content Areas

### Real-Time Updates

1. **Live Feed Updates**
   - Stories refresh automatically
   - New sources added to existing stories
   - Bias distribution recalculated as new sources publish

2. **Bias Bar Updates**
   - Changes as new sources report on story
   - Visual indicator shifts in real-time
   - Blindspot status updates dynamically

3. **Trending Topics**
   - Updated based on current coverage
   - Real-time trending indicators
   - Topic pills change based on activity

### Personalized Dynamic Content

4. **My Feed Algorithm**
   - Updates based on reading behavior
   - Adapts to followed topics/sources
   - Location-aware content
   - Time-of-day optimization

5. **My News Bias Dashboard**
   - Recalculates personal bias profile
   - Updates factuality distribution
   - Identifies new blindspots
   - Tracks reading patterns over time

6. **Blindspot Detection**
   - Algorithmic identification of asymmetric coverage
   - Updates as coverage shifts
   - Filters by left/right bias automatically

### Interactive Dynamic Elements

7. **Bias Comparison**
   - Updates when switching between stories
   - Dynamic side-by-side comparison
   - Framing analysis updates

8. **Timeline View**
   - Updates as new sources publish
   - Chronological progression visualization
   - Coverage evolution tracking

9. **Source Filtering**
   - Real-time filtering by bias/factuality/ownership
   - Dynamic source count updates
   - Bias distribution recalculates instantly

10. **Search Results**
    - Instant search results
    - Autocomplete for topics/sources
    - Real-time result filtering

### Subscription-Based Dynamic Content

11. **Premium Features (Vantage)**
    - Ground Summary generation (AI)
    - Advanced filtering options
    - Enhanced My News Bias insights
    - Unlimited topic/source following
    - Full Blindspot feed access
    - Factuality distribution per story

12. **Newsletters**
    - Daily briefings generated dynamically
    - Blindspot Report weekly updates
    - Burst Your Bubble personalized content

### External Dynamic Content

13. **External Source Previews**
    - Link previews for source articles
    - Open Graph metadata integration
    - Source favicon/logo loading

14. **Social Media Integration**
    - Twitter/X embeds
    - LinkedIn share functionality
    - Instagram content references

### Location-Based Dynamic Content

15. **Local News**
    - Geolocation-based story selection
    - Regional edition selection
    - Location-aware trending topics

16. **International Editions**
    - Region-specific content
    - Localized trending topics
    - Geographic source distribution

### Analytics & Metrics

17. **Source Metrics**
    - Dynamic source credibility scores
    - Factuality rating updates
    - Ownership classification updates

18. **Story Metrics**
    - Real-time source count
    - Bias distribution calculations
    - Coverage timeline updates

---

## 9. Content Organization Philosophy

### Core Principles

1. **Multi-Perspective Presentation**
   - Every story shown from multiple angles
   - No single "correct" narrative
   - User makes informed decisions

2. **Bias Transparency**
   - All sources labeled by political bias
   - Factuality ratings for credibility assessment
   - Ownership data for understanding influence

3. **Blindspot Exposure**
   - Highlights stories underreported by one side
   - Helps users see beyond their bubble
   - Encourages media literacy

4. **AI-Enhanced Neutrality**
   - Ground Summary provides neutral overview
   - Reduces sensationalism
   - Focuses on factual information

5. **Personalization with Balance**
   - My Feed tailored to interests
   - Still shows diverse perspectives
   - Prevents echo chambers

---

## 10. Technical Architecture Notes

### Data Sources

- **50,000+ News Sources** aggregated globally
- **Rating Partners:**
  - AllSides (bias ratings)
  - Ad Fontes Media (bias/factuality)
  - Media Bias/Fact Check (bias/factuality)

### Content Processing

- **AI Summarization** - Ground Summary uses proprietary AI
- **Bias Classification** - Automated + manual verification
- **Blindspot Algorithm** - Proprietary formula for asymmetric coverage detection
- **Factuality Assessment** - Based on independent rating organizations

### Platform Features

- **Responsive Design** - Desktop, tablet, mobile optimized
- **Mobile App** - iOS and Android native apps
- **Browser Extension** - Chrome extension available
- **API Integration** - Third-party ratings API

---

## 11. User Experience Flow

### Typical User Journey

1. **Discovery** - User lands on homepage or app
2. **Browsing** - Scrolls through Top Stories or My Feed
3. **Engagement** - Clicks on interesting story
4. **Exploration** - Views bias comparison and multiple sources
5. **Deep Dive** - Reads Ground Summary, checks timeline
6. **Personalization** - Follows topics/sources of interest
7. **Return** - Returns to personalized feed with refined preferences

### Subscription Conversion Path

1. **Free User** - Accesses basic features
2. **Engagement** - Uses blindspot, basic comparisons
3. **Limit Encountered** - Hits My Feed or advanced filter limit
4. **Premium Consideration** - Sees value in Ground Summary, full bias data
5. **Vantage Upgrade** - Subscribes for full features, My News Bias
6. **Retention** - Ongoing personalized experience

---

## 12. Content Strategy Insights

### Content Curation Approach

- **Algorithmic + Manual Hybrid** - Balanced approach to story selection
- **Bias-Aware Ranking** - Not click-driven, perspective-driven
- **Diversity Priority** - Ensures multiple viewpoints represented
- **Factuality Weighted** - Higher-rated sources given prominence

### Monetization Integration

- **Subscription Tiers** - Free, Pro, Premium, Vantage
- **Educational Licensing** - Group subscriptions for institutions
- **Gift Subscriptions** - Gift market penetration
- **Newsletter Products** - Email-based revenue stream

### Differentiation Strategy

- **Unique Value Prop** - Multi-perspective news comparison
- **Media Literacy Focus** - Educational approach to news consumption
- **Data-Driven** - Quantified bias and factuality
- **Alternative to Algorithms** - Human-centered curation over algorithmic optimization

---

## 13. Future Content Areas (Potential Expansion)

### Observed Gaps/Oppertunities

1. **Video Content** - Currently text-focused; video integration potential
2. **Podcast Coverage** - No podcast aggregation noted
3. **User-Generated Content** - No community features beyond following
4. **Fact-Checking Integration** - Could integrate real-time fact-check overlays
5. **Interactive Data** - More data visualization potential
6. **Commentary/Analysis** - Could add expert analysis layer
7. **Local Hyperlocal** - Could expand deeper local coverage
8. **Topic Deep Dives** - Could add explainer content

---

## 14. Key Takeaways

### Strengths

- **Clear bias transparency** - 7-point spectrum visualized
- **Comprehensive source coverage** - 50,000+ sources
- **AI-powered summaries** - Ground Summary adds unique value
- **Blindspot detection** - Addresses echo chamber problem
- **Educational approach** - Focus on media literacy

### Content Structure Highlights

- **Modular card design** - Consistent story presentation
- **Multi-layered navigation** - Geographic, topic, bias-based
- **Rich metadata** - Every story tagged with bias/factuality/ownership
- **Personalization options** - My Feed customization
- **Cross-platform consistency** - Similar UX across web/app

### Innovation Areas

- **Bias comparison engine** - Unique feature in news aggregation
- **Blindspot algorithm** - Proprietary asymmetric coverage detection
- **Ground Summary** - AI-generated neutral summaries
- **My News Bias** - Personal media diet analytics

---

## Appendix: URL Patterns

### Story URLs
- `/article/{story_id}_{hash}` - Individual story pages
- `/article/{story_id}?tab=comparison` - Bias comparison view
- `/article/{story_id}?tab=timeline` - Timeline view

### Source URLs
- `/source/{source_name}` - Source detail page (implied)
- Search-based source discovery

### Topic URLs
- `/interest/{topic_name}` - Topic-specific feed
- `/topic/{category}` - Category browsing (implied)

### Geographic URLs
- `/local` - Local news feed
- `/international` - International feed
- Edition-specific paths (e.g., `/edition/us`, `/edition/uk`)

### Subscription URLs
- `/subscribe` - Subscription tiers
- `/my-news-bias-vantage` - Vantage feature
- `/gift` - Gift subscriptions
- `/group-subscriptions` - Educational subscriptions

### Tool URLs
- `/blindspot` - Blindspot feed
- `/bias-bar` - Bias distribution tool
- `/rating-system` - Rating methodology
- `/timelines` - Story timelines
- `/blindspotter/reddit/{subreddit}` - Reddit community analysis

---

**Report End**

*This document provides a comprehensive analysis of Ground News content structure as of February 15, 2026. The platform is actively evolving, and some features may change over time.*
