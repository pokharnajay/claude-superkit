/**
 * AccentLine — Animated horizontal accent line that expands from center
 *
 * A recurring visual motif for scene breaks, section dividers, and emphasis.
 * Subtle glow matches accent color.
 *
 * Usage:
 * <AccentLine delay={10} color="#C4703F" width={120} />
 */
import React from "react";
import { useCurrentFrame, useVideoConfig, spring, interpolate } from "remotion";

interface Props {
  delay?: number;
  color?: string;
  width?: number;
  height?: number;
}

export const AccentLine: React.FC<Props> = ({
  delay = 0,
  color = "#C4703F",
  width = 120,
  height = 3,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const CLAMP = { extrapolateLeft: "clamp" as const, extrapolateRight: "clamp" as const };

  const s = spring({ frame: frame - delay, fps, config: { damping: 16, stiffness: 80 } });
  const w = interpolate(s, [0, 1], [0, width], CLAMP);
  const opacity = interpolate(s, [0, 0.3], [0, 1], CLAMP);

  return (
    <div style={{ width: w, height, borderRadius: height, background: color, boxShadow: `0 0 20px ${color}55`, opacity, margin: "0 auto" }} />
  );
};
