# Mix-Blend-Mode Compositions — Complete Reference Catalog

Each recipe includes complete HTML structure and CSS for multi-layer blend compositions. These are designed for static rendering via Playwright screenshot.

---

## 1. Duotone Effect

Converts any image to a two-tone color scheme using overlay + multiply blending.

```html
<div class="duotone-container">
  <img src="photo.jpg" class="duotone-image" alt="" />
  <div class="duotone-overlay"></div>
</div>
```

```css
.duotone-container {
  position: relative;
  width: 100%;
  height: 100%;
  overflow: hidden;
  background: #1a0533; /* Dark tone — shadows become this color */
}

.duotone-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  filter: grayscale(100%) contrast(1.2);
  mix-blend-mode: multiply;
}

.duotone-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, #ff6b6b, #ffd93d); /* Light tone — highlights become this */
  mix-blend-mode: screen;
}
```

### Common Duotone Color Pairs
| Style | Background (shadows) | Overlay gradient (highlights) |
|-------|---------------------|------------------------------|
| Midnight Blue | `#0a1628` | `#4facfe → #00f2fe` |
| Warm Sunset | `#2d1b00` | `#ff9a56 → #ff6b6b` |
| Royal Purple | `#1a0533` | `#a855f7 → #ec4899` |
| Forest | `#0a1a0a` | `#34d399 → #a3e635` |
| Vintage Sepia | `#1a1200` | `#d4a574 → #f5deb3` |

---

## 2. Light Leak

Simulates analog film light leak using screen blend mode.

```html
<div class="light-leak-container">
  <img src="photo.jpg" class="light-leak-base" alt="" />
  <div class="light-leak-effect"></div>
</div>
```

```css
.light-leak-container {
  position: relative;
  width: 100%;
  height: 100%;
  overflow: hidden;
}

.light-leak-base {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.light-leak-effect {
  position: absolute;
  inset: 0;
  background:
    radial-gradient(ellipse at 10% 50%, rgba(255, 120, 50, 0.6) 0%, transparent 50%),
    radial-gradient(ellipse at 90% 30%, rgba(255, 200, 50, 0.4) 0%, transparent 40%),
    radial-gradient(ellipse at 50% 90%, rgba(255, 80, 120, 0.3) 0%, transparent 45%);
  mix-blend-mode: screen;
}
```

### Light Leak Variations
```css
/* Top corner leak */
.light-leak-corner {
  background:
    radial-gradient(ellipse at 0% 0%, rgba(255, 180, 80, 0.7) 0%, transparent 50%),
    radial-gradient(ellipse at 5% 10%, rgba(255, 100, 50, 0.4) 0%, transparent 40%);
  mix-blend-mode: screen;
}

/* Full warm wash */
.light-leak-wash {
  background: linear-gradient(
    120deg,
    rgba(255, 120, 50, 0.5) 0%,
    rgba(255, 200, 100, 0.2) 40%,
    transparent 70%
  );
  mix-blend-mode: screen;
}

/* Cool light leak (anamorphic lens feel) */
.light-leak-cool {
  background:
    radial-gradient(ellipse at 20% 50%, rgba(100, 200, 255, 0.4) 0%, transparent 40%),
    radial-gradient(ellipse at 80% 50%, rgba(150, 100, 255, 0.3) 0%, transparent 40%);
  mix-blend-mode: screen;
}
```

---

## 3. Neon Glow

Color-dodge on dark backgrounds creates intense neon-like illumination.

```html
<div class="neon-glow-container">
  <div class="neon-base"></div>
  <div class="neon-shapes"></div>
</div>
```

```css
.neon-glow-container {
  position: relative;
  width: 100%;
  height: 100%;
  background: #0a0a0a;
  overflow: hidden;
}

.neon-base {
  position: absolute;
  inset: 0;
  background:
    radial-gradient(circle at 30% 50%, rgba(20, 20, 40, 1) 0%, transparent 50%),
    radial-gradient(circle at 70% 50%, rgba(20, 10, 30, 1) 0%, transparent 50%);
}

.neon-shapes {
  position: absolute;
  inset: 0;
  background:
    radial-gradient(circle at 30% 50%, rgba(0, 200, 255, 0.3) 0%, transparent 25%),
    radial-gradient(circle at 70% 50%, rgba(255, 0, 128, 0.3) 0%, transparent 25%),
    radial-gradient(circle at 50% 30%, rgba(128, 0, 255, 0.2) 0%, transparent 20%);
  mix-blend-mode: color-dodge;
}
```

