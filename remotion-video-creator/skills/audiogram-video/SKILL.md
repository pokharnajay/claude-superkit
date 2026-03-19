---
name: audiogram-video
description: Create podcast audiograms, audio waveform visualizations, and audio-reactive videos. Use when user wants to visualize audio content for social sharing.
---

# Audiogram Video

Visual representations of audio content — perfect for podcasts, music, and audio clips shared on social media.

## When to Use

- User wants to create a podcast audiogram or clip
- User asks for an audio waveform visualization
- User wants a music visualizer with spectrum bars
- User mentions audio-reactive visuals or sound visualization
- User wants to turn a podcast episode into a shareable video

## Common Formats

- Podcast audiogram (waveform + artwork + captions)
- Music visualizer (spectrum bars, circular, reactive shapes)
- Audio waveform display (oscilloscope-style line)
- Speaker card (photo + name + animated waveform indicator)
- Quote highlight (pull quote from transcript with audio)
- Interview clip (two speakers with indicator)

## Audio Visualization Methods

### Spectrum Bars

Vertical bars that react to audio frequency data.

```tsx
import { useCurrentFrame, useVideoConfig, interpolate } from "remotion";
import { getAudioData, visualizeAudio } from "@remotion/media-utils";
import { useEffect, useState } from "react";

const SpectrumBars: React.FC<{
  audioSrc: string;
  barCount?: number;
  barColor?: string;
  barWidth?: number;
  maxHeight?: number;
  gap?: number;
  smoothing?: boolean;
}> = ({
  audioSrc,
  barCount = 32,
  barColor = "#00f5d4",
  barWidth = 8,
  maxHeight = 200,
  gap = 4,
  smoothing = true,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const [audioData, setAudioData] = useState<Awaited<ReturnType<typeof getAudioData>> | null>(null);

  useEffect(() => {
    getAudioData(audioSrc).then((data) => setAudioData(data));
  }, [audioSrc]);

  if (!audioData) return null;

  const visualization = visualizeAudio({
    fps,
    frame,
    audioData,
    numberOfSamples: barCount,
    smoothing,
  });

  const totalWidth = barCount * (barWidth + gap) - gap;

  return (
    <div
      style={{
        display: "flex",
        alignItems: "flex-end",
        justifyContent: "center",
        gap,
        height: maxHeight,
      }}
    >
      {visualization.map((value, i) => (
        <div
          key={i}
          style={{
            width: barWidth,
            height: `${value * 100}%`,
            backgroundColor: barColor,
            borderRadius: barWidth / 2,
            minHeight: 4,
          }}
        />
      ))}
    </div>
  );
};
```

### Waveform Line (SVG)

Continuous line waveform drawn as an SVG path.

```tsx
const WaveformLine: React.FC<{
  audioSrc: string;
  color?: string;
  strokeWidth?: number;
  width?: number;
  height?: number;
  samples?: number;
}> = ({ audioSrc, color = "#00f5d4", strokeWidth = 3, width = 800, height = 200, samples = 128 }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const [audioData, setAudioData] = useState<Awaited<ReturnType<typeof getAudioData>> | null>(null);

  useEffect(() => {
    getAudioData(audioSrc).then((data) => setAudioData(data));
  }, [audioSrc]);

  if (!audioData) return null;

  const visualization = visualizeAudio({
    fps,
    frame,
    audioData,
    numberOfSamples: samples,
    smoothing: true,
  });

  const midY = height / 2;
  const stepX = width / (samples - 1);

  const pathData = visualization
    .map((v, i) => {
      const x = i * stepX;
      const y = midY - v * midY * 0.9; // mirror around center
      return `${i === 0 ? "M" : "L"} ${x} ${y}`;
    })
    .join(" ");

  // Mirror path for symmetry
  const mirrorData = visualization
    .map((v, i) => {
      const x = (samples - 1 - i) * stepX;
      const y = midY + v * midY * 0.9;
      return `L ${x} ${y}`;
    })
    .join(" ");

  return (
    <svg width={width} height={height} viewBox={`0 0 ${width} ${height}`}>
      <path d={`${pathData} ${mirrorData} Z`} fill={color} opacity={0.3} />
      <path d={pathData} fill="none" stroke={color} strokeWidth={strokeWidth} strokeLinecap="round" strokeLinejoin="round" />
    </svg>
  );
};
```

