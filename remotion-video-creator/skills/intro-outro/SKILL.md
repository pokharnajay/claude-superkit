---
name: intro-outro
description: Create logo animations, channel intros, subscribe CTAs, end screens, and stinger transitions. Use for branding elements at the start or end of videos.
---

# Intro / Outro

Branding elements — logo reveals, channel intros, subscribe CTAs, end screens, and stingers.

## When to Use

- User wants a logo animation or logo reveal
- User asks for a channel intro or branded opening
- User wants an end screen, outro, or subscribe CTA
- User needs a stinger or bumper transition between segments
- User wants a lower third for speaker identification

## Types

| Type | Duration | Purpose |
|------|----------|---------|
| Logo reveal | 3-5s | Brand identity, channel intro |
| Channel intro | 5-8s | Logo + tagline + mood setting |
| End screen | 5-15s | CTA, subscribe, social links |
| Stinger/bumper | 1-3s | Short transition between segments |
| Lower third | 3-5s | Name/title overlay during content |
| Title card | 3-5s | Episode/video title display |

## Logo Reveal Animations

| Animation | Description | Best For |
|-----------|-------------|----------|
| Fade + Scale | Simple spring-in reveal | Corporate, minimal |
| SVG Path Draw | Lines draw to form logo | Tech, creative |
| Particle Assembly | Dots converge to form shape | Dynamic, modern |
| Glitch Reveal | Digital distortion effect | Tech, gaming |
| Letter-by-letter | Text logo types out | Text-based brands |
| Slide + Bounce | Logo slides in with spring | Playful, energetic |
| Circular Reveal | Expanding circle mask | Cinematic, dramatic |

## Sound Design

- Short stinger/jingle aligned to the logo reveal keyframe
- Whoosh or impact SFX at the moment the logo is fully visible
- Musical sting for end screen transitions
- Keep total audio under the visual duration

## Complete Starter Template — Logo Reveal

```tsx
import {
  AbsoluteFill,
  Img,
  Sequence,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
  interpolate,
  spring,
  Audio,
} from "remotion";

// -- Logo Reveal --
const LogoReveal: React.FC<{
  logoSrc: string;
  tagline?: string;
  bgColor?: string;
  accentColor?: string;
}> = ({ logoSrc, tagline, bgColor = "#0f0f0f", accentColor = "#00f5d4" }) => {
  const frame = useCurrentFrame();
  const { fps, width, height } = useVideoConfig();

  // Logo entrance — spring with overshoot
  const logoScale = spring({ frame, fps, config: { damping: 10, stiffness: 180, mass: 1.2 } });
  const logoOpacity = interpolate(frame, [0, 12], [0, 1], { extrapolateRight: "clamp" });

  // Tagline entrance — delayed
  const taglineProgress = spring({ frame: frame - 25, fps, config: { damping: 14 } });
  const taglineY = interpolate(taglineProgress, [0, 1], [30, 0]);

  // Subtle background glow
  const glowOpacity = interpolate(frame, [5, 20, 80, 100], [0, 0.3, 0.3, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  // Exit fade (last 20 frames)
  const { durationInFrames } = useVideoConfig();
  const exitOpacity = interpolate(frame, [durationInFrames - 20, durationInFrames], [1, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  return (
    <AbsoluteFill style={{ backgroundColor: bgColor, opacity: exitOpacity }}>
      {/* Background glow */}
      <div
        style={{
          position: "absolute",
          inset: 0,
          background: `radial-gradient(circle at center, ${accentColor}20, transparent 60%)`,
          opacity: glowOpacity,
        }}
      />

      {/* Particle dots */}
      <ParticleField frame={frame} color={accentColor} />

      {/* Logo */}
      <AbsoluteFill style={{ justifyContent: "center", alignItems: "center" }}>
        <div
          style={{
            transform: `scale(${logoScale})`,
            opacity: logoOpacity,
          }}
        >
          <Img
            src={logoSrc}
            style={{
              width: 280,
              height: 280,
              objectFit: "contain",
            }}
          />
        </div>

        {/* Tagline */}
        {tagline && (
          <div
            style={{
              marginTop: 30,
              transform: `translateY(${taglineY}px)`,
              opacity: taglineProgress,
              color: "rgba(255,255,255,0.7)",
              fontSize: 28,
              fontWeight: 500,
              fontFamily: "Inter, sans-serif",
              letterSpacing: 4,
              textTransform: "uppercase",
            }}
          >
            {tagline}
          </div>
        )}
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

// -- Subtle Particle Background --
const ParticleField: React.FC<{ frame: number; color: string; count?: number }> = ({
  frame,
  color,
  count = 30,
}) => {
  const particles = Array.from({ length: count }).map((_, i) => {
    const seed = (i * 137.508) % 1; // golden angle spread
    const x = seed * 100;
    const y = ((i * 97.135) % 1) * 100;
    const size = 2 + (i % 3);
    const speed = 0.2 + (i % 5) * 0.1;
    const yOffset = Math.sin(frame * speed * 0.02 + i) * 20;
    const opacity = interpolate(
      Math.sin(frame * 0.03 + i * 0.5),
      [-1, 0, 1],
      [0.05, 0.15, 0.25]
    );

    return { x, y: y + yOffset * 0.1, size, opacity };
  });

  return (
    <AbsoluteFill>
      {particles.map((p, i) => (
        <div
          key={i}
          style={{
            position: "absolute",
            left: `${p.x}%`,
            top: `${p.y}%`,
            width: p.size,
            height: p.size,
            borderRadius: "50%",
            backgroundColor: color,
            opacity: p.opacity,
          }}
        />
      ))}
    </AbsoluteFill>
  );
};

// -- Main Composition --
export const IntroOutro: React.FC<{
  logoSrc: string;
  tagline?: string;
  stingerSrc?: string;
}> = ({ logoSrc, tagline, stingerSrc }) => {
  return (
    <AbsoluteFill>
      <Sequence from={0} durationInFrames={120} name="LogoReveal">
        <LogoReveal logoSrc={logoSrc} tagline={tagline} />
      </Sequence>
      {stingerSrc && (
        <Sequence from={0} durationInFrames={120} name="StingerAudio">
          <Audio src={stingerSrc} volume={0.7} />
        </Sequence>
      )}
    </AbsoluteFill>
  );
};
```

