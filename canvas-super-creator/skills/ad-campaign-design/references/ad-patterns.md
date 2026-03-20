# Ad Campaign Design — CSS Recipes by IAB Size

Complete CSS patterns for each IAB standard ad size, plus CTA styles, campaign visual system, and A/B variant generation.

---

## Leaderboard (728 x 90)

Horizontal flow: logo left, headline center, CTA right.

```css
html, body { width: 728px; height: 90px; }

body {
    --bg: #0C0C0F;
    --fg: #E8ECF0;
    --accent: #4A90D9;
    --cta-bg: #E63B2E;
    --cta-fg: #FFFFFF;
    --muted: #1A1A24;
    position: relative;
    background: var(--bg);
    border: 1px solid rgba(0, 0, 0, 0.1);
}

.ad-layout {
    position: absolute;
    top: 0; left: 0; width: 100%; height: 100%;
    display: flex;
    align-items: center;
    padding: 0 20px;
    gap: 20px;
    z-index: 3;
}
.logo {
    flex-shrink: 0;
    font-family: 'BricolageGrotesque', sans-serif;
    font-size: 18px;
    font-weight: 700;
    color: var(--accent);
    letter-spacing: 0.02em;
}
.headline {
    flex: 1;
    font-family: 'BricolageGrotesque', sans-serif;
    font-size: 24px;
    font-weight: 700;
    color: var(--fg);
    line-height: 1.1;
    letter-spacing: -0.01em;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}
.cta-btn {
    flex-shrink: 0;
    font-family: 'WorkSans', sans-serif;
    font-size: 13px;
    font-weight: 600;
    color: var(--cta-fg);
    background: var(--cta-bg);
    padding: 8px 24px;
    border-radius: 4px;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    white-space: nowrap;
}
```

---

## Medium Rectangle (300 x 250)

Vertical stack: visual top, headline middle, CTA bottom. The campaign master.

```css
html, body { width: 300px; height: 250px; }

body {
    --bg: #0C0C0F;
    --fg: #E8ECF0;
    --accent: #4A90D9;
    --cta-bg: #E63B2E;
    --cta-fg: #FFFFFF;
    --muted: #1A1A24;
    position: relative;
    background: var(--bg);
    border: 1px solid rgba(0, 0, 0, 0.1);
}

/* Visual zone — top 45% */
.visual-zone {
    position: absolute;
    top: 0; left: 0; width: 100%; height: 45%;
    background: var(--muted);
    overflow: hidden;
    z-index: 2;
}
/* Gradient overlay on visual */
.visual-overlay {
    position: absolute;
    bottom: 0; left: 0; width: 100%;
    height: 50%;
    background: linear-gradient(0deg, var(--bg) 0%, transparent 100%);
    z-index: 3;
}

/* Content zone */
.content {
    position: absolute;
    top: 42%; left: 20px; right: 20px; bottom: 20px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    gap: 10px;
    z-index: 4;
}
.content h2 {
    font-family: 'BricolageGrotesque', sans-serif;
    font-size: 28px;
    font-weight: 700;
    color: var(--fg);
    line-height: 1.1;
    letter-spacing: -0.01em;
}
.content p {
    font-family: 'Outfit', sans-serif;
    font-size: 13px;
    color: var(--fg);
    opacity: 0.6;
    line-height: 1.4;
}
.content .cta-btn {
    display: inline-block;
    width: fit-content;
    font-family: 'WorkSans', sans-serif;
    font-size: 12px;
    font-weight: 600;
    color: var(--cta-fg);
    background: var(--cta-bg);
    padding: 10px 28px;
    border-radius: 4px;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    margin-top: 4px;
}

/* Brand mark — bottom right */
.brand-mark {
    position: absolute;
    bottom: 12px; right: 16px;
    font-family: 'Outfit', sans-serif;
    font-size: 10px;
    color: var(--fg);
    opacity: 0.3;
    letter-spacing: 0.05em;
    z-index: 4;
}
```

---

## Wide Skyscraper (160 x 600)

Vertical scroll: logo top, visual middle, headline below, CTA bottom.

