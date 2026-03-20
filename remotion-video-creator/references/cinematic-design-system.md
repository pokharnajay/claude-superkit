# Cinematic Design System — Professional Video Quality Standard

> This is the quality bar. Every video must meet this standard.

---

## Core Philosophy

**"Nocturnal Signal"** — dark field as foundation, ember accent as direction, typographic architecture as structure.

Videos are NOT slideshows with motion. They are **cinematic experiences** with layered depth, organic motion, and emotional pacing.

---

## Design Tokens

```tsx
// theme.ts — Use this as the foundation for every video project
export const C = {
  bg: "#08080D",           // Near-black, not pure black
  bgCard: "rgba(255,255,255,0.04)",
  bgCardBorder: "rgba(255,255,255,0.08)",
  fg: "#F5F0EB",           // Warm off-white, not pure white
  fgMuted: "#7A756F",      // Secondary text
  fgDim: "#4A4540",        // Labels, metadata
  accent: "#C4703F",       // Ember/copper — primary accent
  accentGlow: "rgba(196,112,63,0.35)",
  accentBright: "#E8934F",
  teal: "#3FC4C4",         // Tech/voice
  green: "#4FC47B",        // Success/growth
  purple: "#9B6DD7",       // Creative/design
  red: "#E74C3C",          // Error/emphasis
  blue: "#5B9BD5",         // Code/trust
};

export const FONT = {
  serif: "Playfair Display",    // Headlines — elegant, weighty
  sans: "Source Sans 3",        // Body — open, legible
  mono: "JetBrains Mono",      // Code, labels, metadata
};
```

---

## Background System — MUST VARY PER SCENE

The background is a **4-layer composition**. Each layer has parameters that MUST change per scene to avoid repetition:

### Layer 1: Base Gradient
```
radial-gradient(ellipse at 50% 40%, #12121A 0%, #08080D 70%)
```

### Layer 2: Animated Grid
| Parameter | Range | Varies By |
|-----------|-------|-----------|
| opacity | 0.02–0.05 | Scene energy (low = mystery, high = tech) |
| cellSize | 40–100px | Scene density (tight = data, open = emotional) |
| angle | 0°, 15°, 30°, 45° | Scene uniqueness |
| scrollSpeed | 0.1–0.5px/frame | Scene energy |

### Layer 3: Gradient Orbs
| Parameter | Range | Varies By |
|-----------|-------|-----------|
| count | 2–4 | Scene complexity |
| color | Per-scene accent | Scene topic (copper, teal, purple, etc.) |
| size | 300–700px | Scene prominence |
| blur | 120–280px | Subtlety level |
| opacity | 0.08–0.20 | Scene energy |
| drift | noise2D driven | Always organic, never linear |

### Layer 4: Particle Field
| Parameter | Range | Varies By |
|-----------|-------|-----------|
| count | 20–60 | Scene density (sparse = quiet, dense = energy) |
| size | 1–3.5px | Mix of sizes within scene |
| opacity | 0.06–0.24 | Depth variation |
| drift | noise2D driven | Always organic |
| speed | 0.5–2.0 units/s | Scene energy |

### Layer 5: Vignette
| Parameter | Range | Varies By |
|-----------|-------|-----------|
| intensity | 0.3–0.6 | Scene focus (higher = more focused) |

### Per-Scene Accent Colors (emotional storytelling)
| Scene Mood | Accent Color | Example |
|-----------|-------------|---------|
| Mystery/intrigue | Copper #C4703F | Cold opens |
| Code/building | Blue #5B9BD5 | Dev scenes |
| Growth/momentum | Green #4FC47B | Progress/stats |
| Creativity/design | Purple #9B6DD7 | Design scenes |
| Voice/tech | Teal #3FC4C4 | Audio/AI scenes |
| Triumph/pride | Copper #C4703F | Reveals |
| Error/danger | Red #E74C3C | Problem statements |

---

## Component Hierarchy

Every video should use these components (templates/components/):

### Tier 1 — Always Use
- **CinematicBg** — layered background (grid + orbs + particles + vignette)
- **KineticText** — word-by-word spring reveals with emphasis coloring
- **AccentLine** — animated horizontal accent (scene breaks, emphasis)

### Tier 2 — Use When Applicable
- **GlassCard** — glassmorphism containers for grouped content
- **StatCounter** — animated counting numbers for data/metrics
- **CodeEditor** — code mockup with typing animation

### Tier 3 — Specialized
- **WaveformBars** — noise-driven audio waveform
- **ParticleSystem** — scene-specific particle effects
- **IconElement** — inline SVG icons

---

## Animation Standards

### Spring Physics (preferred over linear interpolation)
```tsx
// Standard entrance spring
spring({ frame, fps, config: { damping: 14, stiffness: 120, mass: 0.8 } })

// Heavy/dramatic entrance
spring({ frame, fps, config: { damping: 12, stiffness: 80, mass: 1.2 } })

// Snappy/UI feel
spring({ frame, fps, config: { damping: 18, stiffness: 200, mass: 0.5 } })
```

### Stagger Pattern
Elements in groups (cards, stats, list items) MUST stagger:
- 3–5 frame stagger for words in text
- 8–12 frame stagger for cards in a list
- 5–8 frame stagger for stats in a row

### Entrance → Hold → Exit
Every scene follows this rhythm:
- **Entrance** (first 25%): Elements animate in with springs
- **Hold** (middle 50%): Content is visible and readable
- **Exit** (last 25%): Opacity fades or elements drift out (handled by TransitionSeries)

---

## Typography Rules

| Element | Font | Size | Weight | Color |
|---------|------|------|--------|-------|
| Headline | Playfair Display | 52–72px | 700–900 | #F5F0EB |
| Subhead | Playfair Display | 36–48px | 700 | #F5F0EB |
| Body | Source Sans 3 | 24–30px | 400 | #7A756F |
| Label | JetBrains Mono | 13–18px | 400 | #4A4540 |
| Stat number | JetBrains Mono | 56–72px | 800 | accent color |
| Code | JetBrains Mono | 16–20px | 400 | varies |

### Labels are uppercase + letterspaced
```tsx
{
  fontFamily: "JetBrains Mono",
  fontSize: 13,
  color: "#4A4540",
  letterSpacing: 3,
  textTransform: "uppercase",
}
```

---

## What Makes a Video Professional vs Amateur

| Amateur | Professional |
|---------|-------------|
| Static image slides with motion | 100% code-generated graphics |
| Same background every scene | Per-scene accent colors and varied backgrounds |
| Text appears instantly | Word-by-word spring animation with emphasis |
| Flat colored rectangles | Glassmorphism with blur, glow, subtle borders |
| No ambient elements | Particles, orbs, grid — layered depth |
| Same animation speed everywhere | Spring physics with mass/damping variety |
| Generic flat design | Cinematic dark field with warm accent |
| Everything animates at once | Staggered entrances with reading order |

---

## NEVER Do

1. Never use static PNG/JPG images as the primary visual content
2. Never use the same particle count/grid/orb config across all scenes
3. Never use pure black (#000) or pure white (#fff)
4. Never use CSS transitions or Tailwind animate classes
5. Never have text appear without animation
6. Never use more than 3 font families
7. Never skip the background system (grid + orbs + particles + vignette)
8. Never use linear easing for entrances (always spring or ease-out)
