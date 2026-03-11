# CSS Techniques Catalog

Comprehensive reference of CSS techniques for canvas-design HTML rendering. Every technique includes a complete, copy-paste-ready code snippet.

---

## Backgrounds & Atmosphere

### Glassmorphism Card

Frosted glass effect with backdrop blur, translucent background, and subtle border.

```css
.glass-card {
    background: rgba(255, 255, 255, 0.08);
    backdrop-filter: blur(24px);
    -webkit-backdrop-filter: blur(24px);
    border: 1px solid rgba(255, 255, 255, 0.12);
    border-radius: 16px;
    padding: 40px;
    box-shadow:
        0 8px 32px rgba(0, 0, 0, 0.3),
        inset 0 1px 0 rgba(255, 255, 255, 0.1);
}
```

For dark themes, swap to `rgba(0, 0, 0, 0.4)` background and `rgba(255, 255, 255, 0.06)` border.

---

### Gradient Orbs (Ambient Blobs)

Large blurred circles positioned behind content to create atmosphere and color depth.

```css
.orb {
    position: absolute;
    border-radius: 50%;
    filter: blur(80px);
    opacity: 0.6;
    pointer-events: none;
}
.orb-1 {
    width: 500px;
    height: 500px;
    background: #E8622B;
    top: -100px;
    left: -150px;
}
.orb-2 {
    width: 400px;
    height: 400px;
    background: #00D4AA;
    bottom: -80px;
    right: -120px;
}
.orb-3 {
    width: 300px;
    height: 300px;
    background: #F5A623;
    top: 40%;
    left: 60%;
}
```

Use 2-4 orbs max. Place them at canvas edges so they bleed off. Vary sizes by at least 30%.

---

### SVG Noise Overlay

Inline SVG with feTurbulence to add organic grain texture over the entire canvas.

```css
.noise-overlay {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    pointer-events: none;
    z-index: 999;
    opacity: 0.03;
}
```

```html
<div class="noise-overlay">
    <svg width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
        <filter id="noise">
            <feTurbulence type="fractalNoise" baseFrequency="0.65" numOctaves="4" stitchTiles="stitch"/>
            <feColorMatrix type="saturate" values="0"/>
        </filter>
        <rect width="100%" height="100%" filter="url(#noise)"/>
    </svg>
</div>
```

Adjust `baseFrequency` for grain size: 0.5 = coarse, 0.8 = fine. Keep opacity between 0.02-0.06.

---

### Grid Pattern Background

Repeating line grid with radial fade mask for depth.

```css
.grid-bg {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background:
        repeating-linear-gradient(
            0deg,
            rgba(255, 255, 255, 0.03) 0px,
            rgba(255, 255, 255, 0.03) 1px,
            transparent 1px,
            transparent 60px
        ),
        repeating-linear-gradient(
            90deg,
            rgba(255, 255, 255, 0.03) 0px,
            rgba(255, 255, 255, 0.03) 1px,
            transparent 1px,
            transparent 60px
        );
    mask-image: radial-gradient(ellipse 70% 70% at 50% 50%, black 30%, transparent 70%);
    -webkit-mask-image: radial-gradient(ellipse 70% 70% at 50% 50%, black 30%, transparent 70%);
    pointer-events: none;
}
```

The radial mask fades the grid at edges, preventing a harsh cutoff. Adjust grid spacing (60px) to taste.

---

### Mesh Gradient

Multiple overlapping radial gradients to create a rich, multi-color atmospheric background.

```css
.mesh-gradient {
    background:
        radial-gradient(ellipse at 20% 30%, #E8622B33 0%, transparent 50%),
        radial-gradient(ellipse at 80% 20%, #00D4AA33 0%, transparent 50%),
        radial-gradient(ellipse at 50% 80%, #F5A62333 0%, transparent 50%),
        radial-gradient(ellipse at 70% 60%, #C4453D22 0%, transparent 40%),
        linear-gradient(135deg, #1C1210 0%, #0A1628 100%);
}
```

Layer 3-5 radial gradients over a base linear gradient. Use palette colors at low alpha (0x22-0x44).

---

### Conic Gradient

Rotational gradient emanating from a center point.

```css
.conic-bg {
    background: conic-gradient(
        from 45deg at 50% 50%,
        #1C1210 0deg,
        #3D2B24 90deg,
        #E8622B 180deg,
        #C4453D 270deg,
        #1C1210 360deg
    );
}
```

Useful for spotlight effects, clock-like divisions, or abstract radial compositions.

---

## Blending & Compositing

### mix-blend-mode

Apply blending between stacked elements.

