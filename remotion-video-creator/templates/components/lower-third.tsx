import React from 'react';
import { useCurrentFrame, useVideoConfig, interpolate, spring } from 'remotion';

interface LowerThirdProps {
  name: string;
  title?: string;
  accentColor?: string;
  textColor?: string;
  backgroundColor?: string;
  position?: 'left' | 'center';
  startFrame?: number;
  duration?: number;
  fontFamily?: string;
}

export const LowerThird: React.FC<LowerThirdProps> = ({
  name,
  title,
  accentColor = '#FF6B35',
  textColor = '#FFFFFF',
  backgroundColor = 'rgba(0,0,0,0.75)',
  position = 'left',
  startFrame = 0,
  duration = 90,
  fontFamily = 'Inter, sans-serif',
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const f = frame - startFrame;

  if (f < 0 || f > duration) return null;

  // Accent bar slides in first
  const barProgress = spring({
    frame: f,
    fps,
    config: { damping: 14, stiffness: 180 },
  });

  // Background panel slides in after a short delay
  const panelDelay = 5;
  const panelF = Math.max(0, f - panelDelay);
  const panelProgress = spring({
    frame: panelF,
    fps,
    config: { damping: 14, stiffness: 150 },
  });

  // Text fades in after panel
  const textOpacity = interpolate(f, [panelDelay + 5, panelDelay + 15], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  // Exit animation: slide out in the last 15 frames
  const exitStart = duration - 15;
  const exitProgress =
    f >= exitStart
      ? interpolate(f, [exitStart, duration], [0, 1], {
          extrapolateLeft: 'clamp',
          extrapolateRight: 'clamp',
        })
      : 0;

  const slideOut = interpolate(exitProgress, [0, 1], [0, -120]);

  return (
    <div
      style={{
        position: 'absolute',
        bottom: 80,
        left: position === 'left' ? 60 : '50%',
        transform: position === 'center' ? `translateX(-50%) translateX(${slideOut}px)` : `translateX(${slideOut}px)`,
        display: 'flex',
        flexDirection: 'row',
        alignItems: 'stretch',
        fontFamily,
        opacity: 1 - exitProgress,
      }}
    >
      {/* Accent bar */}
      <div
        style={{
          width: 5,
          backgroundColor: accentColor,
          transform: `scaleY(${barProgress})`,
          transformOrigin: 'bottom',
          borderRadius: 2,
        }}
      />

      {/* Content panel */}
      <div
        style={{
          backgroundColor,
          padding: '12px 28px',
          marginLeft: 0,
          transform: `scaleX(${panelProgress})`,
          transformOrigin: 'left',
          backdropFilter: 'blur(8px)',
          borderRadius: '0 6px 6px 0',
          overflow: 'hidden',
        }}
      >
        <div
          style={{
            opacity: textOpacity,
            whiteSpace: 'nowrap',
          }}
        >
          <div
            style={{
              fontSize: 28,
              fontWeight: 700,
              color: textColor,
              lineHeight: 1.3,
            }}
          >
            {name}
          </div>
          {title && (
            <div
              style={{
                fontSize: 18,
                fontWeight: 400,
                color: accentColor,
                lineHeight: 1.3,
                marginTop: 2,
              }}
            >
              {title}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};