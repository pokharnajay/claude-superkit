# Data Visualization -- Chart Patterns

Copy-paste-ready chart components for data visualization videos. All use Remotion primitives.

---

## 1. Animated Bar Chart (Vertical, Staggered Spring)

Full bar chart with Y-axis labels, X-axis labels, grid lines, and staggered spring animation per bar.

```tsx
import { AbsoluteFill, useCurrentFrame, useVideoConfig, interpolate, spring } from "remotion";

interface BarData {
  label: string;
  value: number;
  color?: string;
}

const BAR_COLORS = ["#3b82f6", "#8b5cf6", "#06b6d4", "#f59e0b", "#ef4444", "#22c55e"];

const VerticalBarChart: React.FC<{
  data: BarData[];
  width?: number;
  height?: number;
  maxValue?: number;
}> = ({ data, width = 1200, height = 500, maxValue }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const max = maxValue || Math.max(...data.map((d) => d.value)) * 1.1;
  const barGap = 20;
  const barWidth = (width - barGap * (data.length + 1)) / data.length;

  return (
    <div style={{ position: "relative", width, height }}>
      {/* Grid lines */}
      {[0, 0.25, 0.5, 0.75, 1].map((pct, i) => (
        <div
          key={i}
          style={{
            position: "absolute",
            bottom: pct * height,
            left: 0,
            right: 0,
            height: 1,
            backgroundColor: "rgba(148,163,184,0.15)",
          }}
        />
      ))}

      {/* Y-axis labels */}
      {[0, 0.25, 0.5, 0.75, 1].map((pct, i) => (
        <div
          key={i}
          style={{
            position: "absolute",
            bottom: pct * height - 10,
            left: -65,
            fontSize: 14,
            fontFamily: "Inter, sans-serif",
            color: "#94a3b8",
            textAlign: "right",
            width: 55,
          }}
        >
          {Math.round(max * pct).toLocaleString()}
        </div>
      ))}

      {/* Bars with labels */}
      {data.map((item, i) => {
        const delay = 10 + i * 8;
        const s = spring({ frame: frame - delay, fps, config: { damping: 12, stiffness: 100 } });
        const barH = (item.value / max) * height * s;
        const x = barGap + i * (barWidth + barGap);
        const color = item.color || BAR_COLORS[i % BAR_COLORS.length];

        return (
          <div key={i}>
            <div
              style={{
                position: "absolute",
                bottom: 0,
                left: x,
                width: barWidth,
                height: barH,
                backgroundColor: color,
                borderRadius: "6px 6px 0 0",
              }}
            />
            {/* Value on top */}
            <div
              style={{
                position: "absolute",
                bottom: barH + 8,
                left: x,
                width: barWidth,
                textAlign: "center",
                fontSize: 15,
                fontWeight: 700,
                fontFamily: "Inter, sans-serif",
                color: "#f8fafc",
                opacity: s,
              }}
            >
              {Math.round(item.value * s).toLocaleString()}
            </div>
            {/* X-axis label */}
            <div
              style={{
                position: "absolute",
                bottom: -30,
                left: x,
                width: barWidth,
                textAlign: "center",
                fontSize: 13,
                fontFamily: "Inter, sans-serif",
                color: "#94a3b8",
                opacity: s,
              }}
            >
              {item.label}
            </div>
          </div>
        );
      })}
    </div>
  );
};
```

---

## 2. Line Chart with evolvePath

Progressive path drawing using `@remotion/paths`. Line draws itself from left to right.

