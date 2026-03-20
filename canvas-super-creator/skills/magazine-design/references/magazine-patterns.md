# Magazine Design — CSS Recipes by Category

Complete CSS patterns for magazine covers, editorial spreads, drop caps, pull quotes, and multi-column layouts. Each recipe includes full background, typography, and layout styling.

---

## Magazine Cover Layouts

### Fashion Cover

Bold serif masthead, full-bleed hero visual, stacked cover lines left side. High-fashion editorial drama.

```css
html, body { width: 2550px; height: 3300px; }

body {
    --bg: #0A0A0A;
    --fg: #F5F0E8;
    --accent: #D4AF37;
    --muted: #1A1A1A;
    position: relative;
    background: var(--bg);
}

/* Full-bleed visual area */
.hero-visual {
    position: absolute; top: 0; left: 0; width: 100%; height: 100%;
    background: var(--muted);
    z-index: 1;
}
/* Gradient overlay for text legibility */
.overlay {
    position: absolute; top: 0; left: 0; width: 100%; height: 100%;
    background: linear-gradient(180deg, rgba(0,0,0,0.4) 0%, transparent 30%, transparent 60%, rgba(0,0,0,0.6) 100%);
    z-index: 2;
}

/* Masthead */
.masthead {
    position: absolute;
    top: 80px; left: 0; width: 100%;
    text-align: center;
    z-index: 5;
}
.masthead h1 {
    font-family: 'InstrumentSerif', serif;
    font-size: 180px;
    font-weight: 400;
    color: var(--fg);
    letter-spacing: 0.08em;
    text-transform: uppercase;
}

/* Date / Issue */
.issue-info {
    position: absolute;
    top: 100px; right: 120px;
    z-index: 5;
}
.issue-info span {
    font-family: 'WorkSans', sans-serif;
    font-size: 16px;
    color: var(--fg);
    opacity: 0.5;
    letter-spacing: 0.1em;
    text-transform: uppercase;
}

/* Cover lines — stacked left */
.cover-lines {
    position: absolute;
    top: 45%; left: 120px;
    z-index: 5;
}
.cover-line-primary {
    font-family: 'InstrumentSerif', serif;
    font-size: 72px;
    color: var(--fg);
    line-height: 1.1;
    margin-bottom: 32px;
}
.cover-line-secondary {
    font-family: 'WorkSans', sans-serif;
    font-size: 28px;
    font-weight: 500;
    color: var(--fg);
    opacity: 0.7;
    line-height: 1.4;
    margin-bottom: 20px;
    letter-spacing: 0.02em;
}
.cover-line-accent {
    font-family: 'WorkSans', sans-serif;
    font-size: 18px;
    font-weight: 600;
    color: var(--accent);
    text-transform: uppercase;
    letter-spacing: 0.12em;
}

/* Barcode zone */
.barcode {
    position: absolute;
    bottom: 80px; right: 120px;
    width: 160px; height: 100px;
    background: var(--fg);
    z-index: 5;
}
```

---

### News Cover

Bold sans-serif masthead, strong red/black palette, urgent headline treatment. Newsweek/Time style.

```css
html, body { width: 2550px; height: 3300px; }

body {
    --bg: #FFFFFF;
    --fg: #1A1A1A;
    --accent: #E30613;
    --muted: #F0F0F0;
    position: relative;
    background: var(--bg);
}

/* Red masthead bar */
.masthead-bar {
    position: absolute;
    top: 0; left: 0; width: 100%; height: 200px;
    background: var(--accent);
    z-index: 5;
}
.masthead-bar h1 {
    font-family: 'BricolageGrotesque', sans-serif;
    font-size: 120px;
    font-weight: 800;
    color: var(--bg);
    text-align: center;
    line-height: 200px;
    letter-spacing: 0.06em;
    text-transform: uppercase;
}

/* Main headline — overlapping image */
.main-headline {
    position: absolute;
    bottom: 300px; left: 120px; right: 120px;
    z-index: 5;
}
.main-headline h2 {
    font-family: 'BricolageGrotesque', sans-serif;
    font-size: 96px;
    font-weight: 800;
    color: var(--fg);
    line-height: 1.05;
    letter-spacing: -0.02em;
}
.main-headline .deck {
    font-family: 'CrimsonPro', serif;
    font-size: 32px;
    color: var(--fg);
    opacity: 0.7;
    margin-top: 24px;
    line-height: 1.4;
}

/* Date and price */
.meta {
    position: absolute;
    top: 220px; left: 120px;
    font-family: 'WorkSans', sans-serif;
    font-size: 14px;
    color: var(--fg);
    opacity: 0.4;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    z-index: 5;
}
```

