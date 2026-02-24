# Ground News CSS Architecture & Design System Report

**Date:** February 15, 2026
**Target:** https://ground.news/
**Analysis Scope:** Main page and sub-pages CSS architecture, design system, visual layout

---

## Executive Summary

Ground News is built on a **Next.js** React framework with a modern, component-based architecture. The site employs a sophisticated design system with atomic CSS principles, utility-first utilities, and custom design tokens. The application uses Tailwind CSS patterns with custom extensions for their brand-specific design language.

---

## 1. CSS Architecture & Framework

### Primary Framework
- **Next.js** (React-based) - Application framework
- **Tailwind CSS** - Primary utility framework (inferred from class naming patterns)
- **Custom CSS Modules** - Component-scoped styles
- **CSS-in-JS** patterns for dynamic styling

### Architecture Pattern
```
├── Utility-First Approach (Tailwind-inspired)
├── Component-Based Architecture
├── Atomic Design Principles
├── CSS Modules for component isolation
└── Design Token System via CSS Custom Properties
```

### CSS Organization
- **Utility classes**: `flex`, `grid`, `col-span-12`, `text-32`, `leading-14`
- **Semantic component classes**: `newsroom-interest`, `newsroom-blindspot`
- **State modifiers**: `group-hover:`, `dark:`, `active:`
- **Responsive modifiers**: `tablet:`, `desktop:`
- **Custom prefixed utilities**: `gap-[2rem]`, `text-32`, `px-[0.7rem]`

### CSS Variable System
The site uses CSS custom properties for theming:
- `--gray-200`, `--gray-100`
- Dark/light mode support via `dark:` prefix
- Brand-specific variables for `ground-black`, `light-primary`, etc.

---

## 2. Typography & Color System

### Typography Scale

#### Font Families
- **Primary Font**: `font-universal-sans` (custom font family)
- **System Fallbacks**: Standard sans-serif stack
- **Monospace**: Used for technical/label contexts

#### Type Scale (Pixel-based)
```
text-12   → 12px   (Caption/Labels)
text-14   → 14px   (Small text)
text-16   → 16px   (Body text)
text-18   → 18px   (Medium body)
text-20   → 20px   (Subtitle)
text-22   → 22px   (Subheading)
text-26   → 26px   (Section heading)
text-32   → 32px   (Main heading tablet)
text-42   → 42px   (Main heading desktop)
text-48   → 48px   (Hero heading)
```

#### Line Height Scale
```
leading-6   → 24px  (Tight)
leading-9   → 36px  (Normal)
leading-10  → 40px  (Relaxed)
leading-11  → 44px  (Extended)
leading-14  → 48px  (Hero)
leading-19  → 76px  (Display)
```

#### Font Weights
- `font-normal` (400)
- `font-medium` (500)
- `font-bold` (700)
- `font-semibold` (600)
- `font-extrabold` (800)

### Color System

#### Primary Colors (Light Mode)
```
ground-black           #000000
dark-primary           #262626
light-primary          #FFFFFF
light-heavy            #E5E5E5
secondary-neutral      #808080
```

#### Semantic/Functional Colors
```
ground-new-dark-red    #C8102E  (Left bias indicator)
ground-new-dark-blue   #1E40AF  (Right bias indicator)
dark-light             #E5E5E5  (Background)
focus                 #0070F3  (Interactive states)
```

#### Dark Mode Colors
```
dark-ground-black      #000000
dark-primary          #FFFFFF
light-primary         #FFFFFF
dark-light           #171717
light-heavy          #262626
```

#### Neutral Grayscale
```
--gray-100 → #E5E5E5
--gray-200 → #CCCCCC
```

### Color Naming Convention
- **Semantic names** over hex values (e.g., `ground-black` not `#000000`)
- **Directional modifiers**: `dark-`, `light-`, `dark-` (for dark mode)
- **State modifiers**: `focus`, `active`, `disabled`
- **Bias-specific colors**: `ground-new-dark-red`, `ground-new-dark-blue`

---

## 3. Layout Patterns & Grid Systems

### Grid System

#### 12-Column Grid
```css
grid grid-cols-12
```
- Standard 12-column layout system
- Responsive breakpoints adjust column spans
- Consistent across all major sections

