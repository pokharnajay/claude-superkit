---
name: canvas-super-creator
description: World-class graphic design skill bundle. Routes to 12 specialized skills for covers, posters, social media, thumbnails, brand assets, billboards, magazines, ad campaigns, carousels, and abstract art. 120+ fonts, 25 palettes, advanced CSS/SVG techniques.
license: MIT
metadata:
  author: canvas-super-creator
  version: 4.0.0
---

# Canvas Super Creator — Skill Router (v4)

This skill routes design requests to 12 specialized sub-skills. Each skill focuses on a specific design category with dedicated techniques, references, and CSS patterns.

**This file serves as a router.** Use the appropriate specialized skill below based on the task.

---

## Specialized Skills (12)

| Skill | Use When |
|---|---|
| **html-design** | Any HTML/CSS visual design task. Core foundation for all HTML-rendered designs. Start here for general design requests. |
| **render-engine** | Converting HTML to PNG via Playwright. Font loading, pipeline troubleshooting. |
| **cover-design** | GitHub, Notion, LinkedIn, YouTube, Twitter/X covers and banners. |
| **poster-design** | Event posters, movie posters, concert flyers, gallery pieces. |
| **social-media-design** | Instagram, LinkedIn, Twitter/X, Facebook, Pinterest posts and cards. |
| **thumbnail-design** | YouTube thumbnails and Open Graph (OG) images. |
| **billboard-design** | Highway billboards, bus shelter ads, transit ads, outdoor advertising. |
| **magazine-design** | Magazine covers, editorial spreads, multi-column layouts. |
| **ad-campaign-design** | Digital ad banners (IAB sizes), Google/Facebook ads, multi-size campaigns. |
| **carousel-design** | Instagram/LinkedIn carousels with storyline arcs and visual continuity. |
| **abstract-art** | Generative/procedural art using Python/Pillow. Noise fields, flow fields, particles, Voronoi. |
| **brand-assets** | Logo marks, app icons, favicons, brand identity kits. |

---

## Routing Guide

**User says "make me a cover"** → `cover-design`
**User says "create a poster"** → `poster-design`
**User says "Instagram post"** → `social-media-design`
**User says "YouTube thumbnail"** → `thumbnail-design`
**User says "design a logo"** → `brand-assets`
**User says "billboard" or "outdoor ad"** → `billboard-design`
**User says "magazine" or "editorial"** → `magazine-design`
**User says "ad banner" or "display ad"** → `ad-campaign-design`
**User says "carousel" or "multi-slide"** → `carousel-design`
**User says "abstract art" or "generative"** → `abstract-art`
**User says "design" (general)** → `html-design`
**User has rendering issues** → `render-engine`

### Multi-Piece Requests

For carousels, campaigns, or any multi-deliverable project:
1. Invoke **creative-director** agent first (for concept and creative brief)
2. Invoke **strategic-planner** agent (for production plan and visual system)
3. Then execute the appropriate skill(s)

---

## Agents (7)

| Agent | Role |
|---|---|
| **creative-director** | Creative brain — writes briefs, develops concepts, finds visual metaphors, rejects generic ideas. Invoke BEFORE complex/ambiguous/multi-piece work. |
| **strategic-planner** | Production coordinator — defines visual systems, creates execution plans, manages multi-piece consistency. |
| **design-director** | Orchestrator — routes to skills and agents, oversees quality. |
| **layout-architect** | Composition, CSS Grid/Flexbox, spatial layout. |
| **typography-director** | Font pairing, type scale, text hierarchy. |
| **color-specialist** | Palette, contrast, color harmony. |
| **render-engineer** | Playwright pipeline, font loading, resolution. |

---

## Shared Resources

### canvas-fonts/

The bundled font collection (120+ fonts) used by all HTML-based skills. Located at:

```
./canvas-super-creator/canvas-fonts/
```

Font categories:
- **Sans:** Outfit, WorkSans, InstrumentSans, BricolageGrotesque, BigShoulders, Jura, NationalPark, SmoochSans, Montserrat, Poppins, SpaceGrotesk, PlusJakartaSans, DMSans, Manrope, Inter, Sora
- **Serif:** Lora, CrimsonPro, InstrumentSerif, IBMPlexSerif, LibreBaskerville, Italiana, YoungSerif, Gloock, PlayfairDisplay, CormorantGaramond, DMSerifDisplay, LibreCaslonText, Spectral
- **Mono:** JetBrainsMono, IBMPlexMono, GeistMono, DMMono, RedHatMono
- **Display:** Boldonse, EricaOne, Silkscreen, PixelifySans, PoiretOne, Tektur, ArsenalSC, NothingYouCouldDo, BebasNeue, Anton, Oswald, Arvo, BlackOpsOne, Righteous, Bungee, PermanentMarker
- **Playful:** Fredoka, Bangers, Baloo2, BubblegumSans
- **Handwritten:** Caveat, DancingScript, Pacifico, Sacramento, Satisfy, Kalam

### core/

Python/Pillow helper modules for generative art. Used by `abstract-art` skill. Located at:

```
./canvas-super-creator/core/
```

Modules: `noise`, `gradients`, `textures`, `color_engine`, `blending`, `composition`, `geometry`, `effects`

### references/

Shared design reference documents used by all skills. Located at:

```
./canvas-super-creator/references/
```

| Document | Contents |
|---|---|
| `formats.md` | Canvas dimensions, safe zones, typography scales for all platforms |
| `color-palettes.md` | 25 curated palettes with WCAG contrast guidance |
| `typography-pairings.md` | 23 validated font pairings with weight/spacing guidance |
| `composition-guide.md` | Layout techniques with coordinate math (rule of thirds, golden ratio, etc.) |
| `anti-slop-checklist.md` | Quality gates, forbidden patterns, self-audit checklist |
| `svg-filters.md` | SVG filter recipes: paper texture, grain, watercolor, glass distortion, marble |
| `mesh-gradients.md` | CSS mesh gradient simulation — 10 presets with overlapping radial gradients |
| `clip-path-library.md` | 25+ creative CSS clip-path shapes: geometric, organic, diagonal cuts |
| `backdrop-effects.md` | 6 glass effect recipes: frosted, tinted, iced, holographic, smoke, crystal |
| `blend-mode-recipes.md` | 8 multi-layer blend mode compositions: duotone, light leaks, neon glow |
| `text-effects.md` | Advanced text CSS: 3D, neon, chrome, letterpress, glitch, gradient, knockout |
| `halftone-patterns.md` | CSS halftone techniques: dot, line, cross, circular, CMYK |
| `svg-patterns.md` | 10 inline SVG texture patterns: dots, lines, waves, hexagons, circuits |
| `cdn-libraries.md` | p5.js, three.js, rough.js, anime.js, GSAP — CDN usage for advanced effects |
| `remotion-bridge.md` | Integration guide for using canvas-super-creator with remotion-super-creator |

---

## For HTML/CSS Workflow

Start with `html-design` skill, which teaches:
1. The 4-phase design process (Specification, Philosophy, HTML Creation, Self-Audit)
2. CSS techniques catalog (`html-design/references/css-techniques.md`)
3. HTML starter templates (`html-design/references/html-templates.md`)
4. Font loading via `@font-face` with `file://` paths
5. Rendering via the `render-engine` pipeline

## For PIL/Pillow Workflow

Start with `abstract-art` skill, which teaches:
1. Using the `core/` module library
2. Generative algorithm catalog (`abstract-art/references/generative-patterns.md`)
3. Noise, flow fields, particles, Voronoi, and geometric patterns
4. Layer compositing with blend modes
5. The same 4-phase design process adapted for procedural art
