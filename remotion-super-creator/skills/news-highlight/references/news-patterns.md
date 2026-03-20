# News Highlight — Code Patterns

Dense, copy-paste-ready component patterns for news graphics, headlines, tickers, and data overlays.

---

## Breaking News Banner Component

Animated red bar with white text that slides up from bottom.

```tsx
const BreakingBanner: React.FC<{
  text: string;
  bannerColor?: string;
  labelText?: string;
}> = ({ text, bannerColor = "#CC0000", labelText = "BREAKING NEWS" }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const slideUp = spring({ frame, fps, config: { damping: 18, stiffness: 200 } });
  const bannerY = interpolate(slideUp, [0, 1], [150, 0]);

  // Flashing label
  const flash = Math.sin(frame * 0.15) > 0 ? 1 : 0.6;

  return (
    <div style={{ position: "absolute", bottom: 80, left: 0, right: 0, transform: `translateY(${bannerY}px)` }}>
      {/* Label tab */}
      <div style={{ display: "inline-block", backgroundColor: bannerColor, padding: "8px 20px", marginLeft: 40, marginBottom: -1 }}>
        <span style={{ color: "#fff", fontSize: 20, fontWeight: 900, fontFamily: "Inter, sans-serif", letterSpacing: 3, opacity: flash }}>
          {labelText}
        </span>
      </div>
      {/* Main bar */}
      <div style={{ backgroundColor: "rgba(0,0,0,0.88)", backdropFilter: "blur(10px)", padding: "18px 40px", borderLeft: `6px solid ${bannerColor}` }}>
        <div style={{ color: "#fff", fontSize: 38, fontWeight: 800, fontFamily: "Inter, sans-serif" }}>{text}</div>
      </div>
    </div>
  );
};
```

---

## Headline Text Animation

Word-by-word bold reveal with emphasis on key terms.

