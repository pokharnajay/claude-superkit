# Transition Catalog — Complete @remotion/transitions Reference

> Every transition type, with imports, parameters, code examples, and usage guidance.

---

## Setup — Imports

```tsx
// Core
import { TransitionSeries, linearTiming, springTiming } from '@remotion/transitions';

// Presentations (import each separately)
import { fade } from '@remotion/transitions/fade';
import { slide } from '@remotion/transitions/slide';
import { wipe } from '@remotion/transitions/wipe';
import { flip } from '@remotion/transitions/flip';
import { clockWipe } from '@remotion/transitions/clock-wipe';
import { cube3d } from '@remotion/transitions/cube-3d';
```

---

## TransitionSeries — Core Component

TransitionSeries replaces `<Series>` when you need transitions between scenes. Each `<TransitionSeries.Sequence>` is a scene, and `<TransitionSeries.Transition>` defines the crossover between them.

```tsx
<TransitionSeries>
  <TransitionSeries.Sequence durationInFrames={90}>
    <SceneA />
  </TransitionSeries.Sequence>

  <TransitionSeries.Transition
    presentation={fade()}
    timing={linearTiming({ durationInFrames: 15 })}
  />

  <TransitionSeries.Sequence durationInFrames={90}>
    <SceneB />
  </TransitionSeries.Sequence>
</TransitionSeries>
```

**Key rules:**
- Transition OVERLAPS the adjacent sequences — it does NOT add time
- A 15-frame transition means 15 frames where both scenes are visible simultaneously
- The total duration = sum of all sequence durations MINUS sum of all transition durations
- Example: 90f + 90f with a 15f transition = 165f total (not 180f)
- Each sequence's `durationInFrames` includes the overlap period

---

## Timing Functions

### linearTiming
```tsx
import { linearTiming } from '@remotion/transitions';

linearTiming({
  durationInFrames: 15,  // how many frames the transition lasts
})
// Constant-speed transition. Simple and predictable.
// Best for: fade, simple wipes, when you want precise control.
```

### springTiming
```tsx
import { springTiming } from '@remotion/transitions';

springTiming({
  config: {
    damping: 200,          // friction
    stiffness: 100,        // tightness
    mass: 1,               // weight
  },
  durationInFrames: 30,              // optional: auto-calculated if omitted
  durationRestThreshold: 0.001,      // when to consider spring "at rest"
})
// Physics-based timing. Feels natural and organic.
// Best for: slide, flip, cube3d — any transition with physical movement.
```

---

## Transition Presentations — Complete Catalog

---

### 1. fade()

**Import:** `import { fade } from '@remotion/transitions/fade';`

**Parameters:** None. It's a simple opacity crossfade.

**Behavior:** Outgoing scene fades from opacity 1 to 0 while incoming scene fades from 0 to 1. Both are visible during the transition.

```tsx
<TransitionSeries>
  <TransitionSeries.Sequence durationInFrames={90}>
    <Scene1 />
  </TransitionSeries.Sequence>
  <TransitionSeries.Transition
    presentation={fade()}
    timing={linearTiming({ durationInFrames: 15 })}
  />
  <TransitionSeries.Sequence durationInFrames={90}>
    <Scene2 />
  </TransitionSeries.Sequence>
</TransitionSeries>
```

**When to use:** The most versatile, safest transition. Works for ANY content. Default choice when unsure.

**Mood:** Elegant, smooth, professional, understated.

**Duration recommendation:** 10-20 frames. Shorter (8-12f) for fast-paced content, longer (15-25f) for cinematic feel.

---

### 2. slide()

**Import:** `import { slide } from '@remotion/transitions/slide';`

**Parameters:**
```tsx
slide({
  direction: 'from-left',  // 'from-left' | 'from-right' | 'from-top' | 'from-bottom'
})
```

**Behavior:** Incoming scene slides in from the specified direction, pushing the outgoing scene away.

