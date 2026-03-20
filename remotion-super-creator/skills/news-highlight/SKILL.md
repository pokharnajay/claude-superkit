---
name: news-highlight
description: Create breaking news banners, headline animations, news tickers, data overlays, and story recaps. Use for news-style video content with urgency and editorial feel.
---

# News Highlight

Broadcast-quality news graphics, headlines, data presentations, and editorial video content.

## When to Use

- User wants a breaking news banner or alert
- User asks for news-style graphics or headlines
- User wants a scrolling ticker/crawl
- User needs data overlays, stat cards, or comparison graphics
- User wants a story recap or bullet-point summary video
- User asks for interview lower thirds or news chyrons

## Common Formats

- Breaking news banner (urgency, alert)
- Headline video (topic + key facts animation)
- Scrolling ticker/crawl (continuous bottom-screen text)
- Data overlay (stats, comparisons, trends)
- Story recap (bullet point sequence)
- Interview lower third (name + title chyron)
- Quote card (attributed statement)

## Design Language

| Category | Background | Accent | Typography | Mood |
|----------|-----------|--------|-----------|------|
| Breaking news | Dark / #111 | Red #CC0000 | Bold sans-serif | Urgent, high energy |
| Financial | Dark navy #0a1628 | Green #00C853 | Monospace for numbers | Authoritative, data-driven |
| Tech | Dark #0f0f0f | Blue #2196F3 / Cyan #00BCD4 | Modern sans-serif | Clean, forward-looking |
| Sports | Bold team colors | White/gold | Impact, heavy weight | Dynamic, energetic |
| Editorial | Neutral #1a1a1a | Warm white | Serif headings | Measured, thoughtful |

## Standard Elements

| Element | Position | Purpose |
|---------|----------|---------|
| News bar | Bottom 15% | Colored strip with headline text |
| Ticker/crawl | Bottom edge | Scrolling continuous text |
| Lower third | Bottom-left | Speaker name + title |
| Data card | Center/overlay | Stat value + label |
| Logo bug | Top-right corner | Network/brand logo |
| Timestamp | Top-left | Date + time display |
| Source line | Below data | Attribution text |

## Complete Starter Template — Breaking News

