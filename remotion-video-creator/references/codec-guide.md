# Video Codec & Rendering Guide for Remotion

Complete reference for video output formats, encoding settings, and rendering optimization.

---

## Codec Comparison

| Codec | Container | Quality | File Size | Compatibility | Best For |
|-------|-----------|---------|-----------|---------------|----------|
| H.264 (AVC) | `.mp4` | Good | Medium | Universal — every device | Social media, general distribution |
| H.265 (HEVC) | `.mp4` | Better | 30-50% smaller than H.264 | Modern devices/browsers | Storage-efficient, Apple ecosystem |
| VP8 | `.webm` | Good | Medium | All browsers | Web embedding, legacy |
| VP9 | `.webm` | Better | 30-50% smaller than VP8 | Modern browsers | Web, YouTube internal |
| ProRes | `.mov` | Lossless/Near-lossless | Very Large (1GB+/min) | Apple, pro editing software | Post-production, DaVinci Resolve |
| GIF | `.gif` | Low (256 colors) | Large for quality | Universal | Short loops, no audio, previews |

---

## Remotion Render Commands

### CLI Rendering

```bash
# H.264 (default, most compatible)
npx remotion render src/index.ts MyComposition out/video.mp4 --codec=h264

# H.265 (smaller files, modern devices)
npx remotion render src/index.ts MyComposition out/video.mp4 --codec=h265

# VP9 WebM (web embedding)
npx remotion render src/index.ts MyComposition out/video.webm --codec=vp9

# VP8 WebM (broader browser support)
npx remotion render src/index.ts MyComposition out/video.webm --codec=vp8

# ProRes (professional editing)
npx remotion render src/index.ts MyComposition out/video.mov --codec=prores --prores-profile=hq

# GIF (short loops)
npx remotion render src/index.ts MyComposition out/animation.gif --codec=gif

# Still image (single frame)
npx remotion still src/index.ts MyComposition out/thumbnail.png --frame=0
```

### Node.js API

```tsx
import { renderMedia, renderStill } from '@remotion/renderer';
import { bundle } from '@remotion/bundler';
import path from 'path';

const bundled = await bundle({
  entryPoint: path.resolve('./src/index.ts'),
});

// Render video
await renderMedia({
  composition: {
    id: 'MyComposition',
    width: 1920,
    height: 1080,
    fps: 30,
    durationInFrames: 300,
    defaultProps: {},
    defaultCodec: 'h264',
  },
  serveUrl: bundled,
  codec: 'h264',
  outputLocation: 'out/video.mp4',
  crf: 18,
  // Optional settings:
  imageFormat: 'jpeg',       // 'png' for transparency
  jpegQuality: 85,           // 0-100, only for jpeg
  scale: 1,                  // 0.5 for half-res preview
  concurrency: null,         // null = auto, or number
  everyNthFrame: 1,          // 2 = render every other frame (for preview)
  audioBitrate: '320k',      // Audio quality
  videoBitrate: '10M',       // Override CRF with target bitrate
});

// Render still frame
await renderStill({
  composition: { /* ... */ },
  serveUrl: bundled,
  output: 'out/thumbnail.png',
  frame: 0,
  imageFormat: 'png',
  scale: 2, // 2x resolution for thumbnails
});
```

---

## CRF (Constant Rate Factor) Guide

CRF controls quality vs. file size. Lower = better quality, larger file.

| CRF | Quality Level | File Size | Use Case |
|-----|--------------|-----------|----------|
| 0 | Lossless | Massive | Archival, master copy |
| 10-12 | Virtually lossless | Very large | Professional mastering |
| 15 | Excellent | Large | Professional delivery, YouTube upload |
| 18 | High quality | Medium-large | **Recommended default** |
| 23 | Good quality | Medium | H.264 default, acceptable for most uses |
| 28 | Medium | Small | Draft review, fast iteration |
| 35 | Low | Very small | Quick preview only |
| 51 | Worst possible | Tiny | Not recommended |

**Codec-specific CRF ranges:**
- H.264: 0-51 (default 23, recommended 18)
- H.265: 0-51 (default 28, recommended 22 — better quality per CRF unit)
- VP9: 0-63 (default 31, recommended 23-28)

---

## Platform-Specific Encoding Presets

### TikTok / Instagram Reels
```bash
npx remotion render src/index.ts MyComp out/tiktok.mp4 \
  --codec=h264 --crf=18 \
  --props='{"width":1080,"height":1920}'
# Max 287MB, max 10 minutes (TikTok), max 90s (Reels)
# 30fps recommended, 9:16 aspect ratio
```

### YouTube
```bash
npx remotion render src/index.ts MyComp out/youtube.mp4 \
  --codec=h264 --crf=15 \
  --video-bitrate=20M --audio-bitrate=320k
# High bitrate for YouTube re-encoding: 10-20 Mbps for 1080p, 35-68 Mbps for 4K
# 16:9 aspect ratio, 24/30/60fps
```