```tsx
// Slide from right (new content enters from right side)
<TransitionSeries.Transition
  presentation={slide({ direction: 'from-right' })}
  timing={springTiming({ config: { damping: 200, stiffness: 100 } })}
/>

// Slide from bottom (content rises up)
<TransitionSeries.Transition
  presentation={slide({ direction: 'from-bottom' })}
  timing={linearTiming({ durationInFrames: 18 })}
/>

// Slide from left
<TransitionSeries.Transition
  presentation={slide({ direction: 'from-left' })}
  timing={springTiming({ config: { damping: 30, stiffness: 120 }, durationInFrames: 20 })}
/>

// Slide from top
<TransitionSeries.Transition
  presentation={slide({ direction: 'from-top' })}
  timing={linearTiming({ durationInFrames: 15 })}
/>
```

**When to use:** Sequential content, navigation-style transitions, content that has directional flow (timelines, steps, before/after).

**Mood:** Dynamic, energetic, directional, purposeful.

**Duration recommendation:** 12-20 frames. Use springTiming for natural deceleration.

**Direction guide:**
- `from-right`: "Next" content, forward progression, timeline advancing
- `from-left`: "Previous" content, going back, reverse chronological
- `from-bottom`: Reveals, rising action, unveiling, uplifting
- `from-top`: Descending action, dropping in, gravity-based

---

### 3. wipe()

**Import:** `import { wipe } from '@remotion/transitions/wipe';`

**Parameters:**
```tsx
wipe({
  direction: 'from-left',  // 'from-left' | 'from-right' | 'from-top' | 'from-bottom'
})
```

**Behavior:** A hard edge sweeps across the screen, revealing the incoming scene. Unlike slide, the outgoing scene does NOT move — it's simply covered/revealed by the wipe edge.

```tsx
// Wipe from left to right
<TransitionSeries.Transition
  presentation={wipe({ direction: 'from-left' })}
  timing={linearTiming({ durationInFrames: 15 })}
/>

// Wipe from bottom (curtain rising)
<TransitionSeries.Transition
  presentation={wipe({ direction: 'from-bottom' })}
  timing={linearTiming({ durationInFrames: 20 })}
/>

// Wipe from right with spring (soft landing)
<TransitionSeries.Transition
  presentation={wipe({ direction: 'from-right' })}
  timing={springTiming({ config: { damping: 200, stiffness: 80 }, durationInFrames: 25 })}
/>

// Wipe from top
<TransitionSeries.Transition
  presentation={wipe({ direction: 'from-top' })}
  timing={linearTiming({ durationInFrames: 12 })}
/>
```

**When to use:** Before/after reveals, comparison content, progress indicators, news/broadcast style.

**Mood:** Clean, decisive, editorial, broadcast-like.

**Duration recommendation:** 10-20 frames. Linear timing often works best for clean wipes.

---

### 4. flip()

**Import:** `import { flip } from '@remotion/transitions/flip';`

**Parameters:**
```tsx
flip({
  direction: 'from-left',  // 'from-left' | 'from-right' | 'from-top' | 'from-bottom'
  perspective: 1000,        // optional: CSS perspective value (default: 1000)
})
```

**Behavior:** 3D page-flip effect. The outgoing scene rotates away like a page turning, revealing the incoming scene on the "back side."

```tsx
// Horizontal flip from left
<TransitionSeries.Transition
  presentation={flip({ direction: 'from-left' })}
  timing={springTiming({ config: { damping: 200, stiffness: 100 }, durationInFrames: 25 })}
/>

// Vertical flip from bottom
<TransitionSeries.Transition
  presentation={flip({ direction: 'from-bottom' })}
  timing={linearTiming({ durationInFrames: 20 })}
/>

// Flip with tighter perspective (more dramatic 3D)
<TransitionSeries.Transition
  presentation={flip({ direction: 'from-right', perspective: 600 })}
  timing={springTiming({ config: { damping: 30, stiffness: 120 }, durationInFrames: 25 })}
/>

// Flip from top (card flip down)
<TransitionSeries.Transition
  presentation={flip({ direction: 'from-top', perspective: 1200 })}
  timing={linearTiming({ durationInFrames: 18 })}
/>
```

**When to use:** Card reveals, before/after, flashcard-style educational content, Q&A reveals.

**Mood:** Playful, interactive, 3D, card-like, tactile.

