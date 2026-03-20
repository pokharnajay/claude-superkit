# Advanced Text CSS Effects — Complete Reference Catalog

Complete, copy-paste-ready CSS for every text effect. Each block is self-contained.

---

## 1. 3D Text (Stacked Shadow)

Creates a solid 3D extrusion effect using many text-shadow layers. Uses CSS custom properties for easy tuning.

```css
.text-3d {
  --depth: 50;
  --shadow-color-r: 80;
  --shadow-color-g: 40;
  --shadow-color-b: 120;

  font-size: 80px;
  font-weight: 900;
  color: #a855f7;
  text-shadow:
    1px 1px 0 rgb(var(--shadow-color-r), var(--shadow-color-g), var(--shadow-color-b)),
    2px 2px 0 rgb(var(--shadow-color-r), var(--shadow-color-g), var(--shadow-color-b)),
    3px 3px 0 rgb(var(--shadow-color-r), var(--shadow-color-g), var(--shadow-color-b)),
    4px 4px 0 rgb(var(--shadow-color-r), var(--shadow-color-g), var(--shadow-color-b)),
    5px 5px 0 rgb(var(--shadow-color-r), var(--shadow-color-g), var(--shadow-color-b)),
    6px 6px 0 rgb(var(--shadow-color-r), var(--shadow-color-g), var(--shadow-color-b)),
    7px 7px 0 rgb(var(--shadow-color-r), var(--shadow-color-g), var(--shadow-color-b)),
    8px 8px 0 rgb(var(--shadow-color-r), var(--shadow-color-g), var(--shadow-color-b)),
    9px 9px 0 rgb(var(--shadow-color-r), var(--shadow-color-g), var(--shadow-color-b)),
    10px 10px 0 rgb(var(--shadow-color-r), var(--shadow-color-g), var(--shadow-color-b)),
    11px 11px 15px rgba(0, 0, 0, 0.35);
}
```

### 3D Text (Isometric direction — down-right)
```css
.text-3d-iso {
  font-size: 80px;
  font-weight: 900;
  color: #3b82f6;
  text-shadow:
    1px 1px 0 #1e40af,
    2px 2px 0 #1e3a8a,
    3px 3px 0 #1e3580,
    4px 4px 0 #1e3075,
    5px 5px 0 #1e2b6a,
    6px 6px 0 #1e2660,
    7px 7px 0 #1e2155,
    8px 8px 0 #1e1c4a,
    9px 9px 20px rgba(0, 0, 0, 0.4);
}
```

---

## 2. Neon Glow

Multi-layer text-shadow with increasing blur radius for realistic neon tube effect.

```css
.text-neon {
  font-size: 72px;
  font-weight: 700;
  color: #fff;
  text-shadow:
    0 0 7px rgba(255, 255, 255, 0.9),
    0 0 10px rgba(255, 255, 255, 0.7),
    0 0 21px rgba(255, 255, 255, 0.5),
    0 0 42px rgba(0, 255, 255, 0.8),
    0 0 82px rgba(0, 255, 255, 0.6),
    0 0 92px rgba(0, 255, 255, 0.4),
    0 0 102px rgba(0, 255, 255, 0.2),
    0 0 151px rgba(0, 255, 255, 0.1);
}
```

### Neon Pink
```css
.text-neon-pink {
  color: #fff;
  text-shadow:
    0 0 7px rgba(255, 255, 255, 0.9),
    0 0 10px rgba(255, 255, 255, 0.7),
    0 0 21px rgba(255, 255, 255, 0.5),
    0 0 42px rgba(255, 0, 128, 0.8),
    0 0 82px rgba(255, 0, 128, 0.6),
    0 0 92px rgba(255, 0, 128, 0.4),
    0 0 102px rgba(255, 0, 128, 0.2);
}
```

