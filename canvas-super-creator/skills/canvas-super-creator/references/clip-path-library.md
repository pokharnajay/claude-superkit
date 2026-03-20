# Creative CSS Clip-Path Shapes — Complete Reference Catalog

All values are ready to copy into `clip-path:` declarations. Each shape clips to 100% width/height of the element.

---

## Geometric Shapes

### Triangle (equilateral, pointing up)
```css
clip-path: polygon(50% 0%, 0% 100%, 100% 100%);
```

### Triangle (pointing right)
```css
clip-path: polygon(0% 0%, 100% 50%, 0% 100%);
```

### Triangle (pointing left)
```css
clip-path: polygon(100% 0%, 0% 50%, 100% 100%);
```

### Pentagon
```css
clip-path: polygon(50% 0%, 100% 38%, 82% 100%, 18% 100%, 0% 38%);
```

### Hexagon
```css
clip-path: polygon(25% 0%, 75% 0%, 100% 50%, 75% 100%, 25% 100%, 0% 50%);
```

### Hexagon (flat top)
```css
clip-path: polygon(50% 0%, 100% 25%, 100% 75%, 50% 100%, 0% 75%, 0% 25%);
```

### Octagon
```css
clip-path: polygon(30% 0%, 70% 0%, 100% 30%, 100% 70%, 70% 100%, 30% 100%, 0% 70%, 0% 30%);
```

### Star (5-pointed)
```css
clip-path: polygon(50% 0%, 61% 35%, 98% 35%, 68% 57%, 79% 91%, 50% 70%, 21% 91%, 32% 57%, 2% 35%, 39% 35%);
```

### Star (6-pointed / Star of David)
```css
clip-path: polygon(50% 0%, 65% 25%, 100% 25%, 80% 50%, 100% 75%, 65% 75%, 50% 100%, 35% 75%, 0% 75%, 20% 50%, 0% 25%, 35% 25%);
```

### Diamond
```css
clip-path: polygon(50% 0%, 100% 50%, 50% 100%, 0% 50%);
```

### Parallelogram
```css
clip-path: polygon(15% 0%, 100% 0%, 85% 100%, 0% 100%);
```

### Parallelogram (reversed)
```css
clip-path: polygon(0% 0%, 85% 0%, 100% 100%, 15% 100%);
```

### Arrow (right)
```css
clip-path: polygon(0% 20%, 70% 20%, 70% 0%, 100% 50%, 70% 100%, 70% 80%, 0% 80%);
```

### Arrow (left)
```css
clip-path: polygon(30% 0%, 30% 20%, 100% 20%, 100% 80%, 30% 80%, 30% 100%, 0% 50%);
```

### Cross / Plus
```css
clip-path: polygon(35% 0%, 65% 0%, 65% 35%, 100% 35%, 100% 65%, 65% 65%, 65% 100%, 35% 100%, 35% 65%, 0% 65%, 0% 35%, 35% 35%);
```

### Rhombus (wide)
```css
clip-path: polygon(50% 15%, 100% 50%, 50% 85%, 0% 50%);
```

### Trapezoid
```css
clip-path: polygon(20% 0%, 80% 0%, 100% 100%, 0% 100%);
```

### Inverted Trapezoid
```css
clip-path: polygon(0% 0%, 100% 0%, 80% 100%, 20% 100%);
```

---

## Organic Shapes

### Blob 1 (smooth)
```css
clip-path: path('M 50,5 C 75,-5 105,15 95,45 C 108,70 85,105 55,95 C 25,108 -5,80 5,50 C -5,20 25,8 50,5 Z');
/* Note: path() coordinates based on 100x100 viewBox — apply on a square element or use % */
```

### Blob 2 (wide)
```css
clip-path: polygon(
  2% 30%, 8% 12%, 22% 2%, 40% 5%, 55% 0%,
  72% 4%, 88% 10%, 98% 28%, 100% 48%,
  97% 68%, 90% 85%, 75% 96%, 58% 100%,
  40% 97%, 22% 92%, 8% 80%, 0% 60%
);
```

### Blob 3 (compact)
```css
clip-path: polygon(
  30% 2%, 55% 0%, 78% 8%, 95% 25%,
  100% 50%, 95% 75%, 80% 92%, 55% 100%,
  30% 95%, 10% 80%, 0% 55%, 2% 30%, 12% 10%
);
```

### Blob 4 (asymmetric)
```css
clip-path: polygon(
  5% 20%, 15% 5%, 35% 0%, 60% 3%, 80% 10%,
  95% 30%, 100% 55%, 92% 78%, 75% 95%,
  50% 100%, 25% 92%, 8% 75%, 0% 50%
);
```

### Blob 5 (organic circle)
```css
clip-path: polygon(
  40% 2%, 65% 0%, 85% 10%, 97% 30%,
  100% 55%, 95% 78%, 80% 95%, 55% 100%,
  30% 97%, 10% 82%, 0% 58%, 3% 32%, 18% 12%
);
```