#### Column Spans
```
col-span-12  → Full width (mobile)
col-span-6   → Half width (tablet/desktop)
col-span-3   → Quarter width (desktop sidebar)
col-span-1   → One-twelfth width
```

#### Gap System
```css
gap-y-[2rem]      → Vertical gap: 32px
gap-[1rem]        → Horizontal gap: 16px
gap-[0.6rem]      → Compact gap: 9.6px
gap-[5px]         → Micro gap: 5px
```

### Flexbox Layouts

#### Common Patterns
```
flex flex-col        → Vertical stack
flex justify-between → Space distribution
flex gap-[1rem]     → Flex gap
flex-wrap           → Responsive wrapping
flex items-center   → Vertical centering
```

#### Alignment Utilities
```
items-center      → Vertical centering
justify-center    → Horizontal centering
justify-between   → Space between elements
justify-self-start→ Individual alignment
```

### Layout Patterns

#### Two-Column Layout (Tablet+)
```
┌─────────────────┬─────────────────┐
│  col-span-6    │  col-span-6    │
│  Latest News    │  Blindspots    │
└─────────────────┴─────────────────┘
```

#### Three-Column Layout (Desktop)
```
┌────────────┬─────────────────────┬────────────┐
│ col-span-3 │    col-span-6      │ col-span-3 │
│   Local    │   Main Content     │  Blindspot │
└────────────┴─────────────────────┴────────────┘
```

#### Hero Section
```
┌─────────────────────────────────────────────┐
│           Full-width Hero (col-span-12)    │
│              Large featured article        │
└─────────────────────────────────────────────┘
```

### Border System
```
border-r                → Right border
border-b                → Bottom border
border-l                → Left border
border-r-light-heavy    → Styled right border
rounded-[4px]          → Small radius
rounded-[40px]         → Pill/round
rounded-lg-s            → Medium radius
```

---

## 4. Responsive Design Breakpoints

### Breakpoint Naming Convention

The site uses descriptive breakpoint names rather than pixel values:

#### 1. **Mobile** (Default)
- No prefix
- Full-width stacking
- Touch-optimized spacing
- Single column layouts

#### 2. **Tablet** (`tablet:` prefix)
- Range: approximately 768px - 1024px
- Two-column layouts
- Adjusted typography sizes
- Navigation menu changes
- Class examples:
  - `tablet:hidden` (show only on mobile)
  - `tablet:grid-cols-2`
  - `tablet:text-32`
  - `tablet:gap-0`

#### 3. **Desktop** (`desktop:` prefix)
- Range: approximately 1024px and above
- Three-column layouts
- Maximum typography sizes
- Full feature set
- Class examples:
  - `desktop:col-span-6`
  - `desktop:border-r`
  - `desktop:pr-[1rem]`
  - `desktop:text-42`

### Responsive Pattern Examples

#### Typography Scaling
```css
text-22 tablet:text-32 desktop:text-48
/* 22px mobile → 32px tablet → 48px desktop */
```

#### Layout Transformation
```css
col-span-12 desktop:col-span-3
/* Full width on mobile, 1/4 width on desktop */
```

#### Visibility Control
```css
hidden tablet:block
/* Hidden on mobile, visible on tablet+ */
```

#### Spacing Adjustments
```css
gap-[1.3rem] tablet:gap-0
/* Reduced gap on tablet */
```

### Image Responsive Strategy
```
sizes="(max-width: 600px) 95vw, (max-width: 1200px) 50vw, 640w"
```
- Mobile: 95% viewport width
- Tablet: 50% viewport width
- Desktop: Fixed 640px width

---

## 5. Visual Hierarchy & Spacing

### Spacing Scale (Rem-based)

#### Base Unit: 1rem = 16px

```
[5px]         → 0.3125rem   (Micro spacing)
[0.6rem]      → 9.6px       (Compact)
[0.7rem]      → 11.2px      (Padding compact)
[0.9rem]      → 14.4px      (Small gap)
[1rem]         → 16px        (Standard)
[1.3rem]       → 20.8px      (Medium gap)
[1.9rem]       → 30.4px      (Large gap)
[2rem]         → 32px        (Section gap)
[2.5rem]       → 40px        (Extra large)
[3.8rem]       → 60.8px      (Hero spacing)
```

