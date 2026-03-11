"""Photoshop-style blend modes using numpy arrays."""

import numpy as np
from PIL import Image


def blend_multiply(base: np.ndarray, overlay: np.ndarray) -> np.ndarray:
    """Multiply blend: darkens by multiplying channels."""
    return base * overlay


def blend_screen(base: np.ndarray, overlay: np.ndarray) -> np.ndarray:
    """Screen blend: lightens by inverting multiply."""
    return 1.0 - (1.0 - base) * (1.0 - overlay)


def blend_overlay(base: np.ndarray, overlay: np.ndarray) -> np.ndarray:
    """Overlay blend: combines multiply and screen."""
    mask = base < 0.5
    result = np.where(
        mask,
        2.0 * base * overlay,
        1.0 - 2.0 * (1.0 - base) * (1.0 - overlay),
    )
    return result


def blend_soft_light(base: np.ndarray, overlay: np.ndarray) -> np.ndarray:
    """Soft light blend: gentle contrast adjustment."""
    return np.where(
        overlay < 0.5,
        base - (1.0 - 2.0 * overlay) * base * (1.0 - base),
        base + (2.0 * overlay - 1.0) * (np.sqrt(base) - base),
    )


def blend_hard_light(base: np.ndarray, overlay: np.ndarray) -> np.ndarray:
    """Hard light blend: overlay with swapped roles."""
    return blend_overlay(base, overlay)


def blend_color_dodge(base: np.ndarray, overlay: np.ndarray) -> np.ndarray:
    """Color dodge: brightens base by decreasing contrast."""
    denom = np.maximum(1.0 - overlay, 1e-7)
    return np.minimum(base / denom, 1.0)


def blend_color_burn(base: np.ndarray, overlay: np.ndarray) -> np.ndarray:
    """Color burn: darkens base by increasing contrast."""
    denom = np.maximum(overlay, 1e-7)
    return np.maximum(1.0 - (1.0 - base) / denom, 0.0)


def blend_difference(base: np.ndarray, overlay: np.ndarray) -> np.ndarray:
    """Difference blend: absolute difference of channels."""
    return np.abs(base - overlay)


_BLEND_MODES = {
    "multiply": blend_multiply,
    "screen": blend_screen,
    "overlay": blend_overlay,
    "soft_light": blend_soft_light,
    "hard_light": blend_hard_light,
    "color_dodge": blend_color_dodge,
    "color_burn": blend_color_burn,
    "difference": blend_difference,
}


def composite(
    base: Image.Image,
    overlay: Image.Image,
    mode: str = "normal",
    opacity: float = 1.0,
) -> Image.Image:
    """Composite two PIL Images with blend mode and opacity."""
    base_rgba = base.convert("RGBA")
    overlay_rgba = overlay.convert("RGBA").resize(base_rgba.size)

    base_arr = np.array(base_rgba, dtype=np.float32) / 255.0
    over_arr = np.array(overlay_rgba, dtype=np.float32) / 255.0

    base_rgb = base_arr[..., :3]
    over_rgb = over_arr[..., :3]
    base_a = base_arr[..., 3:4]
    over_a = over_arr[..., 3:4] * opacity

    if mode == "normal":
        blended_rgb = over_rgb
    elif mode in _BLEND_MODES:
        blended_rgb = _BLEND_MODES[mode](base_rgb, over_rgb)
    else:
        raise ValueError(f"Unknown blend mode: {mode}. Options: {list(_BLEND_MODES.keys()) + ['normal']}")

    blended_rgb = np.clip(blended_rgb, 0.0, 1.0)

    # Alpha compositing
    out_rgb = blended_rgb * over_a + base_rgb * (1.0 - over_a)
    out_a = over_a + base_a * (1.0 - over_a)

    out = np.concatenate([out_rgb, out_a], axis=2)
    out = (np.clip(out, 0.0, 1.0) * 255).astype(np.uint8)
    return Image.fromarray(out, "RGBA")
