/**
 * GlassCard — Glassmorphism card with spring entrance animation
 *
 * Professional glass effect: semi-transparent bg, backdrop blur, subtle border, accent glow.
 * Each card springs in from below with scale + opacity.
 *
 * Usage:
 * <GlassCard delay={10} width={800} glowColor="rgba(196,112,63,0.25)">
 *   <h2>Content here</h2>
 * </GlassCard>
 */
import React from "react";
import { useCurrentFrame, useVideoConfig, spring, interpolate } from "remotion";
import { makeTransform, translateY, scale } from "@remotion/animation-utils";

interface Props {
  children: React.ReactNode;
  delay?: number;
  width?: number | string;
  glowColor?: string;
  padding?: string;
  borderRadius?: number;
  style?: React.CSSProperties;
}

export const GlassCard: React.FC<Props> = ({
  children,
  delay = 0,
  width = "auto",
  glowColor = "rgba(196,112,63,0.35)",
  padding = "28px 32px",
  borderRadius = 20,
  style,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const entrance = spring({
    frame: frame - delay,
    fps,
    config: { damping: 14, stiffness: 120, mass: 0.8 },
  });

  const CLAMP = { extrapolateLeft: "clamp" as const, extrapolateRight: "clamp" as const };
  const yOffset = interpolate(entrance, [0, 1], [40, 0], CLAMP);
  const opacity = interpolate(entrance, [0, 1], [0, 1], CLAMP);

  return (
    <div
      style={{
        width,
        padding,
        borderRadius,
        background: "rgba(255,255,255,0.04)",
        border: "1px solid rgba(255,255,255,0.08)",
        backdropFilter: "blur(16px)",
        WebkitBackdropFilter: "blur(16px)",
        boxShadow: `0 0 40px ${glowColor}, inset 0 1px 0 rgba(255,255,255,0.05)`,
        opacity,
        transform: makeTransform([translateY(yOffset), scale(0.95 + entrance * 0.05)]),
        ...style,
      }}
    >
      {children}
    </div>
  );
};
