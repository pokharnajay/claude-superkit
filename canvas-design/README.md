# Canvas Design v3

Production-grade visual design with HTML/CSS + Playwright rendering. 8 specialized skills, 5 agents, 8 quick commands. Covers, posters, social media, thumbnails, brand assets, and abstract art.

## Installation

```bash
claude plugin marketplace add pokharnajay/claude-superkit
claude plugin install canvas-design@claude-superkit
```

## Rendering Modes

| Mode | Engine | Use For |
|------|--------|---------|
| **HTML/CSS** (primary) | Playwright screenshot | Covers, posters, social media, thumbnails, brand assets |
| **PIL/Pillow** (secondary) | Python image generation | Abstract/generative art |

## Skills (8)

| Skill | Renderer | Purpose |
|-------|----------|---------|
| `html-design` | HTML/CSS | Core design patterns, CSS techniques, rendering pipeline |
| `cover-design` | HTML/CSS | GitHub, Notion, LinkedIn, YouTube, Twitter/X covers |
| `poster-design` | HTML/CSS | Event, movie, concert, print posters |
| `social-media-design` | HTML/CSS | Instagram, LinkedIn, Twitter/X, Facebook, Pinterest |
| `thumbnail-design` | HTML/CSS | YouTube thumbnails, Open Graph images |
| `abstract-art` | PIL | Generative/procedural art (noise, flow fields, particles) |
| `brand-assets` | HTML/CSS | Logos, icons, favicons, brand identity kits |
| `render-engine` | Playwright | HTML to PNG rendering pipeline |

## Agents (5)

| Agent | Role |
|-------|------|
| `design-director` | Main orchestrator — routes to skills and specialists |
| `layout-architect` | Composition, CSS Grid/Flexbox, spatial layout |
| `typography-director` | Font pairing, type scale, text hierarchy |
| `color-specialist` | Palette selection, contrast, color harmony |
| `render-engineer` | Playwright pipeline, font loading, resolution |

## Quick Commands

| Command | Action |
|---------|--------|
| `/quick-cover` | Fast cover generation |
| `/quick-poster` | Fast poster generation |
| `/quick-social` | Fast social media post |
| `/quick-thumbnail` | Fast thumbnail |
| `/quick-abstract` | Fast generative art (PIL) |
| `/render-html` | Screenshot HTML to PNG |
| `/list-fonts` | Show available fonts |
| `/list-palettes` | Show available palettes |

## Resources

- **80+ bundled TTF fonts** — Sans, Serif, Mono, Display categories
- **20 curated color palettes** — Warm, Cool, Earthy, Bold, Refined moods
- **15 typography pairings** — Validated display + body font combinations
- **20+ format presets** — Dimensions, safe zones, typography scales
- **8 composition techniques** — Rule of thirds, golden ratio, grids, etc.
- **CSS techniques catalog** — Glassmorphism, gradient orbs, SVG noise, blend modes, clip-path
- **8 PIL core modules** — Noise, gradients, textures, blending, composition, geometry, effects

## How It Works

1. **HTML/CSS path** (covers, posters, social, thumbnails, brand): Write HTML → Playwright navigates to `file://` URL → resize viewport → screenshot PNG → optional PIL grain overlay
2. **PIL path** (abstract art): Python generates image using core modules → save PNG

Fonts load via `@font-face` with `file://` paths to bundled TTFs. No external dependencies.

## License

MIT
