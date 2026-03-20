# Kinetic Typography -- Code Patterns

Copy-paste-ready text animation components. All use Remotion primitives.

---

## 1. Word-by-Word Reveal (Staggered Spring)

Each word fades and slides in with a spring delay. The core pattern for kinetic text.

```tsx
import { useCurrentFrame, useVideoConfig, interpolate, spring } from "remotion";

const WordByWordReveal: React.FC<{
  text: string;
  fontSize?: number;
  color?: string;
  fontFamily?: string;
  delayPerWord?: number;
  startDelay?: number;
}> = ({ text, fontSize = 64, color = "#fff", fontFamily = "Inter, sans-serif", delayPerWord = 6, startDelay = 0 }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const words = text.split(" ");

  return (
    <div style={{ display: "flex", flexWrap: "wrap", justifyContent: "center", gap: "0 16px", padding: "0 60px" }}>
      {words.map((word, i) => {
        const delay = startDelay + i * delayPerWord;
        const s = spring({ frame: frame - delay, fps, config: { damping: 12, stiffness: 180 } });
        const translateY = interpolate(s, [0, 1], [30, 0]);
        return (
          <span
            key={i}
            style={{
              display: "inline-block",
              fontSize,
              fontWeight: 700,
              fontFamily,
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
```

---

## 2. Character Cascade

Each letter drops in one by one with staggered timing.

```tsx
const CharacterCascade: React.FC<{
  text: string;
  fontSize?: number;
  color?: string;
  delayPerChar?: number;
}> = ({ text, fontSize = 80, color = "#fff", delayPerChar = 2 }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  return (
    <div style={{ display: "flex", justifyContent: "center", flexWrap: "wrap" }}>
      {text.split("").map((char, i) => {
        const delay = i * delayPerChar;
        const s = spring({ frame: frame - delay, fps, config: { damping: 10, stiffness: 200 } });
        const translateY = interpolate(s, [0, 1], [-60, 0]);
        const rotation = interpolate(s, [0, 1], [-15, 0]);

        return (
          <span
            key={i}
            style={{
              display: "inline-block",
              fontSize,
              fontWeight: 900,
              fontFamily: "Inter, sans-serif",
              color,
              opacity: s,
              transform: `translateY(${translateY}px) rotate(${rotation}deg)`,
              whiteSpace: char === " " ? "pre" : "normal",
              minWidth: char === " " ? "0.3em" : undefined,
            }}
          >
            {char}
          </span>
        );
      })}
    </div>
  );
};
```

---

## 3. Typewriter with Blinking Cursor

Characters appear sequentially with a blinking block cursor.

```tsx
const Typewriter: React.FC<{
  text: string;
  fontSize?: number;
  color?: string;
  cursorColor?: string;
  framesPerChar?: number;
}> = ({ text, fontSize = 48, color = "#fff", cursorColor = "#00f5d4", framesPerChar = 2 }) => {
  const frame = useCurrentFrame();
  const charsVisible = Math.min(Math.floor(frame / framesPerChar), text.length);
  const visibleText = text.slice(0, charsVisible);
  const cursorOpacity = Math.sin(frame * 0.3) > 0 ? 1 : 0;
  const isDone = charsVisible >= text.length;

  return (
    <div style={{ textAlign: "center", padding: "0 60px" }}>
      <span
        style={{
          fontSize,
          fontWeight: 600,
          fontFamily: "'Courier New', monospace",
          color,
          lineHeight: 1.4,
        }}
      >
        {visibleText}
      </span>
      <span
        style={{
          display: "inline-block",
          width: fontSize * 0.55,
          height: fontSize * 0.85,
          backgroundColor: isDone ? "transparent" : cursorColor,
          opacity: isDone ? 0 : cursorOpacity,
          marginLeft: 2,
          verticalAlign: "text-bottom",
        }}
      />
    </div>
  );
};
```

---

## 4. Word Highlight Wipe

Active word gets a colored background wipe. Great for lyric videos and read-along text.

