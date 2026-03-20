# Billboard Design — CSS Recipes by Layout Type

Complete CSS patterns for outdoor advertising formats. Each recipe is tuned to extreme viewing distances, harsh lighting, and 3-second comprehension windows.

---

## 1. Classic Center

Giant headline centered on solid background. Logo anchored bottom-right. The most readable billboard format.

```css
html, body { width: 4800px; height: 1400px; }

body {
    --bg: #002855;
    --fg: #FFFFFF;
    --accent: #FFD700;
    --muted: #003A7A;
    position: relative;
    background: var(--bg);
}

/* Solid background — no gradient for maximum clarity */
.bg-solid {
    position: absolute; top: 0; left: 0; width: 100%; height: 100%;
    background: var(--bg);
    z-index: 1;
}

/* Centered headline — dominates the entire canvas */
.headline {
    position: absolute;
    top: 50%; left: 50%;
    transform: translate(-50%, -50%);
    text-align: center;
    z-index: 4;
}
.headline h1 {
    font-family: 'BigShoulders', sans-serif;
    font-size: 300px;
    font-weight: 700;
    color: var(--fg);
    line-height: 0.9;
    letter-spacing: -0.03em;
    text-transform: uppercase;
    white-space: nowrap;
}
.headline .sub {
    font-family: 'WorkSans', sans-serif;
    font-size: 72px;
    font-weight: 600;
    color: var(--accent);
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-top: 24px;
}

/* Logo — anchored bottom-right */
.logo {
    position: absolute;
    bottom: 80px; right: 120px;
    z-index: 4;
}
.logo img {
    height: 120px;
    width: auto;
}
.logo .brand-name {
    font-family: 'WorkSans', sans-serif;
    font-size: 48px;
    font-weight: 700;
    color: var(--fg);
    letter-spacing: 0.05em;
    text-transform: uppercase;
}
```

---

## 2. Image Left + Text Right

Hero image takes 60% left side, text block occupies 40% right. Strong directional flow.

```css
html, body { width: 4800px; height: 1400px; }

body {
    --bg: #1A1A1A;
    --fg: #F5F5F0;
    --accent: #E63B2E;
    --muted: #2A2A2A;
    position: relative;
    background: var(--bg);
}

/* Image zone — left 60% */
.image-zone {
    position: absolute;
    top: 0; left: 0;
    width: 60%; height: 100%;
    background: var(--muted);
    overflow: hidden;
    z-index: 2;
}
/* Gradient fade from image to text zone */
.image-fade {
    position: absolute;
    top: 0; right: 0;
    width: 300px; height: 100%;
    background: linear-gradient(90deg, transparent 0%, var(--bg) 100%);
    z-index: 3;
}

/* Text zone — right 40% */
.text-zone {
    position: absolute;
    top: 0; right: 0;
    width: 40%; height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: center;
    padding: 80px 120px 80px 60px;
    z-index: 4;
}
.text-zone h1 {
    font-family: 'BigShoulders', sans-serif;
    font-size: 200px;
    font-weight: 700;
    color: var(--fg);
    line-height: 0.9;
    letter-spacing: -0.03em;
    text-transform: uppercase;
}
.text-zone .cta {
    font-family: 'WorkSans', sans-serif;
    font-size: 56px;
    font-weight: 700;
    color: var(--accent);
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-top: 40px;
}

/* Logo mark — bottom-right corner */
.logo-mark {
    position: absolute;
    bottom: 60px; right: 120px;
    font-family: 'WorkSans', sans-serif;
    font-size: 36px;
    font-weight: 700;
    color: var(--fg);
    opacity: 0.6;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    z-index: 4;
}
```

---

## 3. Full-Bleed Text

Text fills the entire canvas. No image, no visual — pure typographic impact. Ultra-tight tracking, extreme scale.

