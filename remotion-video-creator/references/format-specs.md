# Video Format Specifications — All Platforms

> Quick reference for resolution, FPS, duration, codec, and safe zones per platform.

---

## Platform Specifications

| Platform | Width | Height | Aspect | FPS | Max Duration | Codec | Max Size | Notes |
|----------|-------|--------|--------|-----|-------------|-------|----------|-------|
| TikTok | 1080 | 1920 | 9:16 | 30 | 10 min | H.264 MP4 | 287.6 MB | First 3s critical for hook |
| Instagram Reels | 1080 | 1920 | 9:16 | 30 | 90s | H.264 MP4 | 250 MB | Cover frame at 1s mark |
| Instagram Stories | 1080 | 1920 | 9:16 | 30 | 60s | H.264 MP4 | 250 MB | 15s segments auto-split |
| Instagram Feed | 1080 | 1080 | 1:1 | 30 | 60s | H.264 MP4 | 250 MB | Square or 4:5 (1080x1350) |
| YouTube Shorts | 1080 | 1920 | 9:16 | 30 | 60s | H.264 MP4 | 256 MB | Vertical only, no landscape |
| YouTube Standard | 1920 | 1080 | 16:9 | 30/60 | 12 hr | H.264 MP4 | 256 GB | 1080p30 recommended default |
| YouTube 4K | 3840 | 2160 | 16:9 | 30/60 | 12 hr | H.264/VP9 | 256 GB | High bitrate: 35-68 Mbps |
| Twitter/X Video | 1920 | 1080 | 16:9 | 30 | 2m 20s | H.264 MP4 | 512 MB | 1280x720 min recommended |
| Twitter/X Square | 1080 | 1080 | 1:1 | 30 | 2m 20s | H.264 MP4 | 512 MB | Higher engagement than 16:9 |
| LinkedIn Video | 1920 | 1080 | 16:9 | 30 | 10 min | H.264 MP4 | 5 GB | Also supports 1:1, 9:16 |
| Facebook Feed | 1080 | 1080 | 1:1 | 30 | 240 min | H.264 MP4 | 10 GB | Square preferred for feed |
| Facebook Reels | 1080 | 1920 | 9:16 | 30 | 90s | H.264 MP4 | 4 GB | Similar specs to IG Reels |
| Pinterest Video | 1000 | 1500 | 2:3 | 25 | 15 min | H.264 MP4 | 2 GB | Vertical preferred |
| Snapchat | 1080 | 1920 | 9:16 | 30 | 60s | H.264 MP4 | 256 MB | Full screen vertical |
| Threads | 1080 | 1920 | 9:16 | 30 | 5 min | H.264 MP4 | 250 MB | Same as IG infrastructure |

---

## Safe Zones — Critical Content Boundaries

Platform UIs overlay buttons, usernames, captions, and navigation on top of your video. Keep all critical content (text, faces, logos, CTAs) within the safe zone.

### TikTok Safe Zones
```
+---------------------------+
|   TOP: 150px unsafe       |  ← username, follow button
|                           |
|   +-------------------+   |
|   |                   |   |
|   |   SAFE ZONE       |   |  ← center 80% of frame
|   |   (critical text) |   |
|   |                   |   |
|   +-------------------+   |
|                       |   |  ← RIGHT: 70px unsafe (like, comment, share buttons)
|   BOTTOM: 270px unsafe    |  ← caption text, music ticker
+---------------------------+
```
- Top: 150px (username, follow button)
- Bottom: 270px (caption, music ticker, nav bar)
- Right: 70px (action buttons: like, comment, share, bookmark)
- Left: Safe

### Instagram Reels Safe Zones
```
Top: 120px (header, camera, close button)
Bottom: 200px (caption, audio, share row)
Right: 60px (like, comment, share, save buttons)
Left: Safe
```

### YouTube Shorts Safe Zones
```
Top: 100px (status bar, back button)
Bottom: 180px (title, subscribe, controls)
Right: 60px (like, dislike, comment, share)
Left: Safe
```

### General Rule
**Keep ALL critical text and visual elements within the center 80% of the frame** — that is, 10% margin on all sides. This covers most platforms safely.

For 1080x1920 (9:16):
- Horizontal safe area: x=108 to x=972 (center 864px)
- Vertical safe area: y=192 to y=1728 (center 1536px)

For 1920x1080 (16:9):
- Horizontal safe area: x=192 to x=1728
- Vertical safe area: y=108 to y=972

---

## Composition Presets — Copy-Paste Ready

### Vertical (9:16) — TikTok, Reels, Shorts, Stories
```tsx
<Composition
  id="VerticalVideo"
  component={MyVideo}
  width={1080}
  height={1920}
  fps={30}
  durationInFrames={900} // 30s
/>
```

