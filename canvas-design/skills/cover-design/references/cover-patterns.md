# Cover Design — Platform-Specific CSS Recipes

Complete CSS patterns optimized for each cover platform. Each recipe includes background, typography, and layout tuned for the platform's dimensions and constraints.

---

## GitHub Repository Cover (1280 x 640)

Dark developer aesthetic with code-inspired elements and monospace accents.

```css
/* Dimensions */
html, body { width: 1280px; height: 640px; }

/* Color scheme — developer dark */
body {
    --bg: #0D1117;
    --fg: #E6EDF3;
    --accent: #58A6FF;
    --accent2: #3FB950;
    --muted: #161B22;
    --highlight: #F0883E;
    position: relative;
    background: var(--bg);
}

/* Code-grid background */
.code-grid {
    position: absolute; top: 0; left: 0; width: 100%; height: 100%;
    background:
        repeating-linear-gradient(
            0deg,
            rgba(88, 166, 255, 0.02) 0px,
            rgba(88, 166, 255, 0.02) 1px,
            transparent 1px,
            transparent 32px
        ),
        repeating-linear-gradient(
            90deg,
            rgba(88, 166, 255, 0.02) 0px,
            rgba(88, 166, 255, 0.02) 1px,
            transparent 1px,
            transparent 32px
        );
    mask-image: radial-gradient(ellipse 80% 80% at 50% 50%, black 20%, transparent 70%);
    -webkit-mask-image: radial-gradient(ellipse 80% 80% at 50% 50%, black 20%, transparent 70%);
    z-index: 1;
}

/* Accent glow */
.glow {
    position: absolute;
    width: 400px; height: 400px;
    border-radius: 50%;
    filter: blur(120px);
    opacity: 0.15;
    z-index: 1;
}
.glow-1 { background: var(--accent); top: -100px; left: 20%; }
.glow-2 { background: var(--accent2); bottom: -80px; right: 25%; }

/* Content */
.content {
    position: absolute; top: 0; left: 0; width: 100%; height: 100%;
    display: flex; align-items: center; justify-content: center;
    flex-direction: column; gap: 16px;
    z-index: 3;
}
.title {
    font-family: 'BigShoulders', sans-serif;
    font-size: 64px; font-weight: 700;
    color: var(--fg);
    letter-spacing: 0.02em;
}
.tagline {
    font-family: 'JetBrainsMono', monospace;
    font-size: 18px; color: var(--accent);
    letter-spacing: 0.02em; opacity: 0.8;
}

/* Terminal-style decorative element */
.terminal-bar {
    position: absolute; bottom: 60px; left: 60px; right: 60px;
    height: 36px; background: var(--muted);
    border-radius: 6px; border: 1px solid rgba(255,255,255,0.06);
    display: flex; align-items: center; padding: 0 16px;
    z-index: 3;
}
.terminal-dots {
    display: flex; gap: 6px;
}
.terminal-dot {
    width: 10px; height: 10px; border-radius: 50%;
    background: rgba(255,255,255,0.15);
}
.terminal-text {
    font-family: 'JetBrainsMono', monospace;
    font-size: 12px; color: var(--accent2);
    margin-left: 16px; opacity: 0.5;
}
```

---

## Notion Cover (1500 x 600)

Clean, modern, glassmorphism-friendly. Avoid bottom 120px left half (title overlay area).

