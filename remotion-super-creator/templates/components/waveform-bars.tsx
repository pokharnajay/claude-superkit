/**
 * WaveformBars — Noise-driven audio waveform visualization
 *
 * Bars pulse with organic noise, creating a "living" waveform effect.
 * Perfect for audiogram videos, voice AI scenes, or music visualizers.
 *
 * Usage:
 * <WaveformBars barCount={48} delay={10} color="#3FC4C4" maxHeight={180} width={860} />
 */
import React from "react";
import { useCurrentFrame, useVideoConfig, interpolate } from "remotion";
import { noise2D } from "@remotion/noise";

interface Props {
  barCount?: number;
  delay?: number;
  color?: string;
  maxHeight?: number;
  width?: number;
}

export const WaveformBars: React.FC<Props> = ({
  barCount = 48,
  delay = 0,
  color = "#3FC4C4",
  maxHeight = 160,
  width = 800,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = (frame - delay) / fps;
  const active = frame >= delay;
  const CLAMP = { extrapolateLeft: "clamp" as const, extrapolateRight: "clamp" as const };

  const barWidth = (width / barCount) * 0.65;
  const gap = (width / barCount) * 0.35;

  return (
    <div style={{ display: "flex", alignItems: "center", justifyContent: "center", gap, height: maxHeight, width }}>
      {Array.from({ length: barCount }, (_, i) => {
        const n = active ? noise2D("wave", i * 0.15, t * 2.5) : 0;
        const normalized = (n + 1) / 2;
        const entrance = interpolate(frame - delay, [0, 15 + i * 0.5], [0, 1], CLAMP);
        const h = normalized * maxHeight * 0.8 * entrance + maxHeight * 0.05;
        const hue = (i / barCount) * 40;
        return (
          <div key={i} style={{ width: barWidth, height: h, borderRadius: barWidth, background: `linear-gradient(to top, ${color}, ${color}88)`, filter: `hue-rotate(${hue}deg)`, opacity: 0.5 + normalized * 0.5 }} />
        );
      })}
    </div>
  );
};