```tsx
import {
  AbsoluteFill,
  Sequence,
  useCurrentFrame,
  useVideoConfig,
  interpolate,
  spring,
} from "remotion";

// -- Breaking News Banner --
const BreakingNewsBanner: React.FC<{
  headline: string;
  subheadline?: string;
  bannerColor?: string;
}> = ({ headline, subheadline, bannerColor = "#CC0000" }) => {
  const frame = useCurrentFrame();
  const { fps, width } = useVideoConfig();

  // Banner slides up from bottom
  const bannerY = spring({ frame, fps, config: { damping: 18, stiffness: 200 } });
  const bannerTranslate = interpolate(bannerY, [0, 1], [120, 0]);

  // "BREAKING NEWS" label flash
  const labelFlash = Math.sin(frame * 0.15) > 0 ? 1 : 0.7;

  // Headline text reveal (word by word)
  const words = headline.split(" ");

  return (
    <div
      style={{
        position: "absolute",
        bottom: 100,
        left: 0,
        right: 0,
        transform: `translateY(${bannerTranslate}px)`,
      }}
    >
      {/* Breaking News label */}
      <div
        style={{
          backgroundColor: bannerColor,
          display: "inline-block",
          padding: "8px 24px",
          marginLeft: 40,
          marginBottom: -1,
        }}
      >
        <span
          style={{
            color: "#ffffff",
            fontSize: 22,
            fontWeight: 900,
            fontFamily: "Inter, sans-serif",
            letterSpacing: 3,
            textTransform: "uppercase",
            opacity: labelFlash,
          }}
        >
          BREAKING NEWS
        </span>
      </div>

      {/* Main banner */}
      <div
        style={{
          backgroundColor: "rgba(0, 0, 0, 0.85)",
          backdropFilter: "blur(10px)",
          padding: "20px 40px",
          borderLeft: `6px solid ${bannerColor}`,
        }}
      >
        {/* Headline — word by word */}
        <div style={{ display: "flex", flexWrap: "wrap", gap: 10 }}>
          {words.map((word, i) => {
            const delay = 15 + i * 4;
            const wordOpacity = interpolate(frame - delay, [0, 8], [0, 1], {
              extrapolateLeft: "clamp",
              extrapolateRight: "clamp",
            });
            return (
              <span
                key={i}
                style={{
                  color: "#ffffff",
                  fontSize: 40,
                  fontWeight: 800,
                  fontFamily: "Inter, sans-serif",
                  opacity: wordOpacity,
                }}
              >
                {word}
              </span>
            );
          })}
        </div>

        {/* Subheadline */}
        {subheadline && (
          <div
            style={{
              color: "rgba(255,255,255,0.6)",
              fontSize: 24,
              fontWeight: 500,
              fontFamily: "Inter, sans-serif",
              marginTop: 8,
              opacity: interpolate(frame, [40, 55], [0, 1], {
                extrapolateLeft: "clamp",
                extrapolateRight: "clamp",
              }),
            }}
          >
            {subheadline}
          </div>
        )}
      </div>
    </div>
  );
};

// -- Scrolling Ticker --
const NewsTicker: React.FC<{
  items: string[];
  speed?: number;
  bgColor?: string;
  textColor?: string;
  separator?: string;
}> = ({ items, speed = 2, bgColor = "#CC0000", textColor = "#ffffff", separator = " /// " }) => {
  const frame = useCurrentFrame();
  const { width } = useVideoConfig();

  const fullText = items.join(separator) + separator;
  // Approximate character width (monospace-like for consistency)
  const charWidth = 14;
  const textWidth = fullText.length * charWidth;
  const totalWidth = textWidth + width;

  const translateX = width - (frame * speed) % totalWidth;

  return (
    <div
      style={{
        position: "absolute",
        bottom: 0,
        left: 0,
        right: 0,
        height: 44,
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
          fontSize: 20,
          fontWeight: 700,
          fontFamily: "Inter, sans-serif",
          letterSpacing: 0.5,
        }}
      >
        {fullText}{fullText}
      </div>
    </div>
  );
};

// -- Data Overlay Card --
const DataCard: React.FC<{
  value: string;
  label: string;
  trend?: "up" | "down" | "neutral";
  accentColor?: string;
}> = ({ value, label, trend, accentColor = "#00f5d4" }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const entrance = spring({ frame, fps, config: { damping: 14 } });

  const trendColor = trend === "up" ? "#00C853" : trend === "down" ? "#FF1744" : "#888";
  const trendIcon = trend === "up" ? "+" : trend === "down" ? "-" : "";

  return (
    <div
      style={{
        transform: `scale(${entrance}) translateY(${interpolate(entrance, [0, 1], [20, 0])}px)`,
        backgroundColor: "rgba(0, 0, 0, 0.8)",
        backdropFilter: "blur(10px)",
        borderRadius: 16,
        padding: "24px 36px",
        border: `1px solid rgba(255,255,255,0.1)`,
        borderLeft: `4px solid ${accentColor}`,
        textAlign: "center",
      }}
    >
      <div style={{ display: "flex", alignItems: "baseline", justifyContent: "center", gap: 8 }}>
        <span
          style={{
            color: "#ffffff",
            fontSize: 52,
            fontWeight: 900,
            fontFamily: "Inter, sans-serif",
            fontVariantNumeric: "tabular-nums",
          }}
        >
          {value}
        </span>
        {trend && (
          <span style={{ color: trendColor, fontSize: 28, fontWeight: 700, fontFamily: "Inter, sans-serif" }}>
            {trendIcon}
          </span>
        )}
      </div>
      <div
        style={{
          color: "rgba(255,255,255,0.5)",
          fontSize: 18,
          fontWeight: 600,
          fontFamily: "Inter, sans-serif",
          textTransform: "uppercase",
          letterSpacing: 2,
          marginTop: 8,
        }}
      >
        {label}
      </div>
    </div>
  );
};

// -- Main Composition --
export const NewsHighlight: React.FC<{
  headline: string;
  subheadline?: string;
  tickerItems: string[];
  stats?: { value: string; label: string; trend?: "up" | "down" | "neutral" }[];
}> = ({ headline, subheadline, tickerItems, stats }) => {
  const { fps } = useVideoConfig();

  return (
    <AbsoluteFill style={{ backgroundColor: "#111111" }}>
      {/* Background gradient */}
      <div
        style={{
          position: "absolute",
          inset: 0,
          background: "radial-gradient(ellipse at top, #1a1a2e 0%, #111111 70%)",
        }}
      />

      {/* Data cards */}
      {stats && (
        <Sequence from={60} name="DataCards">
          <div
            style={{
              position: "absolute",
              top: 200,
              left: 0,
              right: 0,
              display: "flex",
              justifyContent: "center",
              gap: 30,
            }}
          >
            {stats.map((stat, i) => (
              <Sequence key={i} from={i * 12} name={`DataCard-${i}`}>
                <DataCard value={stat.value} label={stat.label} trend={stat.trend} />
              </Sequence>
            ))}
          </div>
        </Sequence>
      )}

      {/* Breaking news banner */}
      <Sequence from={0} name="BreakingBanner">
        <BreakingNewsBanner headline={headline} subheadline={subheadline} />
      </Sequence>

      {/* Scrolling ticker */}
      <Sequence from={30} name="Ticker">
        <NewsTicker items={tickerItems} />
      </Sequence>
    </AbsoluteFill>
  );
};
```

