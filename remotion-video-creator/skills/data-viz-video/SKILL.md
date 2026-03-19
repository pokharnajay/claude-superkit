---
name: data-viz-video
description: Create animated charts, dashboard reveals, data stories, and statistical visualizations. Use when user wants to visualize data, animate charts, create data-driven video content, or bring numbers to life with motion.
---

# Data Visualization Video

Animated charts, dashboards, and data stories that bring numbers to life through motion.

## When to Use

- User wants animated charts or graphs
- User asks for a data story or statistics video
- User wants a dashboard reveal or metrics overview
- User mentions bar chart, line chart, pie chart, or any data visualization
- User wants to visualize numbers, trends, or comparisons

## Chart Types

| Chart | Implementation | Animation Style |
|---|---|---|
| Bar chart | Div-based or SVG rect | Spring per bar, staggered |
| Line chart | SVG path + `@remotion/paths` | `evolvePath()` progressive draw |
| Pie / donut | SVG circle | `stroke-dashoffset` rotation |
| Number counter | `interpolate` + `Math.round` | Counting from 0 to target |
| Progress ring | SVG circle | `stroke-dasharray` animation |
| Area chart | SVG path + fill | Fill under evolving line |
| Horizontal bar race | Div-based | Bars reorder as values change |

## Data Story Structure

| Scene | Duration | Content | Animation |
|---|---|---|---|
| Title | 3-5s (90-150 frames) | Topic + context setting | Fade in, slide |
| Key stat | 5-8s (150-240 frames) | Big number with counter | Number count up |
| Chart 1 | 8-15s (240-450 frames) | Primary visualization | Bars/lines grow in |
| Chart 2 (optional) | 8-15s | Secondary visualization | Progressive reveal |
| Comparison | 5-8s (150-240 frames) | Before/after or A vs B | Side-by-side animation |
| Conclusion | 3-5s (90-150 frames) | Key takeaway message | Fade to emphasis text |

## Design Strategy

- **Clear, high-contrast colors** for data categories (no similar hues)
- **Animate data in** -- never show static charts, always reveal progressively
- **Label everything** -- axes, values, categories (min 18px at 1920x1080)
- **Use spring animations** for organic bar/element growth
- **Use `evolvePath()`** from `@remotion/paths` for progressive line drawing
- **Start from zero** to show scale and growth
- **One chart per scene** -- do not overcrowd
- **Grid lines** at 20-30% opacity for reference without distraction
- **Consistent color mapping** -- same category = same color throughout

## Workflow

1. Read `references/chart-patterns.md` for chart components
2. Read `../../references/color-palettes.md` for data-friendly palettes
3. Define the data story: what insight are you communicating?
4. Choose chart types that best represent the data
5. Structure scenes: title -> key stat -> charts -> takeaway
6. Build chart components with spring animations
7. Add labels, axes, and grid lines
8. Register composition with data as `defaultProps`
9. Render

## Starter Template (Animated Bar Chart)

