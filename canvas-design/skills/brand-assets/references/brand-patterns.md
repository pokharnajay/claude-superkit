# Brand Assets — CSS Recipes

Complete CSS patterns for different brand asset types. Each recipe is ready to render via the Playwright pipeline.

---

## Lettermark

Single letter in a geometric frame. The most common logo pattern — a distinctive initial in a shape.

```css
html, body { width: 512px; height: 512px; }

body {
    --bg: #FAF8F5;
    --fg: #2C2C2C;
    --accent: #E8622B;
    position: relative;
    background: var(--bg);
    display: flex;
    align-items: center;
    justify-content: center;
}

/* Geometric frame — circle */
.frame {
    width: 380px;
    height: 380px;
    border-radius: 50%;
    background: var(--fg);
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
}

/* Letter */
.letter {
    font-family: 'InstrumentSerif', serif;
    font-size: 220px;
    font-weight: 400;
    color: var(--bg);
    line-height: 1;
    /* Optical adjustment — letters rarely center perfectly */
    margin-top: -10px;
    margin-left: 5px;
}

/* Accent ring */
.accent-ring {
    position: absolute;
    top: 50%; left: 50%;
    transform: translate(-50%, -50%);
    width: 420px;
    height: 420px;
    border-radius: 50%;
    border: 2px solid var(--accent);
    opacity: 0.3;
}
```

### Lettermark Variant: Square Frame

```css
.frame-square {
    width: 360px;
    height: 360px;
    border-radius: 24px;
    background: var(--accent);
    display: flex;
    align-items: center;
    justify-content: center;
}
.letter-square {
    font-family: 'BigShoulders', sans-serif;
    font-size: 240px;
    font-weight: 700;
    color: #FFFFFF;
    line-height: 1;
}
```

### Lettermark Variant: Outlined

```css
.frame-outlined {
    width: 380px;
    height: 380px;
    border-radius: 50%;
    border: 4px solid var(--fg);
    background: transparent;
    display: flex;
    align-items: center;
    justify-content: center;
}
.letter-outlined {
    font-family: 'YoungSerif', serif;
    font-size: 200px;
    color: var(--fg);
    line-height: 1;
}
```

---

## Wordmark

Styled text-only logo. Typography does all the heavy lifting.

```css
html, body { width: 800px; height: 200px; }

body {
    --bg: #FFFFFF;
    --fg: #1A1410;
    --accent: #E8622B;
    position: relative;
    background: var(--bg);
    display: flex;
    align-items: center;
    justify-content: center;
}

/* Wordmark text */
.wordmark {
    font-family: 'BricolageGrotesque', sans-serif;
    font-size: 72px;
    font-weight: 700;
    color: var(--fg);
    letter-spacing: -0.03em;
    position: relative;
}

/* Accent on a specific letter or dot */
.wordmark .accent-char {
    color: var(--accent);
}

/* Subtle underline accent */
.wordmark::after {
    content: '';
    position: absolute;
    bottom: -4px;
    left: 0;
    width: 30%;
    height: 3px;
    background: var(--accent);
    border-radius: 2px;
}
```

### Wordmark Variant: Spaced Caps

```css
.wordmark-caps {
    font-family: 'Outfit', sans-serif;
    font-size: 48px;
    font-weight: 700;
    color: var(--fg);
    text-transform: uppercase;
    letter-spacing: 0.15em;
}
```

### Wordmark Variant: Serif Elegant

```css
.wordmark-serif {
    font-family: 'InstrumentSerif', serif;
    font-size: 80px;
    font-weight: 400;
    color: var(--fg);
    letter-spacing: -0.02em;
    font-style: italic;
}
```

---

## Icon Mark

Geometric symbol built from CSS shapes. No text — pure visual identity.

```css
html, body { width: 512px; height: 512px; }

body {
    --bg: transparent;
    --primary: #1B4D72;
    --secondary: #5C8DAD;
    position: relative;
    background: var(--bg);
    display: flex;
    align-items: center;
    justify-content: center;
}

/* Overlapping circles pattern */
.mark {
    position: relative;
    width: 300px;
    height: 300px;
}
.circle-a {
    position: absolute;
    width: 200px;
    height: 200px;
    border-radius: 50%;
    background: var(--primary);
    top: 0;
    left: 50px;
}
.circle-b {
    position: absolute;
    width: 200px;
    height: 200px;
    border-radius: 50%;
    background: var(--secondary);
    bottom: 0;
    left: 0;
    mix-blend-mode: multiply;
}
.circle-c {
    position: absolute;
    width: 200px;
    height: 200px;
    border-radius: 50%;
    background: var(--secondary);
    bottom: 0;
    right: 0;
    opacity: 0.6;
    mix-blend-mode: multiply;
}
```

