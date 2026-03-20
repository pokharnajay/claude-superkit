# Generative Art — Algorithm Catalog

Complete Python code patterns using PIL/Pillow and the core/ library modules. Each algorithm produces a distinct visual style.

---

## 1. Perlin Noise Field

Organic cloud-like textures with smooth gradients. Foundation for natural-looking backgrounds.

```python
from PIL import Image
from core.noise import perlin_noise_2d, noise_to_image
from core.textures import grain_overlay
from core.blending import composite
from core.color_engine import hex_to_rgb

W, H = 2000, 2000
SEED = 42

# Define palette
bg_dark = hex_to_rgb("#1C1210")
bg_light = hex_to_rgb("#3D2B24")
accent = hex_to_rgb("#E8622B")

# Generate base noise
noise = perlin_noise_2d(W, H, scale=250, seed=SEED)
base = noise_to_image(noise, bg_dark, bg_light)

# Add a second noise layer at different scale for detail
detail_noise = perlin_noise_2d(W, H, scale=80, seed=SEED + 1)
detail = noise_to_image(detail_noise, bg_dark, accent)

# Blend layers
canvas = composite(base, detail, mode="soft_light", opacity=0.3)

# Add grain
grain = grain_overlay(W, H, intensity=0.04, seed=SEED)
canvas = composite(canvas, grain, mode="overlay", opacity=0.25)

canvas.save("perlin-field.png", "PNG")
```

**Variations:**
- Change `scale` to control feature size (50 = fine detail, 500 = broad sweeps)
- Layer 3-4 noise fields at different scales for fractal-like depth
- Use `turbulence()` instead of `perlin_noise_2d()` for more turbulent patterns

---

## 2. Flow Field

Directional particle traces following a mathematical vector field. Creates organic, flowing compositions.

```python
from PIL import Image, ImageDraw
from core.noise import flow_field
from core.color_engine import hex_to_rgb, tint, shade
from core.textures import grain_overlay
from core.blending import composite
import random
import math

W, H = 2000, 2000
SEED = 42
random.seed(SEED)

# Palette
bg = hex_to_rgb("#0A1628")
colors = [
    hex_to_rgb("#00D4AA"),
    hex_to_rgb("#2E7D9B"),
    hex_to_rgb("#5CE0D0"),
    hex_to_rgb("#E0EAF0"),
]

# Create canvas
canvas = Image.new("RGB", (W, H), bg)
draw = ImageDraw.Draw(canvas, "RGBA")

# Generate flow field
field = flow_field(W, H, scale=120, seed=SEED)

# Trace particles
num_particles = 3000
steps = 80
step_size = 3

for _ in range(num_particles):
    x = random.uniform(0, W)
    y = random.uniform(0, H)
    color = random.choice(colors)
    alpha = random.randint(15, 60)

    points = []
    for _ in range(steps):
        points.append((x, y))
        # Sample field angle at current position
        gx = int(x) % W
        gy = int(y) % H
        angle = field[gy][gx]
        x += math.cos(angle) * step_size
        y += math.sin(angle) * step_size
        # Boundary check
        if x < 0 or x >= W or y < 0 or y >= H:
            break

    if len(points) > 2:
        draw.line(points, fill=(*color, alpha), width=1)

# Add grain
grain = grain_overlay(W, H, intensity=0.03, seed=SEED)
canvas = composite(canvas, grain, mode="overlay", opacity=0.2)

canvas.save("flow-field.png", "PNG")
```

**Variations:**
- Adjust `scale` to change field frequency (smaller = more turbulent)
- Vary `step_size` for tighter or looser curves
- Use line width variation based on distance from center for depth

---

## 3. Particle System

Scattered dots with controlled size, opacity, and position distributions. Creates star fields, dust, and atmospheric effects.

