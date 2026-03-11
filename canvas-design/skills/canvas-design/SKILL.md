---
name: canvas-design
description: Create museum-quality visual art — covers, posters, social media posts, and compositions in any format with 80+ bundled fonts, procedural noise/textures, advanced blending, and curated color palettes. Use when the user asks to create a poster, cover image, social media graphic, piece of art, banner, or any static visual. Create original visual designs, never copying existing artists' work.
license: Complete terms in LICENSE.txt
---

# Canvas Design — Professional Visual Art Generation

Generate production-grade visual art through a structured 4-phase process. Output `.png` or `.pdf` files alongside a design philosophy `.md` file.

**Complete these 4 phases in order:**
1. Design Specification
2. Design Philosophy
3. Canvas Creation
4. Self-Audit & Refinement

---

## PHASE 1: DESIGN SPECIFICATION

**MANDATORY.** Before any creative work, read the reference documents and output a specification:

- Read `./references/formats.md` for dimensions and safe zones
- Read `./references/color-palettes.md` for curated palettes
- Read `./references/typography-pairings.md` for font combinations
- Read `./references/composition-guide.md` for layout techniques
- Read `./references/anti-slop-checklist.md` for forbidden patterns

Output this specification block:

```
DESIGN SPECIFICATION
====================
FORMAT:      [name + dimensions from formats.md, e.g., "Instagram Square 1080x1080"]
PALETTE:     [name from color-palettes.md OR custom 5-6 hex colors with roles]
TYPOGRAPHY:  [pairing from typography-pairings.md, e.g., "Brutalist: BigShoulders + GeistMono"]
COMPOSITION: [technique from composition-guide.md, e.g., "Rule of Thirds"]
MOOD:        [specific aesthetic — NEVER "modern", "clean", "minimal", "professional"]
```

If the user doesn't specify a format, infer the best one from context. If they say "poster," use A3 or Event Poster. If they say "cover," ask which platform or default to Notion 1500x600. If they say "social media post," ask which platform or default to Instagram Square 1080x1080.

---

## PHASE 2: DESIGN PHILOSOPHY

Create a visual philosophy — an aesthetic manifesto that will be expressed through the artwork.

### THE CRITICAL UNDERSTANDING
- What is received: The user's request as a subtle foundation — it should not constrain creative freedom.
- What is created: A design philosophy/aesthetic movement as a `.md` file.
- What happens next: The philosophy is EXPRESSED VISUALLY — 90% visual design, 10% essential text.

### HOW TO CREATE THE PHILOSOPHY

**Name the movement** (1-2 words): "Brutalist Joy" / "Chromatic Silence" / "Metabolist Dreams"

**Articulate the philosophy** (4-6 paragraphs) covering:
- Space and form
- Color and material
- Scale and rhythm
- Composition and balance
- Visual hierarchy

The philosophy MUST:
- Reference the chosen composition technique from the specification
- Acknowledge the format's constraints (aspect ratio, safe zones)
- Emphasize craftsmanship REPEATEDLY: "meticulously crafted," "product of deep expertise," "painstaking attention," "master-level execution"
- Keep the aesthetic direction generic enough for creative interpretation
- Guide toward VISUAL expression, not text-based communication

### PHILOSOPHY EXAMPLES

**"Concrete Poetry"** — Monumental form, bold geometry, Brutalist spatial divisions, Polish poster energy. Text as rare, powerful gesture. Every element placed with the precision of a master craftsman.

**"Chromatic Language"** — Color as the primary information system. Geometric precision where color zones create meaning. The result of painstaking chromatic calibration.

**"Analog Meditation"** — Quiet visual contemplation through texture and breathing room. Paper grain, ink bleeds, vast negative space. Japanese photobook aesthetic.

**"Organic Systems"** — Natural clustering and modular growth patterns. Rounded forms, organic arrangements. The composition tells the story through expert spatial orchestration.

**"Geometric Silence"** — Pure order and restraint. Grid-based precision, dramatic negative space. Swiss formalism meets Brutalist material honesty.

Output the philosophy as a `.md` file.

### DEDUCING THE SUBTLE REFERENCE

Before creating the canvas, identify the subtle conceptual thread from the request. The topic is a **niche reference embedded within the art** — not literal, always sophisticated. Someone familiar with the subject should feel it intuitively; others simply experience a masterful composition. Think like a jazz musician quoting another song — only those who know will catch it.

---

## PHASE 3: CANVAS CREATION

With specification and philosophy established, create the artwork using Python/Pillow.

### TOOLKIT — Import from `./core/`

The `core/` directory contains professional helper modules. **USE THEM.** Import what you need:

```python
# Procedural noise — organic, non-flat backgrounds
from core.noise import perlin_noise_2d, fractal_noise, turbulence, noise_to_image, flow_field

# Gradients — beyond flat colors
from core.gradients import linear_gradient, radial_gradient, conic_gradient, multi_stop_gradient, noise_gradient

# Textures — depth and tactile quality
from core.textures import grain_overlay, paper_texture, halftone, scanlines, stipple, crosshatch

# Color intelligence — harmony and accessibility
from core.color_engine import hex_to_rgb, rgb_to_hex, tint, shade, complementary, analogous, contrast_ratio, ensure_readable

# Compositing — Photoshop-style blend modes
from core.blending import composite  # modes: "multiply", "screen", "overlay", "soft_light", "hard_light", "color_dodge", "color_burn", "difference"

# Layout — mathematical precision
from core.composition import rule_of_thirds, golden_ratio, fibonacci_spiral, safe_zone, modular_grid, margin_rect, diagonal_armature

# Advanced shapes — beyond PIL primitives
from core.geometry import bezier_curve, wave_line, regular_polygon, star, concentric_circles, parallel_lines, rounded_rect

# Post-processing — professional polish
from core.effects import drop_shadow, outer_glow, vignette, duotone, posterize, color_overlay
```

