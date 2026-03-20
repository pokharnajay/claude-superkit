"""
font-loader.py — Font scanning and @font-face CSS generation utilities.

Provides functions to scan the canvas-fonts directory, parse font metadata
from filenames, and generate complete @font-face CSS blocks with file:// URLs.
"""

from pathlib import Path
from urllib.parse import quote

# Default path to the bundled font collection
DEFAULT_FONTS_DIR = Path(__file__).resolve().parent.parent / "canvas-super-creator" / "canvas-fonts"

# Weight mapping from filename suffixes to CSS font-weight values
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


def scan_fonts(fonts_dir: Path | None = None) -> list[dict]:
    """Scan a fonts directory and return metadata for each font file.

    Args:
        fonts_dir: Path to directory containing .ttf files.
                   Defaults to the bundled canvas-fonts directory.

    Returns:
        List of dicts with keys: family, weight, style, path, filename.
        Sorted by family name, then weight, then style.
    """
    fonts_dir = fonts_dir or DEFAULT_FONTS_DIR
    results = []

    for ttf in fonts_dir.glob("*.ttf"):
        stem = ttf.stem  # e.g. "Lora-BoldItalic"
        if "-" not in stem:
            continue

        family, variant = stem.rsplit("-", 1)

        # Determine style
        style = "normal"
        if "Italic" in variant:
            style = "italic"
            variant = variant.replace("Italic", "")

        # Determine weight
        weight = 400  # default to Regular
        for keyword, value in WEIGHT_MAP.items():
            if variant == keyword or variant.startswith(keyword):
                weight = value
                break

        # Build file:// URL with proper encoding
        abs_path = str(ttf.resolve())
        file_url = "file://" + quote(abs_path)

        results.append({
            "family": family,
            "weight": weight,
            "style": style,
            "path": file_url,
            "filename": ttf.name,
        })

    # Sort for consistent output
    results.sort(key=lambda f: (f["family"], f["weight"], f["style"]))
    return results


def generate_font_face_css(fonts_dir: Path | None = None) -> str:
    """Generate a complete @font-face CSS block for all fonts in a directory.

    Args:
        fonts_dir: Path to directory containing .ttf files.
                   Defaults to the bundled canvas-fonts directory.

    Returns:
        A string containing all @font-face declarations, ready to embed
        in a <style> tag.
    """
    fonts = scan_fonts(fonts_dir)
    declarations = []

    for font in fonts:
        decl = (
            f"@font-face {{\n"
            f"    font-family: '{font['family']}';\n"
            f"    src: url('{font['path']}') format('truetype');\n"
            f"    font-weight: {font['weight']};\n"
            f"    font-style: {font['style']};\n"
            f"}}"
        )
        declarations.append(decl)

    return "\n\n".join(declarations)


def get_font_path(font_name: str, fonts_dir: Path | None = None) -> str | None:
    """Get the file:// URL for a specific font file.

    Args:
        font_name: The font filename (e.g. "Outfit-Bold.ttf") or
                   partial match (e.g. "Outfit-Bold").

    Returns:
        The file:// URL string, or None if not found.
    """
    fonts_dir = fonts_dir or DEFAULT_FONTS_DIR

    # Try exact match first
    exact = fonts_dir / font_name
    if exact.exists():
        return "file://" + quote(str(exact.resolve()))

    # Try with .ttf extension
    with_ext = fonts_dir / (font_name + ".ttf")
    if with_ext.exists():
        return "file://" + quote(str(with_ext.resolve()))

    # Try partial match
    for ttf in fonts_dir.glob("*.ttf"):
        if font_name.lower() in ttf.stem.lower():
            return "file://" + quote(str(ttf.resolve()))

    return None


def list_font_families(fonts_dir: Path | None = None) -> dict[str, list[dict]]:
    """Group all fonts by family name.

    Returns:
        Dict mapping family name to list of available variants
        (each with weight, style, filename, path).
    """
    fonts = scan_fonts(fonts_dir)
    families: dict[str, list[dict]] = {}

    for font in fonts:
        family = font["family"]
        if family not in families:
            families[family] = []
        families[family].append({
            "weight": font["weight"],
            "style": font["style"],
            "filename": font["filename"],
            "path": font["path"],
        })

    return families


if __name__ == "__main__":
    # Print a summary of available fonts when run directly
    families = list_font_families()
    for family, variants in sorted(families.items()):
        variant_strs = [
            f"  w{v['weight']} {'italic' if v['style'] == 'italic' else 'normal'}: {v['filename']}"
            for v in variants
        ]
        print(f"\n{family}:")
        for vs in variant_strs:
            print(vs)