```python
from PIL import Image, ImageDraw
from core.color_engine import hex_to_rgb, tint
from core.composition import golden_ratio
from core.textures import grain_overlay
from core.blending import composite
import random
import math

W, H = 2000, 2000
SEED = 42
random.seed(SEED)

# Palette
bg = hex_to_rgb("#0C0C0F")
colors = [
    hex_to_rgb("#00E5FF"),
    hex_to_rgb("#FF2D78"),
    hex_to_rgb("#B4FF39"),
    hex_to_rgb("#E8ECF0"),
]

canvas = Image.new("RGB", (W, H), bg)
draw = ImageDraw.Draw(canvas, "RGBA")

# Get focal point from composition
focal = golden_ratio(W, H)
fx, fy = focal["golden_point"]

# Dense particle cluster around focal point
for _ in range(8000):
    # Gaussian distribution centered on focal point
    x = random.gauss(fx, W * 0.25)
    y = random.gauss(fy, H * 0.25)

    # Distance from focal point affects size and opacity
    dist = math.sqrt((x - fx)**2 + (y - fy)**2)
    max_dist = math.sqrt(W**2 + H**2) / 2
    proximity = 1 - min(dist / max_dist, 1)

    radius = random.uniform(0.5, 3) + proximity * 4
    alpha = int(random.uniform(10, 40) + proximity * 60)
    color = random.choice(colors)

    x0, y0 = x - radius, y - radius
    x1, y1 = x + radius, y + radius
    draw.ellipse([x0, y0, x1, y1], fill=(*color, alpha))

# Sparse large particles
for _ in range(50):
    x = random.uniform(0, W)
    y = random.uniform(0, H)
    radius = random.uniform(8, 25)
    alpha = random.randint(5, 20)
    color = random.choice(colors[:2])
    draw.ellipse([x-radius, y-radius, x+radius, y+radius], fill=(*color, alpha))

# Grain
grain = grain_overlay(W, H, intensity=0.03, seed=SEED)
canvas = composite(canvas, grain, mode="overlay", opacity=0.2)

canvas.save("particles.png", "PNG")
```

---

## 4. Voronoi Tessellation

Cell-based divisions that create organic, crystal-like patterns.

```python
from PIL import Image, ImageDraw
from core.color_engine import hex_to_rgb, tint, shade
from core.textures import grain_overlay
from core.blending import composite
import random
import math

W, H = 2000, 2000
SEED = 42
random.seed(SEED)

# Palette
bg = hex_to_rgb("#F0E8D8")
colors = [
    hex_to_rgb("#6B4226"),
    hex_to_rgb("#B8452A"),
    hex_to_rgb("#8C7A62"),
    hex_to_rgb("#D8CCBA"),
    hex_to_rgb("#1A1410"),
]

# Generate Voronoi sites
num_sites = 60
sites = [(random.randint(0, W), random.randint(0, H)) for _ in range(num_sites)]
site_colors = [random.choice(colors) for _ in range(num_sites)]

# Pixel-by-pixel Voronoi (brute force — suitable for moderate sizes)
canvas = Image.new("RGB", (W, H), bg)
pixels = canvas.load()

# Optimization: sample at lower res, then upscale, or use KD-tree
# For 2000x2000 this is slow — use a grid-based approximation:
cell_size = 4  # Process every 4th pixel
temp = Image.new("RGB", (W // cell_size, H // cell_size), bg)
temp_pixels = temp.load()

for py in range(H // cell_size):
    for px in range(W // cell_size):
        x, y = px * cell_size, py * cell_size
        min_dist = float('inf')
        closest = 0
        for i, (sx, sy) in enumerate(sites):
            dist = (x - sx)**2 + (y - sy)**2
            if dist < min_dist:
                min_dist = dist
                closest = i
        temp_pixels[px, py] = site_colors[closest]

canvas = temp.resize((W, H), Image.NEAREST)

# Draw cell borders
draw = ImageDraw.Draw(canvas, "RGBA")
border_color = (*hex_to_rgb("#1A1410"), 40)
# Re-detect edges by checking neighbors
temp_pixels = temp.load()
for py in range(1, H // cell_size - 1):
    for px in range(1, W // cell_size - 1):
        c = temp_pixels[px, py]
        neighbors = [
            temp_pixels[px+1, py], temp_pixels[px-1, py],
            temp_pixels[px, py+1], temp_pixels[px, py-1],
        ]
        if any(n != c for n in neighbors):
            x, y = px * cell_size, py * cell_size
            draw.rectangle([x, y, x + cell_size, y + cell_size], fill=border_color)

# Add grain
grain = grain_overlay(W, H, intensity=0.03, seed=SEED)
canvas = composite(canvas, grain, mode="overlay", opacity=0.2)

canvas.save("voronoi.png", "PNG")
```

---

## 5. Fibonacci Spiral

Mathematical golden spiral rendered as a visual guide with concentric elements.

