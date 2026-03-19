# Intro / Outro — Code Patterns

Dense, copy-paste-ready component patterns for logo reveals, end screens, stingers, and lower thirds.

---

## Fade + Scale Logo Reveal

Classic, clean logo entrance with spring animation.

```tsx
const FadeScaleLogo: React.FC<{
  logoSrc: string;
  bgColor?: string;
}> = ({ logoSrc, bgColor = "#0f0f0f" }) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();

  const scale = spring({ frame, fps, config: { damping: 10, stiffness: 180, mass: 1.1 } });
  const opacity = interpolate(frame, [0, 15], [0, 1], { extrapolateRight: "clamp" });

  // Exit fade
  const exit = interpolate(frame, [durationInFrames - 20, durationInFrames], [1, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  return (
    <AbsoluteFill style={{ backgroundColor: bgColor, justifyContent: "center", alignItems: "center", opacity: exit }}>
      <Img
        src={logoSrc}
        style={{
          width: 300,
          height: 300,
          objectFit: "contain",
          transform: `scale(${scale})`,
          opacity,
        }}
      />
    </AbsoluteFill>
  );
};
```

---

## SVG Path Draw Logo

Lines draw to form the logo using `@remotion/paths`.

```tsx
import { evolvePath, getLength } from "@remotion/paths";

const PathDrawLogo: React.FC<{
  paths: string[];
  color?: string;
  strokeWidth?: number;
  viewBox?: string;
}> = ({ paths, color = "#ffffff", strokeWidth = 2.5, viewBox = "0 0 400 400" }) => {
  const frame = useCurrentFrame();
  const { durationInFrames } = useVideoConfig();

  const drawPhase = durationInFrames * 0.6;
  const fillPhase = durationInFrames * 0.3;

  return (
    <AbsoluteFill style={{ justifyContent: "center", alignItems: "center", backgroundColor: "#0f0f0f" }}>
      <svg width={400} height={400} viewBox={viewBox}>
        {paths.map((d, i) => {
          // Stagger each path
          const delay = (i / paths.length) * drawPhase * 0.5;
          const drawProgress = interpolate(frame - delay, [0, drawPhase - delay], [0, 1], {
            extrapolateLeft: "clamp",
            extrapolateRight: "clamp",
          });
          const fillOpacity = interpolate(frame, [drawPhase, drawPhase + fillPhase], [0, 1], {
            extrapolateLeft: "clamp",
            extrapolateRight: "clamp",
          });

          const { strokeDasharray, strokeDashoffset } = evolvePath(drawProgress, d);

          return (
            <g key={i}>
              <path d={d} fill="none" stroke={color} strokeWidth={strokeWidth} strokeDasharray={strokeDasharray} strokeDashoffset={strokeDashoffset} strokeLinecap="round" />
              <path d={d} fill={color} opacity={fillOpacity} />
            </g>
          );
        })}
      </svg>
    </AbsoluteFill>
  );
};
```

---

## Particle Assembly

Dots converge from random positions to form the logo shape.

```tsx
const ParticleAssembly: React.FC<{
  logoSrc: string;
  particleCount?: number;
  particleColor?: string;
}> = ({ logoSrc, particleCount = 80, particleColor = "#00f5d4" }) => {
  const frame = useCurrentFrame();
  const { fps, width, height, durationInFrames } = useVideoConfig();

  // Phase 1: particles fly in (0-60%), Phase 2: logo fades in (50-80%), Phase 3: hold
  const assembleEnd = durationInFrames * 0.6;
  const logoFadeStart = durationInFrames * 0.5;
  const logoFadeEnd = durationInFrames * 0.8;

  const assembleProgress = interpolate(frame, [0, assembleEnd], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const logoOpacity = interpolate(frame, [logoFadeStart, logoFadeEnd], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const particleOpacity = interpolate(frame, [logoFadeStart, logoFadeEnd], [1, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  // Eased assembly
  const eased = 1 - Math.pow(1 - assembleProgress, 3);

  const particles = Array.from({ length: particleCount }).map((_, i) => {
    // Deterministic random positions
    const startX = ((i * 137.508 + 50) % width);
    const startY = ((i * 97.135 + 30) % height);
    // Target: center area (logo position)
    const targetX = width / 2 + ((i % 10) - 5) * 20;
    const targetY = height / 2 + (Math.floor(i / 10) % 8 - 4) * 20;

    const x = interpolate(eased, [0, 1], [startX, targetX]);
    const y = interpolate(eased, [0, 1], [startY, targetY]);
    const size = 3 + (i % 4);

    return { x, y, size };
  });

  return (
    <AbsoluteFill style={{ backgroundColor: "#0f0f0f" }}>
      {/* Particles */}
      <AbsoluteFill style={{ opacity: particleOpacity }}>
        {particles.map((p, i) => (
          <div
            key={i}
            style={{
              position: "absolute",
              left: p.x,
              top: p.y,
              width: p.size,
              height: p.size,
              borderRadius: "50%",
              backgroundColor: particleColor,
              opacity: 0.6,
            }}
          />
        ))}
      </AbsoluteFill>

      {/* Logo fading in */}
      <AbsoluteFill style={{ justifyContent: "center", alignItems: "center", opacity: logoOpacity }}>
        <Img src={logoSrc} style={{ width: 300, height: 300, objectFit: "contain" }} />
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
```

