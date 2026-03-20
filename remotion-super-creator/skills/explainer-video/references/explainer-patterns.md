# Explainer Video -- Code Patterns

Copy-paste-ready components for product demos, tutorials, and explainer videos.

---

## 1. Browser Chrome Mockup

Wraps content in a browser-style frame with URL bar, traffic lights, and content area.

```tsx
import { AbsoluteFill, useCurrentFrame, useVideoConfig, interpolate, spring } from "remotion";

const BrowserMockup: React.FC<{
  url: string;
  children: React.ReactNode;
  width?: number;
  height?: number;
}> = ({ url, children, width = 1400, height = 820 }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const scale = spring({ frame, fps, config: { damping: 14, stiffness: 180 } });

  return (
    <div
      style={{
        transform: `scale(${scale})`,
        width,
        borderRadius: 12,
        overflow: "hidden",
        boxShadow: "0 8px 40px rgba(0,0,0,0.15)",
      }}
    >
      {/* Title bar */}
      <div
        style={{
          height: 48,
          backgroundColor: "#f1f3f4",
          display: "flex",
          alignItems: "center",
          padding: "0 16px",
          gap: 8,
        }}
      >
        {/* Traffic lights */}
        <div style={{ width: 12, height: 12, borderRadius: "50%", backgroundColor: "#ff5f57" }} />
        <div style={{ width: 12, height: 12, borderRadius: "50%", backgroundColor: "#febd2e" }} />
        <div style={{ width: 12, height: 12, borderRadius: "50%", backgroundColor: "#28c840" }} />
        {/* URL bar */}
        <div
          style={{
            flex: 1,
            height: 28,
            backgroundColor: "#fff",
            borderRadius: 14,
            display: "flex",
            alignItems: "center",
            paddingLeft: 14,
            marginLeft: 12,
            fontSize: 13,
            fontFamily: "Inter, sans-serif",
            color: "#666",
          }}
        >
          {url}
        </div>
      </div>
      {/* Content area */}
      <div
        style={{
          height,
          backgroundColor: "#fff",
          position: "relative",
          overflow: "hidden",
        }}
      >
        {children}
      </div>
    </div>
  );
};
```

---

## 2. Phone Mockup (iPhone Style)

iPhone-style frame with notch, status bar, and screen content area.

```tsx
const PhoneMockup: React.FC<{
  children: React.ReactNode;
  width?: number;
}> = ({ children, width = 360 }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const scale = spring({ frame, fps, config: { damping: 14 } });
  const height = width * (19.5 / 9); // iPhone aspect ratio

  return (
    <div
      style={{
        transform: `scale(${scale})`,
        width: width + 24,
        height: height + 24,
        backgroundColor: "#1a1a1a",
        borderRadius: 40,
        padding: 12,
        boxShadow: "0 8px 40px rgba(0,0,0,0.2)",
      }}
    >
      {/* Screen */}
      <div
        style={{
          width,
          height,
          borderRadius: 28,
          overflow: "hidden",
          backgroundColor: "#fff",
          position: "relative",
        }}
      >
        {/* Notch */}
        <div
          style={{
            position: "absolute",
            top: 0,
            left: "50%",
            transform: "translateX(-50%)",
            width: 120,
            height: 30,
            backgroundColor: "#1a1a1a",
            borderRadius: "0 0 16px 16px",
            zIndex: 10,
          }}
        />
        {/* Content */}
        <div style={{ position: "absolute", inset: 0 }}>{children}</div>
      </div>
    </div>
  );
};
```

---

## 3. Callout Arrow (Animated SVG)

Animated line from a label to a target point with a circle indicator.

```tsx
const CalloutArrow: React.FC<{
  fromX: number;
  fromY: number;
  toX: number;
  toY: number;
  label: string;
  color?: string;
  delay?: number;
}> = ({ fromX, fromY, toX, toY, label, color = "#3b82f6", delay = 0 }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const progress = spring({ frame: frame - delay, fps, config: { damping: 14 } });

  const lineEndX = interpolate(progress, [0, 1], [fromX, toX]);
  const lineEndY = interpolate(progress, [0, 1], [fromY, toY]);

  return (
    <>
      {/* Line */}
      <svg
        style={{ position: "absolute", inset: 0, zIndex: 20, pointerEvents: "none" }}
        width="100%"
        height="100%"
      >
        <line
          x1={fromX}
          y1={fromY}
          x2={lineEndX}
          y2={lineEndY}
          stroke={color}
          strokeWidth={2.5}
          strokeDasharray="6 4"
        />
      </svg>
      {/* Target circle */}
      <div
        style={{
          position: "absolute",
          left: toX - 16,
          top: toY - 16,
          width: 32,
          height: 32,
          borderRadius: "50%",
          border: `3px solid ${color}`,
          opacity: progress,
          transform: `scale(${progress})`,
          zIndex: 20,
        }}
      />
      {/* Label */}
      <div
        style={{
          position: "absolute",
          left: fromX - 80,
          top: fromY - 16,
          fontSize: 18,
          fontWeight: 700,
          fontFamily: "Inter, sans-serif",
          color,
          opacity: progress,
          whiteSpace: "nowrap",
          zIndex: 20,
        }}
      >
        {label}
      </div>
    </>
  );
};
```

