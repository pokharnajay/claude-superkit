# SVG Pattern Library for Textures — Complete Reference Catalog

Each pattern is provided as both an inline SVG `<defs>` block and as a data-URI ready for CSS `background-image`. All patterns tile seamlessly.

---

## 1. Dots Grid (Regular)

```html
<svg width="0" height="0">
  <defs>
    <pattern id="dots-grid" x="0" y="0" width="20" height="20" patternUnits="userSpaceOnUse">
      <circle cx="10" cy="10" r="2" fill="#000000" opacity="0.3" />
    </pattern>
  </defs>
</svg>
```

```css
.dots-grid {
  background-image: url("data:image/svg+xml,%3Csvg width='20' height='20' xmlns='http://www.w3.org/2000/svg'%3E%3Ccircle cx='10' cy='10' r='2' fill='%23000000' opacity='0.3'/%3E%3C/svg%3E");
  background-size: 20px 20px;
}
```

### Dots Grid (Offset / Staggered)

```html
<svg width="0" height="0">
  <defs>
    <pattern id="dots-offset" x="0" y="0" width="20" height="20" patternUnits="userSpaceOnUse">
      <circle cx="5" cy="5" r="1.5" fill="#000000" opacity="0.25" />
      <circle cx="15" cy="15" r="1.5" fill="#000000" opacity="0.25" />
    </pattern>
  </defs>
</svg>
```

```css
.dots-offset {
  background-image: url("data:image/svg+xml,%3Csvg width='20' height='20' xmlns='http://www.w3.org/2000/svg'%3E%3Ccircle cx='5' cy='5' r='1.5' fill='%23000000' opacity='0.25'/%3E%3Ccircle cx='15' cy='15' r='1.5' fill='%23000000' opacity='0.25'/%3E%3C/svg%3E");
  background-size: 20px 20px;
}
```

---

## 2. Horizontal Lines

```html
<svg width="0" height="0">
  <defs>
    <pattern id="lines-horizontal" x="0" y="0" width="10" height="10" patternUnits="userSpaceOnUse">
      <line x1="0" y1="5" x2="10" y2="5" stroke="#000000" stroke-width="0.5" opacity="0.2" />
    </pattern>
  </defs>
</svg>
```

```css
.lines-horizontal {
  background-image: url("data:image/svg+xml,%3Csvg width='10' height='10' xmlns='http://www.w3.org/2000/svg'%3E%3Cline x1='0' y1='5' x2='10' y2='5' stroke='%23000000' stroke-width='0.5' opacity='0.2'/%3E%3C/svg%3E");
  background-size: 10px 10px;
}
```

### Vertical Lines

```css
.lines-vertical {
  background-image: url("data:image/svg+xml,%3Csvg width='10' height='10' xmlns='http://www.w3.org/2000/svg'%3E%3Cline x1='5' y1='0' x2='5' y2='10' stroke='%23000000' stroke-width='0.5' opacity='0.2'/%3E%3C/svg%3E");
  background-size: 10px 10px;
}
```

### Diagonal Lines (45 degrees)

```html
<svg width="0" height="0">
  <defs>
    <pattern id="lines-diagonal" x="0" y="0" width="10" height="10" patternUnits="userSpaceOnUse">
      <line x1="0" y1="10" x2="10" y2="0" stroke="#000000" stroke-width="0.5" opacity="0.2" />
    </pattern>
  </defs>
</svg>
```

```css
.lines-diagonal {
  background-image: url("data:image/svg+xml,%3Csvg width='10' height='10' xmlns='http://www.w3.org/2000/svg'%3E%3Cline x1='0' y1='10' x2='10' y2='0' stroke='%23000000' stroke-width='0.5' opacity='0.2'/%3E%3C/svg%3E");
  background-size: 10px 10px;
}
```

### Crosshatch

```html
<svg width="0" height="0">
  <defs>
    <pattern id="crosshatch" x="0" y="0" width="10" height="10" patternUnits="userSpaceOnUse">
      <line x1="0" y1="10" x2="10" y2="0" stroke="#000000" stroke-width="0.5" opacity="0.15" />
      <line x1="0" y1="0" x2="10" y2="10" stroke="#000000" stroke-width="0.5" opacity="0.15" />
    </pattern>
  </defs>
</svg>
```

```css
.crosshatch {
  background-image: url("data:image/svg+xml,%3Csvg width='10' height='10' xmlns='http://www.w3.org/2000/svg'%3E%3Cline x1='0' y1='10' x2='10' y2='0' stroke='%23000000' stroke-width='0.5' opacity='0.15'/%3E%3Cline x1='0' y1='0' x2='10' y2='10' stroke='%23000000' stroke-width='0.5' opacity='0.15'/%3E%3C/svg%3E");
  background-size: 10px 10px;
}
```

