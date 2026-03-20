# Thumbnail Design — CSS Recipes

Platform-specific CSS patterns for YouTube thumbnails and Open Graph images. Each recipe prioritizes readability at small preview sizes.

---

## YouTube Coding Tutorial Thumbnail

Dark background, code snippet preview, bold number or keyword. Developer audience.

```css
html, body { width: 1280px; height: 720px; }

body {
    --bg: #0D1117;
    --fg: #E6EDF3;
    --accent: #58A6FF;
    --accent2: #3FB950;
    --highlight: #F0883E;
    position: relative;
    background: var(--bg);
}

/* Code snippet preview — left side */
.code-preview {
    position: absolute;
    top: 60px; left: 60px; bottom: 60px;
    width: 45%;
    background: #161B22;
    border-radius: 12px;
    border: 1px solid rgba(255, 255, 255, 0.06);
    padding: 30px;
    overflow: hidden;
    z-index: 2;
}
.code-line {
    font-family: 'JetBrainsMono', monospace;
    font-size: 18px;
    color: var(--fg);
    opacity: 0.6;
    line-height: 2;
    white-space: nowrap;
}
.code-line .keyword { color: var(--accent); opacity: 1; }
.code-line .string { color: var(--accent2); opacity: 1; }
.code-line .number { color: var(--highlight); opacity: 1; }

/* Fade mask on code */
.code-preview::after {
    content: '';
    position: absolute;
    bottom: 0; left: 0; width: 100%; height: 40%;
    background: linear-gradient(to bottom, transparent, #161B22);
}

/* Bold text — right side */
.thumb-content {
    position: absolute;
    top: 0; right: 0; width: 50%; height: 100%;
    display: flex; flex-direction: column;
    align-items: flex-start; justify-content: center;
    padding: 60px 60px 60px 40px;
    z-index: 3;
}
.thumb-number {
    font-family: 'BigShoulders', sans-serif;
    font-size: 160px; font-weight: 700;
    color: var(--accent);
    line-height: 0.9;
    letter-spacing: -0.02em;
}
.thumb-keyword {
    font-family: 'BigShoulders', sans-serif;
    font-size: 64px; font-weight: 700;
    color: var(--fg);
    text-transform: uppercase;
    letter-spacing: 0.02em;
    line-height: 1.1;
    text-shadow:
        0 2px 8px rgba(0, 0, 0, 0.8),
        2px 2px 0 rgba(0, 0, 0, 0.5);
}
.thumb-sub {
    font-family: 'GeistMono', monospace;
    font-size: 18px; color: var(--accent);
    margin-top: 12px; opacity: 0.7;
}

/* Glow accent */
.glow {
    position: absolute;
    width: 300px; height: 300px;
    border-radius: 50%;
    background: var(--accent);
    filter: blur(120px);
    opacity: 0.08;
    top: 30%; right: 10%;
    z-index: 1;
}

.noise { position: absolute; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; z-index: 10; opacity: 0.03; }
```

---

## YouTube Vlog / General Thumbnail

Split composition: face/visual placeholder on one side, vibrant accent and bold text on the other.

