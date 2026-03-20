# Carousel Design — CSS Recipes and Storyline Templates

Complete CSS patterns for carousel slide types, storyline templates, edge-continuity techniques, numbering styles, and hook patterns.

---

## Storyline Templates

### 1. Educational / How-To

Structure: Hook question → Step-by-step instructions → Summary CTA

```
Slide 1 (Hook): "How to Deploy in 5 Minutes" — bold question or bold claim
Slide 2: Step 1 — Setup (tip slide format)
Slide 3: Step 2 — Configure (tip slide format)
Slide 4: Step 3 — Test (tip slide format)
Slide 5: Step 4 — Deploy (tip slide format)
Slide 6: Step 5 — Monitor (tip slide format)
Slide 7 (CTA): Summary checklist + "Save this for later" + follow prompt
```

### 2. Listicle / Tips

Structure: Hook with number → Individual tip slides → CTA

```
Slide 1 (Hook): "7 CSS Tricks You Didn't Know" — number creates expectation
Slide 2: Trick #1 (tip slide with code example)
Slide 3: Trick #2
Slide 4: Trick #3
Slide 5: Trick #4
Slide 6: Trick #5
Slide 7: Trick #6
Slide 8: Trick #7
Slide 9 (CTA): "Which was your favorite?" + comment prompt + follow
```

### 3. Case Study / Before-After

Structure: Problem hook → Before state → Transformation → After state → CTA

```
Slide 1 (Hook): "We cut load time by 94%" — surprising stat
Slide 2: The problem (stat slide — "12.3 seconds average load time")
Slide 3: Root cause analysis (list slide — 3 issues found)
Slide 4: Solution 1 (comparison slide — before/after)
Slide 5: Solution 2 (comparison slide — before/after)
Slide 6: Results (stat slide — "0.7 seconds new load time")
Slide 7 (CTA): Summary + "Want us to audit your site?" + link in bio
```

### 4. Myth-Busting

Structure: Provocative myth → Myth/fact pairs → CTA

```
Slide 1 (Hook): "Stop Believing These Design Myths" — controversy hook
Slide 2: Myth #1 + Reality (comparison slide)
Slide 3: Myth #2 + Reality
Slide 4: Myth #3 + Reality
Slide 5: Myth #4 + Reality
Slide 6: Myth #5 + Reality
Slide 7 (CTA): "What other myths should we bust?" + follow for more
```

### 5. Data Story

Structure: Headline stat → Supporting data points → Insight → CTA

```
Slide 1 (Hook): "The State of AI in 2026" — big-picture framing
Slide 2: Key stat #1 (stat slide — market size)
Slide 3: Key stat #2 (stat slide — adoption rate)
Slide 4: Trend visualization (list slide — top 5 trends)
Slide 5: Comparison (comparison slide — 2024 vs 2026)
Slide 6: Key insight (quote slide — expert perspective)
Slide 7 (CTA): "Full report — link in bio" + save + follow
```

---

## Slide Type CSS Patterns

### Stat Slide

```css
html, body { width: 1080px; height: 1080px; }

body {
    --bg: #0C0C0F;
    --fg: #E8ECF0;
    --accent: #00E5FF;
    --muted: #1A1A24;
    position: relative;
    background: var(--bg);
}

.stat-container {
    position: absolute;
    top: 50%; left: 50%;
    transform: translate(-50%, -50%);
    text-align: center;
    z-index: 3;
}
.stat-number {
    font-family: 'BigShoulders', sans-serif;
    font-size: 200px;
    font-weight: 700;
    color: var(--accent);
    line-height: 1;
    letter-spacing: -0.02em;
}
.stat-unit {
    font-family: 'BigShoulders', sans-serif;
    font-size: 80px;
    font-weight: 700;
    color: var(--accent);
    opacity: 0.6;
    vertical-align: top;
}
.stat-context {
    font-family: 'Outfit', sans-serif;
    font-size: 28px;
    color: var(--fg);
    opacity: 0.6;
    margin-top: 24px;
    line-height: 1.4;
    max-width: 600px;
    margin-left: auto;
    margin-right: auto;
}
.stat-source {
    font-family: 'GeistMono', monospace;
    font-size: 13px;
    color: var(--fg);
    opacity: 0.25;
    margin-top: 32px;
    letter-spacing: 0.05em;
}
```

