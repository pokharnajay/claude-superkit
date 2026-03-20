# Poster Design — CSS Recipes by Category

Platform-specific CSS recipes for different poster genres. Each recipe includes complete background, typography, and layout styling.

---

## Event Poster

Bold diagonal compositions, high contrast, urgent typography. Communicates energy and excitement.

```css
html, body { width: 3300px; height: 5100px; }

body {
    --bg: #121212;
    --fg: #F5F5F0;
    --accent: #E63B2E;
    --accent2: #F5C518;
    --muted: #2A2A2A;
    position: relative;
    background: var(--bg);
}

/* Diagonal color slash */
.diagonal-slash {
    position: absolute;
    top: 0; left: 0; width: 100%; height: 100%;
    clip-path: polygon(0 0, 65% 0, 35% 100%, 0 100%);
    background: linear-gradient(180deg, var(--accent) 0%, #8B1A10 100%);
    z-index: 1;
}

/* Grid overlay */
.grid {
    position: absolute; top: 0; left: 0; width: 100%; height: 100%;
    background:
        repeating-linear-gradient(0deg, rgba(255,255,255,0.02) 0px, rgba(255,255,255,0.02) 1px, transparent 1px, transparent 80px),
        repeating-linear-gradient(90deg, rgba(255,255,255,0.02) 0px, rgba(255,255,255,0.02) 1px, transparent 1px, transparent 80px);
    z-index: 2;
}

/* Title — massive, positioned at the collision of the diagonal */
.title {
    position: absolute;
    top: 25%; left: 100px; right: 100px;
    font-family: 'Boldonse', sans-serif;
    font-size: 200px;
    color: var(--fg);
    line-height: 0.9;
    letter-spacing: -0.03em;
    z-index: 4;
    text-shadow: 4px 4px 0 rgba(0,0,0,0.3);
}

/* Date block — urgent, highlighted */
.date-block {
    position: absolute;
    top: 60%; left: 100px;
    z-index: 4;
}
.date-block .day {
    font-family: 'BigShoulders', sans-serif;
    font-size: 160px; font-weight: 700;
    color: var(--accent2);
    line-height: 1;
}
.date-block .month-year {
    font-family: 'WorkSans', sans-serif;
    font-size: 28px; color: var(--fg);
    text-transform: uppercase;
    letter-spacing: 0.15em; opacity: 0.7;
}

/* Venue info — bottom zone */
.venue {
    position: absolute;
    bottom: 150px; left: 100px; right: 100px;
    z-index: 4;
}
.venue .name {
    font-family: 'WorkSans', sans-serif;
    font-size: 36px; font-weight: 600;
    color: var(--fg); letter-spacing: 0.05em;
}
.venue .address {
    font-family: 'JetBrainsMono', monospace;
    font-size: 18px; color: var(--fg);
    opacity: 0.4; margin-top: 8px;
}

/* Noise */
.noise { position: absolute; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; z-index: 10; opacity: 0.04; }
```

---

## Movie Poster

Dramatic full-bleed gradients, cinematic title treatment, credits block at bottom 25%.

```css
html, body { width: 2700px; height: 4000px; }

body {
    --bg: #0D1117;
    --fg: #D4D4D8;
    --accent: #9B1B30;
    --accent2: #D43D51;
    --muted: #1A2030;
    position: relative;
    background: var(--bg);
}

/* Dramatic vignette gradient */
.vignette {
    position: absolute; top: 0; left: 0; width: 100%; height: 100%;
    background:
        radial-gradient(ellipse 80% 60% at 50% 35%, transparent 30%, var(--bg) 80%),
        linear-gradient(180deg, var(--muted) 0%, var(--bg) 40%);
    z-index: 2;
}

/* Central light source */
.light-source {
    position: absolute;
    top: 15%; left: 50%; transform: translateX(-50%);
    width: 800px; height: 800px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(155, 27, 48, 0.2) 0%, transparent 70%);
    filter: blur(60px);
    z-index: 1;
}

/* Title treatment */
.title {
    position: absolute;
    top: 50%; left: 50%; transform: translate(-50%, -50%);
    text-align: center;
    z-index: 4;
}
.title h1 {
    font-family: 'InstrumentSerif', serif;
    font-size: 140px; font-weight: 400;
    color: var(--fg);
    letter-spacing: -0.02em; line-height: 1;
    text-shadow: 0 4px 60px rgba(155, 27, 48, 0.3);
}
.title .tagline {
    font-family: 'CrimsonPro', serif;
    font-size: 28px; font-style: italic;
    color: var(--accent2); opacity: 0.8;
    margin-top: 24px; letter-spacing: 0.05em;
}

/* Credits block — bottom 25% */
.credits {
    position: absolute;
    bottom: 80px; left: 100px; right: 100px;
    z-index: 4;
}
.credits .separator {
    width: 100%; height: 1px;
    background: rgba(212, 212, 216, 0.15);
    margin-bottom: 24px;
}
.credits .billing {
    font-family: 'DMMono', monospace;
    font-size: 14px; color: var(--fg);
    opacity: 0.3; line-height: 2;
    letter-spacing: 0.05em;
    text-transform: uppercase;
}
.credits .studio {
    font-family: 'WorkSans', sans-serif;
    font-size: 18px; color: var(--fg);
    opacity: 0.5; margin-top: 16px;
    text-transform: uppercase; letter-spacing: 0.2em;
}

/* Noise */
.noise { position: absolute; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; z-index: 10; opacity: 0.045; }
```

