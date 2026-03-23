# Sound Effects & Audio Integration for Remotion

Comprehensive guide to audio integration, SFX patterns, voiceover, audio visualization, and volume management in Remotion video projects.

---

## SFX Categories & When to Use Them

| Category | Effects | When to Use | Suggested Volume |
|----------|---------|-------------|-----------------|
| **Transitions** | Whoosh, swipe, swoosh, page-turn, slide | Scene changes, element entrances/exits | 0.3 - 0.6 |
| **UI Sounds** | Click, pop, toggle, notification, ding, tap | Button presses, selections, checkmarks | 0.2 - 0.5 |
| **Impacts** | Boom, thud, slam, glass break, punch, stomp | Emphasis, dramatic reveals, title drops | 0.5 - 0.8 |
| **Risers** | Tension build, reverse cymbal, sweep up, swell | Building anticipation before a reveal | 0.3 - 0.6 |
| **Drops** | Bass drop, hit, stab, cinematic hit | Key moment emphasis, beat drops | 0.5 - 0.8 |
| **Ambient** | Keyboard typing, crowd, office, rain, wind, static | Background atmosphere, scene-setting | 0.1 - 0.2 |
| **Musical** | Stinger, jingle, sting, logo reveal | Branding moments, intros/outros | 0.4 - 0.7 |
| **Mechanical** | Camera shutter, typewriter, clock tick, switch | Tech demos, retro effects | 0.3 - 0.5 |
| **Nature** | Bird chirps, water, thunder, fire crackle | Outdoor scenes, nature content | 0.1 - 0.3 |

---

## Free SFX Sources

| Source | URL | License |
|--------|-----|---------|
| Freesound.org | freesound.org | CC0 / CC-BY (check per file) |
| Pixabay | pixabay.com/sound-effects | Royalty-free, no attribution |
| Mixkit | mixkit.co/free-sound-effects | Royalty-free |
| Zapsplat | zapsplat.com | Free with attribution |
| BBC Sound Effects | sound-effects.bbcrewind.co.uk | Personal/educational use |

Place downloaded files in `public/sfx/` for access via `staticFile()`.

---

## Basic Audio Integration

### Playing a Sound Effect at a Specific Frame

```tsx
import { Audio, Sequence, staticFile } from 'remotion';

export const MyScene: React.FC = () => {
  return (
    <>
      {/* SFX plays when this Sequence starts (frame 30) */}
      <Sequence from={30} durationInFrames={30}>
        <Audio src={staticFile('sfx/whoosh.mp3')} volume={0.5} />
      </Sequence>

      {/* Impact sound at frame 60 */}
      <Sequence from={60} durationInFrames={45}>
        <Audio src={staticFile('sfx/impact.mp3')} volume={0.7} />
      </Sequence>

      {/* Background music for the entire video */}
      <Audio src={staticFile('music/background.mp3')} volume={0.25} />
    </>
  );
};
```

### Multiple SFX Synced to Animations

```tsx
import { Audio, Sequence, staticFile, useCurrentFrame, interpolate } from 'remotion';

export const AnimatedList: React.FC = () => {
  const items = ['Item 1', 'Item 2', 'Item 3', 'Item 4'];

  return (
    <>
      {items.map((item, i) => {
        const enterFrame = 20 + i * 12; // Staggered entrance
        return (
          <Sequence key={item} from={enterFrame} durationInFrames={15}>
            <Audio src={staticFile('sfx/pop.mp3')} volume={0.3} />
          </Sequence>
        );
      })}
    </>
  );
};
```

---

## Volume Control Patterns

### Static Volume

```tsx
<Audio src={staticFile('music/bg.mp3')} volume={0.3} />
```

### Dynamic Volume (Fade In / Fade Out)

```tsx
<Audio
  src={staticFile('music/background.mp3')}
  volume={(f) =>
    interpolate(f, [0, 30, 870, 900], [0, 0.3, 0.3, 0], {
      extrapolateLeft: 'clamp',
      extrapolateRight: 'clamp',
    })
  }
/>
```

### Audio Ducking (Lower Music During Voiceover)

```tsx
const VOICEOVER_START = 60;
const VOICEOVER_END = 300;
const DUCK_TRANSITION = 15; // frames to fade

// Music volume function — ducks during voiceover
const musicVolume = (f: number) => {
  return interpolate(
    f,
    [
      VOICEOVER_START - DUCK_TRANSITION,
      VOICEOVER_START,
      VOICEOVER_END,
      VOICEOVER_END + DUCK_TRANSITION,
    ],
    [0.4, 0.08, 0.08, 0.4],
    { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }
  );
};

// In JSX:
<Audio src={staticFile('music/bg.mp3')} volume={musicVolume} />
<Sequence from={VOICEOVER_START}>
  <Audio src={staticFile('voiceover.mp3')} volume={0.9} />
</Sequence>
```

