---
name: carousel-design
description: Multi-image carousel sets for Instagram and LinkedIn. Hook-content-CTA story arcs with visual continuity across slides. Use when user asks for a carousel, multi-slide post, or swipeable content.
license: MIT
metadata:
  author: canvas-super-creator
  version: 4.0.0
---

# Carousel Design — Multi-Slide Story Arcs

Create multi-image carousel sets for Instagram and LinkedIn with intentional story structure, visual continuity across slides, and hook-to-CTA narrative flow. Carousels are the highest-performing organic content format because they reward engagement with value.

---

## Format Quick Reference

| Format | Dimensions (px) | Slides | Platform |
|---|---|---|---|
| Instagram Carousel | 1080 x 1080 | 2-10 | Instagram feed |
| LinkedIn Carousel/PDF | 1080 x 1350 | 2-20 | LinkedIn document posts |
| Instagram Story Sequence | 1080 x 1920 | 2-15 | Instagram Stories |

**Full details:** Read `./canvas-super-creator/references/formats.md` for safe zones and typography scales.

---

## Workflow

1. **Read references:**
   - `./canvas-super-creator/references/formats.md` — dimensions and safe zones
   - `./canvas-super-creator/references/color-palettes.md` — palette selection
   - `./canvas-super-creator/references/typography-pairings.md` — font pairing
   - `./canvas-super-creator/references/composition-guide.md` — layout technique
   - `./canvas-super-creator/references/anti-slop-checklist.md` — quality gates
   - `./html-design/references/css-techniques.md` — CSS techniques
   - `./carousel-design/references/carousel-patterns.md` — carousel-specific recipes

2. **Create storyline outline:**
   - Define the hook (slide 1)
   - List content beats (slides 2 to N-1) — one point per slide
   - Define CTA (final slide)

3. **Define visual system:**
   - Palette, fonts, grid, recurring elements
   - Shared CSS custom properties for all slides

4. **Design hook slide first** — this is the most critical slide (it appears in feed)

5. **Design content slides** following the visual system

6. **Design CTA slide**

7. **Review continuity:** View all slides in sequence. Check color, type, grid, and element consistency.

8. **Render via render-engine** pipeline — each slide is a separate HTML file

---

## Mandatory Storyline Structure

Every carousel follows the Hook → Content → CTA arc. This is not optional.

### Slide 1 — HOOK

The hook slide appears in the feed preview. It must make people stop scrolling and start swiping.

- **Bold headline creating curiosity.** A question, a bold claim, or a surprising statistic.
- **Must work standalone.** If someone only sees this slide and nothing else, it should still make sense.
- **No preamble.** Do not waste the hook on "Introduction" or "Part 1". The hook IS the proposition.
- **Larger typography than content slides.** The hook needs to be bolder, more dramatic.

### Slides 2 to N-1 — CONTENT

The content slides deliver the value promised by the hook. Each slide covers ONE point.

- **One idea per slide.** Never pack two concepts into one slide.
- **Numbered progression.** "1/7", "Step 2", or visual slide indicators give readers position awareness.
- **Consistent layout.** Every content slide uses the same grid, same font sizes, same element positions.
- **Increasing depth.** Start simple, build complexity. The first content slide is the easiest concept.

### Slide N — CTA

The final slide wraps up the narrative and directs action.

- **Summary or key takeaway.** Reinforce the main message.
- **Clear call-to-action.** "Follow for more", "Save this post", "Link in bio", "Comment your favorite".
- **Brand identity.** Handle, logo, or brand mark.
- **Different visual energy.** The CTA slide should feel like a conclusion — it can break the content pattern slightly.

---

## Visual Continuity System

The difference between a professional carousel and amateur slides is visual continuity. These elements MUST be consistent:

### Shared Background System

Every slide shares the same base background treatment:

```css
/* All slides use identical background */
body {
    --bg: #0C0C0F;
    --fg: #E8ECF0;
    --accent: #00E5FF;
    --accent2: #FF2D78;
    --muted: #1A1A24;
    background: var(--bg);
}
```

