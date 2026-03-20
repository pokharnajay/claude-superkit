# CSS Halftone Techniques — Complete Reference Catalog

Pure CSS halftone patterns using repeating gradients. Each is self-contained and ready to apply as a `background` property or overlay via pseudo-element.

---

## 1. Dot Halftone

Regular grid of circular dots. Classic halftone screen effect.

```css
.halftone-dots {
  background:
    radial-gradient(circle, #000 25%, transparent 26%) 0 0 / 8px 8px;
  background-color: #ffffff;
}
```

### Customizable Dot Halftone
```css
.halftone-dots-custom {
  --dot-color: #000000;
  --bg-color: #ffffff;
  --dot-size: 25%;    /* percentage of cell filled by dot */
  --cell-size: 8px;   /* grid spacing */

  background:
    radial-gradient(circle, var(--dot-color) var(--dot-size), transparent calc(var(--dot-size) + 1%))
    0 0 / var(--cell-size) var(--cell-size);
  background-color: var(--bg-color);
}
```

### Fine Dot Halftone (print-like)
```css
.halftone-dots-fine {
  background:
    radial-gradient(circle, #000 20%, transparent 21%) 0 0 / 4px 4px;
  background-color: #fff;
}
```

### Large Dot Halftone (pop art)
```css
.halftone-dots-large {
  background:
    radial-gradient(circle, #000 30%, transparent 31%) 0 0 / 16px 16px;
  background-color: #fff;
}
```

### Offset Dot Halftone (staggered grid)
```css
.halftone-dots-offset {
  background:
    radial-gradient(circle, #000 25%, transparent 26%) 0 0 / 8px 8px,
    radial-gradient(circle, #000 25%, transparent 26%) 4px 4px / 8px 8px;
  background-color: #ffffff;
}
```

### Using as Overlay
```css
.element-with-halftone {
  position: relative;
}
.element-with-halftone::after {
  content: '';
  position: absolute;
  inset: 0;
  background:
    radial-gradient(circle, rgba(0,0,0,0.4) 25%, transparent 26%) 0 0 / 6px 6px;
  pointer-events: none;
  mix-blend-mode: multiply;
}
```

---

## 2. Line Halftone

Parallel lines at an angle. Simulates engraving or line screen printing.

### 45-Degree Lines
```css
.halftone-lines-45 {
  background: repeating-linear-gradient(
    45deg,
    #000 0px,
    #000 1px,
    transparent 1px,
    transparent 4px
  );
  background-color: #ffffff;
}
```

### Horizontal Lines
```css
.halftone-lines-horizontal {
  background: repeating-linear-gradient(
    0deg,
    #000 0px,
    #000 1px,
    transparent 1px,
    transparent 4px
  );
  background-color: #ffffff;
}
```

### Vertical Lines
```css
.halftone-lines-vertical {
  background: repeating-linear-gradient(
    90deg,
    #000 0px,
    #000 1px,
    transparent 1px,
    transparent 4px
  );
  background-color: #ffffff;
}
```

### Customizable Line Halftone
```css
.halftone-lines-custom {
  --line-color: #000000;
  --bg-color: #ffffff;
  --angle: 45deg;
  --line-width: 1px;
  --gap: 4px;

  background: repeating-linear-gradient(
    var(--angle),
    var(--line-color) 0px,
    var(--line-color) var(--line-width),
    transparent var(--line-width),
    transparent var(--gap)
  );
  background-color: var(--bg-color);
}
```

### Thick Diagonal Lines
```css
.halftone-lines-thick {
  background: repeating-linear-gradient(
    45deg,
    #000 0px,
    #000 3px,
    transparent 3px,
    transparent 8px
  );
  background-color: #ffffff;
}
```

---

## 3. Cross Halftone

Overlapping perpendicular line patterns creating a crosshatch texture.

### Crosshatch (0 and 90 degrees)
```css
.halftone-cross {
  background:
    repeating-linear-gradient(
      0deg,
      rgba(0,0,0,0.5) 0px,
      rgba(0,0,0,0.5) 1px,
      transparent 1px,
      transparent 5px
    ),
    repeating-linear-gradient(
      90deg,
      rgba(0,0,0,0.5) 0px,
      rgba(0,0,0,0.5) 1px,
      transparent 1px,
      transparent 5px
    );
  background-color: #ffffff;
}
```

### Diagonal Crosshatch (45 and 135 degrees)
```css
.halftone-cross-diagonal {
  background:
    repeating-linear-gradient(
      45deg,
      rgba(0,0,0,0.4) 0px,
      rgba(0,0,0,0.4) 1px,
      transparent 1px,
      transparent 6px
    ),
    repeating-linear-gradient(
      -45deg,
      rgba(0,0,0,0.4) 0px,
      rgba(0,0,0,0.4) 1px,
      transparent 1px,
      transparent 6px
    );
  background-color: #ffffff;
}
```

