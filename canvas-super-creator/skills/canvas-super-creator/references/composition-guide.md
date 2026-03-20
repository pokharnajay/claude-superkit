# Composition Techniques Reference

Layout systems and coordinate math for canvas-based design. Each technique includes a description, use cases, and Python functions for calculating key positions.

---

## 1. Rule of Thirds

Divide the canvas into a 3x3 grid. Place focal elements at the four intersection points or along the grid lines.

**When to use:** General-purpose layout. Portraits, landscapes, social media posts, any design that needs natural visual balance without centering everything.

```python
def rule_of_thirds(width: int, height: int) -> dict:
    """Calculate Rule of Thirds grid lines and power points."""
    return {
        "vertical_lines": [width / 3, 2 * width / 3],
        "horizontal_lines": [height / 3, 2 * height / 3],
        "power_points": [
            (width / 3, height / 3),          # top-left
            (2 * width / 3, height / 3),       # top-right
            (width / 3, 2 * height / 3),       # bottom-left
            (2 * width / 3, 2 * height / 3),   # bottom-right
        ],
    }
```

**Placement guidance:**
- Primary subject: top-right or bottom-left power point (strongest in left-to-right reading cultures).
- Horizon lines: place along horizontal thirds, not center.
- Text blocks: align to a vertical third line.

---

## 2. Golden Ratio

Use phi (1.618) to divide the canvas into proportional sections. Creates more refined asymmetry than the Rule of Thirds.

**When to use:** Editorial layouts, luxury branding, portfolio pieces. When you want mathematically harmonious proportions.

```python
PHI = 1.618033988749895

def golden_ratio_divisions(width: int, height: int) -> dict:
    """Calculate Golden Ratio division lines and focal point."""
    return {
        "vertical_major": width / PHI,             # ~61.8% from left
        "vertical_minor": width - (width / PHI),   # ~38.2% from left
        "horizontal_major": height / PHI,
        "horizontal_minor": height - (height / PHI),
        "golden_point": (width / PHI, height / PHI),  # primary focal point
    }
```

**Placement guidance:**
- Place the subject at the golden point (61.8% from left, 61.8% from top).
- Divide layout panels at golden ratio: wider panel gets primary content, narrower gets secondary.
- Use golden ratio for font size relationships: if body is 16px, heading is 16 * 1.618 = ~26px.

---

## 3. Fibonacci Spiral

A logarithmic spiral that passes through squares sized by the Fibonacci sequence. Guides the eye along a natural curve.

**When to use:** Organic, flowing compositions. Photography overlays, poster layouts with circular motion, branding with natural themes.

```python
def fibonacci_spiral_points(width: int, height: int, num_points: int = 20) -> list:
    """Generate points along a Fibonacci spiral path within the canvas.

    Returns list of (x, y) coordinates tracing the spiral from outer edge
    to the convergence point.
    """
    import math

    # Golden spiral convergence point (approximately)
    cx = width * 0.618
    cy = height * 0.382

    # Maximum radius from convergence point to corner
    max_radius = math.sqrt(cx**2 + cy**2)

    points = []
    for i in range(num_points):
        t = i / num_points
        # Spiral outward from convergence point
        angle = t * 4 * math.pi  # two full rotations
        radius = max_radius * (t ** 0.8)
        x = cx + radius * math.cos(angle)
        y = cy + radius * math.sin(angle)
        # Clamp to canvas
        x = max(0, min(width, x))
        y = max(0, min(height, y))
        points.append((x, y))

    return points

def fibonacci_convergence_point(width: int, height: int) -> tuple:
    """The focal point where the spiral converges."""
    return (width * 0.618, height * 0.382)
```

**Placement guidance:**
- The convergence point is the ultimate focal spot. Place your subject here.
- Arrange supporting elements along the spiral path.
- The spiral naturally pulls the eye inward; place a CTA or key message at the convergence.

---

## 4. Diagonal Armature

