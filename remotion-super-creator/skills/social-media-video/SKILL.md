---
name: social-media-video
description: Create vertical short-form videos for TikTok, Instagram Reels, YouTube Shorts, and Instagram Stories. Handles platform-specific safe zones, captions, hooks, CTAs, and trending formats. Use when user wants social media video content in 9:16 vertical format.
---

# Social Media Video

Create scroll-stopping vertical videos optimized for each platform's algorithm and UI constraints.

## When to Use

- User wants a TikTok, Reel, Short, or Story
- User asks for a vertical video or short-form content
- User mentions social media video, promotional clip, or viral content
- User wants caption overlays, hook screens, or CTA endings

## Platform Specs

| Platform | Dimensions | FPS | Duration | Sweet Spot | Notes |
|---|---|---|---|---|---|
| TikTok | 1080x1920 | 30 | up to 10min | 21-34s | First 3s critical for retention |
| Instagram Reels | 1080x1920 | 30 | up to 90s | 15-30s | Cover frame at 1s mark |
| YouTube Shorts | 1080x1920 | 30 | up to 60s | 30-45s | Vertical only, loops by default |
| Instagram Stories | 1080x1920 | 30 | 15s segments | 15s | Auto-splits longer videos |
| Facebook Reels | 1080x1920 | 30 | 15-60s | 15-30s | Cross-posted from IG Reels |

All vertical. Always **1080x1920** at **30fps** unless the user specifies otherwise.

## Safe Zones (Vertical 1080x1920)

Platform UI overlays cover certain areas. Keep key content in the safe zone.

```
+------------------------------+
| ### TOP UNSAFE ###           |  0-150px: status bar, time, battery
|                              |
|  +------------------------+  |
|  |                        |  |
|  |   SAFE ZONE            |  |  150px - 1500px: place all key content here
|  |   x: 70-1010           |  |
|  |   y: 150-1500          |  |
|  |                        |  |
|  +------------------------+  |
|                          [*] |  Right 100px bottom half: like/comment/share
| ### BOTTOM UNSAFE ###        |  1500-1920px: captions, TikTok UI, Reels UI
| @handle  sound  ...         |
+------------------------------+
```

**Rules:**
- Top 150px: avoid on all platforms
- Bottom 420px: avoid critical text (TikTok captions, Reels UI)
- Right 100px in bottom half: avoid (reaction buttons)
- Left 20px + Right 20px: horizontal padding always
- Caption zone: y 1100-1400px (if using captions, place them here)

## Scene Structure Patterns

### Pattern 1: Hook -> Content -> CTA (Most Common)
```
Scene 1: Hook          -- 2-3s (60-90 frames) -- bold text + motion to stop the scroll
Scene 2: Content       -- variable            -- the main message, tips, story
Scene 3: CTA           -- 2-3s (60-90 frames) -- follow, like, link in bio
```

### Pattern 2: Listicle (3-5 Items)
```
Scene 1: Title card    -- 2s   -- "5 Things You Need to Know"
Scene 2-6: Items       -- 3-5s each -- numbered, with transition between
Scene 7: CTA           -- 2s
```

### Pattern 3: Before / After Comparison
```
Scene 1: "Before" state -- 3-5s -- show the problem
Scene 2: Transition      -- 1s  -- wipe, flash, or glitch
Scene 3: "After" state   -- 3-5s -- show the result
Scene 4: CTA             -- 2s
```

### Pattern 4: Reaction / Response
```
Scene 1: Source content  -- 3-5s -- quote, tweet, headline
Scene 2: Reaction        -- 3-5s -- response text or visual
Scene 3: CTA             -- 2s
```

## Workflow

1. Read `references/social-patterns.md` for copy-paste component patterns
2. Read `../../references/format-specs.md` for full platform details
3. Read `../../references/color-palettes.md` and `../../references/font-pairings.md`
4. Fill Video Specification:
   - Platform target (TikTok, Reels, Shorts, Stories)
   - Color palette (bg, primary, white, muted)
   - Font pairing (heading + body)
   - Scene breakdown with durations
   - Audio (music, voiceover, or none)
