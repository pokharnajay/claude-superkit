"""Image effects and post-processing filters."""

import numpy as np
from PIL import Image, ImageFilter


def drop_shadow(
    image: Image.Image,
    offset: tuple = (5, 5),
    blur_radius: int = 10,
    shadow_color: tuple = (0, 0, 0),
    opacity: float = 0.5,
) -> Image.Image:
    """Add drop shadow behind image content."""
    src = image.convert("RGBA")
    w, h = src.size

    pad = blur_radius * 2 + max(abs(offset[0]), abs(offset[1]))
    canvas_w = w + pad * 2
    canvas_h = h + pad * 2

    # Create shadow from alpha channel
    alpha = src.split()[3]
    shadow = Image.new("RGBA", (canvas_w, canvas_h), (0, 0, 0, 0))
    shadow_layer = Image.new("RGBA", src.size, shadow_color[:3] + (int(255 * opacity),))
    shadow_layer.putalpha(alpha)

    sx = pad + offset[0]
    sy = pad + offset[1]
    shadow.paste(shadow_layer, (sx, sy))

    if blur_radius > 0:
        shadow = shadow.filter(ImageFilter.GaussianBlur(radius=blur_radius))

    shadow.paste(src, (pad, pad), src)
    return shadow


def outer_glow(
    image: Image.Image,
    radius: int = 15,
    color: tuple = (255, 255, 255),
    intensity: float = 0.5,
) -> Image.Image:
    """Add outer glow around non-transparent pixels."""
    src = image.convert("RGBA")
    w, h = src.size
    pad = radius * 2
    canvas = Image.new("RGBA", (w + pad * 2, h + pad * 2), (0, 0, 0, 0))

    alpha = src.split()[3]
    glow_layer = Image.new("RGBA", src.size, color[:3] + (int(255 * intensity),))
    glow_layer.putalpha(alpha)

    canvas.paste(glow_layer, (pad, pad))
    canvas = canvas.filter(ImageFilter.GaussianBlur(radius=radius))
    canvas.paste(src, (pad, pad), src)
    return canvas


def vignette(image: Image.Image, intensity: float = 0.5) -> Image.Image:
    """Darken edges with radial vignette."""
    src = image.convert("RGBA")
    w, h = src.size

    ys, xs = np.meshgrid(np.arange(h), np.arange(w), indexing="ij")
    cx, cy = w / 2.0, h / 2.0
    max_dist = np.sqrt(cx * cx + cy * cy)
    dist = np.sqrt((xs - cx) ** 2 + (ys - cy) ** 2) / max_dist

    factor = 1.0 - dist * intensity
    factor = np.clip(factor, 0.0, 1.0)

    arr = np.array(src, dtype=np.float64)
    arr[..., :3] *= factor[..., np.newaxis]
    arr = np.clip(arr, 0, 255).astype(np.uint8)
    return Image.fromarray(arr, "RGBA")


def duotone(
    image: Image.Image,
    color_dark: tuple,
    color_light: tuple,
) -> Image.Image:
    """Apply two-tone color mapping to image."""
    gray = np.array(image.convert("L"), dtype=np.float64) / 255.0

    cd = np.array(color_dark[:3], dtype=np.float64)
    cl = np.array(color_light[:3], dtype=np.float64)

    t = gray[..., np.newaxis]
    rgb = (1.0 - t) * cd + t * cl
    rgb = np.clip(rgb, 0, 255).astype(np.uint8)

    alpha = np.full((*gray.shape, 1), 255, dtype=np.uint8)
    rgba = np.concatenate([rgb, alpha], axis=2)
    return Image.fromarray(rgba, "RGBA")


def posterize(image: Image.Image, levels: int = 4) -> Image.Image:
    """Reduce color levels for poster effect."""
    src = image.convert("RGBA")
    arr = np.array(src, dtype=np.float64)

    step = 255.0 / max(levels - 1, 1)
    arr[..., :3] = np.round(arr[..., :3] / step) * step
    arr = np.clip(arr, 0, 255).astype(np.uint8)
    return Image.fromarray(arr, "RGBA")


def color_overlay(
    image: Image.Image,
    color: tuple,
    opacity: float = 0.3,
) -> Image.Image:
    """Apply color tint overlay."""
    src = image.convert("RGBA")
    arr = np.array(src, dtype=np.float64)

    overlay = np.array(color[:3], dtype=np.float64)
    arr[..., :3] = arr[..., :3] * (1.0 - opacity) + overlay * opacity
    arr = np.clip(arr, 0, 255).astype(np.uint8)
    return Image.fromarray(arr, "RGBA")