```css
html, body { width: 160px; height: 600px; }

body {
    --bg: #0C0C0F;
    --fg: #E8ECF0;
    --accent: #4A90D9;
    --cta-bg: #E63B2E;
    --cta-fg: #FFFFFF;
    --muted: #1A1A24;
    position: relative;
    background: var(--bg);
    border: 1px solid rgba(0, 0, 0, 0.1);
}

/* Logo — top */
.logo {
    position: absolute;
    top: 16px; left: 16px;
    font-family: 'BricolageGrotesque', sans-serif;
    font-size: 14px;
    font-weight: 700;
    color: var(--accent);
    z-index: 4;
}

/* Visual zone — middle */
.visual-zone {
    position: absolute;
    top: 60px; left: 0; width: 100%; height: 220px;
    background: var(--muted);
    overflow: hidden;
    z-index: 2;
}

/* Headline — below visual */
.headline {
    position: absolute;
    top: 300px; left: 16px; right: 16px;
    z-index: 4;
}
.headline h2 {
    font-family: 'BricolageGrotesque', sans-serif;
    font-size: 22px;
    font-weight: 700;
    color: var(--fg);
    line-height: 1.15;
    letter-spacing: -0.01em;
}
.headline p {
    font-family: 'Outfit', sans-serif;
    font-size: 12px;
    color: var(--fg);
    opacity: 0.6;
    margin-top: 10px;
    line-height: 1.4;
}

/* CTA — bottom */
.cta-zone {
    position: absolute;
    bottom: 40px; left: 16px; right: 16px;
    z-index: 4;
}
.cta-btn {
    display: block;
    width: 100%;
    font-family: 'WorkSans', sans-serif;
    font-size: 12px;
    font-weight: 600;
    color: var(--cta-fg);
    background: var(--cta-bg);
    padding: 10px 0;
    border-radius: 4px;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    text-align: center;
}

/* Brand mark */
.brand-mark {
    position: absolute;
    bottom: 14px; left: 50%;
    transform: translateX(-50%);
    font-family: 'Outfit', sans-serif;
    font-size: 9px;
    color: var(--fg);
    opacity: 0.25;
    z-index: 4;
}
```

---

## Billboard (970 x 250)

Hero visual left, copy + CTA right. Premium wide format.

```css
html, body { width: 970px; height: 250px; }

body {
    --bg: #0C0C0F;
    --fg: #E8ECF0;
    --accent: #4A90D9;
    --cta-bg: #E63B2E;
    --cta-fg: #FFFFFF;
    --muted: #1A1A24;
    position: relative;
    background: var(--bg);
    border: 1px solid rgba(0, 0, 0, 0.1);
}

/* Visual — left 45% */
.visual-zone {
    position: absolute;
    top: 0; left: 0; width: 45%; height: 100%;
    background: var(--muted);
    overflow: hidden;
    z-index: 2;
}
.visual-fade {
    position: absolute;
    top: 0; right: 0; width: 80px; height: 100%;
    background: linear-gradient(90deg, transparent 0%, var(--bg) 100%);
    z-index: 3;
}

/* Content — right 55% */
.content {
    position: absolute;
    top: 0; right: 0; width: 55%; height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: center;
    padding: 30px 40px 30px 20px;
    z-index: 4;
}
.content .overline {
    font-family: 'WorkSans', sans-serif;
    font-size: 11px;
    font-weight: 600;
    color: var(--accent);
    text-transform: uppercase;
    letter-spacing: 0.12em;
    margin-bottom: 8px;
}
.content h2 {
    font-family: 'BricolageGrotesque', sans-serif;
    font-size: 36px;
    font-weight: 700;
    color: var(--fg);
    line-height: 1.1;
    letter-spacing: -0.01em;
}
.content p {
    font-family: 'Outfit', sans-serif;
    font-size: 14px;
    color: var(--fg);
    opacity: 0.6;
    margin-top: 8px;
    line-height: 1.4;
}
.content .cta-btn {
    display: inline-block;
    width: fit-content;
    font-family: 'WorkSans', sans-serif;
    font-size: 14px;
    font-weight: 600;
    color: var(--cta-fg);
    background: var(--cta-bg);
    padding: 12px 32px;
    border-radius: 4px;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    margin-top: 16px;
}

/* Brand mark */
.brand-mark {
    position: absolute;
    bottom: 16px; right: 20px;
    font-family: 'Outfit', sans-serif;
    font-size: 10px;
    color: var(--fg);
    opacity: 0.25;
    z-index: 4;
}
```

