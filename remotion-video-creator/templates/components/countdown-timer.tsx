import React from 'react';
import { useCurrentFrame, useVideoConfig, interpolate, spring } from 'remotion';

interface CountdownTimerProps {
  from: number;
  to?: number;
  fontSize?: number;
  fontFamily?: string;
  color?: string;
  accentColor?: string;
  showLabel?: boolean;
}

export const CountdownTimer: React.FC<CountdownTimerProps> = ({
  from,
  to = 0,
  fontSize = 120,
  fontFamily = 'Inter, sans-serif',
  color = '#FFFFFF',
  accentColor = '#FF4444',
  showLabel = false,
}) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();

  const totalSteps = from - to;
  const framesPerStep = Math.floor(durationInFrames / totalSteps);

  // Current countdown value
  const currentStep = Math.min(Math.floor(frame / framesPerStep), totalSteps - 1);
  const currentNumber = from - currentStep;

  // Frame within the current step (for per-tick animation)
  const stepFrame = frame - currentStep * framesPerStep;

  // Spring scale on each new number
  const scaleSpring = spring({
    frame: stepFrame,
    fps,
    config: { damping: 8, stiffness: 200 },
  });
  const scale = interpolate(scaleSpring, [0, 1], [1.4, 1]);

  // Flash effect on tick: bright accent color fades to normal
  const flashOpacity = interpolate(stepFrame, [0, 10], [1, 0], {
    extrapolateRight: 'clamp',
  });

  // Gentle pulse ring
  const ringScale = interpolate(stepFrame, [0, framesPerStep * 0.6], [0.8, 1.3], {
    extrapolateRight: 'clamp',
  });
  const ringOpacity = interpolate(stepFrame, [0, framesPerStep * 0.6], [0.4, 0], {
    extrapolateRight: 'clamp',
  });

  return (
    <div
      style={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        position: 'relative',
      }}
    >
      {/* Pulse ring */}
      <div
        style={{
          position: 'absolute',
          width: fontSize * 1.4,
          height: fontSize * 1.4,
          borderRadius: '50%',
          border: `3px solid ${accentColor}`,
          opacity: ringOpacity,
          transform: `scale(${ringScale})`,
        }}
      />

      {/* Number */}
      <div
        style={{
          fontSize,
          fontFamily,
          fontWeight: 900,
          color,
          transform: `scale(${scale})`,
          lineHeight: 1,
          position: 'relative',
          fontVariantNumeric: 'tabular-nums',
        }}
      >
        {/* Flash overlay */}
        <span
          style={{
            position: 'absolute',
            inset: 0,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            color: accentColor,
            opacity: flashOpacity,
          }}
        >
          {currentNumber}
        </span>
        {currentNumber}
      </div>

      {showLabel && (
        <div
          style={{
            fontSize: fontSize * 0.18,
            fontFamily,
            fontWeight: 500,
            color,
            opacity: 0.6,
            marginTop: fontSize * 0.15,
            letterSpacing: '0.1em',
            textTransform: 'uppercase',
          }}
        >
          seconds
        </div>
      )}
    </div>
  );
};