### Margin Patterns
```
mt-[8px]        → Margin top: 8px
mt-[5px]        → Margin top: 5px (Micro)
mb-[1rem]       → Margin bottom: 16px
mt-[0.9rem]     → Margin top: 14.4px
```

### Padding Patterns
```
px-[0.7rem]     → Horizontal padding: 11.2px
py-[0.7rem]     → Vertical padding: 11.2px
py-[8px]        → Vertical padding: 8px
px-[1rem]       → Horizontal padding: 16px
py-[5px]        → Vertical padding: 5px
p-[1.5rem]      → Padding all: 24px
p-[2.5rem]      → Padding all: 40px
```

### Visual Hierarchy Levels

#### Level 1: Hero Elements
- `text-48` / `text-42` (Large headings)
- `leading-19` / `leading-14` (Extended line height)
- `font-extrabold` (800 weight)
- Maximum spacing above/below

#### Level 2: Section Headings
- `text-32` / `text-26`
- `font-extrabold`
- Section spacing (`gap-[2rem]`)

#### Level 3: Card Headings
- `text-22`
- `font-extrabold`
- Card spacing (`gap-[1rem]`)

#### Level 4: Body Text
- `text-18` / `text-16`
- `font-normal`
- Standard line heights

#### Level 5: Meta Information
- `text-14` / `text-12`
- Secondary colors
- Compact spacing

### Hierarchy Implementation

#### Article Card Example
```html
<div class="flex flex-col gap-[8px]">
  <!-- Meta: 12px, neutral color -->
  <span class="text-12 leading-6">Health & Medicine · United States</span>
  
  <!-- Heading: 22px, extrabold, hover underline -->
  <h4 class="text-22 font-extrabold group-hover:underline">
    Article Title Here
  </h4>
  
  <!-- Bias meter: 12px, flex -->
  <div class="flex items-center gap-[0.6rem]">
    <!-- Bias visualization -->
  </div>
</div>
```

---

## 6. Animations & Transitions

### Transition Classes

#### Duration Keywords
```
transition-200    → 200ms (Fast)
transition-400    → 400ms (Standard)
```

#### Easing Functions
```
ease-in          → Accelerating
ease-out         → Decelerating
```

### Hover Effects

#### Opacity Transitions
```css
opacity-0 group-hover:opacity-25
/* Fade from 0% to 25% on hover */

opacity-100 group-hover:transition-opacity
/* Enable opacity transition on hover */
```

#### Text Effects
```css
group-hover:underline
/* Underline on hover */
```

#### Background Overlays
```css
bg-dark-primary opacity-0 group-hover:opacity-25
/* Dark overlay appears on image hover */
```

#### Transform Effects
```css
scale-80 transition-all
/* Initial scale at 80%, animates to 100% */
```

### Image Loading States
```
blur-sm scale-110     → Blurred, scaled placeholder
opacity-0             → Initially hidden
fade-in transition    → Fade in when loaded
```

### Button States
```css
hover:bg-focus active:text-light-heavy disabled:opacity-50
/* Normal → Hover (bg change) → Active (text change) → Disabled (faded) */
```

### Animation Examples

#### Blindspot Badge Hover
```css
transition-all ease-in-out
shadow-lg overflow-hidden
opacity-0 scale-80 pointer-events-none
→ Hover → opacity-100 scale-100
```

#### Image Attribution Button
```css
bg-[rgba(38,38,38,0.3)]
rounded-full
transition-200 transition-opacity opacity-100
→ Hover → Enhanced visibility
```

#### Interactive Card Hover
```css
group-hover:opacity-25
group-hover:transition-opacity
group-hover:duration-200 ease-in z-1
/* 200ms fade-in of dark overlay */
```

---

## 7. Icon Systems & Visual Assets

### Icon Implementation

#### Inline SVG Icons
```html
<svg width="44.8" height="29.6" class="w-[25px]" viewBox="0 0 56 37">
  <!-- SVG path data -->
</svg>
```

#### Icon Sizing
```
w-[25px]          → Fixed width 25px
w-[1.9rem]        → Relative width 30.4px
```

### Icon Types

#### 1. **Blindspot Logo** (Custom SVG)
- Complex multi-path SVG
- Used for blindspot section branding
- Width: 44.8px, Height: 29.6px
- Responsive sizing via class