Lines connecting corners and bisecting edges create a web of diagonals. Produces dynamic, energetic compositions.

**When to use:** Posters, action-oriented content, dynamic marketing materials. When the composition needs implied movement or tension.

```python
def diagonal_armature(width: int, height: int) -> dict:
    """Calculate diagonal armature lines and key intersections."""
    w, h = width, height
    return {
        "primary_diagonals": [
            ((0, 0), (w, h)),       # top-left to bottom-right
            ((w, 0), (0, h)),       # top-right to bottom-left
        ],
        "reciprocal_diagonals": [
            ((0, 0), (w, h / 2)),   # top-left to mid-right
            ((0, h / 2), (w, h)),   # mid-left to bottom-right
            ((0, 0), (w / 2, h)),   # top-left to bottom-center
            ((w / 2, 0), (w, h)),   # top-center to bottom-right
            # Mirror set
            ((w, 0), (0, h / 2)),
            ((0, h / 2), (w, 0)),
            ((w, 0), (w / 2, h)),
            ((w / 2, 0), (0, h)),
        ],
        "center": (w / 2, h / 2),
        # Key intersections along primary diagonals
        "quarter_points": [
            (w * 0.25, h * 0.25),
            (w * 0.75, h * 0.25),
            (w * 0.25, h * 0.75),
            (w * 0.75, h * 0.75),
        ],
    }
```

**Placement guidance:**
- Align text baselines or image edges along diagonal lines.
- Place focal elements at diagonal intersections.
- Use diagonals to create implied motion (objects along the diagonal feel like they are moving).

---

## 5. Modular Grid

A structured grid with columns, rows, and gutters. The foundation of editorial and web design.

**When to use:** Multi-element layouts, infographics, data-heavy designs, editorial spreads, social media carousels. Any design with more than 3 distinct content blocks.

```python
def modular_grid(
    width: int,
    height: int,
    columns: int = 12,
    rows: int = 8,
    gutter: int = 20,
    margin: int = 40,
) -> dict:
    """Calculate a modular grid with columns, rows, and gutters.

    Returns column positions, row positions, and individual cell bounds.
    """
    usable_w = width - 2 * margin - (columns - 1) * gutter
    usable_h = height - 2 * margin - (rows - 1) * gutter
    col_w = usable_w / columns
    row_h = usable_h / rows

    col_positions = []
    for c in range(columns):
        x = margin + c * (col_w + gutter)
        col_positions.append({"x": x, "width": col_w})

    row_positions = []
    for r in range(rows):
        y = margin + r * (row_h + gutter)
        row_positions.append({"y": y, "height": row_h})

    return {
        "columns": col_positions,
        "rows": row_positions,
        "column_width": col_w,
        "row_height": row_h,
        "gutter": gutter,
        "margin": margin,
        "total_cells": columns * rows,
    }

def grid_cell(grid: dict, col: int, row: int, col_span: int = 1, row_span: int = 1) -> dict:
    """Get the bounding box for a cell or merged cell region."""
    c = grid["columns"][col]
    r = grid["rows"][row]
    w = col_span * grid["column_width"] + (col_span - 1) * grid["gutter"]
    h = row_span * grid["row_height"] + (row_span - 1) * grid["gutter"]
    return {"x": c["x"], "y": r["y"], "width": w, "height": h}
```

**Placement guidance:**
- Content blocks should span whole columns (2-col, 3-col, 4-col, 6-col spans work well on a 12-col grid).
- Gutters provide breathing room; never place text in gutter space.
- Use row spans for vertical rhythm; heading + body + caption = 3 row-span block.

---

## 6. Asymmetric Balance

Place a large element on one side and balance it with smaller, strategically placed elements on the other. Weight is distributed by size, color intensity, and visual density.

**When to use:** Hero sections, feature callouts, magazine layouts, when you want dynamic balance without symmetry.

