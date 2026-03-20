# Audiogram Video — Code Patterns

Dense, copy-paste-ready component patterns for audio visualizations and podcast audiograms. All assume `@remotion/media-utils` is installed.

---

## Spectrum Bar Visualizer

Vertical bars reacting to audio frequency data with configurable appearance.

```tsx
import { getAudioData, visualizeAudio } from "@remotion/media-utils";
import { useEffect, useState } from "react";

const SpectrumBars: React.FC<{
  audioSrc: string;
  barCount?: number;
  barColor?: string;
  barWidth?: number;
  maxHeight?: number;
  gap?: number;
  mirror?: boolean;
  rounded?: boolean;
}> = ({
  audioSrc,
  barCount = 32,
  barColor = "#00f5d4",
  barWidth = 8,
  maxHeight = 200,
  gap = 4,
  mirror = false,
  rounded = true,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const [audioData, setAudioData] = useState<Awaited<ReturnType<typeof getAudioData>> | null>(null);

  useEffect(() => {
    getAudioData(audioSrc).then(setAudioData);
  }, [audioSrc]);

  if (!audioData) return null;

  const values = visualizeAudio({
    fps,
    frame,
    audioData,
    numberOfSamples: barCount,
    smoothing: true,
  });

  return (
    <div
      style={{
        display: "flex",
        alignItems: mirror ? "center" : "flex-end",
        justifyContent: "center",
        gap,
        height: maxHeight,
        flexDirection: "row",
      }}
    >
      {values.map((v, i) => {
        const h = Math.max(v * maxHeight, 4);
        return (
          <div
            key={i}
            style={{
              width: barWidth,
              height: mirror ? h : h,
              marginTop: mirror ? undefined : undefined,
              backgroundColor: barColor,
              borderRadius: rounded ? barWidth / 2 : 0,
              transform: mirror ? `scaleY(1)` : undefined,
              boxShadow: v > 0.5 ? `0 0 ${v * 10}px ${barColor}40` : "none",
            }}
          />
        );
      })}
    </div>
  );
};
```

---

## Circular Audio Visualizer

Bars radiating outward from a center circle, ideal for album artwork.

```tsx
const CircularVis: React.FC<{
  audioSrc: string;
  radius?: number;
  barCount?: number;
  barColor?: string;
  maxBarLength?: number;
}> = ({ audioSrc, radius = 140, barCount = 64, barColor = "#00f5d4", maxBarLength = 100 }) => {
  const frame = useCurrentFrame();
  const { fps, width, height } = useVideoConfig();
  const [audioData, setAudioData] = useState<Awaited<ReturnType<typeof getAudioData>> | null>(null);

  useEffect(() => {
    getAudioData(audioSrc).then(setAudioData);
  }, [audioSrc]);

  if (!audioData) return null;

  const values = visualizeAudio({ fps, frame, audioData, numberOfSamples: barCount, smoothing: true });
  const cx = width / 2;
  const cy = height / 2;

  return (
    <svg width={width} height={height}>
      {values.map((v, i) => {
        const angle = (i / barCount) * Math.PI * 2 - Math.PI / 2;
        const len = v * maxBarLength + 6;
        const x1 = cx + Math.cos(angle) * (radius + 8);
        const y1 = cy + Math.sin(angle) * (radius + 8);
        const x2 = cx + Math.cos(angle) * (radius + 8 + len);
        const y2 = cy + Math.sin(angle) * (radius + 8 + len);
        return (
          <line key={i} x1={x1} y1={y1} x2={x2} y2={y2} stroke={barColor} strokeWidth={3} strokeLinecap="round" opacity={0.6 + v * 0.4} />
        );
      })}
      <circle cx={cx} cy={cy} r={radius} fill="#111" stroke={barColor} strokeWidth={2} opacity={0.8} />
    </svg>
  );
};
```

---

## Waveform Line Component

SVG path from audio data, oscilloscope style.