---

### Lifestyle Cover

Warm earth tones, thin sans-serif, generous whitespace. Kinfolk/Cereal aesthetic.

```css
html, body { width: 2550px; height: 3300px; }

body {
    --bg: #F5F0E8;
    --fg: #3B322A;
    --accent: #9B8B78;
    --muted: #E8DFD2;
    position: relative;
    background: var(--bg);
}

/* Centered minimal masthead */
.masthead {
    position: absolute;
    top: 120px; left: 0; width: 100%;
    text-align: center;
    z-index: 5;
}
.masthead h1 {
    font-family: 'Outfit', sans-serif;
    font-size: 96px;
    font-weight: 200;
    color: var(--fg);
    letter-spacing: 0.2em;
    text-transform: uppercase;
}

/* Central image — generously padded */
.feature-image {
    position: absolute;
    top: 18%; left: 12%; width: 76%; height: 50%;
    background: var(--muted);
    z-index: 2;
}

/* Cover text — minimal, lower third */
.cover-text {
    position: absolute;
    bottom: 15%; left: 0; width: 100%;
    text-align: center;
    z-index: 5;
}
.cover-text .lead {
    font-family: 'InstrumentSerif', serif;
    font-size: 48px;
    font-style: italic;
    color: var(--fg);
    margin-bottom: 16px;
}
.cover-text .issue {
    font-family: 'Outfit', sans-serif;
    font-size: 16px;
    font-weight: 300;
    color: var(--accent);
    letter-spacing: 0.2em;
    text-transform: uppercase;
}
```

---

### Tech Cover

Dark background, monospace accents, neon highlights. Wired/Ars Technica energy.

```css
html, body { width: 2550px; height: 3300px; }

body {
    --bg: #0C0C0F;
    --fg: #E8ECF0;
    --accent: #00E5FF;
    --accent2: #FF2D78;
    --muted: #1A1A24;
    position: relative;
    background: var(--bg);
}

/* Grid background */
.grid-bg {
    position: absolute; top: 0; left: 0; width: 100%; height: 100%;
    background:
        repeating-linear-gradient(0deg, rgba(0,229,255,0.03) 0px, rgba(0,229,255,0.03) 1px, transparent 1px, transparent 60px),
        repeating-linear-gradient(90deg, rgba(0,229,255,0.03) 0px, rgba(0,229,255,0.03) 1px, transparent 1px, transparent 60px);
    z-index: 1;
}

/* Masthead — monospace */
.masthead {
    position: absolute;
    top: 80px; left: 120px;
    z-index: 5;
}
.masthead h1 {
    font-family: 'GeistMono', monospace;
    font-size: 80px;
    font-weight: 700;
    color: var(--accent);
    letter-spacing: 0.1em;
    text-transform: uppercase;
}

/* Main headline — bold, glitchy */
.headline {
    position: absolute;
    top: 40%; left: 120px; right: 120px;
    z-index: 5;
}
.headline h2 {
    font-family: 'BricolageGrotesque', sans-serif;
    font-size: 120px;
    font-weight: 800;
    color: var(--fg);
    line-height: 1;
    letter-spacing: -0.03em;
}
.headline .deck {
    font-family: 'GeistMono', monospace;
    font-size: 22px;
    color: var(--accent);
    opacity: 0.7;
    margin-top: 32px;
    line-height: 1.6;
    letter-spacing: 0.02em;
}

/* Issue data — bottom left */
.issue-data {
    position: absolute;
    bottom: 120px; left: 120px;
    z-index: 5;
}
.issue-data .label {
    font-family: 'GeistMono', monospace;
    font-size: 12px;
    color: var(--accent);
    opacity: 0.5;
    text-transform: uppercase;
    letter-spacing: 0.15em;
}
.issue-data .value {
    font-family: 'GeistMono', monospace;
    font-size: 14px;
    color: var(--fg);
    opacity: 0.4;
    margin-top: 4px;
}

.noise { position: absolute; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; z-index: 10; opacity: 0.04; }
```

---

### Art Cover

Full-bleed artwork, minimal type, gallery aesthetic. The art dominates.