```python
def asymmetric_balance(width: int, height: int, anchor_side: str = "left") -> dict:
    """Calculate zones for asymmetric balance layout.

    anchor_side: 'left' or 'right' -- where the dominant element sits.
    """
    if anchor_side == "left":
        dominant = {"x": 0, "y": 0, "width": width * 0.618, "height": height}
        counter = {"x": width * 0.618, "y": 0, "width": width * 0.382, "height": height}
    else:
        dominant = {"x": width * 0.382, "y": 0, "width": width * 0.618, "height": height}
        counter = {"x": 0, "y": 0, "width": width * 0.382, "height": height}

    # Counter-weight placement points (smaller elements placed strategically)
    cw = counter["width"]
    cx = counter["x"]
    cy = counter["y"]
    ch = counter["height"]

    return {
        "dominant_zone": dominant,
        "counter_zone": counter,
        "counter_focal_points": [
            (cx + cw * 0.5, cy + ch * 0.33),   # upper third
            (cx + cw * 0.5, cy + ch * 0.67),   # lower third
        ],
    }
```

**Placement guidance:**
- The dominant zone holds the hero image, large heading, or primary visual.
- Counter zone holds supporting text, secondary images, or a CTA.
- Visual weight factors: large > small, dark > light, saturated > muted, complex > simple, sharp > blurred.

---

## 7. Z-Pattern

The eye follows a Z-shape: top-left to top-right, diagonal to bottom-left, then to bottom-right. Ideal for layouts with a clear beginning and end.

**When to use:** Marketing materials, landing page sections, social media cards, any design where you want the viewer to process information in a specific order.

```python
def z_pattern(width: int, height: int, padding: int = 50) -> dict:
    """Calculate Z-pattern reading path positions."""
    return {
        "path": [
            (padding, padding),                          # 1. Start: top-left (logo/brand)
            (width - padding, padding),                  # 2. Top-right (navigation/CTA)
            (padding, height - padding),                 # 3. Bottom-left (supporting info)
            (width - padding, height - padding),         # 4. End: bottom-right (final CTA)
        ],
        "diagonal_midpoint": (width / 2, height / 2),   # Center of the Z diagonal
        "top_bar": {"y": padding, "x_start": padding, "x_end": width - padding},
        "bottom_bar": {"y": height - padding, "x_start": padding, "x_end": width - padding},
    }
```

**Placement guidance:**
- **Position 1** (top-left): Brand mark or headline. First thing seen.
- **Position 2** (top-right): Secondary hook or CTA.
- **Diagonal**: The eye sweeps here naturally; place an image or visual break.
- **Position 3** (bottom-left): Supporting details, features, testimonials.
- **Position 4** (bottom-right): Final CTA. Most important action item.

---

## 8. F-Pattern

The eye scans horizontally across the top, drops down, scans a shorter horizontal line, then drifts down the left edge. Common for text-heavy content.

**When to use:** Blog headers, article previews, LinkedIn posts, content where the left edge anchors attention and detail fades to the right.

```python
def f_pattern(width: int, height: int, padding: int = 50) -> dict:
    """Calculate F-pattern reading path and content zones."""
    return {
        "top_bar": {
            "y": padding,
            "x_start": padding,
            "x_end": width - padding,
            "description": "Full-width headline. Most important content."
        },
        "second_bar": {
            "y": height * 0.35,
            "x_start": padding,
            "x_end": width * 0.7,
            "description": "Shorter secondary scan line. Subheading or key feature."
        },
        "left_spine": {
            "x": padding,
            "y_start": height * 0.35,
            "y_end": height - padding,
            "description": "Vertical drift zone. Bullet points, labels, anchors."
        },
        "attention_zones": [
            {"label": "high", "bounds": (padding, padding, width - padding, height * 0.35)},
            {"label": "medium", "bounds": (padding, height * 0.35, width * 0.5, height * 0.65)},
            {"label": "low", "bounds": (width * 0.5, height * 0.5, width - padding, height - padding)},
        ],
    }
```

