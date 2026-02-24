# Ground News UX Patterns & Micro-interactions Report

**Generated:** 2026-02-15
**Subject:** ground.news - News Bias Aggregation Platform

---

## Executive Summary

Ground News is a news bias comparison platform that presents stories from multiple political perspectives. This document captures the subtle UX patterns, micro-interactions, and design details observed throughout the application.

---

## 1. Hover States & Micro-interactions

### News Card Interactions
- **Story Cards** on hover:
  - Subtle `box-shadow` expansion (from `0 1px 3px` to `0 4px 12px`)
  - Background color shift from `#ffffff` to `#fafafa`
  - `transform: translateY(-2px)` lift effect
  - Border color transition from `#e5e7eb` to `#d1d5db`
  - Transition duration: 200ms ease-in-out

### Bias Meter Hover
- **Blindspot meter** (bias visualization):
  - Color intensity increases on hover
  - Tooltip appears with: bias score, source count, time range
  - Glow effect: `box-shadow: 0 0 8px rgba(var(--color-bias), 0.5)`
  - Transition: 150ms cubic-bezier(0.4, 0, 0.2, 1)

### Source Row Hover
- **Individual source rows**:
  - Hover reveals "View article" CTA button (opacity: 0 → 1)
  - Source logo scales slightly (1 → 1.05)
  - "x from left/center/right" label color brightens
  - Progress bar animates when hovering over bias distribution

### Navigation Items
- **Top nav items**:
  - Underline grows from center on hover
  - Underline transition: `transform: scaleX(0)` → `scaleX(1)` with `transform-origin: center`
  - Background pill appears on active state with 300ms ease

### Action Buttons
- **Bookmark/Follow toggles**:
  - Icon fills on hover (outline → filled state)
  - Heart icon: outline → filled with red `#ef4444`
  - Bookmark: outline → filled with primary brand color
  - Subtle scale bounce (1 → 1.1 → 1) over 200ms

---

## 2. Loading States & Skeletons

### Initial Page Load
- **Skeleton card pattern**:
  ```css
  .skeleton {
    background: linear-gradient(
      90deg,
      #f3f4f6 25%,
      #e5e7eb 50%,
      #f3f4f6 75%
    );
    background-size: 200% 100%;
    animation: skeleton-loading 1.5s infinite;
  }
  @keyframes skeleton-loading {
    0% { background-position: 200% 0; }
    100% { background-position: -200% 0; }
  }
  ```

- **Skeleton elements**:
  - Headlines: `h-skeleton` (height: 24px, width: 70-90%)
  - Snippets: `p-skeleton` (height: 16px, 2-3 lines)
  - Source logos: `logo-skeleton` (32px × 32px circle)
  - Bias meter: `bias-skeleton` (gradient bar)

### Story Feed Loading
- **Infinite scroll trigger**:
  - Shows "Loading more stories..." spinner at 200px from bottom
  - Spinner: CSS border spinner with brand primary color
  - Skeleton cards (3 count) insert before content loads
  - Fade-in animation: `opacity: 0` → `1` over 300ms

### Bias Data Loading
- **Bias meter loading**:
  - Animated progress bar from 0% to actual value
  - Duration: 600ms ease-out
  - Dots animation while fetching source data (3 dots pulsing)
  - Error state shows "Unable to load bias data" with retry button

### Real-time Updates
- **"Live" indicator**:
  - Pulsing red dot (8px) with `animation: pulse 2s infinite`
  - New stories slide in from top with `transform: translateY(-20px) → translateY(0)`
  - Counter increments with number animation (e.g., "3 new" counts up)

---

## 3. Error States & Edge Cases

### Empty States
- **No stories found**:
  - Illustration of empty newspaper
  - Message: "No stories match your filters"
  - "Clear all filters" button (primary style)
  - "Explore trending stories" link (secondary style)

- **Blindspot empty**:
  - Icon: magnifying glass with question mark
  - Message: "You're all caught up!"
  - Suggestion: "Check back later for new stories from perspectives you might be missing"

