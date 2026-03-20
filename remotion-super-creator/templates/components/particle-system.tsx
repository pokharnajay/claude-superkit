import React, { useMemo } from 'react';
import { useCurrentFrame, useVideoConfig, interpolate } from 'remotion';
import { noise2D } from '@remotion/noise';

interface ParticleSystemProps {
  count?: number;
  color?: string;
  maxSize?: number;
  speed?: number;
  spread?: number;
  opacity?: number;
  seed?: string;
}

interface Particle {
  id: number;
  baseX: number;
  baseY: number;
  size: number;
  baseOpacity: number;
  phase: number;
}

export const ParticleSystem: React.FC<ParticleSystemProps> = ({
  count = 30,
  color = '#FFFFFF',
  maxSize = 8,
  speed = 1,
  spread = 1,
  opacity = 0.6,
  seed = 'particles',
}) => {
  const frame = useCurrentFrame();
  const { width, height, durationInFrames } = useVideoConfig();

  // Generate stable particle positions using index-based seeding
  const particles: Particle[] = useMemo(() => {
    return Array.from({ length: count }, (_, i) => {
      const hash1 = Math.abs(Math.sin(i * 127.1 + 311.7) * 43758.5453) % 1;
      const hash2 = Math.abs(Math.sin(i * 269.5 + 183.3) * 43758.5453) % 1;
      const hash3 = Math.abs(Math.sin(i * 419.2 + 371.9) * 43758.5453) % 1;
      const hash4 = Math.abs(Math.sin(i * 547.3 + 257.1) * 43758.5453) % 1;
      return {
        id: i,
        baseX: hash1 * width,
        baseY: hash2 * height,
        size: 2 + hash3 * (maxSize - 2),
        baseOpacity: 0.3 + hash4 * 0.7,
        phase: hash1 * 1000,
      };
    });
  }, [count, width, height, maxSize]);

  // Fade particles in at start, out at end
  const globalOpacity = interpolate(
    frame,
    [0, 20, durationInFrames - 20, durationInFrames],
    [0, 1, 1, 0],
    { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }
  );

  return (
    <div
      style={{
        position: 'absolute',
        inset: 0,
        overflow: 'hidden',
        pointerEvents: 'none',
      }}
    >
      {particles.map((p) => {
        const t = (frame * speed * 0.01) + p.phase;
        const noiseX = noise2D(seed, p.id * 0.1, t * 0.3) * spread * 80;
        const noiseY = noise2D(seed + 'y', p.id * 0.1, t * 0.3) * spread * 80;
        const noiseOpacity = noise2D(seed + 'o', p.id * 0.2, t * 0.5);
        const particleOpacity = opacity * p.baseOpacity * interpolate(noiseOpacity, [-1, 1], [0.3, 1]);

        return (
          <div
            key={p.id}
            style={{
              position: 'absolute',
              left: p.baseX + noiseX,
              top: p.baseY + noiseY,
              width: p.size,
              height: p.size,
              borderRadius: '50%',
              backgroundColor: color,
              opacity: particleOpacity * globalOpacity,
            }}
          />
        );
      })}
    </div>
  );
};