---

## Glitch Effect Component

Digital glitch with random translation, opacity flicker, and color channel shift.

```tsx
const GlitchReveal: React.FC<{
  logoSrc: string;
  glitchIntensity?: number;
}> = ({ logoSrc, glitchIntensity = 1 }) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();

  // Glitch active during middle portion
  const glitchStart = 10;
  const glitchEnd = durationInFrames * 0.6;
  const isGlitching = frame >= glitchStart && frame <= glitchEnd;

  // Deterministic pseudo-random from frame
  const hash = (f: number) => Math.sin(f * 12.9898 + f * 78.233) * 43758.5453 % 1;

  const offsetX = isGlitching ? hash(frame) * 20 * glitchIntensity - 10 : 0;
  const offsetY = isGlitching ? hash(frame + 1) * 10 * glitchIntensity - 5 : 0;
  const skewX = isGlitching ? hash(frame + 2) * 4 * glitchIntensity - 2 : 0;
  const flickerOpacity = isGlitching ? (hash(frame + 3) > 0.8 ? 0.3 : 1) : 1;

  // Final reveal
  const revealScale = spring({ frame: Math.max(0, frame - glitchEnd), fps, config: { damping: 12 } });
  const finalOpacity = frame > glitchEnd ? 1 : flickerOpacity;

  return (
    <AbsoluteFill style={{ backgroundColor: "#0a0a0a", justifyContent: "center", alignItems: "center" }}>
      {/* RGB channel offset layers */}
      {isGlitching && (
        <>
          <Img
            src={logoSrc}
            style={{
              position: "absolute",
              width: 280,
              height: 280,
              objectFit: "contain",
              transform: `translate(${offsetX - 5}px, ${offsetY}px)`,
              filter: "hue-rotate(120deg)",
              opacity: 0.3,
              mixBlendMode: "screen",
            }}
          />
          <Img
            src={logoSrc}
            style={{
              position: "absolute",
              width: 280,
              height: 280,
              objectFit: "contain",
              transform: `translate(${offsetX + 5}px, ${offsetY}px)`,
              filter: "hue-rotate(240deg)",
              opacity: 0.3,
              mixBlendMode: "screen",
            }}
          />
        </>
      )}

      {/* Main logo */}
      <Img
        src={logoSrc}
        style={{
          width: 280,
          height: 280,
          objectFit: "contain",
          transform: `translate(${offsetX}px, ${offsetY}px) skewX(${skewX}deg) scale(${frame > glitchEnd ? revealScale : 1})`,
          opacity: finalOpacity,
        }}
      />

      {/* Scan lines */}
      {isGlitching && (
        <div
          style={{
            position: "absolute",
            inset: 0,
            background: `repeating-linear-gradient(0deg, transparent, transparent 2px, rgba(0,0,0,0.1) 2px, rgba(0,0,0,0.1) 4px)`,
            pointerEvents: "none",
          }}
        />
      )}
    </AbsoluteFill>
  );
};
```

---

## Letter-by-Letter Text Logo Animation

Text logo that types out character by character.

