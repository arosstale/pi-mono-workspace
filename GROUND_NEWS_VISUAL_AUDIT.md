# Ground News Visual Audit Report

**Date:** February 15, 2026  
**Audited Pages:** Homepage (ground.news)  
**Method:** HTML/CSS analysis via content extraction

---

## Executive Summary

Ground News employs a sophisticated, modern design system built on a Tailwind CSS-inspired framework. The visual language emphasizes clarity, accessibility, and data-driven storytelling through a refined color palette, systematic typography, and consistent component patterns.

---

## 1. Color Palette and Usage

### Primary Brand Colors
- **Black/Dark (`ground-black`, `dark-primary`)**: Primary text color, main CTA backgrounds
- **White/Light (`light-primary`)**: Backgrounds, text in dark mode, button backgrounds
- **Gray Neutrals**:
  - `secondary-neutral`: Center bias indicator background
  - `gray-100`, `gray-200`: Placeholder and divider colors

### Semantic Colors (Bias Visualization)
- **Left Bias**:
  - `ground-red`, `ground-new-dark-red`: #FF0000 range
  - Used for left-leaning bias indicators (0-50% coverage)
  
- **Center Bias**:
  - `secondary-neutral`: Neutral gray
  - Used for centrist/center coverage
  
- **Right Bias**:
  - `ground-blue`, `ground-new-dark-blue`: Blue spectrum
  - Used for right-leaning bias indicators (0-50% coverage)

### Accent Colors
- **Yellow**: `#FFD600` - Interest icons
- **Cyan**: `#00B8D4` - Letter icons (H, C)
- **Teal**: `#00BFA5` - Letter icons (E, W)
- **Green**: `#00C853` - Letter icons (M)
- **Purple**: `#AA00FF` - Letter icons (C)
- **Red**: `#FF0000` - Letter icons (I)

### Dark Mode Colors
- `dark-ground-black`: Deep background
- `dark-light`: Card backgrounds in dark mode
- `light-heavy`: Hover states, accent text

### Color Usage Patterns
- **Contrast Ratio**: High contrast between primary text and backgrounds
- **Semantic Color Coding**: Consistent bias color system throughout
- **Responsive Colors**: Light/dark mode support with inverted color schemes
- **Subtle Overlays**: `bg-[rgba(38,38,38,0.3)]` for image overlays

---

## 2. Typography Scale and Weights

### Font Families
- **Primary**: `font-universal-sans` - Sans-serif system font
- **Fallback**: Standard system sans-serif fonts

### Text Scale (Pixel-based)
| Class | Size | Usage |
|-------|-------|-------|
| `text-9px` | 9px | Micro labels, supplemental info |
| `text-12` | 12px | Bias percentages, source counts, metadata |
| `text-14` | 14px | Card metadata, labels |
| `text-16` | 16px | Button text, small headings |
| `text-18` | 18px | Subheadings, descriptions |
| `text-20` | 20px | CTA buttons |
| `text-22` | 22px | Section headers, card titles (mobile) |
| `text-26` | 26px | Section headers (tablet) |
| `text-32` | 32px | Main section titles |
| `text-42` | 42px | Card titles (desktop) |
| `text-48` | 48px | Hero titles (desktop) |

### Font Weights
- **`font-normal`** (400): Body text, descriptions
- **`font-semibold`** (600): Emphasized headings
- **`font-bold`** (700): Section titles, CTAs
- **`font-extrabold`** (800): Headlines, emphasized text

### Line Heights
| Class | Value | Usage |
|-------|-------|-------|
| `leading-6` | 1.5rem | Compact text, metadata |
| `leading-9` | 2.25rem | Larger text, CTAs |
| `leading-10` | 2.5rem | Standard heading |
| `leading-11` | 2.75rem | Larger headings |
| `leading-14` | 3.5rem | Main titles |
| `leading-19` | 4.75rem | Hero titles |
| `leading-tight` | 1.25 | Compact headlines |
| `leading-tightest` | 1.125 | Extra compact text |

### Letter Spacing
- **`tracking-tighter`**: Very tight spacing (0.05em) - Large display text
- **`tracking-tight`**: Tight spacing (0.025em) - Headings

