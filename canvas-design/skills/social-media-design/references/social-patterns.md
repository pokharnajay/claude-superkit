# Social Media Design — Platform-Specific CSS Recipes

Complete CSS patterns for each social media platform. Each recipe is tuned to the platform's dimensions, compression behavior, and audience context.

---

## Instagram Square (1080 x 1080)

### Glass Card on Gradient

```css
html, body { width: 1080px; height: 1080px; }

body {
    --bg: #0C0C0F;
    --fg: #E8ECF0;
    --accent: #00E5FF;
    --accent2: #FF2D78;
    --muted: #1A1A24;
    position: relative;
    background: var(--bg);
}

/* Mesh background */
.mesh {
    position: absolute; top: 0; left: 0; width: 100%; height: 100%;
    background:
        radial-gradient(ellipse at 25% 25%, rgba(0, 229, 255, 0.12) 0%, transparent 50%),
        radial-gradient(ellipse at 75% 75%, rgba(255, 45, 120, 0.1) 0%, transparent 50%),
        var(--bg);
    z-index: 1;
}

/* Glass card */
.card {
    position: absolute;
    top: 50%; left: 50%;
    transform: translate(-50%, -50%);
    width: 80%; padding: 60px;
    background: rgba(255, 255, 255, 0.06);
    backdrop-filter: blur(24px);
    -webkit-backdrop-filter: blur(24px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 20px;
    z-index: 3;
    text-align: center;
}
.card h1 {
    font-family: 'BigShoulders', sans-serif;
    font-size: 64px; font-weight: 700;
    color: var(--fg); line-height: 1.1;
}
.card p {
    font-family: 'Outfit', sans-serif;
    font-size: 22px; color: var(--fg);
    opacity: 0.6; margin-top: 16px; line-height: 1.5;
}

.noise { position: absolute; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; z-index: 10; opacity: 0.03; }
```

### Stat Card

```css
.stat-card {
    position: absolute;
    top: 50%; left: 50%;
    transform: translate(-50%, -50%);
    text-align: center;
    z-index: 3;
}
.stat-card .number {
    font-family: 'BigShoulders', sans-serif;
    font-size: 180px; font-weight: 700;
    background: linear-gradient(135deg, var(--accent), var(--accent2));
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
    line-height: 1;
}
.stat-card .label {
    font-family: 'WorkSans', sans-serif;
    font-size: 20px; color: var(--fg);
    text-transform: uppercase;
    letter-spacing: 0.15em; opacity: 0.5;
    margin-top: 16px;
}
.stat-card .context {
    font-family: 'Outfit', sans-serif;
    font-size: 18px; color: var(--fg);
    opacity: 0.4; margin-top: 24px;
    max-width: 400px;
    margin-left: auto; margin-right: auto;
    line-height: 1.5;
}
```

### Quote Card

```css
.quote-container {
    position: absolute;
    top: 0; left: 0; width: 100%; height: 100%;
    display: flex; align-items: center; justify-content: center;
    padding: 80px;
    z-index: 3;
}
.quote-mark {
    position: absolute; top: 60px; left: 60px;
    font-family: 'InstrumentSerif', serif;
    font-size: 240px; color: var(--accent);
    opacity: 0.1; line-height: 0.5;
}
.quote-text {
    font-family: 'Lora', serif;
    font-size: 40px; font-weight: 600;
    color: var(--fg); line-height: 1.4;
    font-style: italic; text-align: center;
}
.attribution {
    position: absolute; bottom: 80px; left: 50%;
    transform: translateX(-50%);
    font-family: 'WorkSans', sans-serif;
    font-size: 16px; color: var(--fg);
    opacity: 0.4; text-transform: uppercase;
    letter-spacing: 0.12em;
}
```

### Product / Feature Card

```css
.feature-card {
    position: absolute;
    top: 0; left: 0; width: 100%; height: 100%;
    display: flex; flex-direction: column;
    z-index: 3;
}
.feature-visual {
    height: 55%;
    background: var(--muted);
    display: flex; align-items: center; justify-content: center;
    position: relative; overflow: hidden;
}
.feature-icon {
    width: 120px; height: 120px;
    border: 3px solid var(--accent);
    border-radius: 24px;
    display: flex; align-items: center; justify-content: center;
}
.feature-info {
    height: 45%;
    padding: 40px 50px;
    display: flex; flex-direction: column; justify-content: center;
}
.feature-info .badge {
    display: inline-block; width: fit-content;
    font-family: 'JetBrainsMono', monospace;
    font-size: 11px; color: var(--accent);
    text-transform: uppercase; letter-spacing: 0.12em;
    border: 1px solid var(--accent); border-radius: 4px;
    padding: 4px 12px; margin-bottom: 16px;
}
.feature-info h2 {
    font-family: 'BricolageGrotesque', sans-serif;
    font-size: 36px; font-weight: 700;
    color: var(--fg); line-height: 1.2;
}
.feature-info p {
    font-family: 'Outfit', sans-serif;
    font-size: 18px; color: var(--fg);
    opacity: 0.5; margin-top: 12px; line-height: 1.5;
}
```

