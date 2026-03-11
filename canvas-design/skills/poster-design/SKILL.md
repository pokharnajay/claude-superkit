---
name: poster-design
description: Event posters, movie posters, concert flyers, gallery pieces. Use when user asks for a poster, flyer, or large-format print design.
license: MIT
metadata:
  author: canvas-design
  version: 3.0.0
---

# Poster Design — Large-Format Visual Compositions

Create dramatic, high-impact posters for events, films, concerts, exhibitions, and gallery display. Posters demand bold scale, commanding typography, and layered compositions that reward sustained viewing.

---

## Format Quick Reference

| Format | Dimensions (px) | DPI | Typography Scale |
|---|---|---|---|
| A3 Portrait | 3508 x 4961 | 300 | Heading: 144pt, Sub: 72pt, Body: 36pt |
| A4 Portrait | 2480 x 3508 | 300 | Heading: 96pt, Sub: 56pt, Body: 28pt |
| US Letter | 2550 x 3300 | 300 | Heading: 96pt, Sub: 56pt, Body: 28pt |
| Movie Poster 27x40 | 2700 x 4000 | ~100 | Heading: 120pt, Sub: 64pt, Body: 32pt |
| Event Poster 11x17 | 3300 x 5100 | 300 | Heading: 128pt, Sub: 68pt, Body: 34pt |

**Full details:** Read `./canvas-design/references/formats.md` for safe zones and bleed areas.

---

## Workflow

1. **Read references:**
   - `./canvas-design/references/formats.md` — dimensions, safe zones, bleed
   - `./canvas-design/references/color-palettes.md` — palette selection
   - `./canvas-design/references/typography-pairings.md` — font pairing
   - `./canvas-design/references/composition-guide.md` — layout technique
   - `./canvas-design/references/anti-slop-checklist.md` — quality gates
   - `./html-design/references/css-techniques.md` — CSS technique catalog
   - `./poster-design/references/poster-patterns.md` — poster-specific recipes

2. **Output specification** with format, palette, typography, composition, mood

3. **Create design philosophy** — posters demand a strong aesthetic manifesto

4. **Design with html-design patterns** — follow the 4-phase process

5. **Render via render-engine** pipeline

---

## Poster-Specific Design Principles

### Dramatic Typography

Posters are the arena where typography becomes architecture:

- **Display sizes: 120-200px.** Headings on posters should dominate. They are the first thing seen from across a room.
- **Weight extremes.** Use the heaviest available weight for display text. Pair with the lightest for contrast.
- **Tight tracking on display.** Letter-spacing of -0.03em to -0.05em creates density and impact at large sizes.
- **Wide tracking on labels.** Caps labels and meta text should be 0.12-0.20em for airiness.
- **Typographic hierarchy must survive distance.** The title should read at 3 meters. The subtitle at 1.5 meters. Body text at arm's length.

### 5+ Layer Compositions

Posters require depth. Build compositions with distinct visual layers:

1. **Background atmosphere** — gradient, mesh, texture, or full-bleed color
2. **Midground structure** — geometric shapes, color blocks, image treatments
3. **Foreground content** — typography, icons, key visual elements
4. **Texture overlay** — noise, grain, halftone, paper texture
5. **Accent details** — rules, dots, small decorative geometry

### Poster-Specific CSS Techniques

**Dramatic scale contrast:**
```css
.poster-title {
    font-size: 160px;
    line-height: 0.9;
    letter-spacing: -0.04em;
}
.poster-subtitle {
    font-size: 24px;
    letter-spacing: 0.15em;
    text-transform: uppercase;
}
/* Size ratio: 6.7:1 — creates extreme hierarchy */
```

**Full-bleed type that bleeds off edges:**
```css
.bleed-type {
    font-size: 300px;
    position: absolute;
    bottom: -40px;
    left: -20px;
    color: rgba(255, 255, 255, 0.03);
    line-height: 0.8;
    white-space: nowrap;
    pointer-events: none;
}
```

**Vertical text for sidebars:**
```css
.vertical-text {
    writing-mode: vertical-rl;
    text-orientation: mixed;
    font-size: 12px;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    position: absolute;
    right: 40px;
    top: 50%;
    transform: translateY(-50%);
}
```

**Credits block (movie poster style):**
```css
.credits-block {
    position: absolute;
    bottom: 80px;
    left: 80px;
    right: 80px;
}
.credits-block .title-credits {
    font-family: 'DMMono', monospace;
    font-size: 10px;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: var(--fg);
    opacity: 0.4;
    line-height: 2;
}
.credits-block .separator {
    width: 100%;
    height: 1px;
    background: var(--muted);
    margin: 16px 0;
}
```

---

## Composition for Posters

Posters are vertical — this changes composition fundamentally:

- **Diagonal Armature** works exceptionally well for dynamic energy
- **Rule of Thirds** — the top-third intersection is the power position for poster titles
- **Asymmetric Balance** — a large visual element counterbalanced by smaller text blocks
- **Modular Grid** — useful for event posters with multiple information blocks (date, venue, performers)
- **F-Pattern** — natural for event information: headliner at top, details below

### The Poster "Zones"

```
+----------------------------+
|  VISUAL IMPACT ZONE (top)  |  <- Main visual, hero image, or dramatic type
|  40% of height             |
+----------------------------+
|  INFORMATION ZONE (middle) |  <- Title, subtitle, key details
|  35% of height             |
+----------------------------+
|  DETAILS ZONE (bottom)     |  <- Date, venue, credits, sponsors
|  25% of height             |
+----------------------------+
```

This is a guideline, not a rule. The best posters deliberately break this structure.

---

## Anti-Patterns Specific to Posters

- **Evenly distributed elements.** Posters need dramatic concentration and breathing room, not uniform spacing.
- **Small, timid typography.** If the headline is under 80px on an A3, it is too small.
- **Centered-everything layout.** Center alignment is static. Use it intentionally for one element, not all of them.
- **Too many competing elements.** A poster is a billboard, not a brochure. One hero element, one message.
- **Ignoring the bottom 25%.** The credits/details zone needs as much design attention as the top.