### Neon Green
```css
.text-neon-green {
  color: #fff;
  text-shadow:
    0 0 7px rgba(255, 255, 255, 0.9),
    0 0 10px rgba(255, 255, 255, 0.7),
    0 0 21px rgba(255, 255, 255, 0.5),
    0 0 42px rgba(0, 255, 100, 0.8),
    0 0 82px rgba(0, 255, 100, 0.6),
    0 0 92px rgba(0, 255, 100, 0.4),
    0 0 102px rgba(0, 255, 100, 0.2);
}
```

### Subtle Neon (less intense, more sophisticated)
```css
.text-neon-subtle {
  color: rgba(255, 255, 255, 0.95);
  text-shadow:
    0 0 5px rgba(255, 255, 255, 0.6),
    0 0 20px rgba(100, 200, 255, 0.4),
    0 0 40px rgba(100, 200, 255, 0.2);
}
```

---

## 3. Retro Chrome

Gradient fill with stroke outline for a metallic chrome look.

```css
.text-chrome {
  font-size: 80px;
  font-weight: 900;
  text-transform: uppercase;
  background: linear-gradient(
    180deg,
    #e8e8e8 0%,
    #c0c0c0 25%,
    #ffffff 50%,
    #a0a0a0 75%,
    #d0d0d0 100%
  );
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
  -webkit-text-stroke: 1px rgba(0, 0, 0, 0.15);
  filter: drop-shadow(2px 4px 6px rgba(0, 0, 0, 0.4));
}
```

### Gold Chrome
```css
.text-chrome-gold {
  font-size: 80px;
  font-weight: 900;
  text-transform: uppercase;
  background: linear-gradient(
    180deg,
    #f0d060 0%,
    #c09030 20%,
    #ffe080 45%,
    #d4a040 55%,
    #f0c050 80%,
    #a07020 100%
  );
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
  -webkit-text-stroke: 1px rgba(100, 60, 0, 0.2);
  filter: drop-shadow(2px 4px 6px rgba(0, 0, 0, 0.3));
}
```

---

## 4. Letterpress / Debossed

Simulates text pressed into a surface using light and dark shadows.

```css
.text-letterpress {
  font-size: 48px;
  font-weight: 800;
  color: rgba(0, 0, 0, 0.15);
  text-shadow:
    0 1px 0 rgba(255, 255, 255, 0.6),
    0 -1px 0 rgba(0, 0, 0, 0.15);
}
```

### Letterpress on Dark Background
```css
.text-letterpress-dark {
  font-size: 48px;
  font-weight: 800;
  color: rgba(255, 255, 255, 0.08);
  text-shadow:
    0 -1px 0 rgba(0, 0, 0, 0.5),
    0 1px 0 rgba(255, 255, 255, 0.1);
}
```

### Embossed (raised from surface)
```css
.text-embossed {
  font-size: 48px;
  font-weight: 800;
  color: rgba(128, 128, 128, 0.1);
  text-shadow:
    0 -1px 0 rgba(255, 255, 255, 0.5),
    0 1px 0 rgba(0, 0, 0, 0.3);
}
```

---

## 5. Glitch

Multi-layer offset with clip-path slicing for a digital glitch effect. Uses keyframes but you can capture a specific frame by setting fixed transforms.

```css
.text-glitch {
  position: relative;
  font-size: 80px;
  font-weight: 900;
  color: #fff;
  text-transform: uppercase;
}

/* Red channel offset */
.text-glitch::before {
  content: attr(data-text);
  position: absolute;
  left: -3px;
  top: 0;
  color: #ff0040;
  clip-path: inset(10% 0 60% 0);
  mix-blend-mode: screen;
}

/* Cyan channel offset */
.text-glitch::after {
  content: attr(data-text);
  position: absolute;
  left: 3px;
  top: 0;
  color: #00ffff;
  clip-path: inset(55% 0 10% 0);
  mix-blend-mode: screen;
}
```

```html
<h1 class="text-glitch" data-text="GLITCH">GLITCH</h1>
```

