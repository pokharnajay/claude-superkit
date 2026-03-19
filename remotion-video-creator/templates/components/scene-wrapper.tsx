import React from 'react';
import { useCurrentFrame, useVideoConfig, interpolate, spring } from 'remotion';

type TransitionType = 'fade' | 'slideUp' | 'slideDown' | 'slideLeft' | 'slideRight' | 'scale' | 'none';

interface SceneWrapperProps {
  children: React.ReactNode;
  enterAnimation?: TransitionType;
  exitAnimation?: TransitionType;
  enterDuration?: number;
  exitDuration?: number;
  backgroundColor?: string;
  padding?: number;
}

const getTransformAndOpacity = (
  animation: TransitionType,
  progress: number, // 0 = hidden, 1 = fully visible
): { opacity: number; transform: string } => {
  switch (animation) {
    case 'none':
      return { opacity: 1, transform: 'none' };
    case 'fade':
      return { opacity: progress, transform: 'none' };
    case 'slideUp':
      return {
        opacity: progress,
        transform: `translateY(${interpolate(progress, [0, 1], [60, 0])}px)`,
      };
    case 'slideDown':
      return {
        opacity: progress,
        transform: `translateY(${interpolate(progress, [0, 1], [-60, 0])}px)`,
      };
    case 'slideLeft':
      return {
        opacity: progress,
        transform: `translateX(${interpolate(progress, [0, 1], [80, 0])}px)`,
      };
    case 'slideRight':
      return {
        opacity: progress,
        transform: `translateX(${interpolate(progress, [0, 1], [-80, 0])}px)`,
      };
    case 'scale':
      return {
        opacity: progress,
        transform: `scale(${interpolate(progress, [0, 1], [0.8, 1])})`,
      };
  }
};

export const SceneWrapper: React.FC<SceneWrapperProps> = ({
  children,
  enterAnimation = 'fade',
  exitAnimation = 'fade',
  enterDuration = 15,
  exitDuration = 15,
  backgroundColor,
  padding = 0,
}) => {
  const frame = useCurrentFrame();
  const { durationInFrames, fps } = useVideoConfig();

  // Enter progress: 0 -> 1
  const enterProgress =
    enterAnimation === 'none'
      ? 1
      : enterAnimation === 'scale'
        ? spring({ frame, fps, config: { damping: 12, stiffness: 150 }, durationInFrames: enterDuration })
        : interpolate(frame, [0, enterDuration], [0, 1], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });

  // Exit progress: 1 -> 0
  const exitStart = durationInFrames - exitDuration;
  const exitProgress =
    exitAnimation === 'none'
      ? 1
      : interpolate(frame, [exitStart, durationInFrames], [1, 0], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });

  const inExit = frame >= exitStart;
  const activeAnimation = inExit ? exitAnimation : enterAnimation;
  const progress = inExit ? exitProgress : enterProgress;

  const { opacity, transform } = getTransformAndOpacity(activeAnimation, progress);

  return (
    <div
      style={{
        position: 'absolute',
        inset: 0,
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'center',
        alignItems: 'center',
        backgroundColor,
        padding,
        opacity,
        transform,
      }}
    >
      {children}
    </div>
  );
};