```css
html, body { width: 4800px; height: 1400px; }

body {
    --bg: #000000;
    --fg: #FFFFFF;
    --accent: #FF3B30;
    position: relative;
    background: var(--bg);
}

/* Full-bleed headline — fills canvas */
.full-bleed-text {
    position: absolute;
    top: 0; left: 0; width: 100%; height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 40px 100px;
    z-index: 3;
}
.full-bleed-text h1 {
    font-family: 'Boldonse', sans-serif;
    font-size: 380px;
    color: var(--fg);
    line-height: 0.85;
    letter-spacing: -0.04em;
    text-transform: uppercase;
    text-align: center;
    /* Text should nearly touch top and bottom edges */
}

/* Accent word in different color */
.full-bleed-text .accent-word {
    color: var(--accent);
}

/* Tiny brand mark — bottom right, barely visible but present */
.brand {
    position: absolute;
    bottom: 40px; right: 80px;
    font-family: 'WorkSans', sans-serif;
    font-size: 32px;
    font-weight: 600;
    color: var(--fg);
    opacity: 0.4;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    z-index: 4;
}
```

---

## 4. Silhouette + Headline

Product silhouette or iconic shape with bold headline overlay. The silhouette creates recognition; the headline delivers the message.

```css
html, body { width: 4800px; height: 1400px; }

body {
    --bg: #FFFFFF;
    --fg: #1A1A1A;
    --accent: #E63B2E;
    --muted: #F0F0F0;
    position: relative;
    background: var(--bg);
}

/* Silhouette container — centered, large */
.silhouette {
    position: absolute;
    top: 50%; left: 35%;
    transform: translate(-50%, -50%);
    width: 900px; height: 900px;
    z-index: 2;
    /* Place product image or SVG silhouette here */
    opacity: 0.12;
}

/* Headline — overlapping the silhouette */
.headline-overlay {
    position: absolute;
    top: 50%; left: 50%;
    transform: translate(-30%, -50%);
    z-index: 4;
}
.headline-overlay h1 {
    font-family: 'BigShoulders', sans-serif;
    font-size: 260px;
    font-weight: 700;
    color: var(--fg);
    line-height: 0.9;
    letter-spacing: -0.02em;
    text-transform: uppercase;
}
.headline-overlay .tagline {
    font-family: 'WorkSans', sans-serif;
    font-size: 56px;
    font-weight: 600;
    color: var(--accent);
    letter-spacing: 0.06em;
    margin-top: 24px;
}

/* CTA — bottom right */
.cta {
    position: absolute;
    bottom: 80px; right: 120px;
    font-family: 'WorkSans', sans-serif;
    font-size: 48px;
    font-weight: 700;
    color: var(--fg);
    text-transform: uppercase;
    letter-spacing: 0.1em;
    z-index: 4;
}
```

---

## 5. Split Diagonal

Angled divide splits the billboard into two contrasting color zones. Creates energy and movement.

```css
html, body { width: 4800px; height: 1400px; }

body {
    --bg: #1A1A1A;
    --fg: #FFFFFF;
    --accent: #FFD700;
    --color-left: #E63B2E;
    --color-right: #1A1A1A;
    position: relative;
    background: var(--color-right);
}

/* Left diagonal zone */
.diagonal-left {
    position: absolute;
    top: 0; left: 0; width: 100%; height: 100%;
    clip-path: polygon(0 0, 58% 0, 42% 100%, 0 100%);
    background: var(--color-left);
    z-index: 2;
}

/* Headline — positioned at the diagonal collision point */
.headline {
    position: absolute;
    top: 50%; left: 50%;
    transform: translate(-50%, -50%);
    text-align: center;
    z-index: 4;
}
.headline h1 {
    font-family: 'BigShoulders', sans-serif;
    font-size: 240px;
    font-weight: 700;
    color: var(--fg);
    line-height: 0.9;
    letter-spacing: -0.02em;
    text-transform: uppercase;
    text-shadow: 4px 4px 0 rgba(0, 0, 0, 0.2);
}

/* Left zone text */
.left-text {
    position: absolute;
    top: 50%; left: 120px;
    transform: translateY(-50%);
    z-index: 4;
}
.left-text .label {
    font-family: 'WorkSans', sans-serif;
    font-size: 64px;
    font-weight: 700;
    color: var(--fg);
    text-transform: uppercase;
    letter-spacing: 0.1em;
}

/* Right zone CTA */
.right-cta {
    position: absolute;
    top: 50%; right: 120px;
    transform: translateY(-50%);
    text-align: right;
    z-index: 4;
}
.right-cta .action {
    font-family: 'WorkSans', sans-serif;
    font-size: 72px;
    font-weight: 700;
    color: var(--accent);
    text-transform: uppercase;
    letter-spacing: 0.08em;
}
.right-cta .url {
    font-family: 'WorkSans', sans-serif;
    font-size: 42px;
    font-weight: 600;
    color: var(--fg);
    opacity: 0.6;
    margin-top: 16px;
    letter-spacing: 0.05em;
}
```