---

## Large Rectangle (336 x 280)

Similar to Medium Rectangle but slightly larger. More breathing room.

```css
html, body { width: 336px; height: 280px; }

body {
    --bg: #0C0C0F;
    --fg: #E8ECF0;
    --accent: #4A90D9;
    --cta-bg: #E63B2E;
    --cta-fg: #FFFFFF;
    --muted: #1A1A24;
    position: relative;
    background: var(--bg);
    border: 1px solid rgba(0, 0, 0, 0.1);
}

.visual-zone {
    position: absolute;
    top: 0; left: 0; width: 100%; height: 48%;
    background: var(--muted);
    z-index: 2;
}
.content {
    position: absolute;
    top: 45%; left: 24px; right: 24px; bottom: 24px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    gap: 10px;
    z-index: 4;
}
.content h2 {
    font-family: 'BricolageGrotesque', sans-serif;
    font-size: 30px;
    font-weight: 700;
    color: var(--fg);
    line-height: 1.1;
}
.content p {
    font-family: 'Outfit', sans-serif;
    font-size: 14px;
    color: var(--fg);
    opacity: 0.6;
    line-height: 1.4;
}
.content .cta-btn {
    display: inline-block;
    width: fit-content;
    font-family: 'WorkSans', sans-serif;
    font-size: 13px;
    font-weight: 600;
    color: var(--cta-fg);
    background: var(--cta-bg);
    padding: 10px 28px;
    border-radius: 4px;
    text-transform: uppercase;
    letter-spacing: 0.06em;
}
.brand-mark {
    position: absolute;
    bottom: 12px; right: 16px;
    font-family: 'Outfit', sans-serif;
    font-size: 10px;
    color: var(--fg);
    opacity: 0.25;
    z-index: 4;
}
```

---

## Half Page (300 x 600)

Expanded vertical format with generous space for visual impact.

```css
html, body { width: 300px; height: 600px; }

body {
    --bg: #0C0C0F;
    --fg: #E8ECF0;
    --accent: #4A90D9;
    --cta-bg: #E63B2E;
    --cta-fg: #FFFFFF;
    --muted: #1A1A24;
    position: relative;
    background: var(--bg);
    border: 1px solid rgba(0, 0, 0, 0.1);
}

/* Logo — top */
.logo {
    position: absolute;
    top: 20px; left: 20px;
    font-family: 'BricolageGrotesque', sans-serif;
    font-size: 16px;
    font-weight: 700;
    color: var(--accent);
    z-index: 4;
}

/* Visual — large center area */
.visual-zone {
    position: absolute;
    top: 60px; left: 0; width: 100%; height: 250px;
    background: var(--muted);
    z-index: 2;
}

/* Content — below visual */
.content {
    position: absolute;
    top: 330px; left: 20px; right: 20px;
    z-index: 4;
}
.content h2 {
    font-family: 'BricolageGrotesque', sans-serif;
    font-size: 32px;
    font-weight: 700;
    color: var(--fg);
    line-height: 1.15;
}
.content p {
    font-family: 'Outfit', sans-serif;
    font-size: 14px;
    color: var(--fg);
    opacity: 0.6;
    margin-top: 12px;
    line-height: 1.5;
}
.content .cta-btn {
    display: inline-block;
    width: fit-content;
    font-family: 'WorkSans', sans-serif;
    font-size: 14px;
    font-weight: 600;
    color: var(--cta-fg);
    background: var(--cta-bg);
    padding: 12px 32px;
    border-radius: 4px;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    margin-top: 20px;
}

.brand-mark {
    position: absolute;
    bottom: 16px; right: 16px;
    font-family: 'Outfit', sans-serif;
    font-size: 10px;
    color: var(--fg);
    opacity: 0.25;
    z-index: 4;
}
```

---

## Mobile Leaderboard (320 x 50)

Ultra-compressed: headline left, CTA right. No visual.