```tsx
import { AbsoluteFill, useCurrentFrame, useVideoConfig, interpolate } from "remotion";
import { evolvePath } from "@remotion/paths";

interface LinePoint {
  x: number;
  y: number;
}

const LineChart: React.FC<{
  points: LinePoint[];
  width?: number;
  height?: number;
  color?: string;
  strokeWidth?: number;
  drawDuration?: number;
}> = ({ points, width = 1200, height = 500, color = "#3b82f6", strokeWidth = 3, drawDuration = 60 }) => {
  const frame = useCurrentFrame();
  const progress = interpolate(frame, [0, drawDuration], [0, 1], { extrapolateRight: "clamp" });

  // Build SVG path string
  const pathD = points
    .map((p, i) => `${i === 0 ? "M" : "L"} ${p.x} ${p.y}`)
    .join(" ");

  const { strokeDasharray, strokeDashoffset } = evolvePath(progress, pathD);

  return (
    <div style={{ position: "relative", width, height }}>
      {/* Grid lines */}
      {[0, 0.25, 0.5, 0.75, 1].map((pct, i) => (
        <div
          key={i}
          style={{
            position: "absolute",
            top: pct * height,
            left: 0,
            right: 0,
            height: 1,
            backgroundColor: "rgba(148,163,184,0.12)",
          }}
        />
      ))}

      <svg width={width} height={height} style={{ position: "absolute", inset: 0 }}>
        <path
          d={pathD}
          fill="none"
          stroke={color}
          strokeWidth={strokeWidth}
          strokeLinecap="round"
          strokeLinejoin="round"
          strokeDasharray={strokeDasharray}
          strokeDashoffset={strokeDashoffset}
        />
      </svg>

      {/* Data point markers */}
      {points.map((p, i) => {
        const pointProgress = interpolate(frame, [drawDuration * (i / points.length), drawDuration * (i / points.length) + 10], [0, 1], {
          extrapolateLeft: "clamp",
          extrapolateRight: "clamp",
        });
        return (
          <div
            key={i}
            style={{
              position: "absolute",
              left: p.x - 5,
              top: p.y - 5,
              width: 10,
              height: 10,
              borderRadius: "50%",
              backgroundColor: color,
              border: "2px solid #fff",
              opacity: pointProgress,
              transform: `scale(${pointProgress})`,
            }}
          />
        );
      })}
    </div>
  );
};
```

---

## 3. Pie Chart (Stroke-Dashoffset)

SVG circle-based pie chart with animated segments.

```tsx
const PieChart: React.FC<{
  data: { label: string; value: number; color: string }[];
  size?: number;
  strokeWidth?: number;
  animationDuration?: number;
}> = ({ data, size = 400, strokeWidth = 80, animationDuration = 60 }) => {
  const frame = useCurrentFrame();
  const total = data.reduce((sum, d) => sum + d.value, 0);
  const radius = (size - strokeWidth) / 2;
  const circumference = 2 * Math.PI * radius;
  const center = size / 2;

  const progress = interpolate(frame, [0, animationDuration], [0, 1], { extrapolateRight: "clamp" });
  let cumulativePercent = 0;

  return (
    <div style={{ position: "relative", width: size, height: size }}>
      <svg width={size} height={size} style={{ transform: "rotate(-90deg)" }}>
        {data.map((item, i) => {
          const percent = item.value / total;
          const dashLength = circumference * percent * progress;
          const dashOffset = -circumference * cumulativePercent * progress;
          cumulativePercent += percent;

          return (
            <circle
              key={i}
              cx={center}
              cy={center}
              r={radius}
              fill="none"
              stroke={item.color}
              strokeWidth={strokeWidth}
              strokeDasharray={`${dashLength} ${circumference - dashLength}`}
              strokeDashoffset={dashOffset}
              strokeLinecap="butt"
            />
          );
        })}
      </svg>
    </div>
  );
};
```

---

## 4. Donut Chart with Center Value

Donut with a big number in the center showing total or percentage.

```tsx
const DonutChart: React.FC<{
  data: { label: string; value: number; color: string }[];
  centerValue: string;
  centerLabel: string;
  size?: number;
}> = ({ data, centerValue, centerLabel, size = 400 }) => {
  const frame = useCurrentFrame();
  const strokeWidth = 60;
  const total = data.reduce((sum, d) => sum + d.value, 0);
  const radius = (size - strokeWidth) / 2;
  const circumference = 2 * Math.PI * radius;
  const center = size / 2;
  const progress = interpolate(frame, [0, 50], [0, 1], { extrapolateRight: "clamp" });
  const centerOpacity = interpolate(frame, [30, 45], [0, 1], { extrapolateRight: "clamp" });

  let cumulative = 0;

  return (
    <div style={{ position: "relative", width: size, height: size }}>
      <svg width={size} height={size} style={{ transform: "rotate(-90deg)" }}>
        {data.map((item, i) => {
          const pct = item.value / total;
          const dash = circumference * pct * progress;
          const offset = -circumference * cumulative * progress;
          cumulative += pct;
          return (
            <circle
              key={i}
              cx={center}
              cy={center}
              r={radius}
              fill="none"
              stroke={item.color}
              strokeWidth={strokeWidth}
              strokeDasharray={`${dash} ${circumference - dash}`}
              strokeDashoffset={offset}
            />
          );
        })}
      </svg>
      {/* Center text */}
      <div
        style={{
          position: "absolute",
          inset: 0,
          display: "flex",
          flexDirection: "column",
          justifyContent: "center",
          alignItems: "center",
          opacity: centerOpacity,
        }}
      >
        <div style={{ fontSize: 48, fontWeight: 900, fontFamily: "Inter, sans-serif", color: "#f8fafc" }}>
          {centerValue}
        </div>
        <div style={{ fontSize: 18, fontWeight: 500, fontFamily: "Inter, sans-serif", color: "#94a3b8" }}>
          {centerLabel}
        </div>
      </div>
    </div>
  );
};
```