**Placement guidance:**
- Top bar gets the headline -- full width, largest type.
- Second bar gets a subheading or the most important supporting statement.
- Left spine is for labels, icons, bullet points, or numbered lists.
- Bottom-right is a dead zone in F-pattern; avoid placing critical content there unless you break the pattern with a visual element.

---

## Safe Zone Calculator

Platform-specific safe areas prevent critical content from being cropped or obscured by UI overlays.

```python
def safe_zone(
    width: int,
    height: int,
    top: int,
    right: int,
    bottom: int,
    left: int,
) -> dict:
    """Calculate the safe content area within platform margins.

    Args:
        width, height: Canvas dimensions in pixels.
        top, right, bottom, left: Margin from each edge in pixels.

    Returns:
        Safe area bounding box and usable dimensions.
    """
    return {
        "x": left,
        "y": top,
        "width": width - left - right,
        "height": height - top - bottom,
        "x_end": width - right,
        "y_end": height - bottom,
        "center": ((left + width - right) / 2, (top + height - bottom) / 2),
    }

# Preset safe zones (from formats.md)
SAFE_ZONE_PRESETS = {
    "github_repo":         {"w": 1280, "h": 640,  "t": 60,  "r": 60,  "b": 60,  "l": 60},
    "notion_cover_wide":   {"w": 1500, "h": 600,  "t": 40,  "r": 40,  "b": 120, "l": 40},
    "linkedin_personal":   {"w": 1584, "h": 396,  "t": 60,  "r": 60,  "b": 60,  "l": 260},
    "linkedin_company":    {"w": 1128, "h": 191,  "t": 30,  "r": 30,  "b": 30,  "l": 30},
    "youtube_banner":      {"w": 2560, "h": 1440, "t": 509, "r": 507, "b": 509, "l": 507},
    "twitter_header":      {"w": 1500, "h": 500,  "t": 60,  "r": 60,  "b": 60,  "l": 200},
    "instagram_square":    {"w": 1080, "h": 1080, "t": 50,  "r": 50,  "b": 50,  "l": 50},
    "instagram_story":     {"w": 1080, "h": 1920, "t": 200, "r": 50,  "b": 250, "l": 50},
    "youtube_thumbnail":   {"w": 1280, "h": 720,  "t": 50,  "r": 50,  "b": 50,  "l": 50},
    "open_graph":          {"w": 1200, "h": 630,  "t": 50,  "r": 50,  "b": 50,  "l": 50},
}

def get_safe_zone(preset_name: str) -> dict:
    """Get safe zone for a named format preset."""
    p = SAFE_ZONE_PRESETS[preset_name]
    return safe_zone(p["w"], p["h"], p["t"], p["r"], p["b"], p["l"])
```

---

## Choosing a Composition Technique

| Scenario | Recommended Technique |
|---|---|
| Single focal subject, simple background | Rule of Thirds or Golden Ratio |
| Flowing, organic, nature-themed | Fibonacci Spiral |
| High-energy, action, or movement | Diagonal Armature |
| Multiple content blocks, data-rich | Modular Grid |
| Hero image with supporting text | Asymmetric Balance |
| Marketing card with CTA | Z-Pattern |
| Text-heavy with headline hierarchy | F-Pattern |
| Need dynamic tension without chaos | Diagonal Armature + Rule of Thirds |

---

## Combining Techniques

Techniques are not mutually exclusive. Common combinations:

1. **Modular Grid + Rule of Thirds**: Use a 12-column grid but place the primary content block at a thirds intersection.
2. **Asymmetric Balance + Golden Ratio**: The 61.8%/38.2% split is itself the golden ratio.
3. **Z-Pattern + Safe Zones**: Calculate the Z-path within the safe zone, not the full canvas.
4. **Diagonal Armature + Modular Grid**: Align some elements to the grid while tilting images or decorative elements along diagonals for energy.

Always calculate positions within the safe zone first, then apply composition techniques to the safe area dimensions.