```css
html, body { width: 320px; height: 50px; }

body {
    --bg: #0C0C0F;
    --fg: #E8ECF0;
    --cta-bg: #E63B2E;
    --cta-fg: #FFFFFF;
    position: relative;
    background: var(--bg);
    border: 1px solid rgba(0, 0, 0, 0.1);
}

.ad-layout {
    position: absolute;
    top: 0; left: 0; width: 100%; height: 100%;
    display: flex;
    align-items: center;
    padding: 0 12px;
    gap: 12px;
    z-index: 3;
}
.headline {
    flex: 1;
    font-family: 'BricolageGrotesque', sans-serif;
    font-size: 15px;
    font-weight: 700;
    color: var(--fg);
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}
.cta-btn {
    flex-shrink: 0;
    font-family: 'WorkSans', sans-serif;
    font-size: 10px;
    font-weight: 600;
    color: var(--cta-fg);
    background: var(--cta-bg);
    padding: 6px 16px;
    border-radius: 3px;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    white-space: nowrap;
}
```

---

## Mobile Interstitial (320 x 480)

Full-screen mobile — the most design room in mobile formats.

```css
html, body { width: 320px; height: 480px; }

body {
    --bg: #0C0C0F;
    --fg: #E8ECF0;
    --accent: #4A90D9;
    --cta-bg: #E63B2E;
    --cta-fg: #FFFFFF;
    --muted: #1A1A24;
    position: relative;
    background: var(--bg);
    border: 1px solid rgba(0, 0, 0, 0.1);
}

/* Visual — top half */
.visual-zone {
    position: absolute;
    top: 0; left: 0; width: 100%; height: 50%;
    background: var(--muted);
    z-index: 2;
}
.visual-overlay {
    position: absolute;
    bottom: 0; left: 0; width: 100%; height: 40%;
    background: linear-gradient(0deg, var(--bg) 0%, transparent 100%);
    z-index: 3;
}

/* Content — centered lower half */
.content {
    position: absolute;
    top: 46%; left: 24px; right: 24px; bottom: 24px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
    gap: 12px;
    z-index: 4;
}
.content .logo {
    font-family: 'BricolageGrotesque', sans-serif;
    font-size: 20px;
    font-weight: 700;
    color: var(--accent);
    margin-bottom: 4px;
}
.content h2 {
    font-family: 'BricolageGrotesque', sans-serif;
    font-size: 32px;
    font-weight: 700;
    color: var(--fg);
    line-height: 1.1;
}
.content p {
    font-family: 'Outfit', sans-serif;
    font-size: 14px;
    color: var(--fg);
    opacity: 0.6;
    line-height: 1.4;
}
.content .cta-btn {
    font-family: 'WorkSans', sans-serif;
    font-size: 15px;
    font-weight: 600;
    color: var(--cta-fg);
    background: var(--cta-bg);
    padding: 14px 36px;
    border-radius: 6px;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    margin-top: 8px;
}
```

---

## Large Mobile (320 x 100)

Compact mobile: logo left, headline center, CTA right.

```css
html, body { width: 320px; height: 100px; }

body {
    --bg: #0C0C0F;
    --fg: #E8ECF0;
    --accent: #4A90D9;
    --cta-bg: #E63B2E;
    --cta-fg: #FFFFFF;
    position: relative;
    background: var(--bg);
    border: 1px solid rgba(0, 0, 0, 0.1);
}

.ad-layout {
    position: absolute;
    top: 0; left: 0; width: 100%; height: 100%;
    display: flex;
    align-items: center;
    padding: 12px 16px;
    gap: 14px;
    z-index: 3;
}
.logo {
    flex-shrink: 0;
    font-family: 'BricolageGrotesque', sans-serif;
    font-size: 13px;
    font-weight: 700;
    color: var(--accent);
}
.text-block {
    flex: 1;
}
.text-block h3 {
    font-family: 'BricolageGrotesque', sans-serif;
    font-size: 18px;
    font-weight: 700;
    color: var(--fg);
    line-height: 1.15;
}
.text-block p {
    font-family: 'Outfit', sans-serif;
    font-size: 11px;
    color: var(--fg);
    opacity: 0.5;
    margin-top: 2px;
}
.cta-btn {
    flex-shrink: 0;
    font-family: 'WorkSans', sans-serif;
    font-size: 11px;
    font-weight: 600;
    color: var(--cta-fg);
    background: var(--cta-bg);
    padding: 8px 18px;
    border-radius: 4px;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    white-space: nowrap;
}
```

---

## CTA Button Styles

### 1. Solid CTA

