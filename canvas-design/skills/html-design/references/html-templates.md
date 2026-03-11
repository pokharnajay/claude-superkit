# HTML Templates Reference

Starter templates for common design layouts. Each template is a complete, working HTML document ready to customize. Replace placeholder values (WIDTH, HEIGHT, colors, fonts, content) with your specification values.

All templates include: @font-face placeholder, fixed canvas dimensions, box-sizing reset, overflow hidden, layered z-index structure.

---

## Template 1: Full-Bleed Gradient Background with Centered Content

Best for: simple statements, quote cards, announcement graphics.

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<style>
    @font-face {
        font-family: 'DisplayFont';
        src: url('FONT_URL_DISPLAY') format('truetype');
        font-weight: 700; font-style: normal;
    }
    @font-face {
        font-family: 'BodyFont';
        src: url('FONT_URL_BODY') format('truetype');
        font-weight: 400; font-style: normal;
    }
    *, *::before, *::after { margin: 0; padding: 0; box-sizing: border-box; }
    html, body { width: 1080px; height: 1080px; overflow: hidden; -webkit-font-smoothing: antialiased; }

    body {
        position: relative;
        background: linear-gradient(155deg, var(--bg) 0%, var(--muted) 50%, var(--bg) 100%);
        --bg: #1C1210;
        --fg: #F5E6D3;
        --accent: #E8622B;
        --muted: #3D2B24;
    }

    /* Atmosphere layer */
    .orb {
        position: absolute;
        border-radius: 50%;
        filter: blur(100px);
        opacity: 0.4;
        pointer-events: none;
    }
    .orb-1 { width: 600px; height: 600px; background: var(--accent); top: -200px; right: -200px; }
    .orb-2 { width: 400px; height: 400px; background: var(--muted); bottom: -100px; left: -100px; }

    /* Content */
    .content {
        position: absolute;
        top: 0; left: 0; width: 100%; height: 100%;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 80px;
        z-index: 2;
    }
    .heading {
        font-family: 'DisplayFont', serif;
        font-size: 72px;
        font-weight: 700;
        color: var(--fg);
        text-align: center;
        line-height: 1.1;
        letter-spacing: -0.02em;
        margin-bottom: 24px;
    }
    .subtitle {
        font-family: 'BodyFont', sans-serif;
        font-size: 24px;
        color: var(--fg);
        opacity: 0.7;
        text-align: center;
        letter-spacing: 0.08em;
        text-transform: uppercase;
    }

    /* Noise overlay */
    .noise {
        position: absolute;
        top: 0; left: 0; width: 100%; height: 100%;
        pointer-events: none;
        z-index: 10;
        opacity: 0.035;
    }
</style>
</head>
<body>
    <div class="orb orb-1"></div>
    <div class="orb orb-2"></div>
    <div class="content">
        <div class="heading">Your Headline Here</div>
        <div class="subtitle">Supporting text goes here</div>
    </div>
    <div class="noise">
        <svg width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
            <filter id="n"><feTurbulence type="fractalNoise" baseFrequency="0.65" numOctaves="4" stitchTiles="stitch"/><feColorMatrix type="saturate" values="0"/></filter>
            <rect width="100%" height="100%" filter="url(#n)"/>
        </svg>
    </div>