### Twitter / X
```bash
npx remotion render src/index.ts MyComp out/twitter.mp4 \
  --codec=h264 --crf=20
# Max 512MB, max 2:20 duration
# Recommended: 1280x720 or 1920x1080, 30-60fps
```

### LinkedIn
```bash
npx remotion render src/index.ts MyComp out/linkedin.mp4 \
  --codec=h264 --crf=18
# Max 5GB, max 10 minutes
# 1920x1080 or 1080x1080, 30fps
```

### Web Embedding
```bash
npx remotion render src/index.ts MyComp out/web.webm \
  --codec=vp9 --crf=28
# Smaller files for faster loading
# Consider providing MP4 fallback for Safari
```

### Professional Editing (DaVinci Resolve, Premiere, Final Cut)
```bash
npx remotion render src/index.ts MyComp out/edit.mov \
  --codec=prores --prores-profile=hq
# Massive files (~1GB/minute at 1080p) but no quality loss
# Use for compositing or color grading workflows
```

---

## Transparent Video

### ProRes 4444 (for editing software)
```bash
npx remotion render src/index.ts MyComp out/transparent.mov \
  --codec=prores \
  --prores-profile=4444 \
  --pixel-format=yuva444p10le
```

### VP9 WebM (for web playback)
```bash
npx remotion render src/index.ts MyComp out/transparent.webm \
  --codec=vp9 \
  --pixel-format=yuva420p
```

### Important: Transparent video requirements
- Your `<AbsoluteFill>` must NOT have a background color (or use `transparent`)
- Use `--image-format=png` (default) — JPEG does not support transparency
- Test with a checkerboard background to verify alpha channel

---

## ProRes Profile Reference

| Profile | Flag | Quality | Bitrate (1080p30) | Use For |
|---------|------|---------|-------------------|---------|
| ProRes 422 Proxy | `proxy` | Preview | ~45 Mbps | Offline editing |
| ProRes 422 LT | `light` | Good | ~102 Mbps | Simple edits |
| ProRes 422 | `standard` | High | ~147 Mbps | Standard post-production |
| ProRes 422 HQ | `hq` | Very High | ~220 Mbps | High-quality finishing |
| ProRes 4444 | `4444` | Highest + Alpha | ~330 Mbps | VFX, transparent video |
| ProRes 4444 XQ | `4444-xq` | Maximum | ~500 Mbps | HDR, highest quality |

```bash
npx remotion render src/index.ts MyComp out/video.mov --codec=prores --prores-profile=hq
```

---

## Performance Optimization

### Faster Renders
```bash
# Use JPEG (no alpha) — faster frame capture
--image-format=jpeg --jpeg-quality=80

# Limit concurrency to prevent OOM
--concurrency=50%

# Half-resolution preview
--scale=0.5

# Skip frames for quick preview (renders every 2nd frame)
--every-nth-frame=2

# Limit frames for testing
--frames=0-90
```

### GIF Optimization
```bash
# GIF tips: keep dimensions small and fps low
npx remotion render src/index.ts MyComp out/anim.gif \
  --codec=gif \
  --scale=0.5 \
  --every-nth-frame=2
# Results in ~15fps at half resolution
# GIFs over 5MB load slowly — aim for 2-3 second loops
```

### Memory Management
```bash
# For complex compositions, limit concurrency
--concurrency=2

# For very long videos, use Lambda for parallel rendering
npx remotion lambda render ...

# Monitor with verbose logging
--log=verbose
```

---

## Audio Settings

| Setting | Flag | Default | Recommended |
|---------|------|---------|-------------|
| Audio bitrate | `--audio-bitrate` | 128k | 320k for music, 192k for voice |
| Audio codec | `--audio-codec` | aac | aac (mp4), opus (webm) |
| Mute | `--muted` | false | true for silent videos |
| Enforce audio | `--enforce-audio-track` | false | true to always include audio track |

```bash
# High quality audio
--audio-bitrate=320k

# No audio (faster render)
--muted

# Force audio track even if no audio in composition
--enforce-audio-track
```

---

## Resolution Presets

| Name | Dimensions | Aspect | Use For |
|------|-----------|--------|---------|
| 1080p Landscape | 1920x1080 | 16:9 | YouTube, general |
| 1080p Portrait | 1080x1920 | 9:16 | TikTok, Reels, Shorts |
| 1080p Square | 1080x1080 | 1:1 | Instagram feed, LinkedIn |
| 720p | 1280x720 | 16:9 | Twitter, fast renders |
| 4K | 3840x2160 | 16:9 | High-end production |
| 4K Portrait | 2160x3840 | 9:16 | High-end vertical |
| Instagram Story | 1080x1920 | 9:16 | Stories, Reels |

```tsx
// In Root.tsx composition registration
<Composition
  id="TikTok"
  component={MyVideo}
  width={1080}
  height={1920}
  fps={30}
  durationInFrames={300}
/>
```
