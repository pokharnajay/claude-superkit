---
name: render-engine
description: Remotion project scaffolding, CLI and Node.js API rendering, multi-format output. Use when user wants to set up a new Remotion project, render a video, configure output format, or optimize rendering performance.
---

# Render Engine

Complete rendering pipeline for Remotion videos — from project scaffolding to MP4 output.

## Project Scaffolding

### New Project
```bash
npx create-video@latest my-video
```

Creates:
```
my-video/
├── src/
│   ├── index.ts          # registerRoot entry point
│   ├── Root.tsx           # Composition registrations
│   └── MyComposition.tsx  # Your first video component
├── public/                # Static assets (images, audio, fonts)
├── package.json
├── tsconfig.json
└── remotion.config.ts     # Remotion configuration
```

### Minimal Manual Setup
```bash
npm init -y
npm install remotion @remotion/cli @remotion/bundler @remotion/renderer @remotion/transitions @remotion/animation-utils @remotion/google-fonts @remotion/layout-utils @remotion/media-utils @remotion/shapes @remotion/paths @remotion/noise @remotion/captions @remotion/tailwind
npx remotion browser ensure
```

### Essential Files
```tsx
// src/index.ts
import { registerRoot } from 'remotion';
import { RemotionRoot } from './Root';
registerRoot(RemotionRoot);
```

```tsx
// src/Root.tsx
import { Composition } from 'remotion';
import { MyVideo } from './compositions/MyVideo';

export const RemotionRoot: React.FC = () => (
  <>
    <Composition
      id="MyVideo"
      component={MyVideo}
      durationInFrames={900}
      fps={30}
      width={1080}
      height={1920}
    />
  </>
);
```

```tsx
// remotion.config.ts
import { Config } from '@remotion/cli/config';
Config.setVideoImageFormat('jpeg');
Config.setOverwriteOutput(true);
```

## CLI Rendering

### Basic Commands
```bash
# Render video
npx remotion render src/index.ts MyVideo out/video.mp4

# Render still image
npx remotion still src/index.ts MyVideo out/thumbnail.png --frame=0

# Preview in browser
npx remotion studio

# List available compositions
npx remotion compositions src/index.ts

# Ensure Chrome is installed
npx remotion browser ensure
```

### Complete CLI Flags
| Flag | Description | Example |
|------|-------------|---------|
| `--codec` | Output codec | `h264`, `h265`, `vp8`, `vp9`, `prores`, `gif` |
| `--crf` | Quality (0=best, 51=worst) | `--crf=18` |
| `--props` | JSON props or file path | `--props='{"title":"Hi"}'` |
| `--output` | Output path | `--output=out/video.mp4` |
| `--frames` | Frame range | `--frames=0-89` |
| `--concurrency` | Parallel threads | `--concurrency=4` |
| `--image-format` | Frame format | `jpeg` (fast) or `png` (transparency) |
| `--jpeg-quality` | JPEG quality 0-100 | `--jpeg-quality=80` |
| `--scale` | Output scale factor | `--scale=0.5` (half res preview) |
| `--muted` | No audio | `--muted` |
| `--log` | Log level | `error`, `warn`, `info`, `verbose` |
| `--timeout` | Frame timeout ms | `--timeout=60000` |
| `--height`/`--width` | Override dimensions | `--width=1920 --height=1080` |
| `--fps` | Override FPS | `--fps=60` |
| `--hardware-acceleration` | GPU rendering | `--hardware-acceleration` |

### Platform Render Presets
```bash
# TikTok / Reels / Shorts (vertical)
npx remotion render src/index.ts MyVideo out/tiktok.mp4 --codec=h264 --crf=18

# YouTube (horizontal HD)
npx remotion render src/index.ts MyVideo out/youtube.mp4 --codec=h264 --crf=15

# Twitter (square)
npx remotion render src/index.ts MyVideo out/twitter.mp4 --codec=h264 --crf=20

# Web embed (VP9, smaller)
npx remotion render src/index.ts MyVideo out/web.webm --codec=vp9 --crf=23

# GIF (short loop)
npx remotion render src/index.ts MyVideo out/loop.gif --codec=gif

# Preview (fast, half res)
npx remotion render src/index.ts MyVideo out/preview.mp4 --scale=0.5 --jpeg-quality=60
```

## Node.js API Rendering

