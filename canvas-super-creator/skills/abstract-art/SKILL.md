---
name: abstract-art
description: Generative and procedural art using Python/Pillow. Use when user asks for abstract art, generative design, algorithmic art, or pattern-based compositions.
license: MIT
metadata:
  author: canvas-super-creator
  version: 3.0.0
---

# Abstract Art — Generative & Procedural Design

Create generative, algorithmic, and procedural art using Python and Pillow (PIL). This skill produces visual art through mathematical systems, noise functions, particle simulations, and geometric algorithms rather than HTML/CSS rendering.

---

## When to Use This Skill

Use `abstract-art` when the user asks for:
- Abstract or generative art
- Algorithmic patterns or procedural textures
- Mathematical visualizations (Fibonacci, Voronoi, flow fields)
- Organic textures and noise-based compositions
- Art that emerges from code rather than layout

For HTML/CSS-based designs (covers, posters, social media), use `html-design` or the format-specific skills instead.

---

## Core Toolkit

The `core/` directory (located at `./canvas-super-creator/core/`) contains professional PIL helper modules. Import what you need:

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

---

## 4-Phase Workflow

The design philosophy approach applies equally to generative art:

### Phase 1: Specification

```
DESIGN SPECIFICATION
====================
FORMAT:       [dimensions, e.g., "Square 2000x2000" or "A3 Portrait 3508x4961"]
PALETTE:      [from color-palettes.md OR custom 5-6 hex colors]
ALGORITHM:    [primary generative technique: flow field, Voronoi, particles, noise, etc.]
COMPOSITION:  [from composition-guide.md: golden ratio, rule of thirds, etc.]
MOOD:         [specific aesthetic: "mathematical precision", "organic chaos", "crystalline order"]
LAYERS:       [number and types: noise base + particle trace + grain overlay]
```

### Phase 2: Design Philosophy

Create an aesthetic manifesto as with any design. Generative art benefits from a strong conceptual framework:

- What mathematical system is being explored?
- What natural phenomenon is being referenced?
- What tension exists between order and chaos?
- How does the algorithm express the philosophy?

### Phase 3: Creation

Write Python code using PIL and the core/ modules. Follow these principles:

- **Seed everything.** Use explicit random seeds for reproducibility.
- **Layer composites.** Build 3-5 layers and blend them together.
- **Add texture last.** Grain and paper texture as the final overlay.
- **Use the composition module.** Even generative art benefits from focal point placement.

### Phase 4: Self-Audit

- Does the piece have a clear focal area?
- Is the color palette coherent (max 5-6 colors)?
- Does it have depth (multiple layers, texture, varied opacity)?
- Does the composition technique guide the eye?
- Would it hold up at gallery scale?

---

## Algorithm Categories

### Noise-Based

Organic textures and landscapes using Perlin noise and fractal variations:

```python
noise = perlin_noise_2d(W, H, scale=200, seed=42)
img = noise_to_image(noise, color_dark, color_light)
```

### Flow Fields

Directional particle traces following a vector field:

```python
field = flow_field(W, H, scale=100, seed=42)
# Trace particles through the field
```

### Particle Systems

Scattered elements with controlled randomness:

```python
import random
random.seed(42)
for _ in range(5000):
    x = random.gauss(W/2, W/6)
    y = random.gauss(H/2, H/6)
    r = random.uniform(1, 4)
    opacity = random.randint(20, 80)
    # Draw particle
```

### Geometric Systems

Mathematical curves, tessellations, and repeating structures:

```python
from core.geometry import regular_polygon, bezier_curve, concentric_circles
```

### Voronoi Tessellation

Cell-based divisions of space:

```python
# Generate random sites, compute Voronoi cells, fill with palette colors
```

### Reaction-Diffusion

Turing patterns and emergent biological forms (requires iterative simulation).

---

## Design Principles for Generative Art

1. **Constraint breeds creativity.** Limit your palette, limit your algorithm, limit your parameters. Constraint produces coherence.
2. **Imperfection is beauty.** Add noise, jitter, and variance. Perfect geometric repetition looks mechanical. Slight randomness looks alive.
3. **Density rewards viewing.** The best generative art reveals detail at every zoom level. Use thousands of elements, not dozens.
4. **Composition still matters.** Even random-looking art should have focal areas. Use the composition module to weight element density.
5. **Color is 80% of the impact.** A mediocre algorithm with a great palette looks better than a great algorithm with bad colors.

---

## Output

Save as PNG (default) or PDF:

```python
img.save("output.png", "PNG", quality=100)
```

For multi-page generative series, save each as a separate PNG or combine into a PDF.

---

## Reference

See `./abstract-art/references/generative-patterns.md` for a catalog of algorithms with complete Python code examples.

See `./canvas-super-creator/references/` for shared design references (palettes, typography, composition, formats).