```css
html, body { width: 2550px; height: 3300px; }

body {
    --bg: #FAF8F5;
    --fg: #2C2C2C;
    --accent: #8B6914;
    --muted: #E8E4DE;
    position: relative;
    background: var(--bg);
}

/* Full-bleed artwork area */
.artwork {
    position: absolute;
    top: 0; left: 0; width: 100%; height: 75%;
    background: var(--muted);
    z-index: 1;
}

/* Minimal masthead — top, overlaying image */
.masthead {
    position: absolute;
    top: 60px; left: 0; width: 100%;
    text-align: center;
    z-index: 5;
}
.masthead h1 {
    font-family: 'InstrumentSerif', serif;
    font-size: 64px;
    font-weight: 400;
    color: var(--fg);
    letter-spacing: 0.15em;
    text-transform: uppercase;
    mix-blend-mode: multiply;
}

/* Info bar — bottom 25% */
.info-bar {
    position: absolute;
    bottom: 0; left: 0; width: 100%; height: 25%;
    padding: 60px 120px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    z-index: 3;
}
.info-bar .artist {
    font-family: 'InstrumentSerif', serif;
    font-size: 42px;
    color: var(--fg);
}
.info-bar .title {
    font-family: 'InstrumentSerif', serif;
    font-size: 28px;
    font-style: italic;
    color: var(--accent);
    margin-top: 8px;
}
.info-bar .meta {
    font-family: 'Outfit', sans-serif;
    font-size: 13px;
    color: var(--fg);
    opacity: 0.4;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-top: 24px;
}
```

---

### Minimal Cover

Maximum whitespace, one word masthead, single element. Whisper, do not shout.

```css
html, body { width: 2550px; height: 3300px; }

body {
    --bg: #FFFFFF;
    --fg: #1A1A1A;
    --accent: #999999;
    --muted: #F5F5F5;
    position: relative;
    background: var(--bg);
}

/* Masthead — large, centered, top */
.masthead {
    position: absolute;
    top: 200px; left: 0; width: 100%;
    text-align: center;
    z-index: 5;
}
.masthead h1 {
    font-family: 'Outfit', sans-serif;
    font-size: 140px;
    font-weight: 100;
    color: var(--fg);
    letter-spacing: 0.25em;
    text-transform: uppercase;
}

/* Single visual element — centered */
.single-element {
    position: absolute;
    top: 50%; left: 50%;
    transform: translate(-50%, -50%);
    width: 600px; height: 600px;
    background: var(--muted);
    z-index: 2;
}

/* Issue line — bottom center */
.issue-line {
    position: absolute;
    bottom: 200px; left: 0; width: 100%;
    text-align: center;
    z-index: 5;
}
.issue-line span {
    font-family: 'Outfit', sans-serif;
    font-size: 16px;
    font-weight: 300;
    color: var(--accent);
    letter-spacing: 0.3em;
    text-transform: uppercase;
}
```

---

## Editorial Spread Grid Templates

### 6-Column Text-Heavy Spread

```css
html, body { width: 5100px; height: 3300px; }

body {
    --bg: #FAFAF8;
    --fg: #2C2C2C;
    --accent: #B8452A;
    --muted: #E8E4DE;
    position: relative;
    background: var(--bg);
}

.spread-grid {
    position: absolute;
    top: 120px; left: 120px; right: 120px; bottom: 120px;
    display: grid;
    grid-template-columns: repeat(6, 1fr);
    grid-template-rows: auto 1fr auto;
    gap: 30px;
    z-index: 3;
}

/* Headline spanning 4 columns */
.spread-headline {
    grid-column: 1 / 5;
    grid-row: 1;
    font-family: 'InstrumentSerif', serif;
    font-size: 96px;
    color: var(--fg);
    line-height: 1.05;
    letter-spacing: -0.02em;
    padding-bottom: 40px;
    border-bottom: 2px solid var(--fg);
}

/* Body text in 3 columns */
.body-text {
    grid-column: 1 / 4;
    grid-row: 2;
    column-count: 3;
    column-gap: 30px;
    font-family: 'CrimsonPro', serif;
    font-size: 22px;
    line-height: 1.7;
    color: var(--fg);
    text-align: justify;
}

/* Image in right 3 columns */
.spread-image {
    grid-column: 4 / 7;
    grid-row: 1 / 4;
    background: var(--muted);
}

/* Folio */
.folio {
    grid-column: 1 / 7;
    grid-row: 3;
    display: flex;
    justify-content: space-between;
    font-family: 'Outfit', sans-serif;
    font-size: 12px;
    color: var(--fg);
    opacity: 0.3;
    letter-spacing: 0.1em;
    text-transform: uppercase;
}
```

### 8-Column Data Spread