```tsx
import { AbsoluteFill, useCurrentFrame, useVideoConfig, interpolate, spring, Sequence } from "remotion";
import { loadFont } from "@remotion/google-fonts/Inter";

const { fontFamily } = loadFont();

const COLORS = {
  bg: "#0f172a",
  card: "#1e293b",
  text: "#f8fafc",
  muted: "#94a3b8",
  bars: ["#3b82f6", "#8b5cf6", "#06b6d4", "#f59e0b", "#ef4444", "#22c55e"],
  grid: "rgba(148, 163, 184, 0.15)",
};

interface BarData {
  label: string;
  value: number;
}

const AnimatedBarChart: React.FC<{
  data: BarData[];
  title: string;
  yAxisLabel?: string;
  maxValue?: number;
}> = ({ data, title, yAxisLabel = "", maxValue }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const max = maxValue || Math.max(...data.map((d) => d.value));
  const chartWidth = 1200;
  const chartHeight = 500;
  const barGap = 20;
  const barWidth = (chartWidth - barGap * (data.length + 1)) / data.length;

  // Title fade in
  const titleOpacity = interpolate(frame, [0, 15], [0, 1], { extrapolateRight: "clamp" });

  return (
    <AbsoluteFill style={{ backgroundColor: COLORS.bg, justifyContent: "center", alignItems: "center" }}>
      {/* Title */}
      <div
        style={{
          position: "absolute",
          top: 80,
          fontSize: 40,
          fontWeight: 800,
          fontFamily,
          color: COLORS.text,
          opacity: titleOpacity,
          textAlign: "center",
        }}
      >
        {title}
      </div>

      {/* Chart container */}
      <div style={{ position: "relative", width: chartWidth, height: chartHeight, marginTop: 60 }}>
        {/* Grid lines */}
        {[0, 0.25, 0.5, 0.75, 1].map((pct, i) => (
          <div
            key={i}
            style={{
              position: "absolute",
              bottom: pct * chartHeight,
              left: 0,
              right: 0,
              height: 1,
              backgroundColor: COLORS.grid,
            }}
          />
        ))}

        {/* Y-axis labels */}
        {[0, 0.25, 0.5, 0.75, 1].map((pct, i) => (
          <div
            key={i}
            style={{
              position: "absolute",
              bottom: pct * chartHeight - 10,
              left: -60,
              fontSize: 14,
              fontFamily,
              color: COLORS.muted,
              textAlign: "right",
              width: 50,
            }}
          >
            {Math.round(max * pct)}
          </div>
        ))}

        {/* Bars */}
        {data.map((item, i) => {
          const delay = 15 + i * 8;
          const s = spring({ frame: frame - delay, fps, config: { damping: 12, stiffness: 100 } });
          const barHeight = (item.value / max) * chartHeight * s;
          const x = barGap + i * (barWidth + barGap);

          return (
            <div key={i}>
              {/* Bar */}
              <div
                style={{
                  position: "absolute",
                  bottom: 0,
                  left: x,
                  width: barWidth,
                  height: barHeight,
                  backgroundColor: COLORS.bars[i % COLORS.bars.length],
                  borderRadius: "6px 6px 0 0",
                }}
              />
              {/* Value label */}
              <div
                style={{
                  position: "absolute",
                  bottom: barHeight + 8,
                  left: x,
                  width: barWidth,
                  textAlign: "center",
                  fontSize: 16,
                  fontWeight: 700,
                  fontFamily,
                  color: COLORS.text,
                  opacity: s,
                }}
              >
                {Math.round(item.value * s)}
              </div>
              {/* X-axis label */}
              <div
                style={{
                  position: "absolute",
                  bottom: -30,
                  left: x,
                  width: barWidth,
                  textAlign: "center",
                  fontSize: 14,
                  fontFamily,
                  color: COLORS.muted,
                  opacity: s,
                }}
              >
                {item.label}
              </div>
            </div>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};

// -- Key Stat Scene --
const KeyStat: React.FC<{ value: number; label: string; prefix?: string; suffix?: string }> = ({
  value,
  label,
  prefix = "",
  suffix = "",
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const progress = interpolate(frame, [0, 60], [0, 1], { extrapolateRight: "clamp" });
  const eased = 1 - Math.pow(1 - progress, 3);
  const displayValue = Math.round(eased * value);
  const labelOpacity = interpolate(frame, [30, 45], [0, 1], { extrapolateRight: "clamp" });

  return (
    <AbsoluteFill style={{ backgroundColor: COLORS.bg, justifyContent: "center", alignItems: "center" }}>
      <div style={{ textAlign: "center" }}>
        <div
          style={{
            fontSize: 120,
            fontWeight: 900,
            fontFamily,
            color: COLORS.bars[0],
            fontVariantNumeric: "tabular-nums",
          }}
        >
          {prefix}{displayValue.toLocaleString()}{suffix}
        </div>
        <div
          style={{
            fontSize: 32,
            fontWeight: 500,
            fontFamily,
            color: COLORS.muted,
            marginTop: 16,
            opacity: labelOpacity,
          }}
        >
          {label}
        </div>
      </div>
    </AbsoluteFill>
  );
};

// -- Main Composition --
export const DataVizVideo: React.FC<{
  title: string;
  keyStatValue: number;
  keyStatLabel: string;
  chartTitle: string;
  chartData: BarData[];
}> = ({ title, keyStatValue, keyStatLabel, chartTitle, chartData }) => (
  <AbsoluteFill>
    <Sequence from={0} durationInFrames={120} name="Title">
      <AbsoluteFill style={{ backgroundColor: COLORS.bg, justifyContent: "center", alignItems: "center" }}>
        <div style={{ fontSize: 56, fontWeight: 900, fontFamily, color: COLORS.text, textAlign: "center", padding: "0 100px" }}>
          {title}
        </div>
      </AbsoluteFill>
    </Sequence>
    <Sequence from={120} durationInFrames={180} name="KeyStat">
      <KeyStat value={keyStatValue} label={keyStatLabel} />
    </Sequence>
    <Sequence from={300} durationInFrames={300} name="BarChart">
      <AnimatedBarChart data={chartData} title={chartTitle} />
    </Sequence>
  </AbsoluteFill>
);
```

