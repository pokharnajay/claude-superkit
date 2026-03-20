---
name: social-media-design
description: Social media graphics — Instagram (square, story), LinkedIn, Twitter/X, Facebook, Pinterest posts. Use when user asks for social media content, cards, or graphics.
license: MIT
metadata:
  author: canvas-super-creator
  version: 3.0.0
---

# Social Media Design — Platform Graphics

Create scroll-stopping social media graphics optimized for specific platforms. Social posts must communicate in under 2 seconds, survive aggressive compression, and work at small mobile preview sizes.

---

## Platform Quick Reference

| Platform | Dimensions | Aspect | Key Constraint |
|---|---|---|---|
| Instagram Square | 1080 x 1080 | 1:1 | Feed may crop to circle in grid. High compression. |
| Instagram Story | 1080 x 1920 | 9:16 | Top 200px = story bar. Bottom 250px = CTA buttons. |
| Instagram Landscape | 1080 x 566 | 1.91:1 | Feed crops to square preview. Center must read alone. |
| LinkedIn Post | 1200 x 627 | 1.91:1 | Professional context. Avoid meme aesthetics. |
| Twitter/X Post | 1600 x 900 | 16:9 | Aggressive JPEG compression. Bold contrast needed. |
| Facebook Post | 1200 x 630 | ~1.91:1 | News Feed crops vary by device. Test center crop. |
| Pinterest Pin | 1000 x 1500 | 2:3 | Tall format. Grid may cut bottom. Key content in top 2/3. |

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
   - `./social-media-design/references/social-patterns.md` — platform-specific recipes

2. **Output specification** with format, palette, typography, composition, mood

3. **Design with html-design patterns** — follow the 4-phase process

4. **Render via render-engine** pipeline

---

## Social Media Design Principles

### The 2-Second Rule

Social media is a scroll environment. Your design gets approximately 2 seconds of attention in a feed:

- **One clear message.** If you cannot summarize the post in 5 words, simplify.
- **One focal point.** The eye should land on exactly one element first.
- **High contrast.** Low-contrast designs disappear in busy feeds.
- **Bold type or none.** Either make text large and commanding, or rely entirely on visual elements.

### Compression Survival

Every platform re-encodes uploads with aggressive compression:

- Avoid thin lines under 2px (they artifact)
- Avoid subtle gradients (banding risk)
- Use bold shapes and high contrast (survive JPEG artifacts)
- Dark text on light backgrounds compresses better than the reverse
- Test at 50% zoom to simulate mobile feed view

### Card Patterns

Social media graphics commonly use card-based layouts:

**Stat Card:** Large number + label + supporting context
**Quote Card:** Pull quote + attribution + decorative elements
**Feature Card:** Icon/visual + title + description
**Comparison Card:** Side-by-side or before/after
**List Card:** Numbered items with clear hierarchy
**Data Card:** Key metric + trend visualization

### Carousel Design

When creating multiple slides for carousels:

- Maintain consistent palette, typography, and layout grid across all slides
- First slide is the hook — it must work standalone in the feed preview
- Last slide is the CTA — clear action or summary
- Middle slides provide value — information, tips, data
- Consider visual continuity (elements that span across slide boundaries)

---

## CSS Patterns for Social Media

### Mobile-First Text Sizing

Social posts are viewed primarily on phones. Text must be readable at ~50% of design size:

```css
/* Minimum readable sizes at 1080x1080 */
.heading { font-size: 72px; }    /* Reads at ~36px on phone */
.subheading { font-size: 42px; } /* Reads at ~21px on phone */
.body { font-size: 28px; }       /* Reads at ~14px on phone */
.caption { font-size: 18px; }    /* Minimum — smaller will be illegible */
```

### High-Contrast Badge

Eye-catching label/tag element:

```css
.badge {
    display: inline-block;
    font-family: 'WorkSans', sans-serif;
    font-size: 14px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    padding: 8px 20px;
    background: var(--accent);
    color: var(--bg);
    border-radius: 4px;
}
```

### Stat Display

Large numbers that grab attention:

```css
.stat-number {
    font-family: 'BigShoulders', sans-serif;
    font-size: 120px;
    font-weight: 700;
    line-height: 1;
    color: var(--accent);
    letter-spacing: -0.02em;
}
.stat-label {
    font-family: 'WorkSans', sans-serif;
    font-size: 18px;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    color: var(--fg);
    opacity: 0.6;
    margin-top: 8px;
}
```

### Quote Block

```css
.quote-mark {
    font-family: 'InstrumentSerif', serif;
    font-size: 200px;
    color: var(--accent);
    opacity: 0.15;
    line-height: 0.5;
    position: absolute;
    top: 40px;
    left: 40px;
}
.quote-text {
    font-family: 'Lora', serif;
    font-size: 36px;
    font-weight: 600;
    color: var(--fg);
    line-height: 1.4;
    font-style: italic;
}
.quote-attribution {
    font-family: 'WorkSans', sans-serif;
    font-size: 16px;
    color: var(--fg);
    opacity: 0.5;
    margin-top: 24px;
    text-transform: uppercase;
    letter-spacing: 0.1em;
}
```