---

## 5. Number Counter (Formatted with Commas)

Counts from 0 to target with ease-out cubic. Supports prefix, suffix, decimal places.

```tsx
const NumberCounter: React.FC<{
  target: number;
  prefix?: string;
  suffix?: string;
  decimals?: number;
  color?: string;
  fontSize?: number;
  duration?: number;
}> = ({ target, prefix = "", suffix = "", decimals = 0, color = "#3b82f6", fontSize = 96, duration = 60 }) => {
  const frame = useCurrentFrame();
  const progress = interpolate(frame, [0, duration], [0, 1], { extrapolateRight: "clamp" });
  const eased = 1 - Math.pow(1 - progress, 3);
  const value = eased * target;
  const formatted = decimals > 0
    ? value.toFixed(decimals).replace(/\B(?=(\d{3})+(?!\d))/g, ",")
    : Math.round(value).toLocaleString();

  return (
    <div
      style={{
        fontSize,
        fontWeight: 900,
        fontFamily: "Inter, sans-serif",
        color,
        fontVariantNumeric: "tabular-nums",
        textAlign: "center",
      }}
    >
      {prefix}{formatted}{suffix}
    </div>
  );
};
```

---

## 6. Progress Ring (SVG Circle)

Circular progress indicator that fills to a target percentage.

```tsx
const ProgressRing: React.FC<{
  percentage: number;
  size?: number;
  strokeWidth?: number;
  color?: string;
  bgColor?: string;
  duration?: number;
}> = ({ percentage, size = 200, strokeWidth = 12, color = "#3b82f6", bgColor = "rgba(148,163,184,0.2)", duration = 45 }) => {
  const frame = useCurrentFrame();
  const radius = (size - strokeWidth) / 2;
  const circumference = 2 * Math.PI * radius;
  const progress = interpolate(frame, [0, duration], [0, percentage / 100], { extrapolateRight: "clamp" });
  const dashLength = circumference * progress;
  const center = size / 2;

  return (
    <div style={{ position: "relative", width: size, height: size }}>
      <svg width={size} height={size} style={{ transform: "rotate(-90deg)" }}>
        {/* Background ring */}
        <circle cx={center} cy={center} r={radius} fill="none" stroke={bgColor} strokeWidth={strokeWidth} />
        {/* Progress ring */}
        <circle
          cx={center}
          cy={center}
          r={radius}
          fill="none"
          stroke={color}
          strokeWidth={strokeWidth}
          strokeDasharray={`${dashLength} ${circumference - dashLength}`}
          strokeLinecap="round"
        />
      </svg>
      {/* Center percentage */}
      <div
        style={{
          position: "absolute",
          inset: 0,
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          fontSize: size * 0.22,
          fontWeight: 800,
          fontFamily: "Inter, sans-serif",
          color: "#f8fafc",
        }}
      >
        {Math.round(progress * 100)}%
      </div>
    </div>
  );
};
```

---

## 7. Horizontal Bar Race

Bars that animate horizontally and can reorder as values change. Great for "racing" bar charts.

```tsx
const HorizontalBarRace: React.FC<{
  data: { label: string; value: number; color: string }[];
  width?: number;
  barHeight?: number;
  gap?: number;
}> = ({ data, width = 1000, barHeight = 48, gap = 12 }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const max = Math.max(...data.map((d) => d.value));

  // Sort by value descending
  const sorted = [...data].sort((a, b) => b.value - a.value);

  return (
    <div style={{ display: "flex", flexDirection: "column", gap }}>
      {sorted.map((item, i) => {
        const delay = i * 6;
        const s = spring({ frame: frame - delay, fps, config: { damping: 14 } });
        const barW = (item.value / max) * width * s;

        return (
          <div key={item.label} style={{ display: "flex", alignItems: "center", gap: 16 }}>
            {/* Label */}
            <div
              style={{
                width: 140,
                fontSize: 16,
                fontWeight: 600,
                fontFamily: "Inter, sans-serif",
                color: "#f8fafc",
                textAlign: "right",
                opacity: s,
              }}
            >
              {item.label}
            </div>
            {/* Bar */}
            <div
              style={{
                width: barW,
                height: barHeight,
                backgroundColor: item.color,
                borderRadius: "0 6px 6px 0",
                display: "flex",
                alignItems: "center",
                justifyContent: "flex-end",
                paddingRight: 12,
              }}
            >
              <span
                style={{
                  fontSize: 14,
                  fontWeight: 700,
                  fontFamily: "Inter, sans-serif",
                  color: "#fff",
                  opacity: s,
                }}
              >
                {Math.round(item.value * s).toLocaleString()}
              </span>
            </div>
          </div>
        );
      })}
    </div>
  );
};
```