### Neon Text Glow
```css
.neon-text-container {
  position: relative;
  background: #0a0a0a;
}
.neon-text-container::after {
  content: '';
  position: absolute;
  inset: 0;
  background: radial-gradient(
    ellipse at 50% 50%,
    rgba(0, 255, 200, 0.15) 0%,
    transparent 60%
  );
  mix-blend-mode: color-dodge;
  pointer-events: none;
}
```

---

## 4. Vintage Film

Soft-light warm toning that simulates aged film color grading.

```html
<div class="vintage-container">
  <img src="photo.jpg" class="vintage-base" alt="" />
  <div class="vintage-tone"></div>
  <div class="vintage-vignette"></div>
</div>
```

```css
.vintage-container {
  position: relative;
  width: 100%;
  height: 100%;
  overflow: hidden;
}

.vintage-base {
  width: 100%;
  height: 100%;
  object-fit: cover;
  filter: contrast(0.95) saturate(0.8) brightness(1.05);
}

.vintage-tone {
  position: absolute;
  inset: 0;
  background: linear-gradient(
    180deg,
    rgba(255, 200, 150, 0.3) 0%,
    rgba(200, 150, 100, 0.2) 50%,
    rgba(100, 80, 60, 0.3) 100%
  );
  mix-blend-mode: soft-light;
}

.vintage-vignette {
  position: absolute;
  inset: 0;
  background: radial-gradient(
    ellipse at 50% 50%,
    transparent 40%,
    rgba(0, 0, 0, 0.5) 100%
  );
  mix-blend-mode: multiply;
}
```

### Vintage Film Variants
```css
/* 70s warm */
.vintage-70s {
  background: rgba(180, 120, 60, 0.2);
  mix-blend-mode: soft-light;
}

/* Faded Polaroid */
.vintage-polaroid {
  background: linear-gradient(180deg, rgba(255, 240, 200, 0.3) 0%, rgba(200, 180, 160, 0.2) 100%);
  mix-blend-mode: soft-light;
}

/* Cross-processed */
.vintage-cross {
  background: linear-gradient(180deg, rgba(0, 100, 100, 0.2) 0%, rgba(150, 0, 100, 0.15) 100%);
  mix-blend-mode: soft-light;
}
```

---

## 5. Psychedelic

Difference mode creates wild color inversions, especially effective with gradients.

```html
<div class="psychedelic-container">
  <div class="psychedelic-base"></div>
  <div class="psychedelic-layer-1"></div>
  <div class="psychedelic-layer-2"></div>
</div>
```

```css
.psychedelic-container {
  position: relative;
  width: 100%;
  height: 100%;
  overflow: hidden;
}

.psychedelic-base {
  position: absolute;
  inset: 0;
  background: linear-gradient(45deg, #ff0080, #7928ca, #0070f3, #00d4aa);
}

.psychedelic-layer-1 {
  position: absolute;
  inset: 0;
  background: radial-gradient(
    circle at 30% 40%,
    #ff4500 0%,
    #ff8c00 30%,
    #1e90ff 60%,
    #00ff7f 100%
  );
  mix-blend-mode: difference;
}

.psychedelic-layer-2 {
  position: absolute;
  inset: 0;
  background: radial-gradient(
    circle at 70% 60%,
    #ff1493 0%,
    #00bfff 40%,
    #adff2f 80%
  );
  mix-blend-mode: difference;
  opacity: 0.7;
}
```

---

## 6. Double Exposure

Combines two images (or image + gradient) using multiply and screen to simulate analog double exposure.

```html
<div class="double-exposure">
  <img src="portrait.jpg" class="exposure-layer-1" alt="" />
  <img src="landscape.jpg" class="exposure-layer-2" alt="" />
</div>
```

```css
.double-exposure {
  position: relative;
  width: 100%;
  height: 100%;
  background: #111;
  overflow: hidden;
}

.exposure-layer-1 {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  filter: contrast(1.2);
}

.exposure-layer-2 {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  mix-blend-mode: screen;
  opacity: 0.85;
}
```

