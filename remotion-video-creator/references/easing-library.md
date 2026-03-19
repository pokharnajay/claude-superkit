# Easing Library — Complete Reference for Remotion

> Every easing function, spring preset, and timing guideline.
> Use this to select the right motion curve for any animation.

---

## interpolate() with Easing — Full Reference

```tsx
import { interpolate, Easing, useCurrentFrame } from 'remotion';

const frame = useCurrentFrame();
```

### Base Easing Curves

```tsx
// Linear — constant speed, mechanical feel. AVOID as default.
interpolate(frame, [0, 30], [0, 1], { easing: Easing.linear });

// Ease — CSS default ease equivalent. Good general purpose.
interpolate(frame, [0, 30], [0, 1], { easing: Easing.ease });

// Quadratic — t^2, moderate acceleration
interpolate(frame, [0, 30], [0, 1], { easing: Easing.quad });

// Cubic — t^3, stronger acceleration
interpolate(frame, [0, 30], [0, 1], { easing: Easing.cubic });

// Polynomial — t^n, custom power
interpolate(frame, [0, 30], [0, 1], { easing: Easing.poly(4) }); // quartic
interpolate(frame, [0, 30], [0, 1], { easing: Easing.poly(5) }); // quintic

// Sinusoidal — sine curve, gentle
interpolate(frame, [0, 30], [0, 1], { easing: Easing.sin });

// Circular — quarter circle, sharp start
interpolate(frame, [0, 30], [0, 1], { easing: Easing.circle });

// Exponential — dramatic acceleration
interpolate(frame, [0, 30], [0, 1], { easing: Easing.exp });

// Elastic — springy overshoot with oscillation
interpolate(frame, [0, 30], [0, 1], { easing: Easing.elastic(1) });   // default bounciness
interpolate(frame, [0, 30], [0, 1], { easing: Easing.elastic(2) });   // more bouncy
interpolate(frame, [0, 30], [0, 1], { easing: Easing.elastic(0.5) }); // less bouncy

// Back — overshoot then settle
interpolate(frame, [0, 30], [0, 1], { easing: Easing.back(1.70158) }); // default overshoot
interpolate(frame, [0, 30], [0, 1], { easing: Easing.back(3) });       // more overshoot
interpolate(frame, [0, 30], [0, 1], { easing: Easing.back(1) });       // subtle overshoot

// Bounce — bouncing ball effect
interpolate(frame, [0, 30], [0, 1], { easing: Easing.bounce });

// Custom Bezier — match any CSS cubic-bezier()
interpolate(frame, [0, 30], [0, 1], { easing: Easing.bezier(0.25, 0.1, 0.25, 1) });   // ease
interpolate(frame, [0, 30], [0, 1], { easing: Easing.bezier(0.42, 0, 0.58, 1) });     // ease-in-out
interpolate(frame, [0, 30], [0, 1], { easing: Easing.bezier(0.22, 1, 0.36, 1) });     // ease-out-expo
interpolate(frame, [0, 30], [0, 1], { easing: Easing.bezier(0.68, -0.55, 0.27, 1.55) }); // back-in-out

// Step functions — instant jumps
interpolate(frame, [0, 30], [0, 1], { easing: Easing.step0 }); // jumps at start of interval
interpolate(frame, [0, 30], [0, 1], { easing: Easing.step1 }); // jumps at end of interval
```

### Modifiers — in(), out(), inOut()

Every base curve above defaults to "ease-in" behavior (accelerating). Use modifiers to change:

```tsx
// Easing.in(curve) — ACCELERATE (slow start, fast end)
// Use for: exit animations, things leaving the screen
interpolate(frame, [0, 30], [0, 1], { easing: Easing.in(Easing.quad) });
interpolate(frame, [0, 30], [0, 1], { easing: Easing.in(Easing.cubic) });
interpolate(frame, [0, 30], [0, 1], { easing: Easing.in(Easing.exp) });

// Easing.out(curve) — DECELERATE (fast start, slow end)
// Use for: enter animations, things arriving on screen
interpolate(frame, [0, 30], [0, 1], { easing: Easing.out(Easing.quad) });
interpolate(frame, [0, 30], [0, 1], { easing: Easing.out(Easing.cubic) });
interpolate(frame, [0, 30], [0, 1], { easing: Easing.out(Easing.exp) });
interpolate(frame, [0, 30], [0, 1], { easing: Easing.out(Easing.elastic(1)) });
interpolate(frame, [0, 30], [0, 1], { easing: Easing.out(Easing.back(1.7)) });
interpolate(frame, [0, 30], [0, 1], { easing: Easing.out(Easing.bounce) });

// Easing.inOut(curve) — ACCELERATE THEN DECELERATE (slow-fast-slow)
// Use for: emphasis, scale pulse, continuous motion, data transitions
interpolate(frame, [0, 30], [0, 1], { easing: Easing.inOut(Easing.quad) });
interpolate(frame, [0, 30], [0, 1], { easing: Easing.inOut(Easing.cubic) });
interpolate(frame, [0, 30], [0, 1], { easing: Easing.inOut(Easing.exp) });
interpolate(frame, [0, 30], [0, 1], { easing: Easing.inOut(Easing.ease) });
```