### Quote Slide

```css
.quote-container {
    position: absolute;
    top: 0; left: 0; width: 100%; height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 80px;
    z-index: 3;
}
.decorative-quote {
    position: absolute;
    top: 80px; left: 60px;
    font-family: 'InstrumentSerif', serif;
    font-size: 280px;
    color: var(--accent);
    opacity: 0.08;
    line-height: 0.5;
    z-index: 2;
}
.quote-text {
    font-family: 'InstrumentSerif', serif;
    font-size: 42px;
    font-weight: 400;
    font-style: italic;
    color: var(--fg);
    line-height: 1.35;
    text-align: center;
    max-width: 800px;
}
.quote-attribution {
    position: absolute;
    bottom: 100px; left: 50%;
    transform: translateX(-50%);
    font-family: 'WorkSans', sans-serif;
    font-size: 16px;
    color: var(--fg);
    opacity: 0.4;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    z-index: 3;
}
.quote-role {
    font-family: 'Outfit', sans-serif;
    font-size: 13px;
    color: var(--fg);
    opacity: 0.25;
    margin-top: 8px;
    text-align: center;
    text-transform: none;
    letter-spacing: 0.03em;
}
```

### List Slide

```css
.list-container {
    position: absolute;
    top: 120px; left: 60px; right: 60px; bottom: 80px;
    display: flex;
    flex-direction: column;
    z-index: 3;
}
.list-title {
    font-family: 'WorkSans', sans-serif;
    font-size: 18px;
    font-weight: 600;
    color: var(--accent);
    text-transform: uppercase;
    letter-spacing: 0.12em;
    margin-bottom: 40px;
}
.list-items {
    flex: 1;
    display: flex;
    flex-direction: column;
    justify-content: center;
    gap: 28px;
}
.list-item {
    display: flex;
    align-items: flex-start;
    gap: 20px;
}
.list-item .num {
    font-family: 'BigShoulders', sans-serif;
    font-size: 42px;
    font-weight: 700;
    color: var(--accent);
    line-height: 1;
    flex-shrink: 0;
    width: 50px;
}
.list-item .text {
    flex: 1;
}
.list-item .text h3 {
    font-family: 'BricolageGrotesque', sans-serif;
    font-size: 28px;
    font-weight: 700;
    color: var(--fg);
    line-height: 1.2;
}
.list-item .text p {
    font-family: 'Outfit', sans-serif;
    font-size: 18px;
    color: var(--fg);
    opacity: 0.5;
    margin-top: 4px;
    line-height: 1.4;
}
```

### Comparison Slide

```css
.comparison {
    position: absolute;
    top: 0; left: 0; width: 100%; height: 100%;
    display: flex;
    z-index: 3;
}
.comparison-left {
    width: 50%;
    height: 100%;
    background: var(--muted);
    display: flex;
    flex-direction: column;
    justify-content: center;
    padding: 60px;
}
.comparison-right {
    width: 50%;
    height: 100%;
    background: var(--bg);
    display: flex;
    flex-direction: column;
    justify-content: center;
    padding: 60px;
}
.comparison-label {
    font-family: 'WorkSans', sans-serif;
    font-size: 14px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    margin-bottom: 32px;
}
.comparison-left .comparison-label {
    color: var(--fg);
    opacity: 0.4;
}
.comparison-right .comparison-label {
    color: var(--accent);
}
.comparison-item {
    font-family: 'Outfit', sans-serif;
    font-size: 22px;
    color: var(--fg);
    line-height: 1.4;
    margin-bottom: 16px;
    padding-left: 16px;
    border-left: 3px solid transparent;
}
.comparison-left .comparison-item {
    opacity: 0.5;
    text-decoration: line-through;
    border-left-color: var(--fg);
    opacity: 0.2;
}
.comparison-right .comparison-item {
    border-left-color: var(--accent);
}
/* Divider line */
.comparison-divider {
    position: absolute;
    top: 10%; left: 50%;
    transform: translateX(-50%);
    width: 2px; height: 80%;
    background: rgba(255, 255, 255, 0.1);
    z-index: 4;
}
```