---

## 4. Zoom-to-Detail

Scale and translate to focus on a specific region of a larger image or UI mockup.

```tsx
const ZoomToDetail: React.FC<{
  children: React.ReactNode;
  targetX: number; // 0-1 relative position
  targetY: number; // 0-1 relative position
  zoomScale?: number;
  startFrame?: number;
  duration?: number;
}> = ({ children, targetX, targetY, zoomScale = 2.5, startFrame = 0, duration = 30 }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const progress = spring({
    frame: frame - startFrame,
    fps,
    config: { damping: 15, stiffness: 120 },
  });

  const scale = interpolate(progress, [0, 1], [1, zoomScale]);
  // Translate to center the target area
  const translateX = interpolate(progress, [0, 1], [0, -(targetX - 0.5) * 100 * zoomScale]);
  const translateY = interpolate(progress, [0, 1], [0, -(targetY - 0.5) * 100 * zoomScale]);

  return (
    <div
      style={{
        width: "100%",
        height: "100%",
        overflow: "hidden",
        position: "relative",
      }}
    >
      <div
        style={{
          width: "100%",
          height: "100%",
          transform: `scale(${scale}) translate(${translateX}%, ${translateY}%)`,
          transformOrigin: "center center",
        }}
      >
        {children}
      </div>
    </div>
  );
};
```

---

## 5. Step Counter with Progress

Shows "Step 1 of 3" with a visual progress bar.

```tsx
const StepCounter: React.FC<{
  current: number;
  total: number;
  color?: string;
}> = ({ current, total, color = "#3b82f6" }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const s = spring({ frame, fps, config: { damping: 14 } });
  const progress = current / total;

  return (
    <div style={{ position: "absolute", top: 50, left: 80, right: 80, zIndex: 20 }}>
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          marginBottom: 12,
        }}
      >
        <div style={{ fontSize: 18, fontWeight: 700, fontFamily: "Inter, sans-serif", color: "#1a1a1a", opacity: s }}>
          Step {current} of {total}
        </div>
      </div>
      <div
        style={{
          height: 4,
          backgroundColor: "#e5e7eb",
          borderRadius: 2,
          overflow: "hidden",
        }}
      >
        <div
          style={{
            width: `${progress * 100 * s}%`,
            height: "100%",
            backgroundColor: color,
            borderRadius: 2,
          }}
        />
      </div>
    </div>
  );
};
```

---

## 6. Feature Card with Icon Bounce

Animated card with icon, title, and description. Spring entrance with staggered elements.

```tsx
const FeatureCard: React.FC<{
  icon: string;
  title: string;
  description: string;
  delay?: number;
  accentColor?: string;
}> = ({ icon, title, description, delay = 0, accentColor = "#3b82f6" }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const cardS = spring({ frame: frame - delay, fps, config: { damping: 12 } });
  const iconS = spring({ frame: frame - delay - 8, fps, config: { damping: 8, stiffness: 200 } });
  const textS = spring({ frame: frame - delay - 15, fps, config: { damping: 14 } });

  return (
    <div
      style={{
        transform: `scale(${cardS}) translateY(${interpolate(cardS, [0, 1], [30, 0])}px)`,
        opacity: cardS,
        backgroundColor: "#ffffff",
        borderRadius: 16,
        padding: "40px 32px",
        boxShadow: "0 2px 16px rgba(0,0,0,0.06)",
        textAlign: "center",
        width: 280,
      }}
    >
      <div style={{ fontSize: 48, transform: `scale(${iconS})`, marginBottom: 16 }}>{icon}</div>
      <div
        style={{
          fontSize: 22,
          fontWeight: 800,
          fontFamily: "Inter, sans-serif",
          color: "#1a1a1a",
          marginBottom: 12,
          opacity: textS,
        }}
      >
        {title}
      </div>
      <div
        style={{
          fontSize: 16,
          fontWeight: 400,
          fontFamily: "Inter, sans-serif",
          color: "#6b7280",
          lineHeight: 1.5,
          opacity: textS,
        }}
      >
        {description}
      </div>
    </div>
  );
};
```