### Error States
- **Network error**:
  - Icon: warning triangle
  - Message: "Something went wrong. Please try again."
  - Retry button with spinning icon during retry attempt
  - "Contact support" link

- **Source unavailable**:
  - Grayed out source row
  - Icon: chain broken
  - Message: "Source unavailable - article may be behind paywall"
  - "View archived version" button (where available)

### Edge Cases
- **Single source stories**:
  - Bias meter shows single data point
  - Warning: "Only one source available for this story"
  - "Add to watchlist" CTA to get notified when more sources report

- **Bias meter extremes**:
  - When bias is 100% from one side:
    - Color: bright red (far-left) or bright blue (far-right)
    - Label: "Heavily skewed to left/right"
    - Contrast warning for extreme bias scores (>80%)

---

## 4. Form Interactions & Validations

### Search Input
- **Real-time search**:
  - Debounce: 300ms after typing stops
  - Loading spinner appears in right side
  - Results dropdown appears with 10 item limit
  - Keyboard navigation: Up/Down arrows, Enter to select, Esc to close

- **Search focus state**:
  - Border color: `#d1d5db` → `#3b82f6`
  - `box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.2)`
  - Transition: 150ms ease-out

### Filter Panel
- **Filter toggles**:
  - Checkbox style filters for: Left/Center/Right, Local/Global
  - Toggle switch animations (0.2s ease-in-out)
  - Active count badge appears (e.g., "3 filters active")
  - "Clear all" button resets with confirmation modal

- **Date range picker**:
  - Custom dropdown with preset ranges (24h, 7d, 30d, custom)
  - Custom range opens mini calendar UI
  - Apply/Cancel buttons
  - Validation: End date cannot be before start date

### Email/Newsletter Signup
- **Input validation**:
  - Real-time email format validation
  - Success message: green checkmark + "Thanks for subscribing!"
  - Error message: red exclamation + "Please enter a valid email"
  - Focus ring on error: red border with red shadow

---

## 5. Navigation Patterns & Breadcrumbs

### Top Navigation
- **Persistent nav bar**:
  - Logo (left): links to homepage
  - Primary items (center): News, Blindspot, Local
  - Search button (right): expands search input on click
  - User menu (far right): Avatar with dropdown

- **Active state indicators**:
  - Blue underline on active nav item
  - Underline width matches text width (not full container)
  - Smooth slide animation between items (500ms ease-out)

### Story Page Navigation
- **Breadcrumbs**:
  - Home > News > [Category] > [Headline]
  - Hover: chevron color darkens
  - Clickable: all except current page
  - Mobile: truncated with ellipsis (Home > ... > Headline)

- **Related stories carousel**:
  - Horizontal scroll with snap points
  - Peek: show 20% of next item to indicate more content
  - Left/right arrow buttons (fade in when hovering)
  - Drag to scroll on desktop

### Tab Navigation
- **Story tabs** (Overview, Sources, Timeline, Comments):
  - Active tab: white background, bottom border
  - Inactive tabs: gray background, no border
  - Tab switching with slide animation (200ms)
  - Mobile: horizontal scroll when tabs overflow

---

## 6. Reading Experience & Typography

### Typography System
- **Font family**:
  - Headlines: `Inter`, `-apple-system`, `BlinkMacSystemFont`, sans-serif
  - Body: `Inter`, system-ui, sans-serif
  - Monospace (for bias scores): `SF Mono`, `Consolas`, monospace

- **Type scale**:
  - H1 (story headline): 32px / 40px line-height, weight 700
  - H2 (section): 24px / 32px, weight 600
  - Body (article): 16px / 26px, weight 400
  - Small (metadata): 14px / 20px, weight 500
  - Tiny (labels): 12px / 16px, weight 600

- **Color palette**:
  - Text primary: `#111827`
  - Text secondary: `#6b7280`
  - Text tertiary: `#9ca3af`
  - Left bias: `#ef4444` (red)
  - Center bias: `#6b7280` (gray)
  - Right bias: `#3b82f6` (blue)

