# Anti-Slop Checklist

Quality gates to prevent generic, AI-looking output. Every design must pass through these checks before being considered complete.

---

## Section 1: Pre-Design Specification

Every design MUST begin with a completed specification. Do not start drawing until every field is filled.

```
DESIGN SPECIFICATION
====================
FORMAT:       [name from formats.md — e.g., "Instagram Square 1080x1080"]
PALETTE:      [name from color-palettes.md or custom with 6 hex codes and roles]
TYPOGRAPHY:   [pairing name from typography-pairings.md — e.g., "Editorial Luxe"]
COMPOSITION:  [technique from composition-guide.md — e.g., "Z-Pattern"]
MOOD:         [specific aesthetic — see banned terms below]
TEXTURE:      [at least one: grain, noise, halftone, paper, fabric, concrete, none with justification]
FOCAL POINT:  [describe the single most important element and its position]
```

### Banned Mood Terms

These words are too vague to guide design. Replace them with specific descriptors.

| Banned | Replace With (examples) |
|---|---|
| "modern" | "Swiss grid editorial" or "2024 SaaS dashboard aesthetic" |
| "clean" | "high white-space ratio with sharp type hierarchy" |
| "minimal" | "single-element focus with monochrome palette" |
| "professional" | "corporate-warm with serif authority" |
| "sleek" | "dark UI with chrome accents and thin rules" |
| "aesthetic" | describe the actual aesthetic: "cottagecore", "brutalist", "vaporwave" |
| "beautiful" | describe what makes it beautiful: "golden hour warmth with film grain" |
| "nice" | never |

---

## Section 2: Forbidden Patterns

These patterns instantly make a design look AI-generated, templated, or amateur. Avoid at all costs.

### 1. Centered Text on Gradient Background
**What it looks like:** White sans-serif text dead-centered on a purple-to-blue or pink-to-orange gradient.
**Why it fails:** Default output of every AI design tool. Zero design intent.
**Instead:** Use a composition technique. Offset text. Add texture. Use a defined palette.