### Wave Top (element has wavy top edge)
```css
clip-path: polygon(
  0% 15%, 5% 12%, 10% 10%, 15% 12%, 20% 15%,
  25% 12%, 30% 10%, 35% 12%, 40% 15%,
  45% 12%, 50% 10%, 55% 12%, 60% 15%,
  65% 12%, 70% 10%, 75% 12%, 80% 15%,
  85% 12%, 90% 10%, 95% 12%, 100% 15%,
  100% 100%, 0% 100%
);
```

### Wave Bottom (element has wavy bottom edge)
```css
clip-path: polygon(
  0% 0%, 100% 0%,
  100% 85%, 95% 88%, 90% 90%, 85% 88%, 80% 85%,
  75% 88%, 70% 90%, 65% 88%, 60% 85%,
  55% 88%, 50% 90%, 45% 88%, 40% 85%,
  35% 88%, 30% 90%, 25% 88%, 20% 85%,
  15% 88%, 10% 90%, 5% 88%, 0% 85%
);
```

### Teardrop
```css
clip-path: polygon(50% 0%, 80% 35%, 100% 70%, 85% 90%, 50% 100%, 15% 90%, 0% 70%, 20% 35%);
```

### Cloud
```css
clip-path: polygon(
  15% 60%, 5% 50%, 0% 40%, 5% 28%, 15% 20%,
  25% 18%, 30% 10%, 40% 5%, 52% 5%, 60% 10%,
  68% 8%, 78% 12%, 85% 20%, 92% 15%, 98% 22%,
  100% 35%, 98% 48%, 92% 55%, 100% 65%, 95% 75%,
  85% 78%, 75% 80%, 50% 80%, 25% 80%, 10% 75%,
  5% 68%
);
```

---

## Angled Cuts

### Angled 5deg (top-left to bottom-right, subtle)
```css
clip-path: polygon(0% 0%, 100% 5%, 100% 100%, 0% 95%);
```

### Angled 10deg
```css
clip-path: polygon(0% 0%, 100% 10%, 100% 100%, 0% 90%);
```

### Angled 15deg
```css
clip-path: polygon(0% 0%, 100% 15%, 100% 100%, 0% 85%);
```

### Angled Cut (top only)
```css
clip-path: polygon(0% 10%, 100% 0%, 100% 100%, 0% 100%);
```

### Angled Cut (bottom only)
```css
clip-path: polygon(0% 0%, 100% 0%, 100% 90%, 0% 100%);
```

### Chevron (pointing right)
```css
clip-path: polygon(0% 0%, 85% 0%, 100% 50%, 85% 100%, 0% 100%, 15% 50%);
```

### Chevron (pointing down)
```css
clip-path: polygon(0% 0%, 100% 0%, 100% 75%, 50% 100%, 0% 75%);
```

### Zigzag Bottom Edge
```css
clip-path: polygon(
  0% 0%, 100% 0%, 100% 80%,
  90% 90%, 80% 80%, 70% 90%, 60% 80%, 50% 90%,
  40% 80%, 30% 90%, 20% 80%, 10% 90%, 0% 80%
);
```

### Zigzag Top Edge
```css
clip-path: polygon(
  0% 20%, 10% 10%, 20% 20%, 30% 10%, 40% 20%, 50% 10%,
  60% 20%, 70% 10%, 80% 20%, 90% 10%, 100% 20%,
  100% 100%, 0% 100%
);
```

---

## Frames and Cutouts

### Circle Frame (circle cutout in center)
Use two elements — outer with background, inner with clip:
```css
/* Apply to a square container */
.circle-frame {
  clip-path: circle(45% at 50% 50%);
}
```

### Rounded Frame (rounded rectangle)
```css
/* Use border-radius instead of clip-path for rounded rects */
.rounded-frame {
  border-radius: 20px;
  overflow: hidden;
}

/* Or via clip-path for precise control */
.rounded-frame-clip {
  clip-path: inset(0 round 20px);
}
```

### Inset Rounded (with border effect)
```css
clip-path: inset(5% round 15px);
```

### Pill Shape
```css
clip-path: inset(0 round 50vh);
```

### Squircle (iOS-style rounded square)
```css
clip-path: inset(0 round 22%);
```

---

## Usage Tips

### Responsive Scaling
All `polygon()` values use percentages, so they scale with the element. For `path()`, coordinates are absolute — use a square element or wrap in a `viewBox`-aware SVG.

### Transitions
Clip-path shapes with the same number of points can be animated:
```css
.shape {
  clip-path: polygon(50% 0%, 100% 50%, 50% 100%, 0% 50%);
  transition: clip-path 0.5s ease;
}
.shape:hover {
  clip-path: polygon(0% 0%, 100% 0%, 100% 100%, 0% 100%);
}
```

### Combining with Box Shadow
`clip-path` removes box-shadow. Use `filter: drop-shadow()` instead:
```css
.clipped-with-shadow {
  clip-path: polygon(50% 0%, 100% 38%, 82% 100%, 18% 100%, 0% 38%);
  filter: drop-shadow(0 4px 12px rgba(0,0,0,0.3));
}
```

### Browser Support
- `polygon()` — all modern browsers
- `path()` — Chrome 88+, Firefox 97+, Safari 15.4+
- `inset()` — all modern browsers
- Always works perfectly in Playwright/Chromium screenshots