Register in `Root.tsx`:
```tsx
<Composition
  id="NewsHighlight"
  component={NewsHighlight}
  durationInFrames={300}
  fps={30}
  width={1920}
  height={1080}
  defaultProps={{
    headline: "Major Climate Agreement Reached at Global Summit",
    subheadline: "195 countries sign historic emissions reduction pact",
    tickerItems: [
      "Markets react positively to summit outcome",
      "Tech sector pledges carbon neutrality by 2030",
      "New renewable energy targets set for developing nations",
    ],
    stats: [
      { value: "195", label: "Countries", trend: "up" },
      { value: "40%", label: "Emissions Cut", trend: "up" },
      { value: "2030", label: "Target Year", trend: "neutral" },
    ],
  }}
/>
```

## Ticker/Crawl Pattern

For smooth, continuous scrolling text at the bottom of screen:

```tsx
const totalWidth = textWidth + containerWidth;
const translateX = interpolate(frame, [0, durationInFrames], [containerWidth, -textWidth]);
```

**Tips:**
- Duplicate the text string for seamless looping
- Speed: 2-3px per frame is readable
- Use monospace-adjacent font for consistent character width
- Red background for breaking, blue/dark for standard

## Animated Number Counter for Stats

```tsx
const AnimatedStat: React.FC<{ target: number; prefix?: string; suffix?: string }> = ({
  target,
  prefix = "",
  suffix = "",
}) => {
  const frame = useCurrentFrame();
  const progress = interpolate(frame, [0, 60], [0, 1], { extrapolateRight: "clamp" });
  const eased = 1 - Math.pow(1 - progress, 3);
  const value = Math.round(eased * target);

  return (
    <span style={{ fontVariantNumeric: "tabular-nums", fontFamily: "Inter, sans-serif" }}>
      {prefix}{value.toLocaleString()}{suffix}
    </span>
  );
};
```

## Story Recap Pattern

Bullet points appearing one by one with staggered animation:

```tsx
const StoryRecap: React.FC<{
  title: string;
  bullets: string[];
  secondsPerBullet?: number;
}> = ({ title, bullets, secondsPerBullet = 3 }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const framesPerBullet = secondsPerBullet * fps;

  return (
    <AbsoluteFill style={{ backgroundColor: "#111", padding: 80, justifyContent: "center" }}>
      <div style={{ color: "#CC0000", fontSize: 20, fontWeight: 800, fontFamily: "Inter, sans-serif", letterSpacing: 3, textTransform: "uppercase", marginBottom: 20 }}>
        STORY RECAP
      </div>
      <div style={{ color: "#fff", fontSize: 42, fontWeight: 800, fontFamily: "Inter, sans-serif", marginBottom: 40, lineHeight: 1.3 }}>
        {title}
      </div>
      {bullets.map((bullet, i) => {
        const bulletFrame = frame - i * framesPerBullet;
        const entrance = spring({ frame: bulletFrame, fps, config: { damping: 14 } });
        const isVisible = bulletFrame > 0;
        if (!isVisible) return null;
        return (
          <div
            key={i}
            style={{
              opacity: entrance,
              transform: `translateX(${interpolate(entrance, [0, 1], [40, 0])}px)`,
              display: "flex",
              alignItems: "flex-start",
              gap: 16,
              marginBottom: 20,
            }}
          >
            <div style={{ width: 8, height: 8, borderRadius: "50%", backgroundColor: "#CC0000", marginTop: 12, flexShrink: 0 }} />
            <div style={{ color: "rgba(255,255,255,0.85)", fontSize: 28, fontWeight: 600, fontFamily: "Inter, sans-serif", lineHeight: 1.4 }}>
              {bullet}
            </div>
          </div>
        );
      })}
    </AbsoluteFill>
  );
};
```

## Quality Checklist

- [ ] News bar positioned in lower portion (not blocking key visuals)
- [ ] Text readable on colored backgrounds (white on red, white on dark)
- [ ] Headline animation creates appropriate urgency
- [ ] Data presented clearly with context and units
- [ ] Ticker scrolls smoothly at a readable speed (not too fast)
- [ ] Source attribution visible when presenting data/quotes
- [ ] Font weights heavy enough for broadcast readability (700+)
- [ ] Colors match the news category (red = breaking, blue = tech, etc.)
- [ ] Numbers use `fontVariantNumeric: "tabular-nums"` for alignment
- [ ] All `Sequence` components have explicit `name` props
- [ ] Lower thirds animate in and out cleanly

## Reference Files

- `references/news-patterns.md` — Copy-paste patterns for banners, tickers, data cards
- `../../references/color-palettes.md` — Curated color palettes
- `../../references/font-pairings.md` — Font pairing recommendations
- `../../references/transition-catalog.md` — Transition effects