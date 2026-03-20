"""Gradient generation utilities for canvas designs."""

import math
import numpy as np
from PIL import Image

from .noise import perlin_noise_2d


def linear_gradient(
    width: int,
    height: int,
    color_a: tuple,
    color_b: tuple,
    angle: float = 0,
) -> Image.Image:
    """Linear gradient at any angle. Returns RGBA Image."""
    rad = math.radians(angle)
    cos_a, sin_a = math.cos(rad), math.sin(rad)

    ys, xs = np.meshgrid(np.arange(height), np.arange(width), indexing="ij")
    cx, cy = width / 2.0, height / 2.0
    dx, dy = xs - cx, ys - cy

    proj = dx * cos_a + dy * sin_a
    half_diag = abs(cos_a) * width / 2.0 + abs(sin_a) * height / 2.0
    t = np.clip((proj / half_diag + 1.0) / 2.0, 0.0, 1.0)

    ca = np.array(color_a[:4] if len(color_a) >= 4 else list(color_a[:3]) + [255], dtype=np.float64)
    cb = np.array(color_b[:4] if len(color_b) >= 4 else list(color_b[:3]) + [255], dtype=np.float64)

    t4 = t[..., np.newaxis]
    rgba = ((1.0 - t4) * ca + t4 * cb).astype(np.uint8)
    return Image.fromarray(rgba, "RGBA")


def radial_gradient(
    width: int,
    height: int,
    center: tuple,
    color_inner: tuple,
    color_outer: tuple,
    radius: float = None,
) -> Image.Image:
    """Radial gradient from center point."""
    if radius is None:
        radius = math.hypot(width, height) / 2.0

    ys, xs = np.meshgrid(np.arange(height), np.arange(width), indexing="ij")
    dist = np.sqrt((xs - center[0]) ** 2 + (ys - center[1]) ** 2)
    t = np.clip(dist / radius, 0.0, 1.0)

    ci = np.array(color_inner[:4] if len(color_inner) >= 4 else list(color_inner[:3]) + [255], dtype=np.float64)
    co = np.array(color_outer[:4] if len(color_outer) >= 4 else list(color_outer[:3]) + [255], dtype=np.float64)

    t4 = t[..., np.newaxis]
    rgba = ((1.0 - t4) * ci + t4 * co).astype(np.uint8)
    return Image.fromarray(rgba, "RGBA")


def conic_gradient(
    width: int,
    height: int,
    center: tuple,
    colors: list,
) -> Image.Image:
    """Sweep/conic gradient around center point."""
    ys, xs = np.meshgrid(np.arange(height), np.arange(width), indexing="ij")
    angles = np.arctan2(ys - center[1], xs - center[0])
    t = (angles / (2.0 * np.pi) + 0.5) % 1.0

    n = len(colors)
    rgba = np.zeros((height, width, 4), dtype=np.float64)

    for i in range(n):
        c_cur = np.array(colors[i][:4] if len(colors[i]) >= 4 else list(colors[i][:3]) + [255], dtype=np.float64)
        c_next = np.array(colors[(i + 1) % n][:4] if len(colors[(i + 1) % n]) >= 4 else list(colors[(i + 1) % n][:3]) + [255], dtype=np.float64)
        lo = i / n
        hi = (i + 1) / n
        mask = (t >= lo) & (t < hi)
        local_t = np.where(mask, (t - lo) / (hi - lo), 0.0)[..., np.newaxis]
        contribution = mask[..., np.newaxis] * ((1.0 - local_t) * c_cur + local_t * c_next)
        rgba += contribution

    return Image.fromarray(np.clip(rgba, 0, 255).astype(np.uint8), "RGBA")


def multi_stop_gradient(
    width: int,
    height: int,
    stops: list,
    angle: float = 0,
) -> Image.Image:
    """Multi-color gradient. stops = [(position_0_to_1, (r,g,b,a)), ...]"""
    stops = sorted(stops, key=lambda s: s[0])
    rad = math.radians(angle)
    cos_a, sin_a = math.cos(rad), math.sin(rad)

    ys, xs = np.meshgrid(np.arange(height), np.arange(width), indexing="ij")
    cx, cy = width / 2.0, height / 2.0
    proj = (xs - cx) * cos_a + (ys - cy) * sin_a
    half_diag = abs(cos_a) * width / 2.0 + abs(sin_a) * height / 2.0
    t = np.clip((proj / half_diag + 1.0) / 2.0, 0.0, 1.0)

    rgba = np.zeros((height, width, 4), dtype=np.float64)
    for i in range(len(stops) - 1):
        pos_a, col_a = stops[i]
        pos_b, col_b = stops[i + 1]
        ca = np.array(col_a[:4] if len(col_a) >= 4 else list(col_a[:3]) + [255], dtype=np.float64)
        cb = np.array(col_b[:4] if len(col_b) >= 4 else list(col_b[:3]) + [255], dtype=np.float64)

        mask = (t >= pos_a) & (t <= pos_b)
        span = pos_b - pos_a
        local_t = np.where(mask & (span > 0), (t - pos_a) / span, 0.0)[..., np.newaxis]
        rgba += mask[..., np.newaxis] * ((1.0 - local_t) * ca + local_t * cb)

    return Image.fromarray(np.clip(rgba, 0, 255).astype(np.uint8), "RGBA")


def noise_gradient(
    width: int,
    height: int,
    color_a: tuple,
    color_b: tuple,
    noise_scale: float = 100.0,
    seed: int = 0,
) -> Image.Image:
    """Gradient distorted by Perlin noise for organic feel."""
    noise = perlin_noise_2d(width, height, scale=noise_scale, octaves=4, seed=seed)

    ca = np.array(color_a[:4] if len(color_a) >= 4 else list(color_a[:3]) + [255], dtype=np.float64)
    cb = np.array(color_b[:4] if len(color_b) >= 4 else list(color_b[:3]) + [255], dtype=np.float64)

    t = noise[..., np.newaxis]
    rgba = ((1.0 - t) * ca + t * cb).astype(np.uint8)
    return Image.fromarray(rgba, "RGBA")
