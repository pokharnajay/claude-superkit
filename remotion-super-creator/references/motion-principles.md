# 12 Principles of Animation for Remotion

The classic 12 principles of animation adapted for Remotion's `interpolate()`, `spring()`, and `Easing` APIs. Each principle includes a working code pattern and an anti-pattern to avoid.

---

## 1. Squash & Stretch

**Description:** Objects deform during motion to convey weight and elasticity. When an element stretches vertically, it should compress horizontally (and vice versa) to maintain consistent volume. This is the single most important principle for making motion feel alive.

**Remotion Pattern:**
```tsx
const frame = useCurrentFrame();
const { fps } = useVideoConfig();

// Bounce landing: stretch on approach, squash on impact, settle
const scaleY = interpolate(frame, [0, 12, 15, 20, 25], [0.6, 1.3, 0.85, 1.05, 1], {
  extrapolateRight: 'clamp',
});
const scaleX = interpolate(frame, [0, 12, 15, 20, 25], [1.3, 0.8, 1.15, 0.97, 1], {
  extrapolateRight: 'clamp',
});

<div style={{ transform: `scaleX(${scaleX}) scaleY(${scaleY})` }}>
  <img src={ball} />
</div>
```

**Anti-pattern:** Using uniform `scale()` only. Elements feel rigid and mechanical without independent X/Y deformation.

---

## 2. Anticipation

**Description:** A small reverse movement before the main action prepares the viewer. A button shrinks slightly before expanding on click. A character crouches before jumping. This gives the brain time to register what is about to happen.

**Remotion Pattern:**
```tsx
const frame = useCurrentFrame();

// Element slides right, but pulls back first
const translateX = interpolate(
  frame,
  [0, 8, 12, 30],
  [0, -15, -15, 500],
  { extrapolateRight: 'clamp' }
);

// Scale: shrink slightly before growing
const scale = interpolate(
  frame,
  [0, 8, 12, 25],
  [1, 0.92, 0.92, 1.1],
  { extrapolateRight: 'clamp' }
);

<div style={{ transform: `translateX(${translateX}px) scale(${scale})` }} />
```

**Anti-pattern:** Elements that jump instantly from rest to full motion. No wind-up means no visual storytelling.

---

## 3. Staging

**Description:** Every frame should have a clear visual hierarchy that directs the viewer's eye to the most important element. Use size, position, contrast, blur, and motion to establish focus. Only one element should demand primary attention at any moment.

**Remotion Pattern:**
```tsx
const frame = useCurrentFrame();

// Dim background elements when hero appears
const bgOpacity = interpolate(frame, [30, 45], [1, 0.3], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
const heroScale = interpolate(frame, [30, 50], [0.8, 1], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
const heroOpacity = interpolate(frame, [30, 45], [0, 1], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });

<AbsoluteFill>
  {/* Background elements — dimmed */}
  <div style={{ opacity: bgOpacity, filter: `blur(${interpolate(frame, [30, 45], [0, 4])}px)` }}>
    <BackgroundElements />
  </div>
  {/* Hero element — focused */}
  <div style={{ opacity: heroOpacity, transform: `scale(${heroScale})` }}>
    <HeroContent />
  </div>
</AbsoluteFill>
```

**Anti-pattern:** Everything at the same size, same opacity, same z-level. The viewer's eye has nowhere to land.

---

## 4. Straight Ahead & Pose to Pose

**Description:** Remotion's `interpolate()` is inherently pose-to-pose: you define keyframes and the system fills in between. Use multi-point keyframe arrays to create nuanced motion paths rather than simple A-to-B transitions. Add intermediate poses for overshoot, hesitation, or multi-stage reveals.

