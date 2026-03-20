---
name: render-engine
description: HTML/CSS to PNG rendering pipeline via Playwright. Use when converting HTML designs to screenshot images, troubleshooting font loading, or managing the render pipeline.
license: MIT
metadata:
  author: canvas-super-creator
  version: 3.0.0
---

# Render Engine — HTML/CSS to PNG Pipeline

Converts HTML/CSS designs into pixel-perfect PNG images using the Playwright browser automation MCP tools. This is the rendering backbone for all HTML-based design skills (html-design, cover-design, poster-design, social-media-design, thumbnail-design, brand-assets).

---

## Pipeline Overview

The rendering pipeline has 5 steps executed in strict order:

```
HTML/CSS → Write to /tmp → Navigate Playwright → Resize Viewport → Screenshot PNG → (Optional) PIL Post-Processing
```

---

## Step 1: Write HTML to Temp File

Write the complete HTML document to a temporary file in `/tmp/`. The filename must be unique per render to avoid collisions.

```python
import time
from pathlib import Path

timestamp = int(time.time() * 1000)
filename = f"canvas-super-creator-{timestamp}.html"
filepath = Path(f"/tmp/{filename}")
filepath.write_text(html_string, encoding="utf-8")
file_url = f"file:///tmp/{filename}"
```

**Requirements:**
- File must be a complete HTML document (DOCTYPE, html, head, body)
- All CSS must be inline in a `<style>` tag (no external stylesheets)
- All fonts must use `@font-face` with `file://` paths (no CDN links)
- File encoding must be UTF-8

---

## Step 2: Navigate Playwright to the File

Use the Playwright MCP tool to open the HTML file in a headless browser:

```
Tool: mcp__plugin_playwright_playwright__browser_navigate
Parameter: url = "file:///tmp/canvas-super-creator-1234567890.html"
```

**Important:** The `file://` protocol requires triple slashes for absolute paths. Spaces in paths must be encoded as `%20`.

---

## Step 3: Resize Viewport to Canvas Dimensions

Set the browser viewport to the exact pixel dimensions of your design:

```
Tool: mcp__plugin_playwright_playwright__browser_resize
Parameters: width = 1280, height = 640
```

The viewport dimensions must match the design dimensions exactly. This ensures the screenshot captures the design at 1:1 pixel ratio with no scrollbars or cropping.

---

## Step 4: Take Screenshot as PNG

Capture the rendered page as a PNG image:

```
Tool: mcp__plugin_playwright_playwright__browser_take_screenshot
```

This captures the full viewport as a PNG file. The output path will be returned by the tool.

---

## Step 5: Optional PIL Post-Processing

After capturing the screenshot, you can apply post-processing effects using PIL/Pillow:

```python
from PIL import Image, ImageFilter, ImageEnhance
import numpy as np

# Load the screenshot
img = Image.open(screenshot_path)

# Add film grain
grain = np.random.normal(0, 8, (img.height, img.width, 3)).astype(np.int16)
arr = np.array(img).astype(np.int16)
arr = np.clip(arr + grain, 0, 255).astype(np.uint8)
img = Image.fromarray(arr)

# Add subtle vignette
# (use core.effects.vignette if available)

img.save("final-output.png", "PNG")
```

Common post-processing:
- **Film grain:** Random noise at 2-5% intensity for tactile quality
- **Vignette:** Darken edges 10-20% for depth
- **Sharpening:** Subtle unsharp mask for crisp text
- **Color grading:** Adjust curves, saturation, or apply LUT

---

## Font Loading

Fonts must be loaded via `@font-face` declarations pointing to the bundled font files using `file://` protocol URLs.

**Font directory:** `file:///Users/jaypokharna/Desktop/Shared%20Folder/Shared%20Folder/python/claude-skills/canvas-super-creator/skills/canvas-super-creator/canvas-fonts/`

**Critical:** Spaces in the path MUST be encoded as `%20` in `file://` URLs.

### @font-face Template

```css
@font-face {
    font-family: 'Outfit';
    src: url('file:///Users/jaypokharna/Desktop/Shared%20Folder/Shared%20Folder/python/claude-skills/canvas-super-creator/skills/canvas-super-creator/canvas-fonts/Outfit-Regular.ttf') format('truetype');
    font-weight: 400;
    font-style: normal;
}
@font-face {
    font-family: 'Outfit';
    src: url('file:///Users/jaypokharna/Desktop/Shared%20Folder/Shared%20Folder/python/claude-skills/canvas-super-creator/skills/canvas-super-creator/canvas-fonts/Outfit-Bold.ttf') format('truetype');
    font-weight: 700;
    font-style: normal;
}
```