**Duration recommendation:** 18-30 frames. Needs enough time for the 3D rotation to read clearly. Spring timing adds satisfying settle.

**Perspective guide:**
- `600-800`: Dramatic, exaggerated 3D (elements feel close to camera)
- `1000` (default): Balanced, natural 3D
- `1200-2000`: Subtle, flatter 3D (elements feel farther from camera)

---

### 5. clockWipe()

**Import:** `import { clockWipe } from '@remotion/transitions/clock-wipe';`

**Parameters:**
```tsx
clockWipe({
  width: 1080,   // video width (required)
  height: 1920,  // video height (required)
})
```

**Behavior:** Circular wipe that sweeps around like a clock hand, revealing the incoming scene in a radial pattern from the top center.

```tsx
const { width, height } = useVideoConfig();

<TransitionSeries.Transition
  presentation={clockWipe({ width, height })}
  timing={linearTiming({ durationInFrames: 25 })}
/>

// Full example
const MyVideo: React.FC = () => {
  const { width, height } = useVideoConfig();

  return (
    <TransitionSeries>
      <TransitionSeries.Sequence durationInFrames={90}>
        <Scene1 />
      </TransitionSeries.Sequence>
      <TransitionSeries.Transition
        presentation={clockWipe({ width, height })}
        timing={linearTiming({ durationInFrames: 25 })}
      />
      <TransitionSeries.Sequence durationInFrames={90}>
        <Scene2 />
      </TransitionSeries.Sequence>
    </TransitionSeries>
  );
};
```

**When to use:** Cinematic reveals, time-related content, dramatic scene changes, countdown transitions.

**Mood:** Cinematic, dramatic, time-focused, epic, countdown.

**Duration recommendation:** 20-30 frames. Linear timing works well. Too fast and the circular motion is lost.

**Important:** Must pass width and height — usually from `useVideoConfig()`. Declare the hook OUTSIDE the TransitionSeries JSX.

---

### 6. cube3d()

**Import:** `import { cube3d } from '@remotion/transitions/cube-3d';`

**Parameters:**
```tsx
cube3d({
  direction: 'from-left',  // 'from-left' | 'from-right' | 'from-top' | 'from-bottom'
  perspective: 1000,        // optional: CSS perspective (default: 1000)
})
```

**Behavior:** Both scenes are treated as faces of a 3D cube. The cube rotates 90 degrees to reveal the incoming scene on the adjacent face.

```tsx
// Cube rotation from right
<TransitionSeries.Transition
  presentation={cube3d({ direction: 'from-right' })}
  timing={springTiming({ config: { damping: 200, stiffness: 80 }, durationInFrames: 25 })}
/>

// Cube rotation from bottom
<TransitionSeries.Transition
  presentation={cube3d({ direction: 'from-bottom', perspective: 800 })}
  timing={linearTiming({ durationInFrames: 20 })}
/>

// Cube rotation from left with spring
<TransitionSeries.Transition
  presentation={cube3d({ direction: 'from-left', perspective: 1200 })}
  timing={springTiming({ config: { damping: 30, stiffness: 100 }, durationInFrames: 30 })}
/>
```

**When to use:** Energetic/music videos, tech demos, gaming content, any content that benefits from strong 3D spatial feeling.

**Mood:** Dynamic, 3D, energetic, modern, tech-forward, spatial.

**Duration recommendation:** 15-25 frames. Spring timing adds satisfying weight. Too slow and it feels sluggish.

---

## Duration Guidelines by Video Type

| Video Type | Transition Duration | Recommended Transitions | Timing |
|-----------|-------------------|----------------------|--------|
| Social media (TikTok, Reels) | 8-12 frames | fade, slide, wipe | linearTiming |
| Corporate / explainer | 15-20 frames | fade, slide | springTiming (smooth) |
| Cinematic / trailer | 20-30 frames | fade, clockWipe | linearTiming |
| Energetic / music video | 5-10 frames | slide, wipe, cube3d | linearTiming |
| Data visualization | 15-20 frames | fade | linearTiming |
| News / broadcast | 10-15 frames | slide, wipe | linearTiming |
| Educational / tutorial | 12-18 frames | fade, slide | springTiming (gentle) |
| Product showcase | 15-25 frames | fade, flip, cube3d | springTiming |
| Storytelling / narrative | 20-30 frames | fade | linearTiming |
| Countdown / reveal | 15-20 frames | clockWipe, flip | linearTiming |

