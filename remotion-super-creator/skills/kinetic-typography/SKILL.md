---
name: kinetic-typography
description: Create text-driven motion graphics, kinetic typography videos, lyric videos, and quote animations. Use when the primary visual element is animated text and the user wants words to move, reveal, or transform as the main content.
---

# Kinetic Typography

Text as the star -- animated text drives the entire visual experience. Every word is choreographed with motion.

## When to Use

- User wants a quote or inspiration video
- User asks for a lyric video synced to music
- User wants text animation, word art, or title sequences
- User describes a speech visualization or text story
- User wants kinetic text, animated words, or text motion graphics

## Common Formats

| Format | Description | Typical Duration |
|---|---|---|
| Quote video | Single quote with word-by-word reveal | 8-15s |
| Lyric video | Song lyrics synced to audio timestamps | Full song |
| Speech visualization | Spoken word text appearing in rhythm | 30-120s |
| Text story / narrative | Multi-scene text-driven narrative | 30-90s |
| Title sequence | Stylized intro with animated typography | 5-15s |
| Word art / poster | Artistic text composition with motion | 5-10s |

## Text Animation Taxonomy

| Animation | Description | Timing | Best For |
|---|---|---|---|
| Word-by-word | Each word fades/slides in sequentially | 6-10 frames/word | Quotes, narration |
| Character cascade | Letters drop in one by one | 2-3 frames/char | Titles, dramatic text |
| Typewriter | Characters appear with blinking cursor | 2 frames/char | Technical, retro |
| Line-by-line | Full lines appear with fade/slide | 15-20 frames/line | Lists, bullet points |
| Word highlight | Current word gets color/scale emphasis | Continuous | Lyric videos |
| Scale emphasis | Active word scales up, others stay small | 8-12 frames | Key points, quotes |
| Bounce in | Words bounce with spring physics overshoot | 15-20 frames/word | Playful, energetic |
| Split/scatter | Words split apart and reform | 20-30 frames | Transitions, drama |
| Rotating carousel | Words cycle through a position | 30-45 frames/word | Lists of items |
| Gravity fall | Words fall from top and stack | 10-15 frames/word | Impactful, weighty |

## Design Strategy

- **1-2 font families max** (display + sans-serif body)
- **High contrast** colors (white on dark, or dark on light)
- **Center-weighted** composition (text in middle 60% of frame)
- **Varied text sizes** for hierarchy (hero word 96-140px, supporting 36-48px)
- **Background motion** keeps visual interest (gradient shift, particles, noise)
- **Rhythm matters** -- text timing should feel musical even without audio
- **Whitespace is intentional** -- let text breathe between reveals

## Workflow

1. Read `references/kinetic-patterns.md` for animation components
2. Read `../../references/font-pairings.md` for typography choices
3. Read `../../references/color-palettes.md` for palette selection
4. Break text into segments: words, lines, or phrases
5. Choose animation style per segment from the taxonomy above
6. Map timing: assign frame ranges for each text element
7. Build scene components using patterns from references
8. Add background motion (gradient, noise, particles)
9. Register composition and render

## Starter Template (Quote Animation)

