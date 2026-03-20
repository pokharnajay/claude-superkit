# Backdrop Filter Recipes — Complete Reference Catalog

Each effect is a complete CSS block for a glass-style overlay panel. Apply these to elements positioned over images, gradients, or other visual content.

---

## 1. Frosted Glass

The classic frosted glass panel. Clean, modern, high readability.

```css
.frosted-glass {
  background: rgba(255, 255, 255, 0.15);
  -webkit-backdrop-filter: blur(20px) saturate(180%);
  backdrop-filter: blur(20px) saturate(180%);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 16px;
}
```

### Dark Frosted Variant
```css
.frosted-glass-dark {
  background: rgba(0, 0, 0, 0.2);
  -webkit-backdrop-filter: blur(20px) saturate(180%);
  backdrop-filter: blur(20px) saturate(180%);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 16px;
}
```

### Heavily Frosted (more opaque)
```css
.frosted-glass-heavy {
  background: rgba(255, 255, 255, 0.3);
  -webkit-backdrop-filter: blur(40px) saturate(200%);
  backdrop-filter: blur(40px) saturate(200%);
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: 16px;
}
```

---

## 2. Tinted Glass

Colored frosted glass — great for brand-tinted overlays.

### Warm Tint (amber/gold)
```css
.tinted-glass-warm {
  background: rgba(255, 180, 100, 0.15);
  -webkit-backdrop-filter: blur(16px) saturate(150%);
  backdrop-filter: blur(16px) saturate(150%);
  border: 1px solid rgba(255, 200, 130, 0.2);
  border-radius: 16px;
}
```

### Cool Tint (blue)
```css
.tinted-glass-cool {
  background: rgba(100, 150, 255, 0.15);
  -webkit-backdrop-filter: blur(16px) saturate(150%);
  backdrop-filter: blur(16px) saturate(150%);
  border: 1px solid rgba(130, 170, 255, 0.2);
  border-radius: 16px;
}
```

### Rose Tint
```css
.tinted-glass-rose {
  background: rgba(255, 100, 130, 0.12);
  -webkit-backdrop-filter: blur(16px) saturate(140%);
  backdrop-filter: blur(16px) saturate(140%);
  border: 1px solid rgba(255, 130, 150, 0.2);
  border-radius: 16px;
}
```

### Green Tint
```css
.tinted-glass-green {
  background: rgba(80, 200, 120, 0.12);
  -webkit-backdrop-filter: blur(16px) saturate(140%);
  backdrop-filter: blur(16px) saturate(140%);
  border: 1px solid rgba(100, 220, 140, 0.2);
  border-radius: 16px;
}
```

---

## 3. Iced Glass

Heavy blur with desaturation — creates a muted, frozen look.

```css
.iced-glass {
  background: rgba(200, 220, 240, 0.1);
  -webkit-backdrop-filter: blur(40px) saturate(50%) brightness(1.1);
  backdrop-filter: blur(40px) saturate(50%) brightness(1.1);
  border: 1px solid rgba(255, 255, 255, 0.15);
  border-radius: 16px;
}
```

### Deep Ice (even more desaturated)
```css
.iced-glass-deep {
  background: rgba(180, 200, 230, 0.08);
  -webkit-backdrop-filter: blur(60px) saturate(30%) brightness(1.05);
  backdrop-filter: blur(60px) saturate(30%) brightness(1.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 20px;
}
```

---

## 4. Holographic Glass

Color-shifting blur using hue-rotate — surreal, iridescent feel.

```css
.holographic-glass {
  background: rgba(255, 255, 255, 0.1);
  -webkit-backdrop-filter: blur(16px) saturate(200%) hue-rotate(15deg);
  backdrop-filter: blur(16px) saturate(200%) hue-rotate(15deg);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 16px;
}
```

### Strong Holo Shift
```css
.holographic-glass-strong {
  background: rgba(255, 255, 255, 0.08);
  -webkit-backdrop-filter: blur(20px) saturate(250%) hue-rotate(30deg) brightness(1.1);
  backdrop-filter: blur(20px) saturate(250%) hue-rotate(30deg) brightness(1.1);
  border: 1px solid rgba(255, 255, 255, 0.15);
  border-radius: 16px;
}
```

### Rainbow Holo (multiple pseudo-element layers)
```css
.rainbow-holo {
  position: relative;
  background: rgba(255, 255, 255, 0.05);
  -webkit-backdrop-filter: blur(20px);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.15);
  border-radius: 16px;
  overflow: hidden;
}
.rainbow-holo::before {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(
    135deg,
    rgba(255, 0, 128, 0.1) 0%,
    rgba(0, 255, 255, 0.1) 33%,
    rgba(128, 0, 255, 0.1) 66%,
    rgba(255, 255, 0, 0.1) 100%
  );
  pointer-events: none;
}
```