```css
html, body { width: 1280px; height: 720px; }

body {
    --bg: #121212;
    --fg: #FFFFFF;
    --accent: #E63B2E;
    --accent2: #F5C518;
    position: relative;
    background: var(--bg);
}

/* Split: left visual area, right text area */
.visual-area {
    position: absolute;
    top: 0; left: 0; width: 55%; height: 100%;
    background: linear-gradient(135deg, var(--bg) 0%, #2A2A2A 100%);
    z-index: 1;
    overflow: hidden;
}
/* Placeholder for face/image — use a gradient orb to suggest presence */
.face-placeholder {
    position: absolute;
    width: 400px; height: 400px;
    border-radius: 50%;
    background: radial-gradient(circle, #333 0%, transparent 70%);
    top: 50%; left: 50%;
    transform: translate(-50%, -50%);
}

/* Text area — right side with accent background */
.text-area {
    position: absolute;
    top: 0; right: 0; width: 50%; height: 100%;
    display: flex; flex-direction: column;
    align-items: flex-start; justify-content: center;
    padding: 60px;
    z-index: 3;
}

/* Accent background strip */
.accent-strip {
    position: absolute;
    top: 0; right: 0; width: 45%; height: 100%;
    background: var(--accent);
    clip-path: polygon(15% 0, 100% 0, 100% 100%, 0 100%);
    z-index: 2;
}

.thumb-title {
    font-family: 'Boldonse', sans-serif;
    font-size: 88px;
    color: var(--fg);
    line-height: 1;
    text-shadow:
        3px 3px 0 rgba(0, 0, 0, 0.5),
        0 4px 12px rgba(0, 0, 0, 0.4);
    z-index: 3;
    position: relative;
}
.thumb-accent-word {
    color: var(--accent2);
}

/* Expression emoji/reaction indicator */
.reaction-badge {
    position: absolute;
    top: 30px; right: 30px;
    background: var(--accent2);
    border-radius: 50%;
    width: 80px; height: 80px;
    display: flex; align-items: center; justify-content: center;
    z-index: 4;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3);
}
.reaction-badge span {
    font-family: 'BigShoulders', sans-serif;
    font-size: 32px; font-weight: 700;
    color: var(--bg);
}
```

---

## Open Graph (OG) Image

Logo + title + description in a clean professional layout. Must work as link preview across platforms.

```css
html, body { width: 1200px; height: 630px; }

body {
    --bg: #FAFCFE;
    --fg: #0D1B2A;
    --accent: #1B4D72;
    --accent2: #5C8DAD;
    --muted: #D4E2ED;
    position: relative;
    background: var(--bg);
}

/* Left accent bar */
.accent-bar {
    position: absolute;
    top: 0; left: 0;
    width: 8px; height: 100%;
    background: linear-gradient(180deg, var(--accent), var(--accent2));
    z-index: 3;
}

/* Content layout */
.og-content {
    position: absolute;
    top: 0; left: 0; width: 100%; height: 100%;
    display: flex; flex-direction: column;
    justify-content: center;
    padding: 60px 80px 60px 60px;
    z-index: 3;
}

/* Logo area */
.logo-area {
    display: flex; align-items: center; gap: 12px;
    margin-bottom: 32px;
}
.logo-mark {
    width: 36px; height: 36px;
    background: var(--accent);
    border-radius: 8px;
}
.logo-text {
    font-family: 'BricolageGrotesque', sans-serif;
    font-size: 16px; font-weight: 700;
    color: var(--fg); letter-spacing: 0.02em;
}

/* Title */
.og-title {
    font-family: 'BricolageGrotesque', sans-serif;
    font-size: 48px; font-weight: 700;
    color: var(--fg);
    line-height: 1.2; letter-spacing: -0.02em;
    max-width: 700px;
}

/* Description */
.og-description {
    font-family: 'Outfit', sans-serif;
    font-size: 20px; color: var(--fg);
    opacity: 0.5; margin-top: 16px;
    line-height: 1.5; max-width: 600px;
}

/* URL hint */
.og-url {
    font-family: 'GeistMono', monospace;
    font-size: 14px; color: var(--accent2);
    margin-top: 24px; opacity: 0.6;
}

/* Right decorative area */
.og-visual {
    position: absolute;
    top: 0; right: 0; width: 30%; height: 100%;
    background:
        radial-gradient(ellipse at 70% 50%, rgba(27, 77, 114, 0.06) 0%, transparent 60%),
        var(--bg);
    z-index: 1;
}
.og-pattern {
    position: absolute;
    top: 0; right: 0; width: 30%; height: 100%;
    background:
        repeating-linear-gradient(
            45deg,
            rgba(27, 77, 114, 0.03) 0px,
            rgba(27, 77, 114, 0.03) 1px,
            transparent 1px,
            transparent 20px
        );
    z-index: 2;
}

/* Bottom border */
.og-bottom-border {
    position: absolute;
    bottom: 0; left: 0; width: 100%; height: 4px;
    background: linear-gradient(90deg, var(--accent), var(--accent2), transparent);
    z-index: 3;
}
```