```tsx
import { AbsoluteFill, useCurrentFrame, useVideoConfig, interpolate, spring, Sequence } from "remotion";
import { loadFont } from "@remotion/google-fonts/Playfair_Display";
import { loadFont as loadBody } from "@remotion/google-fonts/Inter";

const { fontFamily: display } = loadFont();
const { fontFamily: body } = loadBody();

const COLORS = { bg: "#0a0a0a", fg: "#ffffff", accent: "#f4a261", muted: "#666666" };

// Word-by-word reveal with staggered spring
const WordReveal: React.FC<{ text: string; startDelay?: number; fontSize?: number; color?: string }> = ({
  text,
  startDelay = 0,
  fontSize = 64,
  color = COLORS.fg,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const words = text.split(" ");

  return (
    <div
      style={{
        display: "flex",
        flexWrap: "wrap",
        justifyContent: "center",
        gap: "0 18px",
        padding: "0 60px",
      }}
    >
      {words.map((word, i) => {
        const delay = startDelay + i * 6;
        const s = spring({ frame: frame - delay, fps, config: { damping: 12, stiffness: 180 } });
        const translateY = interpolate(s, [0, 1], [40, 0]);
        return (
          <span
            key={i}
            style={{
              display: "inline-block",
              fontSize,
              fontWeight: 700,
              fontFamily: display,
              color,
              opacity: s,
              transform: `translateY(${translateY}px)`,
              lineHeight: 1.3,
            }}
          >
            {word}
          </span>
        );
      })}
    </div>
  );
};

// Emphasis word with scale pop
const EmphasisWord: React.FC<{ word: string; delay?: number }> = ({ word, delay = 0 }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const s = spring({ frame: frame - delay, fps, config: { damping: 8, stiffness: 200, mass: 0.5 } });

  return (
    <div
      style={{
        fontSize: 120,
        fontWeight: 900,
        fontFamily: display,
        color: COLORS.accent,
        textAlign: "center",
        transform: `scale(${s})`,
        opacity: s,
      }}
    >
      {word}
    </div>
  );
};

// Animated gradient background
const GradientBG: React.FC = () => {
  const frame = useCurrentFrame();
  const hue = interpolate(frame, [0, 300], [220, 260]);
  return (
    <AbsoluteFill
      style={{
        background: `radial-gradient(ellipse at 50% 50%, hsl(${hue}, 30%, 12%) 0%, ${COLORS.bg} 70%)`,
      }}
    />
  );
};

// Main Composition
export const QuoteVideo: React.FC<{ quote: string; author: string; emphasisWord: string }> = ({
  quote,
  author,
  emphasisWord,
}) => {
  return (
    <AbsoluteFill>
      <GradientBG />
      <AbsoluteFill style={{ justifyContent: "center", alignItems: "center" }}>
        <Sequence from={0} durationInFrames={120} name="Quote">
          <AbsoluteFill style={{ justifyContent: "center", alignItems: "center" }}>
            <WordReveal text={quote} fontSize={56} />
          </AbsoluteFill>
        </Sequence>
        <Sequence from={120} durationInFrames={60} name="Emphasis">
          <AbsoluteFill style={{ justifyContent: "center", alignItems: "center" }}>
            <EmphasisWord word={emphasisWord} />
          </AbsoluteFill>
        </Sequence>
        <Sequence from={180} durationInFrames={90} name="Attribution">
          <AbsoluteFill style={{ justifyContent: "center", alignItems: "center" }}>
            <WordReveal text={quote} fontSize={48} />
            <div
              style={{
                marginTop: 40,
                fontSize: 32,
                fontWeight: 400,
                fontFamily: body,
                color: COLORS.muted,
                textAlign: "center",
              }}
            >
              -- {author}
            </div>
          </AbsoluteFill>
        </Sequence>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
```

Register in `Root.tsx`:
```tsx
<Composition
  id="QuoteVideo"
  component={QuoteVideo}
  durationInFrames={270}
  fps={30}
  width={1080}
  height={1920}
  defaultProps={{
    quote: "The only way to do great work is to love what you do",
    author: "Steve Jobs",
    emphasisWord: "LOVE",
  }}
/>
```

## Audio Sync for Lyric Videos

Map timestamps to Sequences for lyric sync:

```tsx
interface LyricLine {
  text: string;
  startMs: number;
  endMs: number;
}

const LyricVideo: React.FC<{ lyrics: LyricLine[] }> = ({ lyrics }) => {
  const { fps } = useVideoConfig();

  return (
    <AbsoluteFill style={{ backgroundColor: "#0a0a0a" }}>
      {lyrics.map((line, i) => {
        const startFrame = Math.round((line.startMs / 1000) * fps);
        const endFrame = Math.round((line.endMs / 1000) * fps);
        const duration = endFrame - startFrame;

        return (
          <Sequence key={i} from={startFrame} durationInFrames={duration} name={`Line-${i}`}>
            <AbsoluteFill style={{ justifyContent: "center", alignItems: "center" }}>
              <WordReveal text={line.text} fontSize={60} />
            </AbsoluteFill>
          </Sequence>
        );
      })}
    </AbsoluteFill>
  );
};
```

## Background Patterns

### Gradient Rotation
Subtle hue shift over time for visual interest without distraction.

### Noise Field
Use `@remotion/noise` for organic texture:
```tsx
import { noise2D } from "@remotion/noise";
// Use noise2D("seed", x * 0.01, frame * 0.01) for position offsets
```

### Particle Drift
Floating dots with sine/cosine motion (see references).

### Radial Pulse
Subtle expansion from center:
```tsx
const scale = 1 + Math.sin(frame * 0.03) * 0.05;
// Apply to a radial gradient background
```

## Quality Checklist

- [ ] Text is the primary visual element (not backgrounds or images)
- [ ] Animation timing feels rhythmic and intentional
- [ ] No more than 2 font families used
- [ ] High contrast between text and background
- [ ] Key words have emphasis (scale, color, or weight)
- [ ] Text is centered and well-padded (60px+ sides)
- [ ] Spring animations used (not linear interpolation)
- [ ] Background has subtle motion (not static)
- [ ] If lyric video: audio and text are synced
- [ ] Text readable at target platform size (40px+ for mobile)
- [ ] Whitespace between text reveals (let it breathe)

## Reference Files

- `references/kinetic-patterns.md` -- All text animation component patterns
- `../../references/font-pairings.md` -- Typography selections
- `../../references/color-palettes.md` -- Color palette options
- `../../references/easing-library.md` -- Easing and spring configurations
- `../../references/motion-principles.md` -- Animation principles