</body>
</html>
```

---

## Template 2: Split Layout (Golden Ratio 62/38)

Best for: cover images, feature announcements, editorial layouts.

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<style>
    @font-face {
        font-family: 'DisplayFont';
        src: url('FONT_URL_DISPLAY') format('truetype');
        font-weight: 700; font-style: normal;
    }
    @font-face {
        font-family: 'BodyFont';
        src: url('FONT_URL_BODY') format('truetype');
        font-weight: 400; font-style: normal;
    }
    *, *::before, *::after { margin: 0; padding: 0; box-sizing: border-box; }
    html, body { width: 1280px; height: 640px; overflow: hidden; -webkit-font-smoothing: antialiased; }

    body {
        position: relative;
        display: flex;
        --bg: #0A1628;
        --fg: #E0EAF0;
        --accent: #00D4AA;
        --accent2: #2E7D9B;
        --muted: #1A2D4A;
    }

    /* Left panel — 62% */
    .panel-left {
        width: 62%;
        height: 100%;
        background: var(--bg);
        display: flex;
        flex-direction: column;
        justify-content: center;
        padding: 60px 80px;
        position: relative;
    }
    .heading {
        font-family: 'DisplayFont', serif;
        font-size: 56px;
        font-weight: 700;
        color: var(--fg);
        line-height: 1.15;
        letter-spacing: -0.02em;
        margin-bottom: 20px;
    }
    .body-text {
        font-family: 'BodyFont', sans-serif;
        font-size: 20px;
        color: var(--fg);
        opacity: 0.7;
        line-height: 1.5;
    }
    .accent-line {
        width: 60px;
        height: 4px;
        background: var(--accent);
        margin-bottom: 32px;
        border-radius: 2px;
    }

    /* Right panel — 38% */
    .panel-right {
        width: 38%;
        height: 100%;
        background: var(--muted);
        position: relative;
        overflow: hidden;
    }
    .panel-right .orb {
        position: absolute;
        border-radius: 50%;
        filter: blur(60px);
        opacity: 0.5;
    }
    .orb-a { width: 300px; height: 300px; background: var(--accent); top: 20%; left: 10%; }
    .orb-b { width: 200px; height: 200px; background: var(--accent2); bottom: 10%; right: -20%; }
    .panel-right .grid-overlay {
        position: absolute;
        top: 0; left: 0; width: 100%; height: 100%;
        background:
            repeating-linear-gradient(0deg, rgba(255,255,255,0.03) 0px, rgba(255,255,255,0.03) 1px, transparent 1px, transparent 40px),
            repeating-linear-gradient(90deg, rgba(255,255,255,0.03) 0px, rgba(255,255,255,0.03) 1px, transparent 1px, transparent 40px);
    }

    /* Noise */
    .noise { position: absolute; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; z-index: 10; opacity: 0.03; }
</style>
</head>
<body>
    <div class="panel-left">
        <div class="accent-line"></div>
        <div class="heading">Bold Statement Title</div>
        <div class="body-text">Supporting description that provides context and detail.</div>
    </div>
    <div class="panel-right">
        <div class="orb orb-a"></div>
        <div class="orb orb-b"></div>
        <div class="grid-overlay"></div>
    </div>
    <div class="noise">
        <svg width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
            <filter id="n"><feTurbulence type="fractalNoise" baseFrequency="0.65" numOctaves="4" stitchTiles="stitch"/><feColorMatrix type="saturate" values="0"/></filter>
            <rect width="100%" height="100%" filter="url(#n)"/>
        </svg>
    </div>
</body>
</html>
```

---

## Template 3: Card Grid Layout (2x2 Glassmorphism)

Best for: feature highlights, comparison graphics, multi-point content.

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<style>
    @font-face {
        font-family: 'DisplayFont';
        src: url('FONT_URL_DISPLAY') format('truetype');
        font-weight: 700; font-style: normal;
    }
    @font-face {
        font-family: 'BodyFont';
        src: url('FONT_URL_BODY') format('truetype');
        font-weight: 400; font-style: normal;
    }
    *, *::before, *::after { margin: 0; padding: 0; box-sizing: border-box; }
    html, body { width: 1080px; height: 1080px; overflow: hidden; -webkit-font-smoothing: antialiased; }

    body {
        position: relative;
        --bg: #0C0C0F;
        --fg: #E8ECF0;
        --accent: #00E5FF;
        --accent2: #FF2D78;
        --muted: #1A1A24;
        background:
            radial-gradient(ellipse at 20% 30%, rgba(0, 229, 255, 0.15) 0%, transparent 50%),
            radial-gradient(ellipse at 80% 70%, rgba(255, 45, 120, 0.12) 0%, transparent 50%),
            var(--bg);
    }

    .header {
        position: absolute;
        top: 60px;
        left: 60px;
        z-index: 3;
    }
    .header h1 {
        font-family: 'DisplayFont', sans-serif;
        font-size: 48px;
        font-weight: 700;
        color: var(--fg);
        letter-spacing: -0.02em;
    }
    .header p {
        font-family: 'BodyFont', sans-serif;
        font-size: 18px;
        color: var(--fg);
        opacity: 0.5;
        margin-top: 8px;
        text-transform: uppercase;
        letter-spacing: 0.1em;
    }

    .card-grid {
        position: absolute;
        top: 180px;
        left: 60px;
        right: 60px;
        bottom: 60px;
        display: grid;
        grid-template-columns: 1fr 1fr;
        grid-template-rows: 1fr 1fr;
        gap: 24px;
        z-index: 3;
    }
    .card {
        background: rgba(255, 255, 255, 0.06);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 36px;
        display: flex;
        flex-direction: column;
        justify-content: flex-end;
    }
    .card-number {
        font-family: 'DisplayFont', sans-serif;
        font-size: 64px;
        font-weight: 700;
        color: var(--accent);
        opacity: 0.3;
        line-height: 1;
        margin-bottom: auto;
    }
    .card-title {
        font-family: 'DisplayFont', sans-serif;
        font-size: 24px;
        font-weight: 700;
        color: var(--fg);
        margin-bottom: 8px;
    }
    .card-desc {
        font-family: 'BodyFont', sans-serif;
        font-size: 14px;
        color: var(--fg);
        opacity: 0.6;
        line-height: 1.5;
    }

    .noise { position: absolute; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; z-index: 10; opacity: 0.03; }
