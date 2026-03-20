---
name: html-design
description: Core HTML/CSS visual design skill. Foundation for all HTML-rendered designs — covers, posters, social media, thumbnails, brand assets. Teaches CSS techniques, rendering pipeline, and design principles. Use for any visual design task.
license: MIT
metadata:
  author: canvas-super-creator
  version: 3.0.0
---

# HTML Design — Core Visual Design Skill

The foundation skill for creating production-grade visual designs using HTML/CSS rendered to PNG via the Playwright pipeline. All format-specific skills (cover-design, poster-design, social-media-design, thumbnail-design, brand-assets) build on this skill.

---

## 4-Phase Workflow

Every design follows these four phases in strict order:

1. **Specification** — Define format, palette, typography, composition, mood
2. **Philosophy** — Create an aesthetic manifesto that guides the visual expression
3. **HTML Creation** — Write HTML/CSS, load fonts, apply techniques, render to PNG
4. **Self-Audit** — Run the anti-slop checklist, verify quality, refine

---

## PHASE 1: DESIGN SPECIFICATION

**MANDATORY.** Before any creative work, read these shared reference documents:

- Read `./canvas-super-creator/references/formats.md` for dimensions and safe zones
- Read `./canvas-super-creator/references/color-palettes.md` for curated palettes
- Read `./canvas-super-creator/references/typography-pairings.md` for font combinations
- Read `./canvas-super-creator/references/composition-guide.md` for layout techniques
- Read `./canvas-super-creator/references/anti-slop-checklist.md` for forbidden patterns

Then read this skill's local references:
- Read `./html-design/references/css-techniques.md` for CSS technique catalog
- Read `./html-design/references/html-templates.md` for starter templates

Output this specification block:

```
DESIGN SPECIFICATION
====================
FORMAT:       [name + dimensions from formats.md, e.g., "Instagram Square 1080x1080"]
PALETTE:      [name from color-palettes.md OR custom 5-6 hex colors with roles]
TYPOGRAPHY:   [pairing from typography-pairings.md, e.g., "Brutalist Statement: Boldonse + WorkSans"]
COMPOSITION:  [technique from composition-guide.md, e.g., "Rule of Thirds"]
MOOD:         [specific aesthetic — NEVER "modern", "clean", "minimal", "professional"]
TEXTURE:      [at least one: grain, noise, halftone, grid pattern, SVG noise]
FOCAL POINT:  [describe the single most important element and its position]
```

If the user does not specify a format, infer the best one from context. Ask for clarification only when genuinely ambiguous.

---

## PHASE 2: DESIGN PHILOSOPHY

Create a visual philosophy — an aesthetic manifesto expressed through the artwork.

### How to Create the Philosophy

**Name the movement** (1-2 words): "Brutalist Joy" / "Chromatic Silence" / "Metabolist Dreams"

**Articulate the philosophy** (4-6 paragraphs) covering:
- Space and form
- Color and material
- Scale and rhythm
- Composition and balance
- Visual hierarchy

The philosophy MUST:
- Reference the chosen composition technique from the specification
- Acknowledge the format constraints (aspect ratio, safe zones)
- Emphasize craftsmanship: "meticulously crafted," "product of deep expertise," "painstaking attention"
- Guide toward VISUAL expression, not text-based communication
- Keep aesthetic direction generic enough for creative interpretation

### Deducing the Subtle Reference

Before creating the design, identify the subtle conceptual thread from the request. The topic is a niche reference embedded within the art — not literal, always sophisticated. Think like a jazz musician quoting another song.

Output the philosophy as a `.md` file alongside the design.

---

## PHASE 3: HTML CREATION

### Step 1: Font Loading

Load fonts from the bundled collection using `@font-face` with `file://` paths.

**Font path base:** `file:///Users/jaypokharna/Desktop/Shared%20Folder/Shared%20Folder/python/claude-skills/canvas-super-creator/skills/canvas-super-creator/canvas-fonts/`

```css
@font-face {
    font-family: 'BigShoulders';
    src: url('file:///Users/jaypokharna/Desktop/Shared%20Folder/Shared%20Folder/python/claude-skills/canvas-super-creator/skills/canvas-super-creator/canvas-fonts/BigShoulders-Bold.ttf') format('truetype');
    font-weight: 700;
    font-style: normal;
}
```

**Typography rules:**
- Maximum 2-3 fonts per design (one display, one body, optionally one mono accent)
- Use the pairing from your specification
- Typography is a VISUAL ELEMENT — integrate it into the composition
- Nothing touches canvas edges — respect safe zones
- Use different weights for hierarchy (Bold headings, Regular body)

