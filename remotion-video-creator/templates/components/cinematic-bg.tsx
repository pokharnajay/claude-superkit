/**
 * CinematicBg — Layered cinematic background with grid, gradient orbs, particles, and vignette
 *
 * IMPORTANT: Vary these per scene to avoid repetition:
 * - seed: drives particle positions and orb placement (unique per scene)
 * - accentColor: matches scene mood (copper, teal, purple, etc.)
 * - gridOpacity: 0.02 for minimal scenes, 0.05 for tech/energy scenes
 * - orbCount: 2 for quiet scenes, 3-4 for energetic scenes
 * - particleCount: 20 for sparse/mystery, 60 for dense/energy
 * - gridAngle: rotate grid for variety (0, 15, 30, 45 degrees)
 * - gridSize: vary cell size (40px tight, 60px default, 100px open)
 *
 * Usage:
 * <CinematicBg seed={1} accentColor="#C4703F" orbCount={3} gridOpacity={0.03} />
 */
import React from "react";
import { AbsoluteFill, useCurrentFrame, useVideoConfig, interpolate } from "remotion";
import { noise2D } from "@remotion/noise";

interface Props {
  accentColor?: string;
  orbCount?: number;
  seed?: number;
  gridOpacity?: number;
  particleCount?: number;
  gridAngle?: number;
  gridSize?: number;
  vignetteIntensity?: number;
}

function srand(seed: number): number {
  const x = Math.sin(seed * 127.1 + 311.7) * 43758.5453;
  return x - Math.floor(x);
}

export const CinematicBg: React.FC<Props> = ({
  accentColor = "#C4703F",
  orbCount = 3,
  seed = 0,
  gridOpacity = 0.04,
  particleCount = 40,
  gridAngle = 0,
  gridSize = 60,
  vignetteIntensity = 0.5,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = frame / fps;

  const BG = "#08080D";
  const FG = "#F5F0EB";
  const CLAMP = { extrapolateLeft: "clamp" as const, extrapolateRight: "clamp" as const };

  // Orbs — each uniquely positioned and sized per seed
  const orbs = Array.from({ length: orbCount }, (_, i) => {
    const baseSeed = seed + i * 100;
    const cx = srand(baseSeed + 1) * 100;
    const cy = srand(baseSeed + 2) * 100;
    const size = 300 + srand(baseSeed + 3) * 400;
    const driftX = noise2D("orbX" + i, t * 0.08, i * 0.5) * 60;
    const driftY = noise2D("orbY" + i, t * 0.06, i * 0.5) * 40;
    const opacity = 0.08 + srand(baseSeed + 4) * 0.12;
    return { cx, cy, size, driftX, driftY, opacity };
  });

  // Particles — seeded positions with noise-driven drift
  const particles = Array.from({ length: particleCount }, (_, i) => {
    const ps = seed + 500 + i * 10;
    const x = srand(ps + 1) * 100;
    const baseY = srand(ps + 2) * 100;
    const drift = noise2D("p" + i, t * 0.15 + i * 0.3, 0) * 2;
    const yShift = (t * (0.5 + srand(ps + 3) * 1.5)) % 110;
    const y = (baseY + yShift + drift * 10) % 110 - 5;
    const sz = 1 + srand(ps + 4) * 2.5;
    const op = 0.06 + srand(ps + 5) * 0.18;
    return { x, y, sz, op };
  });

  const bgFade = interpolate(frame, [0, 15], [0, 1], CLAMP);

  return (
    <AbsoluteFill style={{ opacity: bgFade }}>
      {/* Base gradient */}
      <AbsoluteFill
        style={{
          background: `radial-gradient(ellipse at 50% 40%, #12121A 0%, ${BG} 70%)`,
        }}
      />

      {/* Animated grid — rotate for variety */}
      <AbsoluteFill
        style={{
          opacity: gridOpacity,
          backgroundImage: `
            linear-gradient(rgba(255,255,255,0.3) 1px, transparent 1px),
            linear-gradient(90deg, rgba(255,255,255,0.3) 1px, transparent 1px)
          `,
          backgroundSize: `${gridSize}px ${gridSize}px`,
          backgroundPosition: `0 ${-frame * 0.3}px`,
          transform: gridAngle ? `rotate(${gridAngle}deg) scale(1.2)` : undefined,
        }}
      />

      {/* Gradient orbs */}
      {orbs.map((orb, i) => (
        <div
          key={i}
          style={{
            position: "absolute",
            left: `${orb.cx + orb.driftX * 0.1}%`,
            top: `${orb.cy + orb.driftY * 0.1}%`,
            width: orb.size,
            height: orb.size,
            borderRadius: "50%",
            background: `radial-gradient(circle, ${accentColor} 0%, transparent 70%)`,
            opacity: orb.opacity,
            filter: `blur(${orb.size * 0.4}px)`,
            transform: "translate(-50%, -50%)",
            pointerEvents: "none",
          }}
        />
      ))}

      {/* Particles */}
      {particles.map((p, i) => (
        <div
          key={i}
          style={{
            position: "absolute",
            left: `${p.x}%`,
            top: `${p.y}%`,
            width: p.sz,
            height: p.sz,
            borderRadius: "50%",
            background: FG,
            opacity: p.op,
            pointerEvents: "none",
          }}
        />
      ))}

      {/* Vignette */}
      <AbsoluteFill
        style={{
          background: `radial-gradient(ellipse at 50% 50%, transparent 40%, rgba(0,0,0,${vignetteIntensity}) 100%)`,
          pointerEvents: "none",
        }}
      />
    </AbsoluteFill>
  );
};