### Tip Slide

```css
.tip-container {
    position: absolute;
    top: 120px; left: 60px; right: 60px; bottom: 80px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    z-index: 3;
}
.tip-number {
    font-family: 'BigShoulders', sans-serif;
    font-size: 72px;
    font-weight: 700;
    color: var(--accent);
    line-height: 1;
    margin-bottom: 8px;
}
.tip-label {
    font-family: 'WorkSans', sans-serif;
    font-size: 14px;
    font-weight: 600;
    color: var(--accent);
    text-transform: uppercase;
    letter-spacing: 0.12em;
    opacity: 0.6;
    margin-bottom: 32px;
}
.tip-title {
    font-family: 'BricolageGrotesque', sans-serif;
    font-size: 48px;
    font-weight: 700;
    color: var(--fg);
    line-height: 1.1;
    letter-spacing: -0.01em;
    margin-bottom: 24px;
}
.tip-body {
    font-family: 'Outfit', sans-serif;
    font-size: 22px;
    color: var(--fg);
    opacity: 0.6;
    line-height: 1.5;
    max-width: 800px;
}

/* Optional code example */
.tip-code {
    font-family: 'GeistMono', monospace;
    font-size: 16px;
    color: var(--accent);
    background: var(--muted);
    padding: 24px;
    border-radius: 8px;
    margin-top: 24px;
    line-height: 1.6;
    overflow: hidden;
}
```

---

## Edge-Continuity Technique

### Matching Gradient Positions

When slides are swiped left-to-right, you can create the illusion of a continuous gradient by matching edge colors:

```css
/* Slide 1: gradient ends at right edge with color A */
.slide-1-bg {
    background: linear-gradient(90deg, #0C0C0F 0%, #1A1035 100%);
}

/* Slide 2: gradient starts at left edge with color A, ends with color B */
.slide-2-bg {
    background: linear-gradient(90deg, #1A1035 0%, #2A1545 100%);
}

/* Slide 3: gradient starts at left edge with color B */
.slide-3-bg {
    background: linear-gradient(90deg, #2A1545 0%, #3A1A55 100%);
}
```

### Spanning Line Element

A decorative line that continues across slide boundaries:

```css
/* On every slide — same position, same style */
.continuity-line {
    position: absolute;
    bottom: 120px; left: 0; width: 100%;
    height: 2px;
    background: linear-gradient(90deg, transparent 0%, var(--accent) 20%, var(--accent) 80%, transparent 100%);
    opacity: 0.15;
    z-index: 4;
}
```

### Spanning Decorative Shape

A circle or shape that appears partially on the right edge of one slide and continues on the left edge of the next:

```css
/* Slide N: circle exits right edge */
.shape-exit {
    position: absolute;
    top: 200px; right: -100px;
    width: 200px; height: 200px;
    border-radius: 50%;
    border: 2px solid var(--accent);
    opacity: 0.1;
    z-index: 2;
}

/* Slide N+1: circle enters left edge (matching position) */
.shape-enter {
    position: absolute;
    top: 200px; left: -100px;
    width: 200px; height: 200px;
    border-radius: 50%;
    border: 2px solid var(--accent);
    opacity: 0.1;
    z-index: 2;
}
```

---

## Slide Numbering Styles

### 1. Dot Indicator

```css
.dot-indicator {
    display: flex;
    gap: 8px;
    align-items: center;
}
.dot {
    width: 8px; height: 8px;
    border-radius: 50%;
    background: var(--fg);
    opacity: 0.2;
}
.dot.active {
    opacity: 1;
    background: var(--accent);
}
```

### 2. Fraction Style ("3/7")

```css
.fraction-indicator {
    font-family: 'GeistMono', monospace;
    font-size: 14px;
    color: var(--fg);
    opacity: 0.4;
}
.fraction-indicator .current {
    color: var(--accent);
    opacity: 1;
    font-weight: 700;
}
/* HTML: <span class="current">3</span>/7 */
```