### Circular Audio Visualizer

Bars radiating outward from a center circle (album artwork).

```tsx
const CircularVisualizer: React.FC<{
  audioSrc: string;
  centerImageSrc?: string;
  radius?: number;
  barCount?: number;
  barColor?: string;
}> = ({ audioSrc, centerImageSrc, radius = 150, barCount = 64, barColor = "#00f5d4" }) => {
  const frame = useCurrentFrame();
  const { fps, width, height } = useVideoConfig();
  const [audioData, setAudioData] = useState<Awaited<ReturnType<typeof getAudioData>> | null>(null);

  useEffect(() => {
    getAudioData(audioSrc).then((data) => setAudioData(data));
  }, [audioSrc]);

  if (!audioData) return null;

  const visualization = visualizeAudio({
    fps,
    frame,
    audioData,
    numberOfSamples: barCount,
    smoothing: true,
  });

  const cx = width / 2;
  const cy = height / 2;

  return (
    <AbsoluteFill>
      <svg width={width} height={height} viewBox={`0 0 ${width} ${height}`}>
        {visualization.map((value, i) => {
          const angle = (i / barCount) * Math.PI * 2 - Math.PI / 2;
          const barLength = value * 120 + 10;
          const x1 = cx + Math.cos(angle) * (radius + 10);
          const y1 = cy + Math.sin(angle) * (radius + 10);
          const x2 = cx + Math.cos(angle) * (radius + 10 + barLength);
          const y2 = cy + Math.sin(angle) * (radius + 10 + barLength);

          return (
            <line
              key={i}
              x1={x1}
              y1={y1}
              x2={x2}
              y2={y2}
              stroke={barColor}
              strokeWidth={4}
              strokeLinecap="round"
              opacity={0.7 + value * 0.3}
            />
          );
        })}
        {/* Center circle for artwork */}
        <circle cx={cx} cy={cy} r={radius} fill="#1a1a1a" stroke={barColor} strokeWidth={2} />
      </svg>

      {/* Center artwork */}
      {centerImageSrc && (
        <div
          style={{
            position: "absolute",
            left: cx - radius + 10,
            top: cy - radius + 10,
            width: (radius - 10) * 2,
            height: (radius - 10) * 2,
            borderRadius: "50%",
            overflow: "hidden",
          }}
        >
          <Img src={centerImageSrc} style={{ width: "100%", height: "100%", objectFit: "cover" }} />
        </div>
      )}
    </AbsoluteFill>
  );
};
```

### Bass-Reactive Background

Background that pulses with bass frequencies.

```tsx
const BassReactiveBG: React.FC<{
  audioSrc: string;
  baseColor?: string;
  pulseColor?: string;
}> = ({ audioSrc, baseColor = "#0f0f0f", pulseColor = "#1a0a2e" }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const [audioData, setAudioData] = useState<Awaited<ReturnType<typeof getAudioData>> | null>(null);

  useEffect(() => {
    getAudioData(audioSrc).then((data) => setAudioData(data));
  }, [audioSrc]);

  if (!audioData) return null;

  const [bass] = visualizeAudio({
    fps,
    frame,
    audioData,
    numberOfSamples: 4,
    smoothing: true,
  });

  const bgScale = 1 + bass * 0.08;
  const glowOpacity = bass * 0.6;

  return (
    <AbsoluteFill style={{ backgroundColor: baseColor }}>
      <div
        style={{
          position: "absolute",
          inset: -50,
          background: `radial-gradient(circle at center, ${pulseColor}, transparent 70%)`,
          opacity: glowOpacity,
          transform: `scale(${bgScale})`,
        }}
      />
    </AbsoluteFill>
  );
};
```