```python
from PIL import Image, ImageDraw
from core.composition import fibonacci_spiral
from core.color_engine import hex_to_rgb, tint
from core.geometry import concentric_circles
from core.textures import grain_overlay
from core.blending import composite
import math

W, H = 2000, 2000
SEED = 42

bg = hex_to_rgb("#FAF8F5")
fg = hex_to_rgb("#2C2C2C")
accent = hex_to_rgb("#C4A35A")

canvas = Image.new("RGB", (W, H), bg)
draw = ImageDraw.Draw(canvas, "RGBA")

# Get spiral path points
spiral_points = fibonacci_spiral(W, H, num_points=200)

# Draw spiral path as connected segments
for i in range(len(spiral_points) - 1):
    x1, y1 = spiral_points[i]
    x2, y2 = spiral_points[i + 1]
    progress = i / len(spiral_points)
    alpha = int(20 + progress * 80)
    width = max(1, int(1 + progress * 4))
    draw.line([(x1, y1), (x2, y2)], fill=(*fg, alpha), width=width)

# Draw concentric circles at Fibonacci number positions
fib_radii = [1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144]
convergence = (W * 0.618, H * 0.382)
for r_base in fib_radii:
    r = r_base * 8
    x0 = convergence[0] - r
    y0 = convergence[1] - r
    x1 = convergence[0] + r
    y1 = convergence[1] + r
    alpha = max(10, 60 - r_base)
    draw.ellipse([x0, y0, x1, y1], outline=(*accent, alpha), width=1)

# Dot at convergence point
draw.ellipse(
    [convergence[0]-6, convergence[1]-6, convergence[0]+6, convergence[1]+6],
    fill=(*accent, 180)
)

# Add grain
grain = grain_overlay(W, H, intensity=0.02, seed=SEED)
canvas = composite(canvas, grain, mode="overlay", opacity=0.15)

canvas.save("fibonacci-spiral.png", "PNG")
```

---

## 6. Geometric Pattern

Repeating mathematical shapes with precise placement and subtle variation.

```python
from PIL import Image, ImageDraw
from core.geometry import regular_polygon
from core.color_engine import hex_to_rgb, tint, shade
from core.composition import modular_grid
from core.textures import grain_overlay
from core.blending import composite
import random
import math

W, H = 2000, 2000
SEED = 42
random.seed(SEED)

bg = hex_to_rgb("#0D1117")
colors = [
    hex_to_rgb("#58A6FF"),
    hex_to_rgb("#3FB950"),
    hex_to_rgb("#F0883E"),
    hex_to_rgb("#E6EDF3"),
]

canvas = Image.new("RGB", (W, H), bg)
draw = ImageDraw.Draw(canvas, "RGBA")

# Create a modular grid
grid = modular_grid(W, H, columns=10, rows=10, gutter=10, margin=80)

for col_data in grid["columns"]:
    for row_data in grid["rows"]:
        cx = col_data["x"] + col_data["width"] / 2
        cy = row_data["y"] + row_data["height"] / 2
        size = min(col_data["width"], row_data["height"]) * 0.4

        # Random variation
        sides = random.choice([3, 4, 5, 6, 8])
        rotation = random.uniform(0, 360)
        color = random.choice(colors)
        alpha = random.randint(15, 60)
        filled = random.random() > 0.6

        # Draw polygon
        points = regular_polygon(cx, cy, size, sides, rotation)
        if filled:
            draw.polygon(points, fill=(*color, alpha))
        else:
            draw.polygon(points, outline=(*color, alpha), width=1)

        # Occasional inner shape
        if random.random() > 0.7:
            inner_size = size * 0.4
            inner_points = regular_polygon(cx, cy, inner_size, sides, rotation + 15)
            draw.polygon(inner_points, outline=(*color, alpha // 2), width=1)

# Add grain
grain = grain_overlay(W, H, intensity=0.03, seed=SEED)
canvas = composite(canvas, grain, mode="overlay", opacity=0.2)

canvas.save("geometric-pattern.png", "PNG")
```

---

## Combining Algorithms

The most compelling generative art combines multiple techniques:

```python
# Layer 1: Perlin noise base for atmosphere
base = noise_to_image(perlin_noise_2d(W, H, scale=300, seed=42), dark, light)

# Layer 2: Flow field traces for organic movement
# (draw on separate transparent layer, then composite)

# Layer 3: Particle scatter for detail and sparkle

# Layer 4: Geometric elements for structure

# Layer 5: Grain overlay for tactile quality
grain = grain_overlay(W, H, intensity=0.03, seed=42)
final = composite(canvas, grain, mode="overlay", opacity=0.25)
```

Each layer uses a different algorithm but shares the same palette and composition framework.
