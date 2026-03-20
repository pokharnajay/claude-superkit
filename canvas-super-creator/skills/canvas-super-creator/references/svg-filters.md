# SVG Filter Effects — Complete Reference Catalog

Use these inline SVG filter definitions in your HTML. Place the `<svg>` block in the document (it can be hidden with `width="0" height="0"`) and apply filters via CSS.

---

## 1. Paper Texture

Simulates rough paper grain. Great for backgrounds behind text or illustrations.

```html
<svg width="0" height="0">
  <defs>
    <filter id="paper-texture" x="0%" y="0%" width="100%" height="100%">
      <feTurbulence type="fractalNoise" baseFrequency="0.04" numOctaves="5" stitchTiles="stitch" result="noise" />
      <feDiffuseLighting in="noise" lighting-color="#fff" surfaceScale="2" result="lit">
        <feDistantLight azimuth="45" elevation="60" />
      </feDiffuseLighting>
      <feComposite in="SourceGraphic" in2="lit" operator="arithmetic" k1="1" k2="0" k3="0" k4="0" />
    </filter>
  </defs>
</svg>
```

```css
.paper {
  filter: url(#paper-texture);
}
```

### Variant: Subtle paper overlay (preserves color)

```html
<svg width="0" height="0">
  <defs>
    <filter id="paper-overlay" x="0%" y="0%" width="100%" height="100%">
      <feTurbulence type="fractalNoise" baseFrequency="0.04" numOctaves="5" stitchTiles="stitch" result="noise" />
      <feDiffuseLighting in="noise" lighting-color="#ffffff" surfaceScale="1.5" result="lit">
        <feDistantLight azimuth="45" elevation="55" />
      </feDiffuseLighting>
      <feBlend in="SourceGraphic" in2="lit" mode="multiply" />
    </filter>
  </defs>
</svg>
```

---

## 2. Film Grain

Adds photographic noise. The feColorMatrix boosts contrast to make the grain sharp.

```html
<svg width="0" height="0">
  <defs>
    <filter id="film-grain" x="0%" y="0%" width="100%" height="100%">
      <feTurbulence type="fractalNoise" baseFrequency="0.65" numOctaves="3" stitchTiles="stitch" result="noise" />
      <feColorMatrix in="noise" type="saturate" values="0" result="mono-noise" />
      <feColorMatrix in="mono-noise" type="matrix"
        values="1 0 0 0 -0.4
                0 1 0 0 -0.4
                0 0 1 0 -0.4
                0 0 0 1 0" result="contrast-noise" />
      <feBlend in="SourceGraphic" in2="contrast-noise" mode="overlay" />
    </filter>
  </defs>
</svg>
```

```css
.film-grain {
  filter: url(#film-grain);
}
```

### Tuning parameters
- `baseFrequency="0.65"` — higher = finer grain (0.3 coarse, 0.8 fine)
- The `-0.4` offset in feColorMatrix controls contrast intensity
- Change `mode="overlay"` to `mode="soft-light"` for subtler effect

---

## 3. Watercolor Bleed

Distorts edges to simulate watercolor paint bleeding into paper.

```html
<svg width="0" height="0">
  <defs>
    <filter id="watercolor-bleed" x="-5%" y="-5%" width="110%" height="110%">
      <feTurbulence type="fractalNoise" baseFrequency="0.03" numOctaves="4" seed="2" stitchTiles="stitch" result="warp" />
      <feDisplacementMap in="SourceGraphic" in2="warp" scale="30" xChannelSelector="R" yChannelSelector="G" result="displaced" />
      <feGaussianBlur in="displaced" stdDeviation="1.5" result="softened" />
      <feComposite in="softened" in2="SourceGraphic" operator="atop" />
    </filter>
  </defs>
</svg>
```

```css
.watercolor {
  filter: url(#watercolor-bleed);
}
```

### Tuning
- `scale="30"` — distortion intensity (10 subtle, 50 extreme)
- `baseFrequency="0.03"` — lower = larger bleed shapes
- `seed="2"` — change for different random patterns

---

## 4. Glass Distortion

Creates a glass/liquid refraction effect.

```html
<svg width="0" height="0">
  <defs>
    <filter id="glass-distortion" x="-2%" y="-2%" width="104%" height="104%">
      <feTurbulence type="turbulence" baseFrequency="0.015" numOctaves="3" seed="5" stitchTiles="stitch" result="ripple" />
      <feDisplacementMap in="SourceGraphic" in2="ripple" scale="15" xChannelSelector="R" yChannelSelector="G" />
    </filter>
  </defs>
</svg>
```