### Typography Best Practices Observed
- **Responsive Scaling**: Text scales appropriately across breakpoints
- **Clear Hierarchy**: Distinct sizes establish visual hierarchy
- **Readable Line Heights**: Generous leading improves readability
- **Consistent Weights**: Limited weight range maintains cohesion

---

## 3. Icon System and Library

### Icon Categories

#### 1. Information Icons
- **Info Icon**: Circle with "i" character
  - SVG path: Circle stroke + fill "i"
  - Size: 16x16px default
  - Usage: Image attribution buttons

#### 2. Blindspot Logo
- **Custom SVG** with complex overlapping circles
  - ViewBox: 0 0 56 37
  - Color: `currentColor` (inherits text color)
  - Usage: Blindspot section headers, labels
  - Sizes: `w-[25px]`, `w-[1.9rem]`

#### 3. Star Rating
- **Star Icon**: 5-point star shape
  - Size: `w-[17px]` for rating displays
  - Usage: Testimonials, reviews
  - Color: `text-focus`

#### 4. Navigation/Action Icons
- **Cross/Cancel Icon**: X shape
  - SVG paths: Two diagonal lines
  - Size: 24x24px (often scaled with `scale-75`)
  - Usage: Close modals, dismiss overlays

#### 5. Location Icons
- **Location Icon**: Standard location pin shape
  - Usage: Location-based features
  - Example class: `location-module__QU6REa__set-location-icon`

#### 6. Letter-based Interest Icons
- Square letter icons for topics/people
  - Colors match accent palette
  - Format: Square background with centered letter
  - Examples: "I" (Israel), "H" (Hungary), "E" (Europe)

### Icon Sizing System
- **Micro**: 16px (info buttons)
- **Small**: 17px (stars), 24px (navigation)
- **Medium**: 25px (blindspot logo small)
- **Large**: 1.9rem (blindspot logo large)
- **Custom**: Scaled with utility classes (e.g., `scale-75`)

### Icon Implementation
- **Format**: Inline SVG within HTML
- **Fill Method**: `fill="currentColor"` for color inheritance
- **Stroke**: `stroke="currentColor"` with `stroke-width`
- **Accessibility**: Includes `<title>` elements for screen readers

---

## 4. Image and Media Treatment

### Image Dimensions
- **Card Images**:
  - Mobile/Tablet: 7.5rem × 5.6rem (aspect-video)
  - Desktop: 40rem × 12.5rem (tablet), 22.5rem (desktop)
  - Aspect ratio: 16:9 (aspect-video)

- **Feature/Hero Images**:
  - Large format: 640px × 440px (typical)
  - Responsive: 95vw (mobile), 50vw (tablet), 640w (desktop)

- **Interest Icons**:
  - Square format: 32px × 32px
  - Shape: `rounded-full` (circular)

- **Attribution Logos**:
  - Source logos: Various sizes
  - Partners: Forbes (95×24px), Mashable (100×18px), USA Today (106×38px)

### Border Radius
| Class | Radius | Usage |
|-------|--------|-------|
| `rounded-[4px]` | 4px | Buttons, small elements |
| `rounded-lg-s` | Small large | Card containers |
| `rounded-[40px]` | 40px | Attribution tooltips |
| `rounded-full` | 50% | Circular icons, avatars |

### Image Effects

#### Blur Effect
- **Purpose**: Background placeholder for image loading
- **Implementation**: `blur-sm scale-110` on background layer
- **Usage**: Dual-layer image system

#### Hover Overlays
- **Default**: `opacity-0`
- **Hover**: `opacity-25` with `transition-opacity duration-200`
- **Color**: `bg-dark-primary`
- **Purpose**: Interactive feedback on image hover

#### Image Attribution
- **Trigger**: Info button (top-right corner of images)
- **Appearance**: `bg-[rgba(38,38,38,0.3)]` circular button
- **Revealed Tooltip**: 
  - Rounded pill shape: `rounded-[40px]`
  - Background: Semi-transparent dark
  - Text: White, 12px
  - Animation: `opacity-0 scale-80` → visible

### Image Loading Strategy
1. **Blur-up**: Blur placeholder loads first
2. **Progressive**: Sharp image overlaid
3. **Responsive**: Multiple srcSet sizes for performance
4. **Fallback**: Placeholder images when content unavailable