5. Generate scene components following the starter template
6. Register composition in `Root.tsx`
7. Preview: `npx remotion studio`
8. Render: `npx remotion render src/index.ts SocialMediaVideo out/video.mp4 --codec=h264 --crf=18`

## Complete Starter Template

```tsx
import { AbsoluteFill, Sequence, useCurrentFrame, useVideoConfig, interpolate, spring } from "remotion";
import { TransitionSeries, linearTiming } from "@remotion/transitions";
import { slide } from "@remotion/transitions/slide";
import { fade } from "@remotion/transitions/fade";
import { loadFont } from "@remotion/google-fonts/Inter";
import { loadFont as loadDisplay } from "@remotion/google-fonts/BebasNeue";

const { fontFamily: body } = loadFont();
const { fontFamily: heading } = loadDisplay();

const COLORS = { bg: "#0f0f0f", primary: "#00f5d4", white: "#ffffff", muted: "#888888" };

// -- Hook Scene --
const HookScene: React.FC<{ text: string }> = ({ text }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const scale = spring({ frame, fps, config: { damping: 12, stiffness: 200 } });
  const opacity = interpolate(frame, [0, 10], [0, 1], { extrapolateRight: "clamp" });

  return (
    <AbsoluteFill style={{ backgroundColor: COLORS.bg, justifyContent: "center", alignItems: "center" }}>
      <div
        style={{
          transform: `scale(${scale})`,
          opacity,
          color: COLORS.white,
          fontSize: 72,
          fontWeight: 900,
          fontFamily: heading,
          textAlign: "center",
          padding: "0 60px",
          lineHeight: 1.1,
        }}
      >
        {text}
      </div>
    </AbsoluteFill>
  );
};

// -- Content Scene (Listicle Item) --
const ContentScene: React.FC<{ items: string[] }> = ({ items }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  return (
    <AbsoluteFill style={{ backgroundColor: COLORS.bg, justifyContent: "center", padding: "0 60px" }}>
      {items.map((item, i) => {
        const delay = i * 15;
        const s = spring({ frame: frame - delay, fps, config: { damping: 12 } });
        const opacity = interpolate(frame - delay, [0, 10], [0, 1], {
          extrapolateLeft: "clamp",
          extrapolateRight: "clamp",
        });
        return (
          <div
            key={i}
            style={{
              transform: `translateX(${interpolate(s, [0, 1], [100, 0])}px)`,
              opacity,
              color: COLORS.white,
              fontSize: 42,
              fontWeight: 700,
              fontFamily: body,
              marginBottom: 30,
              display: "flex",
              alignItems: "center",
              gap: 20,
            }}
          >
            <span style={{ color: COLORS.primary, fontSize: 54, fontFamily: heading }}>{i + 1}.</span>
            {item}
          </div>
        );
      })}
    </AbsoluteFill>
  );
};

// -- CTA Scene --
const CTAScene: React.FC<{ handle: string }> = ({ handle }) => {
  const frame = useCurrentFrame();
  const pulse = Math.sin(frame * 0.15) * 0.05 + 1;

  return (
    <AbsoluteFill style={{ backgroundColor: COLORS.bg, justifyContent: "center", alignItems: "center" }}>
      <div style={{ textAlign: "center" }}>
        <div style={{ color: COLORS.primary, fontSize: 36, fontWeight: 700, fontFamily: body, marginBottom: 20 }}>
          Follow for more
        </div>
        <div style={{ transform: `scale(${pulse})`, color: COLORS.white, fontSize: 52, fontWeight: 900, fontFamily: heading }}>
          {handle}
        </div>
      </div>
    </AbsoluteFill>
  );
};

// -- Main Composition with Transitions --
export const SocialMediaVideo: React.FC<{
  hookText: string;
  items: string[];
  handle: string;
}> = ({ hookText, items, handle }) => (
  <TransitionSeries>
    <TransitionSeries.Sequence durationInFrames={90}>
      <HookScene text={hookText} />
    </TransitionSeries.Sequence>
    <TransitionSeries.Transition
      presentation={slide({ direction: "from-bottom" })}
      timing={linearTiming({ durationInFrames: 10 })}
    />
    <TransitionSeries.Sequence durationInFrames={450}>
      <ContentScene items={items} />
    </TransitionSeries.Sequence>
    <TransitionSeries.Transition
      presentation={fade()}
      timing={linearTiming({ durationInFrames: 15 })}
    />
    <TransitionSeries.Sequence durationInFrames={90}>
      <CTAScene handle={handle} />
    </TransitionSeries.Sequence>
  </TransitionSeries>
);
```