### Icon Mark Variant: Polygon

```css
.polygon-mark {
    width: 300px;
    height: 300px;
    background: var(--primary);
    clip-path: polygon(50% 0%, 100% 38%, 82% 100%, 18% 100%, 0% 38%);
    /* Pentagon shape */
}
```

### Icon Mark Variant: Stacked Bars

```css
.bar-mark {
    display: flex;
    flex-direction: column;
    gap: 12px;
    align-items: flex-start;
}
.bar {
    height: 24px;
    border-radius: 12px;
    background: var(--primary);
}
.bar-1 { width: 200px; }
.bar-2 { width: 280px; opacity: 0.7; }
.bar-3 { width: 160px; opacity: 0.4; }
```

---

## App Icon

Rounded square with centered symbol. Designed for iOS/Android app stores.

```css
html, body { width: 1024px; height: 1024px; }

body {
    --bg: #0D1117;
    --fg: #E6EDF3;
    --accent: #58A6FF;
    position: relative;
    background: transparent;
    display: flex;
    align-items: center;
    justify-content: center;
}

/* Icon container — squircle */
.icon-container {
    width: 1024px;
    height: 1024px;
    border-radius: 227px; /* iOS squircle: ~22.17% */
    background: var(--bg);
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
    overflow: hidden;
}

/* Subtle gradient background */
.icon-bg {
    position: absolute;
    top: 0; left: 0; width: 100%; height: 100%;
    background:
        radial-gradient(circle at 30% 30%, rgba(88, 166, 255, 0.15) 0%, transparent 50%),
        var(--bg);
}

/* Central mark — kept within 60% of icon size */
.icon-mark {
    width: 480px;
    height: 480px;
    position: relative;
    z-index: 2;
    display: flex;
    align-items: center;
    justify-content: center;
}

/* Example: angular bracket mark for a code-related app */
.bracket-left, .bracket-right {
    font-family: 'JetBrainsMono', monospace;
    font-size: 280px;
    font-weight: 700;
    color: var(--accent);
    line-height: 1;
}
.bracket-left { margin-right: -30px; }
.bracket-right { margin-left: -30px; }
.bracket-dot {
    width: 32px;
    height: 32px;
    border-radius: 50%;
    background: var(--fg);
}

/* Subtle noise */
.icon-noise {
    position: absolute;
    top: 0; left: 0; width: 100%; height: 100%;
    pointer-events: none;
    z-index: 10;
    opacity: 0.02;
    border-radius: 227px;
    overflow: hidden;
}
```

---

## Favicon

Ultra-simple at 16x16. Design at 512x512 with extreme simplicity.

```css
html, body { width: 512px; height: 512px; }

body {
    --bg: transparent;
    --primary: #E8622B;
    position: relative;
    background: var(--bg);
    display: flex;
    align-items: center;
    justify-content: center;
}

/* Option 1: Single bold letter */
.favicon-letter {
    font-family: 'BigShoulders', sans-serif;
    font-size: 400px;
    font-weight: 700;
    color: var(--primary);
    line-height: 1;
}

/* Option 2: Simple geometric shape */
.favicon-shape {
    width: 400px;
    height: 400px;
    background: var(--primary);
    border-radius: 80px;
    /* At 16px, details vanish. Keep it bold and simple. */
}

/* Option 3: Circle with initial */
.favicon-circle {
    width: 420px;
    height: 420px;
    border-radius: 50%;
    background: var(--primary);
    display: flex;
    align-items: center;
    justify-content: center;
}
.favicon-circle .init {
    font-family: 'Outfit', sans-serif;
    font-size: 280px;
    font-weight: 700;
    color: #FFFFFF;
    line-height: 1;
    margin-top: -10px;
}
```

**Testing:** After rendering at 512x512, resize the PNG to 32x32 and 16x16 using PIL nearest-neighbor or bilinear scaling. If the mark is not instantly recognizable at 16x16, simplify further.