```tsx
const LetterByLetter: React.FC<{
  text: string;
  color?: string;
  fontSize?: number;
  framesPerLetter?: number;
}> = ({ text, color = "#ffffff", fontSize = 72, framesPerLetter = 4 }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const visibleCount = Math.min(Math.floor(frame / framesPerLetter), text.length);
  const cursorVisible = Math.sin(frame * 0.3) > 0;

  return (
    <AbsoluteFill style={{ backgroundColor: "#0f0f0f", justifyContent: "center", alignItems: "center" }}>
      <div style={{ display: "flex", alignItems: "center" }}>
        {text.split("").map((char, i) => {
          const charFrame = frame - i * framesPerLetter;
          const isVisible = i < visibleCount;
          const charScale = isVisible
            ? spring({ frame: charFrame, fps, config: { damping: 12, stiffness: 300 } })
            : 0;

          return (
            <span
              key={i}
              style={{
                fontSize,
                fontWeight: 900,
                fontFamily: "Inter, sans-serif",
                color,
                transform: `scale(${charScale})`,
                display: "inline-block",
                minWidth: char === " " ? fontSize * 0.3 : undefined,
              }}
            >
              {char}
            </span>
          );
        })}
        {/* Cursor */}
        {visibleCount < text.length && cursorVisible && (
          <span style={{ fontSize, color, fontWeight: 100, opacity: 0.7 }}>|</span>
        )}
      </div>
    </AbsoluteFill>
  );
};
```

---

## 3D Logo Rotation

Logo rotating in 3D using CSS transforms (no Three.js required for simple rotations).

```tsx
const Logo3DRotation: React.FC<{
  logoSrc: string;
  axis?: "Y" | "X";
}> = ({ logoSrc, axis = "Y" }) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();

  // Rotate in, settle, hold
  const rotateIn = spring({ frame, fps, config: { damping: 14, stiffness: 100 } });
  const rotation = interpolate(rotateIn, [0, 1], [axis === "Y" ? -180 : -180, 0]);

  const scale = spring({ frame, fps, config: { damping: 12, stiffness: 200 } });

  return (
    <AbsoluteFill style={{ backgroundColor: "#0f0f0f", justifyContent: "center", alignItems: "center", perspective: 1200 }}>
      <div
        style={{
          transform: `rotate${axis}(${rotation}deg) scale(${scale})`,
          transformStyle: "preserve-3d",
          backfaceVisibility: "hidden",
        }}
      >
        <Img src={logoSrc} style={{ width: 300, height: 300, objectFit: "contain" }} />
      </div>
    </AbsoluteFill>
  );
};
```

---

## Subscribe Button with Pulse

Animated subscribe button with breathing pulse effect.

```tsx
const SubscribeButton: React.FC<{
  text?: string;
  bgColor?: string;
  textColor?: string;
}> = ({ text = "Subscribe", bgColor = "#FF0000", textColor = "#ffffff" }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const entrance = spring({ frame, fps, config: { damping: 10, stiffness: 180 } });
  const pulse = 1 + Math.sin(frame * 0.12) * 0.04;

  // Bell icon wiggle
  const bellRotation = frame > 30 ? Math.sin((frame - 30) * 0.3) * 8 : 0;
  const bellOpacity = spring({ frame: frame - 30, fps, config: { damping: 14 } });

  return (
    <div style={{ display: "flex", alignItems: "center", gap: 16 }}>
      <div
        style={{
          transform: `scale(${entrance * pulse})`,
          backgroundColor: bgColor,
          color: textColor,
          fontSize: 32,
          fontWeight: 800,
          fontFamily: "Inter, sans-serif",
          padding: "16px 48px",
          borderRadius: 8,
          boxShadow: `0 8px 30px ${bgColor}50`,
        }}
      >
        {text}
      </div>
      {/* Bell icon */}
      <div
        style={{
          opacity: bellOpacity,
          transform: `rotate(${bellRotation}deg)`,
          fontSize: 36,
        }}
      >
        <svg width="36" height="36" viewBox="0 0 24 24" fill={textColor}>
          <path d="M12 22c1.1 0 2-.9 2-2h-4c0 1.1.9 2 2 2zm6-6v-5c0-3.07-1.63-5.64-4.5-6.32V4c0-.83-.67-1.5-1.5-1.5s-1.5.67-1.5 1.5v.68C7.64 5.36 6 7.92 6 11v5l-2 2v1h16v-1l-2-2z" />
        </svg>
      </div>
    </div>
  );
};
```

---

## Social Media Icons Row

Staggered bounce-in of social media icon buttons.