```tsx
const WaveformPath: React.FC<{
  audioSrc: string;
  color?: string;
  width?: number;
  height?: number;
  samples?: number;
  filled?: boolean;
}> = ({ audioSrc, color = "#00f5d4", width = 800, height = 150, samples = 128, filled = false }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const [audioData, setAudioData] = useState<Awaited<ReturnType<typeof getAudioData>> | null>(null);

  useEffect(() => {
    getAudioData(audioSrc).then(setAudioData);
  }, [audioSrc]);

  if (!audioData) return null;

  const values = visualizeAudio({ fps, frame, audioData, numberOfSamples: samples, smoothing: true });
  const midY = height / 2;
  const stepX = width / (samples - 1);

  // Top wave
  const topPath = values.map((v, i) => `${i === 0 ? "M" : "L"} ${i * stepX} ${midY - v * midY * 0.85}`).join(" ");

  if (filled) {
    // Bottom wave (mirror)
    const bottomPath = [...values].reverse().map((v, i) => `L ${(samples - 1 - i) * stepX} ${midY + v * midY * 0.85}`).join(" ");
    return (
      <svg width={width} height={height}>
        <path d={`${topPath} ${bottomPath} Z`} fill={color} opacity={0.25} />
        <path d={topPath} fill="none" stroke={color} strokeWidth={2.5} strokeLinecap="round" />
      </svg>
    );
  }

  return (
    <svg width={width} height={height}>
      <path d={topPath} fill="none" stroke={color} strokeWidth={2.5} strokeLinecap="round" strokeLinejoin="round" />
    </svg>
  );
};
```

---

## Podcast Player UI Layout

Complete podcast player with artwork, metadata, waveform, and progress.

```tsx
const PodcastPlayerUI: React.FC<{
  audioSrc: string;
  artworkSrc: string;
  showName: string;
  episodeTitle: string;
  episodeNumber?: string;
  accentColor?: string;
}> = ({ audioSrc, artworkSrc, showName, episodeTitle, episodeNumber, accentColor = "#00f5d4" }) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames, width } = useVideoConfig();
  const progress = frame / durationInFrames;

  return (
    <AbsoluteFill style={{ backgroundColor: "#0f0f0f", padding: 60 }}>
      <Audio src={audioSrc} />

      {/* Top: Show branding */}
      <div style={{ color: "rgba(255,255,255,0.5)", fontSize: 20, fontWeight: 600, fontFamily: "Inter, sans-serif", letterSpacing: 2, textTransform: "uppercase", marginBottom: 40 }}>
        {showName} {episodeNumber && `/ EP ${episodeNumber}`}
      </div>

      {/* Artwork */}
      <div style={{ width: width - 120, aspectRatio: "1/1", borderRadius: 20, overflow: "hidden", marginBottom: 40, boxShadow: `0 20px 80px ${accentColor}30` }}>
        <Img src={artworkSrc} style={{ width: "100%", height: "100%", objectFit: "cover" }} />
      </div>

      {/* Episode title */}
      <div style={{ color: "#fff", fontSize: 36, fontWeight: 800, fontFamily: "Inter, sans-serif", lineHeight: 1.3, marginBottom: 30 }}>
        {episodeTitle}
      </div>

      {/* Progress bar */}
      <div style={{ height: 4, backgroundColor: "rgba(255,255,255,0.1)", borderRadius: 2, marginBottom: 12 }}>
        <div style={{ width: `${progress * 100}%`, height: "100%", backgroundColor: accentColor, borderRadius: 2, position: "relative" }}>
          <div style={{ position: "absolute", right: -6, top: -4, width: 12, height: 12, borderRadius: "50%", backgroundColor: accentColor }} />
        </div>
      </div>

      {/* Time indicators */}
      <div style={{ display: "flex", justifyContent: "space-between", color: "rgba(255,255,255,0.4)", fontSize: 16, fontFamily: "Inter, sans-serif", fontVariantNumeric: "tabular-nums" }}>
        <span>{formatTime(frame / fps)}</span>
        <span>{formatTime(durationInFrames / fps)}</span>
      </div>
    </AbsoluteFill>
  );
};

function formatTime(seconds: number): string {
  const m = Math.floor(seconds / 60);
  const s = Math.floor(seconds % 60);
  return `${m}:${s.toString().padStart(2, "0")}`;
}
```

---

## Speaker Card

Circular photo with name and animated speaking indicator.