### Font Weight/Style Mapping

When loading fonts, match the filename suffix to the correct CSS weight and style:

| Filename Suffix | font-weight | font-style |
|---|---|---|
| `-Regular` | 400 | normal |
| `-Medium` | 500 | normal |
| `-Light` | 300 | normal |
| `-Bold` | 700 | normal |
| `-ExtraBold` | 800 | normal |
| `-Italic` | 400 | italic |
| `-BoldItalic` | 700 | italic |

---

## HTML Boilerplate Template

Use this exact structure for every HTML design:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        /* === FONT LOADING === */
        @font-face {
            font-family: 'FontName';
            src: url('file:///Users/jaypokharna/Desktop/Shared%20Folder/Shared%20Folder/python/claude-skills/canvas-super-creator/skills/canvas-super-creator/canvas-fonts/FontName-Regular.ttf') format('truetype');
            font-weight: 400;
            font-style: normal;
        }

        /* === RESET === */
        *, *::before, *::after {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        /* === CANVAS === */
        html, body {
            width: WIDTH_PX;
            height: HEIGHT_PX;
            overflow: hidden;
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
        }

        body {
            position: relative;
            background: #000000;
        }

        /* === DESIGN CSS === */
        /* Your design styles here */
    </style>
</head>
<body>
    <!-- Your design markup here -->
</body>
</html>
```

**Mandatory boilerplate elements:**
1. `box-sizing: border-box` on all elements
2. Fixed `width` and `height` on `html, body` matching canvas dimensions
3. `overflow: hidden` on `html, body` to prevent scrollbars
4. Font-smoothing for clean text rendering
5. `position: relative` on body for absolute-positioned children

---

## Troubleshooting Guide

### Fonts Not Loading

**Symptom:** Text appears in a fallback system font (Times New Roman, Arial).

**Diagnosis:**
1. Check that the `file://` URL is correct and spaces are encoded as `%20`
2. Verify the `.ttf` file exists at the specified path
3. Ensure `font-family` in CSS matches the `@font-face` declaration exactly (case-sensitive)
4. Check that `format('truetype')` is specified in the `src`

**Fix:** Use the `font-loader.py` utility to auto-generate correct `@font-face` blocks.

### Viewport Size Mismatch

**Symptom:** Design appears cropped, has scrollbars, or shows extra whitespace.

**Diagnosis:**
1. Compare `browser_resize` dimensions with the `html, body` width/height
2. Check for elements that overflow the body

**Fix:** Ensure viewport dimensions match the `html, body` CSS dimensions exactly. Add `overflow: hidden` to prevent any overflow.

### Blank Screenshot

**Symptom:** Screenshot is entirely white or black.

**Diagnosis:**
1. Navigate step may have failed -- check the file URL
2. HTML file may not have been written correctly
3. CSS may have errors preventing rendering

**Fix:** Verify the temp file exists and contains valid HTML. Try `browser_navigate` again.

### Blurry Text

**Symptom:** Text looks fuzzy or anti-aliased poorly.

**Diagnosis:** Device pixel ratio issues or CSS transform scaling.

**Fix:** Avoid CSS `transform: scale()` on text elements. Use font-smoothing properties. Render at 1:1 pixel ratio (no upscaling).

### File Path Issues on macOS

**Symptom:** `file://` URL returns 404 or cannot be loaded.

**Diagnosis:** macOS paths with spaces need `%20` encoding.

**Fix:** Always URL-encode the path. Use `urllib.parse.quote()` in Python:

```python
from urllib.parse import quote
path = "/Users/jaypokharna/Desktop/Shared Folder/file.html"
url = "file://" + quote(path)
# Result: file:///Users/jaypokharna/Desktop/Shared%20Folder/file.html
```

---

## Utility Scripts

This skill includes two Python utility scripts:

- **`render.py`** — HTML generation helpers: font CSS generation, boilerplate assembly, temp file writing
- **`font-loader.py`** — Font scanning and `@font-face` CSS generation

Use these to automate the repetitive parts of the pipeline. See the individual files for API documentation.

---

## Complete Render Workflow Example

```
1. Generate HTML with design CSS and @font-face declarations
2. Write HTML to /tmp/canvas-super-creator-{timestamp}.html
3. mcp__plugin_playwright_playwright__browser_navigate → file:///tmp/canvas-super-creator-{timestamp}.html
4. mcp__plugin_playwright_playwright__browser_resize → width: 1280, height: 640
5. mcp__plugin_playwright_playwright__browser_take_screenshot → PNG output
6. (Optional) Load PNG in PIL for grain/vignette post-processing
7. Save final PNG to user's requested output path
```