---

## 6. Minimal Logo Focus

Oversized logo or brand mark dominates the canvas. Tagline only — no headline needed when the brand IS the message.

```css
html, body { width: 4800px; height: 1400px; }

body {
    --bg: #0C0C0F;
    --fg: #FFFFFF;
    --accent: #00E5FF;
    --muted: #1A1A24;
    position: relative;
    background: var(--bg);
}

/* Subtle background gradient — very minimal */
.bg-glow {
    position: absolute; top: 0; left: 0; width: 100%; height: 100%;
    background: radial-gradient(ellipse 60% 80% at 50% 50%, var(--muted) 0%, var(--bg) 70%);
    z-index: 1;
}

/* Oversized logo — centered, dominant */
.logo-giant {
    position: absolute;
    top: 50%; left: 50%;
    transform: translate(-50%, -55%);
    z-index: 4;
    text-align: center;
}
.logo-giant .mark {
    font-family: 'Boldonse', sans-serif;
    font-size: 400px;
    color: var(--fg);
    line-height: 0.85;
    letter-spacing: -0.02em;
}

/* Tagline — centered below logo */
.tagline {
    position: absolute;
    bottom: 180px; left: 50%;
    transform: translateX(-50%);
    z-index: 4;
}
.tagline p {
    font-family: 'WorkSans', sans-serif;
    font-size: 56px;
    font-weight: 500;
    color: var(--fg);
    opacity: 0.6;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    text-align: center;
    white-space: nowrap;
}

/* Accent underline — subtle brand color */
.accent-line {
    position: absolute;
    bottom: 140px; left: 50%;
    transform: translateX(-50%);
    width: 200px; height: 4px;
    background: var(--accent);
    z-index: 4;
}
```

---

## Bus Shelter Layout (Vertical)

Bus shelters are pedestrian-viewed — closer distance, more time, vertical format.

```css
html, body { width: 1380px; height: 2010px; }

body {
    --bg: #F5F0E8;
    --fg: #1A1410;
    --accent: #D43D51;
    --muted: #E0D8CC;
    position: relative;
    background: var(--bg);
}

/* Top visual zone — 50% */
.visual-zone {
    position: absolute;
    top: 0; left: 0; width: 100%; height: 50%;
    background: var(--muted);
    overflow: hidden;
    z-index: 2;
}

/* Headline — centered in lower half */
.headline {
    position: absolute;
    top: 55%; left: 80px; right: 80px;
    z-index: 4;
}
.headline h1 {
    font-family: 'BigShoulders', sans-serif;
    font-size: 120px;
    font-weight: 700;
    color: var(--fg);
    line-height: 0.95;
    letter-spacing: -0.02em;
    text-transform: uppercase;
}
.headline p {
    font-family: 'WorkSans', sans-serif;
    font-size: 32px;
    color: var(--fg);
    opacity: 0.6;
    margin-top: 24px;
    line-height: 1.4;
}

/* CTA — bottom zone, above frame */
.cta-zone {
    position: absolute;
    bottom: 120px; left: 80px; right: 80px;
    z-index: 4;
}
.cta-zone .action {
    display: inline-block;
    font-family: 'WorkSans', sans-serif;
    font-size: 36px;
    font-weight: 700;
    color: var(--bg);
    background: var(--accent);
    padding: 20px 48px;
    text-transform: uppercase;
    letter-spacing: 0.08em;
}
.cta-zone .brand {
    font-family: 'WorkSans', sans-serif;
    font-size: 24px;
    font-weight: 600;
    color: var(--fg);
    opacity: 0.5;
    margin-top: 24px;
    letter-spacing: 0.1em;
    text-transform: uppercase;
}
```