```css
.glass {
  filter: url(#glass-distortion);
}
```

### Frosted Glass Variant

```html
<svg width="0" height="0">
  <defs>
    <filter id="frosted-glass" x="-2%" y="-2%" width="104%" height="104%">
      <feTurbulence type="turbulence" baseFrequency="0.04" numOctaves="3" result="ripple" />
      <feDisplacementMap in="SourceGraphic" in2="ripple" scale="8" xChannelSelector="R" yChannelSelector="G" result="displaced" />
      <feGaussianBlur in="displaced" stdDeviation="2" />
    </filter>
  </defs>
</svg>
```

---

## 5. Wood Grain

Elongated turbulence simulating wood grain lines.

```html
<svg width="0" height="0">
  <defs>
    <filter id="wood-grain" x="0%" y="0%" width="100%" height="100%" color-interpolation-filters="sRGB">
      <feTurbulence type="turbulence" baseFrequency="0.02 0.2" numOctaves="4" seed="3" stitchTiles="stitch" result="grain" />
      <feColorMatrix in="grain" type="saturate" values="0" result="mono" />
      <feColorMatrix in="mono" type="matrix"
        values="0.6 0 0 0 0.3
                0.4 0 0 0 0.15
                0.2 0 0 0 0.05
                0 0 0 1 0" result="wood-color" />
      <feBlend in="SourceGraphic" in2="wood-color" mode="multiply" />
    </filter>
  </defs>
</svg>
```

```css
.wood {
  filter: url(#wood-grain);
}
```

### Tuning
- `baseFrequency="0.02 0.2"` — first value = horizontal frequency, second = vertical. Higher second value = tighter grain lines
- Adjust the color matrix RGB values to change wood tone (lighter pine vs darker walnut)

---

## 6. Marble Texture

Veined stone texture using turbulence.

```html
<svg width="0" height="0">
  <defs>
    <filter id="marble-texture" x="0%" y="0%" width="100%" height="100%" color-interpolation-filters="sRGB">
      <feTurbulence type="turbulence" baseFrequency="0.05" numOctaves="3" seed="10" stitchTiles="stitch" result="veins" />
      <feColorMatrix in="veins" type="saturate" values="0" result="bw" />
      <feComponentTransfer in="bw" result="contrast">
        <feFuncR type="linear" slope="3" intercept="-0.8" />
        <feFuncG type="linear" slope="3" intercept="-0.8" />
        <feFuncB type="linear" slope="3" intercept="-0.8" />
      </feComponentTransfer>
      <feColorMatrix in="contrast" type="matrix"
        values="0.9 0 0 0 0.1
                0.85 0 0 0 0.1
                0.8 0 0 0 0.12
                0 0 0 1 0" result="marble-color" />
      <feBlend in="SourceGraphic" in2="marble-color" mode="overlay" />
    </filter>
  </defs>
</svg>
```

```css
.marble {
  filter: url(#marble-texture);
}
```

### Dark Marble Variant

```html
<svg width="0" height="0">
  <defs>
    <filter id="dark-marble" x="0%" y="0%" width="100%" height="100%" color-interpolation-filters="sRGB">
      <feTurbulence type="turbulence" baseFrequency="0.05" numOctaves="3" seed="7" result="veins" />
      <feColorMatrix in="veins" type="saturate" values="0" result="bw" />
      <feComponentTransfer in="bw" result="contrast">
        <feFuncR type="linear" slope="4" intercept="-1.2" />
        <feFuncG type="linear" slope="4" intercept="-1.2" />
        <feFuncB type="linear" slope="4" intercept="-1.2" />
      </feComponentTransfer>
      <feColorMatrix in="contrast" type="matrix"
        values="0.2 0 0 0 0.05
                0.2 0 0 0 0.05
                0.22 0 0 0 0.06
                0 0 0 1 0" result="marble-color" />
      <feBlend in="SourceGraphic" in2="marble-color" mode="screen" />
    </filter>
  </defs>
</svg>
```

---

## 7. Fabric Weave

Simulates woven textile using turbulence combined with a convolution kernel.