**Remotion Pattern:**
```tsx
const frame = useCurrentFrame();

// Multi-stage reveal: fade in -> overshoot -> settle -> slight bounce
const translateY = interpolate(
  frame,
  [0, 15, 25, 32, 38],
  [80, -10, 5, -2, 0],
  { extrapolateRight: 'clamp' }
);

const opacity = interpolate(
  frame,
  [0, 10, 15],
  [0, 0.5, 1],
  { extrapolateRight: 'clamp' }
);

// Complex path: element traces an arc
const x = interpolate(frame, [0, 20, 40, 60], [0, 150, 280, 400], { extrapolateRight: 'clamp' });
const y = interpolate(frame, [0, 20, 40, 60], [0, -100, -120, 0], { extrapolateRight: 'clamp' });
```

**Anti-pattern:** Only using two keyframes (`[0, 30]`, `[start, end]`). Motion feels robotic without intermediate poses.

---

## 5. Follow Through & Overlapping Action

**Description:** Not everything stops at the same time. When a character stops running, their hair keeps moving. In UI, stagger element arrivals so related items cascade rather than appearing in unison. Different parts of a composition should have different timing.

**Remotion Pattern:**
```tsx
const frame = useCurrentFrame();
const { fps } = useVideoConfig();

// Staggered entrance for a list of items
const items = ['Revenue', 'Growth', 'Users', 'Retention'];

{items.map((item, i) => {
  const delay = i * 5; // 5-frame stagger
  const progress = spring({
    frame: frame - delay,
    fps,
    config: { damping: 12, stiffness: 120 },
  });
  return (
    <div
      key={item}
      style={{
        transform: `translateX(${interpolate(progress, [0, 1], [-60, 0])}px)`,
        opacity: progress,
      }}
    >
      {item}
    </div>
  );
})}

// Follow-through: main element stops, decoration overshoots
const mainX = interpolate(frame, [0, 20], [0, 300], { extrapolateRight: 'clamp' });
const trailX = spring({ frame: frame - 3, fps, config: { damping: 8 } }); // Delayed, springy
```

**Anti-pattern:** Every element animates in perfect unison. Motion feels artificial and flat.

---

## 6. Slow In & Slow Out (Ease In, Ease Out)

**Description:** Objects in the real world accelerate and decelerate rather than moving at constant speed. Use easing functions to make motion feel natural. Most UI animations should ease-out (fast start, slow end) for responsive feel.

**Remotion Pattern:**
```tsx
import { Easing, interpolate, useCurrentFrame } from 'remotion';

const frame = useCurrentFrame();

// Ease out — snappy entrance (most common for UI)
const x = interpolate(frame, [0, 30], [0, 400], {
  easing: Easing.out(Easing.cubic),
  extrapolateRight: 'clamp',
});

// Ease in-out — smooth transition between states
const opacity = interpolate(frame, [0, 25], [0, 1], {
  easing: Easing.inOut(Easing.quad),
  extrapolateRight: 'clamp',
});

// Ease in — accelerating exit (element leaving)
const exitY = interpolate(frame, [60, 90], [0, 600], {
  easing: Easing.in(Easing.cubic),
  extrapolateLeft: 'clamp',
  extrapolateRight: 'clamp',
});

// Custom bezier for precise control
const custom = interpolate(frame, [0, 30], [0, 1], {
  easing: Easing.bezier(0.34, 1.56, 0.64, 1), // overshoot
  extrapolateRight: 'clamp',
});
```

**Common Easing Reference:**
| Easing | Feel | Use For |
|--------|------|---------|
| `Easing.out(Easing.cubic)` | Snappy, responsive | Entrances |
| `Easing.in(Easing.cubic)` | Accelerating | Exits |
| `Easing.inOut(Easing.quad)` | Smooth, balanced | State transitions |
| `Easing.bezier(0.34, 1.56, 0.64, 1)` | Overshoot | Playful entrances |
| `Easing.out(Easing.exp)` | Very fast start | Dramatic reveals |

**Anti-pattern:** `Easing.linear` everywhere. Linear motion feels mechanical and unnatural for almost all UI/video animation.

---

## 7. Arc

