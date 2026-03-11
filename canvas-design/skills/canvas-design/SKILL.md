---
name: canvas-design
description: Legacy canvas-design skill — now split into specialized skills. Routes to the appropriate skill based on the design task. Shared resources (fonts, core modules, reference docs) remain here.
license: MIT
metadata:
  author: canvas-design
  version: 3.0.0
---

# Canvas Design — Skill Router (v3)

This skill has been restructured into specialized sub-skills for v3. Each skill focuses on a specific design category with dedicated techniques, references, and CSS patterns.

**This file serves as a router.** Use the appropriate specialized skill below based on the task.

---

## Specialized Skills

| Skill | Use When |
|---|---|
| **html-design** | Any HTML/CSS visual design task. Core foundation for all HTML-rendered designs. Start here for general design requests. |
| **render-engine** | Converting HTML to PNG via Playwright. Font loading, pipeline troubleshooting. |
| **cover-design** | GitHub, Notion, LinkedIn, YouTube, Twitter/X covers and banners. |
| **poster-design** | Event posters, movie posters, concert flyers, gallery pieces. |
| **social-media-design** | Instagram, LinkedIn, Twitter/X, Facebook, Pinterest posts and cards. |
| **thumbnail-design** | YouTube thumbnails and Open Graph (OG) images. |
| **abstract-art** | Generative/procedural art using Python/Pillow. Noise fields, flow fields, particles, Voronoi. |
| **brand-assets** | Logo marks, app icons, favicons, brand identity kits. |

---

## Routing Guide

**User says "make me a cover"** → `cover-design`
**User says "create a poster"** → `poster-design`
**User says "Instagram post"** → `social-media-design`
**User says "YouTube thumbnail"** → `thumbnail-design`
**User says "design a logo"** → `brand-assets`
**User says "abstract art" or "generative"** → `abstract-art`
**User says "design" (general)** → `html-design`
**User has rendering issues** → `render-engine`

---

## Shared Resources (Remain Here)

### canvas-fonts/

The bundled font collection (80+ fonts) used by all HTML-based skills. Located at:

```
./canvas-design/canvas-fonts/
```

Font categories:
- **Sans:** Outfit, WorkSans, InstrumentSans, BricolageGrotesque, BigShoulders, Jura, NationalPark, SmoochSans
- **Serif:** Lora, CrimsonPro, InstrumentSerif, IBMPlexSerif, LibreBaskerville, Italiana, YoungSerif, Gloock
- **Mono:** JetBrainsMono, IBMPlexMono, GeistMono, DMMono, RedHatMono
- **Display:** Boldonse, EricaOne, Silkscreen, PixelifySans, PoiretOne, Tektur, ArsenalSC, NothingYouCouldDo

### core/

Python/Pillow helper modules for generative art. Used by `abstract-art` skill. Located at:

```
./canvas-design/core/
```

Modules: `noise`, `gradients`, `textures`, `color_engine`, `blending`, `composition`, `geometry`, `effects`

### references/

Shared design reference documents used by all skills. Located at:

```
./canvas-design/references/
```

| Document | Contents |
|---|---|
| `formats.md` | Canvas dimensions, safe zones, typography scales for all platforms |
| `color-palettes.md` | 20 curated palettes with WCAG contrast guidance |
| `typography-pairings.md` | 15 validated font pairings with weight/spacing guidance |
| `composition-guide.md` | Layout techniques with coordinate math (rule of thirds, golden ratio, etc.) |
| `anti-slop-checklist.md` | Quality gates, forbidden patterns, self-audit checklist |

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
