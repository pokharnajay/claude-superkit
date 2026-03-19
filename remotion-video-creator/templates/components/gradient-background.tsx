import React from 'react';
import { useCurrentFrame, useVideoConfig, interpolate } from 'remotion';

interface GradientBackgroundProps {
  colors: string[];
  angle?: number;
  animateAngle?: boolean;
  animateColors?: boolean;
  speed?: number;
  type?: 'linear' | 'radial';
}

export const GradientBackground: React.FC<GradientBackgroundProps> = ({
  colors,
  angle = 135,
  animateAngle = false,
  animateColors = false,
  speed = 1,
  type = 'linear',
}) => {
  const frame = useCurrentFrame();
  const { durationInFrames } = useVideoConfig();

  // Animate angle rotation
  const currentAngle = animateAngle
    ? angle + interpolate(frame, [0, durationInFrames], [0, 360 * speed], { extrapolateRight: 'clamp' })
    : angle;

  // Animate color positions by shifting stops
  const shift = animateColors
    ? interpolate(frame, [0, durationInFrames], [0, 100 * speed], { extrapolateRight: 'clamp' })
    : 0;

  const buildStops = (): string => {
    const len = colors.length;
    return colors
      .map((c, i) => {
        const basePos = (i / (len - 1)) * 100;
        const pos = (basePos + shift) % 100;
        return `${c} ${pos}%`;
      })
      .join(', ');
  };

  const gradient =
    type === 'radial'
      ? `radial-gradient(circle, ${buildStops()})`
      : `linear-gradient(${currentAngle}deg, ${buildStops()})`;

  return (
    <div
      style={{
        position: 'absolute',
        inset: 0,
        background: gradient,
      }}
    />
  );
};