Register in `Root.tsx`:
```tsx
<Composition
  id="IntroOutro"
  component={IntroOutro}
  durationInFrames={120}
  fps={30}
  width={1920}
  height={1080}
  defaultProps={{
    logoSrc: staticFile("branding/logo.png"),
    tagline: "Creating the Future",
    stingerSrc: staticFile("sfx/intro-stinger.mp3"),
  }}
/>
```

## End Screen Layout

```
+----------------------------+
|                            |
|     "Thanks for            |
|      Watching!"            |
|                            |
|   +--------+ +--------+   |
|   | Next   | | Prev   |   |
|   | Video  | | Video   |   |
|   +--------+ +--------+   |
|                            |
|    [ Subscribe Button ]    |
|       @handle              |
|                            |
+----------------------------+
```

## End Screen Template

```tsx
const EndScreen: React.FC<{
  heading?: string;
  handle: string;
  subscribeCTA?: string;
  accentColor?: string;
}> = ({ heading = "Thanks for Watching!", handle, subscribeCTA = "Subscribe", accentColor = "#FF0000" }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const headingScale = spring({ frame, fps, config: { damping: 12 } });
  const btnEntrance = spring({ frame: frame - 30, fps, config: { damping: 14 } });
  const handleEntrance = spring({ frame: frame - 45, fps, config: { damping: 14 } });

  // Subscribe button pulse
  const pulse = 1 + Math.sin(frame * 0.1) * 0.03;

  return (
    <AbsoluteFill style={{ backgroundColor: "#0f0f0f", justifyContent: "center", alignItems: "center" }}>
      {/* Heading */}
      <div
        style={{
          transform: `scale(${headingScale})`,
          color: "#fff",
          fontSize: 56,
          fontWeight: 900,
          fontFamily: "Inter, sans-serif",
          textAlign: "center",
          marginBottom: 60,
        }}
      >
        {heading}
      </div>

      {/* Video thumbnails placeholder */}
      <div style={{ display: "flex", gap: 30, marginBottom: 50, opacity: btnEntrance }}>
        {["Next Video", "Previous Video"].map((label, i) => (
          <div
            key={i}
            style={{
              width: 320,
              height: 180,
              backgroundColor: "#1a1a1a",
              borderRadius: 12,
              border: "2px solid rgba(255,255,255,0.1)",
              display: "flex",
              justifyContent: "center",
              alignItems: "center",
              color: "rgba(255,255,255,0.4)",
              fontSize: 20,
              fontFamily: "Inter, sans-serif",
            }}
          >
            {label}
          </div>
        ))}
      </div>

      {/* Subscribe button */}
      <div
        style={{
          transform: `scale(${btnEntrance * pulse})`,
          backgroundColor: accentColor,
          color: "#fff",
          fontSize: 28,
          fontWeight: 800,
          fontFamily: "Inter, sans-serif",
          padding: "18px 60px",
          borderRadius: 50,
          marginBottom: 20,
          cursor: "pointer",
        }}
      >
        {subscribeCTA}
      </div>

      {/* Handle */}
      <div
        style={{
          opacity: handleEntrance,
          color: "rgba(255,255,255,0.5)",
          fontSize: 24,
          fontWeight: 600,
          fontFamily: "Inter, sans-serif",
        }}
      >
        {handle}
      </div>
    </AbsoluteFill>
  );
};
```