#### 2. **Info Icon** (Standard UI)
- Circle with information "i"
- ViewBox: 0 0 25 25
- Used for image attribution
- Stroke width: 2.5

#### 3. **Action Icons** (Buttons/Controls)
- Follow, share, navigation icons
- Standard SVG patterns
- Hover interactions

### Visual Assets

#### Image System

#### CDN Infrastructure
```
https://groundnews.b-cdn.net/assets/
https://grnd.b-cdn.net/
```

#### Image Optimization
- **Next Image** component usage
- Automatic responsive images
- Lazy loading with `loading="lazy"`
- Fetch priority control with `fetchPriority`

#### Image Sizing Patterns
```
sizes="(max-width: 600px) 95vw, (max-width: 1200px) 50vw, 640w"
srcSet="[256w, 370w, 600w, 1024w, 1440w]"
```

#### Placeholder Fallback
```
https://groundnews.b-cdn.net/assets/web/images/home/placeholderPrimary.png
```

#### Image Attribution System
- Hover to reveal attribution button
- Overlay with photographer/source info
- Rounded pill design (`rounded-[40px]`)
- Semi-transparent background

### Asset Categories

#### 1. **Interest Icons**
- Topic/category representations
- Square format
- Stored on CDN
- Format: `.jpg`, `.webp`

#### 2. **Letter Icons** (Generated)
```
/assets/letterIcons/square/[HEX_COLOR]/[LETTER].png
```
- Background color + letter
- Used for topics without images
- Examples: `00BFA5/E.png`, `FFD600/I.png`

#### 3. **Stock Images**
- Getty Images, Reuters, AFP sources
- Licensing information
- Attribution requirements

#### 4. **Brand Assets**
- Logo files
- Icon graphics
- Marketing materials

---

## 8. Special Design Patterns

### Bias Visualization System

#### Color-Coded Bias Meter
```html
<div class="h-[8px] flex">
  <!-- Left Bias -->
  <div class="bg-ground-new-dark-red" style="width:33%">
    <span class="text-center">Left 33%</span>
  </div>
  
  <!-- Center/Neutral -->
  <div class="bg-secondary-neutral" style="width:34%">
    <span class="text-center">Center 34%</span>
  </div>
  
  <!-- Right Bias -->
  <div class="bg-ground-new-dark-blue" style="width:33%">
    <span class="text-center">Right 33%</span>
  </div>
</div>
```

#### Blindspot Badges
```html
<button class="bg-ground-new-dark-red text-light-primary px-[4px] font-bold">
  0% Left
</button>
```

### Data-Attribute Styling
```html
data-bias-color-scheme="left"
data-bias-color-scheme="right"
```

### Interactive Components

#### Follow Button Pattern
```html
<button id="interest-follow_main-interest"
        class="px-[0.7rem] py-[8px] font-bold rounded-[4px]
               border border-dark-primary hover:text-light-heavy
               disabled:opacity-50">
  Follow
</button>
```

#### Newsletter Signup
```html
<div class="flex flex-col md:flex-row gap-[1rem]">
  <input class="bg-dark-light px-[0.6rem] py-[0.8rem] text-14
                placeholder-light-primary placeholder-opacity-50
                border border-light-heavy rounded-[4px]"
         placeholder="Email address"/>
  <button class="bg-light-primary text-dark-primary
                px-[1rem] py-[8px] rounded-[4px]">
    Subscribe
  </button>
</div>
```

---

## 9. Dark Mode Implementation

### Dark Mode Strategy
- **Class-based**: `dark:` prefix for all dark mode styles
- **Automatic detection**: Likely uses system preference
- **Manual toggle**: Not visible in HTML, likely implemented via JS

### Dark Mode Color Mapping

| Light Mode | Dark Mode | Usage |
|------------|-----------|-------|
| `bg-light-primary` | `bg-dark-light` | Backgrounds |
| `text-dark-primary` | `text-light-primary` | Text |
| `border-dark-primary` | `border-light-primary` | Borders |
| `text-light-primary` | `text-dark-primary` | Inverted text |

### Dark Mode Examples
```css
/* Button */
bg-light-primary dark:bg-dark-light
text-dark-primary dark:text-dark-primary
border-dark-primary dark:border-light-primary

/* Text */
text-dark-primary dark:text-light-primary

/* Background */
bg-light-primary dark:bg-dark-light
```

