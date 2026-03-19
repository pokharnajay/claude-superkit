---
name: remotion-video-creator
description: Create professional videos with Remotion (React/TypeScript). Use this skill when the user asks to create any kind of video, animation, motion graphics, or video content. Covers social media videos (TikTok, Reels, Shorts), explainer videos, kinetic typography, data visualizations, slideshows, audiograms, intros/outros, news highlights. Full pipeline from concept to rendered MP4. Also trigger when user mentions Remotion, video rendering, motion design, or programmatic video creation.
license: MIT
metadata:
  author: Jay Pokharna
  version: 1.0.0
---

# Remotion Video Creator

Create professional videos programmatically with React and Remotion. Every video is a React component — each frame is a render.

## When to Use

Use this skill when:
- User asks to create any video, animation, or motion graphic
- User mentions TikTok, Reels, Shorts, YouTube, or social media video
- User wants kinetic typography, data visualization video, explainer, slideshow, audiogram, intro/outro, or news highlight
- User mentions Remotion, video rendering, or programmatic video
- User wants to render React components to video

## The 4-Phase Workflow

### Phase 1: CONCEPT
Understand what video the user wants. Determine:
- **Video type** → Route to correct sub-skill
- **Platform/Format** → Dimensions, FPS, duration (read `references/format-specs.md`)
- **Mood/Style** → Select palette and typography (read `references/color-palettes.md` and `references/font-pairings.md`)
- **Audio plan** → Background music, voiceover, SFX, or silent

### Phase 2: STORYBOARD
Create a scene-by-scene breakdown:

| Scene # | Duration (frames) | Content | Transition In | Transition Out | Audio |
|---------|-------------------|---------|---------------|----------------|-------|
| 1 | 90 (3s @30fps) | Hook/Title | fade() | slide() | whoosh SFX |
| 2 | 150 (5s @30fps) | Main content | slide() | wipe() | bg music |
| ... | ... | ... | ... | ... | ... |

Total duration must match platform requirements.

### Phase 3: CODE
Generate Remotion TSX components:
1. `src/Root.tsx` — Register all `<Composition>` entries
2. `src/index.ts` — `registerRoot(RemotionRoot)`
3. `src/compositions/[VideoName].tsx` — Main video component
4. `src/components/[Scene].tsx` — Individual scene components
5. `src/lib/constants.ts` — Colors, fonts, timing constants

**Critical Remotion Rules:**
- ALL animations use `useCurrentFrame()` + `interpolate()` or `spring()` — NEVER CSS transitions or Tailwind animate-* classes
- Use `<AbsoluteFill>` for full-frame containers
- Use `<Sequence from={frame} durationInFrames={n}>` for scene timing
- Use `<TransitionSeries>` for scene transitions (fade, slide, wipe, flip, clockWipe, cube3d)
- Use `<Img>` not `<img>`, `<Video>` not `<video>`, `<Audio>` for sound
- Use `staticFile()` for assets in the `public/` folder
- Load fonts with `@remotion/google-fonts`: `import { loadFont } from '@remotion/google-fonts/Inter'`

### Phase 4: RENDER
Scaffold and render:
```bash
# If no project exists:
npx create-video@latest my-video

# Install dependencies:
npm install

# Preview in browser:
npx remotion studio

# Render to MP4:
npx remotion render src/index.ts CompositionId out/video.mp4

# With custom props:
npx remotion render src/index.ts CompositionId out/video.mp4 --props='{"title":"Hello"}'
```

## Routing Table

| User Request | Route To |
|-------------|----------|
| "Make a TikTok / Reel / Short / Story" | `remotion-video-creator:social-media-video` |
| "Create a product demo / tutorial / explainer" | `remotion-video-creator:explainer-video` |
| "Visualize this data / animate a chart" | `remotion-video-creator:data-viz-video` |
| "Make a text animation / kinetic typography / lyric video" | `remotion-video-creator:kinetic-typography` |
| "Create a slideshow / photo montage" | `remotion-video-creator:slideshow-video` |
| "Make a podcast audiogram / waveform video" | `remotion-video-creator:audiogram-video` |
| "Create a logo animation / intro / outro" | `remotion-video-creator:intro-outro` |
| "Make a news video / headline animation" | `remotion-video-creator:news-highlight` |
| "Render / scaffold a Remotion project" | `remotion-video-creator:render-engine` |

## Specialist Agents

| Agent | Expertise | When to Consult |
|-------|-----------|----------------|
| **video-director** | Full pipeline orchestration | Complex multi-scene videos |
| **motion-designer** | Easing, timing, stagger, parallax | Animation refinement |
| **scene-architect** | Scene planning, duration, pacing | Video structure decisions |
| **audio-engineer** | Music, SFX, voiceover, captions | Audio integration |
| **render-engineer** | Codecs, optimization, Lambda | Rendering issues |
| **typography-director** | Font selection, text animation | Typography decisions |

## Reference Files