```tsx
const SocialIcons: React.FC<{
  icons: { label: string; color: string }[];
}> = ({ icons }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  return (
    <div style={{ display: "flex", gap: 24, justifyContent: "center" }}>
      {icons.map((icon, i) => {
        const s = spring({ frame: frame - i * 8, fps, config: { damping: 10, stiffness: 200 } });
        return (
          <div
            key={i}
            style={{
              transform: `scale(${s}) translateY(${interpolate(s, [0, 1], [30, 0])}px)`,
              width: 56,
              height: 56,
              borderRadius: 16,
              backgroundColor: icon.color,
              display: "flex",
              justifyContent: "center",
              alignItems: "center",
              boxShadow: `0 4px 20px ${icon.color}40`,
            }}
          >
            <span style={{ color: "#fff", fontSize: 14, fontWeight: 700, fontFamily: "Inter, sans-serif" }}>
              {icon.label}
            </span>
          </div>
        );
      })}
    </div>
  );
};

// Usage:
// <SocialIcons icons={[
//   { label: "YT", color: "#FF0000" },
//   { label: "TW", color: "#1DA1F2" },
//   { label: "IG", color: "#E1306C" },
//   { label: "TK", color: "#000000" },
// ]} />
```

---

## End Screen Layout

Thanks message + video thumbnails + subscribe CTA.

```tsx
const EndScreenLayout: React.FC<{
  heading: string;
  handle: string;
  nextVideoLabel?: string;
  prevVideoLabel?: string;
  accentColor?: string;
}> = ({ heading, handle, nextVideoLabel = "Next Video", prevVideoLabel = "Watch Again", accentColor = "#FF0000" }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const h = spring({ frame, fps, config: { damping: 12 } });
  const cards = spring({ frame: frame - 15, fps, config: { damping: 14 } });
  const btn = spring({ frame: frame - 30, fps, config: { damping: 12 } });
  const hdl = spring({ frame: frame - 40, fps, config: { damping: 14 } });

  return (
    <AbsoluteFill style={{ backgroundColor: "#0f0f0f", justifyContent: "center", alignItems: "center", gap: 40 }}>
      <div style={{ transform: `scale(${h})`, color: "#fff", fontSize: 52, fontWeight: 900, fontFamily: "Inter, sans-serif" }}>
        {heading}
      </div>

      <div style={{ display: "flex", gap: 24, opacity: cards, transform: `translateY(${interpolate(cards, [0, 1], [30, 0])}px)` }}>
        {[nextVideoLabel, prevVideoLabel].map((label, i) => (
          <div key={i} style={{ width: 300, height: 170, backgroundColor: "#1a1a1a", borderRadius: 12, border: "2px solid rgba(255,255,255,0.08)", display: "flex", justifyContent: "center", alignItems: "center" }}>
            <span style={{ color: "rgba(255,255,255,0.4)", fontSize: 18, fontFamily: "Inter, sans-serif" }}>{label}</span>
          </div>
        ))}
      </div>

      <div style={{ transform: `scale(${btn})`, backgroundColor: accentColor, color: "#fff", padding: "16px 52px", borderRadius: 50, fontSize: 26, fontWeight: 800, fontFamily: "Inter, sans-serif" }}>
        Subscribe
      </div>

      <div style={{ opacity: hdl, color: "rgba(255,255,255,0.4)", fontSize: 22, fontFamily: "Inter, sans-serif" }}>
        {handle}
      </div>
    </AbsoluteFill>
  );
};
```

---

## Stinger Wipe

Fast brand-colored wipe for transitions between segments.

```tsx
const StingerWipe: React.FC<{
  color?: string;
  direction?: "left" | "right" | "up" | "down";
}> = ({ color = "#00f5d4", direction = "right" }) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames, width, height } = useVideoConfig();

  // Fast wipe in, pause, fast wipe out
  const mid = durationInFrames / 2;
  const wipeIn = spring({ frame, fps, config: { damping: 20, stiffness: 300 } });
  const wipeOut = frame > mid ? spring({ frame: frame - mid, fps, config: { damping: 20, stiffness: 300 } }) : 0;

  const getTransform = () => {
    const inVal = interpolate(wipeIn, [0, 1], [-110, 0]);
    const outVal = interpolate(wipeOut, [0, 1], [0, 110]);
    const val = inVal + outVal;

    switch (direction) {
      case "right": return `translateX(${val}%)`;
      case "left": return `translateX(${-val}%)`;
      case "down": return `translateY(${val}%)`;
      case "up": return `translateY(${-val}%)`;
    }
  };

  return (
    <AbsoluteFill>
      <div
        style={{
          position: "absolute",
          inset: 0,
          backgroundColor: color,
          transform: getTransform(),
        }}
      />
    </AbsoluteFill>
  );
};
```

