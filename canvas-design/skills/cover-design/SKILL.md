---
name: cover-design
description: Platform cover and banner designs — GitHub, Notion, LinkedIn, YouTube, Twitter/X. Use when user asks for a cover image, banner, or header for any platform.
license: MIT
metadata:
  author: canvas-design
  version: 3.0.0
---

# Cover Design — Platform Banners & Headers

Create cover images and banners optimized for specific platforms. Covers are ultra-wide compositions that must communicate instantly at small preview sizes while handling aggressive cropping across devices.

---

## Platform Quick Reference

| Platform | Dimensions | Aspect | Key Constraint |
|---|---|---|---|
| GitHub Repository | 1280 x 640 | 2:1 | Dark mode inversion. Keep centered vertically. |
| Notion Cover Wide | 1500 x 600 | 5:2 | Bottom 120px left half obscured by title. Draggable crop. |
| LinkedIn Personal | 1584 x 396 | 4:1 | Left 260px obscured by profile photo circle. Mobile center crop. |
| LinkedIn Company | 1128 x 191 | 5.9:1 | Extremely horizontal. Logo overlaps bottom-left. |
| YouTube Channel | 2560 x 1440 | 16:9 | Safe area 1546x423 centered. TV=full, desktop=2560x423, mobile=1546x423. |
| Twitter/X Header | 1500 x 500 | 3:1 | Left 200px obscured by profile photo. Mobile center crop. |

**Full details:** Read `./canvas-design/references/formats.md` for safe zones and typography scales.

---

## Workflow

1. **Read references:**
   - `./canvas-design/references/formats.md` — dimensions and safe zones for chosen platform
   - `./canvas-design/references/color-palettes.md` — palette selection
   - `./canvas-design/references/typography-pairings.md` — font pairing
   - `./canvas-design/references/composition-guide.md` — layout technique
   - `./canvas-design/references/anti-slop-checklist.md` — quality gates
   - `./html-design/references/css-techniques.md` — CSS techniques
   - `./cover-design/references/cover-patterns.md` — platform-specific recipes

2. **Output specification** with format, palette, typography, composition, mood

3. **Design with html-design patterns** — follow the 4-phase process from `html-design` SKILL.md

4. **Render via render-engine** pipeline

---

## Cover-Specific Design Principles

### Ultra-Wide Composition

Covers are dramatically horizontal (2:1 to 5.9:1). Standard composition rules bend:

- **Horizontal flow is king.** The eye moves left-to-right naturally. Place the primary element at the left-third or golden-ratio split.
- **Vertical content gets lost.** Avoid tall, narrow elements. Everything should breathe horizontally.
- **Text must be large and few.** At cover aspect ratios, text smaller than 28px becomes invisible. Use 3-6 words maximum.
- **Safe zones are critical.** Platform overlays (profile photos, titles, navigation) eat significant canvas area.

### Device Cropping

Every platform crops differently on mobile vs desktop vs tablet:

- **Design for the safe zone first.** All critical content must work within the platform's safe area.
- **Decorative elements extend beyond.** Gradient orbs, patterns, and atmospheric effects should fill the full canvas.
- **Test the center crop.** Most mobile views crop to the center. The center 60% of your design must read independently.

### Dark Mode Considerations

GitHub, Twitter/X, and LinkedIn all have dark modes:

- Avoid designs that depend on a white page background for contrast
- Use palette backgrounds rather than relying on the platform's white
- Test that your design maintains contrast in both light and dark contexts

---

## CSS Patterns for Ultra-Wide Layouts

### Horizontal thirds with weight distribution

```css
body {
    display: flex;
    align-items: center;
}
.zone-left {
    width: 38%;
    padding: 60px;
    display: flex;
    flex-direction: column;
    justify-content: center;
}
.zone-center {
    width: 24%;
    display: flex;
    align-items: center;
    justify-content: center;
}
.zone-right {
    width: 38%;
    position: relative;
    overflow: hidden;
}
```

### Gradient horizon line

```css
body::after {
    content: '';
    position: absolute;
    left: 0;
    right: 0;
    top: 55%;
    height: 2px;
    background: linear-gradient(
        90deg,
        transparent 5%,
        var(--accent) 30%,
        var(--accent) 70%,
        transparent 95%
    );
    opacity: 0.3;
}
```

### Panoramic depth layers

```css
.layer-far {
    position: absolute;
    top: 0; left: 0; width: 100%; height: 100%;
    background: var(--bg);
    z-index: 1;
}
.layer-mid {
    position: absolute;
    top: 20%; left: -5%; width: 110%; height: 60%;
    background: linear-gradient(90deg, var(--muted) 0%, transparent 40%, transparent 60%, var(--muted) 100%);
    opacity: 0.3;
    z-index: 2;
}
.layer-near {
    position: absolute;
    top: 0; left: 0; width: 100%; height: 100%;
    z-index: 3;
    /* Content goes here */
}
```

---

## Platform-Specific Tips

### GitHub (1280x640)
- Developer audience expects: code themes, dark palettes, monospace accents
- The `Technical Modern` typography pairing (BigShoulders + JetBrainsMono) works naturally
- Repository name appears below the image — the cover should complement, not repeat it

### Notion (1500x600)
- The page title overlays the bottom-left area — keep that zone decorative only
- Notion users tend toward clean, tasteful aesthetics — glassmorphism and subtle gradients work well
- Cover is draggable, so the design must work even when shifted up or down 50-100px

### LinkedIn (1584x396)
- The profile photo circle sits at bottom-left — critical content must avoid left 260px
- Professional context: avoid overly playful or aggressive design
- Mobile crops aggressively to center ~1080px

### YouTube Banner (2560x1440)
- Only the center 1546x423 is safe across all devices
- Design the safe area first, then extend the atmospheric background to fill 2560x1440
- Bold, vibrant, high-contrast — YouTube thumbnails compete for attention

### Twitter/X Header (1500x500)
- Profile photo overlaps bottom-left ~200px
- Fine detail compresses poorly (JPEG-like artifacts)
- High contrast and bold shapes survive compression better