---

## 8. Dashboard Grid (4 Widgets Staggered)

Four stat widgets that slide in with staggered timing. Arranges in a 2x2 grid.

```tsx
const DashboardGrid: React.FC<{
  widgets: { label: string; value: string; change?: string; changePositive?: boolean }[];
}> = ({ widgets }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  return (
    <div
      style={{
        display: "grid",
        gridTemplateColumns: "1fr 1fr",
        gap: 24,
        padding: 40,
      }}
    >
      {widgets.slice(0, 4).map((widget, i) => {
        const delay = i * 8;
        const s = spring({ frame: frame - delay, fps, config: { damping: 12 } });
        const translateY = interpolate(s, [0, 1], [30, 0]);

        return (
          <div
            key={i}
            style={{
              backgroundColor: "#1e293b",
              borderRadius: 16,
              padding: "28px 32px",
              opacity: s,
              transform: `translateY(${translateY}px)`,
            }}
          >
            <div style={{ fontSize: 16, fontWeight: 500, fontFamily: "Inter, sans-serif", color: "#94a3b8", marginBottom: 8 }}>
              {widget.label}
            </div>
            <div style={{ fontSize: 36, fontWeight: 800, fontFamily: "Inter, sans-serif", color: "#f8fafc" }}>
              {widget.value}
            </div>
            {widget.change && (
              <div
                style={{
                  fontSize: 15,
                  fontWeight: 600,
                  fontFamily: "Inter, sans-serif",
                  color: widget.changePositive ? "#22c55e" : "#ef4444",
                  marginTop: 8,
                }}
              >
                {widget.changePositive ? "\u2191" : "\u2193"} {widget.change}
              </div>
            )}
          </div>
        );
      })}
    </div>
  );
};
```

---

## 9. Stat Card (Big Number + Label + Trend Arrow)

Single stat display with animated counter and trend indicator.

```tsx
const StatCard: React.FC<{
  value: number;
  label: string;
  prefix?: string;
  suffix?: string;
  trend?: "up" | "down";
  trendValue?: string;
}> = ({ value, label, prefix = "", suffix = "", trend, trendValue }) => {
  const frame = useCurrentFrame();
  const progress = interpolate(frame, [0, 50], [0, 1], { extrapolateRight: "clamp" });
  const eased = 1 - Math.pow(1 - progress, 3);
  const displayVal = Math.round(eased * value);
  const labelOpacity = interpolate(frame, [25, 40], [0, 1], { extrapolateRight: "clamp" });

  return (
    <div
      style={{
        backgroundColor: "#1e293b",
        borderRadius: 20,
        padding: "40px 48px",
        textAlign: "center",
        minWidth: 300,
      }}
    >
      <div
        style={{
          fontSize: 72,
          fontWeight: 900,
          fontFamily: "Inter, sans-serif",
          color: "#f8fafc",
          fontVariantNumeric: "tabular-nums",
        }}
      >
        {prefix}{displayVal.toLocaleString()}{suffix}
      </div>
      <div
        style={{
          fontSize: 22,
          fontWeight: 500,
          fontFamily: "Inter, sans-serif",
          color: "#94a3b8",
          marginTop: 8,
          opacity: labelOpacity,
        }}
      >
        {label}
      </div>
      {trend && trendValue && (
        <div
          style={{
            fontSize: 18,
            fontWeight: 700,
            fontFamily: "Inter, sans-serif",
            color: trend === "up" ? "#22c55e" : "#ef4444",
            marginTop: 12,
            opacity: labelOpacity,
          }}
        >
          {trend === "up" ? "\u2191" : "\u2193"} {trendValue}
        </div>
      )}
    </div>
  );
};
```

---

## 10. Comparison Bars (Two Bars Side by Side)

Two bars growing next to each other for A vs B comparisons.

