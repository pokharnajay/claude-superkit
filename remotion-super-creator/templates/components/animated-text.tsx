import React from 'react';
import { useCurrentFrame, useVideoConfig, interpolate, spring } from 'remotion';

type AnimationMode =
  | 'fade'
  | 'slideUp'
  | 'slideDown'
  | 'slideLeft'
  | 'slideRight'
  | 'scale'
  | 'typewriter'
  | 'wordByWord';

interface AnimatedTextProps {
  text: string;
  startFrame?: number;
  animation?: AnimationMode;
  fontSize?: number;
  fontFamily?: string;
  fontWeight?: string | number;
  color?: string;
  textAlign?: 'left' | 'center' | 'right';
  style?: React.CSSProperties;
}

export const AnimatedText: React.FC<AnimatedTextProps> = ({
  text,
  startFrame = 0,
  animation = 'fade',
  fontSize = 48,
  fontFamily = 'Inter, sans-serif',
  fontWeight = 'bold',
  color = '#FFFFFF',
  textAlign = 'center',
  style = {},
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const f = frame - startFrame;

  if (f < 0) return null;

  const baseStyle: React.CSSProperties = {
    fontSize,
    fontFamily,
    fontWeight,
    color,
    textAlign,
    whiteSpace: 'pre-wrap',
    ...style,
  };

  // --- Typewriter ---
  if (animation === 'typewriter') {
    const charsPerFrame = 0.5; // 2 frames per character
    const visibleChars = Math.min(Math.floor(f * charsPerFrame), text.length);
    const showCursor = f % 16 < 10; // blinking cursor
    const displayed = text.slice(0, visibleChars);
    return (
      <div style={baseStyle}>
        {displayed}
        <span style={{ opacity: showCursor ? 1 : 0 }}>|</span>
      </div>
    );
  }

  // --- Word by Word ---
  if (animation === 'wordByWord') {
    const words = text.split(' ');
    const framesPerWord = 8;
    return (
      <div style={{ ...baseStyle, display: 'flex', flexWrap: 'wrap', justifyContent: textAlign === 'center' ? 'center' : textAlign === 'right' ? 'flex-end' : 'flex-start', gap: '0 0.3em' }}>
        {words.map((word, i) => {
          const wordDelay = i * framesPerWord;
          const localF = f - wordDelay;
          if (localF < 0) return <span key={i} style={{ opacity: 0 }}>{word}</span>;
          const prog = spring({ frame: localF, fps, config: { damping: 12, stiffness: 200 } });
          return (
            <span
              key={i}
              style={{
                opacity: prog,
                transform: `translateY(${interpolate(prog, [0, 1], [20, 0])}px)`,
                display: 'inline-block',
              }}
            >
              {word}
            </span>
          );
        })}
      </div>
    );
  }

  // --- Standard animations ---
  const opacity = interpolate(f, [0, 20], [0, 1], { extrapolateRight: 'clamp' });

  let transform = '';
  switch (animation) {
    case 'fade':
      break;
    case 'slideUp':
      transform = `translateY(${interpolate(f, [0, 20], [40, 0], { extrapolateRight: 'clamp' })}px)`;
      break;
    case 'slideDown':
      transform = `translateY(${interpolate(f, [0, 20], [-40, 0], { extrapolateRight: 'clamp' })}px)`;
      break;
    case 'slideLeft':
      transform = `translateX(${interpolate(f, [0, 20], [60, 0], { extrapolateRight: 'clamp' })}px)`;
      break;
    case 'slideRight':
      transform = `translateX(${interpolate(f, [0, 20], [-60, 0], { extrapolateRight: 'clamp' })}px)`;
      break;
    case 'scale': {
      const s = spring({ frame: f, fps, config: { damping: 10, stiffness: 150 } });
      transform = `scale(${interpolate(s, [0, 1], [0.5, 1])})`;
      break;
    }
  }

  return (
    <div style={{ ...baseStyle, opacity, transform }}>
      {text}
    </div>
  );
};