### 2. Purple-to-Blue Gradients
**What it looks like:** Linear or radial gradient from violet (#7B2FBE) to blue (#2B7FE0).
**Why it fails:** The #1 most overused AI-generated background. Instantly signals "generated, not designed."
**Instead:** Use a palette from color-palettes.md. If you need a gradient, use adjacent colors within your chosen palette.

### 3. Generic Sans-Serif on Solid Background
**What it looks like:** Default-weight sans-serif (Inter, Helvetica, Arial) on a flat colored rectangle.
**Why it fails:** No typographic personality. No visual hierarchy. Looks like a placeholder.
**Instead:** Use a typography pairing. Apply weight contrast, size contrast, or color contrast.

### 4. Perfect Bilateral Symmetry
**What it looks like:** Everything mirrored exactly on a center axis.
**Why it fails:** Static, lifeless, predictable. The eye has nowhere to explore.
**Instead:** Asymmetric balance. Off-center focal points. Golden ratio divisions.

### 5. Three or More Font Families
**What it looks like:** A headline in one font, body in another, captions in a third, accents in a fourth.
**Why it fails:** Visual chaos. Signals indecision, not sophistication.
**Instead:** Maximum 2 families. Create hierarchy with weight and size, not new fonts.

### 6. Text Touching Canvas Edges
**What it looks like:** Headline or body text that runs right up to (or past) the canvas boundary.
**Why it fails:** Looks like a rendering error. Guarantees clipping on every platform.
**Instead:** Respect safe zones. Use padding from formats.md.

### 7. Flat Shapes With No Texture or Depth
**What it looks like:** Pure flat-colored rectangles, circles, and polygons with no grain, shadow, gradient, or texture.
**Why it fails:** Feels like a wireframe, not a finished design. SVG-icon-as-poster energy.
**Instead:** Add subtle noise/grain (2-5% opacity), a slight inner shadow, or a textured fill.

### 8. Clip-Art Elements Floating in Space
**What it looks like:** Small icons, shapes, or decorative elements scattered with no spatial logic.
**Why it fails:** No relationship between elements. No grounding. Feels random.
**Instead:** Anchor elements to a grid. Group related items. Create visual flow between elements.

### 9. Uniform Rounded Corners Everywhere
**What it looks like:** Every rectangle has the same border-radius (usually 8-16px).
**Why it fails:** UI component aesthetic, not graphic design. Looks like a wireframe mockup.
**Instead:** Mix sharp and rounded. Use rounding intentionally (cards yes, backgrounds no). Vary radii.

### 10. Stock-Photo Color Grading
**What it looks like:** Teal shadows + orange highlights. Desaturated midtones with lifted blacks.
**Why it fails:** Instagram-filter-era cliche. Recognizable and dated.
**Instead:** Grade to your palette. If using photos, apply color overlay or duotone from your defined palette.

### 11. Generic Geometric Patterns Without Purpose
**What it looks like:** Random triangles, hexagons, or dots as a background filler.
**Why it fails:** Decorative without intent. Does not reinforce the message or mood.
**Instead:** If you need a pattern, derive it from the content (data shapes, letter forms, thematic motifs).

### 12. Default Drop Shadows
**What it looks like:** A black or dark gray drop shadow at 45 degrees, ~5px offset, ~10px blur.
**Why it fails:** Looks like PowerPoint 2010. No light source logic. Dated immediately.
**Instead:** If you need depth, use subtle elevation shadows (y-offset only, 0.5-2% opacity, large blur) or colored shadows that match the palette.

### 13. Emoji as Design Elements
**What it looks like:** Standard Unicode emoji used as graphic elements in the composition.
**Why it fails:** Resolution-dependent, platform-inconsistent, and signals low effort.
**Instead:** Draw custom icons or use typographic symbols from the chosen font family.

### 14. Overlapping Transparent Circles
**What it looks like:** 3-5 semi-transparent circles in different colors overlapping in the background.
**Why it fails:** The quintessential "AI thinks this is design" pattern. Meaningless Venn diagram.
**Instead:** Use intentional shapes derived from composition technique or content theme.

---

## Section 3: Self-Audit Checklist

Run every check after completing a design. All must pass.

| # | Check | Pass Criteria |
|---|---|---|
| 1 | **Text Legibility** | All text is fully within the safe zone. No text is clipped, overlapping other text, or touching the canvas edge. |
| 2 | **Color Count** | Maximum 6 colors used (as defined by palette roles). Every color traces back to a role. No rogue hex codes. |
| 3 | **Visual Hierarchy** | Squint at the design at 25% zoom. Can you identify exactly 1 primary element, 1-2 secondary elements, and everything else as background? If everything looks equal, hierarchy has failed. |
| 4 | **Composition Technique** | The stated composition technique is actually applied. Key elements align to the technique's focal points or grid lines. |
| 5 | **Texture and Depth** | At least one non-flat treatment exists: grain, noise, shadow, gradient within palette, texture overlay, or photographic element. Exception: pure Swiss/minimalist designs may be flat with justification. |
| 6 | **Typography as Design** | Type is not just "placed" but actively designed: size contrast, weight contrast, intentional spacing, or alignment to grid. At least one typographic element demonstrates craft. |
| 7 | **Squint Test** | At 25% size, does the composition still read? Are the dark/light zones balanced? Is there a clear focal point? If it becomes a uniform gray blob, contrast has failed. |
| 8 | **Safe Zone Compliance** | All critical content (text, logos, faces, CTAs) falls within the safe zone for the specified format. Decorative elements may extend beyond. |
| 9 | **Contrast Ratios** | Body text on its background: minimum 4.5:1 (WCAG AA). Heading text on its background: minimum 3:1 (AA large text). Check actual hex values, not assumptions. |
| 10 | **Cohesion** | Every element belongs. Remove any element mentally -- if nothing changes, that element should not exist. No orphan decorations. No filler. |

---

## Section 4: Refinement Protocol

When a design needs improvement, follow this protocol. The goal is to refine what exists, not add more.

### Step 1: Diagnose Before Acting

Ask these questions before making any change:

- What is the weakest element in the current design?
- Does the hierarchy read correctly (primary > secondary > tertiary)?
- Is there anything that does not serve the design's stated mood?

### Step 2: Subtract First

Before adding anything new, try removing:

- Remove the weakest element. Does the design improve? Keep it removed.
- Reduce color count by 1. Does it still work? Keep the simpler version.
- Increase white space around the focal point. Better? Keep it.

### Step 3: Adjust, Do Not Add

If subtraction does not solve the problem:

- **Weak hierarchy?** Increase size contrast between heading and body (try 2x or 3x ratio).
- **Flat feeling?** Add a single texture layer at low opacity (3-8% noise or grain).
- **No focal point?** Make one element dramatically larger or darker than everything else.
- **Feels generic?** Check the typography pairing. Swap to a pairing with more personality.
- **Colors feel off?** Verify you are using the palette roles correctly. Background should dominate; accents should be rare.

### Step 4: Never Do These During Refinement

- Do not add a new font family.
- Do not add a new color outside the palette.
- Do not add decorative elements that were not in the original specification.
- Do not center everything as a "fix" for bad composition.
- Do not increase complexity to solve a clarity problem.

### Step 5: Final Pass

After refinement, re-run the Self-Audit Checklist (Section 3). Every check must still pass. If a refinement breaks a previously passing check, revert it.

---

## Quick Reference Card

```
BEFORE DESIGNING:
  [ ] Specification complete (all 7 fields)
  [ ] No banned mood terms
  [ ] Palette, typography, and composition chosen from references

WHILE DESIGNING:
  [ ] Working within safe zone
  [ ] Using composition technique coordinates
  [ ] Maximum 2 font families
  [ ] Maximum 6 palette colors

AFTER DESIGNING:
  [ ] All 10 self-audit checks pass
  [ ] No forbidden patterns present
  [ ] Squint test confirms hierarchy
  [ ] Refinement was subtractive, not additive
```