### Media Attribution Pattern
- **Icons**: Circular buttons (16px) in top-right corner
- **Tooltips**: Expandable pills showing photographer/agency
- **Animation**: Smooth fade-in (400ms transition)
- **Position**: Absolute, z-index layering

---

## 5. Component Styling Patterns

### Button Styles

#### Primary CTA Buttons
- **Class Pattern**: `bg-dark-primary text-light-primary`
- **Dimensions**: `w-[12.5rem] h-[3.1rem]` (desktop CTAs)
- **Padding**: `px-[0.6rem] py-[8px]`
- **Radius**: `rounded-lg-s`
- **Weight**: `font-bold`
- **Hover**: `hover:text-light-heavy`
- **Active**: `active:text-light-heavy`
- **Disabled**: `disabled:opacity-50 disabled:cursor-not-allowed`

#### Secondary/Outline Buttons
- **Style**: `border border-dark-primary text-dark-primary`
- **Radius**: `rounded-[4px]`
- **Padding**: `px-[0.7rem] py-[0.7rem]`
- **Hover**: `hover:text-light-heavy active:text-light-heavy`

#### Blindspot Tag Buttons
- **Colors**: `bg-ground-new-dark-red text-light-primary` (left bias)
- **Size**: `text-12`
- **Padding**: `px-[4px] py-[5px]`
- **Radius**: `rounded-[4px]`

### Card Components

#### Article Cards
- **Layout**: Flex row (image + content)
- **Gap**: `gap-[1rem]`
- **Image Size**: `w-[7.5rem] h-[5.6rem]`
- **Content Width**: Flexible `w-full`
- **Image Visibility**: `hidden tablet:block` (responsive)

#### Blindspot Cards
- **Structure**: Flex column
- **Image Height**: `h-[13.8rem]`
- **Gap**: `gap-[8px]`
- **Badge**: Flex row with icon + label + percentage

### Input Components

#### Search/Input Fields
- **Border**: `border border-ground-black`
- **Radius**: `rounded-[4px]`
- **Padding**: `py-[0.6rem] text-16`
- **Focus**: `focus:underline focus:underline-offset-1`
- **Placeholder**: Color `placeholder-[var(--gray-200)]`
- **Background**: `bg-light-primary` (light mode)

### Navigation Components

#### Logo Placement
- **Alignment**: `flex justify-between`
- **Close Button**: Top-right corner with cross icon
- **Mobile Adaptation**: Hidden on desktop (`hidden md:flex`)

#### Breadcrumbs/Section Headers
- **Layout**: `flex justify-between flex-wrap`
- **Title**: `text-32 leading-14 font-extrabold`
- **Actions**: `flex gap-[1rem]`
- **Responsiveness**: `tablet:gap-0 tablet:flex-none`

---

## 6. Spacing and Sizing System

### Spacing Scale

#### Gaps (Flex/Grid)
- **Micro**: `gap-[4px]`, `gap-[5px]` - Tightly packed elements
- **Small**: `gap-[6px]`, `gap-[8px]` - Icon+text pairs
- **Medium**: `gap-[0.6rem]`, `gap-[0.7rem]` - Related items
- **Standard**: `gap-[1rem]` - Card content
- **Large**: `gap-[1.3rem]`, `gap-[1.5rem]` - Section spacing
- **XL**: `gap-[2rem]` - Major sections
- **XXL**: `gap-[2.5rem]`, `gap-[3.8rem]` - Container spacing

#### Padding (Inline)
| Class | Value | Usage |
|-------|-------|-------|
| `px-[0.6rem]` | 9.6px | Small buttons |
| `px-[0.7rem]` | 11.2px | Standard buttons |
| `px-[1rem]` | 16px | Medium padding |
| `px-[1.3rem]` | 20.8px | Large buttons |
| `px-[1.9rem]` | 30.4px | Card containers |
| `px-[2.5rem]` | 40px | Large containers |

#### Padding (Block)
| Class | Value | Usage |
|-------|-------|-------|
| `py-[5px]` | 5px | Compact buttons |
| `py-[0.6rem]` | 9.6px | Standard inputs |
| `py-[0.7rem]` | 11.2px | Buttons |
| `py-[0.8rem]` | 12.8px | Larger inputs |
| `py-[1rem]` | 16px | Section padding |
| `py-[1.5rem]` | 24px | Large sections |
| `py-[2.5rem]` | 40px | Hero sections |