```tsx
const WordHighlight: React.FC<{
  words: { text: string; startFrame: number; endFrame: number }[];
  fontSize?: number;
  highlightColor?: string;
}> = ({ words, fontSize = 56, highlightColor = "#f4a261" }) => {
  const frame = useCurrentFrame();

  return (
    <div
      style={{
        display: "flex",
        flexWrap: "wrap",
        justifyContent: "center",
        gap: "8px 14px",
        padding: "0 60px",
      }}
    >
      {words.map((word, i) => {
        const isActive = frame >= word.startFrame && frame < word.endFrame;
        const progress = isActive
          ? interpolate(frame, [word.startFrame, word.endFrame], [0, 100], { extrapolateRight: "clamp" })
          : frame >= word.endFrame
          ? 100
          : 0;

        return (
          <span
            key={i}
            style={{
              display: "inline-block",
              fontSize,
              fontWeight: 800,
              fontFamily: "Inter, sans-serif",
              color: "#fff",
              position: "relative",
              padding: "4px 8px",
            }}
          >
            <span
              style={{
                position: "absolute",
                left: 0,
                top: 0,
                height: "100%",
                width: `${progress}%`,
                backgroundColor: highlightColor,
                opacity: 0.3,
                borderRadius: 4,
                zIndex: -1,
              }}
            />
            {word.text}
          </span>
        );
      })}
    </div>
  );
};
```

---

## 5. Text Scale Emphasis

Current word pops up in size while others stay small. Cycles through words based on timing.

```tsx
const ScaleEmphasis: React.FC<{
  words: string[];
  framesPerWord?: number;
  baseSize?: number;
  emphasisSize?: number;
  emphasisColor?: string;
}> = ({ words, framesPerWord = 20, baseSize = 40, emphasisSize = 96, emphasisColor = "#f4a261" }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const currentIndex = Math.min(Math.floor(frame / framesPerWord), words.length - 1);
  const wordFrame = frame - currentIndex * framesPerWord;

  return (
    <div
      style={{
        display: "flex",
        flexWrap: "wrap",
        justifyContent: "center",
        alignItems: "baseline",
        gap: "8px 16px",
        padding: "0 40px",
      }}
    >
      {words.map((word, i) => {
        const isActive = i === currentIndex;
        const s = isActive
          ? spring({ frame: wordFrame, fps, config: { damping: 10, stiffness: 200 } })
          : 1;
        const size = isActive ? interpolate(s, [0, 1], [baseSize, emphasisSize]) : baseSize;
        const color = isActive ? emphasisColor : "rgba(255,255,255,0.5)";

        return (
          <span
            key={i}
            style={{
              display: "inline-block",
              fontSize: size,
              fontWeight: isActive ? 900 : 600,
              fontFamily: "Inter, sans-serif",
              color,
              lineHeight: 1.2,
            }}
          >
            {word}
          </span>
        );
      })}
    </div>
  );
};
```

---

## 6. Line-by-Line Build with Fade

Lines appear one at a time, building up a full block of text.

```tsx
const LineByLineBuild: React.FC<{
  lines: string[];
  framesPerLine?: number;
  fontSize?: number;
}> = ({ lines, framesPerLine = 20, fontSize = 44 }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  return (
    <div style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: 16, padding: "0 60px" }}>
      {lines.map((line, i) => {
        const lineStart = i * framesPerLine;
        const lineFrame = frame - lineStart;
        const s = spring({ frame: lineFrame, fps, config: { damping: 14 } });
        const translateX = interpolate(s, [0, 1], [-60, 0]);

        if (frame < lineStart) return null;

        return (
          <div
            key={i}
            style={{
              fontSize,
              fontWeight: 700,
              fontFamily: "Inter, sans-serif",
              color: "#fff",
              opacity: s,
              transform: `translateX(${translateX}px)`,
              textAlign: "center",
              lineHeight: 1.3,
            }}
          >
            {line}
          </div>
        );
      })}
    </div>
  );
};
```

---

## 7. Bounce-In Text with Overshoot

Words bounce in with spring overshoot for playful energy.

```tsx
const BounceInText: React.FC<{
  words: string[];
  fontSize?: number;
  delayPerWord?: number;
}> = ({ words, fontSize = 64, delayPerWord = 8 }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  return (
    <div style={{ display: "flex", flexWrap: "wrap", justifyContent: "center", gap: "0 16px", padding: "0 50px" }}>
      {words.map((word, i) => {
        const delay = i * delayPerWord;
        // Low damping = more bounce/overshoot
        const s = spring({ frame: frame - delay, fps, config: { damping: 6, stiffness: 200, mass: 0.8 } });
        const translateY = interpolate(s, [0, 1], [100, 0]);
        const rotation = interpolate(s, [0, 0.5, 1], [10, -3, 0]);

        return (
          <span
            key={i}
            style={{
              display: "inline-block",
              fontSize,
              fontWeight: 900,
              fontFamily: "Inter, sans-serif",
              color: "#fff",
              opacity: Math.min(s * 2, 1),
              transform: `translateY(${translateY}px) rotate(${rotation}deg)`,
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
```