### 3. Progress Bar

```css
.progress-bar {
    width: 120px; height: 3px;
    background: rgba(255, 255, 255, 0.1);
    border-radius: 2px;
    overflow: hidden;
}
.progress-fill {
    height: 100%;
    background: var(--accent);
    border-radius: 2px;
    /* Width set per slide: 14.3% for slide 1/7, 28.6% for 2/7, etc. */
}
```

### 4. No Indicator

For carousels where the content flow is obvious and slide count is low (3-4 slides), numbering can be omitted entirely. The visual progression carries the reader.

---

## Hook Slide Patterns

### Question Hook

Asks a question the audience wants answered. Creates an information gap.

```css
.hook-question {
    position: absolute;
    top: 50%; left: 50%;
    transform: translate(-50%, -50%);
    text-align: center;
    z-index: 3;
    max-width: 800px;
}
.hook-question h1 {
    font-family: 'BricolageGrotesque', sans-serif;
    font-size: 64px;
    font-weight: 800;
    color: var(--fg);
    line-height: 1.1;
    letter-spacing: -0.02em;
}
.hook-question .emphasis {
    color: var(--accent);
}
.hook-question .sub {
    font-family: 'Outfit', sans-serif;
    font-size: 22px;
    color: var(--fg);
    opacity: 0.5;
    margin-top: 20px;
}
/* Example: "Are You Making These 5 CSS Mistakes?" */
```

### Stat Hook

Opens with a surprising statistic that demands context.

```css
.hook-stat {
    position: absolute;
    top: 50%; left: 50%;
    transform: translate(-50%, -50%);
    text-align: center;
    z-index: 3;
}
.hook-stat .number {
    font-family: 'BigShoulders', sans-serif;
    font-size: 240px;
    font-weight: 700;
    color: var(--accent);
    line-height: 0.9;
}
.hook-stat .context {
    font-family: 'Outfit', sans-serif;
    font-size: 32px;
    color: var(--fg);
    margin-top: 16px;
    line-height: 1.3;
}
/* Example: "94%" + "of first impressions are design-related" */
```

### Bold Claim Hook

Makes a provocative statement that triggers engagement.

```css
.hook-claim {
    position: absolute;
    top: 50%; left: 60px; right: 60px;
    transform: translateY(-50%);
    z-index: 3;
}
.hook-claim h1 {
    font-family: 'BigShoulders', sans-serif;
    font-size: 80px;
    font-weight: 700;
    color: var(--fg);
    line-height: 1;
    text-transform: uppercase;
    letter-spacing: -0.01em;
}
.hook-claim .accent-word {
    color: var(--accent);
    display: block;
    font-size: 96px;
}
.hook-claim .swipe {
    font-family: 'Outfit', sans-serif;
    font-size: 16px;
    color: var(--fg);
    opacity: 0.3;
    margin-top: 40px;
    letter-spacing: 0.1em;
    text-transform: uppercase;
}
/* Example: "YOUR WEBSITE IS LOSING YOU / MONEY" + "Swipe to find out why →" */
```

### Controversy Hook

Challenges a common belief. Triggers "I need to see if they're right" response.

```css
.hook-controversy {
    position: absolute;
    top: 50%; left: 60px; right: 60px;
    transform: translateY(-50%);
    z-index: 3;
}
.hook-controversy .label {
    font-family: 'WorkSans', sans-serif;
    font-size: 16px;
    font-weight: 600;
    color: var(--accent);
    text-transform: uppercase;
    letter-spacing: 0.15em;
    margin-bottom: 24px;
}
.hook-controversy h1 {
    font-family: 'BricolageGrotesque', sans-serif;
    font-size: 56px;
    font-weight: 800;
    color: var(--fg);
    line-height: 1.15;
    letter-spacing: -0.01em;
}
.hook-controversy .strikethrough {
    text-decoration: line-through;
    opacity: 0.4;
}
/* Example: "UNPOPULAR OPINION" + "You Don't Need a <strike>Framework</strike> to Build Great Websites" */
```