```css
html, body { width: 1500px; height: 600px; }

body {
    --bg: #FAF8F5;
    --fg: #2C2C2C;
    --accent: #6B6B6B;
    --accent2: #A0937D;
    --muted: #E8E4DE;
    --highlight: #C4A35A;
    position: relative;
    background: var(--bg);
}

/* Subtle mesh background */
.mesh {
    position: absolute; top: 0; left: 0; width: 100%; height: 100%;
    background:
        radial-gradient(ellipse at 30% 40%, rgba(192, 163, 90, 0.08) 0%, transparent 50%),
        radial-gradient(ellipse at 75% 30%, rgba(160, 147, 125, 0.06) 0%, transparent 50%),
        var(--bg);
    z-index: 1;
}

/* Glass cards floating */
.glass-card {
    position: absolute;
    background: rgba(255, 255, 255, 0.6);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border: 1px solid rgba(0, 0, 0, 0.06);
    border-radius: 12px;
    z-index: 3;
}
.card-1 {
    width: 280px; height: 180px;
    top: 80px; left: 60%;
    transform: rotate(-2deg);
    padding: 24px;
}
.card-2 {
    width: 220px; height: 140px;
    top: 160px; left: 78%;
    transform: rotate(3deg);
    padding: 20px;
}

/* Title area — upper left, above the Notion title overlay zone */
.heading-area {
    position: absolute;
    top: 80px; left: 80px;
    z-index: 3;
}
.heading-area h1 {
    font-family: 'InstrumentSerif', serif;
    font-size: 56px; font-weight: 400;
    color: var(--fg); line-height: 1.15;
    letter-spacing: -0.02em;
}
.heading-area .sub {
    font-family: 'Outfit', sans-serif;
    font-size: 16px; color: var(--accent);
    margin-top: 12px; letter-spacing: 0.05em;
}

/* Thin horizontal rule */
.rule {
    position: absolute;
    top: 50%; left: 80px; right: 80px;
    height: 1px;
    background: linear-gradient(90deg, var(--muted), transparent);
    z-index: 2;
}
```

---

## LinkedIn Personal Banner (1584 x 396)

Professional warmth. Left 260px is a dead zone (profile photo). Content flows center-right.

```css
html, body { width: 1584px; height: 396px; }

body {
    --bg: #1A2332;
    --fg: #E0EAF0;
    --accent: #4A90D9;
    --accent2: #E8B4B8;
    --muted: #C8D6E0;
    position: relative;
    background: var(--bg);
}

/* Gradient accent on the right */
.gradient-right {
    position: absolute; top: 0; right: 0;
    width: 50%; height: 100%;
    background: linear-gradient(135deg, transparent 0%, rgba(74, 144, 217, 0.08) 100%);
    z-index: 1;
}

/* Content — offset right to avoid profile photo zone */
.content {
    position: absolute;
    top: 0; left: 300px; right: 60px; height: 100%;
    display: flex; align-items: center; gap: 60px;
    z-index: 3;
}
.text-block {
    flex: 1;
}
.text-block h1 {
    font-family: 'BricolageGrotesque', sans-serif;
    font-size: 42px; font-weight: 700;
    color: var(--fg);
    letter-spacing: -0.02em; line-height: 1.2;
}
.text-block p {
    font-family: 'IBMPlexMono', monospace;
    font-size: 14px; color: var(--muted);
    margin-top: 12px; letter-spacing: 0.02em;
}

/* Decorative dots pattern — right side */
.dots-pattern {
    flex-shrink: 0; width: 200px; height: 200px;
    display: grid;
    grid-template-columns: repeat(8, 1fr);
    grid-template-rows: repeat(8, 1fr);
    gap: 12px;
    opacity: 0.15;
}
.dot {
    width: 6px; height: 6px;
    border-radius: 50%;
    background: var(--accent);
    align-self: center; justify-self: center;
}

/* Grid lines */
.grid-lines {
    position: absolute; top: 0; left: 0; width: 100%; height: 100%;
    background: repeating-linear-gradient(
        90deg, rgba(255,255,255,0.02) 0px, rgba(255,255,255,0.02) 1px,
        transparent 1px, transparent 100px
    );
    z-index: 1;
}
```

---

## YouTube Channel Banner (2560 x 1440)

Safe area is 1546x423, centered. Bold, vibrant, high-contrast. Design safe area first, extend background.

