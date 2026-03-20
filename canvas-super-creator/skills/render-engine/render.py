"""
render.py — HTML rendering utilities for the canvas-super-creator render-engine.

Provides helpers for generating @font-face CSS, assembling HTML boilerplate,
and writing temporary HTML files for Playwright screenshot capture.
"""

from pathlib import Path
from urllib.parse import quote
import time

# Base path to the bundled font collection
FONTS_DIR = Path(__file__).resolve().parent.parent / "canvas-super-creator" / "canvas-fonts"

# URL-encoded file:// base for @font-face src
FONT_URL_BASE = "file://" + quote(str(FONTS_DIR)) + "/"


# ---------------------------------------------------------------------------
# Font weight / style inference from filename
# ---------------------------------------------------------------------------

WEIGHT_MAP = {
    "Thin": 100,
    "ExtraLight": 200,
    "Light": 300,
    "Regular": 400,
    "Medium": 500,
    "SemiBold": 600,
    "Bold": 700,
    "ExtraBold": 800,
    "Black": 900,
}

STYLE_KEYWORDS = {"Italic"}


def _parse_font_filename(filename: str) -> dict | None:
    """Parse a .ttf filename into family, weight, and style metadata.

    Expected pattern: FamilyName-WeightStyle.ttf
    Examples:
        Outfit-Regular.ttf  -> family='Outfit', weight=400, style='normal'
        Lora-BoldItalic.ttf -> family='Lora', weight=700, style='italic'
    """
    stem = Path(filename).stem  # e.g. "Lora-BoldItalic"
    if "-" not in stem:
        return None

    family, variant = stem.rsplit("-", 1)

    # Determine style
    style = "normal"
    if "Italic" in variant:
        style = "italic"
        variant = variant.replace("Italic", "")

    # Determine weight
    weight = 400  # default
    for keyword, value in WEIGHT_MAP.items():
        if variant == keyword or variant.startswith(keyword):
            weight = value
            break

    return {
        "family": family,
        "weight": weight,
        "style": style,
        "filename": filename,
    }


# ---------------------------------------------------------------------------
# @font-face CSS generation
# ---------------------------------------------------------------------------


def generate_font_css(fonts_dir: Path | None = None) -> str:
    """Scan the fonts directory and return a complete @font-face CSS block.

    Args:
        fonts_dir: Path to directory containing .ttf files.
                   Defaults to the bundled canvas-fonts directory.

    Returns:
        A string containing all @font-face declarations.
    """
    fonts_dir = fonts_dir or FONTS_DIR
    url_base = "file://" + quote(str(fonts_dir)) + "/"

    declarations = []
    for ttf in sorted(fonts_dir.glob("*.ttf")):
        meta = _parse_font_filename(ttf.name)
        if meta is None:
            continue

        font_url = url_base + quote(ttf.name)
        decl = (
            f"@font-face {{\n"
            f"    font-family: '{meta['family']}';\n"
            f"    src: url('{font_url}') format('truetype');\n"
            f"    font-weight: {meta['weight']};\n"
            f"    font-style: {meta['style']};\n"
            f"}}"
        )
        declarations.append(decl)

    return "\n\n".join(declarations)


# ---------------------------------------------------------------------------
# HTML boilerplate
# ---------------------------------------------------------------------------


def html_boilerplate(
    width: int,
    height: int,
    css: str,
    body: str,
    font_css: str | None = None,
) -> str:
    """Return a complete HTML document ready for Playwright rendering.

    Args:
        width: Canvas width in pixels.
        height: Canvas height in pixels.
        css: CSS rules for the design (excluding font-face and reset).
        body: HTML body content.
        font_css: Optional pre-generated @font-face block.
                  If None, auto-generates from the bundled fonts directory.

    Returns:
        Complete HTML string.
    """
    if font_css is None:
        font_css = generate_font_css()

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
/* === FONT LOADING === */
{font_css}

/* === RESET === */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

/* === CANVAS === */
html, body {{
    width: {width}px;
    height: {height}px;
    overflow: hidden;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
}}

body {{
    position: relative;
    background: #000000;
}}

/* === DESIGN === */
{css}
    </style>
</head>
<body>
{body}
</body>
</html>"""


# ---------------------------------------------------------------------------
# Temp file writing
# ---------------------------------------------------------------------------


def write_temp_html(html: str, prefix: str = "canvas-super-creator") -> str:
    """Write an HTML string to a temp file and return its file:// URL.

    Args:
        html: Complete HTML document string.
        prefix: Filename prefix.

    Returns:
        A file:// URL suitable for Playwright browser_navigate.
    """
    timestamp = int(time.time() * 1000)
    filename = f"{prefix}-{timestamp}.html"
    filepath = Path(f"/tmp/{filename}")
    filepath.write_text(html, encoding="utf-8")
    # /tmp has no spaces, so no encoding needed
    return f"file:///tmp/{filename}"