---

## Instagram Story (1080 x 1920)

Vertical stacked sections with safe zones for story bar (top 200px) and swipe-up CTA (bottom 250px).

```css
html, body { width: 1080px; height: 1920px; }

body {
    --bg: #1C1210;
    --fg: #F5E6D3;
    --accent: #E8622B;
    --muted: #3D2B24;
    position: relative;
    background: var(--bg);
}

/* Full-bleed gradient */
.bg-gradient {
    position: absolute; top: 0; left: 0; width: 100%; height: 100%;
    background: linear-gradient(180deg, var(--muted) 0%, var(--bg) 40%, var(--bg) 70%, var(--muted) 100%);
    z-index: 1;
}

/* Content — between safe zones (200px top, 250px bottom) */
.safe-content {
    position: absolute;
    top: 240px; left: 60px; right: 60px; bottom: 290px;
    display: flex; flex-direction: column;
    justify-content: center; gap: 40px;
    z-index: 3;
}
.story-heading {
    font-family: 'Boldonse', sans-serif;
    font-size: 72px; color: var(--fg);
    line-height: 1.05;
}
.story-body {
    font-family: 'Outfit', sans-serif;
    font-size: 28px; color: var(--fg);
    opacity: 0.7; line-height: 1.5;
}
.story-cta {
    font-family: 'WorkSans', sans-serif;
    font-size: 18px; color: var(--accent);
    text-transform: uppercase;
    letter-spacing: 0.15em;
    margin-top: auto;
}

/* Decorative accent bar */
.accent-bar {
    position: absolute;
    left: 60px; top: 240px;
    width: 60px; height: 4px;
    background: var(--accent);
    z-index: 4;
}

.noise { position: absolute; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; z-index: 10; opacity: 0.04; }
```

---

## LinkedIn Post (1200 x 627)

Professional, credible, data-forward. Avoid casual or meme aesthetics.

```css
html, body { width: 1200px; height: 627px; }

body {
    --bg: #F0F4F8;
    --fg: #1A2332;
    --accent: #4A90D9;
    --accent2: #E8B4B8;
    --muted: #C8D6E0;
    position: relative;
    background: var(--bg);
}

/* Subtle grid background */
.grid-bg {
    position: absolute; top: 0; left: 0; width: 100%; height: 100%;
    background:
        repeating-linear-gradient(0deg, rgba(26, 35, 50, 0.02) 0px, rgba(26, 35, 50, 0.02) 1px, transparent 1px, transparent 50px),
        repeating-linear-gradient(90deg, rgba(26, 35, 50, 0.02) 0px, rgba(26, 35, 50, 0.02) 1px, transparent 1px, transparent 50px);
    z-index: 1;
}

/* Professional card layout */
.card-layout {
    position: absolute;
    top: 50px; left: 50px; right: 50px; bottom: 50px;
    display: flex; gap: 50px;
    z-index: 3;
}
.card-left {
    flex: 1; display: flex; flex-direction: column; justify-content: center;
}
.card-left .overline {
    font-family: 'IBMPlexMono', monospace;
    font-size: 12px; color: var(--accent);
    text-transform: uppercase; letter-spacing: 0.12em;
    margin-bottom: 16px;
}
.card-left h1 {
    font-family: 'BricolageGrotesque', sans-serif;
    font-size: 42px; font-weight: 700;
    color: var(--fg); line-height: 1.2;
    letter-spacing: -0.02em;
}
.card-left p {
    font-family: 'Outfit', sans-serif;
    font-size: 18px; color: var(--fg);
    opacity: 0.6; margin-top: 16px; line-height: 1.5;
}

/* Data visualization placeholder */
.card-right {
    width: 40%;
    background: white;
    border-radius: 12px;
    border: 1px solid rgba(26, 35, 50, 0.08);
    padding: 30px;
    display: flex; flex-direction: column; justify-content: center;
    box-shadow: 0 4px 24px rgba(0, 0, 0, 0.04);
}
.metric {
    margin-bottom: 24px;
}
.metric .value {
    font-family: 'BigShoulders', sans-serif;
    font-size: 56px; font-weight: 700;
    color: var(--accent); line-height: 1;
}
.metric .label {
    font-family: 'Outfit', sans-serif;
    font-size: 14px; color: var(--fg);
    opacity: 0.5; margin-top: 4px;
    text-transform: uppercase; letter-spacing: 0.08em;
}
.metric .bar {
    width: 100%; height: 6px;
    background: var(--muted);
    border-radius: 3px; margin-top: 8px;
    overflow: hidden;
}
.metric .bar-fill {
    height: 100%; background: var(--accent);
    border-radius: 3px;
}
```

