import React from 'react';
import { useCurrentFrame, useVideoConfig, interpolate, spring } from 'remotion';

interface SplitScreenProps {
  left: React.ReactNode;
  right: React.ReactNode;
  ratio?: number;
  gap?: number;
  direction?: 'horizontal' | 'vertical';
  dividerColor?: string;
  dividerWidth?: number;
  animateIn?: boolean;
}

export const SplitScreen: React.FC<SplitScreenProps> = ({
  left,
  right,
  ratio = 0.5,
  gap = 0,
  direction = 'horizontal',
  dividerColor,
  dividerWidth = 2,
  animateIn = false,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const isHorizontal = direction === 'horizontal';

  // Animation progress (0 = hidden, 1 = fully visible)
  const revealProgress = animateIn
    ? spring({ frame, fps, config: { damping: 14, stiffness: 120 } })
    : 1;

  // Divider slides in first, then panels reveal outward
  const dividerProgress = animateIn
    ? spring({ frame, fps, config: { damping: 12, stiffness: 200 } })
    : 1;

  const leftClip = animateIn
    ? interpolate(revealProgress, [0, 1], [isHorizontal ? 100 : 100, 0])
    : 0;
  const rightClip = animateIn
    ? interpolate(revealProgress, [0, 1], [isHorizontal ? 100 : 100, 0])
    : 0;

  const leftSize = `calc(${ratio * 100}% - ${gap / 2}px)`;
  const rightSize = `calc(${(1 - ratio) * 100}% - ${gap / 2}px)`;

  const containerStyle: React.CSSProperties = {
    position: 'absolute',
    inset: 0,
    display: 'flex',
    flexDirection: isHorizontal ? 'row' : 'column',
    overflow: 'hidden',
  };

  const leftPanelStyle: React.CSSProperties = {
    [isHorizontal ? 'width' : 'height']: leftSize,
    overflow: 'hidden',
    position: 'relative',
    clipPath: isHorizontal
      ? `inset(0 ${leftClip}% 0 0)`
      : `inset(0 0 ${leftClip}% 0)`,
  };

  const rightPanelStyle: React.CSSProperties = {
    [isHorizontal ? 'width' : 'height']: rightSize,
    overflow: 'hidden',
    position: 'relative',
    clipPath: isHorizontal
      ? `inset(0 0 0 ${rightClip}%)`
      : `inset(${rightClip}% 0 0 0)`,
  };

  const showDivider = dividerColor && dividerWidth > 0;

  const dividerStyle: React.CSSProperties = showDivider
    ? {
        [isHorizontal ? 'width' : 'height']: dividerWidth,
        [isHorizontal ? 'marginLeft' : 'marginTop']: gap / 2 - dividerWidth / 2,
        [isHorizontal ? 'marginRight' : 'marginBottom']: gap / 2 - dividerWidth / 2,
        backgroundColor: dividerColor,
        flexShrink: 0,
        transform: isHorizontal
          ? `scaleY(${dividerProgress})`
          : `scaleX(${dividerProgress})`,
        transformOrigin: 'center',
      }
    : {
        [isHorizontal ? 'width' : 'height']: gap,
        flexShrink: 0,
      };

  return (
    <div style={containerStyle}>
      <div style={leftPanelStyle}>{left}</div>
      <div style={dividerStyle} />
      <div style={rightPanelStyle}>{right}</div>
    </div>
  );
};