### Double Exposure with Gradient (no second image needed)
```css
.double-exposure-gradient {
  position: relative;
  width: 100%;
  height: 100%;
  overflow: hidden;
}

.double-exposure-gradient img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  filter: grayscale(60%) contrast(1.3);
}

.double-exposure-gradient::after {
  content: '';
  position: absolute;
  inset: 0;
  background:
    radial-gradient(ellipse at 30% 50%, rgba(0, 150, 100, 0.8) 0%, transparent 50%),
    radial-gradient(ellipse at 70% 50%, rgba(100, 0, 150, 0.6) 0%, transparent 50%),
    linear-gradient(135deg, rgba(255, 100, 50, 0.3) 0%, rgba(0, 100, 200, 0.3) 100%);
  mix-blend-mode: multiply;
}
```

---

## 7. Color Grading (Luminosity Isolation)

Separates luminosity from color for cinematic color grading control.

```html
<div class="color-graded">
  <img src="photo.jpg" class="graded-base" alt="" />
  <div class="grade-shadows"></div>
  <div class="grade-highlights"></div>
</div>
```

```css
.color-graded {
  position: relative;
  width: 100%;
  height: 100%;
  overflow: hidden;
}

.graded-base {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

/* Tint the shadows (dark areas) with teal */
.grade-shadows {
  position: absolute;
  inset: 0;
  background: linear-gradient(
    180deg,
    transparent 0%,
    rgba(0, 80, 100, 0.3) 100%
  );
  mix-blend-mode: color;
}

/* Tint the highlights (bright areas) with warm orange */
.grade-highlights {
  position: absolute;
  inset: 0;
  background: radial-gradient(
    ellipse at 50% 30%,
    rgba(255, 180, 100, 0.25) 0%,
    transparent 60%
  );
  mix-blend-mode: luminosity;
}
```

### Cinematic Teal & Orange Grade
```css
.teal-orange-grade {
  position: absolute;
  inset: 0;
  background: linear-gradient(
    180deg,
    rgba(255, 140, 50, 0.15) 0%,
    rgba(0, 100, 120, 0.2) 100%
  );
  mix-blend-mode: color;
}
```

### Cool Moonlight Grade
```css
.moonlight-grade {
  position: absolute;
  inset: 0;
  background: rgba(80, 120, 200, 0.15);
  mix-blend-mode: color;
}
```

---

## 8. Knockout Mask

Using exclusion mode to create text or shape cutouts that reveal the background pattern.

```html
<div class="knockout-container">
  <div class="knockout-bg"></div>
  <div class="knockout-mask">
    <h1>BOLD</h1>
  </div>
</div>
```

```css
.knockout-container {
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

.knockout-mask {
  position: absolute;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #ffffff;
  mix-blend-mode: exclusion;
}

.knockout-mask h1 {
  font-size: 15vw;
  font-weight: 900;
  color: #ffffff;
  margin: 0;
  text-transform: uppercase;
  letter-spacing: -0.02em;
}
```

### Knockout with Pattern Reveal
```css
.knockout-pattern {
  position: absolute;
  inset: 0;
  background:
    repeating-linear-gradient(45deg, #000 0px, #000 2px, transparent 2px, transparent 10px),
    repeating-linear-gradient(-45deg, #000 0px, #000 2px, transparent 2px, transparent 10px);
  mix-blend-mode: exclusion;
}
```

---

## Blend Mode Quick Reference

| Mode | Effect | Best For |
|------|--------|----------|
| `multiply` | Darkens, whites disappear | Duotone shadows, texture overlay |
| `screen` | Lightens, blacks disappear | Light leaks, glow effects |
| `overlay` | Contrast boost, preserves black/white | General tinting, texture |
| `soft-light` | Subtle contrast, gentle tinting | Film toning, color grading |
| `hard-light` | Strong contrast | Dramatic effects |
| `color-dodge` | Extreme lightening | Neon glow on dark backgrounds |
| `color-burn` | Extreme darkening | Deep shadow effects |
| `difference` | Color inversion | Psychedelic, artistic |
| `exclusion` | Softer difference | Knockout masks |
| `luminosity` | Applies luminance only | Color grading isolation |
| `color` | Applies hue+saturation only | Recoloring |
| `hue` | Applies hue only | Subtle hue shift |
| `saturation` | Applies saturation only | Desaturation effects |

---

## Tips

- **Layer order matters**: blend modes affect how an element blends with everything beneath it
- **Opacity stacking**: combine `mix-blend-mode` with `opacity` for intensity control
- **Black and white behavior**: multiply makes white transparent, screen makes black transparent
- **Playwright rendering**: all blend modes render correctly in Chromium-based screenshots
- **Performance**: blend modes are GPU-accelerated; stacking 5-6 layers is fine