---

## 8. Rotating Word Carousel

Cycles through a list of words in one position. Each word fades in, holds, fades out.

```tsx
const RotatingWordCarousel: React.FC<{
  words: string[];
  framesPerWord?: number;
  fontSize?: number;
  color?: string;
}> = ({ words, framesPerWord = 40, fontSize = 80, color = "#f4a261" }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const totalFrames = words.length * framesPerWord;
  const loopFrame = frame % totalFrames;
  const currentIndex = Math.floor(loopFrame / framesPerWord);
  const wordFrame = loopFrame - currentIndex * framesPerWord;

  const fadeIn = interpolate(wordFrame, [0, 8], [0, 1], { extrapolateRight: "clamp" });
  const fadeOut = interpolate(wordFrame, [framesPerWord - 8, framesPerWord], [1, 0], { extrapolateLeft: "clamp" });
  const opacity = Math.min(fadeIn, fadeOut);
  const translateY = interpolate(wordFrame, [0, 8, framesPerWord - 8, framesPerWord], [20, 0, 0, -20], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  return (
    <div style={{ textAlign: "center" }}>
      <div
        style={{
          fontSize,
          fontWeight: 900,
          fontFamily: "Inter, sans-serif",
          color,
          opacity,
          transform: `translateY(${translateY}px)`,
        }}
      >
        {words[currentIndex]}
      </div>
    </div>
  );
};
```

---

## 9. Gravity Text (Words Fall and Stack)

Words fall from off-screen and stack vertically with spring physics.

```tsx
const GravityText: React.FC<{
  words: string[];
  fontSize?: number;
  delayPerWord?: number;
}> = ({ words, fontSize = 56, delayPerWord = 12 }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  return (
    <div style={{ display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", height: "100%", gap: 8 }}>
      {words.map((word, i) => {
        const delay = i * delayPerWord;
        const s = spring({ frame: frame - delay, fps, config: { damping: 8, stiffness: 120 } });
        const translateY = interpolate(s, [0, 1], [-400, 0]);

        if (frame < delay) return null;

        return (
          <div
            key={i}
            style={{
              fontSize,
              fontWeight: 900,
              fontFamily: "Inter, sans-serif",
              color: "#fff",
              transform: `translateY(${translateY}px)`,
              opacity: Math.min(s * 3, 1),
              textAlign: "center",
            }}
          >
            {word}
          </div>
        );
      })}
    </div>
  );
};
```

---

## 10. Outline-to-Fill Animation

Text starts as outline stroke and fills in with color.

```tsx
const OutlineToFill: React.FC<{
  text: string;
  fontSize?: number;
  fillColor?: string;
  strokeColor?: string;
  delay?: number;
  duration?: number;
}> = ({ text, fontSize = 96, fillColor = "#fff", strokeColor = "#fff", delay = 0, duration = 30 }) => {
  const frame = useCurrentFrame();
  const progress = interpolate(frame - delay, [0, duration], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  return (
    <div style={{ textAlign: "center", position: "relative" }}>
      {/* Outline layer (fades out) */}
      <div
        style={{
          fontSize,
          fontWeight: 900,
          fontFamily: "Inter, sans-serif",
          color: "transparent",
          WebkitTextStroke: `2px ${strokeColor}`,
          opacity: 1 - progress,
          position: "absolute",
          left: 0,
          right: 0,
        }}
      >
        {text}
      </div>
      {/* Fill layer (fades in) */}
      <div
        style={{
          fontSize,
          fontWeight: 900,
          fontFamily: "Inter, sans-serif",
          color: fillColor,
          opacity: progress,
        }}
      >
        {text}
      </div>
    </div>
  );
};
```

---

## 11. Lyric Sync Pattern (Timestamps to Sequences)

Map an array of lyric lines with millisecond timestamps to Remotion Sequences.