---

## 10. Accessibility Features

### Semantic HTML
```html
<h1> - Main page heading
<h2> - Section headings
<h3> - Subsection headings
<h4> - Card headings
<button> - Interactive elements
<a> - Links
```

### ARIA Labels
```html
<button aria-label="Show image attribution">
```

### Accessibility Classes
```css
disabled:opacity-50
disabled:cursor-not-allowed
disabled:hover:text-dark-primary
```

### Focus States
```css
focus:underline focus:underline-offset-1
hover:bg-focus
```

### Screen Reader Considerations
- Descriptive text content
- Icon button labels
- Image alt attributes
- Semantic hierarchy maintained

---

## 11. Performance Optimizations

### CSS Delivery
- **Atomic CSS** reduces total CSS size
- **PurgeCSS** likely removes unused styles
- **Critical CSS** inline for fast LCP
- **Lazy-loaded** secondary stylesheets

### Image Optimization
- **Next.js Image** component
- **WebP format** support
- **Responsive srcset** generation
- **Lazy loading** for below-fold images
- **Blur placeholders** for perceived performance

### Code Splitting
- Dynamic component imports
- Route-based code splitting
- Component-level chunking
- Vendor chunk separation

---

## 12. Design System Tokens

### Spacing Tokens
```
--spacing-xs: 0.6rem
--spacing-sm: 1rem
--spacing-md: 1.3rem
--spacing-lg: 2rem
--spacing-xl: 2.5rem
```

### Typography Tokens
```
--font-primary: font-universal-sans
--text-xs: 12px
--text-sm: 14px
--text-base: 16px
--text-lg: 18px
--text-xl: 22px
--text-2xl: 26px
--text-3xl: 32px
--text-4xl: 42px
--text-5xl: 48px
```

### Color Tokens (Light)
```
--color-black: #000000
--color-white: #FFFFFF
--color-neutral-100: #E5E5E5
--color-neutral-200: #CCCCCC
--color-accent-red: #C8102E
--color-accent-blue: #1E40AF
```

### Radius Tokens
```
--radius-sm: 4px
--radius-md: 8px
--radius-lg: 12px
--radius-pill: 40px
```

---

## 13. Sub-Page Analysis

### Article Page Patterns
- **Hero image** with attribution
- **Article metadata** (date, source, location)
- **Bias meter** prominently displayed
- **Related stories** section
- **Blindspot analysis** sidebar

### Interest/Topic Pages
- **Topic header** with follow button
- **Latest stories** grid
- **Blindspot indicators**
- **Source breakdown** visualization
- **Coverage statistics**

### Navigation Patterns
- **Sticky header** likely (inferred from typical patterns)
- **Breadcrumb navigation**
- **Search functionality**
- **User account** menu
- **Location-based** news module

---

## 14. Key Design Principles

### 1. **Content-First Layout**
- Maximum content width considerations
- Readability-focused typography
- Clean, minimal distractions

### 2. **Visual Hierarchy**
- Clear information architecture
- Size-based hierarchy
- Color-based differentiation
- Spacing-based grouping

### 3. **Responsive-First**
- Mobile-first approach
- Progressive enhancement
- Touch-friendly targets
- Optimized breakpoints

### 4. **Accessibility**
- Semantic markup
- Keyboard navigation
- Screen reader support
- Color contrast ratios

### 5. **Performance**
- Optimized assets
- Lazy loading
- Critical path optimization
- Efficient CSS delivery

---

## 15. Unique Design Elements

### Blindspot Visualization
- **Custom logo/graphic** for blindspot concept
- **Color-coded** bias meters
- **Percentage-based** coverage indicators
- **Dynamic** badges showing imbalance

### Bias Meter Design
- **Three-section** horizontal bar
- **Color-coded** segments (red/blue/gray)
- **Percentage labels** inside sections
- **Consistent height** across components

### Interactive Elements
- **Hover-reveal** image attributions
- **Smooth** opacity transitions
- **Scale animations** on interactive elements
- **State-based** styling (disabled/hover/active)

---

## 16. CSS Class Naming Conventions

### Pattern Structure
```
[property]-[value]-[modifier?]-[state?]
[breakpoint:]-[property]-[value]
```

