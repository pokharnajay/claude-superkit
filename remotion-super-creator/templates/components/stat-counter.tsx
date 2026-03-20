/**
 * StatCounter — Animated number counter with spring physics
 *
 * Numbers count up from 0 to target value using spring interpolation.
 * Clean label underneath with uppercase letterSpacing.
 *
 * Usage:
 * <StatCounter value={51} label="Skills" delay={10} color="#C4703F" suffix="+" />
 */
import React from "react";
import { useCurrentFrame, useVideoConfig, spring, interpolate } from "remotion";

interface Props {
  value: number;
  label: string;
  delay?: number;
  color?: string;
  fontSize?: number;
  suffix?: string;
  fontFamily?: string;
}

export const StatCounter: React.FC<Props> = ({
  value,
  label,
  delay = 0,
  color = "#C4703F",
  fontSize = 72,
  suffix = "",
  fontFamily = "JetBrains Mono",
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const CLAMP = { extrapolateLeft: "clamp" as const, extrapolateRight: "clamp" as const };

  const s = spring({ frame: frame - delay, fps, config: { damping: 18, stiffness: 60, mass: 0.8 } });
  const displayNum = Math.round(interpolate(s, [0, 1], [0, value], CLAMP));
  const scaleVal = interpolate(s, [0, 0.5, 1], [0.6, 1.08, 1], CLAMP);
  const opacity = interpolate(s, [0, 0.3], [0, 1], CLAMP);

  return (
    <div style={{ textAlign: "center", opacity, transform: `scale(${scaleVal})` }}>
      <div style={{ fontFamily, fontSize, fontWeight: 800, color, lineHeight: 1, letterSpacing: -2 }}>
        {displayNum}{suffix}
      </div>
      <div style={{ fontFamily: "Source Sans 3", fontSize: 20, color: "#7A756F", marginTop: 8, fontWeight: 400, textTransform: "uppercase", letterSpacing: 3 }}>
        {label}
      </div>
    </div>
  );
};