---

## Twitter/X Post (1600 x 900)

Bold statement, minimal elements, high contrast. Must survive JPEG compression.

```css
html, body { width: 1600px; height: 900px; }

body {
    --bg: #0C0C0F;
    --fg: #E8ECF0;
    --accent: #00E5FF;
    --muted: #1A1A24;
    position: relative;
    background: var(--bg);
}

/* Single accent orb */
.orb {
    position: absolute;
    width: 500px; height: 500px;
    border-radius: 50%;
    background: var(--accent);
    filter: blur(150px);
    opacity: 0.08;
    top: 50%; left: 30%;
    transform: translate(-50%, -50%);
    z-index: 1;
}

/* Bold centered statement */
.statement {
    position: absolute;
    top: 0; left: 0; width: 100%; height: 100%;
    display: flex; align-items: center; justify-content: center;
    padding: 80px;
    z-index: 3;
}
.statement h1 {
    font-family: 'BigShoulders', sans-serif;
    font-size: 80px; font-weight: 700;
    color: var(--fg); text-align: center;
    line-height: 1.1; letter-spacing: 0.02em;
    max-width: 900px;
}
.statement .highlight {
    color: var(--accent);
}

/* Attribution bar — bottom */
.attr-bar {
    position: absolute;
    bottom: 50px; left: 80px; right: 80px;
    display: flex; justify-content: space-between;
    align-items: center;
    z-index: 3;
}
.attr-bar .handle {
    font-family: 'GeistMono', monospace;
    font-size: 16px; color: var(--fg);
    opacity: 0.3;
}
.attr-bar .accent-line {
    flex: 1; height: 1px;
    background: rgba(255,255,255,0.06);
    margin: 0 24px;
}

.noise { position: absolute; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; z-index: 10; opacity: 0.03; }
```

---

## Pinterest Pin (1000 x 1500)

Tall vertical format. Section-based, text-heavy content performs well. Key content in top 2/3.

```css
html, body { width: 1000px; height: 1500px; }

body {
    --bg: #F5EFDF;
    --fg: #3B2F22;
    --accent: #B8860B;
    --accent2: #8B7355;
    --muted: #DDD2BE;
    position: relative;
    background: var(--bg);
}

/* Section layout */
.pin-header {
    position: absolute;
    top: 0; left: 0; width: 100%; height: 30%;
    background: var(--fg);
    display: flex; align-items: center; justify-content: center;
    padding: 40px;
    z-index: 2;
}
.pin-header h1 {
    font-family: 'YoungSerif', serif;
    font-size: 52px; color: var(--bg);
    text-align: center; line-height: 1.2;
    letter-spacing: -0.02em;
}

.pin-body {
    position: absolute;
    top: 30%; left: 0; width: 100%; height: 50%;
    padding: 50px 60px;
    z-index: 2;
}
.pin-item {
    display: flex; align-items: flex-start; gap: 20px;
    margin-bottom: 32px;
}
.pin-item .num {
    font-family: 'BigShoulders', sans-serif;
    font-size: 36px; font-weight: 700;
    color: var(--accent);
    flex-shrink: 0; width: 40px;
}
.pin-item .text h3 {
    font-family: 'WorkSans', sans-serif;
    font-size: 22px; font-weight: 600;
    color: var(--fg); margin-bottom: 4px;
}
.pin-item .text p {
    font-family: 'Outfit', sans-serif;
    font-size: 16px; color: var(--fg);
    opacity: 0.6; line-height: 1.4;
}

.pin-footer {
    position: absolute;
    bottom: 0; left: 0; width: 100%; height: 20%;
    display: flex; align-items: center; justify-content: center;
    border-top: 2px solid var(--muted);
    z-index: 2;
}
.pin-footer .cta {
    font-family: 'WorkSans', sans-serif;
    font-size: 18px; font-weight: 600;
    color: var(--accent);
    text-transform: uppercase;
    letter-spacing: 0.12em;
}

.noise { position: absolute; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; z-index: 10; opacity: 0.025; }
```