```css
/* Multiply: darkens, great for overlaying texture on images */
.multiply-layer {
    mix-blend-mode: multiply;
}

/* Screen: lightens, good for light leaks and highlights */
.screen-layer {
    mix-blend-mode: screen;
}

/* Overlay: increases contrast, rich color interactions */
.overlay-layer {
    mix-blend-mode: overlay;
}

/* Color-dodge: dramatic brightening, neon glow effects */
.dodge-layer {
    mix-blend-mode: color-dodge;
}

/* Difference: inverts colors where layers overlap, psychedelic effects */
.diff-layer {
    mix-blend-mode: difference;
}
```

### background-blend-mode

Blend multiple background layers within the same element.

```css
.blended-bg {
    background:
        url('texture.png'),
        linear-gradient(135deg, #E8622B, #C4453D);
    background-blend-mode: overlay;
    background-size: cover, cover;
}
```

---

## Shapes & Masking

### clip-path Shapes

Cut elements into geometric shapes.

```css
/* Triangle */
.triangle {
    clip-path: polygon(50% 0%, 0% 100%, 100% 100%);
}

/* Hexagon */
.hexagon {
    clip-path: polygon(25% 0%, 75% 0%, 100% 50%, 75% 100%, 25% 100%, 0% 50%);
}

/* Angled section */
.angled {
    clip-path: polygon(0 0, 100% 0, 100% 80%, 0 100%);
}

/* Circle */
.circle-mask {
    clip-path: circle(40% at 50% 50%);
}

/* Ellipse */
.ellipse-mask {
    clip-path: ellipse(45% 35% at 50% 50%);
}

/* Custom path (star shape) */
.star {
    clip-path: path('M50,0 L61,35 L98,35 L68,57 L79,91 L50,70 L21,91 L32,57 L2,35 L39,35 Z');
}
```

### mask-image Gradient Fade

Fade elements to transparency using gradient masks.

```css
/* Fade bottom edge */
.fade-bottom {
    mask-image: linear-gradient(to bottom, black 60%, transparent 100%);
    -webkit-mask-image: linear-gradient(to bottom, black 60%, transparent 100%);
}

/* Fade from center outward */
.fade-edges {
    mask-image: radial-gradient(ellipse 60% 60% at 50% 50%, black 40%, transparent 70%);
    -webkit-mask-image: radial-gradient(ellipse 60% 60% at 50% 50%, black 40%, transparent 70%);
}

/* Diagonal fade */
.fade-diagonal {
    mask-image: linear-gradient(135deg, black 30%, transparent 80%);
    -webkit-mask-image: linear-gradient(135deg, black 30%, transparent 80%);
}
```

---

## Typography Effects

### Gradient Text

Fill text with a gradient using background-clip.

```css
.gradient-text {
    background: linear-gradient(135deg, #E8622B, #F5A623, #C4453D);
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
    color: transparent;
}
```

### Text Stroke (Outline Text)

Hollow text with visible stroke.

```css
.stroke-text {
    -webkit-text-stroke: 2px #F5E6D3;
    -webkit-text-fill-color: transparent;
    color: transparent;
    font-size: 120px;
    font-weight: 700;
}
```

For a filled + stroked look, use `paint-order: stroke fill`:

```css
.filled-stroke-text {
    -webkit-text-stroke: 3px #1C1210;
    color: #F5E6D3;
    paint-order: stroke fill;
}
```

### Text Shadow Stacking

Multiple shadows for depth, glow, or 3D effects.

```css
/* Soft ambient glow */
.glow-text {
    text-shadow:
        0 0 10px rgba(232, 98, 43, 0.5),
        0 0 30px rgba(232, 98, 43, 0.3),
        0 0 60px rgba(232, 98, 43, 0.15);
}

/* Hard 3D extrusion */
.extrude-text {
    text-shadow:
        1px 1px 0 #3D2B24,
        2px 2px 0 #3D2B24,
        3px 3px 0 #3D2B24,
        4px 4px 0 #3D2B24,
        5px 5px 10px rgba(0, 0, 0, 0.4);
}

/* Long shadow */
.long-shadow-text {
    text-shadow:
        1px 1px 0 rgba(0,0,0,0.1),
        2px 2px 0 rgba(0,0,0,0.1),
        3px 3px 0 rgba(0,0,0,0.1),
        4px 4px 0 rgba(0,0,0,0.1),
        5px 5px 0 rgba(0,0,0,0.1),
        6px 6px 0 rgba(0,0,0,0.1),
        7px 7px 0 rgba(0,0,0,0.1),
        8px 8px 0 rgba(0,0,0,0.1);
}
```

### Letter-Spacing & Font Features

Fine-tune typographic detail.

```css
/* Tight display tracking */
.display-type {
    letter-spacing: -0.03em;
    font-feature-settings: 'kern' 1, 'liga' 1;
}

/* Wide caps tracking */
.caps-label {
    text-transform: uppercase;
    letter-spacing: 0.12em;
    font-feature-settings: 'smcp' 1;
}

/* Tabular numbers for data */
.data-number {
    font-feature-settings: 'tnum' 1;
    font-variant-numeric: tabular-nums;
}

/* Oldstyle numbers for editorial */
.editorial-number {
    font-feature-settings: 'onum' 1;
    font-variant-numeric: oldstyle-nums;
}
```