---

## Lower Third with Network Branding

Animated bar + text with brand accent, includes enter and exit.

```tsx
const BrandedLowerThird: React.FC<{
  name: string;
  title: string;
  brandColor?: string;
  logoSrc?: string;
}> = ({ name, title, brandColor = "#00f5d4", logoSrc }) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();

  // Enter
  const barIn = spring({ frame, fps, config: { damping: 18, stiffness: 200 } });
  const textIn = spring({ frame: frame - 6, fps, config: { damping: 14 } });

  // Exit
  const exitFrame = durationInFrames - 20;
  const barOut = frame > exitFrame ? interpolate(frame, [exitFrame, durationInFrames], [1, 0], { extrapolateRight: "clamp" }) : 1;

  return (
    <div style={{ position: "absolute", bottom: 100, left: 0, right: 0, opacity: barOut }}>
      {/* Color bar */}
      <div
        style={{
          position: "absolute",
          bottom: 0,
          left: 0,
          width: interpolate(barIn, [0, 1], [0, 500]),
          height: 80,
          backgroundColor: brandColor,
          borderRadius: "0 8px 8px 0",
        }}
      />
      {/* Text content */}
      <div
        style={{
          position: "relative",
          paddingLeft: logoSrc ? 100 : 24,
          paddingBottom: 16,
          paddingTop: 12,
          opacity: textIn,
          transform: `translateX(${interpolate(textIn, [0, 1], [-40, 0])}px)`,
        }}
      >
        {logoSrc && (
          <Img src={logoSrc} style={{ position: "absolute", left: 16, top: 12, width: 56, height: 56, objectFit: "contain" }} />
        )}
        <div style={{ color: "#fff", fontSize: 32, fontWeight: 800, fontFamily: "Inter, sans-serif", textShadow: "0 1px 4px rgba(0,0,0,0.3)" }}>{name}</div>
        <div style={{ color: "rgba(255,255,255,0.8)", fontSize: 22, fontWeight: 500, fontFamily: "Inter, sans-serif", marginTop: 2 }}>{title}</div>
      </div>
    </div>
  );
};
```

---

## Circular Reveal

Expanding circle mask from center revealing content underneath.

```tsx
const CircularReveal: React.FC<{
  children: React.ReactNode;
  bgColor?: string;
}> = ({ children, bgColor = "#0f0f0f" }) => {
  const frame = useCurrentFrame();
  const { fps, width, height } = useVideoConfig();

  const progress = spring({ frame, fps, config: { damping: 14, stiffness: 80 } });
  // Max radius = diagonal of viewport
  const maxRadius = Math.sqrt(width * width + height * height) / 2;
  const radius = progress * maxRadius;

  return (
    <AbsoluteFill style={{ backgroundColor: bgColor }}>
      <div
        style={{
          position: "absolute",
          left: width / 2 - radius,
          top: height / 2 - radius,
          width: radius * 2,
          height: radius * 2,
          borderRadius: "50%",
          overflow: "hidden",
        }}
      >
        <div style={{ position: "absolute", left: -(width / 2 - radius), top: -(height / 2 - radius), width, height }}>
          {children}
        </div>
      </div>
    </AbsoluteFill>
  );
};
```

---

## Tagline Typewriter Reveal

Tagline text appearing character by character with cursor.

```tsx
const TaglineTypewriter: React.FC<{
  text: string;
  color?: string;
  speed?: number; // frames per character
  startDelay?: number;
}> = ({ text, color = "rgba(255,255,255,0.7)", speed = 3, startDelay = 30 }) => {
  const frame = useCurrentFrame();

  const adjustedFrame = Math.max(0, frame - startDelay);
  const visibleChars = Math.min(Math.floor(adjustedFrame / speed), text.length);
  const showCursor = adjustedFrame > 0 && Math.sin(frame * 0.3) > 0;
  const isDone = visibleChars >= text.length;

  return (
    <div
      style={{
        color,
        fontSize: 28,
        fontWeight: 500,
        fontFamily: "Inter, sans-serif",
        letterSpacing: 3,
        textTransform: "uppercase",
      }}
    >
      {text.substring(0, visibleChars)}
      {!isDone && showCursor && <span style={{ opacity: 0.7 }}>|</span>}
    </div>
  );
};
```