### extrapolateLeft / extrapolateRight

```tsx
// 'clamp' — holds at boundary value (most common, use by default)
// 'extend' — continues the curve beyond the range (default, can cause issues)
// 'wrap' — wraps around (loops)
// 'identity' — returns the input value itself

interpolate(frame, [0, 30], [0, 100], {
  extrapolateLeft: 'clamp',   // before frame 0 → returns 0
  extrapolateRight: 'clamp',  // after frame 30 → returns 100
  easing: Easing.out(Easing.ease),
});

// ALWAYS use extrapolateLeft/Right: 'clamp' unless you specifically need extension
```

---

## spring() — Complete Reference

```tsx
import { spring, useCurrentFrame, useVideoConfig } from 'remotion';

const frame = useCurrentFrame();
const { fps } = useVideoConfig();

const value = spring({
  frame,                    // current frame (required)
  fps,                      // frames per second (required)
  config: {                 // spring physics config
    damping: 200,           // friction (1-500, higher = less bounce)
    stiffness: 100,         // spring tightness (1-500, higher = faster)
    mass: 1,                // weight (0.1-10, higher = slower/heavier)
    overshootClamping: false, // if true, never exceeds target value
  },
  from: 0,                  // start value (default: 0)
  to: 1,                    // end value (default: 1)
  durationInFrames: 30,     // optional: limit duration
  durationRestThreshold: 0.001, // when spring is "at rest"
  delay: 0,                 // delay before animation starts (frames)
  reverse: false,           // play animation in reverse
});
```

### Spring Presets Table

| Preset Name | damping | stiffness | mass | overshootClamping | Character | Best For |
|------------|---------|-----------|------|-------------------|-----------|----------|
| **Gentle** | 200 | 100 | 1 | false | Smooth, no bounce | Text fade-in, subtle UI elements |
| **Bouncy** | 10 | 100 | 0.5 | false | Playful bounce | Logo reveal, playful elements, notifications |
| **Snappy** | 20 | 200 | 1 | false | Quick with slight overshoot | Button press, UI transitions, tabs |
| **Heavy** | 200 | 20 | 2 | false | Slow, deliberate, weighty | Large background elements, slow reveals |
| **Elastic** | 5 | 80 | 0.3 | false | Very bouncy, attention-grabbing | Sale badges, alerts, emoji reactions |
| **Smooth** | 30 | 120 | 1 | true | Professional, no overshoot | Corporate videos, data viz, charts |
| **Quick** | 15 | 300 | 0.8 | true | Fast snap, no bounce | Small elements, icons, quick transitions |
| **Wobbly** | 8 | 150 | 0.5 | false | Wobbly settle | Character animations, organic motion |
| **Stiff** | 100 | 400 | 1 | true | Very fast, rigid | Urgent elements, fast UI responses |
| **Molasses** | 300 | 10 | 3 | false | Very slow, heavy | Cinematic reveals, dramatic entrances |

### Spring Preset Code
```tsx
// Copy-paste spring configs
const springPresets = {
  gentle:   { damping: 200, stiffness: 100, mass: 1, overshootClamping: false },
  bouncy:   { damping: 10,  stiffness: 100, mass: 0.5, overshootClamping: false },
  snappy:   { damping: 20,  stiffness: 200, mass: 1, overshootClamping: false },
  heavy:    { damping: 200, stiffness: 20,  mass: 2, overshootClamping: false },
  elastic:  { damping: 5,   stiffness: 80,  mass: 0.3, overshootClamping: false },
  smooth:   { damping: 30,  stiffness: 120, mass: 1, overshootClamping: true },
  quick:    { damping: 15,  stiffness: 300, mass: 0.8, overshootClamping: true },
  wobbly:   { damping: 8,   stiffness: 150, mass: 0.5, overshootClamping: false },
  stiff:    { damping: 100, stiffness: 400, mass: 1, overshootClamping: true },
  molasses: { damping: 300, stiffness: 10,  mass: 3, overshootClamping: false },
};

// Usage
const scale = spring({ frame, fps, config: springPresets.bouncy });
```