---

## 3D & Transforms

### Perspective Cards

Add depth with CSS 3D transforms.

```css
.perspective-container {
    perspective: 1200px;
}
.tilted-card {
    transform: rotateX(5deg) rotateY(-8deg);
    transform-style: preserve-3d;
    box-shadow: 20px 20px 60px rgba(0, 0, 0, 0.4);
}
```

### Skewed Sections

Dynamic angular compositions.

```css
.skewed-section {
    transform: skewY(-3deg);
    overflow: hidden;
}
.skewed-section > * {
    transform: skewY(3deg); /* Counter-skew content to keep it readable */
}
```

### Multi-Transform Chains

Combine transforms for complex positioning.

```css
.dynamic-element {
    transform: translateX(-20px) rotate(-5deg) scale(1.05);
    transform-origin: bottom left;
}
```

---

## Decorative Elements

### Shine Sweep

Animated or static diagonal shine across a surface.

```css
.shine-element {
    position: relative;
    overflow: hidden;
}
.shine-element::after {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: linear-gradient(
        105deg,
        transparent 40%,
        rgba(255, 255, 255, 0.08) 45%,
        rgba(255, 255, 255, 0.15) 50%,
        rgba(255, 255, 255, 0.08) 55%,
        transparent 60%
    );
    transform: rotate(25deg);
    pointer-events: none;
}
```

### Floating Shapes

Decorative circles or geometric shapes scattered in the background.

```css
.floating-circle {
    position: absolute;
    border-radius: 50%;
    border: 1px solid rgba(255, 255, 255, 0.08);
    background: transparent;
    pointer-events: none;
}
.circle-1 {
    width: 200px;
    height: 200px;
    top: 10%;
    right: 15%;
}
.circle-2 {
    width: 80px;
    height: 80px;
    bottom: 20%;
    left: 10%;
    border-width: 2px;
    border-color: rgba(232, 98, 43, 0.15);
}
.circle-3 {
    width: 350px;
    height: 350px;
    top: 50%;
    left: -5%;
    transform: translate(0, -50%);
    border-style: dashed;
    border-color: rgba(255, 255, 255, 0.04);
}
```

Vary sizes, positions, and opacity. Use outline-only (border, no fill) to avoid the "overlapping circles" anti-pattern.

### Border Gradients via ::before

Gradient borders on elements using a pseudo-element technique.

```css
.gradient-border {
    position: relative;
    background: #1C1210;
    border-radius: 12px;
    padding: 40px;
}
.gradient-border::before {
    content: '';
    position: absolute;
    top: -1px;
    left: -1px;
    right: -1px;
    bottom: -1px;
    border-radius: 13px;
    background: linear-gradient(135deg, #E8622B, #F5A623, #C4453D);
    z-index: -1;
}
```

---

## Advanced Layout

### CSS Grid for Precise Placement

```css
.design-grid {
    display: grid;
    grid-template-columns: repeat(12, 1fr);
    grid-template-rows: repeat(8, 1fr);
    gap: 0;
    width: 100%;
    height: 100%;
}
.element-span {
    grid-column: 2 / 8;
    grid-row: 3 / 6;
    display: flex;
    align-items: center;
}
```

### Absolute Positioning for Layered Compositions

```css
body {
    position: relative;
}
.layer-bg { position: absolute; top: 0; left: 0; width: 100%; height: 100%; z-index: 1; }
.layer-texture { position: absolute; top: 0; left: 0; width: 100%; height: 100%; z-index: 2; }
.layer-shapes { position: absolute; top: 0; left: 0; width: 100%; height: 100%; z-index: 3; }
.layer-content { position: absolute; top: 0; left: 0; width: 100%; height: 100%; z-index: 4; }
.layer-grain { position: absolute; top: 0; left: 0; width: 100%; height: 100%; z-index: 5; pointer-events: none; }
```

### Flexbox Centering with Offset

```css
.centered-content {
    display: flex;
    flex-direction: column;
    align-items: flex-start; /* Left-aligned, not centered */
    justify-content: center;
    padding-left: 12%;
    height: 100%;
}
```

---

## Utility Patterns

### Safe Zone Visualization (Debug Only)

```css
.safe-zone-debug {
    position: absolute;
    top: 60px;
    right: 60px;
    bottom: 60px;
    left: 60px;
    border: 1px dashed rgba(255, 0, 0, 0.3);
    pointer-events: none;
    z-index: 9999;
}
```

### Contrast Overlay (Debug Only)

```css
.contrast-check {
    filter: grayscale(100%) contrast(200%);
}
```

Apply temporarily to verify that the visual hierarchy reads in pure black and white.