Load these as needed:
- `references/remotion-api-reference.md` — Complete API cheatsheet for all Remotion packages
- `references/format-specs.md` — Platform dimensions, FPS, duration limits
- `references/font-pairings.md` — 50 curated video font pairings by mood
- `references/color-palettes.md` — 25+ video-optimized color palettes
- `references/easing-library.md` — All easing curves with Remotion code
- `references/transition-catalog.md` — Every transition type with examples
- `references/sound-effects-library.md` — SFX categories and usage
- `references/motion-principles.md` — 12 animation principles for code
- `references/anti-slop-checklist.md` — Quality gates and banned patterns
- `references/codec-guide.md` — Output formats and quality settings

## Template Components

Reusable TSX components in `templates/components/`:
- `animated-text.tsx` — Word/character reveal animations
- `progress-bar.tsx` — Animated progress indicator
- `particle-system.tsx` — CSS particle effects with noise
- `gradient-background.tsx` — Animated gradient backgrounds
- `scene-wrapper.tsx` — Enter/exit animation wrapper
- `lower-third.tsx` — Broadcast-style name/title overlay
- `countdown-timer.tsx` — Animated number countdown
- `split-screen.tsx` — Responsive split layout

## Core Remotion Patterns Quick Reference

### Entry Point
```tsx
// src/index.ts
import { registerRoot } from 'remotion';
import { RemotionRoot } from './Root';
registerRoot(RemotionRoot);
```

### Root Composition
```tsx
// src/Root.tsx
import { Composition } from 'remotion';
import { MyVideo } from './compositions/MyVideo';

export const RemotionRoot: React.FC = () => (
  <>
    <Composition
      id="MyVideo"
      component={MyVideo}
      durationInFrames={900} // 30s @ 30fps
      fps={30}
      width={1080}
      height={1920}
      defaultProps={{ title: 'Hello World' }}
    />
  </>
);
```

### Animation Basics
```tsx
import { useCurrentFrame, interpolate, spring, useVideoConfig } from 'remotion';
import { AbsoluteFill, Sequence } from 'remotion';

export const MyScene: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Linear interpolation
  const opacity = interpolate(frame, [0, 30], [0, 1], { extrapolateRight: 'clamp' });

  // Spring animation
  const scale = spring({ frame, fps, config: { damping: 200, stiffness: 100 } });

  return (
    <AbsoluteFill style={{ opacity, transform: `scale(${scale})` }}>
      <h1>Hello World</h1>
    </AbsoluteFill>
  );
};
```

### Scene Transitions
```tsx
import { TransitionSeries, linearTiming } from '@remotion/transitions';
import { fade } from '@remotion/transitions/fade';
import { slide } from '@remotion/transitions/slide';

export const MyVideo: React.FC = () => (
  <TransitionSeries>
    <TransitionSeries.Sequence durationInFrames={90}>
      <Scene1 />
    </TransitionSeries.Sequence>
    <TransitionSeries.Transition
      presentation={fade()}
      timing={linearTiming({ durationInFrames: 15 })}
    />
    <TransitionSeries.Sequence durationInFrames={150}>
      <Scene2 />
    </TransitionSeries.Sequence>
    <TransitionSeries.Transition
      presentation={slide({ direction: 'from-right' })}
      timing={linearTiming({ durationInFrames: 15 })}
    />
    <TransitionSeries.Sequence durationInFrames={90}>
      <Scene3 />
    </TransitionSeries.Sequence>
  </TransitionSeries>
);
```

### Loading Fonts
```tsx
import { loadFont } from '@remotion/google-fonts/Inter';
import { loadFont as loadDisplay } from '@remotion/google-fonts/PlayfairDisplay';

const { fontFamily: inter } = loadFont();
const { fontFamily: playfair } = loadDisplay();
```

### Audio & Video
```tsx
import { Audio, Video, Img, staticFile } from 'remotion';

// Audio with volume curve
<Audio src={staticFile('music.mp3')} volume={(f) => interpolate(f, [0, 30], [0, 0.8], { extrapolateRight: 'clamp' })} />

// Video embedding
<Video src={staticFile('clip.mp4')} startFrom={30} endAt={150} volume={0.5} />

// Image (always use Img, not img)
<Img src={staticFile('photo.jpg')} style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
```

## Quality Gates

Before declaring a video complete, verify:
1. All animations use `useCurrentFrame()` — no CSS transitions or requestAnimationFrame
2. Scene timing adds up to total composition duration
3. Transitions don't overlap scenes incorrectly
4. Text is readable at target resolution (minimum 24px for mobile vertical)
5. Audio is properly synced (fade in/out, no abrupt cuts)
6. Colors have sufficient contrast (4.5:1 for text)
7. Safe zones respected (no text in top 150px or bottom 200px for social)
8. Fonts loaded before rendering (`loadFont()` from @remotion/google-fonts)
9. All assets use `staticFile()` or valid remote URLs
10. Output format matches platform requirements