### Volume Envelope (Complex Pattern)

```tsx
// Create a volume envelope for dramatic effect
const dramaticVolume = (f: number) => {
  // Soft intro -> build -> peak -> soft outro
  return interpolate(
    f,
    [0, 30, 60, 90, 150, 200, 250, 270, 300],
    [0, 0.1, 0.2, 0.5, 0.5, 0.7, 0.3, 0.1, 0],
    { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }
  );
};
```

---

## Volume Level Guide

| Audio Type | Volume Range | Notes |
|-----------|-------------|-------|
| Background music (with VO) | 0.05 - 0.15 | Very subtle, never compete with voice |
| Background music (no VO) | 0.2 - 0.4 | Present but not overwhelming |
| Voiceover / narration | 0.8 - 1.0 | Primary audio, clear and dominant |
| SFX (subtle transitions) | 0.2 - 0.4 | Noticeable but not jarring |
| SFX (impacts/emphasis) | 0.5 - 0.8 | Punchy, attention-grabbing |
| SFX (UI clicks/pops) | 0.15 - 0.35 | Subtle feedback |
| Ambient / atmosphere | 0.05 - 0.15 | Barely perceptible, fills silence |
| Logo / stinger | 0.5 - 0.7 | Brief, prominent |

---

## Dynamic Duration Based on Audio

### Calculate Video Duration from Voiceover Length

```tsx
import { CalculateMetadataFunction } from 'remotion';
import { getAudioDurationInSeconds } from '@remotion/media-utils';
import { staticFile } from 'remotion';

type Props = {
  voiceoverFile: string;
};

export const calculateMetadata: CalculateMetadataFunction<Props> = async ({ props }) => {
  const voiceDuration = await getAudioDurationInSeconds(
    staticFile(props.voiceoverFile)
  );

  const fps = 30;
  const introPadding = 60;  // 2 seconds intro
  const outroPadding = 90;  // 3 seconds outro
  const totalFrames = Math.ceil(voiceDuration * fps) + introPadding + outroPadding;

  return {
    fps,
    durationInFrames: totalFrames,
    width: 1920,
    height: 1080,
  };
};
```

### Multiple Audio Sources — Calculate Max Duration

```tsx
export const calculateMetadata: CalculateMetadataFunction<Props> = async ({ props }) => {
  const [voDuration, musicDuration] = await Promise.all([
    getAudioDurationInSeconds(staticFile('voiceover.mp3')),
    getAudioDurationInSeconds(staticFile('music.mp3')),
  ]);

  const fps = 30;
  const contentFrames = Math.ceil(Math.max(voDuration, musicDuration) * fps);

  return {
    fps,
    durationInFrames: contentFrames + 60, // +2s padding
  };
};
```

---

## AI Voiceover Integration

### edge-tts — DEFAULT (Free, No API Key)

Microsoft Edge neural voices. Zero cost, 300+ voices, neural quality. Install once: `pip install edge-tts`

**CLI (simplest):**
```bash
edge-tts --voice en-US-JennyNeural --text "Your narration here." --write-media public/voiceover.mp3
```

**Python script (for multi-segment voiceover):**
```python
# scripts/generate-voiceover.py
import edge_tts
import asyncio

VOICE = "en-US-JennyNeural"  # or en-US-GuyNeural, en-GB-SoniaNeural, en-US-AriaNeural

async def generate(text: str, output: str = "public/voiceover.mp3"):
    await edge_tts.Communicate(text, voice=VOICE).save(output)
    print(f"Saved: {output}")

asyncio.run(generate("Welcome to our product demo. Today we will walk you through the new features."))
```

**Run before render:**
```bash
python scripts/generate-voiceover.py && npx remotion render src/index.ts MyVideo out/video.mp4
```

**Voice quick-reference:**

| Voice | Style |
|---|---|
| `en-US-JennyNeural` | Friendly female (default) |
| `en-US-GuyNeural` | Neutral male |
| `en-US-AriaNeural` | Expressive female |
| `en-US-DavisNeural` | Casual male |
| `en-GB-SoniaNeural` | British female |
| `en-GB-RyanNeural` | British male |
| `en-AU-NatashaNeural` | Australian female |

List all voices: `edge-tts --list-voices`

**Use in Remotion:**
```tsx
<Audio src={staticFile('voiceover.mp3')} volume={0.9} />
```

---