### Static Glitch (no animation, perfect for screenshots)
```css
.text-glitch-static {
  position: relative;
  font-size: 80px;
  font-weight: 900;
  color: #fff;
}
.text-glitch-static::before {
  content: attr(data-text);
  position: absolute;
  left: -2px;
  top: -1px;
  color: #ff0040;
  clip-path: polygon(0 15%, 100% 15%, 100% 30%, 0 30%, 0 50%, 100% 50%, 100% 55%, 0 55%);
  mix-blend-mode: screen;
}
.text-glitch-static::after {
  content: attr(data-text);
  position: absolute;
  left: 2px;
  top: 1px;
  color: #00ffff;
  clip-path: polygon(0 65%, 100% 65%, 100% 75%, 0 75%, 0 85%, 100% 85%, 100% 90%, 0 90%);
  mix-blend-mode: screen;
}
```

---

## 6. Gradient Text

Text filled with gradient color using background-clip.

### Linear Gradient
```css
.text-gradient-linear {
  font-size: 72px;
  font-weight: 800;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
}
```

### Radial Gradient
```css
.text-gradient-radial {
  font-size: 72px;
  font-weight: 800;
  background: radial-gradient(circle at 30% 40%, #ff6b6b 0%, #4ecdc4 50%, #2c3e50 100%);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
}
```

### Conic Gradient (rainbow)
```css
.text-gradient-conic {
  font-size: 72px;
  font-weight: 800;
  background: conic-gradient(from 0deg, #ff0000, #ff8800, #ffff00, #00ff00, #0088ff, #8800ff, #ff0000);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
}
```

### Multi-stop Gradient
```css
.text-gradient-multi {
  font-size: 72px;
  font-weight: 800;
  background: linear-gradient(90deg, #f093fb 0%, #f5576c 25%, #ffd93d 50%, #6bcb77 75%, #4d96ff 100%);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
}
```

---

## 7. Knockout Text

Text is transparent, revealing the background behind it.

```css
.text-knockout-container {
  position: relative;
  background: url('image.jpg') center/cover;
  /* or any gradient / pattern background */
}

.text-knockout {
  font-size: 120px;
  font-weight: 900;
  text-transform: uppercase;
  background: inherit;
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
}
```

### Knockout with Solid Overlay
```css
.knockout-overlay {
  position: relative;
  width: 100%;
  height: 100%;
  overflow: hidden;
}

.knockout-bg {
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, #ff6b6b, #ffd93d, #6bcb77, #4d96ff);
}

.knockout-panel {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 100%;
  background: #1a1a2e;
  mix-blend-mode: screen;
}

.knockout-panel h1 {
  font-size: 15vw;
  font-weight: 900;
  color: #000;
  /* Black text on white bg + screen blend = transparent cutout */
}
```

---

## 8. Stencil / Outlined Text

Text rendered as outline only, with optional dashed stroke.

```css
.text-stencil {
  font-size: 80px;
  font-weight: 900;
  text-transform: uppercase;
  color: transparent;
  -webkit-text-stroke: 2px #ffffff;
}
```

### Thick Outline
```css
.text-stencil-thick {
  font-size: 80px;
  font-weight: 900;
  color: transparent;
  -webkit-text-stroke: 4px #3b82f6;
}
```

### Double Outline (using pseudo-element)
```css
.text-double-outline {
  position: relative;
  font-size: 80px;
  font-weight: 900;
  color: transparent;
  -webkit-text-stroke: 2px #ffffff;
}
.text-double-outline::after {
  content: attr(data-text);
  position: absolute;
  inset: 0;
  color: transparent;
  -webkit-text-stroke: 1px rgba(255, 255, 255, 0.3);
  transform: scale(1.02);
}
```

### Dashed Outline (SVG method)
```html
<svg viewBox="0 0 800 200" width="800" height="200">
  <text x="50%" y="50%" dominant-baseline="central" text-anchor="middle"
        font-size="120" font-weight="900" font-family="system-ui, sans-serif"
        fill="none" stroke="#ffffff" stroke-width="2"
        stroke-dasharray="8 4">
    STENCIL
  </text>
</svg>
```

---

## 9. Long Shadow

Diagonal shadow projection extending from text — classic flat design technique.