**Description:** Natural motion follows curved paths, not straight lines. A tossed ball traces a parabola. Even UI elements feel more natural when they follow slight arcs rather than moving in a perfectly straight line.

**Remotion Pattern:**
```tsx
const frame = useCurrentFrame();

// Parabolic arc: throw animation
const progress = interpolate(frame, [0, 40], [0, 1], {
  easing: Easing.linear,
  extrapolateRight: 'clamp',
});

const x = interpolate(progress, [0, 1], [0, 600]); // Linear horizontal
const y = -400 * (4 * progress * (1 - progress)); // Parabolic vertical (peaks at progress=0.5)

// Circular arc entrance
const angle = interpolate(frame, [0, 30], [-Math.PI / 2, 0], {
  easing: Easing.out(Easing.cubic),
  extrapolateRight: 'clamp',
});
const radius = 300;
const arcX = Math.cos(angle) * radius;
const arcY = Math.sin(angle) * radius;

<div style={{ transform: `translate(${arcX}px, ${arcY}px)` }} />

// Subtle arc on slide-in (combine translateX and translateY with different easings)
const slideX = interpolate(frame, [0, 25], [-200, 0], {
  easing: Easing.out(Easing.cubic),
  extrapolateRight: 'clamp',
});
const slideY = interpolate(frame, [0, 25], [40, 0], {
  easing: Easing.out(Easing.quad),
  extrapolateRight: 'clamp',
});
```

**Anti-pattern:** All motion in perfectly straight horizontal or vertical lines. Especially noticeable for objects entering from corners.

---

## 8. Secondary Action

**Description:** While the primary action plays, secondary elements reinforce the mood without stealing focus. Background particles drift, gradients subtly shift, decorative elements pulse. These make the scene feel alive.

**Remotion Pattern:**
```tsx
const frame = useCurrentFrame();

// Floating background particles
const Particle: React.FC<{ delay: number; x: number }> = ({ delay, x }) => {
  const y = interpolate((frame + delay) % 120, [0, 120], [1080, -20]);
  const opacity = interpolate((frame + delay) % 120, [0, 30, 90, 120], [0, 0.3, 0.3, 0]);
  return (
    <div style={{
      position: 'absolute', left: x, top: y, opacity,
      width: 6, height: 6, borderRadius: '50%',
      backgroundColor: 'rgba(255,255,255,0.4)',
    }} />
  );
};

// Slow gradient rotation behind main content
const gradientAngle = interpolate(frame, [0, 300], [0, 360]);
<div style={{
  background: `conic-gradient(from ${gradientAngle}deg, #1a0033, #6366f1, #1a0033)`,
  filter: 'blur(80px)',
  position: 'absolute', inset: -100,
}} />

// Subtle scale pulse on a background element
const pulse = Math.sin(frame * 0.05) * 0.03 + 1;
<div style={{ transform: `scale(${pulse})` }} />
```

**Anti-pattern:** Completely static backgrounds. The scene feels dead even if the foreground is animated.

---

## 9. Timing

**Description:** The number of frames for an action defines its character. Fewer frames = fast/snappy/energetic. More frames = slow/heavy/dramatic. Timing is the most impactful variable you can adjust.

**Remotion Pattern / Reference:**
```tsx
// Timing guide at 30fps:
// Lightning fast:  3-5 frames  (0.1-0.17s)  — micro-interactions, blips
// Fast/snappy:     6-10 frames (0.2-0.33s)  — button clicks, small moves
// Normal:         12-20 frames (0.4-0.67s)  — standard transitions
// Smooth:         20-30 frames (0.67-1.0s)  — slides, fades
// Dramatic:       30-60 frames (1.0-2.0s)   — hero reveals, cinematic
// Slow/ambient:   60-120 frames (2.0-4.0s)  — background drifts, moods

// Fast card flip
const fastFlip = interpolate(frame, [0, 8], [0, 180], { extrapolateRight: 'clamp' });