```tsx
import { AbsoluteFill, Sequence, useVideoConfig } from "remotion";

interface LyricLine {
  text: string;
  startMs: number;
  endMs: number;
}

const LyricSync: React.FC<{ lyrics: LyricLine[] }> = ({ lyrics }) => {
  const { fps } = useVideoConfig();

  return (
    <AbsoluteFill style={{ backgroundColor: "#0a0a0a" }}>
      {lyrics.map((line, i) => {
        const startFrame = Math.round((line.startMs / 1000) * fps);
        const endFrame = Math.round((line.endMs / 1000) * fps);
        const duration = endFrame - startFrame;

        return (
          <Sequence key={i} from={startFrame} durationInFrames={duration} name={`Lyric-${i}`}>
            <AbsoluteFill style={{ justifyContent: "center", alignItems: "center", padding: "0 60px" }}>
              <WordByWordReveal text={line.text} fontSize={56} delayPerWord={4} />
            </AbsoluteFill>
          </Sequence>
        );
      })}
    </AbsoluteFill>
  );
};
```

---

## 12. Background: Noise Field

Organic texture using `@remotion/noise` for subtle position offsets on a grid of dots.

```tsx
import { AbsoluteFill, useCurrentFrame } from "remotion";
import { noise2D } from "@remotion/noise";

const NoiseField: React.FC<{ cols?: number; rows?: number; color?: string }> = ({
  cols = 20,
  rows = 35,
  color = "rgba(255,255,255,0.06)",
}) => {
  const frame = useCurrentFrame();
  const cellW = 1080 / cols;
  const cellH = 1920 / rows;

  const dots = [];
  for (let r = 0; r < rows; r++) {
    for (let c = 0; c < cols; c++) {
      const baseX = c * cellW + cellW / 2;
      const baseY = r * cellH + cellH / 2;
      const offsetX = noise2D("x", c * 0.1, frame * 0.008 + r * 0.1) * 15;
      const offsetY = noise2D("y", r * 0.1, frame * 0.008 + c * 0.1) * 15;
      dots.push({ x: baseX + offsetX, y: baseY + offsetY });
    }
  }

  return (
    <AbsoluteFill>
      {dots.map((d, i) => (
        <div
          key={i}
          style={{
            position: "absolute",
            left: d.x,
            top: d.y,
            width: 3,
            height: 3,
            borderRadius: "50%",
            backgroundColor: color,
          }}
        />
      ))}
    </AbsoluteFill>
  );
};
```

---

## 13. Background: Gradient Rotation

Slow hue shift over time using HSL interpolation. Subtle and non-distracting.

```tsx
const GradientRotation: React.FC<{ baseHue?: number; saturation?: number; lightness?: number }> = ({
  baseHue = 220,
  saturation = 30,
  lightness = 10,
}) => {
  const frame = useCurrentFrame();
  const hue = baseHue + interpolate(frame, [0, 600], [0, 40]);

  return (
    <AbsoluteFill
      style={{
        background: `radial-gradient(ellipse at 50% 40%, hsl(${hue}, ${saturation}%, ${lightness + 5}%) 0%, hsl(${hue + 20}, ${saturation}%, ${lightness}%) 70%)`,
      }}
    />
  );
};
```

---

## 14. Background: Floating Particles

Deterministic floating dots with sine/cosine movement.

```tsx
const FloatingParticles: React.FC<{ count?: number; color?: string }> = ({
  count = 25,
  color = "rgba(255,255,255,0.05)",
}) => {
  const frame = useCurrentFrame();

  const particles = Array.from({ length: count }).map((_, i) => {
    const seed1 = (i * 73.137) % 1;
    const seed2 = (i * 41.269) % 1;
    const baseX = seed1 * 1080;
    const baseY = seed2 * 1920;
    const radius = 2 + (i % 4) * 2;
    const speed = 0.2 + (i % 5) * 0.1;
    const x = baseX + Math.sin(frame * speed * 0.02 + i) * 30;
    const y = baseY + Math.cos(frame * speed * 0.015 + i * 2) * 25;
    return { x, y, radius };
  });

  return (
    <AbsoluteFill>
      {particles.map((p, i) => (
        <div
          key={i}
          style={{
            position: "absolute",
            left: p.x,
            top: p.y,
            width: p.radius * 2,
            height: p.radius * 2,
            borderRadius: "50%",
            backgroundColor: color,
          }}
        />
      ))}
    </AbsoluteFill>
  );
};
```