```css
.text-long-shadow {
  font-size: 80px;
  font-weight: 900;
  color: #ffffff;
  text-shadow:
    1px 1px 0 rgba(0,0,0,0.15),
    2px 2px 0 rgba(0,0,0,0.14),
    3px 3px 0 rgba(0,0,0,0.13),
    4px 4px 0 rgba(0,0,0,0.12),
    5px 5px 0 rgba(0,0,0,0.11),
    6px 6px 0 rgba(0,0,0,0.10),
    7px 7px 0 rgba(0,0,0,0.09),
    8px 8px 0 rgba(0,0,0,0.08),
    9px 9px 0 rgba(0,0,0,0.07),
    10px 10px 0 rgba(0,0,0,0.06),
    12px 12px 0 rgba(0,0,0,0.05),
    14px 14px 0 rgba(0,0,0,0.04),
    16px 16px 0 rgba(0,0,0,0.03),
    18px 18px 0 rgba(0,0,0,0.02),
    20px 20px 0 rgba(0,0,0,0.01),
    25px 25px 0 rgba(0,0,0,0.005),
    30px 30px 0 rgba(0,0,0,0.003);
}
```

### Long Shadow (solid color, flat)
```css
.text-long-shadow-flat {
  font-size: 80px;
  font-weight: 900;
  color: #e74c3c;
  text-shadow:
    1px 1px 0 #c0392b,
    2px 2px 0 #c0392b,
    3px 3px 0 #c0392b,
    4px 4px 0 #c0392b,
    5px 5px 0 #c0392b,
    6px 6px 0 #c0392b,
    7px 7px 0 #c0392b,
    8px 8px 0 #c0392b,
    9px 9px 0 #c0392b,
    10px 10px 0 #c0392b,
    11px 11px 0 #c0392b,
    12px 12px 0 #c0392b,
    13px 13px 15px rgba(0,0,0,0.2);
}
```

---

## 10. Fire Text

Multi-color text-shadow simulating flames — warm yellows, oranges, and reds.

```css
.text-fire {
  font-size: 80px;
  font-weight: 900;
  color: #fff;
  text-shadow:
    0 0 4px #fff,
    0 -2px 8px #ff3,
    0 -4px 12px #ff3,
    0 -6px 16px #fd3,
    0 -8px 24px #fc0,
    0 -10px 32px #f90,
    0 -14px 40px #f60,
    0 -18px 48px #f30,
    0 -22px 56px #f00,
    0 -26px 64px #c00,
    0 -30px 80px rgba(200, 0, 0, 0.5);
}
```

### Blue Fire
```css
.text-fire-blue {
  font-size: 80px;
  font-weight: 900;
  color: #fff;
  text-shadow:
    0 0 4px #fff,
    0 -2px 8px #cdf,
    0 -4px 12px #8bf,
    0 -6px 16px #68f,
    0 -8px 24px #46f,
    0 -10px 32px #24f,
    0 -14px 40px #00f,
    0 -18px 48px #00c,
    0 -22px 56px #008,
    0 -26px 64px #006,
    0 -30px 80px rgba(0, 0, 100, 0.5);
}
```

---

## Combining Effects

Multiple text effects can be combined:

```css
/* Gradient text + glow */
.text-gradient-glow {
  font-size: 72px;
  font-weight: 800;
  background: linear-gradient(135deg, #667eea, #764ba2);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
  filter: drop-shadow(0 0 20px rgba(102, 126, 234, 0.5));
}

/* Outline + gradient fill */
.text-outline-gradient {
  font-size: 80px;
  font-weight: 900;
  background: linear-gradient(180deg, #fff 0%, #aaa 100%);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
  -webkit-text-stroke: 1px rgba(255, 255, 255, 0.3);
}
```

## Notes for Playwright Rendering

- All CSS text effects render perfectly in Chromium screenshots
- `text-shadow` with many layers is computed statically — no performance concern for screenshots
- `-webkit-text-fill-color: transparent` is required for `background-clip: text` to work
- `data-text` attribute must match the element's text content for pseudo-element effects
- SVG text (for dashed stroke) renders with full fidelity