Register in `Root.tsx`:
```tsx
<Composition
  id="SocialMediaVideo"
  component={SocialMediaVideo}
  durationInFrames={630}
  fps={30}
  width={1080}
  height={1920}
  defaultProps={{
    hookText: "5 Tips You NEED to Know",
    items: ["First tip here", "Second tip here", "Third tip here", "Fourth tip here", "Fifth tip here"],
    handle: "@yourhandle",
  }}
/>
```

## Progress Bar Pattern

Add a thin progress bar at top or bottom to show video duration:

```tsx
const ProgressBar: React.FC<{ color?: string; height?: number; position?: "top" | "bottom" }> = ({
  color = "#00f5d4",
  height = 4,
  position = "top",
}) => {
  const frame = useCurrentFrame();
  const { durationInFrames } = useVideoConfig();
  const progress = frame / durationInFrames;

  return (
    <div
      style={{
        position: "absolute",
        [position]: 0,
        left: 0,
        width: `${progress * 100}%`,
        height,
        backgroundColor: color,
        zIndex: 100,
      }}
    />
  );
};
```

## Caption Overlay with @remotion/captions

Use `@remotion/captions` for TikTok-style word-by-word highlighting:

```tsx
import { createTikTokStyleCaptions } from "@remotion/captions";

// Generate pages from transcript with timestamps
const { pages } = createTikTokStyleCaptions({
  transcription, // from Whisper or manual timestamps
  combineTokensWithinMilliseconds: 800,
});
```

Position captions in the vertical center-bottom safe zone (y: 1100-1400px).

## Background Music Integration

```tsx
import { Audio, staticFile } from "remotion";

// In your composition:
<Audio src={staticFile("music/background.mp3")} volume={0.3} startFrom={0} />
```

Keep music volume at 0.2-0.4 when captions or voiceover are present.

## Font Recommendations

| Use Case | Font | Weight | Size Range |
|---|---|---|---|
| Hook / headline | Bebas Neue, Montserrat, Inter | 800-900 | 60-96px |
| Body text | Inter, DM Sans | 600-700 | 36-48px |
| Caption overlay | Inter, Roboto | 700-800 | 40-52px |
| Handle / watermark | Inter | 500 | 28-36px |

Always use `fontWeight: 700+` for body and `900` for headlines. Thin fonts are unreadable on mobile feeds.

## Quality Checklist

- [ ] Dimensions are 1080x1920 (9:16)
- [ ] FPS is 30
- [ ] Duration is within platform limits
- [ ] No key text in top 150px or bottom 420px
- [ ] No key text in right 100px of bottom half
- [ ] Hook scene grabs attention in first 3 seconds
- [ ] Text is legible at mobile size (font 36px+, weight 700+)
- [ ] All text has shadow or outline for readability over backgrounds
- [ ] CTA is clear and appears at the end
- [ ] Progress bar included (optional but recommended)
- [ ] Background music volume does not drown out captions
- [ ] Used `spring()` for natural motion, not linear interpolation
- [ ] All `Sequence` components have explicit `name` props
- [ ] Transitions are smooth (8-12 frames for social pacing)
- [ ] Tested at 1x, 0.5x, and 2x speed preview

## Reference Files

- `references/social-patterns.md` -- Copy-paste component patterns for hooks, CTAs, captions, split screens, and trending formats
- `../../references/format-specs.md` -- Full platform format specifications
- `../../references/color-palettes.md` -- Curated color palettes
- `../../references/font-pairings.md` -- Font pairing recommendations
- `../../references/transition-catalog.md` -- Transition effects