## Layout Options

| Layout | Description | Best For |
|--------|-------------|----------|
| Centered waveform | Metadata above, waveform center, captions below | Clean audiograms |
| Podcast player UI | Artwork + title + waveform + progress bar | Podcast clips |
| Speaker card | Photo with audio indicator bars | Interview clips |
| Minimal | Just waveform + captions | Transcription clips |
| Full-screen reactive | Background pulses + spectrum fills screen | Music visualizers |

## Caption Integration

### Step 1: Transcribe with Whisper

```bash
npx @remotion/install-whisper-cpp@latest
npx @remotion/install-whisper-cpp --model base
```

### Step 2: Generate Caption JSON

```tsx
import { transcribe } from "@remotion/install-whisper-cpp";

const { transcription } = await transcribe({
  inputPath: "public/audio/episode.mp3",
  whisperPath: "whisper.cpp",
  model: "base",
  tokenLevelTimestamps: true,
});
```

### Step 3: Display TikTok-Style Captions

```tsx
import { createTikTokStyleCaptions } from "@remotion/captions";

const { pages } = createTikTokStyleCaptions({
  transcription,
  combineTokensWithinMilliseconds: 800,
});
```

## Complete Starter Template

```tsx
import {
  AbsoluteFill,
  Audio,
  Img,
  Sequence,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
  interpolate,
} from "remotion";
import { getAudioData, visualizeAudio } from "@remotion/media-utils";
import { useEffect, useState } from "react";

// -- Podcast Audiogram --
export const PodcastAudiogram: React.FC<{
  audioSrc: string;
  artworkSrc: string;
  showName: string;
  episodeTitle: string;
  guestName?: string;
}> = ({ audioSrc, artworkSrc, showName, episodeTitle, guestName }) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames, width, height } = useVideoConfig();
  const [audioData, setAudioData] = useState<Awaited<ReturnType<typeof getAudioData>> | null>(null);

  useEffect(() => {
    getAudioData(audioSrc).then((data) => setAudioData(data));
  }, [audioSrc]);

  const progress = frame / durationInFrames;

  return (
    <AbsoluteFill style={{ backgroundColor: "#0f0f0f" }}>
      {/* Audio playback */}
      <Audio src={audioSrc} />

      {/* Show artwork */}
      <div
        style={{
          position: "absolute",
          top: 200,
          left: width / 2 - 150,
          width: 300,
          height: 300,
          borderRadius: 24,
          overflow: "hidden",
          boxShadow: "0 20px 60px rgba(0,0,0,0.5)",
        }}
      >
        <Img src={artworkSrc} style={{ width: "100%", height: "100%", objectFit: "cover" }} />
      </div>

      {/* Show name */}
      <div
        style={{
          position: "absolute",
          top: 540,
          left: 0,
          right: 0,
          textAlign: "center",
          color: "rgba(255,255,255,0.6)",
          fontSize: 24,
          fontWeight: 600,
          fontFamily: "Inter, sans-serif",
          textTransform: "uppercase",
          letterSpacing: 2,
        }}
      >
        {showName}
      </div>

      {/* Episode title */}
      <div
        style={{
          position: "absolute",
          top: 580,
          left: 60,
          right: 60,
          textAlign: "center",
          color: "#ffffff",
          fontSize: 40,
          fontWeight: 800,
          fontFamily: "Inter, sans-serif",
          lineHeight: 1.3,
        }}
      >
        {episodeTitle}
      </div>

      {/* Guest name */}
      {guestName && (
        <div
          style={{
            position: "absolute",
            top: 680,
            left: 0,
            right: 0,
            textAlign: "center",
            color: "#00f5d4",
            fontSize: 28,
            fontWeight: 600,
            fontFamily: "Inter, sans-serif",
          }}
        >
          with {guestName}
        </div>
      )}

      {/* Spectrum bars */}
      <div style={{ position: "absolute", top: 760, left: 60, right: 60 }}>
        {audioData && (
          <SpectrumDisplay audioData={audioData} frame={frame} fps={fps} />
        )}
      </div>

      {/* Progress bar */}
      <div
        style={{
          position: "absolute",
          bottom: 120,
          left: 60,
          right: 60,
          height: 4,
          backgroundColor: "rgba(255,255,255,0.15)",
          borderRadius: 2,
        }}
      >
        <div
          style={{
            width: `${progress * 100}%`,
            height: "100%",
            backgroundColor: "#00f5d4",
            borderRadius: 2,
          }}
        />
      </div>
    </AbsoluteFill>
  );
};

// -- Inline spectrum for starter template --
const SpectrumDisplay: React.FC<{
  audioData: Awaited<ReturnType<typeof getAudioData>>;
  frame: number;
  fps: number;
}> = ({ audioData, frame, fps }) => {
  const visualization = visualizeAudio({
    fps,
    frame,
    audioData,
    numberOfSamples: 48,
    smoothing: true,
  });

  return (
    <div style={{ display: "flex", alignItems: "flex-end", justifyContent: "center", gap: 3, height: 120 }}>
      {visualization.map((value, i) => (
        <div
          key={i}
          style={{
            width: 6,
            height: `${Math.max(value * 100, 3)}%`,
            backgroundColor: "#00f5d4",
            borderRadius: 3,
          }}
        />
      ))}
    </div>
  );
};
```