```css
html, body { width: 2560px; height: 1440px; }

body {
    --bg: #121212;
    --fg: #F5F5F0;
    --accent: #E63B2E;
    --accent2: #2B5CE6;
    --muted: #2A2A2A;
    --highlight: #F5C518;
    position: relative;
    background: var(--bg);
}

/* Full-bleed atmospheric background */
.atmosphere {
    position: absolute; top: 0; left: 0; width: 100%; height: 100%;
    background:
        radial-gradient(ellipse at 40% 50%, rgba(230, 59, 46, 0.1) 0%, transparent 50%),
        radial-gradient(ellipse at 65% 45%, rgba(43, 92, 230, 0.08) 0%, transparent 50%),
        var(--bg);
    z-index: 1;
}

/* Safe area container — centered 1546x423 */
.safe-area {
    position: absolute;
    top: 50%; left: 50%;
    transform: translate(-50%, -50%);
    width: 1546px; height: 423px;
    display: flex; align-items: center; justify-content: center;
    z-index: 3;
}
.safe-content {
    display: flex; align-items: center; gap: 60px;
    padding: 40px;
}
.channel-title {
    font-family: 'Boldonse', sans-serif;
    font-size: 80px; font-weight: 400;
    color: var(--fg);
    line-height: 1;
    letter-spacing: -0.01em;
}
.channel-tagline {
    font-family: 'WorkSans', sans-serif;
    font-size: 22px; color: var(--fg);
    opacity: 0.6; margin-top: 16px;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}

/* Accent slash */
.accent-slash {
    width: 6px; height: 200px;
    background: var(--accent);
    transform: skewX(-12deg);
    flex-shrink: 0;
}

/* Extended decorative elements beyond safe area */
.deco-bar-top {
    position: absolute; top: 0; left: 0; width: 100%; height: 6px;
    background: linear-gradient(90deg, var(--accent), var(--highlight), var(--accent2));
    z-index: 2;
}
```

---

## Twitter/X Header (1500 x 500)

Avoid left 200px (profile photo). High contrast, bold shapes that survive JPEG compression.

```css
html, body { width: 1500px; height: 500px; }

body {
    --bg: #0C0C0F;
    --fg: #E8ECF0;
    --accent: #00E5FF;
    --accent2: #FF2D78;
    --muted: #1A1A24;
    position: relative;
    background: var(--bg);
}

/* Diagonal color block */
.diagonal-block {
    position: absolute; top: 0; left: 0; width: 100%; height: 100%;
    clip-path: polygon(40% 0, 100% 0, 100% 100%, 55% 100%);
    background: linear-gradient(180deg, var(--muted) 0%, rgba(0, 229, 255, 0.05) 100%);
    z-index: 1;
}

/* Content — shifted right to avoid profile photo */
.content {
    position: absolute;
    top: 0; left: 240px; right: 60px; height: 100%;
    display: flex; align-items: center;
    z-index: 3;
}
.title {
    font-family: 'BigShoulders', sans-serif;
    font-size: 72px; font-weight: 700;
    color: var(--fg);
    letter-spacing: 0.02em; line-height: 1.1;
}
.accent-underline {
    width: 120px; height: 4px;
    background: var(--accent);
    margin-top: 16px;
}
.subtitle {
    font-family: 'GeistMono', monospace;
    font-size: 16px; color: var(--accent);
    margin-top: 12px; opacity: 0.7;
}

/* Floating accent shapes */
.shape-ring {
    position: absolute;
    width: 250px; height: 250px;
    border: 2px solid var(--accent);
    border-radius: 50%;
    opacity: 0.08;
    right: 10%; top: 50%;
    transform: translateY(-50%);
    z-index: 2;
}
.shape-dot {
    position: absolute;
    width: 12px; height: 12px;
    border-radius: 50%;
    background: var(--accent2);
    opacity: 0.4;
    right: 20%; top: 30%;
    z-index: 2;
}
```
