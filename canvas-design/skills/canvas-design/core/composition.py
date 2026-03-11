"""Layout and composition guides for canvas design."""

import math


PHI = (1.0 + math.sqrt(5)) / 2.0


def rule_of_thirds(width: int, height: int) -> dict:
    """Returns third-line positions and intersection points."""
    x1 = width // 3
    x2 = 2 * width // 3
    y1 = height // 3
    y2 = 2 * height // 3
    return {
        "lines": {
            "vertical": [x1, x2],
            "horizontal": [y1, y2],
        },
        "points": [(x1, y1), (x2, y1), (x1, y2), (x2, y2)],
    }


def golden_ratio(width: int, height: int, orientation: str = "horizontal") -> dict:
    """Returns phi-based division rectangles."""
    rects = []
    x, y, w, h = 0, 0, width, height

    for _ in range(8):
        if orientation == "horizontal":
            split = int(w / PHI)
            rects.append((x, y, split, h))
            x += split
            w -= split
        else:
            split = int(h / PHI)
            rects.append((x, y, w, split))
            y += split
            h -= split

        # Alternate orientation each step
        orientation = "vertical" if orientation == "horizontal" else "horizontal"

    return {"phi": PHI, "rectangles": rects}


def fibonacci_spiral(width: int, height: int) -> list:
    """Returns list of (x, y) points along Fibonacci spiral path."""
    cx, cy = width / 2.0, height / 2.0
    scale = min(width, height) / 2.0

    points = []
    max_theta = 6.0 * math.pi
    steps = 200
    a = scale / (max_theta * PHI)

    for i in range(steps):
        theta = max_theta * i / (steps - 1)
        r = a * math.exp(0.3063 * theta)  # ~ln(PHI)/half_pi growth
        x = cx + r * math.cos(theta)
        y = cy + r * math.sin(theta)
        if 0 <= x < width and 0 <= y < height:
            points.append((int(x), int(y)))

    return points


def safe_zone(width: int, height: int, margin: int = 50) -> tuple:
    """Returns (left, top, right, bottom) of safe content area."""
    return (margin, margin, width - margin, height - margin)


def modular_grid(
    width: int,
    height: int,
    cols: int = 3,
    rows: int = 3,
    gutter: int = 20,
) -> list:
    """Returns list of (x, y, w, h) cell rectangles."""
    total_gutter_x = gutter * (cols - 1)
    total_gutter_y = gutter * (rows - 1)
    cell_w = (width - total_gutter_x) // cols
    cell_h = (height - total_gutter_y) // rows

    cells = []
    for row in range(rows):
        for col in range(cols):
            x = col * (cell_w + gutter)
            y = row * (cell_h + gutter)
            cells.append((x, y, cell_w, cell_h))

    return cells


def margin_rect(width: int, height: int, margin_pct: float = 0.05) -> tuple:
    """Returns usable area as (left, top, right, bottom)."""
    mx = int(width * margin_pct)
    my = int(height * margin_pct)
    return (mx, my, width - mx, height - my)


def diagonal_armature(width: int, height: int) -> list:
    """Returns key diagonal lines as [(x1, y1, x2, y2), ...]."""
    return [
        # Corner-to-corner diagonals
        (0, 0, width, height),
        (width, 0, 0, height),
        # Reciprocal diagonals (perpendicular to main diagonals from corners)
        (0, 0, int(height * height / width) if width > 0 else 0, height),
        (width, 0, width - int(height * height / width) if width > 0 else width, height),
        (0, height, width, height - int(width * width / height) if height > 0 else height),
        (width, height, 0, height - int(width * width / height) if height > 0 else height),
    ]