---

## 7. Comparison Layout (Side-by-Side)

Two-column comparison with divider and colored headers.

```tsx
const ComparisonLayout: React.FC<{
  leftTitle: string;
  rightTitle: string;
  leftItems: string[];
  rightItems: string[];
  leftColor?: string;
  rightColor?: string;
}> = ({ leftTitle, rightTitle, leftItems, rightItems, leftColor = "#ef4444", rightColor = "#22c55e" }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  return (
    <AbsoluteFill style={{ backgroundColor: "#fafafa", justifyContent: "center", alignItems: "center" }}>
      <div style={{ display: "flex", gap: 40, padding: "0 80px" }}>
        {/* Left column */}
        <div style={{ flex: 1 }}>
          <div style={{ fontSize: 32, fontWeight: 800, fontFamily: "Inter, sans-serif", color: leftColor, marginBottom: 30 }}>
            {leftTitle}
          </div>
          {leftItems.map((item, i) => {
            const s = spring({ frame: frame - 10 - i * 8, fps, config: { damping: 14 } });
            return (
              <div
                key={i}
                style={{
                  fontSize: 20,
                  fontWeight: 500,
                  fontFamily: "Inter, sans-serif",
                  color: "#374151",
                  marginBottom: 16,
                  opacity: s,
                  transform: `translateX(${interpolate(s, [0, 1], [-30, 0])}px)`,
                  display: "flex",
                  gap: 10,
                }}
              >
                <span style={{ color: leftColor }}>&#x2717;</span>
                {item}
              </div>
            );
          })}
        </div>
        {/* Divider */}
        <div style={{ width: 2, backgroundColor: "#e5e7eb", borderRadius: 1 }} />
        {/* Right column */}
        <div style={{ flex: 1 }}>
          <div style={{ fontSize: 32, fontWeight: 800, fontFamily: "Inter, sans-serif", color: rightColor, marginBottom: 30 }}>
            {rightTitle}
          </div>
          {rightItems.map((item, i) => {
            const s = spring({ frame: frame - 10 - i * 8, fps, config: { damping: 14 } });
            return (
              <div
                key={i}
                style={{
                  fontSize: 20,
                  fontWeight: 500,
                  fontFamily: "Inter, sans-serif",
                  color: "#374151",
                  marginBottom: 16,
                  opacity: s,
                  transform: `translateX(${interpolate(s, [0, 1], [30, 0])}px)`,
                  display: "flex",
                  gap: 10,
                }}
              >
                <span style={{ color: rightColor }}>&#x2713;</span>
                {item}
              </div>
            );
          })}
        </div>
      </div>
    </AbsoluteFill>
  );
};
```

---

## 8. Pricing Tier Animation

Cards scale in staggered with pricing information.

```tsx
const PricingTiers: React.FC<{
  tiers: { name: string; price: string; features: string[]; highlighted?: boolean }[];
}> = ({ tiers }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  return (
    <AbsoluteFill style={{ backgroundColor: "#fafafa", justifyContent: "center", alignItems: "center" }}>
      <div style={{ display: "flex", gap: 24, alignItems: "center" }}>
        {tiers.map((tier, i) => {
          const delay = i * 10;
          const s = spring({ frame: frame - delay, fps, config: { damping: 12 } });
          const isHighlighted = tier.highlighted;

          return (
            <div
              key={i}
              style={{
                transform: `scale(${s}) translateY(${interpolate(s, [0, 1], [40, 0])}px)`,
                opacity: s,
                backgroundColor: isHighlighted ? "#3b82f6" : "#fff",
                borderRadius: 16,
                padding: "36px 32px",
                boxShadow: isHighlighted ? "0 8px 32px rgba(59,130,246,0.3)" : "0 2px 12px rgba(0,0,0,0.06)",
                width: 260,
                textAlign: "center",
              }}
            >
              <div
                style={{
                  fontSize: 20,
                  fontWeight: 700,
                  fontFamily: "Inter, sans-serif",
                  color: isHighlighted ? "rgba(255,255,255,0.8)" : "#6b7280",
                  marginBottom: 8,
                }}
              >
                {tier.name}
              </div>
              <div
                style={{
                  fontSize: 44,
                  fontWeight: 900,
                  fontFamily: "Inter, sans-serif",
                  color: isHighlighted ? "#fff" : "#1a1a1a",
                  marginBottom: 24,
                }}
              >
                {tier.price}
              </div>
              {tier.features.map((feat, j) => (
                <div
                  key={j}
                  style={{
                    fontSize: 15,
                    fontFamily: "Inter, sans-serif",
                    color: isHighlighted ? "rgba(255,255,255,0.85)" : "#6b7280",
                    marginBottom: 10,
                  }}
                >
                  {feat}
                </div>
              ))}
            </div>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};
```