---

## When to Use What — Decision Guide

### Enter Animations (element appearing on screen)
```
PREFERRED: spring() with gentle/smooth preset
           OR Easing.out(Easing.ease)
           OR Easing.out(Easing.cubic)

WHY: Deceleration feels natural — object "arrives" and settles.

EXAMPLES:
  // Fade + slide up (most common enter animation)
  const opacity = interpolate(frame, [0, 20], [0, 1], {
    extrapolateRight: 'clamp', easing: Easing.out(Easing.ease)
  });
  const y = interpolate(frame, [0, 20], [30, 0], {
    extrapolateRight: 'clamp', easing: Easing.out(Easing.cubic)
  });

  // Spring scale-in
  const scale = spring({ frame, fps, config: { damping: 200, stiffness: 100 } });
```

### Exit Animations (element leaving the screen)
```
PREFERRED: Easing.in(Easing.ease)
           OR Easing.in(Easing.cubic)
           OR Easing.in(Easing.exp) for dramatic exits

WHY: Acceleration feels natural — object "leaves" and gains speed.

EXAMPLES:
  const exitStart = 60;
  const opacity = interpolate(frame, [exitStart, exitStart + 15], [1, 0], {
    extrapolateLeft: 'clamp', extrapolateRight: 'clamp',
    easing: Easing.in(Easing.ease)
  });
  const y = interpolate(frame, [exitStart, exitStart + 15], [0, -30], {
    extrapolateLeft: 'clamp', extrapolateRight: 'clamp',
    easing: Easing.in(Easing.cubic)
  });
```

### Emphasis / Pulse (draw attention to element)
```
PREFERRED: spring() with bouncy/elastic preset
           OR Easing.out(Easing.elastic(1))
           OR Easing.out(Easing.back(1.7))

EXAMPLES:
  // Bounce scale
  const emphasis = spring({ frame: frame - triggerFrame, fps,
    config: { damping: 10, stiffness: 100, mass: 0.5 }
  });
  <div style={{ transform: `scale(${emphasis})` }} />

  // Pulse (scale up and back)
  const pulse = interpolate(frame, [0, 10, 20], [1, 1.15, 1], {
    extrapolateRight: 'clamp',
    easing: Easing.inOut(Easing.ease)
  });
```

### Continuous / Looping Motion
```
PREFERRED: Easing.inOut(Easing.ease) or Easing.inOut(Easing.sin)

EXAMPLES:
  // Floating hover effect
  const floatY = interpolate(
    frame % 60, [0, 30, 60], [0, -10, 0],
    { easing: Easing.inOut(Easing.sin) }
  );

  // Breathing scale
  const breathe = interpolate(
    frame % 90, [0, 45, 90], [1, 1.03, 1],
    { easing: Easing.inOut(Easing.ease) }
  );
```

### Data / Chart Transitions
```
PREFERRED: Easing.inOut(Easing.cubic) or spring() with smooth preset

WHY: Smooth acceleration/deceleration makes data changes readable.

EXAMPLES:
  const barHeight = interpolate(frame, [0, 30], [0, targetHeight], {
    extrapolateRight: 'clamp',
    easing: Easing.inOut(Easing.cubic)
  });
```

### Camera / Pan Movements
```
PREFERRED: Easing.inOut(Easing.quad) or Easing.inOut(Easing.ease)

EXAMPLES:
  const panX = interpolate(frame, [0, 60], [0, -500], {
    extrapolateRight: 'clamp',
    easing: Easing.inOut(Easing.quad)
  });
```

### Typewriter / Counter
```
PREFERRED: Easing.linear (one of the few valid uses of linear)
           OR Easing.out(Easing.ease) for counting up to a number

EXAMPLES:
  // Typewriter
  const chars = Math.floor(interpolate(frame, [0, text.length * 3], [0, text.length], {
    extrapolateRight: 'clamp'
  }));
  const displayText = text.slice(0, chars);

  // Number counter
  const count = Math.round(interpolate(frame, [0, 45], [0, targetNumber], {
    extrapolateRight: 'clamp',
    easing: Easing.out(Easing.ease)
  }));
```

---

## Popular CSS Bezier Curves → Remotion Easing

