---
name: magazine-design
description: Magazine covers, editorial spreads, and multi-column layouts. Use when user asks for a magazine cover, editorial layout, spread design, or Swiss/International style grid design.
license: MIT
metadata:
  author: canvas-super-creator
  version: 4.0.0
---

# Magazine Design — Editorial Layouts and Cover Design

Create magazine covers, editorial spreads, and multi-column layouts with sophisticated grid systems, typographic hierarchy, and editorial craft. Magazine design is where typography, photography, and grid intersect at the highest level.

---

## Format Quick Reference

| Format | Dimensions (px) | DPI | Typography Scale |
|---|---|---|---|
| US Cover | 2550 x 3300 | 300 | Masthead: 120pt, Cover line: 72pt, Sub: 36pt |
| A4 Cover | 2480 x 3508 | 300 | Masthead: 110pt, Cover line: 68pt, Sub: 34pt |
| Double Spread | 5100 x 3300 | 300 | Headline: 96pt, Sub: 48pt, Body: 24pt |
| Single Page | 2550 x 3300 | 300 | Headline: 72pt, Sub: 36pt, Body: 22pt |

**Full details:** Read `./canvas-super-creator/references/formats.md` for safe zones and bleed areas.

---

## Workflow

1. **Read references:**
   - `./canvas-super-creator/references/formats.md` — dimensions, safe zones, bleed
   - `./canvas-super-creator/references/color-palettes.md` — palette selection
   - `./canvas-super-creator/references/typography-pairings.md` — font pairing
   - `./canvas-super-creator/references/composition-guide.md` — layout technique
   - `./canvas-super-creator/references/anti-slop-checklist.md` — quality gates
   - `./html-design/references/css-techniques.md` — CSS technique catalog
   - `./magazine-design/references/magazine-patterns.md` — magazine-specific recipes

2. **Output specification** with format, palette, typography, grid system, editorial tone

3. **Create design philosophy** — magazines demand a cohesive editorial voice and visual identity

4. **Design with html-design patterns** — follow the 4-phase process

5. **Render via render-engine** pipeline

---

## Magazine Cover Anatomy

Every magazine cover follows a spatial hierarchy that has been refined over a century of newsstand competition:

```
+----------------------------------+
| DATE/PRICE        ISSUE/SEASON   |  <- Top corners: metadata
+----------------------------------+
|                                  |
|         M A S T H E A D          |  <- Top 15%: publication name
|                                  |
+----------------------------------+
|  Cover lines  |                  |
|  stacked      |    MAIN VISUAL   |  <- Center: hero image/visual
|  left 30%     |    (center)      |
|               |                  |
|  Secondary    |                  |
|  cover lines  |                  |
+----------------------------------+
|                                  |
|  Bottom cover line or tagline    |
|                    BARCODE ZONE  |  <- Bottom-right: UPC/barcode
+----------------------------------+
```

### Zone Rules

- **Masthead zone (top 15%):** The publication name. Must be recognizable even when partially obscured by the main visual. Bold, consistent issue-to-issue.
- **Cover lines (left 30%):** 3-5 article teasers. Stacked vertically. Largest = lead story. Others decrease in size.
- **Main visual (center 60%):** The hero photograph or illustration. This sells the issue.
- **Barcode zone (bottom-right):** 2" x 2" reserved. Never place key design elements here.
- **Date/price (top corners):** Small, functional. Issue number, date, price.

---

## Editorial Spread Principles

### Modular Grid Systems

Magazine interiors live on grids. The grid is not optional — it is the skeleton:

- **6-column grid:** Standard for text-heavy editorial. 3 columns for body text, 3 for images/sidebars.
- **8-column grid:** For complex layouts with data, sidebars, and pull quotes. Bloomberg Businessweek style.
- **12-column grid:** Maximum flexibility. Used for responsive-feeling layouts with varied column spans.
- **Baseline grid:** All text aligns to a shared baseline rhythm (typically 12-14px increments). This creates vertical harmony.

### Grid Math

```
Page width: 2550px
Margins: 120px each side
Available: 2310px
6-col grid: 2310px / 6 = 385px columns
Gutter: 30px between columns
Actual column: 360px with 25px gutters
```

### Spread Elements

- **Pull quotes:** Large, decorative quotes that break up body text and draw readers into the article
- **Drop caps:** Oversized first letters that signal the start of an article section
- **Running headers/footers:** Consistent page numbers, section names, publication name
- **Bleed images:** Photos that extend to the page edge (and beyond, into the bleed area)
- **Sidebar callouts:** Boxed or tinted background areas for supplementary information
- **Folios:** Page numbers with section indicators

---

## Design Movements in Magazine Layout

### Swiss / International Style
- **Fonts:** Helvetica, Univers, Akzidenz-Grotesk (use WorkSans, Outfit as substitutes)
- **Grid:** Strict modular grid, asymmetric placement
- **Color:** Restrained — black, white, one accent
- **Principle:** Content-first objectivity. The grid speaks.

### New York Magazine / Bold Editorial
- **Fonts:** Bold serifs (use InstrumentSerif, YoungSerif), overlapping type
- **Grid:** Broken deliberately for emphasis
- **Color:** High contrast, often black + one bold color
- **Principle:** Typography IS the content. Headlines as art.

### Kinfolk / Cereal (Minimal Lifestyle)
- **Fonts:** Thin sans-serifs, generous spacing (use Outfit 300, CrimsonPro)
- **Grid:** Open, lots of white space, centered compositions
- **Color:** Muted earth tones, cream backgrounds
- **Principle:** Breathing room. Let the photography do the work.

