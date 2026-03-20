"""Color manipulation, conversion, and harmony utilities."""

import colorsys


def hex_to_rgb(hex_str: str) -> tuple:
    """Convert hex color string to (r, g, b) tuple."""
    h = hex_str.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def rgb_to_hex(r: int, g: int, b: int) -> str:
    """Convert RGB values to hex string."""
    return "#{:02x}{:02x}{:02x}".format(r, g, b)


def rgb_to_hsl(r: int, g: int, b: int) -> tuple:
    """Convert RGB (0-255) to HSL (h: 0-360, s: 0-1, l: 0-1)."""
    h, l, s = colorsys.rgb_to_hls(r / 255.0, g / 255.0, b / 255.0)
    return (h * 360.0, s, l)


def hsl_to_rgb(h: float, s: float, l: float) -> tuple:
    """Convert HSL (h: 0-360, s: 0-1, l: 0-1) to RGB (0-255)."""
    r, g, b = colorsys.hls_to_rgb(h / 360.0, l, s)
    return (int(round(r * 255)), int(round(g * 255)), int(round(b * 255)))


def tint(color: tuple, amount: float) -> tuple:
    """Lighten a color by mixing with white. amount: 0-1."""
    return tuple(int(c + (255 - c) * amount) for c in color[:3])


def shade(color: tuple, amount: float) -> tuple:
    """Darken a color by mixing with black. amount: 0-1."""
    return tuple(int(c * (1.0 - amount)) for c in color[:3])


def desaturate(color: tuple, amount: float) -> tuple:
    """Reduce saturation. amount: 0-1 where 1 is fully gray."""
    h, s, l = rgb_to_hsl(*color[:3])
    s = s * (1.0 - amount)
    return hsl_to_rgb(h, s, l)


def _shift_hue(color: tuple, degrees: float) -> tuple:
    """Shift hue by given degrees."""
    h, s, l = rgb_to_hsl(*color[:3])
    h = (h + degrees) % 360.0
    return hsl_to_rgb(h, s, l)


def complementary(color: tuple) -> tuple:
    """Return the complementary color (180 degree hue shift)."""
    return _shift_hue(color, 180.0)


def analogous(color: tuple, count: int = 2, spread: float = 30) -> list:
    """Return analogous colors evenly spread around the hue."""
    results = []
    for i in range(1, count + 1):
        results.append(_shift_hue(color, spread * i))
        results.append(_shift_hue(color, -spread * i))
    return results


def triadic(color: tuple) -> list:
    """Return the two triadic harmony colors."""
    return [_shift_hue(color, 120.0), _shift_hue(color, 240.0)]


def split_complementary(color: tuple) -> list:
    """Return the two split-complementary colors."""
    return [_shift_hue(color, 150.0), _shift_hue(color, 210.0)]


def _relative_luminance(color: tuple) -> float:
    """Compute relative luminance per WCAG 2.0."""
    vals = []
    for c in color[:3]:
        v = c / 255.0
        vals.append(v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4)
    return 0.2126 * vals[0] + 0.7152 * vals[1] + 0.0722 * vals[2]


def contrast_ratio(color_a: tuple, color_b: tuple) -> float:
    """WCAG contrast ratio between two colors."""
    l1 = _relative_luminance(color_a)
    l2 = _relative_luminance(color_b)
    lighter = max(l1, l2)
    darker = min(l1, l2)
    return (lighter + 0.05) / (darker + 0.05)


def ensure_readable(
    text_color: tuple,
    bg_color: tuple,
    min_ratio: float = 4.5,
) -> tuple:
    """Adjust text color to meet minimum contrast ratio against background."""
    if contrast_ratio(text_color, bg_color) >= min_ratio:
        return text_color

    bg_lum = _relative_luminance(bg_color)
    h, s, l = rgb_to_hsl(*text_color[:3])

    # Try making lighter or darker based on background
    if bg_lum < 0.5:
        # Dark background: lighten text
        for step in range(100):
            candidate_l = min(1.0, l + step * 0.01)
            candidate = hsl_to_rgb(h, s, candidate_l)
            if contrast_ratio(candidate, bg_color) >= min_ratio:
                return candidate
    else:
        # Light background: darken text
        for step in range(100):
            candidate_l = max(0.0, l - step * 0.01)
            candidate = hsl_to_rgb(h, s, candidate_l)
            if contrast_ratio(candidate, bg_color) >= min_ratio:
                return candidate

    # Fallback: return black or white
    return (0, 0, 0) if bg_lum >= 0.5 else (255, 255, 255)
