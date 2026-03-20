"""Geometric drawing primitives for PIL ImageDraw."""

import math
from PIL import Image, ImageDraw


def _de_casteljau(points: list, t: float) -> tuple:
    """Evaluate a point on a Bezier curve using de Casteljau's algorithm."""
    pts = list(points)
    while len(pts) > 1:
        pts = [
            (pts[i][0] * (1 - t) + pts[i + 1][0] * t,
             pts[i][1] * (1 - t) + pts[i + 1][1] * t)
            for i in range(len(pts) - 1)
        ]
    return pts[0]


def bezier_curve(
    draw: ImageDraw.ImageDraw,
    points: list,
    segments: int = 50,
    fill: tuple = None,
    width: int = 1,
) -> None:
    """Draw cubic Bezier curve through control points."""
    if len(points) < 2:
        return
    coords = []
    for i in range(segments + 1):
        t = i / segments
        pt = _de_casteljau(points, t)
        coords.append((int(pt[0]), int(pt[1])))

    for i in range(len(coords) - 1):
        draw.line([coords[i], coords[i + 1]], fill=fill, width=width)


def wave_line(
    draw: ImageDraw.ImageDraw,
    start: tuple,
    end: tuple,
    amplitude: float = 20,
    frequency: float = 3,
    fill: tuple = None,
    width: int = 1,
) -> None:
    """Draw sinusoidal wave between two points."""
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    length = math.hypot(dx, dy)
    if length == 0:
        return

    angle = math.atan2(dy, dx)
    cos_a, sin_a = math.cos(angle), math.sin(angle)
    segments = max(int(length), 50)
    coords = []

    for i in range(segments + 1):
        t = i / segments
        along = t * length
        perp = amplitude * math.sin(2.0 * math.pi * frequency * t)
        x = start[0] + cos_a * along - sin_a * perp
        y = start[1] + sin_a * along + cos_a * perp
        coords.append((int(x), int(y)))

    for i in range(len(coords) - 1):
        draw.line([coords[i], coords[i + 1]], fill=fill, width=width)


def regular_polygon(
    draw: ImageDraw.ImageDraw,
    center: tuple,
    radius: float,
    sides: int,
    rotation: float = 0,
    fill: tuple = None,
    outline: tuple = None,
) -> None:
    """Draw regular n-sided polygon."""
    angle_step = 2.0 * math.pi / sides
    offset = math.radians(rotation)
    points = []
    for i in range(sides):
        a = angle_step * i + offset
        x = center[0] + radius * math.cos(a)
        y = center[1] + radius * math.sin(a)
        points.append((int(x), int(y)))
    draw.polygon(points, fill=fill, outline=outline)


def star(
    draw: ImageDraw.ImageDraw,
    center: tuple,
    outer_r: float,
    inner_r: float,
    points: int = 5,
    rotation: float = 0,
    fill: tuple = None,
    outline: tuple = None,
) -> None:
    """Draw star shape."""
    angle_step = math.pi / points
    offset = math.radians(rotation) - math.pi / 2.0
    coords = []
    for i in range(points * 2):
        r = outer_r if i % 2 == 0 else inner_r
        a = angle_step * i + offset
        x = center[0] + r * math.cos(a)
        y = center[1] + r * math.sin(a)
        coords.append((int(x), int(y)))
    draw.polygon(coords, fill=fill, outline=outline)


def concentric_circles(
    draw: ImageDraw.ImageDraw,
    center: tuple,
    radii: list,
    colors: list,
    widths: list = None,
) -> None:
    """Draw multiple concentric circle rings."""
    if widths is None:
        widths = [2] * len(radii)
    for r, color, w in zip(radii, colors, widths):
        bbox = [center[0] - r, center[1] - r, center[0] + r, center[1] + r]
        draw.ellipse(bbox, outline=color, width=w)


def parallel_lines(
    draw: ImageDraw.ImageDraw,
    bbox: tuple,
    count: int,
    angle: float = 0,
    fill: tuple = None,
    width: int = 1,
) -> None:
    """Draw evenly spaced parallel lines within bounding box."""
    x0, y0, x1, y1 = bbox
    cx = (x0 + x1) / 2.0
    cy = (y0 + y1) / 2.0
    diag = math.hypot(x1 - x0, y1 - y0)
    rad = math.radians(angle)
    cos_a, sin_a = math.cos(rad), math.sin(rad)

    span = diag
    spacing = span / max(count - 1, 1) if count > 1 else 0

    for i in range(count):
        offset = -span / 2.0 + i * spacing
        px = cx + cos_a * offset
        py = cy + sin_a * offset
        lx1 = px - sin_a * diag
        ly1 = py + cos_a * diag
        lx2 = px + sin_a * diag
        ly2 = py - cos_a * diag
        draw.line([(int(lx1), int(ly1)), (int(lx2), int(ly2))], fill=fill, width=width)


def rounded_rect(
    draw: ImageDraw.ImageDraw,
    bbox: tuple,
    radius: int,
    fill: tuple = None,
    outline: tuple = None,
    width: int = 1,
) -> None:
    """Draw rounded rectangle (compatible with older PIL versions)."""
    x0, y0, x1, y1 = bbox
    r = min(radius, (x1 - x0) // 2, (y1 - y0) // 2)

    # Use built-in rounded_rectangle if available (Pillow 8.2+)
    if hasattr(draw, "rounded_rectangle"):
        draw.rounded_rectangle(bbox, radius=r, fill=fill, outline=outline, width=width)
        return

    # Fallback for older Pillow
    draw.rectangle([x0 + r, y0, x1 - r, y1], fill=fill)
    draw.rectangle([x0, y0 + r, x1, y1 - r], fill=fill)
    draw.pieslice([x0, y0, x0 + 2 * r, y0 + 2 * r], 180, 270, fill=fill, outline=outline, width=width)
    draw.pieslice([x1 - 2 * r, y0, x1, y0 + 2 * r], 270, 360, fill=fill, outline=outline, width=width)
    draw.pieslice([x0, y1 - 2 * r, x0 + 2 * r, y1], 90, 180, fill=fill, outline=outline, width=width)
    draw.pieslice([x1 - 2 * r, y1 - 2 * r, x1, y1], 0, 90, fill=fill, outline=outline, width=width)

    if outline:
        draw.line([(x0 + r, y0), (x1 - r, y0)], fill=outline, width=width)
        draw.line([(x0 + r, y1), (x1 - r, y1)], fill=outline, width=width)
        draw.line([(x0, y0 + r), (x0, y1 - r)], fill=outline, width=width)
        draw.line([(x1, y0 + r), (x1, y1 - r)], fill=outline, width=width)