### Full Pipeline
```tsx
import { bundle } from '@remotion/bundler';
import { renderMedia, selectComposition } from '@remotion/renderer';
import path from 'path';

async function render() {
  // Step 1: Bundle the project
  const bundleLocation = await bundle({
    entryPoint: path.resolve('./src/index.ts'),
    webpackOverride: (config) => config,
  });

  // Step 2: Select composition and resolve metadata
  const composition = await selectComposition({
    serveUrl: bundleLocation,
    id: 'MyVideo',
    inputProps: { title: 'Hello World' },
  });

  // Step 3: Render video
  await renderMedia({
    composition,
    serveUrl: bundleLocation,
    codec: 'h264',
    outputLocation: 'out/video.mp4',
    inputProps: { title: 'Hello World' },
    crf: 18,
    imageFormat: 'jpeg',
    jpegQuality: 80,
    onProgress: ({ progress }) => {
      console.log(`Rendering: ${(progress * 100).toFixed(1)}%`);
    },
  });

  console.log('Render complete!');
}

render();
```

### renderMedia() Full Options
| Option | Type | Description |
|--------|------|-------------|
| `composition` | object | From selectComposition() |
| `serveUrl` | string | Bundle location |
| `codec` | string | h264, h265, vp8, vp9, prores, gif |
| `outputLocation` | string | File path |
| `inputProps` | object | Props passed to composition |
| `crf` | number | Quality factor (0-51) |
| `imageFormat` | string | jpeg or png |
| `jpegQuality` | number | 0-100 |
| `videoBitrate` | string | e.g. '10M' |
| `audioBitrate` | string | e.g. '320k' |
| `frameRange` | [number, number] | Start and end frame |
| `concurrency` | number | Parallel render threads |
| `muted` | boolean | Strip audio |
| `onProgress` | function | Progress callback |

### renderStill() for Thumbnails
```tsx
import { renderStill } from '@remotion/renderer';

await renderStill({
  composition,
  serveUrl: bundleLocation,
  output: 'out/thumbnail.png',
  frame: 0,
  imageFormat: 'png',
});
```

## Multi-Format Output

### Render to multiple platforms from one source
```tsx
const platforms = [
  { id: 'TikTok', width: 1080, height: 1920, fps: 30 },
  { id: 'YouTube', width: 1920, height: 1080, fps: 30 },
  { id: 'Twitter', width: 1080, height: 1080, fps: 30 },
];

for (const platform of platforms) {
  const composition = await selectComposition({
    serveUrl: bundleLocation,
    id: platform.id,
    inputProps: sharedProps,
  });

  await renderMedia({
    composition,
    serveUrl: bundleLocation,
    codec: 'h264',
    outputLocation: `out/${platform.id.toLowerCase()}.mp4`,
  });
}
```

## Performance Optimization

| Optimization | How | Impact |
|-------------|-----|--------|
| Reduce concurrency | `--concurrency=2` | Less memory usage |
| Use JPEG frames | `--image-format=jpeg` | 2-3x faster |
| Lower quality preview | `--scale=0.5 --crf=28` | 4x faster |
| Skip audio | `--muted` | Faster encoding |
| Increase Node memory | `NODE_OPTIONS=--max-old-space-size=8192` | Prevents OOM |
| Enable multi-process | `enableMultiProcessOnLinux: true` | Linux only, faster |
| GPU acceleration | `--hardware-acceleration` | Faster encoding |

## Lambda Serverless Rendering

For high-volume rendering, use @remotion/lambda:
```bash
npm install @remotion/lambda
npx remotion lambda policies role
npx remotion lambda sites create src/index.ts
npx remotion lambda render SITE_URL MyVideo
```

Best for: batch rendering, API-driven video generation, scaling to thousands of videos.

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Out of memory | Reduce `--concurrency`, increase Node memory |
| Slow rendering | Use `--image-format=jpeg`, reduce concurrency |
| Audio out of sync | Ensure consistent FPS throughout, check audio sample rate |
| Missing fonts | Call `loadFont()` before component renders, ensure waitUntilDone |
| Black/blank frames | Check `delayRender`/`continueRender` pairs |
| Chrome not found | Run `npx remotion browser ensure` |
| Timeout errors | Increase `--timeout=120000`, check heavy computations |
| Codec not supported | Install FFmpeg, check Remotion version compatibility |