</style>
</head>
<body>
    <div class="header">
        <h1>Section Title</h1>
        <p>Category label</p>
    </div>
    <div class="card-grid">
        <div class="card">
            <div class="card-number">01</div>
            <div class="card-title">Feature One</div>
            <div class="card-desc">Brief description of this feature or point.</div>
        </div>
        <div class="card">
            <div class="card-number">02</div>
            <div class="card-title">Feature Two</div>
            <div class="card-desc">Brief description of this feature or point.</div>
        </div>
        <div class="card">
            <div class="card-number">03</div>
            <div class="card-title">Feature Three</div>
            <div class="card-desc">Brief description of this feature or point.</div>
        </div>
        <div class="card">
            <div class="card-number">04</div>
            <div class="card-title">Feature Four</div>
            <div class="card-desc">Brief description of this feature or point.</div>
        </div>
    </div>
    <div class="noise">
        <svg width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
            <filter id="n"><feTurbulence type="fractalNoise" baseFrequency="0.65" numOctaves="4" stitchTiles="stitch"/><feColorMatrix type="saturate" values="0"/></filter>
            <rect width="100%" height="100%" filter="url(#n)"/>
        </svg>
    </div>
</body>
</html>
```

---

## Template 4: Hero Banner with Overlay Text

Best for: GitHub covers, LinkedIn banners, wide-format headers.

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<style>
    @font-face {
        font-family: 'DisplayFont';
        src: url('FONT_URL_DISPLAY') format('truetype');
        font-weight: 700; font-style: normal;
    }
    @font-face {
        font-family: 'BodyFont';
        src: url('FONT_URL_BODY') format('truetype');
        font-weight: 400; font-style: normal;
    }
    *, *::before, *::after { margin: 0; padding: 0; box-sizing: border-box; }
    html, body { width: 1500px; height: 600px; overflow: hidden; -webkit-font-smoothing: antialiased; }

    body {
        position: relative;
        --bg: #1A1614;
        --fg: #E8DCC8;
        --accent: #C4943A;
        --muted: #2E2622;
        background: var(--bg);
    }

    /* Background texture */
    .bg-texture {
        position: absolute; top: 0; left: 0; width: 100%; height: 100%;
        background:
            radial-gradient(ellipse at 70% 40%, rgba(196, 148, 58, 0.12) 0%, transparent 60%),
            repeating-linear-gradient(0deg, rgba(255,255,255,0.015) 0px, rgba(255,255,255,0.015) 1px, transparent 1px, transparent 80px),
            repeating-linear-gradient(90deg, rgba(255,255,255,0.015) 0px, rgba(255,255,255,0.015) 1px, transparent 1px, transparent 80px);
        z-index: 1;
    }

    /* Content overlay */
    .content {
        position: absolute;
        top: 0; left: 0; width: 100%; height: 100%;
        display: flex;
        align-items: center;
        padding: 0 100px;
        z-index: 3;
    }
    .text-block {
        max-width: 60%;
    }
    .label {
        font-family: 'BodyFont', sans-serif;
        font-size: 14px;
        color: var(--accent);
        text-transform: uppercase;
        letter-spacing: 0.15em;
        margin-bottom: 20px;
    }
    .heading {
        font-family: 'DisplayFont', serif;
        font-size: 64px;
        font-weight: 700;
        color: var(--fg);
        line-height: 1.1;
        letter-spacing: -0.02em;
        margin-bottom: 16px;
    }
    .description {
        font-family: 'BodyFont', sans-serif;
        font-size: 18px;
        color: var(--fg);
        opacity: 0.6;
        line-height: 1.5;
        max-width: 500px;
    }

    /* Decorative accent */
    .accent-shape {
        position: absolute;
        right: 80px;
        top: 50%;
        transform: translateY(-50%);
        width: 300px;
        height: 300px;
        border: 2px solid var(--accent);
        border-radius: 50%;
        opacity: 0.2;
        z-index: 2;
    }
    .accent-shape-2 {
        position: absolute;
        right: 120px;
        top: 50%;
        transform: translateY(-50%);
        width: 220px;
        height: 220px;
        border: 1px solid var(--accent);
        border-radius: 50%;
        opacity: 0.1;
        z-index: 2;
    }

    .noise { position: absolute; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; z-index: 10; opacity: 0.04; }
</style>
</head>
<body>
    <div class="bg-texture"></div>
    <div class="content">
        <div class="text-block">
            <div class="label">Category Label</div>
            <div class="heading">Hero Title Goes Here</div>
            <div class="description">A supporting sentence that adds context without overwhelming the visual hierarchy.</div>
        </div>
    </div>
    <div class="accent-shape"></div>
    <div class="accent-shape-2"></div>
    <div class="noise">
        <svg width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
            <filter id="n"><feTurbulence type="fractalNoise" baseFrequency="0.65" numOctaves="4" stitchTiles="stitch"/><feColorMatrix type="saturate" values="0"/></filter>
            <rect width="100%" height="100%" filter="url(#n)"/>
        </svg>
    </div>
</body>
</html>
```

