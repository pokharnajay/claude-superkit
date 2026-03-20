# Social Media Video -- Code Patterns

Dense, copy-paste-ready component patterns for social media videos. All assume 1080x1920 at 30fps.

---

## 1. Hook Screen Component

Big text that springs in to stop the scroll. Supports two lines with staggered timing.

```tsx
import { AbsoluteFill, useCurrentFrame, useVideoConfig, interpolate, spring } from "remotion";

const HookScreen: React.FC<{ line1: string; line2?: string; accentColor?: string }> = ({
  line1,
  line2,
  accentColor = "#00f5d4",
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const scale1 = spring({ frame, fps, config: { damping: 10, stiffness: 200 } });
  const scale2 = spring({ frame: frame - 8, fps, config: { damping: 10, stiffness: 200 } });
  const bgFlash = interpolate(frame, [0, 5, 15], [1, 0.85, 1], { extrapolateRight: "clamp" });

  return (
    <AbsoluteFill
      style={{
        backgroundColor: `rgba(15,15,15,${bgFlash})`,
        justifyContent: "center",
        alignItems: "center",
        padding: "0 60px",
      }}
    >
      <div
        style={{
          transform: `scale(${scale1})`,
          fontSize: 80,
          fontWeight: 900,
          color: "#fff",
          textAlign: "center",
          lineHeight: 1.05,
          fontFamily: "Inter, sans-serif",
        }}
      >
        {line1}
      </div>
      {line2 && (
        <div
          style={{
            transform: `scale(${scale2})`,
            fontSize: 56,
            fontWeight: 700,
            color: accentColor,
            textAlign: "center",
            marginTop: 20,
            fontFamily: "Inter, sans-serif",
          }}
        >
          {line2}
        </div>
      )}
    </AbsoluteFill>
  );
};
```

---

## 2. Text Overlay with Shadow/Outline

Readable text over any background. Supports both drop shadow and stroke outline modes.

```tsx
const TextOverlay: React.FC<{
  text: string;
  y?: number;
  fontSize?: number;
  outline?: boolean;
}> = ({ text, y = 960, fontSize = 48, outline = false }) => {
  return (
    <div
      style={{
        position: "absolute",
        top: y,
        left: 0,
        right: 0,
        textAlign: "center",
        fontSize,
        fontWeight: 800,
        fontFamily: "Inter, sans-serif",
        color: "#ffffff",
        textShadow: outline ? "none" : "0 2px 4px rgba(0,0,0,0.8), 0 4px 12px rgba(0,0,0,0.5)",
        WebkitTextStroke: outline ? "2px #000000" : "none",
        padding: "0 40px",
        lineHeight: 1.2,
      }}
    >
      {text}
    </div>
  );
};
```

---

## 3. Split Screen Comparison

Before/After or A vs B comparison with animated divider line.

```tsx
const SplitScreen: React.FC<{
  topLabel: string;
  bottomLabel: string;
  topColor: string;
  bottomColor: string;
  direction?: "vertical" | "horizontal";
}> = ({ topLabel, bottomLabel, topColor, bottomColor, direction = "vertical" }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const dividerProgress = spring({ frame, fps, config: { damping: 15 } });
  const isVertical = direction === "vertical";

  return (
    <AbsoluteFill>
      <div
        style={{
          position: "absolute",
          top: 0,
          left: 0,
          width: isVertical ? "100%" : "50%",
          height: isVertical ? "50%" : "100%",
          backgroundColor: topColor,
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
        }}
      >
        <div style={{ fontSize: 52, fontWeight: 800, color: "#fff", fontFamily: "Inter, sans-serif" }}>
          {topLabel}
        </div>
      </div>
      <div
        style={{
          position: "absolute",
          bottom: 0,
          right: 0,
          width: isVertical ? "100%" : "50%",
          height: isVertical ? "50%" : "100%",
          backgroundColor: bottomColor,
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
        }}
      >
        <div style={{ fontSize: 52, fontWeight: 800, color: "#fff", fontFamily: "Inter, sans-serif" }}>
          {bottomLabel}
        </div>
      </div>
      <div
        style={{
          position: "absolute",
          top: isVertical ? "50%" : 0,
          left: isVertical ? 0 : "50%",
          width: isVertical ? `${dividerProgress * 100}%` : 4,
          height: isVertical ? 4 : `${dividerProgress * 100}%`,
          backgroundColor: "#ffffff",
          transform: isVertical ? "translateY(-50%)" : "translateX(-50%)",
        }}
      />
    </AbsoluteFill>
  );
};
```