```css
.data-spread {
    position: absolute;
    top: 120px; left: 120px; right: 120px; bottom: 120px;
    display: grid;
    grid-template-columns: repeat(8, 1fr);
    grid-template-rows: auto 1fr 1fr auto;
    gap: 24px;
    z-index: 3;
}

.section-header {
    grid-column: 1 / 9;
    grid-row: 1;
    font-family: 'BricolageGrotesque', sans-serif;
    font-size: 72px;
    font-weight: 800;
    color: var(--fg);
    letter-spacing: -0.02em;
    padding-bottom: 24px;
    border-bottom: 3px solid var(--accent);
}

.data-block {
    grid-column: span 2;
    background: var(--muted);
    padding: 32px;
}
.data-block .value {
    font-family: 'BigShoulders', sans-serif;
    font-size: 64px;
    font-weight: 700;
    color: var(--accent);
    line-height: 1;
}
.data-block .label {
    font-family: 'GeistMono', monospace;
    font-size: 12px;
    color: var(--fg);
    opacity: 0.5;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-top: 12px;
}

.body-column {
    grid-column: span 4;
    column-count: 2;
    column-gap: 24px;
    font-family: 'Outfit', sans-serif;
    font-size: 18px;
    line-height: 1.6;
    color: var(--fg);
}

.sidebar {
    grid-column: span 2;
    background: var(--fg);
    color: var(--bg);
    padding: 32px;
}
.sidebar h3 {
    font-family: 'WorkSans', sans-serif;
    font-size: 20px;
    font-weight: 700;
    margin-bottom: 16px;
    text-transform: uppercase;
    letter-spacing: 0.08em;
}
.sidebar p {
    font-family: 'Outfit', sans-serif;
    font-size: 16px;
    line-height: 1.5;
    opacity: 0.8;
}
```

### Full-Bleed Photo Spread

```css
.photo-spread {
    position: absolute;
    top: 0; left: 0; width: 100%; height: 100%;
    display: grid;
    grid-template-columns: 1fr 1fr;
    z-index: 1;
}

/* Left page — full bleed image */
.left-page {
    background: var(--muted);
    position: relative;
}

/* Right page — text overlay */
.right-page {
    position: relative;
    padding: 200px 120px;
    display: flex;
    flex-direction: column;
    justify-content: center;
}
.right-page .headline {
    font-family: 'InstrumentSerif', serif;
    font-size: 80px;
    color: var(--fg);
    line-height: 1.1;
    margin-bottom: 48px;
}
.right-page .body {
    column-count: 2;
    column-gap: 40px;
    font-family: 'CrimsonPro', serif;
    font-size: 20px;
    line-height: 1.7;
    color: var(--fg);
}
```

### Asymmetric Feature Spread

```css
.feature-spread {
    position: absolute;
    top: 0; left: 0; width: 100%; height: 100%;
    display: grid;
    grid-template-columns: 2fr 3fr;
    z-index: 1;
}

/* Narrow left column — metadata */
.meta-column {
    padding: 120px 60px;
    display: flex;
    flex-direction: column;
    justify-content: flex-end;
    background: var(--fg);
    color: var(--bg);
}
.meta-column .category {
    font-family: 'GeistMono', monospace;
    font-size: 11px;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    opacity: 0.5;
    margin-bottom: auto;
}
.meta-column .headline {
    font-family: 'InstrumentSerif', serif;
    font-size: 64px;
    line-height: 1.1;
    margin-bottom: 32px;
}
.meta-column .byline {
    font-family: 'WorkSans', sans-serif;
    font-size: 14px;
    opacity: 0.6;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}

/* Wide right column — content */
.content-column {
    padding: 120px 120px 120px 80px;
    display: flex;
    flex-direction: column;
    justify-content: center;
}
.content-column .body {
    column-count: 2;
    column-gap: 40px;
    font-family: 'CrimsonPro', serif;
    font-size: 21px;
    line-height: 1.7;
    color: var(--fg);
}
```

---

## Drop Cap CSS Recipes

### Classic Drop Cap

```css
.article-classic::first-letter {
    font-family: 'InstrumentSerif', serif;
    font-size: 120px;
    float: left;
    line-height: 0.8;
    padding-right: 16px;
    padding-top: 4px;
    color: var(--fg);
    font-weight: 400;
}
```

### Decorative Drop Cap

```css
.article-decorative::first-letter {
    font-family: 'YoungSerif', serif;
    font-size: 140px;
    float: left;
    line-height: 0.75;
    padding-right: 20px;
    padding-top: 8px;
    color: var(--accent);
    font-weight: 400;
    text-shadow: 3px 3px 0 var(--muted);
}
```