// Normal entrance
const normalSlide = interpolate(frame, [0, 18], [-100, 0], {
  easing: Easing.out(Easing.cubic),
  extrapolateRight: 'clamp',
});

// Dramatic hero reveal
const heroScale = interpolate(frame, [0, 45], [0.5, 1], {
  easing: Easing.out(Easing.exp),
  extrapolateRight: 'clamp',
});

// Create rhythm: fast entrance, pause, fast exit
// Entrance: frames 0-15 | Hold: frames 15-75 | Exit: frames 75-90
```

**Anti-pattern:** Every animation takes the same duration. A title reveal should not take the same time as a button hover.

---

## 10. Exaggeration

**Description:** Overshoot, bounce, and spring make motion feel dynamic and alive. Elements that land exactly at their target feel robotic. Springs naturally overshoot and settle, which mimics real-world physics.

**Remotion Pattern:**
```tsx
import { spring, useCurrentFrame, useVideoConfig } from 'remotion';

const frame = useCurrentFrame();
const { fps } = useVideoConfig();

// Bouncy entrance — low damping = more overshoot
const bouncy = spring({
  frame,
  fps,
  config: {
    damping: 8,       // Low = more bounce (default 10)
    stiffness: 100,   // How fast it moves
    mass: 1,          // Weight of the element
    overshootClamping: false, // MUST be false for overshoot
  },
});

// Snappy with slight overshoot
const snappy = spring({
  frame,
  fps,
  config: { damping: 14, stiffness: 200 },
});

// Dramatic slow bounce
const dramatic = spring({
  frame,
  fps,
  config: { damping: 6, stiffness: 40, mass: 2 },
});

// Use spring for scale (overshoots past 1.0 then settles)
<div style={{ transform: `scale(${bouncy})` }} />
```

**Spring Config Quick Reference:**
| Feel | damping | stiffness | mass |
|------|---------|-----------|------|
| Snappy | 15-20 | 150-200 | 0.5-1 |
| Bouncy | 6-10 | 80-120 | 1 |
| Dramatic | 4-8 | 30-60 | 1.5-3 |
| Heavy | 12-15 | 40-60 | 3-5 |
| Wobbly | 3-5 | 100-150 | 1 |

**Anti-pattern:** `overshootClamping: true` everywhere, or only using `interpolate()` with linear endpoints. Everything feels dead.

---

## 11. Solid Drawing (Depth)

**Description:** Create the illusion of three-dimensional space through shadows, perspective, parallax, and layering. Even 2D motion graphics benefit enormously from depth cues.

**Remotion Pattern:**
```tsx
const frame = useCurrentFrame();

// Parallax: layers move at different speeds
const bgX = interpolate(frame, [0, 300], [0, -50]);  // Slow
const midX = interpolate(frame, [0, 300], [0, -150]); // Medium
const fgX = interpolate(frame, [0, 300], [0, -300]); // Fast

<AbsoluteFill>
  <div style={{ transform: `translateX(${bgX}px)`, zIndex: 0 }}>
    <BackgroundLayer />
  </div>
  <div style={{ transform: `translateX(${midX}px)`, zIndex: 1 }}>
    <MiddleLayer />
  </div>
  <div style={{ transform: `translateX(${fgX}px)`, zIndex: 2 }}>
    <ForegroundLayer />
  </div>
</AbsoluteFill>

// Card with 3D perspective on hover/reveal
const rotateY = interpolate(frame, [0, 30], [15, 0], { extrapolateRight: 'clamp' });
<div style={{
  perspective: '1000px',
  perspectiveOrigin: 'center',
}}>
  <div style={{
    transform: `rotateY(${rotateY}deg)`,
    boxShadow: `${rotateY * 0.5}px 8px 30px rgba(0,0,0,0.3)`,
  }}>
    <CardContent />
  </div>
</div>

