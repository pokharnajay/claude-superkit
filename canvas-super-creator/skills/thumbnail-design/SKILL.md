---
name: thumbnail-design
description: YouTube thumbnails and Open Graph images. Use when user asks for a thumbnail, OG image, or link preview graphic.
license: MIT
metadata:
  author: canvas-super-creator
  version: 3.0.0
---

# Thumbnail Design — YouTube & Open Graph Images

Create high-impact thumbnails that communicate instantly at tiny preview sizes. Thumbnails are the most constrained design format: they must be readable at 120x68 pixels in a YouTube sidebar while being designed at 1280x720.

---

## Format Quick Reference

| Format | Dimensions | Preview Size | Key Constraint |
|---|---|---|---|
| YouTube Thumbnail | 1280 x 720 | 120 x 68 (sidebar) | Bottom-right 120x28 obscured by timestamp. Max 3 words. |
| Open Graph (OG) | 1200 x 630 | Varies by platform | Center 630x630 must read as a square crop (some platforms). |

**Full details:** Read `./canvas-super-creator/references/formats.md` for safe zones and typography scales.

---

## Workflow

1. **Read references:**
   - `./canvas-super-creator/references/formats.md` — dimensions and safe zones
   - `./canvas-super-creator/references/color-palettes.md` — palette selection
   - `./canvas-super-creator/references/typography-pairings.md` — font pairing
   - `./canvas-super-creator/references/anti-slop-checklist.md` — quality gates
   - `./html-design/references/css-techniques.md` — CSS techniques
   - `./thumbnail-design/references/thumbnail-patterns.md` — thumbnail-specific recipes

2. **Output specification** with format, palette, typography, mood

3. **Design with thumbnail principles** (below)

4. **Render via render-engine** pipeline

5. **Zoom test:** View the final image at 10% zoom. Can you still read the text and identify the subject? If not, simplify.

---

## Thumbnail Design Principles

### The 120x68 Test

YouTube thumbnails appear as 120x68px previews in sidebars and recommendations. Your design MUST work at this size:

- **Maximum 3 words.** Anything more becomes illegible.
- **Minimum 80px font size** at design resolution (1280x720) for primary text.
- **High contrast is mandatory.** Text needs heavy shadow, outline, or background to separate from any backdrop.
- **One subject, one message.** Complex compositions collapse at small sizes.

### Text Treatment for Thumbnails

Text on thumbnails requires aggressive treatment to remain readable:

```css
/* Heavy text shadow stack for readability */
.thumb-text {
    font-family: 'BigShoulders', sans-serif;
    font-size: 96px;
    font-weight: 700;
    color: #FFFFFF;
    text-transform: uppercase;
    letter-spacing: 0.02em;
    text-shadow:
        0 2px 4px rgba(0, 0, 0, 0.8),
        0 4px 8px rgba(0, 0, 0, 0.6),
        0 8px 16px rgba(0, 0, 0, 0.4),
        2px 2px 0 rgba(0, 0, 0, 0.9),
        -2px -2px 0 rgba(0, 0, 0, 0.9);
}
```

Alternatively, use a solid background pill behind text:

```css
.thumb-text-bg {
    display: inline-block;
    font-family: 'Boldonse', sans-serif;
    font-size: 88px;
    color: #FFFFFF;
    background: var(--accent);
    padding: 8px 24px;
    line-height: 1.1;
}
```

### The Timestamp Dead Zone

YouTube overlays a timestamp badge in the bottom-right corner (approximately 120x28px at 1280x720). Never place critical content here:

```css
/* Timestamp dead zone — avoid this area */
.dead-zone {
    position: absolute;
    bottom: 0;
    right: 0;
    width: 120px;
    height: 28px;
    /* Content here will be obscured */
}
```

### Color for Thumbnails

Thumbnail palettes should be more aggressive than other formats:

- **Use maximum 3 colors.** Background + text + one accent.
- **Complementary pairs work best.** Red/cyan, orange/blue, yellow/purple create maximum visual pop.
- **Avoid subtle palettes.** Nuance is lost at 120x68 pixels.
- **Background must contrast sharply with text.** No mid-tone backgrounds with white text.

### Composition for Thumbnails

- **Split compositions** (60/40 or 50/50) work well: text on one side, visual on the other
- **Center-weighted** works for single bold statement + background treatment
- **Avoid Rule of Thirds** for thumbnails — the format is too small for off-center subtlety to register
- **Leave breathing room** around text — tight padding makes text harder to read at small sizes

---

## Open Graph (OG) Image Specifics

OG images appear as link previews on Slack, Discord, Facebook, Twitter, and other platforms:

- Some platforms crop to a center square — ensure the center 630x630px reads independently
- Include logo/brand mark + title + optional description
- Keep it professional and clear — OG images represent links, not standalone art
- Avoid text that duplicates the page title (it appears alongside the OG image)

---

## Anti-Patterns for Thumbnails

- **Too many words.** If you have more than 3 words, the thumbnail will fail the sidebar test.
- **Subtle typography.** Light-weight fonts, thin strokes, and low-contrast text are invisible at preview size.
- **Complex backgrounds.** Busy, detailed backgrounds compete with text and create visual noise.
- **Small text with no shadow.** Text without heavy shadow treatment vanishes against non-uniform backgrounds.
- **Content in the timestamp zone.** Bottom-right corner is always obscured on YouTube.
- **Gradient text on gradient background.** Both become muddy at small sizes.
