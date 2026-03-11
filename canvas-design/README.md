# Canvas Design

Museum-quality visual art generation — covers, posters, social media posts in 20+ formats with 80+ fonts, procedural noise/textures, advanced blending, curated palettes, and composition frameworks.

## Installation

```bash
# Add marketplace (one-time)
claude plugin marketplace add pokharnajay/claude-superkit

# Install plugin
claude plugin install canvas-design@claude-superkit
```

## What It Does

Generates production-grade visual art through a structured 4-phase process:

1. **Design Specification** — select format, palette, typography, composition, and mood
2. **Design Philosophy** — generate an aesthetic manifesto as a `.md` file
3. **Canvas Creation** — express the philosophy as a `.png` or `.pdf` using Python/Pillow + core modules
4. **Self-Audit** — run quality gates to prevent generic AI-looking output

## Supported Formats (20+)

| Category | Formats |
|----------|---------|
| **Covers** | GitHub (1280x640), Notion (1500x600), LinkedIn Personal (1584x396), LinkedIn Company (1128x191), YouTube Banner (2560x1440), Twitter/X Header (1500x500) |
| **Social Media** | Instagram Square (1080x1080), Instagram Story (1080x1920), LinkedIn Post (1200x627), Twitter/X Post (1600x900), Facebook Post (1200x630), Pinterest Pin (1000x1500) |
| **Posters** | A3 (3508x4961), A4 (2480x3508), US Letter (2550x3300), Movie Poster (2700x4000), Event Poster (3300x5100) |
| **Thumbnails** | YouTube (1280x720), Open Graph (1200x630) |

## Core Modules

8 Python helper modules (PIL + numpy only, zero extra dependencies):

| Module | Purpose |
|--------|---------|
| `noise.py` | Perlin noise, fractal noise, turbulence, flow fields |
| `gradients.py` | Linear, radial, conic, multi-stop, noise-distorted gradients |
| `textures.py` | Film grain, paper, halftone, scanlines, stipple, crosshatch |
| `color_engine.py` | Color conversion, harmony, WCAG contrast checking |
| `blending.py` | 8 Photoshop-style blend modes (multiply, screen, overlay, etc.) |
| `composition.py` | Rule of thirds, golden ratio, Fibonacci spiral, grids, safe zones |
| `geometry.py` | Bezier curves, wave lines, polygons, stars, concentric circles |
| `effects.py` | Drop shadows, glows, vignettes, duotone, posterize |

## Reference System

5 curated reference documents:

| Reference | Contents |
|-----------|----------|
| `formats.md` | 20+ format presets with dimensions, safe zones, typography scales |
| `color-palettes.md` | 20 curated palettes (Warm, Cool, Earthy, Bold, Refined) |
| `typography-pairings.md` | 15 validated font pairings from the bundled collection |
| `composition-guide.md` | 8 composition techniques with Python coordinate formulas |
| `anti-slop-checklist.md` | Forbidden patterns, mandatory self-audit, refinement protocol |

## Bundled Fonts (80+)

| Category | Fonts |
|----------|-------|
| **Sans-serif** | Outfit, Work Sans, Instrument Sans, Bricolage Grotesque, Big Shoulders, Jura, National Park, Smooch Sans |
| **Serif** | Lora, Crimson Pro, Instrument Serif, IBM Plex Serif, Libre Baskerville, Italiana, Young Serif, Gloock |
| **Monospace** | JetBrains Mono, IBM Plex Mono, Geist Mono, DM Mono, Red Hat Mono |
| **Display** | Boldonse, Erica One, Silkscreen, Pixelify Sans, Poiret One, Tektur, Arsenal SC, Nothing You Could Do |

## Usage Examples

```
> Create a cover image for my GitHub repo
> Design an Instagram post for a product launch
> Make a movie poster for a sci-fi film
> Create a YouTube thumbnail for a coding tutorial
> Design an event poster for a tech conference
```

## License

MIT