---

## 3. Waves (Sinusoidal)

```html
<svg width="0" height="0">
  <defs>
    <pattern id="waves" x="0" y="0" width="40" height="20" patternUnits="userSpaceOnUse">
      <path d="M0 10 Q10 0 20 10 Q30 20 40 10" fill="none" stroke="#000000" stroke-width="0.8" opacity="0.2" />
    </pattern>
  </defs>
</svg>
```

```css
.waves {
  background-image: url("data:image/svg+xml,%3Csvg width='40' height='20' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M0 10 Q10 0 20 10 Q30 20 40 10' fill='none' stroke='%23000000' stroke-width='0.8' opacity='0.2'/%3E%3C/svg%3E");
  background-size: 40px 20px;
}
```

### Double Waves
```css
.waves-double {
  background-image: url("data:image/svg+xml,%3Csvg width='40' height='20' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M0 5 Q10 0 20 5 Q30 10 40 5' fill='none' stroke='%23000000' stroke-width='0.6' opacity='0.2'/%3E%3Cpath d='M0 15 Q10 10 20 15 Q30 20 40 15' fill='none' stroke='%23000000' stroke-width='0.6' opacity='0.2'/%3E%3C/svg%3E");
  background-size: 40px 20px;
}
```

---

## 4. Scales / Fish Scale

```html
<svg width="0" height="0">
  <defs>
    <pattern id="scales" x="0" y="0" width="24" height="24" patternUnits="userSpaceOnUse">
      <path d="M0 24 A12 12 0 0 1 24 24" fill="none" stroke="#000000" stroke-width="0.8" opacity="0.2" />
      <path d="M12 12 A12 12 0 0 1 36 12" fill="none" stroke="#000000" stroke-width="0.8" opacity="0.2" />
      <path d="M-12 12 A12 12 0 0 1 12 12" fill="none" stroke="#000000" stroke-width="0.8" opacity="0.2" />
    </pattern>
  </defs>
</svg>
```

```css
.scales {
  background-image: url("data:image/svg+xml,%3Csvg width='24' height='24' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M0 24 A12 12 0 0 1 24 24' fill='none' stroke='%23000000' stroke-width='0.8' opacity='0.2'/%3E%3Cpath d='M12 12 A12 12 0 0 1 36 12' fill='none' stroke='%23000000' stroke-width='0.8' opacity='0.2'/%3E%3Cpath d='M-12 12 A12 12 0 0 1 12 12' fill='none' stroke='%23000000' stroke-width='0.8' opacity='0.2'/%3E%3C/svg%3E");
  background-size: 24px 24px;
}
```

---

## 5. Hexagons / Honeycomb

```html
<svg width="0" height="0">
  <defs>
    <pattern id="hexagons" x="0" y="0" width="28" height="48.5" patternUnits="userSpaceOnUse">
      <polygon points="14,2 26,10 26,26 14,34 2,26 2,10"
               fill="none" stroke="#000000" stroke-width="0.8" opacity="0.2" />
      <polygon points="0,18.25 -12,26.25 -12,42.25 0,50.25 12,42.25 12,26.25"
               fill="none" stroke="#000000" stroke-width="0.8" opacity="0.2"
               transform="translate(28, 16.25)" />
    </pattern>
  </defs>
</svg>
```

```css
.hexagons {
  background-image: url("data:image/svg+xml,%3Csvg width='28' height='49' xmlns='http://www.w3.org/2000/svg'%3E%3Cpolygon points='14,2 26,10 26,26 14,34 2,26 2,10' fill='none' stroke='%23000000' stroke-width='0.8' opacity='0.2'/%3E%3Cpolygon points='14,26 26,34 26,50 14,58 2,50 2,34' fill='none' stroke='%23000000' stroke-width='0.8' opacity='0.2' transform='translate(14,16)'/%3E%3C/svg%3E");
  background-size: 28px 49px;
}
```

### Simplified Honeycomb (using a cleaner approach)
```css
.honeycomb {
  background-image: url("data:image/svg+xml,%3Csvg width='56' height='100' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M28 66L0 50L0 16L28 0L56 16L56 50L28 66L28 100' fill='none' stroke='%23000000' stroke-width='0.8' opacity='0.15'/%3E%3Cpath d='M28 0L28 34L0 50L0 84L28 100L56 84L56 50L28 34' fill='none' stroke='%23000000' stroke-width='0.8' opacity='0.15'/%3E%3C/svg%3E");
  background-size: 56px 100px;
}
```

