---
name: brand-assets
description: Logo marks, app icons, favicons, brand identity kits. Use when user asks for a logo, icon, brand assets, or visual identity.
license: MIT
metadata:
  author: canvas-design
  version: 3.0.0
---

# Brand Assets — Logos, Icons & Visual Identity

Create logo marks, app icons, favicons, and brand identity elements. Brand assets must work at multiple sizes (from 16px favicon to 1024px app store icon), maintain legibility in monochrome, and express brand personality through pure geometric and typographic form.

---

## Asset Types

| Asset | Primary Size | Min Size | Key Constraint |
|---|---|---|---|
| Logo Mark | 512 x 512 | 48 x 48 | Must read at 48px. No fine detail. |
| Wordmark | 800 x 200 | 120 x 30 | Text only. Legibility above all. |
| App Icon | 1024 x 1024 | 16 x 16 | Rounded corners applied by OS. Center content in 80% safe area. |
| Favicon | 32 x 32 (design at 512x512) | 16 x 16 | Ultra-simple. 1-2 elements max. |
| Brand Mark Combo | 1200 x 400 | 200 x 67 | Icon + wordmark. Horizontal lock-up. |

---

## Workflow

1. **Read references:**
   - `./canvas-design/references/color-palettes.md` — brand palette
   - `./canvas-design/references/typography-pairings.md` — font selection
   - `./canvas-design/references/anti-slop-checklist.md` — quality gates
   - `./html-design/references/css-techniques.md` — CSS shape techniques
   - `./brand-assets/references/brand-patterns.md` — brand-specific recipes

2. **Output specification:**
   ```
   BRAND SPECIFICATION
   ===================
   BRAND NAME:    [name]
   ASSET TYPE:    [logo mark / wordmark / app icon / favicon / full kit]
   PALETTE:       [3-4 colors max: primary, secondary, background, accent]
   TYPOGRAPHY:    [primary font family for wordmark/logotype]
   STYLE:         [geometric / organic / minimal / bold / playful]
   VARIANTS:      [color on light, color on dark, monochrome, outlined]
   ```

3. **Design using geometric CSS shapes** or **PIL/Pillow** for more complex marks

4. **Render at multiple sizes** to verify scalability

5. **Test monochrome variant** — the mark must work in single-color

---

## Design Principles for Brand Assets

### Geometric Construction

Every brand mark should be built from deliberate geometric relationships:

- **Circle-based construction.** Most iconic logos sit within or derive from circles.
- **Golden ratio proportions.** Use phi (1.618) for width/height relationships.
- **Grid alignment.** Design on a visible grid (8x8, 16x16, or 32x32 units).
- **Optical corrections.** Round shapes need to extend ~3% beyond the grid to appear the same size as squares.

### The Multi-Size Test

Brand assets must work at every size. Test your design at:

- **1024px** — full detail, app store
- **512px** — standard logo usage
- **128px** — social media avatar
- **48px** — small UI element
- **32px** — favicon
- **16px** — absolute minimum (favicon in tab bar)

If any element disappears or becomes confusing below 48px, simplify.

### Color Variants

Every brand mark must exist in at least 3 variants:

1. **Full color on light background** — primary brand usage
2. **Full color on dark background** — dark mode / dark surfaces
3. **Monochrome** — single color (typically black or white) for legal docs, embossing, watermarks

### CSS Shapes for Logo Construction

Brand marks can be built entirely with CSS geometric primitives:

```css
/* Circle */
.circle { border-radius: 50%; }

/* Rounded square (app icon shape) */
.squircle { border-radius: 22.37%; } /* iOS icon radius */

/* Triangle via clip-path */
.triangle { clip-path: polygon(50% 0%, 0% 100%, 100% 100%); }

/* Hexagon */
.hex { clip-path: polygon(25% 0%, 75% 0%, 100% 50%, 75% 100%, 25% 100%, 0% 50%); }

/* Custom SVG path in CSS */
.custom-shape { clip-path: path('M10,10 L90,10 L90,90 L10,90 Z'); }
```

### SVG in HTML for Complex Marks

For marks requiring curves, use inline SVG within the HTML design:

```html
<svg viewBox="0 0 100 100" width="400" height="400">
    <circle cx="50" cy="50" r="45" fill="none" stroke="#E8622B" stroke-width="3"/>
    <path d="M30,50 Q50,20 70,50 Q50,80 30,50" fill="#E8622B"/>
</svg>
```

---

## Typography for Brand

### Wordmark Guidelines

- Choose a single font family with personality
- Modify letter-spacing for uniqueness (-0.05em to 0.15em range)
- Consider customizing 1-2 letterforms (extending a stroke, rounding a corner)
- Never use more than 1 font in a wordmark
- Test at small sizes — if letters merge or become ambiguous, adjust spacing

### Recommended Wordmark Fonts

| Font | Character | Best For |
|---|---|---|
| BricolageGrotesque Bold | Friendly authority | Tech, SaaS, startups |
| BigShoulders Bold | Industrial strength | Dev tools, hardware, sports |
| InstrumentSerif | Elegant refinement | Luxury, editorial, fashion |
| Tektur Medium | Technical future | Aerospace, science, gaming |
| YoungSerif | Bold confidence | Media, publishing, food |
| Outfit Bold | Clean versatility | General purpose, apps |
| PoiretOne | Geometric elegance | Art deco, luxury, events |

---

## App Icon Specifics

App icons have platform-specific requirements:

### iOS / macOS
- Icon is masked to a squircle (continuous corner curve)
- Design at 1024x1024, keep critical content within center 80% (820x820)
- No transparency — icon must have a solid background
- Avoid text in icons (too small to read in most contexts)

### Android
- Adaptive icon: foreground (72x72dp) + background (108x108dp)
- Design at 1024x1024 with circular safe zone (center 66%)
- Background can be a solid color or simple pattern
- Foreground should be a simple mark with transparency

### Design Pattern

```css
.app-icon {
    width: 1024px;
    height: 1024px;
    border-radius: 227px; /* iOS squircle approximation: 22.17% */
    background: var(--brand-primary);
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
}
.icon-mark {
    width: 60%;
    height: 60%;
    /* Your logo mark goes here */
}
```

---

## Favicon Specifics

Favicons must be ultra-simple:

- Design at 512x512 or 256x256, then verify at 32x32 and 16x16
- Maximum 1-2 elements (letter + shape, or single symbol)
- Bold fills, no thin strokes (they disappear at 16px)
- High contrast against both light and dark tab bar backgrounds
- Consider using just the first letter of the brand name in a distinctive color

---

## Anti-Patterns for Brand Assets

- **Too much detail.** If it does not read at 48px, it is too complex.
- **Gradients that flatten at small sizes.** Use flat colors or minimal gradients.
- **Text in icons.** Words become illegible below 128px.
- **Thin strokes.** Lines under 3% of the total size disappear at small renders.
- **Trendy effects.** Shadows, glows, and 3D effects date quickly. Flat geometric marks age well.
- **Too many colors.** Brand marks should use 2-3 colors maximum.