---

## Concert Poster

Grungy textures, layered typography, limited palette. Raw energy.

```css
html, body { width: 3300px; height: 5100px; }

body {
    --bg: #F0E8D8;
    --fg: #1A1410;
    --accent: #6B4226;
    --accent2: #B8452A;
    --muted: #D8CCBA;
    position: relative;
    background: var(--bg);
}

/* Distressed texture background */
.texture-layer {
    position: absolute; top: 0; left: 0; width: 100%; height: 100%;
    background:
        radial-gradient(circle at 30% 70%, rgba(107, 66, 38, 0.08) 0%, transparent 50%),
        radial-gradient(circle at 80% 20%, rgba(184, 69, 42, 0.06) 0%, transparent 40%);
    z-index: 1;
}

/* Heavy noise for grungy feel */
.heavy-noise {
    position: absolute; top: 0; left: 0; width: 100%; height: 100%;
    pointer-events: none; z-index: 8;
    opacity: 0.06;
}

/* Massive stacked type */
.band-name {
    position: absolute;
    top: 8%; left: 80px; right: 80px;
    z-index: 4;
}
.band-name h1 {
    font-family: 'EricaOne', sans-serif;
    font-size: 280px;
    color: var(--fg);
    line-height: 0.85;
    letter-spacing: -0.02em;
    text-transform: uppercase;
}

/* Supporting acts */
.support-acts {
    position: absolute;
    top: 45%; left: 80px;
    z-index: 4;
}
.support-acts .act {
    font-family: 'WorkSans', sans-serif;
    font-size: 42px; font-weight: 600;
    color: var(--accent);
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-bottom: 12px;
}
.support-acts .separator {
    font-family: 'WorkSans', sans-serif;
    font-size: 24px; color: var(--muted);
    margin: 0 16px;
}

/* Event details — bottom */
.details {
    position: absolute;
    bottom: 120px; left: 80px; right: 80px;
    border-top: 3px solid var(--fg);
    padding-top: 40px;
    display: flex; justify-content: space-between;
    z-index: 4;
}
.details .date {
    font-family: 'BigShoulders', sans-serif;
    font-size: 72px; font-weight: 700;
    color: var(--accent2);
    line-height: 1;
}
.details .venue-info {
    text-align: right;
}
.details .venue-name {
    font-family: 'WorkSans', sans-serif;
    font-size: 28px; font-weight: 600;
    color: var(--fg);
}
.details .venue-address {
    font-family: 'DMMono', monospace;
    font-size: 16px; color: var(--fg);
    opacity: 0.5; margin-top: 8px;
}

/* Decorative stamp / badge */
.stamp {
    position: absolute;
    top: 38%; right: 80px;
    width: 200px; height: 200px;
    border: 4px solid var(--accent2);
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    transform: rotate(12deg);
    z-index: 4;
}
.stamp-text {
    font-family: 'BigShoulders', sans-serif;
    font-size: 24px; font-weight: 700;
    color: var(--accent2);
    text-transform: uppercase;
    text-align: center;
    letter-spacing: 0.1em;
}
```

---

## Gallery / Art Poster

Minimal, vast whitespace, precise small type. The art speaks; the poster whispers.

```css
html, body { width: 2480px; height: 3508px; }

body {
    --bg: #FAF8F5;
    --fg: #2C2C2C;
    --accent: #6B6B6B;
    --muted: #E8E4DE;
    position: relative;
    background: var(--bg);
}

/* Central artwork area — 60% of canvas, centered */
.artwork-area {
    position: absolute;
    top: 12%; left: 15%; width: 70%; height: 50%;
    background: var(--muted);
    z-index: 2;
    /* Replace with actual artwork or generated pattern */
}

/* Exhibition title — precise, small, lower third */
.exhibition-info {
    position: absolute;
    bottom: 15%; left: 15%;
    z-index: 4;
}
.exhibition-info .artist {
    font-family: 'InstrumentSerif', serif;
    font-size: 48px; font-weight: 400;
    color: var(--fg);
    letter-spacing: -0.01em;
    margin-bottom: 12px;
}
.exhibition-info .title {
    font-family: 'InstrumentSerif', serif;
    font-size: 32px; font-weight: 400;
    font-style: italic;
    color: var(--accent);
    margin-bottom: 32px;
}
.exhibition-info .details {
    font-family: 'Outfit', sans-serif;
    font-size: 14px; color: var(--fg);
    opacity: 0.5;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    line-height: 2;
}

/* Gallery logo / branding — bottom right */
.gallery-mark {
    position: absolute;
    bottom: 15%; right: 15%;
    font-family: 'Outfit', sans-serif;
    font-size: 12px; color: var(--fg);
    opacity: 0.3;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    z-index: 4;
}

/* Subtle paper texture — very light */
.paper {
    position: absolute; top: 0; left: 0; width: 100%; height: 100%;
    pointer-events: none; z-index: 8;
    opacity: 0.02;
}
```