```tsx
const ComparisonBars: React.FC<{
  labelA: string;
  labelB: string;
  valueA: number;
  valueB: number;
  colorA?: string;
  colorB?: string;
  height?: number;
}> = ({ labelA, labelB, valueA, valueB, colorA = "#3b82f6", colorB = "#8b5cf6", height = 300 }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const max = Math.max(valueA, valueB) * 1.1;

  const sA = spring({ frame: frame - 10, fps, config: { damping: 12 } });
  const sB = spring({ frame: frame - 18, fps, config: { damping: 12 } });
  const barHeightA = (valueA / max) * height * sA;
  const barHeightB = (valueB / max) * height * sB;

  return (
    <div style={{ display: "flex", alignItems: "flex-end", gap: 24, height }}>
      <div style={{ textAlign: "center" }}>
        <div style={{ fontSize: 20, fontWeight: 700, fontFamily: "Inter, sans-serif", color: "#f8fafc", marginBottom: 8, opacity: sA }}>
          {Math.round(valueA * sA).toLocaleString()}
        </div>
        <div style={{ width: 120, height: barHeightA, backgroundColor: colorA, borderRadius: "8px 8px 0 0" }} />
        <div style={{ fontSize: 16, fontFamily: "Inter, sans-serif", color: "#94a3b8", marginTop: 8, opacity: sA }}>
          {labelA}
        </div>
      </div>
      <div style={{ textAlign: "center" }}>
        <div style={{ fontSize: 20, fontWeight: 700, fontFamily: "Inter, sans-serif", color: "#f8fafc", marginBottom: 8, opacity: sB }}>
          {Math.round(valueB * sB).toLocaleString()}
        </div>
        <div style={{ width: 120, height: barHeightB, backgroundColor: colorB, borderRadius: "8px 8px 0 0" }} />
        <div style={{ fontSize: 16, fontFamily: "Inter, sans-serif", color: "#94a3b8", marginTop: 8, opacity: sB }}>
          {labelB}
        </div>
      </div>
    </div>
  );
};
```

---

## 11. Axis and Grid Line Components

Reusable axis labels and grid lines for any chart.

```tsx
const GridLines: React.FC<{
  width: number;
  height: number;
  divisions?: number;
  color?: string;
}> = ({ width, height, divisions = 4, color = "rgba(148,163,184,0.15)" }) => (
  <>
    {Array.from({ length: divisions + 1 }).map((_, i) => {
      const y = (i / divisions) * height;
      return (
        <div
          key={i}
          style={{ position: "absolute", top: y, left: 0, width, height: 1, backgroundColor: color }}
        />
      );
    })}
  </>
);

const YAxisLabels: React.FC<{
  maxValue: number;
  height: number;
  divisions?: number;
  format?: (v: number) => string;
}> = ({ maxValue, height, divisions = 4, format = (v) => v.toLocaleString() }) => (
  <>
    {Array.from({ length: divisions + 1 }).map((_, i) => {
      const pct = 1 - i / divisions;
      const value = maxValue * pct;
      return (
        <div
          key={i}
          style={{
            position: "absolute",
            top: (i / divisions) * height - 8,
            right: 12,
            fontSize: 13,
            fontFamily: "Inter, sans-serif",
            color: "#94a3b8",
          }}
        >
          {format(value)}
        </div>
      );
    })}
  </>
);
```

---

## 12. Data-Driven Composition (Zod Schema + inputProps)

Pass data dynamically via `inputProps` with Zod validation.

```tsx
import { z } from "zod";
import { Composition } from "remotion";

export const chartDataSchema = z.object({
  title: z.string(),
  subtitle: z.string().optional(),
  data: z.array(
    z.object({
      label: z.string(),
      value: z.number(),
      color: z.string().optional(),
    })
  ),
  chartType: z.enum(["bar", "line", "pie", "donut"]).default("bar"),
});

type ChartProps = z.infer<typeof chartDataSchema>;

// In Root.tsx:
// <Composition
//   id="DynamicChart"
//   component={DynamicChart}
//   schema={chartDataSchema}
//   durationInFrames={300}
//   fps={30}
//   width={1920}
//   height={1080}
//   defaultProps={{
//     title: "Sales by Month",
//     data: [
//       { label: "Jan", value: 120 },
//       { label: "Feb", value: 180 },
//       { label: "Mar", value: 250 },
//     ],
//     chartType: "bar",
//   }}
// />

// Render with custom data:
// npx remotion render src/index.ts DynamicChart out/chart.mp4 \
//   --props='{"title":"Revenue","data":[{"label":"Q1","value":500},{"label":"Q2","value":750}]}'
```