---

## Common Patterns

### Consistent Transitions Throughout
```tsx
// Use the same transition between ALL scenes for consistency
const MyVideo: React.FC = () => {
  const { width, height } = useVideoConfig();
  const scenes = [<Scene1 />, <Scene2 />, <Scene3 />, <Scene4 />];
  const sceneDuration = 90;
  const transitionDuration = 12;

  return (
    <TransitionSeries>
      {scenes.map((scene, i) => (
        <React.Fragment key={i}>
          <TransitionSeries.Sequence durationInFrames={sceneDuration}>
            {scene}
          </TransitionSeries.Sequence>
          {i < scenes.length - 1 && (
            <TransitionSeries.Transition
              presentation={fade()}
              timing={linearTiming({ durationInFrames: transitionDuration })}
            />
          )}
        </React.Fragment>
      ))}
    </TransitionSeries>
  );
};
```

### Alternating Transitions
```tsx
// Alternate between transitions for visual variety
const transitions = [
  { presentation: slide({ direction: 'from-right' }), timing: springTiming({ config: { damping: 200 } }) },
  { presentation: fade(), timing: linearTiming({ durationInFrames: 15 }) },
  { presentation: wipe({ direction: 'from-left' }), timing: linearTiming({ durationInFrames: 12 }) },
];

<TransitionSeries>
  {scenes.map((scene, i) => (
    <React.Fragment key={i}>
      <TransitionSeries.Sequence durationInFrames={90}>
        {scene}
      </TransitionSeries.Sequence>
      {i < scenes.length - 1 && (
        <TransitionSeries.Transition
          presentation={transitions[i % transitions.length].presentation}
          timing={transitions[i % transitions.length].timing}
        />
      )}
    </React.Fragment>
  ))}
</TransitionSeries>
```

### No Transition (Hard Cut)
```tsx
// Simply don't add a <TransitionSeries.Transition> between sequences
<TransitionSeries>
  <TransitionSeries.Sequence durationInFrames={90}>
    <Scene1 />
  </TransitionSeries.Sequence>
  {/* No transition = hard cut */}
  <TransitionSeries.Sequence durationInFrames={90}>
    <Scene2 />
  </TransitionSeries.Sequence>
</TransitionSeries>

// Or use a 1-frame fade for an almost-hard cut with slight softening:
<TransitionSeries.Transition
  presentation={fade()}
  timing={linearTiming({ durationInFrames: 2 })}
/>
```

---

## Custom Transitions

You can build custom presentations for TransitionSeries. A presentation is a function that returns enter/exit style objects.

```tsx
import type { TransitionPresentation, TransitionPresentationComponentProps } from '@remotion/transitions';

// Custom zoom transition
const customZoom: TransitionPresentation = () => {
  return {
    component: ({ progress, isExiting, children }: TransitionPresentationComponentProps) => {
      const style: React.CSSProperties = isExiting
        ? {
            opacity: 1 - progress,
            transform: `scale(${1 + progress * 0.3})`,
            position: 'absolute' as const,
            width: '100%',
            height: '100%',
          }
        : {
            opacity: progress,
            transform: `scale(${1 - (1 - progress) * 0.3})`,
            position: 'absolute' as const,
            width: '100%',
            height: '100%',
          };

      return <div style={style}>{children}</div>;
    },
  };
};

// Usage
<TransitionSeries.Transition
  presentation={customZoom()}
  timing={linearTiming({ durationInFrames: 20 })}
/>
```

### Custom Blur Transition
```tsx
const blurTransition: TransitionPresentation = () => ({
  component: ({ progress, isExiting, children }) => {
    const blur = isExiting
      ? interpolate(progress, [0, 1], [0, 10])
      : interpolate(progress, [0, 1], [10, 0]);
    const opacity = isExiting ? 1 - progress : progress;

    return (
      <div style={{
        filter: `blur(${blur}px)`,
        opacity,
        position: 'absolute',
        width: '100%',
        height: '100%',
      }}>
        {children}
      </div>
    );
  },
});
```