Register in `Root.tsx`:
```tsx
<Composition
  id="DataVizVideo"
  component={DataVizVideo}
  durationInFrames={600}
  fps={30}
  width={1920}
  height={1080}
  defaultProps={{
    title: "Q4 Revenue Growth",
    keyStatValue: 2400000,
    keyStatLabel: "Total Revenue",
    chartTitle: "Revenue by Region",
    chartData: [
      { label: "North America", value: 850000 },
      { label: "Europe", value: 620000 },
      { label: "Asia Pacific", value: 480000 },
      { label: "Latin America", value: 280000 },
      { label: "Africa", value: 170000 },
    ],
  }}
/>
```

## Data-Driven Composition with Zod Schema

Use Zod to validate `inputProps` for data-driven videos:

```tsx
import { z } from "zod";

export const dataVizSchema = z.object({
  title: z.string(),
  data: z.array(
    z.object({
      label: z.string(),
      value: z.number(),
    })
  ),
});

// In Root.tsx:
<Composition
  id="DataViz"
  component={DataVizVideo}
  schema={dataVizSchema}
  durationInFrames={600}
  fps={30}
  width={1920}
  height={1080}
  defaultProps={{ title: "My Chart", data: [] }}
/>
```

## Color Palettes for Data

### Categorical (distinct categories)
`["#3b82f6", "#8b5cf6", "#06b6d4", "#f59e0b", "#ef4444", "#22c55e"]`

### Sequential (low to high)
`["#dbeafe", "#93c5fd", "#3b82f6", "#1d4ed8", "#1e3a8a"]`

### Diverging (negative to positive)
`["#ef4444", "#fca5a5", "#e5e7eb", "#86efac", "#22c55e"]`

## Quality Checklist

- [ ] Data animates in (no static charts)
- [ ] Axes and labels are clear and readable (18px+)
- [ ] Grid lines present but subtle (15-20% opacity)
- [ ] Color palette is accessible (distinct hues, not just brightness)
- [ ] Numbers formatted with commas for thousands
- [ ] Spring animations for organic data growth
- [ ] One chart per scene (not overcrowded)
- [ ] Key insight or takeaway stated explicitly
- [ ] Data starts from zero baseline
- [ ] Consistent color mapping throughout video
- [ ] Values shown on or near data elements

## Reference Files

- `references/chart-patterns.md` -- All chart component patterns
- `../../references/color-palettes.md` -- Color palettes including data-specific
- `../../references/easing-library.md` -- Easing configurations
- `../../references/motion-principles.md` -- Animation principles