```tsx
const SpeakerCard: React.FC<{
  photoSrc: string;
  name: string;
  title?: string;
  audioSrc: string;
  accentColor?: string;
}> = ({ photoSrc, name, title, audioSrc, accentColor = "#00f5d4" }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const [audioData, setAudioData] = useState<Awaited<ReturnType<typeof getAudioData>> | null>(null);

  useEffect(() => {
    getAudioData(audioSrc).then(setAudioData);
  }, [audioSrc]);

  const isSpeaking = audioData
    ? visualizeAudio({ fps, frame, audioData, numberOfSamples: 1, smoothing: true })[0] > 0.15
    : false;

  const ringScale = isSpeaking ? 1.08 : 1;
  const ringOpacity = isSpeaking ? 1 : 0.3;

  return (
    <div style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: 16 }}>
      {/* Photo with speaking ring */}
      <div style={{ position: "relative" }}>
        <div
          style={{
            width: 180,
            height: 180,
            borderRadius: "50%",
            border: `4px solid ${accentColor}`,
            opacity: ringOpacity,
            transform: `scale(${ringScale})`,
            transition: "transform 0.1s, opacity 0.1s",
            position: "absolute",
            inset: -4,
          }}
        />
        <div style={{ width: 180, height: 180, borderRadius: "50%", overflow: "hidden" }}>
          <Img src={photoSrc} style={{ width: "100%", height: "100%", objectFit: "cover" }} />
        </div>
      </div>
      {/* Name */}
      <div style={{ color: "#fff", fontSize: 28, fontWeight: 700, fontFamily: "Inter, sans-serif" }}>{name}</div>
      {title && <div style={{ color: "rgba(255,255,255,0.5)", fontSize: 20, fontWeight: 500, fontFamily: "Inter, sans-serif" }}>{title}</div>}
    </div>
  );
};
```

---

## Auto-Captions Display

Word-by-word highlight synced to audio timing.

```tsx
type CaptionWord = { text: string; startFrame: number; endFrame: number };

const AutoCaptions: React.FC<{
  words: CaptionWord[];
  highlightColor?: string;
  wordsPerLine?: number;
}> = ({ words, highlightColor = "#00f5d4", wordsPerLine = 5 }) => {
  const frame = useCurrentFrame();

  // Find current window of words
  const currentWordIndex = words.findIndex((w) => frame >= w.startFrame && frame < w.endFrame);
  const lineStart = Math.max(0, currentWordIndex - Math.floor(wordsPerLine / 2));
  const lineEnd = Math.min(words.length, lineStart + wordsPerLine);
  const visibleWords = words.slice(lineStart, lineEnd);

  return (
    <div
      style={{
        position: "absolute",
        bottom: 200,
        left: 40,
        right: 40,
        textAlign: "center",
        display: "flex",
        flexWrap: "wrap",
        justifyContent: "center",
        gap: "6px 10px",
      }}
    >
      {visibleWords.map((word, i) => {
        const isActive = frame >= word.startFrame && frame < word.endFrame;
        const isPast = frame >= word.endFrame;
        return (
          <span
            key={lineStart + i}
            style={{
              fontSize: 44,
              fontWeight: 800,
              fontFamily: "Inter, sans-serif",
              color: isActive ? highlightColor : isPast ? "#ffffff" : "rgba(255,255,255,0.4)",
              textShadow: "0 2px 8px rgba(0,0,0,0.8)",
              transform: isActive ? "scale(1.12)" : "scale(1)",
              display: "inline-block",
            }}
          >
            {word.text}
          </span>
        );
      })}
    </div>
  );
};
```

---

## Episode Metadata Overlay

Show name, episode number, and guest info with staggered reveal.

```tsx
const EpisodeMetadata: React.FC<{
  showName: string;
  episodeNumber: string;
  guestName?: string;
  accentColor?: string;
}> = ({ showName, episodeNumber, guestName, accentColor = "#00f5d4" }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const line1 = spring({ frame, fps, config: { damping: 14 } });
  const line2 = spring({ frame: frame - 8, fps, config: { damping: 14 } });
  const line3 = spring({ frame: frame - 16, fps, config: { damping: 14 } });

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
      <div style={{ opacity: line1, transform: `translateY(${interpolate(line1, [0, 1], [20, 0])}px)`, color: "rgba(255,255,255,0.5)", fontSize: 18, fontWeight: 600, fontFamily: "Inter, sans-serif", textTransform: "uppercase", letterSpacing: 2 }}>
        {showName}
      </div>
      <div style={{ opacity: line2, transform: `translateY(${interpolate(line2, [0, 1], [20, 0])}px)`, color: accentColor, fontSize: 22, fontWeight: 700, fontFamily: "Inter, sans-serif" }}>
        Episode {episodeNumber}
      </div>
      {guestName && (
        <div style={{ opacity: line3, transform: `translateY(${interpolate(line3, [0, 1], [20, 0])}px)`, color: "#fff", fontSize: 20, fontWeight: 500, fontFamily: "Inter, sans-serif" }}>
          with {guestName}
        </div>
      )}
    </div>
  );
};
```

---

## Pull Quote Display

Highlighted quote from transcript with speaker attribution.

