---
name: Deep Space Intelligence
colors:
  surface: '#0b1326'
  surface-dim: '#0b1326'
  surface-bright: '#31394d'
  surface-container-lowest: '#060e20'
  surface-container-low: '#131b2e'
  surface-container: '#171f33'
  surface-container-high: '#222a3d'
  surface-container-highest: '#2d3449'
  on-surface: '#dae2fd'
  on-surface-variant: '#cbc3d7'
  inverse-surface: '#dae2fd'
  inverse-on-surface: '#283044'
  outline: '#958ea0'
  outline-variant: '#494454'
  surface-tint: '#d0bcff'
  primary: '#d0bcff'
  on-primary: '#3c0091'
  primary-container: '#a078ff'
  on-primary-container: '#340080'
  inverse-primary: '#6d3bd7'
  secondary: '#4edea3'
  on-secondary: '#003824'
  secondary-container: '#00a572'
  on-secondary-container: '#00311f'
  tertiary: '#adc6ff'
  on-tertiary: '#002e6a'
  tertiary-container: '#4d8eff'
  on-tertiary-container: '#00285d'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#e9ddff'
  primary-fixed-dim: '#d0bcff'
  on-primary-fixed: '#23005c'
  on-primary-fixed-variant: '#5516be'
  secondary-fixed: '#6ffbbe'
  secondary-fixed-dim: '#4edea3'
  on-secondary-fixed: '#002113'
  on-secondary-fixed-variant: '#005236'
  tertiary-fixed: '#d8e2ff'
  tertiary-fixed-dim: '#adc6ff'
  on-tertiary-fixed: '#001a42'
  on-tertiary-fixed-variant: '#004395'
  background: '#0b1326'
  on-background: '#dae2fd'
  surface-variant: '#2d3449'
typography:
  display-lg:
    fontFamily: Hanken Grotesk
    fontSize: 48px
    fontWeight: '700'
    lineHeight: 56px
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Hanken Grotesk
    fontSize: 32px
    fontWeight: '600'
    lineHeight: 40px
  headline-md:
    fontFamily: Hanken Grotesk
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
  body-lg:
    fontFamily: Inter
    fontSize: 18px
    fontWeight: '400'
    lineHeight: 28px
  body-md:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  body-sm:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
  label-md:
    fontFamily: JetBrains Mono
    fontSize: 12px
    fontWeight: '500'
    lineHeight: 16px
  label-sm:
    fontFamily: JetBrains Mono
    fontSize: 10px
    fontWeight: '500'
    lineHeight: 14px
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  base: 4px
  xs: 8px
  sm: 16px
  md: 24px
  lg: 32px
  xl: 48px
  gutter: 20px
  margin-mobile: 16px
  margin-desktop: 32px
---

## Brand & Style

The design system is engineered for the high-velocity world of social media management. It balances a professional, data-centric atmosphere with the creative energy required for content strategy. The personality is **intelligent, sophisticated, and dependable**, designed to reduce cognitive load during complex scheduling tasks.

The visual style is a refined **Corporate Modern** aesthetic with **Glassmorphic** accents. It utilizes a deep charcoal foundation to make vibrant content previews and status indicators pop. The "AI" aspect is reflected through subtle glows, precise linework, and a futuristic but grounded color palette. The goal is to make the user feel in total control of a powerful, automated engine.

## Colors

This design system uses a high-depth dark theme. The primary **Electric Purple** (#8B5CF6) is reserved for primary actions, branding, and active states. 

- **Primary (Purple):** Used for CTA buttons, active sidebar states, and AI-driven features.
- **Secondary (Green):** Specifically used for positive growth metrics and "Connected" statuses.
- **Tertiary (Blue):** Used for informational accents and secondary data points.
- **Neutral/Surface:** A range of deep charcoals. The background is almost black, while surface cards use a slightly lighter grey-blue to create layered depth.
- **Status Indicators:** Use high-vibrancy tokens (Red for errors/disconnected, Amber for pending) to ensure they are glanceable against the dark background.

## Typography

The typography strategy emphasizes clarity and technical precision. **Hanken Grotesk** provides a sharp, modern feel for headlines, while **Inter** ensures maximum readability for body content and data tables. 

**JetBrains Mono** is strategically used for labels, timestamps, and metadata to reinforce the data-driven "AI" nature of the platform. All typography should maintain a high contrast ratio against the dark background, primarily using off-white (#F8FAFC) for primary text and muted grey (#94A3B8) for secondary information.

## Layout & Spacing

The design system utilizes a **12-column fluid grid** for the main dashboard area, with a fixed-width left sidebar (260px). 

- **Grid System:** 20px gutters facilitate breathing room between dense data cards.
- **Padding:** Internal card padding should be a consistent 24px (md) to maintain a premium feel.
- **Reflow:** On mobile, the sidebar collapses into a bottom navigation bar or a hamburger menu, and the 12-column grid stacks into a single column.
- **Rhythm:** All spacing must be multiples of 4px to ensure a strict geometric alignment.

## Elevation & Depth

Visual hierarchy is achieved through **Tonal Layering** and **Subtle Outlines** rather than heavy shadows.

1.  **Level 0 (Base):** The darkest color (#0B0E14), used for the application background.
2.  **Level 1 (Surface):** The primary card color (#161B22). These feature a 1px solid border (#30363D) to define edges.
3.  **Level 2 (Hover/Active):** A slightly lighter surface (#1C2128) with a subtle outer glow using the primary purple color at 10% opacity.
4.  **Glassmorphism:** For overlays, modals, and tooltips, use a backdrop blur (12px) with a semi-transparent background (#161B22CC) to maintain context.

## Shapes

The shape language is **Rounded**, conveying modern software friendliness without being overly "bubbly." 

- Standard components (buttons, inputs) use a **0.5rem (8px)** radius.
- Feature cards and containers use **1rem (16px)** for a more structured, distinct appearance.
- Icons are housed in soft-square containers or circular badges depending on their priority level.

## Components

### Buttons
- **Primary:** Solid purple background (#8B5CF6) with white text. High-contrast hover state with a subtle glow.
- **Secondary:** Ghost style with a purple border and transparent background.
- **Ghost/Tertiary:** No border, muted text, becomes solid charcoal on hover.

### Cards
- Standard cards must have a 1px border (#30363D). 
- Header areas within cards should use a slightly darker sub-header background to separate controls from content.

### Inputs & Selects
- Backgrounds should be darker than the card surface to create an "inset" feel. 
- Active focus states must use a 2px purple ring.

### Status Chips
- Small, pill-shaped badges with 10% opacity background of the status color (Green/Red/Blue) and a 100% opacity text color for readability.

### Sidebar
- Use a vertical navigation list with icons. The active item should feature a vertical purple bar on the left edge and a subtle gradient background.

### Data Visualizations
- Charts should use the Primary, Secondary, and Tertiary colors for data lines, with grid lines kept at extremely low contrast (#30363D).