Register in `Root.tsx`:
```tsx
<Composition
  id="PodcastAudiogram"
  component={PodcastAudiogram}
  durationInFrames={900}
  fps={30}
  width={1080}
  height={1080}
  defaultProps={{
    audioSrc: staticFile("audio/episode-clip.mp3"),
    artworkSrc: staticFile("artwork/podcast-cover.jpg"),
    showName: "The Tech Pod",
    episodeTitle: "The Future of AI in Creative Tools",
    guestName: "Jane Doe",
  }}
/>
```

## Dynamic Duration from Audio File

```tsx
import { getAudioDurationInSeconds } from "@remotion/media-utils";
import { CalculateMetadataFunction } from "remotion";

type AudiogramProps = { audioSrc: string; artworkSrc: string; showName: string; episodeTitle: string };

export const calculateMetadata: CalculateMetadataFunction<AudiogramProps> = async ({ props }) => {
  const fps = 30;
  const duration = await getAudioDurationInSeconds(props.audioSrc);
  return { durationInFrames: Math.ceil(duration * fps), fps };
};
```

## Audio Specs

| Format | Support | Notes |
|--------|---------|-------|
| MP3 | Full | Most common, good compression |
| WAV | Full | Uncompressed, large files |
| AAC | Full | Good quality, smaller than WAV |
| M4A | Full | AAC in MP4 container |
| OGG | Partial | Browser-dependent |

- Always use `staticFile()` for local audio files in `public/` folder
- Use `getAudioDurationInSeconds()` for dynamic composition length
- Audio visualization requires `getAudioData()` loaded asynchronously

## Quality Checklist

- [ ] Audio plays correctly with `<Audio>` component
- [ ] Visualization reacts to actual audio (not random)
- [ ] `getAudioData` loaded in `useEffect` with proper state
- [ ] Bars/waveform smoothing enabled for fluid motion
- [ ] Progress bar reflects actual playback position
- [ ] Captions synced to audio timestamps
- [ ] Background not too busy (doesn't distract from waveform)
- [ ] Font sizes readable at target platform size
- [ ] Used `staticFile()` for all local audio/image assets
- [ ] Dynamic duration set via `calculateMetadata` if needed

## Reference Files

- `references/audiogram-patterns.md` — Copy-paste patterns for visualizers, players, captions
- `../../references/color-palettes.md` — Curated color palettes
- `../../references/sound-effects-library.md` — SFX catalog
- `../../references/font-pairings.md` — Font pairing recommendations