```html
<svg width="0" height="0">
  <defs>
    <filter id="fabric-weave" x="0%" y="0%" width="100%" height="100%">
      <feTurbulence type="turbulence" baseFrequency="0.15 0.15" numOctaves="2" seed="1" result="weave-noise" />
      <feConvolveMatrix in="weave-noise" order="3" kernelMatrix="
        1 -1  1
       -1  2 -1
        1 -1  1
      " divisor="2" bias="0.5" result="weave-pattern" />
      <feColorMatrix in="weave-pattern" type="saturate" values="0" result="mono-weave" />
      <feBlend in="SourceGraphic" in2="mono-weave" mode="multiply" />
    </filter>
  </defs>
</svg>
```

```css
.fabric {
  filter: url(#fabric-weave);
}
```

### Linen Variant (finer weave)

```html
<svg width="0" height="0">
  <defs>
    <filter id="linen-weave" x="0%" y="0%" width="100%" height="100%">
      <feTurbulence type="turbulence" baseFrequency="0.3 0.3" numOctaves="2" seed="4" result="noise" />
      <feConvolveMatrix in="noise" order="3" kernelMatrix="
        0 -1  0
       -1  4 -1
        0 -1  0
      " divisor="2" bias="0.5" result="pattern" />
      <feColorMatrix in="pattern" type="saturate" values="0" result="mono" />
      <feBlend in="SourceGraphic" in2="mono" mode="soft-light" />
    </filter>
  </defs>
</svg>
```

---

## 8. Halftone Dots via SVG

Posterizes the image into dot-like halftone via component transfer.

```html
<svg width="0" height="0">
  <defs>
    <filter id="halftone-svg" x="0%" y="0%" width="100%" height="100%">
      <!-- Convert to grayscale -->
      <feColorMatrix type="saturate" values="0" result="gray" />
      <!-- Posterize to few levels -->
      <feComponentTransfer in="gray" result="posterized">
        <feFuncR type="discrete" tableValues="0 0.25 0.5 0.75 1" />
        <feFuncG type="discrete" tableValues="0 0.25 0.5 0.75 1" />
        <feFuncB type="discrete" tableValues="0 0.25 0.5 0.75 1" />
      </feComponentTransfer>
      <!-- Add dot pattern -->
      <feTurbulence type="turbulence" baseFrequency="0.12" numOctaves="1" result="dots" />
      <feColorMatrix in="dots" type="saturate" values="0" result="mono-dots" />
      <feComponentTransfer in="mono-dots" result="sharp-dots">
        <feFuncR type="discrete" tableValues="0 1" />
        <feFuncG type="discrete" tableValues="0 1" />
        <feFuncB type="discrete" tableValues="0 1" />
      </feComponentTransfer>
      <feComposite in="posterized" in2="sharp-dots" operator="arithmetic" k1="1.5" k2="0.3" k3="0" k4="-0.3" />
    </filter>
  </defs>
</svg>
```

```css
.halftone {
  filter: url(#halftone-svg);
}
```

### Color Halftone (preserves hue)

```html
<svg width="0" height="0">
  <defs>
    <filter id="color-halftone" x="0%" y="0%" width="100%" height="100%">
      <feComponentTransfer result="posterized">
        <feFuncR type="discrete" tableValues="0 0.2 0.4 0.6 0.8 1" />
        <feFuncG type="discrete" tableValues="0 0.2 0.4 0.6 0.8 1" />
        <feFuncB type="discrete" tableValues="0 0.2 0.4 0.6 0.8 1" />
      </feComponentTransfer>
      <feGaussianBlur in="posterized" stdDeviation="0.5" />
    </filter>
  </defs>
</svg>
```

---

## Combining Filters

You can chain effects by applying multiple filters or nesting filter primitives:

```css
/* Chain via CSS */
.combined {
  filter: url(#paper-texture) url(#film-grain);
}

/* Or layer via pseudo-elements */
.layered {
  position: relative;
}
.layered::after {
  content: '';
  position: absolute;
  inset: 0;
  filter: url(#film-grain);
  pointer-events: none;
  mix-blend-mode: overlay;
}
```

## Performance Notes

- SVG filters are GPU-accelerated in modern browsers
- `feTurbulence` is the most expensive primitive — keep `numOctaves` at 5 or below
- For Playwright screenshots, SVG filters render perfectly since they are static
- Always include `x`, `y`, `width`, `height` attributes on the filter to prevent clipping
- Use `stitchTiles="stitch"` on feTurbulence to avoid visible seams at tile boundaries