### Color-Block Drop Cap

```css
.article-block::first-letter {
    font-family: 'BigShoulders', sans-serif;
    font-size: 100px;
    float: left;
    line-height: 1;
    padding: 12px 24px;
    margin-right: 16px;
    margin-top: 4px;
    background: var(--accent);
    color: var(--bg);
    font-weight: 700;
}
```

---

## Pull Quote CSS Recipes

### Large Serif Pull Quote

```css
.pq-serif {
    font-family: 'InstrumentSerif', serif;
    font-size: 52px;
    font-style: italic;
    color: var(--fg);
    line-height: 1.25;
    text-align: center;
    padding: 80px 60px;
    margin: 60px 0;
    position: relative;
}
.pq-serif::before {
    content: '\201C';
    font-size: 200px;
    position: absolute;
    top: -20px; left: 50%;
    transform: translateX(-50%);
    color: var(--accent);
    opacity: 0.15;
    line-height: 1;
}
.pq-serif .attribution {
    display: block;
    font-family: 'WorkSans', sans-serif;
    font-size: 14px;
    font-style: normal;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    color: var(--fg);
    opacity: 0.4;
    margin-top: 24px;
}
```

### Rule-Bordered Pull Quote

```css
.pq-ruled {
    font-family: 'CrimsonPro', serif;
    font-size: 36px;
    font-style: italic;
    color: var(--fg);
    line-height: 1.4;
    padding: 48px 0;
    margin: 48px 0;
    border-top: 3px solid var(--fg);
    border-bottom: 1px solid var(--muted);
}
.pq-ruled .attribution {
    display: block;
    font-family: 'WorkSans', sans-serif;
    font-size: 13px;
    font-style: normal;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: var(--accent);
    margin-top: 20px;
}
```

### Sidebar Inset Pull Quote

```css
.pq-sidebar {
    float: right;
    width: 40%;
    margin: 0 0 32px 40px;
    padding: 32px;
    background: var(--muted);
    font-family: 'InstrumentSerif', serif;
    font-size: 28px;
    font-style: italic;
    color: var(--fg);
    line-height: 1.4;
    border-left: 4px solid var(--accent);
}
.pq-sidebar .attribution {
    display: block;
    font-family: 'Outfit', sans-serif;
    font-size: 12px;
    font-style: normal;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: var(--fg);
    opacity: 0.5;
    margin-top: 16px;
}
```

---

## Running Header / Footer Pattern

```css
/* Running header — top of every page */
.running-header {
    position: absolute;
    top: 60px; left: 120px; right: 120px;
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    z-index: 6;
}
.running-header .section-name {
    font-family: 'WorkSans', sans-serif;
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 0.15em;
    color: var(--fg);
    opacity: 0.35;
}
.running-header .publication {
    font-family: 'InstrumentSerif', serif;
    font-size: 13px;
    font-style: italic;
    color: var(--fg);
    opacity: 0.3;
}

/* Running footer — bottom of every page */
.running-footer {
    position: absolute;
    bottom: 60px; left: 120px; right: 120px;
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    z-index: 6;
}
.running-footer .page-number {
    font-family: 'GeistMono', monospace;
    font-size: 14px;
    color: var(--fg);
    opacity: 0.3;
}
.running-footer .issue-date {
    font-family: 'Outfit', sans-serif;
    font-size: 11px;
    color: var(--fg);
    opacity: 0.25;
    letter-spacing: 0.1em;
    text-transform: uppercase;
}
```

---

## Multi-Column Text Flow with Image Interrupt

```css
/* 3-column article body with inline image breaking the flow */
.article-flow {
    position: absolute;
    top: 300px; left: 120px; right: 120px; bottom: 120px;
    column-count: 3;
    column-gap: 40px;
    column-rule: 1px solid rgba(0, 0, 0, 0.06);
    font-family: 'CrimsonPro', serif;
    font-size: 21px;
    line-height: 1.7;
    color: var(--fg);
    text-align: justify;
    hyphens: auto;
    z-index: 3;
}

/* Image that breaks across columns */
.inline-image {
    column-span: all;
    width: 100%;
    height: 600px;
    background: var(--muted);
    margin: 40px 0;
}

/* Caption for inline image */
.inline-caption {
    column-span: all;
    font-family: 'Outfit', sans-serif;
    font-size: 13px;
    color: var(--fg);
    opacity: 0.5;
    margin-top: -28px;
    margin-bottom: 40px;
    letter-spacing: 0.03em;
}
```