### Landscape (16:9) — YouTube, LinkedIn, Twitter
```tsx
<Composition
  id="LandscapeVideo"
  component={MyVideo}
  width={1920}
  height={1080}
  fps={30}
  durationInFrames={1800} // 60s
/>
```

### Square (1:1) — Instagram Feed, Facebook, Twitter
```tsx
<Composition
  id="SquareVideo"
  component={MyVideo}
  width={1080}
  height={1080}
  fps={30}
  durationInFrames={900} // 30s
/>
```

### Portrait (4:5) — Instagram Feed Optimized
```tsx
<Composition
  id="PortraitVideo"
  component={MyVideo}
  width={1080}
  height={1350}
  fps={30}
  durationInFrames={900} // 30s
/>
```

### Pinterest (2:3)
```tsx
<Composition
  id="PinterestVideo"
  component={MyVideo}
  width={1000}
  height={1500}
  fps={25}
  durationInFrames={375} // 15s
/>
```

---

## Duration Quick Reference

| Duration (seconds) | Frames @ 30fps | Frames @ 60fps | Best For |
|--------------------|----------------|----------------|----------|
| 5 | 150 | 300 | Ad bumper, logo sting |
| 10 | 300 | 600 | Quick tip, promo |
| 15 | 450 | 900 | Story segment, ad |
| 30 | 900 | 1800 | Short explainer, trailer |
| 60 | 1800 | 3600 | Full short, tutorial clip |
| 90 | 2700 | 5400 | Max Reels/Facebook Reels |
| 120 | 3600 | 7200 | Standard explainer |
| 140 | 4200 | 8400 | Max Twitter video |

---

## Multi-Format Strategy

Design at **1080x1920 (9:16)** as the primary canvas, then adapt:

### Approach 1: Responsive Composition
```tsx
const MyVideo: React.FC<{ format: '9:16' | '16:9' | '1:1' }> = ({ format }) => {
  const { width, height } = useVideoConfig();
  // Layout adapts based on aspect ratio
  const isVertical = height > width;
  const isSquare = width === height;

  return (
    <AbsoluteFill>
      {isVertical ? <VerticalLayout /> : isSquare ? <SquareLayout /> : <LandscapeLayout />}
    </AbsoluteFill>
  );
};
```

### Approach 2: Multiple Compositions
```tsx
// Register multiple compositions with the same component
<Composition id="TikTok" component={MyVideo} width={1080} height={1920} fps={30} durationInFrames={900} />
<Composition id="YouTube" component={MyVideo} width={1920} height={1080} fps={30} durationInFrames={900} />
<Composition id="Instagram" component={MyVideo} width={1080} height={1080} fps={30} durationInFrames={900} />
```

### Approach 3: Scale and Crop
```tsx
// Render at 1080x1920, then scale/crop for other formats
const scaleForLandscape = (
  <AbsoluteFill style={{ transform: 'scale(1.78) rotate(0deg)', transformOrigin: 'center' }}>
    <VerticalContent />
  </AbsoluteFill>
);
```

---

## Render Settings by Platform

```bash
# TikTok / Instagram Reels / YouTube Shorts (high quality, small file)
npx remotion render src/index.ts MyVideo out/tiktok.mp4 --codec=h264 --crf=18 --video-bitrate=8M

# YouTube 1080p (high quality)
npx remotion render src/index.ts MyVideo out/youtube.mp4 --codec=h264 --crf=15 --video-bitrate=12M

# YouTube 4K
npx remotion render src/index.ts MyVideo out/youtube4k.mp4 --codec=h264 --crf=15 --video-bitrate=40M

# Twitter (optimized file size)
npx remotion render src/index.ts MyVideo out/twitter.mp4 --codec=h264 --crf=23 --video-bitrate=5M

# GIF (for short loops)
npx remotion render src/index.ts MyVideo out/loop.gif --codec=gif --every-nth-frame=2

# ProRes (for editing, lossless)
npx remotion render src/index.ts MyVideo out/master.mov --codec=prores --prores-profile=4444
```

---

## Audio Specifications

| Platform | Audio Codec | Sample Rate | Bitrate | Channels |
|----------|------------|-------------|---------|----------|
| All platforms | AAC | 44100 Hz | 128-256 kbps | Stereo |
| YouTube (recommended) | AAC | 48000 Hz | 384 kbps | Stereo |
| Podcast video | AAC | 44100 Hz | 192 kbps | Mono/Stereo |

```tsx
// Audio in Remotion
<Audio src={staticFile('bgm.mp3')} volume={0.3} />

// Fade audio in/out
<Audio
  src={staticFile('bgm.mp3')}
  volume={(f) => {
    const { durationInFrames } = useVideoConfig();
    if (f < 15) return interpolate(f, [0, 15], [0, 0.3]);
    if (f > durationInFrames - 15) return interpolate(f, [durationInFrames - 15, durationInFrames], [0.3, 0]);
    return 0.3;
  }}
/>
```