### Triple Crosshatch (0, 60, 120 degrees)
```css
.halftone-cross-triple {
  background:
    repeating-linear-gradient(
      0deg,
      rgba(0,0,0,0.3) 0px,
      rgba(0,0,0,0.3) 1px,
      transparent 1px,
      transparent 6px
    ),
    repeating-linear-gradient(
      60deg,
      rgba(0,0,0,0.3) 0px,
      rgba(0,0,0,0.3) 1px,
      transparent 1px,
      transparent 6px
    ),
    repeating-linear-gradient(
      120deg,
      rgba(0,0,0,0.3) 0px,
      rgba(0,0,0,0.3) 1px,
      transparent 1px,
      transparent 6px
    );
  background-color: #ffffff;
}
```

---

## 4. Circular Halftone

Concentric rings radiating from center.

```css
.halftone-circular {
  background: repeating-radial-gradient(
    circle at 50% 50%,
    #000 0px,
    #000 1px,
    transparent 1px,
    transparent 6px
  );
  background-color: #ffffff;
}
```

### Off-Center Circular
```css
.halftone-circular-offset {
  background: repeating-radial-gradient(
    circle at 30% 40%,
    #000 0px,
    #000 1px,
    transparent 1px,
    transparent 8px
  );
  background-color: #ffffff;
}
```

### Thick Rings
```css
.halftone-circular-thick {
  background: repeating-radial-gradient(
    circle at 50% 50%,
    #000 0px,
    #000 2px,
    transparent 2px,
    transparent 10px
  );
  background-color: #ffffff;
}
```

### Elliptical Rings
```css
.halftone-circular-ellipse {
  background: repeating-radial-gradient(
    ellipse at 50% 50%,
    #000 0px,
    #000 1px,
    transparent 1px,
    transparent 6px
  );
  background-color: #ffffff;
}
```

---

## 5. Color CMYK Halftone

Four overlapping dot layers at different angles, simulating CMYK printing separation.

```css
.halftone-cmyk {
  position: relative;
  background-color: #ffffff;
}
.halftone-cmyk::before,
.halftone-cmyk::after {
  content: '';
  position: absolute;
  inset: 0;
  pointer-events: none;
}

/* Cyan layer (15 degrees) */
.halftone-cmyk::before {
  background:
    radial-gradient(circle, rgba(0, 255, 255, 0.5) 25%, transparent 26%) 0 0 / 6px 6px;
  transform: rotate(15deg);
  mix-blend-mode: multiply;
}

/* Magenta layer (75 degrees) */
.halftone-cmyk::after {
  background:
    radial-gradient(circle, rgba(255, 0, 255, 0.5) 25%, transparent 26%) 0 0 / 6px 6px;
  transform: rotate(75deg);
  mix-blend-mode: multiply;
}
```

For the full 4-color CMYK, use 4 child elements:

```html
<div class="halftone-cmyk-full">
  <div class="cmyk-c"></div>
  <div class="cmyk-m"></div>
  <div class="cmyk-y"></div>
  <div class="cmyk-k"></div>
</div>
```

```css
.halftone-cmyk-full {
  position: relative;
  width: 100%;
  height: 100%;
  background: #ffffff;
  overflow: hidden;
}

.halftone-cmyk-full > div {
  position: absolute;
  inset: -20%;   /* overflow to compensate for rotation */
  width: 140%;
  height: 140%;
  pointer-events: none;
  mix-blend-mode: multiply;
}

/* Cyan — 15deg */
.cmyk-c {
  background: radial-gradient(circle, rgba(0, 255, 255, 0.6) 25%, transparent 26%) 0 0 / 8px 8px;
  transform: rotate(15deg);
}

/* Magenta — 75deg */
.cmyk-m {
  background: radial-gradient(circle, rgba(255, 0, 255, 0.6) 25%, transparent 26%) 0 0 / 8px 8px;
  transform: rotate(75deg);
}

/* Yellow — 0deg */
.cmyk-y {
  background: radial-gradient(circle, rgba(255, 255, 0, 0.6) 25%, transparent 26%) 0 0 / 8px 8px;
  transform: rotate(0deg);
}

/* Key (Black) — 45deg */
.cmyk-k {
  background: radial-gradient(circle, rgba(0, 0, 0, 0.4) 20%, transparent 21%) 0 0 / 8px 8px;
  transform: rotate(45deg);
}
```

---

## Tuning Parameters

### Dot Size vs Gap
- **Dot percentage** (e.g., `25%` in radial-gradient stop) controls dot size relative to cell
- **Cell size** (e.g., `8px 8px` in background-size) controls grid spacing
- Ratio of dot% to cell controls density: `30% / 6px` = dense, `20% / 12px` = sparse

### Color and Opacity
- Use `rgba()` for the pattern color to control intensity
- Combine with `mix-blend-mode: multiply` for overlay on images
- Dark-on-light is classic halftone; light-on-dark creates a screen print feel:
```css
.halftone-inverted {
  background:
    radial-gradient(circle, rgba(255,255,255,0.5) 25%, transparent 26%) 0 0 / 8px 8px;
  background-color: #1a1a1a;
}
```

### Converting to Overlay
Any halftone pattern can be used as an overlay on existing content:
```css
.halftone-overlay {
  position: relative;
}
.halftone-overlay::after {
  content: '';
  position: absolute;
  inset: 0;
  background: radial-gradient(circle, rgba(0,0,0,0.3) 25%, transparent 26%) 0 0 / 8px 8px;
  pointer-events: none;
  mix-blend-mode: multiply;
}
```