```tsx
const PullQuote: React.FC<{
  quote: string;
  speaker: string;
  speakerPhotoSrc?: string;
  accentColor?: string;
}> = ({ quote, speaker, speakerPhotoSrc, accentColor = "#00f5d4" }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const entrance = spring({ frame, fps, config: { damping: 12 } });

  return (
    <AbsoluteFill style={{ justifyContent: "center", alignItems: "center", padding: 80 }}>
      {/* Quote mark */}
      <div style={{ color: accentColor, fontSize: 120, fontWeight: 900, fontFamily: "Georgia, serif", opacity: 0.3, position: "absolute", top: 180, left: 60 }}>
        &ldquo;
      </div>
      {/* Quote text */}
      <div
        style={{
          transform: `translateY(${interpolate(entrance, [0, 1], [40, 0])}px)`,
          opacity: entrance,
          color: "#fff",
          fontSize: 40,
          fontWeight: 700,
          fontFamily: "Inter, sans-serif",
          lineHeight: 1.5,
          textAlign: "center",
          fontStyle: "italic",
        }}
      >
        &ldquo;{quote}&rdquo;
      </div>
      {/* Attribution */}
      <div
        style={{
          marginTop: 40,
          display: "flex",
          alignItems: "center",
          gap: 16,
          opacity: spring({ frame: frame - 15, fps, config: { damping: 14 } }),
        }}
      >
        {speakerPhotoSrc && (
          <div style={{ width: 48, height: 48, borderRadius: "50%", overflow: "hidden" }}>
            <Img src={speakerPhotoSrc} style={{ width: "100%", height: "100%", objectFit: "cover" }} />
          </div>
        )}
        <div style={{ color: accentColor, fontSize: 24, fontWeight: 600, fontFamily: "Inter, sans-serif" }}>
          {speaker}
        </div>
      </div>
    </AbsoluteFill>
  );
};
```

---

## Background Pulse

Scale and opacity reacting to bass frequency for ambient energy.

```tsx
const BackgroundPulse: React.FC<{
  audioSrc: string;
  color?: string;
  maxScale?: number;
}> = ({ audioSrc, color = "#1a0a2e", maxScale = 1.1 }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const [audioData, setAudioData] = useState<Awaited<ReturnType<typeof getAudioData>> | null>(null);

  useEffect(() => {
    getAudioData(audioSrc).then(setAudioData);
  }, [audioSrc]);

  if (!audioData) return null;

  const [bass] = visualizeAudio({ fps, frame, audioData, numberOfSamples: 4, smoothing: true });
  const scale = 1 + bass * (maxScale - 1);
  const opacity = 0.3 + bass * 0.5;

  return (
    <AbsoluteFill>
      <div
        style={{
          position: "absolute",
          inset: -100,
          background: `radial-gradient(ellipse at center, ${color}, transparent 70%)`,
          transform: `scale(${scale})`,
          opacity,
        }}
      />
    </AbsoluteFill>
  );
};
```

---

## Progress Bar

Shows playback position with time labels.

```tsx
const AudioProgressBar: React.FC<{
  totalDurationSeconds: number;
  color?: string;
  height?: number;
  showTime?: boolean;
}> = ({ totalDurationSeconds, color = "#00f5d4", height = 4, showTime = true }) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();
  const progress = frame / durationInFrames;
  const currentTime = frame / fps;

  const formatT = (s: number) => `${Math.floor(s / 60)}:${Math.floor(s % 60).toString().padStart(2, "0")}`;

  return (
    <div style={{ width: "100%" }}>
      <div style={{ height, backgroundColor: "rgba(255,255,255,0.1)", borderRadius: height / 2, overflow: "hidden" }}>
        <div style={{ width: `${progress * 100}%`, height: "100%", backgroundColor: color, borderRadius: height / 2 }} />
      </div>
      {showTime && (
        <div style={{ display: "flex", justifyContent: "space-between", marginTop: 8, color: "rgba(255,255,255,0.4)", fontSize: 14, fontFamily: "Inter, sans-serif", fontVariantNumeric: "tabular-nums" }}>
          <span>{formatT(currentTime)}</span>
          <span>{formatT(totalDurationSeconds)}</span>
        </div>
      )}
    </div>
  );
};
```

---

## Dynamic Duration from Audio

Calculate composition duration based on the audio file length.

```tsx
import { getAudioDurationInSeconds } from "@remotion/media-utils";
import { CalculateMetadataFunction } from "remotion";

type Props = { audioSrc: string; [key: string]: unknown };

export const calculateAudiogramMetadata: CalculateMetadataFunction<Props> = async ({ props }) => {
  const fps = 30;
  const duration = await getAudioDurationInSeconds(props.audioSrc);
  return {
    durationInFrames: Math.ceil(duration * fps),
    fps,
  };
};
```