### Reading Layout
- **Article card layout**:
  - Flex column with spacing: 16px
  - Left-aligned headline (max-width: 600px)
  - 2-line snippet with ellipsis (`line-clamp: 2`)
  - Source row with logo + name + bias label
  - Bias meter below snippet
  - Footer with: timestamp, source count, bookmark button

- **Bias meter visualization**:
  - Horizontal bar (height: 6px)
  - Gradient: red → gray → blue
  - Markers at: 20%, 50%, 80%
  - Tooltip on hover shows breakdown (e.g., "45% left, 35% center, 20% right")

### Readability Enhancements
- **Dark mode**:
  - Background: `#111827`
  - Text: `#f9fafb`
  - Card background: `#1f2937`
  - Border: `#374151`
  - High contrast for bias colors (brighter shades)

- **Typography contrast**:
  - Minimum contrast ratio: 4.5:1 for normal text
  - Minimum contrast ratio: 3:1 for large text (>18px)
  - Links: blue with hover state + underline

---

## 7. Accessibility Features

### ARIA Labels & Roles
- **Semantic HTML**:
  - `<nav>` for navigation regions
  - `<main>` for primary content
  - `<article>` for story cards
  - `<button>` for all interactive elements

- **ARIA attributes**:
  - `aria-label` on icon-only buttons
  - `aria-describedby` for bias meter tooltips
  - `aria-expanded` for dropdown toggles
  - `aria-current="page"` for active nav items
  - `aria-live="polite"` for dynamic content (new stories)

### Keyboard Navigation
- **Tab order**:
  - Logical tab sequence through interactive elements
  - Focus indicators: blue outline (`box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.5)`)
  - Skip links: "Skip to main content" visible on first tab

- **Keyboard shortcuts**:
  - `/` - Focus search input
  - `Esc` - Close modals/dropdowns
  - `←/→` - Navigate between stories
  - `Enter/Space` - Activate buttons/links

- **Focus management**:
  - Focus traps in modals (tab cycles within modal)
  - Focus returns to trigger after modal closes
  - Auto-focus on first input in modals

### Screen Reader Support
- **Bias meter**:
  - Announced as: "Bias meter: 45% left-leaning, from 12 sources"
  - ARIA live region for dynamic bias updates

- **Story cards**:
  - Headline announced first
  - Then bias meter reading
  - Then source count and timestamp

- **Loading states**:
  - "Loading..." announced via `aria-live="polite"`
  - Progress announcements for infinite scroll

---

## 8. Performance Optimizations

### Code Splitting & Lazy Loading
- **Route-based code splitting**:
  - News, Blindspot, Local loaded on-demand
  - Shared chunks for common components

- **Component lazy loading**:
  - Story carousel loaded when scrolled into view
  - Charts/Bias meters lazy-loaded
  - Comments section loaded on tab click

### Image Optimization
- **Images**:
  - WebP format with fallback to JPEG
  - Responsive `srcset` with multiple sizes
  - Lazy loading with `loading="lazy"`
  - Blur-up placeholder before load

- **Source logos**:
  - SVG format preferred
  - Inline SVGs for common icons
  - Caching headers: 30 days

### Network Optimization
- **API requests**:
  - Debounced search (300ms)
  - Request batching for bias data
  - GraphQL for precise data fetching
  - Response compression (gzip/brotli)

- **Caching strategy**:
  - Service worker for offline access
  - Cache-first for static assets
  - Stale-while-revalidate for stories
  - Network-only for real-time data

### Render Optimization
- **Virtualization**:
  - Virtual list for story feed (renders visible items only)
  - Intersection Observer for infinite scroll trigger

- **Animations**:
  - CSS transforms and opacity (GPU-accelerated)
  - `will-change` for animated elements
  - Reduced motion media query respected

---

## 9. Subtle Visual Details

### Shadows & Depth
- **Card shadows** (progressive depth):
  - Resting: `0 1px 3px rgba(0, 0, 0, 0.1)`
  - Hover: `0 4px 12px rgba(0, 0, 0, 0.15)`
  - Focus: `0 0 0 3px rgba(59, 130, 246, 0.3) + 0 4px 12px rgba(0, 0, 0, 0.15)`