// Dynamic shadow that follows motion
const x = interpolate(frame, [0, 30], [-200, 0], { extrapolateRight: 'clamp' });
const shadowX = interpolate(frame, [0, 30], [20, 0], { extrapolateRight: 'clamp' });
<div style={{
  transform: `translateX(${x}px)`,
  boxShadow: `${shadowX}px 10px 40px rgba(0,0,0,0.2)`,
}} />
```

**Anti-pattern:** Flat compositions with no shadows, no layering, no perspective. Everything sits on a single plane.

---

## 12. Appeal

**Description:** The final polish that makes a video feel professional. Consistent spacing, rounded corners, color harmony, subtle micro-animations, attention to pixel-level detail. Appeal is the sum of many small decisions.

**Remotion Pattern:**
```tsx
const frame = useCurrentFrame();

// Rounded, padded containers instead of bare rectangles
const Card = ({ children }: { children: React.ReactNode }) => (
  <div style={{
    backgroundColor: 'rgba(255,255,255,0.08)',
    borderRadius: 16,
    padding: '24px 32px',
    backdropFilter: 'blur(12px)',
    border: '1px solid rgba(255,255,255,0.1)',
    boxShadow: '0 8px 32px rgba(0,0,0,0.2)',
  }}>
    {children}
  </div>
);

// Micro-animation: subtle shimmer on text
const shimmerX = interpolate(frame % 90, [0, 90], [-200, 200]);
<h1 style={{
  backgroundImage: `linear-gradient(90deg, #fff 0%, #fff 40%, #60a5fa ${50 + shimmerX * 0.1}%, #fff 60%, #fff 100%)`,
  backgroundClip: 'text',
  WebkitBackgroundClip: 'text',
  WebkitTextFillColor: 'transparent',
}}>
  Premium Title
</h1>

// Consistent 8px grid spacing
const GRID = 8;
const spacing = (n: number) => n * GRID;
// spacing(1) = 8, spacing(2) = 16, spacing(3) = 24, spacing(4) = 32

// Polish checklist:
// - Border radius on all containers (8-16px)
// - Consistent color palette (never random hex values)
// - Box shadows with multiple layers for depth
// - Text line-height 1.4-1.6
// - Minimum 16px padding inside containers
// - Backdrop blur on overlapping translucent elements
// - Subtle gradient overlays rather than flat colors
```

**Anti-pattern:** Bare unstyled rectangles, inconsistent spacing, sharp corners, no shadows, random colors. The hallmark of a first draft that shipped as final.

---

## Combining Principles: Complete Example

```tsx
import { AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig, Easing } from 'remotion';

export const PolishedEntrance: React.FC<{ text: string }> = ({ text }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Principle 2 (Anticipation): slight scale down before spring
  const anticipation = frame < 5
    ? interpolate(frame, [0, 5], [1, 0.95])
    : 1;

  // Principle 10 (Exaggeration): bouncy spring
  const s = spring({ frame: Math.max(0, frame - 5), fps, config: { damping: 10, stiffness: 100 } });

  // Principle 6 (Slow in/out): eased opacity
  const opacity = interpolate(frame, [3, 18], [0, 1], {
    easing: Easing.out(Easing.quad),
    extrapolateLeft: 'clamp', extrapolateRight: 'clamp',
  });

  // Principle 7 (Arc): curved entrance path
  const x = interpolate(s, [0, 1], [-120, 0]);
  const y = interpolate(s, [0, 1], [40, 0]);

  // Principle 1 (Squash & Stretch): deform during motion
  const scaleX = interpolate(s, [0, 0.5, 0.8, 1], [0.8, 1.05, 0.98, 1]);
  const scaleY = interpolate(s, [0, 0.5, 0.8, 1], [1.1, 0.96, 1.01, 1]);

  return (
    <div style={{
      transform: `translate(${x}px, ${y}px) scaleX(${scaleX * anticipation}) scaleY(${scaleY * anticipation})`,
      opacity,
      fontSize: 64, fontWeight: 700, color: '#fff',
    }}>
      {text}
    </div>
  );
};
```
