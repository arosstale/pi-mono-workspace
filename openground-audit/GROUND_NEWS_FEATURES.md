# GROUND NEWS - FEATURE INVENTORY

**Date:** Feb 15, 2026
**Source:** Research via web search and documentation
**Baseline:** https://ground.news/

---

## 📱 PLATFORM FEATURES

### Multi-Platform Support
- **Web Application:** Full-featured web platform
- **Mobile Apps:** iOS (App Store), Android
- **Browser Extension:** Chrome/Edge extension
- **Newsletter:** Weekly Blindspot report via email

---

## 🎯 CORE FUNCTIONALITY

### 1. News Aggregation ✅

**Purpose:** Aggregate news from multiple sources
- Multi-source collection
- Deduplication of stories
- Topic clustering
- Real-time updates

**Display:** Feed-based interface with chronological sorting

---

### 2. Blindspot Feature ✅

**Description:** Stories disproportionately covered by one political side

**Methodology:**
- Specific bias breakdown formula required
- Lopsided coverage detection
- Political undertone identification

**Formula:**
```
A Blindspot story must meet specific conditions:
- Political undertones present
- Disproportionate coverage from one side
- Meets L/C/R ratio requirements
```

**Display:** Dedicated Blindspot feed

**Key Benefit:** Exposes how media bias shapes narratives

---

### 3. Bias Bar ✅

**Purpose:** Visual representation of source bias distribution

**Display:**
```
[████████░░░░░] L: 60%  C: 30%  R: 10%
```

**Labels:**
- L = Left-leaning sources
- C = Center sources
- R = Right-leaning sources

**Color Coding (Region-Specific):**
- **US:** Red = Left, Blue = Right
- **UK/Canada/Australia:** Blue = Left, Red = Right

**Calculation:** Based on number of bias-rated sources reporting

**Interactive:** Tap to see source breakdown

---

### 4. Bias & Factuality Ratings ✅

**Bias Rating Scale:**
- **Range:** -6 (furthest Left) to +6 (furthest Right)
- **Reference:** -6 ← Left ← 0 (Center) → Right → +6

**Factuality Rating:**
- Scale: Measures source credibility
- Source: External bias raters
- Independent: Ground team does NOT rate sources

**Ownership Rating:**
- Shows media outlet ownership
- Purpose: Transparency about ownership

**Implementation:**
- Ratings applied to news outlets (not individual articles)
- Ratings visible on source cards
- Click to view detailed rating methodology

---

### 5. Bias Comparison Feature (Beta) ✅

**Description:** Compare coverage from different perspectives

**Display:**
- Side-by-side comparison
- Left perspective articles
- Center perspective articles
- Right perspective articles

**Status:** Beta feature

**Purpose:** Step into different viewpoints

---

## 👤 USER FEATURES

### 6. My News Bias ✅

**Purpose:** Personalization based on user preferences

**Configuration:**
- Bias preferences
- Source preferences
- Topic interests
- Region settings

**Access:** Settings → My News Bias

---

### 7. Search & Filtering ✅

**Search:**
- Full-text search
- Real-time results
- Sort options (date, relevance)

**Filtering:**
- By topic/category
- By bias rating
- By source
- By date range

---

### 8. Suggest News Source ✅

**Purpose:** User can submit new sources for review

**Location:** Settings → Support → Suggest News Source

**Process:**
- User submits source URL
- Ground team reviews
- If approved, source added to database

---

## 📧 COMMUNICATION FEATURES

### 9. Newsletters ✅

**Blindspot Report:**
- Frequency: Weekly
- Content: Stories with lopsided coverage
- Delivery: Email

**Subscription Settings:**
- Opt-in via email
- Manage preferences

---

## 💼 BUSINESS FEATURES

### 10. Pro Subscription ✅

**Tier:** Paid subscription model

**Benefits (not fully documented):**
- Enhanced features
- Ad-free experience
- Priority access
- Advanced filters

**Pricing:** Tiered (exact rates need verification)

**Location:** /subscribe page

---

### 11. Group Subscriptions ✅

**Purpose:** Team/organization access

**Use Cases:**
- Teams
- Organizations
- Educational institutions
- Newsrooms

**Features:**
- Shared subscription
- Team management
- Billing coordination

**Location:** /group-subscriptions

---

## 🌐 ACCESSIBILITY FEATURES

### 12. Mobile Optimization ✅
- Responsive design
- Touch-friendly interface
- Native apps (iOS/Android)

### 13. Keyboard Navigation ✅
- Full keyboard support
- Screen reader compatible

### 14. International Editions ✅
- Multiple region support
- Localized bias colors
- Region-specific content

---

## 🔧 TECHNICAL FEATURES

### 15. Browser Extension ✅

**Purpose:** Bias analysis while browsing external sites

**Features:**
- Inline bias indicators
- Source ratings
- Quick access to Ground News

**Location:** /extension page

---

### 16. API Integration ✅

**External Data Sources:**
- Bias rating providers (AllSides, Ad Fontes Media)
- News aggregation APIs
- Multiple outlet integrations

---

## 📊 CONTENT FEATURES

### 17. Story Display

**Article Card Elements:**
- Headline
- Source name with bias indicator
- Timestamp
- Bias bar (distribution of sources covering story)
- Blindspot indicator (if applicable)
- Thumbnail/image
- Share options

**Article Page:**
- Full article content (external link)
- Related stories
- Source breakdown
- Comments (if available)
- Share functionality

---

### 18. Source Cards

**Display Elements:**
- Source name
- Bias rating (number and label)
- Factuality rating
- Ownership information
- Link to full rating details

---

### 19. Navigation Structure

**Main Navigation:**
- Home/Feed
- Blindspot
- Topics
- Search
- Settings

**Settings Sections:**
- My News Bias
- Source Suggestions
- Subscription Management
- Account

---

## 🎨 UX PATTERNS (Observed)

### Reading Experience
- Clean, minimal design
- Bias-focused visual hierarchy
- Quick scanning via card layout
- External article links (not hosting content)

### Micro-Interactions
- Tap bias bar to expand source breakdown
- Hover states on cards
- Loading skeletons (inferred)
- Smooth transitions (inferred)

---

## 🔍 MISSING DATA (Requires Browser Access)

### Visual Design
- ❌ Exact color palette
- ❌ Typography system
- ❌ Spacing/sizing
- ❌ Component library details

### Technical Implementation
- ❌ Frontend framework
- ❌ Backend technology
- ❌ Database schema
- ❌ API endpoints

### UX Details
- ❌ Loading states
- ❌ Error states
- ❌ Animation timings
- ❌ Breakpoint values

---

## 📋 FEATURE SUMMARY

| Category | Feature Count | Status |
|-----------|----------------|---------|
| Core Functionality | 5 | ✅ Partial |
| User Features | 3 | ✅ Partial |
| Communication | 1 | ✅ Partial |
| Business | 2 | ✅ Partial |
| Accessibility | 3 | ✅ Partial |
| Technical | 2 | ✅ Partial |
| Content | 3 | ✅ Partial |
| UX | 1 | ⚠️ Inferred |
| **TOTAL** | **20** | **⚠️ Partial** |

---

## 📊 COMPLETENESS

**Feature Inventory:** ~80% complete
**Missing:** Visual details, technical architecture
**Gap:** Requires browser access for interactive exploration

---

**Next Step:** Access OpenGroundNews codebase for Phase 2 comparison