## Lower Third Template

```tsx
const LowerThird: React.FC<{
  name: string;
  title: string;
  accentColor?: string;
}> = ({ name, title, accentColor = "#00f5d4" }) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();

  // Enter
  const barWidth = spring({ frame, fps, config: { damping: 15 } });
  const textSlide = spring({ frame: frame - 5, fps, config: { damping: 14 } });

  // Exit (last 15 frames)
  const exitProgress = interpolate(frame, [durationInFrames - 15, durationInFrames], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const exitX = interpolate(exitProgress, [0, 1], [0, -400]);
  const exitOpacity = interpolate(exitProgress, [0, 1], [1, 0]);

  return (
    <div
      style={{
        position: "absolute",
        bottom: 120,
        left: 60,
        transform: `translateX(${exitX}px)`,
        opacity: exitOpacity,
      }}
    >
      {/* Accent bar */}
      <div
        style={{
          width: interpolate(barWidth, [0, 1], [0, 300]),
          height: 4,
          backgroundColor: accentColor,
          marginBottom: 12,
          borderRadius: 2,
        }}
      />
      {/* Name */}
      <div
        style={{
          transform: `translateX(${interpolate(textSlide, [0, 1], [-100, 0])}px)`,
          opacity: textSlide,
          color: "#ffffff",
          fontSize: 36,
          fontWeight: 800,
          fontFamily: "Inter, sans-serif",
          textShadow: "0 2px 8px rgba(0,0,0,0.5)",
        }}
      >
        {name}
      </div>
      {/* Title */}
      <div
        style={{
          transform: `translateX(${interpolate(textSlide, [0, 1], [-80, 0])}px)`,
          opacity: spring({ frame: frame - 10, fps, config: { damping: 14 } }),
          color: "rgba(255,255,255,0.7)",
          fontSize: 24,
          fontWeight: 500,
          fontFamily: "Inter, sans-serif",
          marginTop: 6,
          textShadow: "0 2px 8px rgba(0,0,0,0.5)",
        }}
      >
        {title}
      </div>
    </div>
  );
};
```

## SVG Path Draw Logo

Use `@remotion/paths` to animate SVG path drawing:

```tsx
import { evolvePath } from "@remotion/paths";

const SVGLogoReveal: React.FC<{ pathData: string; color?: string }> = ({
  pathData,
  color = "#ffffff",
}) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames, width, height } = useVideoConfig();

  const drawProgress = interpolate(frame, [0, durationInFrames * 0.7], [0, 1], {
    extrapolateRight: "clamp",
  });
  const fillOpacity = interpolate(frame, [durationInFrames * 0.6, durationInFrames * 0.9], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  const { strokeDasharray, strokeDashoffset } = evolvePath(drawProgress, pathData);

  return (
    <AbsoluteFill style={{ justifyContent: "center", alignItems: "center" }}>
      <svg width={400} height={400} viewBox="0 0 400 400">
        {/* Drawing stroke */}
        <path
          d={pathData}
          fill="none"
          stroke={color}
          strokeWidth={3}
          strokeDasharray={strokeDasharray}
          strokeDashoffset={strokeDashoffset}
          strokeLinecap="round"
        />
        {/* Fill fading in */}
        <path d={pathData} fill={color} opacity={fillOpacity} />
      </svg>
    </AbsoluteFill>
  );
};
```

## Quality Checklist

- [ ] Logo centered and properly sized (not too large, not too small)
- [ ] Animation smooth — uses `spring()` with proper damping
- [ ] Audio aligned to the visual reveal keyframe
- [ ] Duration appropriate: intros 3-8s, outros 5-15s, stingers 1-3s
- [ ] Brand colors consistent throughout
- [ ] Exit animation included (fade out or slide out)
- [ ] Lower thirds position in safe zone (not overlapping content)
- [ ] End screen has clear CTA (subscribe, follow, etc.)
- [ ] Tagline readable (appropriate size and contrast)
- [ ] Spring configs have no jarring overshoot
- [ ] All `Sequence` components have explicit `name` props

## Reference Files

- `references/intro-patterns.md` — Copy-paste patterns for logo reveals, end screens, stingers
- `../../references/transition-catalog.md` — Transition effects
- `../../references/easing-library.md` — Easing and spring configurations
- `../../references/color-palettes.md` — Brand color palettes
- `../../references/sound-effects-library.md` — SFX for stingers