### Step 2: HTML Structure

Use the boilerplate from `render-engine` skill or the templates from `html-templates.md`:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <style>
        /* @font-face declarations */
        /* CSS reset: *, *::before, *::after { margin:0; padding:0; box-sizing:border-box; } */
        /* html, body { width: Wpx; height: Hpx; overflow: hidden; } */
        /* Design CSS */
    </style>
</head>
<body>
    <!-- Design markup -->
</body>
</html>
```

### Step 3: Apply CSS Techniques

Reference `css-techniques.md` for the full catalog. Every design MUST use:

1. **At least one texture/depth layer** — SVG noise overlay, gradient mesh, grid pattern, or grain effect. NO flat, untextured outputs.
2. **At least one composition technique** — Rule of thirds positioning, golden ratio splits, diagonal armature alignment.
3. **Safe zones** — All critical content (text, logos) within the margins defined in formats.md.
4. **Contrast checking** — Verify WCAG contrast ratios: body text >= 4.5:1, headings >= 3.0:1.

### Step 4: Color Application

- Maximum 5-6 colors from the specification palette
- Use CSS custom properties for palette consistency:
  ```css
  :root {
      --bg: #1C1210;
      --fg: #F5E6D3;
      --accent: #E8622B;
      --accent2: #C4453D;
      --muted: #3D2B24;
      --highlight: #F5A623;
  }
  ```
- Never use colors outside the palette without justification

### Step 5: Render via Pipeline

Follow the `render-engine` skill pipeline:

1. Write HTML to `/tmp/canvas-super-creator-{timestamp}.html`
2. `mcp__plugin_playwright_playwright__browser_navigate` to `file:///tmp/...`
3. `mcp__plugin_playwright_playwright__browser_resize` to W x H
4. `mcp__plugin_playwright_playwright__browser_take_screenshot`
5. Optional PIL post-processing (grain, vignette)

---

## PHASE 4: SELF-AUDIT & REFINEMENT

**MANDATORY.** After creating the design, verify against the anti-slop checklist:

| # | Check | Pass? |
|---|-------|-------|
| 1 | No text overlaps or clips canvas edges | |
| 2 | Color palette <= 5-6 intentional colors | |
| 3 | Clear visual hierarchy (squint test passes) | |
| 4 | Composition technique is recognizable | |
| 5 | At least one texture/depth layer present | |
| 6 | At least one blend mode or layering technique used | |
| 7 | Typography used as visual element, not just information | |
| 8 | All critical content within safe zones | |
| 9 | Text contrast ratio >= 4.5 (body) / >= 3.0 (headings) | |
| 10 | No forbidden patterns (centered text on gradient, purple-blue gradients, etc.) | |

### Refinement Protocol

**To refine: SUBTRACT, do not add.**
- Do NOT add more shapes, filters, or elements
- Instead: tighten spacing, refine color relationships, adjust typography weight
- Ask: "How can I make what is already here more cohesive?"
- Check pixel-level alignment, margin consistency, color harmony
- Take a second pass through the code — polish, do not pile on

---

## Available Fonts Quick Reference

**Sans:** Outfit (R/B), WorkSans (R/B/I/BI), InstrumentSans (R/B/I/BI), BricolageGrotesque (R/B), BigShoulders (R/B), Jura (L/M), NationalPark (R/B), SmoochSans (M)

**Serif:** Lora (R/B/I/BI), CrimsonPro (R/B/I), InstrumentSerif (R/I), IBMPlexSerif (R/B/I/BI), LibreBaskerville (R), Italiana (R), YoungSerif (R), Gloock (R)

**Mono:** JetBrainsMono (R/B), IBMPlexMono (R/B), GeistMono (R/B), DMMono (R), RedHatMono (R/B)

**Display:** Boldonse (R), EricaOne (R), Silkscreen (R), PixelifySans (M), PoiretOne (R), Tektur (R/M), ArsenalSC (R), NothingYouCouldDo (R)

---

## Anti-Patterns — NEVER Do These

- **No Bootstrap/Tailwind defaults** — No uniform rounded corners, no default shadows, no component library aesthetic
- **No uniform border-radius** — Mix sharp and rounded intentionally
- **No Inter/Roboto/Arial** — These are not in the bundled collection. Use the bundled fonts only.
- **No purple-to-blue gradients** — The #1 AI-generated background cliche
- **No centered text on gradient** — Zero design intent
- **No flat untextured backgrounds** — Always add depth (noise, grain, mesh, pattern)
- **No more than 6 colors** — Every color must trace to a palette role
- **No emoji as design elements** — Draw custom shapes or use typographic symbols
