# Advanced Rendering Guide

Complete reference for Remotion rendering configuration, CI/CD, batch rendering, and deployment.

## remotion.config.ts Full Reference

```tsx
import { Config } from '@remotion/cli/config';

// Output settings
Config.setVideoImageFormat('jpeg');        // 'jpeg' (fast) or 'png' (transparency)
Config.setOverwriteOutput(true);           // Overwrite without prompt
Config.setCodec('h264');                   // Default codec
Config.setCrf(18);                         // Default quality
Config.setJpegQuality(80);                // JPEG frame quality

// Performance
Config.setConcurrency(4);                  // Parallel render threads
Config.setTimeoutInMilliseconds(60000);    // Frame render timeout

// Browser
Config.setChromiumDisableWebSecurity(true); // Allow cross-origin in dev
Config.setChromiumOpenGlRenderer('angle');  // GPU renderer: 'angle', 'egl', 'swiftshader'

// Audio
Config.setMuted(false);                    // Strip audio from output
Config.setAudioBitrate('320k');            // Audio quality

// Encoding
Config.setVideoBitrate('10M');             // Video bitrate cap
Config.setHardwareAcceleration('if-possible'); // GPU encoding: 'if-possible', 'required', 'disable'
```

### Config Options Table

| Method | Type | Default | Description |
|--------|------|---------|-------------|
| `setVideoImageFormat` | 'jpeg' \| 'png' | 'jpeg' | Frame image format |
| `setOverwriteOutput` | boolean | false | Overwrite existing output |
| `setCodec` | string | 'h264' | Output codec |
| `setCrf` | number | 18 | Constant rate factor (quality) |
| `setJpegQuality` | number | 80 | JPEG quality 0-100 |
| `setConcurrency` | number | 50% of CPUs | Parallel threads |
| `setTimeoutInMilliseconds` | number | 30000 | Frame timeout |
| `setMuted` | boolean | false | Strip audio |
| `setAudioBitrate` | string | '320k' | Audio bitrate |
| `setVideoBitrate` | string | null | Video bitrate cap |
| `setHardwareAcceleration` | string | 'if-possible' | GPU encoding |

## Docker Setup for CI/CD Rendering

### Dockerfile
```dockerfile
FROM node:22-bookworm-slim

# Install Chrome dependencies
RUN apt-get update && apt-get install -y \
  libnss3 \
  libdbus-1-3 \
  libatk1.0-0 \
  libgbm-dev \
  libasound2 \
  libxrandr2 \
  libxcomposite1 \
  libxdamage1 \
  libatk-bridge2.0-0 \
  libcups2 \
  libdrm2 \
  libpango-1.0-0 \
  libcairo2 \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN npm ci

# Ensure Chrome is available
RUN npx remotion browser ensure

# Copy source
COPY . .

# Default render command
CMD ["npx", "remotion", "render", "src/index.ts", "MyVideo", "out/video.mp4"]
```

### Docker Build & Run
```bash
# Build
docker build -t my-video-renderer .

# Render with default settings
docker run -v $(pwd)/out:/app/out my-video-renderer

# Render with custom composition and props
docker run -v $(pwd)/out:/app/out my-video-renderer \
  npx remotion render src/index.ts CustomComp out/custom.mp4 \
  --props='{"title":"Custom Title"}'
```

### Docker Compose (with output volume)
```yaml
version: '3.8'
services:
  renderer:
    build: .
    volumes:
      - ./out:/app/out
    environment:
      - NODE_OPTIONS=--max-old-space-size=8192
    command: npx remotion render src/index.ts MyVideo out/video.mp4 --codec=h264 --crf=18
```

## GitHub Actions Workflow

### Automatic Rendering on Push
```yaml
# .github/workflows/render.yml
name: Render Video

on:
  push:
    branches: [main]
    paths:
      - 'src/**'
      - 'public/**'

jobs:
  render:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-node@v4
        with:
          node-version: 22
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Install Chrome
        run: npx remotion browser ensure

      - name: Render video
        run: npx remotion render src/index.ts MyVideo out/video.mp4 --codec=h264 --crf=18

      - name: Upload artifact
        uses: actions/upload-artifact@v4
        with:
          name: rendered-video
          path: out/video.mp4
          retention-days: 30
```

### Render on PR (preview quality)
```yaml
name: Render Preview

on:
  pull_request:
    paths: ['src/**']

jobs:
  preview:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 22
          cache: 'npm'
      - run: npm ci
      - run: npx remotion browser ensure
      - name: Render preview
        run: npx remotion render src/index.ts MyVideo out/preview.mp4 --scale=0.5 --crf=28
      - uses: actions/upload-artifact@v4
        with:
          name: preview-video
          path: out/preview.mp4
```

## Batch Rendering Script

### Render all compositions
```bash
#!/bin/bash
# scripts/render-all.sh

SRC="src/index.ts"
OUT_DIR="out"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

mkdir -p "$OUT_DIR"

# Get all composition IDs
COMPOSITIONS=$(npx remotion compositions "$SRC" --quiet)

echo "Found compositions: $COMPOSITIONS"

for COMP in $COMPOSITIONS; do
  echo "Rendering: $COMP"
  npx remotion render "$SRC" "$COMP" "$OUT_DIR/${COMP}_${TIMESTAMP}.mp4" \
    --codec=h264 --crf=18
  echo "Done: $COMP"
done

echo "All compositions rendered to $OUT_DIR/"
```