### Custom Scale + Rotate Transition
```tsx
const scaleRotate: TransitionPresentation = () => ({
  component: ({ progress, isExiting, children }) => {
    const scale = isExiting
      ? interpolate(progress, [0, 1], [1, 0.5])
      : interpolate(progress, [0, 1], [0.5, 1]);
    const rotate = isExiting
      ? interpolate(progress, [0, 1], [0, -15])
      : interpolate(progress, [0, 1], [15, 0]);
    const opacity = isExiting ? 1 - progress : progress;

    return (
      <div style={{
        transform: `scale(${scale}) rotate(${rotate}deg)`,
        opacity,
        position: 'absolute',
        width: '100%',
        height: '100%',
      }}>
        {children}
      </div>
    );
  },
});
```

---

## Light Leak Overlays with Transitions

```tsx
import { LightLeak } from '@remotion/light-leaks';

// Method 1: Light leak as a scene overlay during transition
<TransitionSeries>
  <TransitionSeries.Sequence durationInFrames={90}>
    <AbsoluteFill>
      <Scene1 />
    </AbsoluteFill>
  </TransitionSeries.Sequence>
  <TransitionSeries.Transition
    presentation={fade()}
    timing={linearTiming({ durationInFrames: 30 })}
  />
  <TransitionSeries.Sequence durationInFrames={90}>
    <AbsoluteFill>
      <Scene2 />
      {/* Light leak overlay on the incoming scene */}
      <AbsoluteFill style={{ mixBlendMode: 'screen' }}>
        <LightLeak seed={42} hueShift={0} />
      </AbsoluteFill>
    </AbsoluteFill>
  </TransitionSeries.Sequence>
</TransitionSeries>

// Method 2: Light leak as standalone atmosphere on specific frames
const frame = useCurrentFrame();
const showLeak = frame > 80 && frame < 120;

{showLeak && (
  <AbsoluteFill style={{ mixBlendMode: 'screen', opacity: 0.7 }}>
    <LightLeak seed={7} hueShift={30} />
  </AbsoluteFill>
)}
```

---

## Transition Cheat Sheet — Quick Reference

```
SAFEST DEFAULT:        fade() + linearTiming({ durationInFrames: 15 })
DYNAMIC HORIZONTAL:   slide({ direction: 'from-right' }) + springTiming({ config: { damping: 200 } })
CLEAN REVEAL:         wipe({ direction: 'from-left' }) + linearTiming({ durationInFrames: 12 })
CARD FLIP:            flip({ direction: 'from-right' }) + springTiming({ config: { damping: 30, stiffness: 120 } })
CINEMATIC:            clockWipe({ width, height }) + linearTiming({ durationInFrames: 25 })
ENERGETIC 3D:         cube3d({ direction: 'from-right' }) + springTiming({ config: { damping: 200, stiffness: 80 } })
HARD CUT:             (no transition element between sequences)
ALMOST-HARD CUT:      fade() + linearTiming({ durationInFrames: 2 })
```

---

## Total Duration Calculation

```
totalFrames = sum(allSequenceDurations) - sum(allTransitionDurations)

Example:
  Scene 1: 90 frames
  Transition: 15 frames (fade)
  Scene 2: 120 frames
  Transition: 15 frames (slide)
  Scene 3: 90 frames

  Total = (90 + 120 + 90) - (15 + 15) = 300 - 30 = 270 frames
  At 30fps = 9 seconds

IMPORTANT: Set your Composition durationInFrames to this calculated total,
not to the sum of scene durations.
```

### Helper: Calculate Total Duration
```tsx
const scenes = [
  { duration: 90 },
  { duration: 120 },
  { duration: 90 },
];
const transitionDuration = 15;
const numTransitions = scenes.length - 1;
const totalFrames = scenes.reduce((sum, s) => sum + s.duration, 0)
  - (numTransitions * transitionDuration);
// Use totalFrames as your Composition's durationInFrames
```