---

## 4. Number Counter Animation

Counts from 0 to target with ease-out cubic deceleration. Supports prefix/suffix for units.

```tsx
const NumberCounter: React.FC<{
  target: number;
  prefix?: string;
  suffix?: string;
  color?: string;
  duration?: number;
}> = ({ target, prefix = "", suffix = "", color = "#00f5d4", duration = 60 }) => {
  const frame = useCurrentFrame();
  const progress = interpolate(frame, [0, duration], [0, 1], { extrapolateRight: "clamp" });
  const eased = 1 - Math.pow(1 - progress, 3);
  const value = Math.round(eased * target);

  return (
    <div style={{ textAlign: "center" }}>
      <div
        style={{
          fontSize: 96,
          fontWeight: 900,
          color,
          fontFamily: "Inter, sans-serif",
          fontVariantNumeric: "tabular-nums",
        }}
      >
        {prefix}{value.toLocaleString()}{suffix}
      </div>
    </div>
  );
};
```

---

## 5. Progress Bar

Thin bar at top or bottom showing video progress. Place as a sibling inside AbsoluteFill.

```tsx
const ProgressBar: React.FC<{
  color?: string;
  height?: number;
  position?: "top" | "bottom";
}> = ({ color = "#00f5d4", height = 4, position = "top" }) => {
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

---

## 6. Story Progress Dots

Instagram Stories-style multi-segment progress bar at the top.

```tsx
const StoryProgressBar: React.FC<{
  totalSegments: number;
  currentSegment: number;
  segmentProgress: number;
}> = ({ totalSegments, currentSegment, segmentProgress }) => {
  const gap = 4;
  const barHeight = 3;
  const padding = 20;

  return (
    <div
      style={{
        position: "absolute",
        top: 60,
        left: padding,
        right: padding,
        display: "flex",
        gap,
        zIndex: 100,
      }}
    >
      {Array.from({ length: totalSegments }).map((_, i) => {
        let fill = 0;
        if (i < currentSegment) fill = 1;
        else if (i === currentSegment) fill = segmentProgress;

        return (
          <div
            key={i}
            style={{
              flex: 1,
              height: barHeight,
              backgroundColor: "rgba(255,255,255,0.3)",
              borderRadius: 2,
              overflow: "hidden",
            }}
          >
            <div
              style={{
                width: `${fill * 100}%`,
                height: "100%",
                backgroundColor: "#fff",
                borderRadius: 2,
              }}
            />
          </div>
        );
      })}
    </div>
  );
};
```

---

## 7. Swipe-Up Indicator

Bouncing chevron at bottom of Stories. Animated with sine wave for continuous motion.

```tsx
const SwipeUpIndicator: React.FC<{ label?: string }> = ({ label = "Swipe Up" }) => {
  const frame = useCurrentFrame();
  const bounce = Math.sin(frame * 0.2) * 10;

  return (
    <div
      style={{
        position: "absolute",
        bottom: 200,
        left: 0,
        right: 0,
        textAlign: "center",
        transform: `translateY(${bounce}px)`,
      }}
    >
      <div
        style={{
          fontSize: 40,
          color: "#fff",
          fontFamily: "Inter, sans-serif",
          fontWeight: 600,
          marginBottom: 8,
        }}
      >
        {label}
      </div>
      <svg width="40" height="24" viewBox="0 0 40 24" style={{ margin: "0 auto", display: "block" }}>
        <polyline
          points="4,20 20,4 36,20"
          fill="none"
          stroke="#fff"
          strokeWidth="4"
          strokeLinecap="round"
          strokeLinejoin="round"
        />
      </svg>
    </div>
  );
};
```

---

## 8. TikTok Caption with Word Highlighting

Current word is highlighted, surrounding words visible. Pass an array of word objects with frame timing.

```tsx
const TikTokCaption: React.FC<{
  words: { text: string; startFrame: number; endFrame: number }[];
  highlightColor?: string;
}> = ({ words, highlightColor = "#00f5d4" }) => {
  const frame = useCurrentFrame();

  return (
    <div
      style={{
        position: "absolute",
        bottom: 500,
        left: 40,
        right: 40,
        textAlign: "center",
        display: "flex",
        flexWrap: "wrap",
        justifyContent: "center",
        gap: "8px 12px",
      }}
    >
      {words.map((word, i) => {
        const isActive = frame >= word.startFrame && frame < word.endFrame;
        const isPast = frame >= word.endFrame;
        return (
          <span
            key={i}
            style={{
              fontSize: 48,
              fontWeight: 800,
              fontFamily: "Inter, sans-serif",
              color: isActive ? highlightColor : isPast ? "#ffffff" : "rgba(255,255,255,0.5)",
              textShadow: "0 2px 8px rgba(0,0,0,0.8)",
              transform: isActive ? "scale(1.15)" : "scale(1)",
              display: "inline-block",
            }}
          >
            {word.text}
          </span>
        );
      })}
    </div>
  );
};
```

---

## 9. Floating Emoji Animation

Emojis float up from bottom like live reactions. Deterministic positions from index for consistent renders.

```tsx
const FloatingEmojis: React.FC<{ emojis?: string[]; count?: number }> = ({
  emojis = ["\u{1F525}", "\u{2764}\u{FE0F}", "\u{1F602}", "\u{1F389}", "\u{1F4AF}"],
  count = 8,
}) => {
  const frame = useCurrentFrame();

  const items = Array.from({ length: count }).map((_, i) => {
    const seed = (i * 137.508) % 1;
    const x = 100 + seed * 880;
    const startFrame = i * 8;
    const speed = 2 + (i % 3);
    const emoji = emojis[i % emojis.length];
    const y = 1920 - (frame - startFrame) * speed;
    const opacity = interpolate(y, [200, 400, 1600, 1920], [0, 1, 1, 0], {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
    });
    const wobble = Math.sin((frame - startFrame) * 0.1 + i) * 20;
    return { emoji, x: x + wobble, y, opacity, visible: frame >= startFrame };
  });

  return (
    <>
      {items
        .filter((it) => it.visible && it.opacity > 0)
        .map((it, i) => (
          <div
            key={i}
            style={{ position: "absolute", left: it.x, top: it.y, fontSize: 48, opacity: it.opacity }}
          >
            {it.emoji}
          </div>
        ))}
    </>
  );
};
```

---

## 10. Username/Handle Lower Third

Animated lower third with accent bar and staggered name/handle reveal.

```tsx
const LowerThird: React.FC<{ name: string; handle: string }> = ({ name, handle }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const slideIn = spring({ frame, fps, config: { damping: 15 } });
  const barWidth = interpolate(slideIn, [0, 1], [0, 400]);

  return (
    <div style={{ position: "absolute", bottom: 480, left: 40, zIndex: 50 }}>
      <div
        style={{
          width: barWidth,
          height: 3,
          backgroundColor: "#00f5d4",
          marginBottom: 12,
          borderRadius: 2,
        }}
      />
      <div
        style={{
          transform: `translateX(${interpolate(slideIn, [0, 1], [-200, 0])}px)`,
          opacity: slideIn,
        }}
      >
        <div style={{ fontSize: 36, fontWeight: 800, color: "#fff", fontFamily: "Inter, sans-serif" }}>
          {name}
        </div>
        <div
          style={{
            fontSize: 26,
            fontWeight: 500,
            color: "rgba(255,255,255,0.6)",
            fontFamily: "Inter, sans-serif",
            marginTop: 4,
          }}
        >
          {handle}
        </div>
      </div>
    </div>
  );
};
```

---

## 11. End Screen CTA

Follow / Like / Share buttons with staggered spring animation.

```tsx
const EndScreenCTA: React.FC<{ actions?: string[]; accentColor?: string }> = ({
  actions = ["Follow", "Like", "Share"],
  accentColor = "#00f5d4",
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  return (
    <AbsoluteFill
      style={{ backgroundColor: "#0f0f0f", justifyContent: "center", alignItems: "center", gap: 30 }}
    >
      <div
        style={{
          fontSize: 48,
          fontWeight: 900,
          color: "#fff",
          fontFamily: "Inter, sans-serif",
          marginBottom: 40,
        }}
      >
        Don't forget to...
      </div>
      {actions.map((action, i) => {
        const s = spring({ frame: frame - i * 10, fps, config: { damping: 12 } });
        return (
          <div
            key={i}
            style={{
              transform: `scale(${s})`,
              backgroundColor: accentColor,
              color: "#0f0f0f",
              fontSize: 36,
              fontWeight: 800,
              fontFamily: "Inter, sans-serif",
              padding: "16px 48px",
              borderRadius: 50,
            }}
          >
            {action}
          </div>
        );
      })}
    </AbsoluteFill>
  );
};
```

---

## 12. Background with Subtle Motion

Gradient that slowly rotates over the video duration. Use as first child in AbsoluteFill.

```tsx
const AnimatedGradientBG: React.FC<{ colors?: [string, string, string] }> = ({
  colors = ["#0f0f0f", "#1a1a2e", "#16213e"],
}) => {
  const frame = useCurrentFrame();
  const angle = interpolate(frame, [0, 900], [135, 225]);

  return (
    <AbsoluteFill
      style={{
        background: `linear-gradient(${angle}deg, ${colors[0]}, ${colors[1]}, ${colors[2]})`,
      }}
    />
  );
};
```

### Particle Drift Background

Floating dots that drift slowly for organic texture.

```tsx
const ParticleDrift: React.FC<{ count?: number; color?: string }> = ({
  count = 20,
  color = "rgba(255,255,255,0.08)",
}) => {
  const frame = useCurrentFrame();

  const particles = Array.from({ length: count }).map((_, i) => {
    const seed1 = ((i * 73.137) % 1);
    const seed2 = ((i * 41.269) % 1);
    const baseX = seed1 * 1080;
    const baseY = seed2 * 1920;
    const radius = 3 + (i % 5) * 2;
    const speed = 0.3 + (i % 4) * 0.15;
    const x = baseX + Math.sin(frame * speed * 0.02 + i) * 40;
    const y = baseY + Math.cos(frame * speed * 0.015 + i * 2) * 30;

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

---

## Listicle Scene Pattern

Numbered items that slide in one at a time, showing current item with counter.

```tsx
const ListicleScene: React.FC<{
  title: string;
  items: string[];
  secondsPerItem?: number;
}> = ({ title, items, secondsPerItem = 4 }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const framesPerItem = secondsPerItem * fps;
  const currentIndex = Math.min(Math.floor(frame / framesPerItem), items.length - 1);
  const itemFrame = frame - currentIndex * framesPerItem;

  const slideIn = spring({ frame: itemFrame, fps, config: { damping: 14 } });
  const opacity = interpolate(itemFrame, [0, 8], [0, 1], { extrapolateRight: "clamp" });

  return (
    <AbsoluteFill
      style={{ backgroundColor: "#0f0f0f", justifyContent: "center", alignItems: "center", padding: "0 60px" }}
    >
      <div
        style={{
          position: "absolute",
          top: 200,
          fontSize: 40,
          fontWeight: 700,
          color: "rgba(255,255,255,0.6)",
          fontFamily: "Inter, sans-serif",
          textAlign: "center",
          padding: "0 40px",
        }}
      >
        {title}
      </div>
      <div
        style={{
          transform: `translateY(${interpolate(slideIn, [0, 1], [80, 0])}px)`,
          opacity,
          textAlign: "center",
        }}
      >
        <div
          style={{
            fontSize: 120,
            fontWeight: 900,
            color: "#00f5d4",
            fontFamily: "Inter, sans-serif",
            marginBottom: 20,
          }}
        >
          {currentIndex + 1}
        </div>
        <div
          style={{
            fontSize: 52,
            fontWeight: 800,
            color: "#fff",
            fontFamily: "Inter, sans-serif",
            lineHeight: 1.2,
          }}
        >
          {items[currentIndex]}
        </div>
      </div>
      <div
        style={{
          position: "absolute",
          bottom: 500,
          fontSize: 28,
          color: "rgba(255,255,255,0.4)",
          fontFamily: "Inter, sans-serif",
        }}
      >
        {currentIndex + 1} / {items.length}
      </div>
    </AbsoluteFill>
  );
};
```
