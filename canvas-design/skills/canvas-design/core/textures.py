"""Texture generation for overlays and backgrounds."""

import math
import numpy as np
from PIL import Image, ImageDraw

from .noise import perlin_noise_2d


def grain_overlay(
    width: int,
    height: int,
    intensity: float = 0.1,
    seed: int = 0,
) -> Image.Image:
    """Film grain noise overlay. Returns RGBA."""
    rng = np.random.RandomState(seed)
    noise = rng.normal(0, 1, (height, width)).astype(np.float64)
    noise = np.clip(noise * intensity, -1.0, 1.0)

    gray = ((noise + 1.0) / 2.0 * 255).astype(np.uint8)
    alpha = (np.abs(noise) * 255).astype(np.uint8)

    rgba = np.stack([gray, gray, gray, alpha], axis=2)
    return Image.fromarray(rgba, "RGBA")


def paper_texture(
    width: int,
    height: int,
    base_color: tuple = (245, 240, 230),
    roughness: float = 0.3,
    seed: int = 0,
) -> Image.Image:
    """Simulated paper/parchment texture."""
    noise = perlin_noise_2d(width, height, scale=80.0, octaves=5, seed=seed)
    rng = np.random.RandomState(seed + 1)
    fine = rng.normal(0, 1, (height, width)) * 0.05

    combined = noise * roughness + fine
    combined = np.clip(combined, -0.5, 0.5)

    bc = np.array(base_color[:3], dtype=np.float64)
    offset = (combined * 40)[..., np.newaxis]
    rgb = np.clip(bc + offset, 0, 255).astype(np.uint8)

    alpha = np.full((height, width, 1), 255, dtype=np.uint8)
    rgba = np.concatenate([rgb, alpha], axis=2)
    return Image.fromarray(rgba, "RGBA")


def halftone(
    image: Image.Image,
    dot_size: int = 8,
    spacing: int = 10,
) -> Image.Image:
    """Convert image to halftone dot pattern."""
    gray = image.convert("L")
    arr = np.array(gray, dtype=np.float64) / 255.0
    w, h = image.size

    result = Image.new("RGBA", (w, h), (255, 255, 255, 255))
    draw = ImageDraw.Draw(result)

    for y in range(0, h, spacing):
        for x in range(0, w, spacing):
            region = arr[y:y + spacing, x:x + spacing]
            if region.size == 0:
                continue
            brightness = float(np.mean(region))
            r = int((1.0 - brightness) * dot_size / 2)
            if r > 0:
                draw.ellipse(
                    [x - r, y - r, x + r, y + r],
                    fill=(0, 0, 0, 255),
                )

    return result


def scanlines(
    width: int,
    height: int,
    line_width: int = 2,
    gap: int = 4,
    color: tuple = (0, 0, 0),
    alpha: int = 40,
) -> Image.Image:
    """CRT/retro scanline overlay."""
    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    fill = tuple(color[:3]) + (alpha,)
    step = line_width + gap

    for y in range(0, height, step):
        draw.rectangle([0, y, width - 1, y + line_width - 1], fill=fill)

    return img


def stipple(
    width: int,
    height: int,
    density: float = 0.1,
    dot_size: int = 2,
    color: tuple = (0, 0, 0),
    seed: int = 0,
) -> Image.Image:
    """Stippled dot pattern."""
    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    fill = tuple(color[:3]) + (255,)

    rng = np.random.RandomState(seed)
    count = int(width * height * density / (dot_size * dot_size))
    xs = rng.randint(0, width, count)
    ys = rng.randint(0, height, count)

    r = dot_size // 2
    for x, y in zip(xs, ys):
        draw.ellipse([int(x) - r, int(y) - r, int(x) + r, int(y) + r], fill=fill)

    return img


def crosshatch(
    width: int,
    height: int,
    spacing: int = 12,
    angle: float = 45,
    line_width: int = 1,
    color: tuple = (0, 0, 0),
) -> Image.Image:
    """Cross-hatching pattern overlay."""
    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    fill = tuple(color[:3]) + (180,)
    diag = int(math.hypot(width, height))

    for a in [angle, angle + 90]:
        rad = math.radians(a)
        cos_a, sin_a = math.cos(rad), math.sin(rad)
        cx, cy = width / 2.0, height / 2.0

        for offset in range(-diag, diag, spacing):
            px = cx + cos_a * offset
            py = cy + sin_a * offset
            x1 = px - sin_a * diag
            y1 = py + cos_a * diag
            x2 = px + sin_a * diag
            y2 = py - cos_a * diag
            draw.line(
                [(int(x1), int(y1)), (int(x2), int(y2))],
                fill=fill,
                width=line_width,
            )

    return img
