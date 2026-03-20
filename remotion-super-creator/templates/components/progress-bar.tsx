import React from 'react';
import { useCurrentFrame, useVideoConfig, interpolate, spring } from 'remotion';

interface ProgressBarProps {
  progress?: number | 'auto';
  color?: string;
  backgroundColor?: string;
  height?: number;
  position?: 'top' | 'bottom';
  borderRadius?: number;
  margin?: number;
}

export const ProgressBar: React.FC<ProgressBarProps> = ({
  progress = 'auto',
  color = '#FFFFFF',
  backgroundColor = 'rgba(255,255,255,0.2)',
  height = 6,
  position = 'bottom',
  borderRadius = 3,
  margin = 0,
}) => {
  const frame = useCurrentFrame();
  const { durationInFrames, fps } = useVideoConfig();

  const resolvedProgress =
    progress === 'auto'
      ? interpolate(frame, [0, durationInFrames - 1], [0, 1], {
          extrapolateLeft: 'clamp',
          extrapolateRight: 'clamp',
        })
      : progress;

  // Smooth entrance animation
  const barOpacity = interpolate(frame, [0, 15], [0, 1], {
    extrapolateRight: 'clamp',
  });

  const barScale = spring({
    frame,
    fps,
    config: { damping: 15, stiffness: 120 },
  });

  return (
    <div
      style={{
        position: 'absolute',
        left: margin,
        right: margin,
        [position]: margin,
        height,
        backgroundColor,
        borderRadius,
        overflow: 'hidden',
        opacity: barOpacity,
        transform: `scaleX(${barScale})`,
        transformOrigin: 'left center',
      }}
    >
      <div
        style={{
          width: `${resolvedProgress * 100}%`,
          height: '100%',
          backgroundColor: color,
          borderRadius,
          transition: progress === 'auto' ? 'none' : 'width 0.1s ease-out',
        }}
      />
    </div>
  );
};