---

## 9. CTA Button with Pulse

Pulsing call-to-action button that draws the eye.

```tsx
const CTAButton: React.FC<{
  text: string;
  color?: string;
  delay?: number;
}> = ({ text, color = "#3b82f6", delay = 0 }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const s = spring({ frame: frame - delay, fps, config: { damping: 10 } });
  const pulse = 1 + Math.sin(frame * 0.1) * 0.03;

  return (
    <div
      style={{
        transform: `scale(${s * pulse})`,
        backgroundColor: color,
        color: "#fff",
        fontSize: 28,
        fontWeight: 700,
        fontFamily: "Inter, sans-serif",
        padding: "18px 52px",
        borderRadius: 12,
        boxShadow: `0 4px 20px ${color}44`,
        display: "inline-block",
      }}
    >
      {text}
    </div>
  );
};
```

---

## 10. Tooltip / Annotation Bubble

Speech bubble with pointer triangle. Position next to UI elements.

```tsx
const TooltipBubble: React.FC<{
  text: string;
  x: number;
  y: number;
  pointerDirection?: "up" | "down" | "left" | "right";
  delay?: number;
}> = ({ text, x, y, pointerDirection = "down", delay = 0 }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const s = spring({ frame: frame - delay, fps, config: { damping: 10, stiffness: 200 } });

  const pointerStyles: Record<string, React.CSSProperties> = {
    down: { bottom: -8, left: "50%", transform: "translateX(-50%) rotate(45deg)" },
    up: { top: -8, left: "50%", transform: "translateX(-50%) rotate(45deg)" },
    left: { left: -8, top: "50%", transform: "translateY(-50%) rotate(45deg)" },
    right: { right: -8, top: "50%", transform: "translateY(-50%) rotate(45deg)" },
  };

  return (
    <div
      style={{
        position: "absolute",
        left: x,
        top: y,
        transform: `scale(${s}) translateY(${interpolate(s, [0, 1], [10, 0])}px)`,
        opacity: s,
        zIndex: 30,
      }}
    >
      <div
        style={{
          backgroundColor: "#1a1a1a",
          color: "#fff",
          fontSize: 16,
          fontWeight: 600,
          fontFamily: "Inter, sans-serif",
          padding: "10px 18px",
          borderRadius: 8,
          whiteSpace: "nowrap",
          position: "relative",
        }}
      >
        {text}
        <div
          style={{
            position: "absolute",
            width: 14,
            height: 14,
            backgroundColor: "#1a1a1a",
            ...pointerStyles[pointerDirection],
          }}
        />
      </div>
    </div>
  );
};
```

---

## 11. Checkmark List (Animated)

Items appear one by one with animated checkmarks. Great for feature lists or benefits.

```tsx
const CheckmarkList: React.FC<{
  items: string[];
  delayPerItem?: number;
  checkColor?: string;
}> = ({ items, delayPerItem = 20, checkColor = "#22c55e" }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: 20, padding: "0 80px" }}>
      {items.map((item, i) => {
        const delay = i * delayPerItem;
        const s = spring({ frame: frame - delay, fps, config: { damping: 12 } });
        const checkS = spring({ frame: frame - delay - 5, fps, config: { damping: 8, stiffness: 200 } });

        if (frame < delay) return null;

        return (
          <div
            key={i}
            style={{
              display: "flex",
              alignItems: "center",
              gap: 16,
              opacity: s,
              transform: `translateX(${interpolate(s, [0, 1], [40, 0])}px)`,
            }}
          >
            {/* Checkmark circle */}
            <div
              style={{
                width: 32,
                height: 32,
                borderRadius: "50%",
                backgroundColor: checkColor,
                display: "flex",
                justifyContent: "center",
                alignItems: "center",
                transform: `scale(${checkS})`,
                flexShrink: 0,
              }}
            >
              <svg width="16" height="12" viewBox="0 0 16 12">
                <polyline
                  points="2,6 6,10 14,2"
                  fill="none"
                  stroke="#fff"
                  strokeWidth="2.5"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                />
              </svg>
            </div>
            <div
              style={{
                fontSize: 22,
                fontWeight: 600,
                fontFamily: "Inter, sans-serif",
                color: "#1a1a1a",
              }}
            >
              {item}
            </div>
          </div>
        );
      })}
    </div>
  );
};
```