### OpenAI TTS (Paid, High Quality)

```typescript
import OpenAI from 'openai';
import fs from 'fs';

const openai = new OpenAI();

async function generateVoiceover(text: string, outputPath: string) {
  const response = await openai.audio.speech.create({
    model: 'tts-1-hd',      // or 'tts-1' for faster/cheaper
    voice: 'onyx',           // alloy, echo, fable, onyx, nova, shimmer
    input: text,
    speed: 1.0,              // 0.25 to 4.0
    response_format: 'mp3',
  });

  const buffer = Buffer.from(await response.arrayBuffer());
  fs.writeFileSync(outputPath, buffer);
}
```

### ElevenLabs (Paid, Premium Quality)

```typescript
import fs from 'fs';

async function generateVoiceover(text: string, outputPath: string) {
  const VOICE_ID = 'pNInz6obpgDQGcFmaJgB'; // Adam — change to your preferred voice
  const API_KEY = process.env.ELEVEN_LABS_API_KEY;

  const response = await fetch(
    `https://api.elevenlabs.io/v1/text-to-speech/${VOICE_ID}`,
    {
      method: 'POST',
      headers: { 'xi-api-key': API_KEY!, 'Content-Type': 'application/json' },
      body: JSON.stringify({
        text,
        model_id: 'eleven_multilingual_v2',
        voice_settings: { stability: 0.5, similarity_boost: 0.75, style: 0.3, use_speaker_boost: true },
      }),
    }
  );

  if (!response.ok) throw new Error(`ElevenLabs API error: ${response.status}`);
  fs.writeFileSync(outputPath, Buffer.from(await response.arrayBuffer()));
}
```

---

## Audio Visualization

### Waveform / Bar Visualization

```tsx
import { useCurrentFrame, useVideoConfig, Audio, staticFile, AbsoluteFill } from 'remotion';
import { visualizeAudio, useWindowedAudioData } from '@remotion/media-utils';

const audioSrc = staticFile('music.mp3');

export const AudioBars: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps, width, height } = useVideoConfig();

  const audioData = useWindowedAudioData({
    src: audioSrc,
    frame,
    fps,
    windowInSeconds: 0.5,
  });

  if (!audioData) return null;

  const visualization = visualizeAudio({
    fps,
    frame,
    audioData,
    numberOfSamples: 64,    // Number of bars
    smoothing: true,         // Smooth transitions between frames
    optimizeFor: 'speed',    // 'speed' or 'accuracy'
  });

  const barWidth = width / visualization.length;

  return (
    <AbsoluteFill style={{ backgroundColor: '#0a0a0a' }}>
      <Audio src={audioSrc} />
      <svg width={width} height={height} style={{ position: 'absolute' }}>
        {visualization.map((value, i) => {
          const barHeight = value * height * 0.8;
          return (
            <rect
              key={i}
              x={i * barWidth + 2}
              y={height - barHeight}
              width={barWidth - 4}
              height={barHeight}
              rx={4}
              fill={`hsl(${210 + value * 60}, 80%, ${50 + value * 30}%)`}
            />
          );
        })}
      </svg>
    </AbsoluteFill>
  );
};
```

### Circular Audio Visualization

```tsx
export const AudioCircle: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const audioData = useWindowedAudioData({
    src: staticFile('music.mp3'),
    frame, fps,
    windowInSeconds: 0.3,
  });

  if (!audioData) return null;

  const viz = visualizeAudio({
    fps, frame, audioData,
    numberOfSamples: 32,
    smoothing: true,
    optimizeFor: 'speed',
  });

  const centerX = 960;
  const centerY = 540;
  const baseRadius = 150;

  return (
    <AbsoluteFill>
      <Audio src={staticFile('music.mp3')} />
      <svg width={1920} height={1080}>
        {viz.map((value, i) => {
          const angle = (i / viz.length) * Math.PI * 2 - Math.PI / 2;
          const radius = baseRadius + value * 200;
          const x1 = centerX + Math.cos(angle) * baseRadius;
          const y1 = centerY + Math.sin(angle) * baseRadius;
          const x2 = centerX + Math.cos(angle) * radius;
          const y2 = centerY + Math.sin(angle) * radius;
          return (
            <line
              key={i}
              x1={x1} y1={y1} x2={x2} y2={y2}
              stroke={`hsl(${280 + value * 80}, 90%, 65%)`}
              strokeWidth={3}
              strokeLinecap="round"
            />
          );
        })}
        {/* Center circle */}
        <circle cx={centerX} cy={centerY} r={baseRadius - 5} fill="none" stroke="#fff" strokeWidth={2} opacity={0.3} />
      </svg>
    </AbsoluteFill>
  );
};
```

### Audio-Reactive Element (Pulse on Beat)

```tsx
export const PulsingLogo: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const audioData = useWindowedAudioData({
    src: staticFile('music.mp3'),
    frame, fps,
    windowInSeconds: 0.1, // Short window for beat detection
  });

  if (!audioData) return null;

  const viz = visualizeAudio({
    fps, frame, audioData,
    numberOfSamples: 4,  // Few samples — just need overall energy
    smoothing: false,     // No smoothing for responsive beats
    optimizeFor: 'accuracy',
  });

  // Average energy across all samples
  const energy = viz.reduce((a, b) => a + b, 0) / viz.length;
  const scale = 1 + energy * 0.3;     // Scale 1.0 to 1.3 based on audio
  const glow = energy * 40;           // Glow intensity

  return (
    <div style={{
      transform: `scale(${scale})`,
      filter: `drop-shadow(0 0 ${glow}px rgba(99, 102, 241, ${energy}))`,
      transition: 'none',
    }}>
      <img src={staticFile('logo.png')} width={200} />
    </div>
  );
};
```

---

## Audio Timing Sync Patterns

### Sync Animations to Beat Markers

```tsx
// Pre-defined beat timestamps (in frames at 30fps)
const BEATS = [0, 15, 30, 45, 60, 75, 90, 105, 120]; // Every 0.5s at 120 BPM