### Wired / Bloomberg (Data-Forward)
- **Fonts:** Monospace + geometric sans (use GeistMono, BricolageGrotesque)
- **Grid:** Dense 8-12 column grids, data tables, infographics
- **Color:** Bold, unexpected palettes — neon on dark, high saturation
- **Principle:** Information density with visual clarity.

### Harper's Bazaar (High Fashion)
- **Fonts:** Ultra-thin display + elegant serif (use Outfit 200, InstrumentSerif italic)
- **Grid:** Full-bleed photography, type overlapping images
- **Color:** Black and white dominant, with selective color
- **Principle:** Drama. The photograph is everything.

---

## CSS Patterns for Magazine Layout

### CSS Grid for Modular Layouts

```css
.editorial-grid {
    display: grid;
    grid-template-columns: repeat(6, 1fr);
    grid-template-rows: auto;
    gap: 30px;
    padding: 120px;
    width: 100%;
    height: 100%;
}
/* Article text spanning 3 columns */
.body-text {
    grid-column: 1 / 4;
}
/* Image spanning 3 columns */
.feature-image {
    grid-column: 4 / 7;
    grid-row: 1 / 3;
}
/* Pull quote spanning full width */
.pull-quote {
    grid-column: 1 / 7;
}
```

### Multi-Column Text Flow

```css
.article-body {
    column-count: 3;
    column-gap: 40px;
    column-rule: 1px solid rgba(0, 0, 0, 0.08);
    font-family: 'CrimsonPro', serif;
    font-size: 22px;
    line-height: 1.7;
    color: var(--fg);
    text-align: justify;
    hyphens: auto;
}
```

### Drop Cap — First Letter

```css
.article-body::first-letter {
    font-family: 'InstrumentSerif', serif;
    font-size: 120px;
    float: left;
    line-height: 0.8;
    padding-right: 16px;
    padding-top: 8px;
    color: var(--accent);
    font-weight: 400;
}
```

### Pull Quote Styling

```css
.pull-quote {
    font-family: 'InstrumentSerif', serif;
    font-size: 48px;
    font-style: italic;
    color: var(--fg);
    line-height: 1.3;
    padding: 60px 0;
    border-top: 3px solid var(--fg);
    border-bottom: 1px solid var(--muted);
    margin: 60px 0;
    text-align: center;
}
.pull-quote .attribution {
    font-family: 'WorkSans', sans-serif;
    font-size: 14px;
    font-style: normal;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    color: var(--fg);
    opacity: 0.5;
    margin-top: 24px;
    display: block;
}
```

### Baseline Grid via Line-Height

```css
/* Base unit: 14px — all line heights are multiples */
body {
    --baseline: 14px;
}
.body-text {
    font-size: 22px;
    line-height: calc(var(--baseline) * 2); /* 28px */
}
.subheading {
    font-size: 36px;
    line-height: calc(var(--baseline) * 3); /* 42px */
    margin-bottom: calc(var(--baseline) * 2); /* 28px */
}
.heading {
    font-size: 72px;
    line-height: calc(var(--baseline) * 6); /* 84px */
    margin-bottom: calc(var(--baseline) * 2);
}
```

### Running Header / Footer

```css
.running-header {
    position: absolute;
    top: 60px; left: 120px; right: 120px;
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    z-index: 5;
}
.running-header .section {
    font-family: 'WorkSans', sans-serif;
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 0.15em;
    color: var(--fg);
    opacity: 0.4;
}
.running-header .page-num {
    font-family: 'GeistMono', monospace;
    font-size: 12px;
    color: var(--fg);
    opacity: 0.3;
}
```

### Font Loading

```css
@font-face {
    font-family: 'InstrumentSerif';
    src: url('file:///Users/jaypokharna/Desktop/Shared%20Folder/Shared%20Folder/python/claude-skills/canvas-super-creator/skills/canvas-super-creator/canvas-fonts/InstrumentSerif-Regular.ttf');
    font-weight: 400;
}
@font-face {
    font-family: 'CrimsonPro';
    src: url('file:///Users/jaypokharna/Desktop/Shared%20Folder/Shared%20Folder/python/claude-skills/canvas-super-creator/skills/canvas-super-creator/canvas-fonts/CrimsonPro-Regular.ttf');
    font-weight: 400;
}
@font-face {
    font-family: 'WorkSans';
    src: url('file:///Users/jaypokharna/Desktop/Shared%20Folder/Shared%20Folder/python/claude-skills/canvas-super-creator/skills/canvas-super-creator/canvas-fonts/WorkSans-SemiBold.ttf');
    font-weight: 600;
}
```

---

## Anti-Patterns Specific to Magazines

- **Uniform margins on all sides.** Vary them — wider outside margins, narrower gutters. Asymmetry creates editorial sophistication.
- **Same font size for everything.** Magazine layouts thrive on extreme typographic hierarchy — 6:1 or 8:1 ratios between headline and body.
- **Ignoring gutter/column structure.** If elements do not snap to columns, the page feels amateur.
- **Text flowing past the fold line.** On a spread, the center gutter eats 30-40px. Never place critical content there.
- **Body text wider than 60-70 characters per line.** Optimal readability is 55-65 characters. Use columns to enforce this.
- **All-centered layouts.** Magazine spreads use left-aligned or justified text with deliberate asymmetry. Centered text is for pull quotes, not body copy.
- **Missing running elements.** Pages without folios, section headers, or publication marks look like unfinished layouts.
- **Uniform image sizes.** Vary image scales dramatically — one large hero, smaller supporting images. Creates visual rhythm.