---

## Template 5: Stacked Sections with Visual Separators

Best for: infographics, multi-section social posts, Pinterest pins.

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<style>
    @font-face {
        font-family: 'DisplayFont';
        src: url('FONT_URL_DISPLAY') format('truetype');
        font-weight: 700; font-style: normal;
    }
    @font-face {
        font-family: 'BodyFont';
        src: url('FONT_URL_BODY') format('truetype');
        font-weight: 400; font-style: normal;
    }
    *, *::before, *::after { margin: 0; padding: 0; box-sizing: border-box; }
    html, body { width: 1000px; height: 1500px; overflow: hidden; -webkit-font-smoothing: antialiased; }

    body {
        position: relative;
        --bg: #F5EFDF;
        --fg: #3B2F22;
        --accent: #B8860B;
        --muted: #DDD2BE;
        background: var(--bg);
    }

    .section {
        padding: 60px 80px;
        position: relative;
    }
    .section-header {
        border-bottom: 2px solid var(--muted);
        padding-bottom: 40px;
        margin-bottom: 0;
    }
    .section-header .label {
        font-family: 'BodyFont', sans-serif;
        font-size: 12px;
        color: var(--accent);
        text-transform: uppercase;
        letter-spacing: 0.15em;
        margin-bottom: 16px;
    }
    .section-header h1 {
        font-family: 'DisplayFont', serif;
        font-size: 56px;
        font-weight: 700;
        color: var(--fg);
        line-height: 1.15;
        letter-spacing: -0.02em;
    }

    .section-body {
        border-bottom: 1px solid var(--muted);
        display: flex;
        align-items: baseline;
        gap: 40px;
    }
    .section-body .number {
        font-family: 'DisplayFont', serif;
        font-size: 48px;
        font-weight: 700;
        color: var(--accent);
        opacity: 0.4;
        flex-shrink: 0;
        width: 60px;
    }
    .section-body .text {
        flex: 1;
    }
    .section-body h2 {
        font-family: 'DisplayFont', serif;
        font-size: 28px;
        font-weight: 700;
        color: var(--fg);
        margin-bottom: 8px;
    }
    .section-body p {
        font-family: 'BodyFont', sans-serif;
        font-size: 16px;
        color: var(--fg);
        opacity: 0.7;
        line-height: 1.5;
    }

    .section-footer {
        padding-top: 40px;
        text-align: center;
    }
    .section-footer p {
        font-family: 'BodyFont', sans-serif;
        font-size: 14px;
        color: var(--fg);
        opacity: 0.4;
        text-transform: uppercase;
        letter-spacing: 0.1em;
    }

    .noise { position: absolute; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; z-index: 10; opacity: 0.025; }