---

## 5. Smoke Glass

Darkened blur — moody, cinematic. Background content is dimmed.

```css
.smoke-glass {
  background: rgba(0, 0, 0, 0.25);
  -webkit-backdrop-filter: blur(24px) brightness(0.7) saturate(120%);
  backdrop-filter: blur(24px) brightness(0.7) saturate(120%);
  border: 1px solid rgba(255, 255, 255, 0.06);
  border-radius: 16px;
}
```

### Light Smoke
```css
.smoke-glass-light {
  background: rgba(0, 0, 0, 0.15);
  -webkit-backdrop-filter: blur(16px) brightness(0.8) saturate(110%);
  backdrop-filter: blur(16px) brightness(0.8) saturate(110%);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 16px;
}
```

### Heavy Smoke (very dark)
```css
.smoke-glass-heavy {
  background: rgba(0, 0, 0, 0.4);
  -webkit-backdrop-filter: blur(30px) brightness(0.5) saturate(80%);
  backdrop-filter: blur(30px) brightness(0.5) saturate(80%);
  border: 1px solid rgba(255, 255, 255, 0.04);
  border-radius: 16px;
}
```

---

## 6. Crystal Glass

Hyper-vivid — increases saturation and contrast of what's behind, with minimal blur. Makes backgrounds pop.

```css
.crystal-glass {
  background: rgba(255, 255, 255, 0.05);
  -webkit-backdrop-filter: saturate(200%) contrast(1.1) blur(1px);
  backdrop-filter: saturate(200%) contrast(1.1) blur(1px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 16px;
}
```

### Crystal with Light Blur
```css
.crystal-glass-soft {
  background: rgba(255, 255, 255, 0.08);
  -webkit-backdrop-filter: saturate(180%) contrast(1.05) blur(4px);
  backdrop-filter: saturate(180%) contrast(1.05) blur(4px);
  border: 1px solid rgba(255, 255, 255, 0.15);
  border-radius: 16px;
}
```

### Crystal Dark
```css
.crystal-glass-dark {
  background: rgba(0, 0, 0, 0.1);
  -webkit-backdrop-filter: saturate(220%) contrast(1.15) blur(1px) brightness(0.9);
  backdrop-filter: saturate(220%) contrast(1.15) blur(1px) brightness(0.9);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 16px;
}
```

---

## Complete Glass Card Template

A production-ready glass card combining backdrop-filter with proper layering:

```css
.glass-card {
  position: relative;
  padding: 32px;
  background: rgba(255, 255, 255, 0.1);
  -webkit-backdrop-filter: blur(20px) saturate(180%);
  backdrop-filter: blur(20px) saturate(180%);
  border: 1px solid rgba(255, 255, 255, 0.18);
  border-radius: 16px;
  box-shadow:
    0 8px 32px rgba(0, 0, 0, 0.12),
    inset 0 1px 0 rgba(255, 255, 255, 0.15);
}
```

### Glass Card with Top Highlight
```css
.glass-card-highlight {
  position: relative;
  padding: 32px;
  background: rgba(255, 255, 255, 0.08);
  -webkit-backdrop-filter: blur(24px) saturate(180%);
  backdrop-filter: blur(24px) saturate(180%);
  border: 1px solid rgba(255, 255, 255, 0.12);
  border-radius: 16px;
  box-shadow:
    0 8px 32px rgba(0, 0, 0, 0.15),
    inset 0 1px 0 rgba(255, 255, 255, 0.2),
    inset 0 -1px 0 rgba(255, 255, 255, 0.05);
  overflow: hidden;
}
.glass-card-highlight::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 1px;
  background: linear-gradient(
    90deg,
    transparent 0%,
    rgba(255, 255, 255, 0.4) 50%,
    transparent 100%
  );
}
```

---

## Important Notes

### Webkit Prefix Required
Always include both `-webkit-backdrop-filter` and `backdrop-filter`. Safari requires the prefix.

### Stacking Context
`backdrop-filter` creates a new stacking context. The element must have some transparency in its `background` for the filter to be visible.

### Rendering in Playwright
Backdrop filters render correctly in Playwright/Chromium. No special configuration needed. They are computed at screenshot time.

### Performance
- `blur()` is the most expensive operation — keep under 40px for complex layouts
- Combining multiple filter functions is fine (they chain efficiently)
- Avoid applying backdrop-filter to more than 5-6 overlapping elements

### Filter Function Order
The order of filter functions matters. They apply left to right:
```css
/* First blurs, then saturates the blurred result */
backdrop-filter: blur(20px) saturate(180%);

/* First saturates, then blurs — different result */
backdrop-filter: saturate(180%) blur(20px);
```