### Render with different props
```bash
#!/bin/bash
# scripts/render-batch.sh

SRC="src/index.ts"
COMP="MyVideo"

# Array of prop sets
declare -a PROPS=(
  '{"title":"Episode 1","color":"#FF6B35"}'
  '{"title":"Episode 2","color":"#004E89"}'
  '{"title":"Episode 3","color":"#7B2D8E"}'
)

for i in "${!PROPS[@]}"; do
  echo "Rendering variant $((i+1))..."
  npx remotion render "$SRC" "$COMP" "out/video_$((i+1)).mp4" \
    --props="${PROPS[$i]}" --codec=h264 --crf=18
done

echo "Batch render complete!"
```

## Output Naming Patterns

```bash
# Date-stamped
out/video_$(date +%Y%m%d_%H%M%S).mp4

# Platform-based
out/${PLATFORM}_${COMP}_$(date +%Y%m%d).mp4

# ID-based (for API-driven rendering)
out/${VIDEO_ID}_${VARIANT}.mp4

# Version-based
out/${COMP}_v${VERSION}.mp4
```

## S3 Upload After Render

```bash
#!/bin/bash
# scripts/render-and-upload.sh

VIDEO_FILE="out/video.mp4"
S3_BUCKET="my-videos-bucket"
S3_KEY="renders/$(date +%Y/%m/%d)/video_$(date +%H%M%S).mp4"

# Render
npx remotion render src/index.ts MyVideo "$VIDEO_FILE" --codec=h264 --crf=18

# Upload to S3
aws s3 cp "$VIDEO_FILE" "s3://${S3_BUCKET}/${S3_KEY}" \
  --content-type "video/mp4" \
  --metadata "composition=MyVideo,rendered=$(date -u +%Y-%m-%dT%H:%M:%SZ)"

echo "Uploaded to s3://${S3_BUCKET}/${S3_KEY}"
```

### Node.js S3 Upload
```tsx
import { S3Client, PutObjectCommand } from '@aws-sdk/client-s3';
import { readFileSync } from 'fs';

const s3 = new S3Client({ region: 'us-east-1' });

async function uploadToS3(filePath: string, key: string) {
  await s3.send(new PutObjectCommand({
    Bucket: 'my-videos-bucket',
    Key: key,
    Body: readFileSync(filePath),
    ContentType: 'video/mp4',
  }));
  return `https://my-videos-bucket.s3.amazonaws.com/${key}`;
}
```

## Webhook Notification Pattern

```tsx
import { renderMedia } from '@remotion/renderer';

async function renderAndNotify() {
  const startTime = Date.now();

  try {
    await renderMedia({
      composition,
      serveUrl: bundleLocation,
      codec: 'h264',
      outputLocation: 'out/video.mp4',
      onProgress: ({ progress }) => {
        // Optional: send progress webhooks
        if (Math.floor(progress * 100) % 25 === 0) {
          fetch(WEBHOOK_URL, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              event: 'render.progress',
              progress: Math.floor(progress * 100),
            }),
          });
        }
      },
    });

    // Success webhook
    await fetch(WEBHOOK_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        event: 'render.complete',
        duration: Date.now() - startTime,
        outputUrl: 'https://cdn.example.com/video.mp4',
      }),
    });
  } catch (error) {
    // Failure webhook
    await fetch(WEBHOOK_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        event: 'render.failed',
        error: error.message,
      }),
    });
  }
}
```

## Custom Webpack Override Examples

### Path Aliases
```tsx
// remotion.config.ts
import { Config } from '@remotion/cli/config';
import path from 'path';

Config.overrideWebpackConfig((config) => ({
  ...config,
  resolve: {
    ...config.resolve,
    alias: {
      ...config.resolve?.alias,
      '@components': path.resolve('./src/components'),
      '@assets': path.resolve('./public/assets'),
      '@utils': path.resolve('./src/utils'),
    },
  },
}));
```

### Custom Loaders (SVG, YAML)
```tsx
Config.overrideWebpackConfig((config) => ({
  ...config,
  module: {
    ...config.module,
    rules: [
      ...(config.module?.rules ?? []),
      {
        test: /\.svg$/,
        use: ['@svgr/webpack'],
      },
      {
        test: /\.yaml$/,
        use: ['yaml-loader'],
      },
    ],
  },
}));
```

### Enable TailwindCSS
```tsx
// remotion.config.ts
import { Config } from '@remotion/cli/config';
import { enableTailwind } from '@remotion/tailwind';

Config.overrideWebpackConfig((config) => enableTailwind(config));
```

## Rspack Bundler Setup (Faster Builds)

Rspack is significantly faster than Webpack for bundling:

```bash
npm install @remotion/bundler-rspack
```

```tsx
// render.mjs (Node.js API)
import { bundle } from '@remotion/bundler-rspack';

const bundleLocation = await bundle({
  entryPoint: './src/index.ts',
});
```

For CLI usage, Rspack is used automatically when `@remotion/bundler-rspack` is installed and configured.

### Rspack vs Webpack Performance

| Metric | Webpack | Rspack |
|--------|---------|--------|
| Cold bundle | ~8-15s | ~2-4s |
| Hot rebuild | ~2-5s | ~0.5-1s |
| Memory usage | Higher | Lower |

## Environment Variables in Rendering

```bash
# Pass env vars to render
TITLE="Hello" COLOR="#FF6B35" npx remotion render src/index.ts MyVideo out/video.mp4

# Access in component
const title = process.env.TITLE ?? 'Default Title';
```

Or use `--props` for structured data:
```bash
npx remotion render src/index.ts MyVideo out/video.mp4 \
  --props='{"title":"Hello","color":"#FF6B35","items":["a","b","c"]}'
```