</style>
</head>
<body>
    <div class="section section-header">
        <div class="label">Topic Category</div>
        <h1>Main Title of This Piece</h1>
    </div>
    <div class="section section-body">
        <div class="number">01</div>
        <div class="text">
            <h2>First Point</h2>
            <p>Explanation of the first key point with enough detail to be useful.</p>
        </div>
    </div>
    <div class="section section-body">
        <div class="number">02</div>
        <div class="text">
            <h2>Second Point</h2>
            <p>Explanation of the second key point with enough detail to be useful.</p>
        </div>
    </div>
    <div class="section section-body">
        <div class="number">03</div>
        <div class="text">
            <h2>Third Point</h2>
            <p>Explanation of the third key point with enough detail to be useful.</p>
        </div>
    </div>
    <div class="section section-footer">
        <p>Footer attribution or call to action</p>
    </div>
    <div class="noise">
        <svg width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
            <filter id="n"><feTurbulence type="fractalNoise" baseFrequency="0.5" numOctaves="3" stitchTiles="stitch"/><feColorMatrix type="saturate" values="0"/></filter>
            <rect width="100%" height="100%" filter="url(#n)"/>
        </svg>
    </div>
</body>
</html>
```

---

## Template 6: Asymmetric Composition with Floating Elements

Best for: creative covers, art-directed layouts, editorial designs.

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<style>
    @font-face {
        font-family: 'DisplayFont';
        src: url('FONT_URL_DISPLAY') format('truetype');
        font-weight: 700; font-style: normal;
    }
    @font-face {
        font-family: 'BodyFont';
        src: url('FONT_URL_BODY') format('truetype');
        font-weight: 400; font-style: normal;
    }
    *, *::before, *::after { margin: 0; padding: 0; box-sizing: border-box; }
    html, body { width: 1080px; height: 1080px; overflow: hidden; -webkit-font-smoothing: antialiased; }

    body {
        position: relative;
        --bg: #F0E8D8;
        --fg: #1A1410;
        --accent: #6B4226;
        --accent2: #B8452A;
        --muted: #D8CCBA;
        background: var(--bg);
    }

    /* Large geometric shape */
    .geo-block {
        position: absolute;
        width: 55%;
        height: 70%;
        top: 15%;
        right: -5%;
        background: var(--accent);
        opacity: 0.08;
        transform: rotate(-6deg);
        z-index: 1;
    }

    /* Accent bar */
    .accent-bar {
        position: absolute;
        width: 8px;
        height: 40%;
        top: 30%;
        left: 10%;
        background: var(--accent2);
        z-index: 2;
    }

    /* Floating circle */
    .float-circle {
        position: absolute;
        width: 180px;
        height: 180px;
        border-radius: 50%;
        border: 2px solid var(--accent);
        opacity: 0.15;
        bottom: 15%;
        right: 20%;
        z-index: 2;
    }

    /* Text content — positioned asymmetrically */
    .content {
        position: absolute;
        top: 20%;
        left: 14%;
        max-width: 55%;
        z-index: 3;
    }
    .overline {
        font-family: 'BodyFont', sans-serif;
        font-size: 13px;
        color: var(--accent);
        text-transform: uppercase;
        letter-spacing: 0.2em;
        margin-bottom: 24px;
    }
    .heading {
        font-family: 'DisplayFont', serif;
        font-size: 80px;
        font-weight: 700;
        color: var(--fg);
        line-height: 1.05;
        letter-spacing: -0.03em;
        margin-bottom: 20px;
    }
    .body-text {
        font-family: 'BodyFont', sans-serif;
        font-size: 18px;
        color: var(--fg);
        opacity: 0.6;
        line-height: 1.55;
        max-width: 400px;
    }

    /* Bottom-right attribution */
    .attribution {
        position: absolute;
        bottom: 50px;
        right: 50px;
        font-family: 'BodyFont', sans-serif;
        font-size: 11px;
        color: var(--fg);
        opacity: 0.3;
        text-transform: uppercase;
        letter-spacing: 0.15em;
        z-index: 3;
    }

    .noise { position: absolute; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; z-index: 10; opacity: 0.03; }
</style>
</head>
<body>
    <div class="geo-block"></div>
    <div class="accent-bar"></div>
    <div class="float-circle"></div>
    <div class="content">
        <div class="overline">Category or Label</div>
        <div class="heading">Asymmetric Title</div>
        <div class="body-text">A brief supporting statement that grounds the composition and provides context.</div>
    </div>
    <div class="attribution">Attribution Text</div>
    <div class="noise">
        <svg width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
            <filter id="n"><feTurbulence type="fractalNoise" baseFrequency="0.55" numOctaves="4" stitchTiles="stitch"/><feColorMatrix type="saturate" values="0"/></filter>
            <rect width="100%" height="100%" filter="url(#n)"/>
        </svg>
    </div>
</body>
</html>
```