---

## 6. Triangles Tessellation

```html
<svg width="0" height="0">
  <defs>
    <pattern id="triangles" x="0" y="0" width="20" height="17.32" patternUnits="userSpaceOnUse">
      <polygon points="10,0 20,17.32 0,17.32"
               fill="none" stroke="#000000" stroke-width="0.5" opacity="0.2" />
      <polygon points="10,17.32 0,0 20,0"
               fill="none" stroke="#000000" stroke-width="0.5" opacity="0.2" />
    </pattern>
  </defs>
</svg>
```

```css
.triangles {
  background-image: url("data:image/svg+xml,%3Csvg width='20' height='17' xmlns='http://www.w3.org/2000/svg'%3E%3Cpolygon points='10,0 20,17 0,17' fill='none' stroke='%23000000' stroke-width='0.5' opacity='0.2'/%3E%3Cpolygon points='10,17 0,0 20,0' fill='none' stroke='%23000000' stroke-width='0.5' opacity='0.2'/%3E%3C/svg%3E");
  background-size: 20px 17px;
}
```

---

## 7. Chevrons

```html
<svg width="0" height="0">
  <defs>
    <pattern id="chevrons" x="0" y="0" width="24" height="24" patternUnits="userSpaceOnUse">
      <path d="M0 12 L12 0 L24 12 M0 24 L12 12 L24 24"
            fill="none" stroke="#000000" stroke-width="0.8" opacity="0.2" />
    </pattern>
  </defs>
</svg>
```

```css
.chevrons {
  background-image: url("data:image/svg+xml,%3Csvg width='24' height='24' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M0 12 L12 0 L24 12 M0 24 L12 12 L24 24' fill='none' stroke='%23000000' stroke-width='0.8' opacity='0.2'/%3E%3C/svg%3E");
  background-size: 24px 24px;
}
```

### Thick Chevrons
```css
.chevrons-thick {
  background-image: url("data:image/svg+xml,%3Csvg width='30' height='30' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M0 15 L15 0 L30 15 M0 30 L15 15 L30 30' fill='none' stroke='%23000000' stroke-width='2' opacity='0.15'/%3E%3C/svg%3E");
  background-size: 30px 30px;
}
```

---

## 8. Circuit Board Nodes

```html
<svg width="0" height="0">
  <defs>
    <pattern id="circuit" x="0" y="0" width="40" height="40" patternUnits="userSpaceOnUse">
      <circle cx="20" cy="20" r="2" fill="#000000" opacity="0.3" />
      <line x1="20" y1="0" x2="20" y2="18" stroke="#000000" stroke-width="0.5" opacity="0.2" />
      <line x1="22" y1="20" x2="40" y2="20" stroke="#000000" stroke-width="0.5" opacity="0.2" />
      <line x1="20" y1="22" x2="20" y2="40" stroke="#000000" stroke-width="0.5" opacity="0.2" />
      <line x1="0" y1="20" x2="18" y2="20" stroke="#000000" stroke-width="0.5" opacity="0.2" />
      <circle cx="0" cy="0" r="1" fill="#000000" opacity="0.2" />
      <line x1="0" y1="2" x2="0" y2="18" stroke="#000000" stroke-width="0.3" opacity="0.15" />
      <line x1="2" y1="0" x2="18" y2="0" stroke="#000000" stroke-width="0.3" opacity="0.15" />
    </pattern>
  </defs>
</svg>
```

```css
.circuit {
  background-image: url("data:image/svg+xml,%3Csvg width='40' height='40' xmlns='http://www.w3.org/2000/svg'%3E%3Ccircle cx='20' cy='20' r='2' fill='%23000000' opacity='0.3'/%3E%3Cline x1='20' y1='0' x2='20' y2='18' stroke='%23000000' stroke-width='0.5' opacity='0.2'/%3E%3Cline x1='22' y1='20' x2='40' y2='20' stroke='%23000000' stroke-width='0.5' opacity='0.2'/%3E%3Cline x1='20' y1='22' x2='20' y2='40' stroke='%23000000' stroke-width='0.5' opacity='0.2'/%3E%3Cline x1='0' y1='20' x2='18' y2='20' stroke='%23000000' stroke-width='0.5' opacity='0.2'/%3E%3Ccircle cx='0' cy='0' r='1' fill='%23000000' opacity='0.2'/%3E%3C/svg%3E");
  background-size: 40px 40px;
}
```

