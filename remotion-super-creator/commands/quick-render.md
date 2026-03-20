---
description: "Render the current Remotion project. Usage: /quick-render [composition-id] [format]"
disable-model-invocation: true
---

Invoke the `remotion-video-creator:render-engine` skill. If no composition ID given, list available compositions with `npx remotion compositions src/index.ts`. Default render: `npx remotion render src/index.ts [CompositionId] out/video.mp4 --codec=h264 --crf=18`. Formats: `social` (H.264 CRF 18), `youtube` (H.264 CRF 15), `web` (VP9 CRF 23), `gif`, `preview` (half-res CRF 28).