export const BeatSyncedScene: React.FC = () => {
  const frame = useCurrentFrame();

  // Find the most recent beat
  const currentBeat = BEATS.filter((b) => b <= frame).length - 1;
  const framesSinceLastBeat = frame - BEATS[currentBeat];

  // Flash on beat
  const flashOpacity = interpolate(framesSinceLastBeat, [0, 5], [0.8, 0], {
    extrapolateRight: 'clamp',
  });

  // Scale punch on beat
  const beatScale = interpolate(framesSinceLastBeat, [0, 3, 10], [1.1, 1.15, 1], {
    extrapolateRight: 'clamp',
  });

  return (
    <AbsoluteFill>
      {/* Beat flash overlay */}
      <div style={{
        position: 'absolute', inset: 0,
        backgroundColor: '#fff',
        opacity: flashOpacity,
        pointerEvents: 'none',
      }} />
      {/* Beat-reactive element */}
      <div style={{ transform: `scale(${beatScale})` }}>
        <Content />
      </div>
    </AbsoluteFill>
  );
};
```

### Scene Transitions on Music Cues

```tsx
import { Sequence, Audio, staticFile } from 'remotion';

// Organize scenes around music structure
export const MusicVideo: React.FC = () => {
  // Music structure in frames (at 30fps)
  const INTRO_END = 120;      // 4 seconds
  const VERSE1_END = 360;     // 12 seconds
  const CHORUS1_END = 540;    // 18 seconds
  const VERSE2_END = 720;     // 24 seconds
  const CHORUS2_END = 900;    // 30 seconds

  return (
    <>
      <Audio src={staticFile('music/track.mp3')} />

      <Sequence from={0} durationInFrames={INTRO_END}>
        <IntroScene />
      </Sequence>
      <Sequence from={INTRO_END} durationInFrames={VERSE1_END - INTRO_END}>
        <Verse1Scene />
      </Sequence>
      <Sequence from={VERSE1_END} durationInFrames={CHORUS1_END - VERSE1_END}>
        <ChorusScene />
      </Sequence>
      <Sequence from={CHORUS1_END} durationInFrames={VERSE2_END - CHORUS1_END}>
        <Verse2Scene />
      </Sequence>
      <Sequence from={VERSE2_END} durationInFrames={CHORUS2_END - VERSE2_END}>
        <ChorusScene />
      </Sequence>
    </>
  );
};
```

---

## Audio Troubleshooting

| Issue | Cause | Fix |
|-------|-------|-----|
| No audio in output | Missing `<Audio>` component | Add `<Audio src={...} />` to composition |
| Audio plays in preview but not render | Audio file not in `public/` | Move to `public/` and use `staticFile()` |
| Audio out of sync | Wrong fps or variable frame rate source | Ensure audio is CBR (constant bit rate) MP3 or WAV |
| Clicks/pops at transitions | Abrupt volume changes | Add 2-5 frame fade at start/end of each clip |
| Audio too quiet after render | Volume set too low | Check volume function returns expected values |
| Render fails with audio error | Unsupported format | Convert to MP3 (44.1kHz, 16-bit) or WAV |
| Audio visualization empty | `useWindowedAudioData` returns null | Add null check; data loads asynchronously |