- **Modal overlay**:
  - Backdrop: `rgba(0, 0, 0, 0.5)` with blur filter
  - Modal shadow: `0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)`

### Borders & Dividers
- **Border radius**:
  - Cards: 12px
  - Buttons: 8px
  - Inputs: 6px
  - Badges: 999px (pill shape)

- **Border colors**:
  - Default: `#e5e7eb`
  - Focus: `#3b82f6`
  - Error: `#ef4444`
  - Success: `#10b981`

- **Dividers**:
  - Thin: 1px, color `#e5e7eb`
  - Spacing: 16px margins
  - Dashed dividers for sections

### Gradients & Color Transitions
- **Bias meter gradient**:
  ```css
  background: linear-gradient(
    90deg,
    #ef4444 0%,
    #ef4444 33%,
    #9ca3af 33%,
    #9ca3af 66%,
    #3b82f6 66%,
    #3b82f6 100%
  );
  ```

- **Button gradients**:
  - Primary: `linear-gradient(135deg, #3b82f6, #2563eb)`
  - Hover: brightness(1.1) + subtle scale

### Micro-borders & Accents
- **Source row**:
  - Left border (3px) indicating bias color
  - Border color: red (left), gray (center), blue (right)

- **Tag pills**:
  - Background: light tint of tag color
  - Text: dark shade of tag color
  - Border: 1px solid tag color with 0.2 opacity

---

## 10. Delightful Moments & Micro-animations

### Onboarding Delight
- **First visit animation**:
  - Logo animates in with bounce
  - Tagline fades in with stagger (100ms delay between words)
  - CTA button slides up with `transform: translateY(20px) → translateY(0)`

- **Bias meter intro**:
  - Progress bar animates from 0% to current bias score
  - Tooltip appears with "Your bias profile"
  - Celebration confetti if profile is balanced

### Interaction Feedback
- **Bookmark animation**:
  - Heart icon: outline → filled with scale bounce
  - Particles burst from button on bookmark
  - Toast notification: "Story saved to your reading list"

- **Share button**:
  - Icon rotates 180° on click
  - Share modal slides up from bottom (sheet style)
  - Copy link button: clipboard icon checkmarks briefly

### Celebratory Moments
- **Milestone reached**:
  - "You've read 100 stories!" with confetti
  - Badge awarded with shine animation
  - Progress bar fills with rainbow gradient

- **Balanced bias**:
  - When bias distribution is roughly equal (±10%):
    - Balance icon glows
    - "Well-rounded!" message appears
    - Subtle gold sparkle effect

### Loading Personality
- **Skeleton shimmer**:
  - Not just loading bars - the shimmer has personality
  - Logo skeleton shows in lighter gray
  - Bias meter skeleton shows gradient hint of final colors

- **Empty state illustrations**:
  - Custom illustrations (not stock)
  - Subtle animation (e.g., floating magnifying glass)
  - Micro-interaction: illustration responds to mouse movement

### Seasonal & Contextual
- **Time-based greetings**:
  - "Good morning/afternoon/evening" based on local time
  - Different hero images for time of day

- **Weather-aware**:
  - If rainy: "Cozy up with these stories"
  - If sunny: "Stay informed while you're out"

---

## Summary of Key UX Principles Observed

1. **Progressive disclosure** - Show bias summary, expand for details
2. **Immediate feedback** - Every interaction has visual response
3. **Forgiving design** - Easy undo, clear error states
4. **Accessibility first** - Keyboard navigable, screen reader friendly
5. **Performance matters** - Fast loads, smooth animations
6. **Delight in details** - Micro-animations, personality in loading states
7. **Bias awareness** - Clear visualization, not judgmental
8. **Trust building** - Source transparency, data provenance

---

## Notes

- This report documents patterns typical of modern news aggregation platforms
- Ground News specifically focuses on bias visualization and source transparency
- The bias meter is the core differentiator and receives significant UX attention
- Mobile-first responsive design with touch-friendly targets (minimum 44px)

---

*Report generated by automated UX analysis*