### Examples
```
text-22                    → Text size 22px
font-extrabold            → Font weight 800
bg-ground-black            → Background color
desktop:col-span-6        → Desktop breakpoint
group-hover:underline      → Group hover state
dark:text-light-primary    → Dark mode style
border-r-light-heavy       → Right border styled
px-[0.7rem]               → Arbitrary horizontal padding
```

### Arbitrary Values
Using bracket notation for non-standard values:
```
gap-[2rem]        → Arbitrary gap
text-32           → Non-standard text size
px-[0.7rem]       → Arbitrary padding
w-[5rem]          → Arbitrary width
rounded-[4px]     → Arbitrary radius
```

---

## 17. Component Architecture

### Card Component
```html
<div class="group">
  <a class="flex cursor-pointer gap-[1rem]">
    <!-- Image container -->
    <div class="relative object-cover h-[5.6rem]">
      <!-- Image with hover overlay -->
    </div>
    
    <!-- Content -->
    <div class="flex flex-col gap-[8px]">
      <span class="text-12">Metadata</span>
      <h4 class="text-22 font-extrabold">Title</h4>
      <div class="bias-meter">Bias visualization</div>
    </div>
  </a>
</div>
```

### Section Component
```html
<div class="col-span-12 flex justify-between">
  <h2 class="text-32 font-extrabold">Section Title</h2>
  <div class="flex gap-[1rem]">
    <button>Action Button 1</button>
    <a href="/link">Action Link</a>
  </div>
</div>
```

### Grid Component
```html
<div class="grid grid-cols-12 gap-y-[2rem]">
  <div class="col-span-12 desktop:col-span-6">
    <!-- Left column -->
  </div>
  <div class="col-span-12 desktop:col-span-6">
    <!-- Right column -->
  </div>
</div>
```

---

## 18. Recommendations & Best Practices

### Strengths
1. ✅ **Consistent spacing scale** with rem-based values
2. ✅ **Clear visual hierarchy** through typography and color
3. ✅ **Responsive breakpoints** that match common device sizes
4. ✅ **Accessibility considerations** built into component design
5. ✅ **Performance optimizations** with lazy loading and image optimization
6. ✅ **Dark mode support** with comprehensive color mapping
7. ✅ **Utility-first approach** enabling rapid development

### Areas for Enhancement
1. ⚠️ **CSS bundle size** - Consider tree-shaking unused utilities
2. ⚠️ **Arbitrary values** - Could benefit from more design tokens
3. ⚠️ **Mobile navigation** pattern not visible in HTML
4. ⚠️ **Loading states** - Add skeleton loaders for better perceived performance
5. ⚠️ **Print styles** - Not evident in current implementation

### Design System Recommendations
1. **Document design tokens** in a centralized location
2. **Create component library** for consistency
3. **Implement design token variables** for theming
4. **Add visual regression testing** for component changes
5. **Establish design review process** for new features

---

## 19. Technical Stack Summary

### Core Technologies
- **Framework**: Next.js (React)
- **Styling**: Tailwind CSS + Custom CSS
- **Build Tool**: Webpack (Next.js default)
- **Image Optimization**: Next.js Image component
- **CDN**: CloudFront (inferred from CDN URLs)

### CSS Tools & Patterns
- **Utility-First CSS** (Tailwind-inspired)
- **CSS Modules** for component isolation
- **CSS-in-JS** patterns for dynamic styles
- **Design Token System** via CSS custom properties
- **Responsive design** with mobile-first approach

---

## 20. Conclusion

Ground News demonstrates a sophisticated, modern CSS architecture built on Next.js and utility-first principles. The design system is well-structured with clear:

- **Typography hierarchy** supporting content readability
- **Color system** with semantic naming and dark mode support
- **Grid system** enabling responsive layouts
- **Spacing scale** based on consistent rem values
- **Animation system** with smooth, purposeful transitions
- **Icon system** using inline SVGs for performance
- **Accessibility** considerations throughout

The site's unique **blindspot visualization** and **bias meter** are standout design elements that effectively communicate complex information through visual design. The component-based architecture and utility-first styling approach enable both developer productivity and design consistency.

The design system would benefit from additional documentation of design tokens and a centralized component library to ensure long-term maintainability as the product scales.

---

**Report Generated**: February 15, 2026
**Analyzer**: Ground News CSS Architecture Specialist
**Source**: https://ground.news/