### Circuit Board (neon on dark)
```css
.circuit-neon {
  background-color: #0a0a1a;
  background-image: url("data:image/svg+xml,%3Csvg width='40' height='40' xmlns='http://www.w3.org/2000/svg'%3E%3Ccircle cx='20' cy='20' r='2' fill='%2300ff88' opacity='0.4'/%3E%3Cline x1='20' y1='0' x2='20' y2='18' stroke='%2300ff88' stroke-width='0.5' opacity='0.2'/%3E%3Cline x1='22' y1='20' x2='40' y2='20' stroke='%2300ff88' stroke-width='0.5' opacity='0.2'/%3E%3Cline x1='20' y1='22' x2='20' y2='40' stroke='%2300ff88' stroke-width='0.5' opacity='0.2'/%3E%3Cline x1='0' y1='20' x2='18' y2='20' stroke='%2300ff88' stroke-width='0.5' opacity='0.2'/%3E%3C/svg%3E");
  background-size: 40px 40px;
}
```

---

## 9. Topographic Contours

```html
<svg width="0" height="0">
  <defs>
    <pattern id="topographic" x="0" y="0" width="60" height="60" patternUnits="userSpaceOnUse">
      <path d="M30 5 Q45 10 50 25 Q55 40 40 50 Q25 60 15 45 Q5 30 15 15 Q25 5 30 5Z"
            fill="none" stroke="#000000" stroke-width="0.5" opacity="0.15" />
      <path d="M30 15 Q40 18 43 28 Q46 38 36 43 Q26 48 20 38 Q14 28 22 20 Q28 15 30 15Z"
            fill="none" stroke="#000000" stroke-width="0.5" opacity="0.15" />
      <path d="M30 25 Q35 27 36 32 Q37 37 33 39 Q29 41 26 36 Q23 31 27 28 Q29 25 30 25Z"
            fill="none" stroke="#000000" stroke-width="0.5" opacity="0.15" />
    </pattern>
  </defs>
</svg>
```

```css
.topographic {
  background-image: url("data:image/svg+xml,%3Csvg width='60' height='60' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M30 5 Q45 10 50 25 Q55 40 40 50 Q25 60 15 45 Q5 30 15 15 Q25 5 30 5Z' fill='none' stroke='%23000000' stroke-width='0.5' opacity='0.15'/%3E%3Cpath d='M30 15 Q40 18 43 28 Q46 38 36 43 Q26 48 20 38 Q14 28 22 20 Q28 15 30 15Z' fill='none' stroke='%23000000' stroke-width='0.5' opacity='0.15'/%3E%3Cpath d='M30 25 Q35 27 36 32 Q37 37 33 39 Q29 41 26 36 Q23 31 27 28 Q29 25 30 25Z' fill='none' stroke='%23000000' stroke-width='0.5' opacity='0.15'/%3E%3C/svg%3E");
  background-size: 60px 60px;
}
```

---

## 10. Noise Clouds

Soft cloudy texture via embedded SVG filter, rendered as a background.

```css
.noise-clouds {
  background-image: url("data:image/svg+xml,%3Csvg width='256' height='256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.03' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='0.15'/%3E%3C/svg%3E");
  background-size: 256px 256px;
}
```

### Noise Overlay (fine grain)
```css
.noise-fine {
  background-image: url("data:image/svg+xml,%3Csvg width='256' height='256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.65' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='0.08'/%3E%3C/svg%3E");
  background-size: 256px 256px;
}
```

### Noise Overlay (coarse)
```css
.noise-coarse {
  background-image: url("data:image/svg+xml,%3Csvg width='256' height='256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.01' numOctaves='5' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='0.2'/%3E%3C/svg%3E");
  background-size: 256px 256px;
}
```

---

## Using Patterns as Overlays

Apply any pattern on top of existing content:

```css
.patterned-element {
  position: relative;
}
.patterned-element::after {
  content: '';
  position: absolute;
  inset: 0;
  background-image: url("data:image/svg+xml,..."); /* any pattern from above */
  background-size: 20px 20px;
  pointer-events: none;
  opacity: 0.5;
  mix-blend-mode: multiply; /* or overlay, soft-light, etc. */
}
```

## Customizing Colors

To change pattern colors in data-URIs, replace the URL-encoded color values:
- `%23000000` = `#000000` (black)
- `%23ffffff` = `#ffffff` (white)
- `%2300ff88` = `#00ff88` (green)

For rgba, use the `opacity` attribute on individual SVG elements rather than encoding rgba into the URI.

## Performance Notes

- Data-URI SVG patterns are lightweight (typically under 500 bytes each)
- They render as vector at any scale — no pixelation
- `background-size` controls the pattern density
- Patterns render perfectly in Playwright/Chromium screenshots
- For large areas, use `background-repeat: repeat` (default)