#### Margin (Top)
| Class | Value | Usage |
|-------|-------|-------|
| `mt-[0.6rem]` | 9.6px | Small spacing |
| `mt-[0.9rem]` | 14.4px | Medium spacing |
| `mt-[1.3rem]` | 20.8px | Standard spacing |
| `mt-[1.5rem]` | 24px | Large spacing |

### Sizing System

#### Width Classes
- **Full**: `w-full`, `max-w-screen-designmax`
- **Fixed**: `w-[7.5rem]`, `w-[5rem]`, `w-[12.5rem]`
- **Percentage**: `w-[37%]`, `w-[31%]`, `w-[32%]` (bias bars)
- **Max Width**: `max-w-[42.2rem]`, `max-w-[33.75rem]`

#### Height Classes
- **Images**: `h-[5.6rem]`, `h-[8px]`, `h-[11.3rem]`, `h-[13.8rem]`
- **Buttons**: `h-[3.1rem]`, `h-[2.5rem]`
- **Bars**: `h-[1rem]`, `h-[2.06rem]`
- **Components**: `h-[4.4rem]`, `h-[2.5rem]`

---

## 7. Border Radius and Visual Softening

### Radius Scale
| Class | Radius | Visual Effect |
|-------|--------|---------------|
| `rounded-[4px]` | 4px | Subtle softening (buttons, tags) |
| `rounded-lg-s` | ~8px | Standard card radius |
| `rounded-[40px]` | 40px | Pill shape (tooltips) |
| `rounded-full` | 50% | Complete circle (icons) |

### Border Styles

#### Solid Borders
- **Standard**: `border border-ground-black` (1px)
- **Dark**: `border-dark-primary`
- **Light**: `border-light-heavy`
- **Thin**: `border-l`, `border-b`, `border-r` (single edge)

#### Responsive Borders
- Mobile visible: `max-md:hidden`
- Tablet/Desktop: `hidden tablet:block`

### Visual Softening Techniques
1. **Corner Rounding**: Consistent 4px-8px radii for UI elements
2. **Shadows**: `shadow-lg` for elevation
3. **Opacity Layers**: Subtle overlays for depth
4. **Transitions**: Smooth state changes (200-400ms)

---

## 8. Gradients, Patterns, and Textures

### Linear Gradients

#### Bias Bar Gradients
- **Left Bias**: `bg-linear-to-r from-ground-red`
  - Direction: Rightward
  - Purpose: Visualize left-leaning coverage

- **Right Bias**: `bg-linear-to-l from-ground-blue`
  - Direction: Leftward
  - Purpose: Visualize right-leaning coverage

#### Gradient Usage
- **Format**: `bg-linear-to-{direction} from-{color}`
- **Implementation**: Inline styles with `transform` for animation
- **Animation**: Bars slide in with `transform: translateY()` transitions

### Textures

#### Background Patterns
- **Newspaper Watermark**: Hero section background image
  - File: `about_page_newspaper_watermark.819d2aca.png`
  - Style: `object-cover`, full coverage
  - Purpose: Thematic background

#### Blur Effects
- **Image Background**: `blur-sm scale-110`
  - Creates depth between layers
  - Improves perceived performance

### No Complex Textures
- Design uses **flat, clean aesthetic**
- Relies on **color, typography, and spacing** rather than textures
- Strategic use of **gradients** for data visualization only

---

## 9. Visual Hierarchy Implementation

### Heading Hierarchy

#### Level 1: Hero Title
- **Class**: `text-32 tablet:text-42 desktop:text-48`
- **Weight**: `font-bold`
- **Leading**: `leading-tightest`
- **Spacing**: `mt-[1.3rem] desktop:mt-0`
- **Example**: "See every side of every news story."

#### Level 2: Section Titles
- **Class**: `text-32 leading-14 font-extrabold`
- **Usage**: "Israel-Gaza News", "European Politics News", "Latest Stories"

#### Level 3: Subsection Headers
- **Class**: `text-22 leading-10 font-bold`
- **Usage**: "Latest Israel-Gaza News", "Blindspots"

#### Level 4: Card Titles
- **Class**: `text-22 tablet:text-32 desktop:text-42`
- **Weight**: `font-extrabold`
- **Hover**: `group-hover:underline`
- **Clamp**: `line-clamp-3` (limit to 3 lines)