| CSS Name | Bezier Values | Remotion Equivalent |
|----------|--------------|---------------------|
| `ease` | (0.25, 0.1, 0.25, 1) | `Easing.ease` |
| `ease-in` | (0.42, 0, 1, 1) | `Easing.in(Easing.ease)` |
| `ease-out` | (0, 0, 0.58, 1) | `Easing.out(Easing.ease)` |
| `ease-in-out` | (0.42, 0, 0.58, 1) | `Easing.inOut(Easing.ease)` |
| Material standard | (0.4, 0, 0.2, 1) | `Easing.bezier(0.4, 0, 0.2, 1)` |
| Material decelerate | (0, 0, 0.2, 1) | `Easing.bezier(0, 0, 0.2, 1)` |
| Material accelerate | (0.4, 0, 1, 1) | `Easing.bezier(0.4, 0, 1, 1)` |
| Apple ease | (0.25, 0.1, 0.25, 1) | `Easing.bezier(0.25, 0.1, 0.25, 1)` |
| Power2 out | (0.22, 1, 0.36, 1) | `Easing.bezier(0.22, 1, 0.36, 1)` |
| Power3 out | (0.16, 1, 0.3, 1) | `Easing.bezier(0.16, 1, 0.3, 1)` |
| Power4 out | (0.11, 1, 0.24, 1) | `Easing.bezier(0.11, 1, 0.24, 1)` |
| Expo out | (0.19, 1, 0.22, 1) | `Easing.bezier(0.19, 1, 0.22, 1)` |
| Back out | (0.34, 1.56, 0.64, 1) | `Easing.bezier(0.34, 1.56, 0.64, 1)` |

---

## Duration Guidelines by Animation Type

| Animation | Frames @ 30fps | Seconds | Notes |
|-----------|---------------|---------|-------|
| Fade in/out | 10-20 | 0.33-0.67 | Faster = snappier |
| Slide in/out | 12-24 | 0.4-0.8 | Depends on distance |
| Scale pop | 8-15 | 0.27-0.5 | Quick feels punchy |
| Spring bounce | 20-40 | 0.67-1.33 | Needs time to settle |
| Text reveal | 15-25 | 0.5-0.83 | Per line, not per character |
| Background transition | 20-30 | 0.67-1.0 | Slow enough to notice |
| Counter/number | 30-60 | 1.0-2.0 | Let viewer read the number |
| Path drawing | 30-90 | 1.0-3.0 | Depends on complexity |
| Scene transition | 8-20 | 0.27-0.67 | Faster for energetic content |
| Camera pan | 30-90 | 1.0-3.0 | Smooth and deliberate |

---

## Combining Easings — Advanced Patterns

### Enter + Hold + Exit
```tsx
const enterEnd = 20;
const exitStart = 70;
const exitEnd = 90;

const opacity = interpolate(
  frame,
  [0, enterEnd, exitStart, exitEnd],
  [0, 1, 1, 0],
  {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
    // Note: Easing applies to the ENTIRE range, not per segment.
    // For per-segment easing, use separate interpolate calls:
  }
);

// Better: separate calls for per-segment easing
const enterOpacity = interpolate(frame, [0, enterEnd], [0, 1], {
  extrapolateLeft: 'clamp', extrapolateRight: 'clamp',
  easing: Easing.out(Easing.ease),
});
const exitOpacity = interpolate(frame, [exitStart, exitEnd], [1, 0], {
  extrapolateLeft: 'clamp', extrapolateRight: 'clamp',
  easing: Easing.in(Easing.ease),
});
const opacity = frame < exitStart ? enterOpacity : exitOpacity;
```

### Spring with Delay (Stagger)
```tsx
const items = ['A', 'B', 'C', 'D'];
const staggerDelay = 6; // frames between items

{items.map((item, i) => {
  const s = spring({
    frame: frame - i * staggerDelay,
    fps,
    config: { damping: 200, stiffness: 100 },
  });
  return (
    <div key={i} style={{
      opacity: s,
      transform: `translateY(${(1 - s) * 30}px)`,
    }}>
      {item}
    </div>
  );
})}
```

### Chained Springs
```tsx
// Second spring starts when first settles
const spring1 = spring({ frame, fps, config: { damping: 200, stiffness: 100 } });
const spring2 = spring({
  frame: frame - 20, // starts 20 frames later
  fps,
  config: { damping: 15, stiffness: 200 },
});

const scale = spring1;
const rotation = spring2 * 360; // full rotation after scale completes
```