### MANDATORY REQUIREMENTS

Every canvas MUST use:
1. **At least one texture/noise layer** for depth (grain, paper, noise, halftone). NO flat, untextured outputs.
2. **At least one blend mode** for sophistication (overlay grain, multiply shadows, screen highlights).
3. **Composition module** for focal point placement — use `rule_of_thirds()`, `golden_ratio()`, or `modular_grid()` to position elements precisely.
4. **Safe zones** from the format specification — critical content must stay within margins.
5. **Typography from `./canvas-fonts/`** — load fonts with `ImageFont.truetype("./canvas-fonts/FontName.ttf", size)`.

### TYPOGRAPHY RULES

- **Maximum 2-3 fonts per canvas** (one display, one body, optionally one accent/mono)
- Use the pairing from your specification
- Typography is a VISUAL ELEMENT — integrate it into the composition, don't float it
- Nothing touches canvas edges. Check margins.
- Use different weights for hierarchy (Bold for headings, Regular for body)
- Letter-spacing and size ratios from `typography-pairings.md`

### COLOR RULES

- **Maximum 5-6 colors** from your specification palette
- Use `tint()` and `shade()` for subtle variations within the palette
- Verify text legibility: `contrast_ratio(text_color, bg_color)` must be ≥ 4.5 for body text, ≥ 3.0 for large headings
- Use `ensure_readable()` to auto-adjust if needed

### COMPOSITION PATTERNS

```python
# Pattern 1: Textured noise background
bg = noise_to_image(perlin_noise_2d(W, H, scale=200, seed=42), color_dark, color_light)
grain = grain_overlay(W, H, intensity=0.04, seed=42)
bg = composite(bg, grain, mode="overlay", opacity=0.3)

# Pattern 2: Rich gradient with paper feel
bg = linear_gradient(W, H, color_a, color_b, angle=135)
paper = paper_texture(W, H, base_color=(240, 235, 225), roughness=0.2)
bg = composite(bg, paper, mode="multiply", opacity=0.15)

# Pattern 3: Vignette finish
final = vignette(canvas, intensity=0.4)

# Pattern 4: Duotone treatment
mono = duotone(source_image, dark_color, light_color)

# Pattern 5: Precise element placement
grid = rule_of_thirds(W, H)
focal_x, focal_y = grid["points"][0]  # Top-left intersection
```

### CRAFTSMANSHIP STANDARDS

- Create work that looks like it took countless hours by someone at the absolute top of their field
- Every element must be positioned with mathematical intention
- The composition must reward sustained viewing — dense details that reveal themselves over time
- Use repeating patterns, layered marks, and systematic visual language
- Embrace the paradox of analytical visual language expressing human experience
- Text is always minimal, visual-first, and integrated as a design element
- **IMPORTANT: Search `./canvas-fonts` for available fonts. Use distinctive fonts, never system defaults.**

### OUTPUT

Save as `.png` (default) or `.pdf` alongside the philosophy `.md` file.

```python
img.save("output.png", "PNG", quality=100)
```

---

## PHASE 4: SELF-AUDIT & REFINEMENT

**MANDATORY.** After creating the canvas, run through this checklist before outputting the final file.

### Self-Audit Checklist

Read `./references/anti-slop-checklist.md` and verify:

| # | Check | Pass? |
|---|-------|-------|
| 1 | No text overlaps or clips canvas edges | |
| 2 | Color palette ≤ 5-6 intentional colors | |
| 3 | Clear visual hierarchy (squint test passes) | |
| 4 | Composition technique is recognizable | |
| 5 | At least one texture/noise layer for depth | |
| 6 | At least one blend mode used for sophistication | |
| 7 | Typography used as visual element, not just information | |
| 8 | All critical content within safe zones | |
| 9 | Text contrast ratio ≥ 4.5 (body) / ≥ 3.0 (headings) | |
| 10 | No forbidden patterns (centered text on gradient, purple-blue gradients, etc.) | |

### Refinement Protocol

The user ALREADY said: "It must be pristine, a masterpiece of craftsmanship, as if displayed in a museum."

**To refine: SUBTRACT, don't add.**
- Do NOT add more shapes, filters, or elements
- Instead: tighten spacing, refine color relationships, adjust typography weight
- Ask: "How can I make what's already here more cohesive?"
- Check pixel-level alignment. Check margin consistency. Check color harmony.
- Take a second pass through the code — polish, don't pile on.

Output the final result.

---

## MULTI-PAGE OPTION

When multiple pages are requested, create distinctly different compositions along the same philosophy. Bundle in a single `.pdf` or multiple `.png` files. Treat each page as part of a coffee table book — unique twists on the original theme that tell a visual story. Exercise full creative freedom while maintaining aesthetic cohesion.

---

## QUICK REFERENCE: Available Fonts

**Sans:** Outfit (R/B), WorkSans (R/B/I/BI), InstrumentSans (R/B/I/BI), BricolageGrotesque (R/B), BigShoulders (R/B), Jura (L/M), NationalPark (R/B), SmoochSans (M)

**Serif:** Lora (R/B/I/BI), CrimsonPro (R/B/I), InstrumentSerif (R/I), IBMPlexSerif (R/B/I/BI), LibreBaskerville (R), Italiana (R), YoungSerif (R), Gloock (R)

**Mono:** JetBrainsMono (R/B), IBMPlexMono (R/B), GeistMono (R/B), DMMono (R), RedHatMono (R/B)

**Display:** Boldonse (R), EricaOne (R), Silkscreen (R), PixelifySans (M), PoiretOne (R), Tektur (R/M), ArsenalSC (R), NothingYouCouldDo (R)