#### Level 5: Metadata Labels
- **Class**: `text-12` - `text-14`
- **Usage**: Source names, locations, bias percentages

### Content Hierarchy Techniques

#### Size Contrast
- 48px (hero) → 32px (sections) → 22px (cards) → 14px (metadata)

#### Weight Contrast
- 800 (headlines) → 700 (titles) → 600 (subheads) → 400 (body)

#### Color Contrast
- Primary text → Muted text → Disabled text
- Active states → Hover states → Disabled states

#### Spatial Hierarchy
- Generous whitespace around top-level elements
- Tighter spacing within content groups
- Consistent section separation

### Information Architecture Visuals

#### Bias Visualization
- **Prominent**: 3-bar system (Left/Center/Right)
- **Placement**: Below headlines, above descriptions
- **Color-coded**: Red (left) → Gray (center) → Blue (right)
- **Interactive**: Hoverable segments

#### Source Counting
- **Format**: "X sources" or "X / Y sources"
- **Position**: Right side of bias bars
- **Style**: `text-12`

#### Blindspot Badges
- **Icon**: Blindspot logo
- **Label**: "Blindspot:"
- **Percentage**: Colored tag (e.g., "0% Left")
- **Placement**: Top of card, before title

---

## 10. Brand Identity Elements

### Logo and Branding

#### Blindspot Logo
- **Design**: Overlapping eye/blindfold motif
- **Format**: Custom SVG
- **Color**: Inherits from text color
- **Usage**: Section headers, feature identification
- **Sizes**: Multiple responsive variants

#### Partner Logos
- **Placement**: Footer/credibility section
- **Treatment**: `filter:brightness(0%)` (grayscale)
- **Hover**: No interaction (static presentation)
- **Included**: Forbes, Mashable, USA Today, Wall Street Journal, CTV

### Brand Color System
- **Primary**: Black/White high-contrast
- **Accent**: Systematic bias colors (red/gray/blue)
- **Support**: Grayscale neutral palette
- **Dark Mode**: Complete inversion available

### Typography Identity
- **Font**: `font-universal-sans` (system sans)
- **Voice**: Clean, authoritative, accessible
- **Hierarchy**: Bold headlines, legible body
- **Distinctiveness**: Tight letter spacing on large type

### Visual DNA
1. **Data-First**: Bias bars, source counts, percentages prominent
2. **Clean & Minimal**: Flat design, minimal decoration
3. **High Contrast**: Accessibility-focused color ratios
4. **Systematic**: Consistent patterns across components
5. **Responsive**: Graceful adaptation across devices

### Brand Personality
- **Authoritative**: Strong typography, data-driven presentation
- **Objective**: Neutral color scheme for center bias
- **Accessible**: Clear hierarchy, readable text
- **Modern**: Smooth transitions, responsive design

---

## Technical Implementation Notes

### Framework
- **CSS Architecture**: Tailwind-inspired utility classes
- **Custom Properties**: CSS variables for semantic colors
- **Dark Mode**: `dark:` prefix classes
- **Responsive**: `mobile:`, `tablet:`, `desktop:` prefixes

### Performance Optimizations
- **Image Loading**: Progressive blur-up technique
- **Responsive Images**: Multiple srcSet sizes
- **Animations**: GPU-accelerated transforms
- **Lazy Loading**: `loading="lazy"` on images

### Accessibility
- **Semantic HTML**: Proper heading hierarchy
- **Icon Labels**: `<title>` elements for screen readers
- **Focus States**: `focus:underline` on inputs
- **Color Contrast**: High contrast ratios maintained

---

## Recommendations

### Strengths
✅ Consistent spacing and sizing system  
✅ Clear visual hierarchy with typography scale  
✅ Effective bias visualization through color coding  
✅ Responsive design across all breakpoints  
✅ Accessible color contrasts  

### Opportunities
1. **Icon Library**: Consider consolidating into an icon font or SVG sprite system
2. **Color Tokens**: Formalize semantic color variables in design system
3. **Animation System**: Standardize transition durations and easing functions
4. **Component Documentation**: Create visual component library for consistency

---

**Report Generated:** February 15, 2026  
**Audited By:** Subagent (Ground News Visual Audit Specialist)  
**Scope:** Homepage visual analysis via HTML/CSS extraction