```css
.cta-solid {
    font-family: 'WorkSans', sans-serif;
    font-weight: 600;
    color: var(--cta-fg);
    background: var(--cta-bg);
    padding: 12px 32px;
    border-radius: 4px;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    border: none;
}
```

### 2. Outline CTA

```css
.cta-outline {
    font-family: 'WorkSans', sans-serif;
    font-weight: 600;
    color: var(--cta-bg);
    background: transparent;
    padding: 10px 30px;
    border: 2px solid var(--cta-bg);
    border-radius: 4px;
    text-transform: uppercase;
    letter-spacing: 0.06em;
}
```

### 3. Rounded Pill CTA

```css
.cta-pill {
    font-family: 'WorkSans', sans-serif;
    font-weight: 600;
    color: var(--cta-fg);
    background: var(--cta-bg);
    padding: 12px 36px;
    border-radius: 100px;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    border: none;
}
```

### 4. Arrow-Right CTA

```css
.cta-arrow {
    font-family: 'WorkSans', sans-serif;
    font-weight: 600;
    color: var(--cta-fg);
    background: var(--cta-bg);
    padding: 12px 40px 12px 32px;
    border-radius: 4px;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    border: none;
    position: relative;
}
.cta-arrow::after {
    content: '\2192';
    margin-left: 8px;
    font-size: 1.1em;
}
```

### 5. Gradient CTA

```css
.cta-gradient {
    font-family: 'WorkSans', sans-serif;
    font-weight: 600;
    color: var(--cta-fg);
    background: linear-gradient(135deg, var(--cta-bg) 0%, var(--accent) 100%);
    padding: 12px 32px;
    border-radius: 6px;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    border: none;
}
```

---

## Campaign Visual System Template

Shared CSS custom properties that define a campaign's visual identity across all sizes:

```css
/* campaign-system.css — import into every ad HTML */
:root {
    /* Brand Colors */
    --brand-bg: #0C0C0F;
    --brand-fg: #E8ECF0;
    --brand-accent: #4A90D9;
    --brand-muted: #1A1A24;

    /* CTA Colors */
    --cta-bg: #E63B2E;
    --cta-fg: #FFFFFF;

    /* Typography */
    --font-heading: 'BricolageGrotesque', sans-serif;
    --font-body: 'Outfit', sans-serif;
    --font-cta: 'WorkSans', sans-serif;
    --font-mono: 'GeistMono', monospace;

    /* CTA Style */
    --cta-radius: 4px;
    --cta-weight: 600;
    --cta-transform: uppercase;
    --cta-spacing: 0.06em;

    /* Brand Mark */
    --brand-mark-size: 10px;
    --brand-mark-opacity: 0.25;
}

/* Universal ad border */
body {
    border: 1px solid rgba(0, 0, 0, 0.1);
}

/* Reusable CTA component */
.cta-btn {
    font-family: var(--font-cta);
    font-weight: var(--cta-weight);
    color: var(--cta-fg);
    background: var(--cta-bg);
    border-radius: var(--cta-radius);
    text-transform: var(--cta-transform);
    letter-spacing: var(--cta-spacing);
    border: none;
    cursor: pointer;
}

/* Reusable brand mark */
.brand-mark {
    font-family: var(--font-body);
    font-size: var(--brand-mark-size);
    color: var(--brand-fg);
    opacity: var(--brand-mark-opacity);
}
```

---

## A/B Variant Generation Guide

### Color Variant

Change only `--cta-bg` to test CTA button color impact:

```css
/* Variant A (control) */
:root { --cta-bg: #E63B2E; } /* Red */

/* Variant B */
:root { --cta-bg: #4A90D9; } /* Blue */

/* Variant C */
:root { --cta-bg: #2ECC71; } /* Green */
```

### CTA Text Variant

Same design, swap the CTA label only:

```
Variant A: "Shop Now"
Variant B: "Get 20% Off"
Variant C: "Free Shipping"
```

### Layout Variant (300x250 example)

```css
/* Variant A: Visual top, text bottom (default) */
.visual-zone { top: 0; height: 45%; }
.content { top: 42%; }

/* Variant B: Text top, visual bottom */
.content { top: 16px; bottom: auto; }
.visual-zone { top: auto; bottom: 0; height: 45%; }
```

### Image Variant

Same CSS layout, swap only the image source or background in `.visual-zone`. All typography, CTA, and layout remain identical.