Options for background continuity:
- **Solid color** — safest, cleanest
- **Shared gradient** — same gradient on every slide
- **Color progression** — background subtly shifts hue across slides (e.g., dark blue → dark purple → dark red)

### Consistent Header/Footer Zones

```
+----------------------------------+
| [Logo]         [Slide 3/7]       |  <- Header zone: same position on ALL slides
|                                  |
|         SLIDE CONTENT            |
|                                  |
| [accent line]                    |  <- Footer zone: consistent element
+----------------------------------+
```

- Header zone height: fixed (e.g., 80px from top)
- Footer zone height: fixed (e.g., 60px from bottom)
- Logo position: same corner on every slide
- Slide indicator: same position on every slide

### Typography Consistency

All slides use the SAME:
- Font family for headings
- Font family for body text
- Font sizes for equivalent elements
- Letter-spacing and line-height values
- Color for text (from shared custom properties)

### Color Accent Progression

For visual interest without breaking continuity, shift the accent color subtly across slides:

```css
/* Slide 1 */ --accent: #00E5FF;
/* Slide 2 */ --accent: #00D4FF;
/* Slide 3 */ --accent: #00C3FF;
/* Slide 4 */ --accent: #00B2FF;
/* Slide 5 */ --accent: #00A1FF;
/* CTA slide */ --accent: #FF2D78; /* Contrasting CTA color */
```

### Edge Continuity

Elements that span across slide boundaries create the illusion of a continuous canvas:

- A gradient that continues from slide edge to next slide edge
- A line or shape that starts on the right edge of slide N and continues from the left edge of slide N+1
- Consistent position of decorative elements (e.g., a line at 80% height on every slide)

---

## Slide Type Templates

### Stat Slide

Big number with supporting context. High impact, minimal text.

```
+----------------------------------+
|                                  |
|            87%                   |  <- Giant number, accent color
|    of developers prefer          |  <- Context line, muted
|    TypeScript in 2026            |
|                                  |
+----------------------------------+
```

### Quote Slide

Pull quote with attribution. Decorative quotation mark.

```
+----------------------------------+
|   "                              |  <- Decorative quote mark, very large, low opacity
|                                  |
|   "The best code is the code     |
|    you never had to write."      |  <- Quote text, italic serif
|                                  |
|         — Jeff Atwood            |  <- Attribution, small caps
+----------------------------------+
```

### List Slide

3-4 bullets with icons or numbers. Clear vertical hierarchy.

```
+----------------------------------+
|   KEY BENEFITS                   |
|                                  |
|   01  Faster deployment          |
|   02  Lower costs                |
|   03  Better reliability         |
|   04  Happier teams              |
|                                  |
+----------------------------------+
```

### Comparison Slide

Before/after or versus layout. Split screen.

```
+----------------------------------+
|   BEFORE       |    AFTER        |
|   [old way]    |    [new way]    |
|   slow         |    fast         |
|   expensive    |    affordable   |
|   fragile      |    resilient    |
+----------------------------------+
```

### Tip Slide

Numbered tip with explanation. Educational format.

```
+----------------------------------+
|   TIP #3                         |  <- Tip number, accent color
|                                  |
|   Use Semantic HTML              |  <- Tip title, bold
|                                  |
|   Screen readers and search      |
|   engines understand your        |  <- Explanation, regular weight
|   content better when you use    |
|   the right elements.            |
+----------------------------------+
```

### Image + Text Slide

Visual on one half, text on the other. Flexible split.

```
+----------------------------------+
|                 |                 |
|   [IMAGE]       |   Headline     |
|                 |   Body text    |
|                 |   goes here    |
|                 |                 |
+----------------------------------+
```

---

## CSS Approach — Shared Custom Properties

All slides in a carousel share a common CSS foundation. Define it once, use it everywhere:

```css
/* carousel-system.css — shared across all slides */
:root {
    /* Palette */
    --bg: #0C0C0F;
    --fg: #E8ECF0;
    --accent: #00E5FF;
    --accent2: #FF2D78;
    --muted: #1A1A24;

    /* Typography */
    --font-heading: 'BigShoulders', sans-serif;
    --font-body: 'Outfit', sans-serif;
    --font-accent: 'InstrumentSerif', serif;
    --font-mono: 'GeistMono', monospace;

    /* Grid */
    --padding: 60px;
    --header-height: 80px;
    --footer-height: 60px;

    /* Slide indicator */
    --indicator-size: 14px;
}

body {
    position: relative;
    background: var(--bg);
    overflow: hidden;
}

/* Consistent header zone */
.slide-header {
    position: absolute;
    top: 0; left: 0; width: 100%; height: var(--header-height);
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 var(--padding);
    z-index: 5;
}
.slide-header .logo {
    font-family: var(--font-heading);
    font-size: 18px;
    font-weight: 700;
    color: var(--accent);
}
.slide-header .indicator {
    font-family: var(--font-mono);
    font-size: var(--indicator-size);
    color: var(--fg);
    opacity: 0.4;
}

/* Consistent footer zone */
.slide-footer {
    position: absolute;
    bottom: 0; left: 0; width: 100%; height: var(--footer-height);
    display: flex;
    align-items: center;
    padding: 0 var(--padding);
    z-index: 5;
}
.slide-footer .accent-line {
    width: 40px; height: 3px;
    background: var(--accent);
}

/* Content area — between header and footer */
.slide-content {
    position: absolute;
    top: var(--header-height);
    left: var(--padding);
    right: var(--padding);
    bottom: var(--footer-height);
    display: flex;
    flex-direction: column;
    justify-content: center;
    z-index: 3;
}
```

### Font Loading

```css
@font-face {
    font-family: 'BigShoulders';
    src: url('file:///Users/jaypokharna/Desktop/Shared%20Folder/Shared%20Folder/python/claude-skills/canvas-super-creator/skills/canvas-super-creator/canvas-fonts/BigShouldersDisplay-Bold.ttf');
    font-weight: 700;
}
@font-face {
    font-family: 'Outfit';
    src: url('file:///Users/jaypokharna/Desktop/Shared%20Folder/Shared%20Folder/python/claude-skills/canvas-super-creator/skills/canvas-super-creator/canvas-fonts/Outfit-Regular.ttf');
    font-weight: 400;
}
@font-face {
    font-family: 'InstrumentSerif';
    src: url('file:///Users/jaypokharna/Desktop/Shared%20Folder/Shared%20Folder/python/claude-skills/canvas-super-creator/skills/canvas-super-creator/canvas-fonts/InstrumentSerif-Regular.ttf');
    font-weight: 400;
}
@font-face {
    font-family: 'GeistMono';
    src: url('file:///Users/jaypokharna/Desktop/Shared%20Folder/Shared%20Folder/python/claude-skills/canvas-super-creator/skills/canvas-super-creator/canvas-fonts/GeistMono-Regular.ttf');
    font-weight: 400;
}
```

---

## Anti-Patterns Specific to Carousels

- **No hook on slide 1.** If the first slide says "Introduction" or "Part 1 of 7", nobody swipes.
- **Inconsistent typography across slides.** Different font sizes, different families between slides = amateur.
- **Missing slide indicators.** Readers need position awareness (where am I in this sequence?).
- **Too much text per slide.** One idea per slide. If it takes 10 seconds to read, split it.
- **No CTA on the final slide.** The last slide must direct action — follow, save, comment, visit.
- **Breaking the grid between slides.** If content shifts position between slides, the experience feels broken.
- **Same visual weight on all slides.** The hook should be bolder. Content slides should be consistent. The CTA should feel like a conclusion.
- **Ignoring color continuity.** If slide 3 suddenly uses different colors, the carousel loses cohesion.
- **No narrative arc.** Random tips in random order is a list, not a carousel. Build toward a conclusion.
- **More than one point per slide.** The moment you put two ideas on one slide, you have lost the format's advantage.