```tsx
const HeadlineReveal: React.FC<{
  text: string;
  emphasisWords?: string[];
  emphasisColor?: string;
  framesPerWord?: number;
}> = ({ text, emphasisWords = [], emphasisColor = "#CC0000", framesPerWord = 5 }) => {
  const frame = useCurrentFrame();
  const words = text.split(" ");

  return (
    <div style={{ display: "flex", flexWrap: "wrap", gap: "8px 14px", justifyContent: "center", padding: "0 80px" }}>
      {words.map((word, i) => {
        const delay = i * framesPerWord;
        const opacity = interpolate(frame - delay, [0, 8], [0, 1], {
          extrapolateLeft: "clamp",
          extrapolateRight: "clamp",
        });
        const y = interpolate(frame - delay, [0, 8], [20, 0], {
          extrapolateLeft: "clamp",
          extrapolateRight: "clamp",
        });
        const isEmphasis = emphasisWords.some((ew) => word.toLowerCase().includes(ew.toLowerCase()));

        return (
          <span
            key={i}
            style={{
              opacity,
              transform: `translateY(${y}px)`,
              color: isEmphasis ? emphasisColor : "#ffffff",
              fontSize: 56,
              fontWeight: 900,
              fontFamily: "Inter, sans-serif",
              display: "inline-block",
              textDecoration: isEmphasis ? "underline" : "none",
              textDecorationColor: isEmphasis ? emphasisColor : undefined,
              textUnderlineOffset: 8,
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

## Scrolling Ticker / Crawl

Seamless looping text crawl at the bottom of the screen.

```tsx
const ScrollingTicker: React.FC<{
  items: string[];
  speed?: number;
  bgColor?: string;
  textColor?: string;
  height?: number;
  separator?: string;
}> = ({
  items,
  speed = 2.5,
  bgColor = "rgba(0,0,0,0.9)",
  textColor = "#ffffff",
  height = 44,
  separator = "  \u2022  ", // bullet separator
}) => {
  const frame = useCurrentFrame();
  const { width } = useVideoConfig();

  const fullText = items.join(separator) + separator;
  const charWidth = 13;
  const textWidth = fullText.length * charWidth;

  // Loop position
  const offset = (frame * speed) % textWidth;
  const translateX = width - offset;

  return (
    <div
      style={{
        position: "absolute",
        bottom: 0,
        left: 0,
        right: 0,
        height,
        backgroundColor: bgColor,
        overflow: "hidden",
        display: "flex",
        alignItems: "center",
      }}
    >
      <div
        style={{
          whiteSpace: "nowrap",
          transform: `translateX(${translateX}px)`,
          color: textColor,
          fontSize: 18,
          fontWeight: 600,
          fontFamily: "Inter, sans-serif",
          letterSpacing: 0.5,
        }}
      >
        {/* Duplicate for seamless loop */}
        {fullText}
        {fullText}
        {fullText}
      </div>
    </div>
  );
};
```

---

## Split Screen Layout

Anchor/speaker area on one side, graphics/data on the other.

```tsx
const SplitScreenNews: React.FC<{
  leftContent: React.ReactNode;
  rightContent: React.ReactNode;
  splitRatio?: number;
  dividerColor?: string;
}> = ({ leftContent, rightContent, splitRatio = 0.4, dividerColor = "#CC0000" }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const dividerIn = spring({ frame, fps, config: { damping: 18 } });

  return (
    <AbsoluteFill>
      {/* Left panel */}
      <div style={{ position: "absolute", left: 0, top: 0, bottom: 0, width: `${splitRatio * 100}%`, overflow: "hidden" }}>
        {leftContent}
      </div>
      {/* Divider */}
      <div
        style={{
          position: "absolute",
          left: `${splitRatio * 100}%`,
          top: 0,
          width: 4,
          height: `${dividerIn * 100}%`,
          backgroundColor: dividerColor,
          zIndex: 10,
        }}
      />
      {/* Right panel */}
      <div style={{ position: "absolute", right: 0, top: 0, bottom: 0, width: `${(1 - splitRatio) * 100}%`, overflow: "hidden" }}>
        {rightContent}
      </div>
    </AbsoluteFill>
  );
};
```

---

## Data Overlay Card

Stat value + label + trend indicator for data presentations.

```tsx
const DataOverlayCard: React.FC<{
  value: string | number;
  label: string;
  trend?: "up" | "down" | "neutral";
  prefix?: string;
  suffix?: string;
  accentColor?: string;
  animate?: boolean;
}> = ({ value, label, trend, prefix = "", suffix = "", accentColor = "#00f5d4", animate = true }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const entrance = animate ? spring({ frame, fps, config: { damping: 14 } }) : 1;
  const trendColor = trend === "up" ? "#00C853" : trend === "down" ? "#FF1744" : "#666";
  const trendArrow = trend === "up" ? "\u2191" : trend === "down" ? "\u2193" : "\u2013";

  return (
    <div
      style={{
        transform: `scale(${entrance})`,
        opacity: entrance,
        backgroundColor: "rgba(0,0,0,0.8)",
        backdropFilter: "blur(10px)",
        border: "1px solid rgba(255,255,255,0.08)",
        borderLeft: `4px solid ${accentColor}`,
        borderRadius: 12,
        padding: "20px 32px",
        minWidth: 180,
      }}
    >
      <div style={{ display: "flex", alignItems: "baseline", gap: 8 }}>
        <span style={{ color: "#fff", fontSize: 48, fontWeight: 900, fontFamily: "Inter, sans-serif", fontVariantNumeric: "tabular-nums" }}>
          {prefix}{typeof value === "number" ? value.toLocaleString() : value}{suffix}
        </span>
        {trend && (
          <span style={{ color: trendColor, fontSize: 24, fontWeight: 700 }}>{trendArrow}</span>
        )}
      </div>
      <div style={{ color: "rgba(255,255,255,0.45)", fontSize: 16, fontWeight: 600, fontFamily: "Inter, sans-serif", textTransform: "uppercase", letterSpacing: 2, marginTop: 6 }}>
        {label}
      </div>
    </div>
  );
};
```

---

## Timeline Component

Events appearing on a horizontal line for chronological stories.

```tsx
const TimelineEvent: React.FC<{
  events: { date: string; text: string }[];
  activeIndex: number;
  accentColor?: string;
}> = ({ events, activeIndex, accentColor = "#CC0000" }) => {
  const frame = useCurrentFrame();
  const { fps, width } = useVideoConfig();

  const eventWidth = (width - 160) / events.length;

  return (
    <div style={{ position: "relative", padding: "0 80px" }}>
      {/* Line */}
      <div style={{ height: 3, backgroundColor: "rgba(255,255,255,0.15)", position: "relative", marginBottom: 40 }}>
        {/* Active progress */}
        <div
          style={{
            height: "100%",
            backgroundColor: accentColor,
            width: `${((activeIndex + 1) / events.length) * 100}%`,
            borderRadius: 2,
          }}
        />
      </div>

      {/* Events */}
      <div style={{ display: "flex" }}>
        {events.map((event, i) => {
          const isActive = i <= activeIndex;
          const isCurrent = i === activeIndex;
          const entrance = spring({ frame: frame - i * 15, fps, config: { damping: 14 } });

          return (
            <div key={i} style={{ flex: 1, textAlign: "center", opacity: entrance }}>
              {/* Dot */}
              <div
                style={{
                  width: isCurrent ? 16 : 10,
                  height: isCurrent ? 16 : 10,
                  borderRadius: "50%",
                  backgroundColor: isActive ? accentColor : "rgba(255,255,255,0.2)",
                  margin: "-48px auto 12px",
                  border: isCurrent ? `3px solid ${accentColor}40` : "none",
                  boxShadow: isCurrent ? `0 0 12px ${accentColor}60` : "none",
                }}
              />
              <div style={{ color: isActive ? "#fff" : "rgba(255,255,255,0.3)", fontSize: 16, fontWeight: 700, fontFamily: "Inter, sans-serif" }}>
                {event.date}
              </div>
              <div style={{ color: isActive ? "rgba(255,255,255,0.7)" : "rgba(255,255,255,0.2)", fontSize: 14, fontWeight: 500, fontFamily: "Inter, sans-serif", marginTop: 4, padding: "0 8px" }}>
                {event.text}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};
```

---

## Source Attribution Overlay

Small text showing date and source, typically placed below data or quotes.

```tsx
const SourceAttribution: React.FC<{
  source: string;
  date?: string;
}> = ({ source, date }) => {
  const frame = useCurrentFrame();
  const opacity = interpolate(frame, [20, 35], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  return (
    <div style={{ opacity, display: "flex", gap: 12, alignItems: "center" }}>
      {date && (
        <span style={{ color: "rgba(255,255,255,0.3)", fontSize: 14, fontFamily: "Inter, sans-serif", fontVariantNumeric: "tabular-nums" }}>
          {date}
        </span>
      )}
      <span style={{ color: "rgba(255,255,255,0.3)", fontSize: 14, fontFamily: "Inter, sans-serif" }}>|</span>
      <span style={{ color: "rgba(255,255,255,0.35)", fontSize: 14, fontWeight: 500, fontFamily: "Inter, sans-serif" }}>
        Source: {source}
      </span>
    </div>
  );
};
```

---

## Quote Display

Attributed quote with speaker photo and styling.

```tsx
const NewsQuote: React.FC<{
  quote: string;
  speaker: string;
  speakerTitle?: string;
  speakerPhotoSrc?: string;
  accentColor?: string;
}> = ({ quote, speaker, speakerTitle, speakerPhotoSrc, accentColor = "#CC0000" }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const quoteIn = spring({ frame, fps, config: { damping: 14 } });
  const attrIn = spring({ frame: frame - 20, fps, config: { damping: 14 } });

  return (
    <AbsoluteFill style={{ justifyContent: "center", padding: "0 100px" }}>
      {/* Quote bar */}
      <div style={{ borderLeft: `6px solid ${accentColor}`, paddingLeft: 30 }}>
        <div
          style={{
            opacity: quoteIn,
            transform: `translateY(${interpolate(quoteIn, [0, 1], [30, 0])}px)`,
            color: "#ffffff",
            fontSize: 38,
            fontWeight: 700,
            fontFamily: "Georgia, 'Times New Roman', serif",
            fontStyle: "italic",
            lineHeight: 1.5,
          }}
        >
          &ldquo;{quote}&rdquo;
        </div>

        {/* Attribution */}
        <div
          style={{
            opacity: attrIn,
            marginTop: 24,
            display: "flex",
            alignItems: "center",
            gap: 16,
          }}
        >
          {speakerPhotoSrc && (
            <div style={{ width: 52, height: 52, borderRadius: "50%", overflow: "hidden", border: `2px solid ${accentColor}` }}>
              <Img src={speakerPhotoSrc} style={{ width: "100%", height: "100%", objectFit: "cover" }} />
            </div>
          )}
          <div>
            <div style={{ color: "#fff", fontSize: 22, fontWeight: 700, fontFamily: "Inter, sans-serif" }}>{speaker}</div>
            {speakerTitle && (
              <div style={{ color: "rgba(255,255,255,0.5)", fontSize: 16, fontWeight: 500, fontFamily: "Inter, sans-serif" }}>{speakerTitle}</div>
            )}
          </div>
        </div>
      </div>
    </AbsoluteFill>
  );
};
```

---

## Story Recap Sequence

Bullet points appearing one by one with staggered entrance.

```tsx
const StoryRecapSequence: React.FC<{
  title: string;
  bullets: string[];
  category?: string;
  categoryColor?: string;
  framesPerBullet?: number;
}> = ({ title, bullets, category = "RECAP", categoryColor = "#CC0000", framesPerBullet = 90 }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  return (
    <AbsoluteFill style={{ backgroundColor: "#111", justifyContent: "center", padding: "80px 100px" }}>
      {/* Category label */}
      <div style={{ color: categoryColor, fontSize: 18, fontWeight: 900, fontFamily: "Inter, sans-serif", letterSpacing: 4, textTransform: "uppercase", marginBottom: 16 }}>
        {category}
      </div>
      {/* Title */}
      <div style={{ color: "#fff", fontSize: 40, fontWeight: 800, fontFamily: "Inter, sans-serif", lineHeight: 1.3, marginBottom: 40 }}>
        {title}
      </div>
      {/* Bullets */}
      {bullets.map((bullet, i) => {
        const bulletStart = 30 + i * framesPerBullet;
        const isVisible = frame >= bulletStart;
        if (!isVisible) return null;

        const entrance = spring({ frame: frame - bulletStart, fps, config: { damping: 14 } });
        return (
          <div
            key={i}
            style={{
              opacity: entrance,
              transform: `translateX(${interpolate(entrance, [0, 1], [30, 0])}px)`,
              display: "flex",
              gap: 16,
              marginBottom: 18,
              alignItems: "flex-start",
            }}
          >
            <div style={{ width: 8, height: 8, borderRadius: "50%", backgroundColor: categoryColor, marginTop: 10, flexShrink: 0 }} />
            <div style={{ color: "rgba(255,255,255,0.85)", fontSize: 26, fontWeight: 600, fontFamily: "Inter, sans-serif", lineHeight: 1.4 }}>
              {bullet}
            </div>
          </div>
        );
      })}
    </AbsoluteFill>
  );
};
```

---

## Countdown / Date Display Component

Animated date or countdown for event-related news.

```tsx
const DateDisplay: React.FC<{
  date: string;
  label?: string;
  accentColor?: string;
}> = ({ date, label, accentColor = "#CC0000" }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const entrance = spring({ frame, fps, config: { damping: 14 } });

  return (
    <div style={{ textAlign: "center", opacity: entrance, transform: `scale(${entrance})` }}>
      <div style={{ color: accentColor, fontSize: 64, fontWeight: 900, fontFamily: "Inter, sans-serif", fontVariantNumeric: "tabular-nums" }}>
        {date}
      </div>
      {label && (
        <div style={{ color: "rgba(255,255,255,0.4)", fontSize: 18, fontWeight: 600, fontFamily: "Inter, sans-serif", textTransform: "uppercase", letterSpacing: 3, marginTop: 8 }}>
          {label}
        </div>
      )}
    </div>
  );
};
```

---

## Lower Third with Network Branding

Animated chyron bar with text for speaker identification.

```tsx
const NewsLowerThird: React.FC<{
  name: string;
  title: string;
  networkLogo?: string;
  barColor?: string;
}> = ({ name, title, networkLogo, barColor = "#CC0000" }) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();

  // Enter
  const barExpand = spring({ frame, fps, config: { damping: 20, stiffness: 200 } });
  const textReveal = spring({ frame: frame - 8, fps, config: { damping: 14 } });

  // Exit
  const exitStart = durationInFrames - 20;
  const exitProgress = interpolate(frame, [exitStart, durationInFrames], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  return (
    <div
      style={{
        position: "absolute",
        bottom: 80,
        left: 0,
        transform: `translateX(${interpolate(exitProgress, [0, 1], [0, -600])}px)`,
        opacity: interpolate(exitProgress, [0, 0.8, 1], [1, 1, 0]),
      }}
    >
      {/* Color bar background */}
      <div
        style={{
          width: interpolate(barExpand, [0, 1], [0, 520]),
          height: 80,
          backgroundColor: barColor,
          borderRadius: "0 6px 6px 0",
          position: "absolute",
          bottom: 0,
        }}
      />
      {/* Text layer */}
      <div
        style={{
          position: "relative",
          padding: "12px 28px",
          paddingLeft: networkLogo ? 80 : 28,
          opacity: textReveal,
          transform: `translateX(${interpolate(textReveal, [0, 1], [-30, 0])}px)`,
          minWidth: 400,
        }}
      >
        {networkLogo && (
          <Img
            src={networkLogo}
            style={{ position: "absolute", left: 16, top: 14, width: 48, height: 48, objectFit: "contain" }}
          />
        )}
        <div style={{ color: "#fff", fontSize: 28, fontWeight: 800, fontFamily: "Inter, sans-serif" }}>{name}</div>
        <div style={{ color: "rgba(255,255,255,0.8)", fontSize: 18, fontWeight: 500, fontFamily: "Inter, sans-serif", marginTop: 2 }}>{title}</div>
      </div>
    </div>
  );
};
```

---

## Logo Bug

Corner network logo, subtle and persistent.

```tsx
const LogoBug: React.FC<{
  logoSrc: string;
  position?: "top-left" | "top-right" | "bottom-left" | "bottom-right";
  size?: number;
  opacity?: number;
}> = ({ logoSrc, position = "top-right", size = 60, opacity = 0.4 }) => {
  const frame = useCurrentFrame();
  const fadeIn = interpolate(frame, [0, 20], [0, opacity], {
    extrapolateRight: "clamp",
  });

  const posStyle: Record<string, React.CSSProperties> = {
    "top-left": { top: 30, left: 30 },
    "top-right": { top: 30, right: 30 },
    "bottom-left": { bottom: 100, left: 30 },
    "bottom-right": { bottom: 100, right: 30 },
  };

  return (
    <div style={{ position: "absolute", ...posStyle[position], opacity: fadeIn, zIndex: 50 }}>
      <Img src={logoSrc} style={{ width: size, height: size, objectFit: "contain" }} />
    </div>
  );
};
```

---

## Alert Animation

Pulsing/flashing element for urgent news alerts.

```tsx
const AlertPulse: React.FC<{
  text?: string;
  color?: string;
}> = ({ text = "ALERT", color = "#CC0000" }) => {
  const frame = useCurrentFrame();

  // Fast pulse
  const pulse = Math.sin(frame * 0.2) * 0.15 + 1;
  const flash = Math.sin(frame * 0.15) > 0 ? 1 : 0.5;
  // Glow intensity
  const glow = (Math.sin(frame * 0.2) + 1) * 0.5;

  return (
    <div
      style={{
        display: "inline-flex",
        alignItems: "center",
        gap: 10,
        transform: `scale(${pulse})`,
      }}
    >
      {/* Pulsing dot */}
      <div
        style={{
          width: 14,
          height: 14,
          borderRadius: "50%",
          backgroundColor: color,
          opacity: flash,
          boxShadow: `0 0 ${glow * 20}px ${color}`,
        }}
      />
      <span
        style={{
          color,
          fontSize: 22,
          fontWeight: 900,
          fontFamily: "Inter, sans-serif",
          letterSpacing: 3,
          opacity: flash,
        }}
      >
        {text}
      </span>
    </div>
  );
};
```