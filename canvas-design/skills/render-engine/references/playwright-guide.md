# Playwright MCP Tool Reference

Quick reference for the Playwright browser automation tools used in the canvas-design render pipeline.

---

## Tools Used in Render Pipeline

### browser_navigate

Opens a URL in the headless browser.

```
Tool: mcp__plugin_playwright_playwright__browser_navigate
Parameter: url (string) — the URL to navigate to
```

**Usage in render pipeline:**
```
url: "file:///tmp/canvas-design-1234567890.html"
```

**Notes:**
- Always use `file://` protocol with triple slashes for local files
- Spaces in paths must be encoded as `%20`
- Wait for navigation to complete before proceeding to resize

---

### browser_resize

Sets the browser viewport to exact pixel dimensions.

```
Tool: mcp__plugin_playwright_playwright__browser_resize
Parameters:
  width (integer) — viewport width in pixels
  height (integer) — viewport height in pixels
```

**Usage in render pipeline:**
```
width: 1280
height: 640
```

**Notes:**
- Viewport dimensions must match the HTML/CSS canvas dimensions exactly
- No minimum or maximum enforced, but extremely large sizes (>4000px) may cause memory issues
- Resize after navigation, not before — the page must be loaded first

---

### browser_take_screenshot

Captures the current viewport as a PNG image.

```
Tool: mcp__plugin_playwright_playwright__browser_take_screenshot
```

**Usage in render pipeline:**
- Call after navigate and resize are both complete
- Returns the path to the saved PNG file

**Notes:**
- Output is always PNG format
- Captures the full viewport at 1:1 pixel ratio
- Does not capture elements outside the viewport (no full-page mode needed for fixed canvases)

---

### browser_close

Closes the browser instance.

```
Tool: mcp__plugin_playwright_playwright__browser_close
```

**Usage:** Call after screenshot is captured to free resources. Optional but good practice for long sessions.

---

## Common Issues & Solutions

### Fonts Not Rendering

**Problem:** Text appears in Times New Roman or a system fallback font.

**Causes:**
1. Incorrect `file://` URL path in `@font-face` declaration
2. Missing `%20` encoding for spaces in the path
3. Font family name in CSS does not match `@font-face` declaration (case-sensitive)
4. Missing `format('truetype')` in the `src` property

**Debugging steps:**
1. Copy the `file://` URL from your `@font-face` and paste it into a browser — it should download the font file
2. Use `browser_snapshot` to inspect the rendered DOM and check computed styles
3. Verify font files exist at the path using `ls` or `Glob`

### Viewport Size Issues

**Problem:** Design appears cropped or has unwanted scrollbars.

**Causes:**
1. `browser_resize` dimensions don't match HTML `body` dimensions
2. Content overflows the body element
3. Default browser margins not reset

**Fix:**
- Always include the CSS reset: `* { margin: 0; padding: 0; box-sizing: border-box; }`
- Set `overflow: hidden` on `html, body`
- Ensure `browser_resize` width/height matches the CSS `html, body` width/height exactly

### file:// Protocol Not Working

**Problem:** Browser shows a blank page or error when navigating to `file://` URL.

**Causes:**
1. Wrong number of slashes — must be `file:///` (three) for absolute paths
2. File does not exist at the specified path
3. Path contains unencoded special characters

**Fix:**
- Use Python `urllib.parse.quote()` to encode paths
- Verify the file exists before navigating
- Use absolute paths, never relative

### Slow Rendering

**Problem:** Screenshot takes a long time or times out.

**Causes:**
1. Very large canvas dimensions (>4000px in either direction)
2. Complex CSS animations or transitions still running
3. Heavy blur filters (`filter: blur(80px)`) on large elements

**Fix:**
- For large canvases, increase timeout
- Avoid CSS animations (they're not visible in a screenshot anyway)
- Use smaller blur radii or apply blur to smaller elements

---

## Additional Playwright Tools (Not in Main Pipeline)

These tools can be useful for debugging but are not part of the standard render flow:

### browser_snapshot
Returns accessibility snapshot of the current page. Useful for verifying element structure.

### browser_evaluate
Runs JavaScript in the browser context. Useful for checking computed styles or font loading status:
```javascript
document.fonts.ready.then(() => console.log('Fonts loaded'))
```

### browser_console_messages
Returns console messages from the browser. Useful for catching CSS errors or font loading failures.
