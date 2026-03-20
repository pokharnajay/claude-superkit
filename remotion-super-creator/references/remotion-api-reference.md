# Remotion API Reference — Complete Cheatsheet

> Every package, every API, with imports and code snippets.
> Use this as the single source of truth when generating Remotion code.

---

## 1. Core (`remotion`)

### useCurrentFrame
```tsx
import { useCurrentFrame } from 'remotion';

const MyComp: React.FC = () => {
  const frame = useCurrentFrame(); // 0-indexed, increments each frame
  return <div style={{ opacity: frame / 30 }}>Hello</div>;
};
```

### useVideoConfig
```tsx
import { useVideoConfig } from 'remotion';

const MyComp: React.FC = () => {
  const { fps, durationInFrames, width, height } = useVideoConfig();
  return <div>Video is {durationInFrames / fps}s long</div>;
};
```

### interpolate
```tsx
import { interpolate, Easing } from 'remotion';

// Basic: map frame 0-30 to opacity 0-1
const opacity = interpolate(frame, [0, 30], [0, 1]);

// With easing
const scale = interpolate(frame, [0, 30], [0.5, 1], {
  easing: Easing.out(Easing.ease),
});

// Clamped (default: extrapolateLeft='extend', extrapolateRight='extend')
const x = interpolate(frame, [0, 30], [0, 100], {
  extrapolateLeft: 'clamp',
  extrapolateRight: 'clamp',
});

// Multiple ranges (keyframes)
const y = interpolate(frame, [0, 15, 30], [0, -50, 0], {
  extrapolateLeft: 'clamp',
  extrapolateRight: 'clamp',
});
```

### spring
```tsx
import { spring, useCurrentFrame, useVideoConfig } from 'remotion';

const frame = useCurrentFrame();
const { fps } = useVideoConfig();

const value = spring({
  frame,
  fps,
  config: {
    damping: 200,    // resistance (higher = less oscillation)
    stiffness: 100,  // spring tightness (higher = faster)
    mass: 1,         // weight (higher = slower)
    overshootClamping: false, // clamp at target value
  },
  from: 0,           // start value (default 0)
  to: 1,             // end value (default 1)
  durationInFrames: 30, // optional: auto-calculate rest
  durationRestThreshold: 0.001, // when to consider "at rest"
  delay: 10,         // delay in frames before starting
  reverse: false,    // play in reverse
});
```

### Easing
```tsx
import { Easing } from 'remotion';

// Base curves
Easing.linear    // t => t
Easing.ease      // CSS ease equivalent
Easing.quad      // t => t*t
Easing.cubic     // t => t*t*t
Easing.poly(n)   // t => t^n
Easing.sin       // sine curve
Easing.circle    // circular curve
Easing.exp       // exponential curve
Easing.elastic(bounciness?) // elastic bounce (default 1)
Easing.back(overshoot?)     // overshoot and return (default 1.70158)
Easing.bounce    // bouncing ball
Easing.bezier(x1, y1, x2, y2) // custom cubic bezier
Easing.step0     // jump at start
Easing.step1     // jump at end

// Modifiers — wrap any base curve
Easing.in(Easing.quad)      // accelerate
Easing.out(Easing.quad)     // decelerate
Easing.inOut(Easing.quad)   // accelerate then decelerate
```

### AbsoluteFill
```tsx
import { AbsoluteFill } from 'remotion';

// position:absolute, top/right/bottom/left:0, width/height:100%
<AbsoluteFill style={{ backgroundColor: '#000', justifyContent: 'center', alignItems: 'center' }}>
  <h1>Centered</h1>
</AbsoluteFill>
```

### Sequence
```tsx
import { Sequence } from 'remotion';

// Offsets child's frame counter. Child sees frame=0 at parent frame=30.
<Sequence from={30} durationInFrames={60} name="Scene 2" layout="none">
  <MyScene />
</Sequence>

// layout="none" prevents wrapping in an AbsoluteFill
// name is optional, shows in Remotion Studio timeline
```

### Series
```tsx
import { Series } from 'remotion';

// Sequential scenes, each starts after the previous ends
<Series>
  <Series.Sequence durationInFrames={60}><Scene1 /></Series.Sequence>
  <Series.Sequence durationInFrames={90} offset={-10}><Scene2 /></Series.Sequence>
  <Series.Sequence durationInFrames={60}><Scene3 /></Series.Sequence>
</Series>
// offset={-10} means Scene2 starts 10 frames BEFORE Scene1 ends (overlap)
// offset={10} means 10 frame gap between scenes
```

### Composition & Still
```tsx
import { Composition, Still } from 'remotion';

// In Root.tsx
export const RemotionRoot: React.FC = () => (
  <>
    <Composition
      id="MyVideo"
      component={MyVideo}
      durationInFrames={300}
      fps={30}
      width={1080}
      height={1920}
      defaultProps={{ title: 'Hello' }}
      schema={myZodSchema} // optional: Zod schema for props
      calculateMetadata={async ({ props }) => ({ // optional: dynamic metadata
        durationInFrames: props.items.length * 30,
      })}
    />
    <Still
      id="Thumbnail"
      component={Thumbnail}
      width={1280}
      height={720}
      defaultProps={{ title: 'Thumb' }}
    />
  </>
);
```

### registerRoot
```tsx
import { registerRoot } from 'remotion';
import { RemotionRoot } from './Root';

registerRoot(RemotionRoot);
// Called in src/index.ts — entry point for Remotion
```

### staticFile
```tsx
import { staticFile } from 'remotion';

// References files in the /public folder
const src = staticFile('logo.png');     // → /public/logo.png
const audio = staticFile('music.mp3');  // → /public/music.mp3

// Use with Remotion components
import { Img, Audio, Video } from 'remotion';
<Img src={staticFile('photo.jpg')} />
<Audio src={staticFile('bgm.mp3')} volume={0.5} />
<Video src={staticFile('clip.mp4')} />
```

### delayRender / continueRender / cancelRender
```tsx
import { delayRender, continueRender, cancelRender } from 'remotion';

const MyComp: React.FC = () => {
  const [data, setData] = useState(null);
  const [handle] = useState(() => delayRender('Loading data'));

  useEffect(() => {
    fetch('https://api.example.com/data')
      .then(res => res.json())
      .then(d => { setData(d); continueRender(handle); })
      .catch(err => cancelRender(err));
  }, [handle]);

  if (!data) return null;
  return <div>{data.title}</div>;
};
```

### random
```tsx
import { random } from 'remotion';

// Deterministic random (same seed → same value), 0 to 1
const r = random('my-seed');       // always the same
const r2 = random(`item-${i}`);   // per-item deterministic random
const r3 = random(null);          // truly random (non-deterministic)
```

### Img, Audio, Video, OffthreadVideo, IFrame
```tsx
import { Img, Audio, Video, OffthreadVideo, IFrame } from 'remotion';

// ALWAYS use these instead of native HTML tags
<Img src={staticFile('photo.jpg')} style={{ width: '100%' }} />

<Audio src={staticFile('bgm.mp3')} volume={0.5} startFrom={30} endAt={150} />
<Audio src={staticFile('sfx.wav')} volume={(f) => interpolate(f, [0, 10], [0, 1])} />

<Video src={staticFile('clip.mp4')} volume={0} startFrom={0} endAt={90} playbackRate={1.5} />

// OffthreadVideo: renders video frames without <video> element — better for rendering
<OffthreadVideo src={staticFile('clip.mp4')} volume={0} transparent={false} />

<IFrame src="https://example.com" width={1920} height={1080} />
```

### Loop
```tsx
import { Loop } from 'remotion';

<Loop durationInFrames={60} times={3} layout="none">
  <PulseAnimation />
</Loop>
// Loops child 3 times, each iteration 60 frames
// times is optional (defaults to infinite)
```

### Freeze
```tsx
import { Freeze } from 'remotion';

<Freeze frame={15}>
  <MyAnimation />
</Freeze>
// Freezes child at frame 15
```

---

## 2. Animation Utils (`@remotion/animation-utils`)

### makeTransform
```tsx
import { makeTransform, scale, translate, rotate, skew } from '@remotion/animation-utils';

const transform = makeTransform([
  scale(1.2),
  translate(50, 100),       // translateX, translateY
  rotate(45),               // degrees
]);
// → "scale(1.2) translate(50px, 100px) rotate(45deg)"

// Individual transforms
translateX(100)   // "translateX(100px)"
translateY(-50)   // "translateY(-50px)"
scaleX(1.5)       // "scaleX(1.5)"
scaleY(0.8)       // "scaleY(0.8)"
rotateX(45)       // "rotateX(45deg)"
rotateY(90)       // "rotateY(90deg)"
rotateZ(30)       // "rotateZ(30deg)"
skewX(10)         // "skewX(10deg)"
skewY(5)          // "skewY(5deg)"
matrix(a,b,c,d,tx,ty) // CSS matrix()
```

### interpolateStyles
```tsx
import { interpolateStyles } from '@remotion/animation-utils';

const style = interpolateStyles(
  frame,
  [0, 30],                    // input range
  [                            // output range (CSS style objects)
    { opacity: 0, transform: 'translateY(50px)' },
    { opacity: 1, transform: 'translateY(0px)' },
  ]
);
// Returns interpolated CSS style object
```

---

## 3. Transitions (`@remotion/transitions`)

### TransitionSeries
```tsx
import { TransitionSeries, linearTiming, springTiming } from '@remotion/transitions';
import { fade } from '@remotion/transitions/fade';
import { slide } from '@remotion/transitions/slide';

<TransitionSeries>
  <TransitionSeries.Sequence durationInFrames={90}>
    <Scene1 />
  </TransitionSeries.Sequence>
  <TransitionSeries.Transition
    presentation={fade()}
    timing={linearTiming({ durationInFrames: 15 })}
  />
  <TransitionSeries.Sequence durationInFrames={90}>
    <Scene2 />
  </TransitionSeries.Sequence>
  <TransitionSeries.Transition
    presentation={slide({ direction: 'from-left' })}
    timing={springTiming({ config: { damping: 200 }, durationInFrames: 20 })}
  />
  <TransitionSeries.Sequence durationInFrames={90}>
    <Scene3 />
  </TransitionSeries.Sequence>
</TransitionSeries>
```

### Presentations
```tsx
import { fade } from '@remotion/transitions/fade';
import { slide } from '@remotion/transitions/slide';
import { wipe } from '@remotion/transitions/wipe';
import { flip } from '@remotion/transitions/flip';
import { clockWipe } from '@remotion/transitions/clock-wipe';
import { cube3d } from '@remotion/transitions/cube-3d';

fade()                                    // opacity crossfade
slide({ direction: 'from-left' })         // from-left|from-right|from-top|from-bottom
wipe({ direction: 'from-left' })          // from-left|from-right|from-top|from-bottom
flip({ direction: 'from-left' })          // from-left|from-right|from-top|from-bottom
clockWipe({ width: 1080, height: 1920 })  // circular clock wipe
cube3d({ direction: 'from-left', perspective: 1000 }) // 3D cube rotation
```

---

## 4. Noise (`@remotion/noise`)

```tsx
import { noise2D, noise3D, noise4D } from '@remotion/noise';

// Perlin noise — returns -1 to 1
const val2d = noise2D('my-seed', x * 0.01, y * 0.01);
const val3d = noise3D('my-seed', x * 0.01, y * 0.01, frame * 0.02);
const val4d = noise4D('my-seed', x, y, z, frame * 0.02);

// Animated noise field example
const noiseValue = noise2D('seed', frame * 0.05, 0);
const offset = interpolate(noiseValue, [-1, 1], [-20, 20]);
```

---

## 5. Paths (`@remotion/paths`)

```tsx
import {
  getLength, getPointAtLength, getSubpaths,
  evolvePath, parsePath, interpolatePath,
  scalePath, translatePath, reversePath,
  normalizePath, resetPath, getBoundingBox,
  getInstructionIndexAtLength,
} from '@remotion/paths';

const d = 'M 0 0 L 100 100 L 200 0';

getLength(d);                      // total length of SVG path
getPointAtLength(d, 50);           // { x, y } at length 50
getSubpaths(d);                    // array of sub-path strings
evolvePath(progress, d);           // { strokeDasharray, strokeDashoffset } for path drawing
parsePath(d);                      // parsed instruction array
interpolatePath(progress, d1, d2); // morph between two paths
scalePath(d, 2, 2);               // scale path by x, y
translatePath(d, 50, 100);        // translate path by x, y
reversePath(d);                    // reverse direction
normalizePath(d);                  // normalize to cubic beziers
resetPath(d);                      // move path origin to 0,0
getBoundingBox(d);                 // { x1, y1, x2, y2, width, height }
getInstructionIndexAtLength(d, 50); // which instruction at length

// Path drawing animation
const { strokeDasharray, strokeDashoffset } = evolvePath(progress, d);
<path d={d} strokeDasharray={strokeDasharray} strokeDashoffset={strokeDashoffset}
  stroke="white" strokeWidth={3} fill="none" />
```

---

## 6. Shapes (`@remotion/shapes`)

```tsx
import { Rect, Circle, Triangle, Star, Polygon, Ellipse } from '@remotion/shapes';
import { makeRect, makeCircle, makeTriangle, makeStar, makePolygon, makeEllipse } from '@remotion/shapes';

// React components
<Rect width={200} height={100} fill="blue" cornerRadius={10} edgeRoundness={0.5} />
<Circle radius={50} fill="red" />
<Triangle length={100} direction="up" fill="green" cornerRadius={5} edgeRoundness={0.5} />
// direction: "up" | "down" | "left" | "right"
<Star innerRadius={30} outerRadius={60} points={5} fill="gold" cornerRadius={3} edgeRoundness={0} />
<Polygon radius={50} points={6} fill="purple" cornerRadius={5} />
<Ellipse rx={80} ry={50} fill="orange" />

// Path generators — return { path, width, height, instructions, transformOrigin }
const rect = makeRect({ width: 200, height: 100, cornerRadius: 10, edgeRoundness: 0.5 });
const circle = makeCircle({ radius: 50 });
const triangle = makeTriangle({ length: 100, direction: 'up', cornerRadius: 5 });
const star = makeStar({ innerRadius: 30, outerRadius: 60, points: 5, cornerRadius: 3 });
const polygon = makePolygon({ radius: 50, points: 6, cornerRadius: 5 });
const ellipse = makeEllipse({ rx: 80, ry: 50 });

// Use path with SVG
<svg viewBox={`0 0 ${rect.width} ${rect.height}`}>
  <path d={rect.path} fill="blue" />
</svg>
```

---

## 7. Motion Blur (`@remotion/motion-blur`)

```tsx
import { Trail } from '@remotion/motion-blur';

<Trail layers={8} lagInFrames={0.3}>
  <MovingElement />
</Trail>
// layers: number of ghost copies (more = smoother blur, heavier render)
// lagInFrames: how far back each layer looks (higher = more blur)
```

---

## 8. Light Leaks (`@remotion/light-leaks`)

```tsx
import { LightLeak } from '@remotion/light-leaks';

<LightLeak seed={42} hueShift={0} />
// seed: deterministic random (number)
// hueShift: rotate hue 0-360
// Renders as overlay — use with mix-blend-mode or as transition
```

---

## 9. Google Fonts (`@remotion/google-fonts`)

```tsx
import { loadFont } from '@remotion/google-fonts/Inter';

const { fontFamily, waitUntilDone } = loadFont();
// OR load specific variants
const { fontFamily } = loadFont('normal', {
  weights: ['400', '700'],
  subsets: ['latin'],
});

// Use in components
<div style={{ fontFamily }}>Text in Inter</div>

// Wait for font before rendering
const [handle] = useState(() => delayRender());
useEffect(() => {
  waitUntilDone().then(() => continueRender(handle));
}, [handle]);
```

---

## 10. Layout Utils (`@remotion/layout-utils`)

```tsx
import { fitText, measureText, fillTextBox } from '@remotion/layout-utils';

// fitText: calculate fontSize to fit within maxWidth
const { fontSize } = fitText({
  text: 'Hello World',
  withinWidth: 800,
  fontFamily: 'Inter',
  fontWeight: '700',
  maxLines: 1,        // optional: wrap to multiple lines
});

// measureText: get dimensions of text
const { width, height } = measureText({
  text: 'Hello',
  fontFamily: 'Inter',
  fontSize: 48,
  fontWeight: '400',
  letterSpacing: undefined,
  validateFontIsLoaded: true,
});

// fillTextBox: break text into lines that fit within a box
const { lines } = fillTextBox({
  maxWidth: 500,
  maxLines: 3,
  maxBoxHeight: 200,
  fontSize: 24,
  fontFamily: 'Inter',
  fontWeight: '400',
  text: 'A long paragraph that will be broken into lines...',
});
```

---

## 11. Media Utils (`@remotion/media-utils`)

```tsx
import { getAudioData, visualizeAudio, getVideoMetadata } from '@remotion/media-utils';

// Audio visualization
const audioData = await getAudioData(staticFile('music.mp3'));
// Use inside component:
const frame = useCurrentFrame();
const { fps } = useVideoConfig();
const visualization = visualizeAudio({
  fps,
  frame,
  audioData,
  numberOfSamples: 256,  // FFT size (power of 2)
  smoothing: true,        // temporal smoothing
  optimizeFor: 'accuracy', // 'accuracy' | 'speed'
});
// visualization is number[] of frequency amplitudes 0-1

// Video metadata
const metadata = await getVideoMetadata(staticFile('clip.mp4'));
// { width, height, durationInSeconds, fps, codec, ... }
```

---

## 12. Captions (`@remotion/captions`)

```tsx
import { createTikTokStyleCaptions, parseSrt } from '@remotion/captions';
import type { Caption } from '@remotion/captions';

// Parse SRT file
const captions: Caption[] = parseSrt({ input: srtString });

// Create TikTok-style word-by-word captions
const { pages } = createTikTokStyleCaptions({
  captions,
  combineTokensWithinMilliseconds: 800,
});
// Each page: { text, startMs, tokens: [{ text, fromMs, toMs }] }
```

---

## 13. GIF (`@remotion/gif`)

```tsx
import { Gif } from '@remotion/gif';

<Gif
  src={staticFile('animation.gif')}
  width={300}
  height={300}
  fit="contain"          // 'contain' | 'cover' | 'fill'
  playbackRate={1}       // speed multiplier
  loopBehavior="loop"    // 'loop' | 'pause-after-finish'
/>
```

---

## 14. Lottie (`@remotion/lottie`)

```tsx
import { Lottie } from '@remotion/lottie';
import animationData from './animation.json';

<Lottie
  animationData={animationData}
  playbackRate={1}
  direction="forward"    // 'forward' | 'backward'
  loop={false}
  style={{ width: 300, height: 300 }}
/>
```

---

## 15. Animated Emoji (`@remotion/animated-emoji`)

```tsx
import { AnimatedEmoji } from '@remotion/animated-emoji';

<AnimatedEmoji emoji="fire" />
<AnimatedEmoji emoji="heart" />
<AnimatedEmoji emoji="rocket" />
// Uses Google's Animated Emoji — vector-based
```

---

## 16. Three.js (`@remotion/three`)

```tsx
import { ThreeCanvas } from '@remotion/three';
import { useCurrentFrame, useVideoConfig } from 'remotion';

// IMPORTANT: use useCurrentFrame from 'remotion', NOT useFrame from @react-three/fiber
const MyScene: React.FC = () => {
  const frame = useCurrentFrame();
  const { width, height } = useVideoConfig();

  return (
    <ThreeCanvas
      width={width}
      height={height}
      camera={{ position: [0, 0, 5], fov: 75 }}
      orthographic={false}
    >
      <ambientLight intensity={0.5} />
      <mesh rotation={[0, frame * 0.05, 0]}>
        <boxGeometry args={[1, 1, 1]} />
        <meshStandardMaterial color="orange" />
      </mesh>
    </ThreeCanvas>
  );
};
```

---

## 17. Preload (`@remotion/preload`)

```tsx
import { preloadAudio, preloadVideo, preloadImage, preloadFont } from '@remotion/preload';

// Call outside components (top-level) — returns cleanup function
const cleanup = preloadAudio(staticFile('bgm.mp3'));
const cleanup2 = preloadVideo('https://example.com/clip.mp4');
const cleanup3 = preloadImage(staticFile('photo.jpg'));
const cleanup4 = preloadFont(staticFile('CustomFont.woff2'));
```

---

## 18. Tailwind (`@remotion/tailwind`)

```tsx
// In tailwind.config.ts for Remotion:
import type { Config } from 'tailwindcss';
export default {
  content: ['./src/**/*.{ts,tsx}'],
} satisfies Config;

// CRITICAL: NEVER use transition-*, animate-*, or any CSS animation classes
// ALL animation MUST be done via useCurrentFrame() + interpolate/spring
// Tailwind is for LAYOUT and STYLING only

// Usage in components:
<div className="flex items-center justify-center bg-slate-900 text-white text-4xl font-bold">
  Hello
</div>
```

---

## 19. Zod Types (`@remotion/zod-types`)

```tsx
import { zColor } from '@remotion/zod-types';
import { z } from 'zod';

const schema = z.object({
  title: z.string(),
  backgroundColor: zColor(), // shows color picker in Remotion Studio
  fontSize: z.number().min(10).max(200),
});
```

---

## 20. CLI (`@remotion/cli`)

```bash
# Start Remotion Studio
npx remotion studio

# Render video
npx remotion render src/index.ts MyVideo out/video.mp4 \
  --props='{"title":"Hello"}' --codec=h264

# Render still image
npx remotion still src/index.ts Thumbnail out/thumb.png

# List compositions
npx remotion compositions src/index.ts
```

---

## 21. Renderer (`@remotion/renderer`)

```tsx
import { bundle } from '@remotion/bundler';
import { renderMedia, renderStill, selectComposition, renderFrames, stitchFramesToVideo } from '@remotion/renderer';

// Bundle project
const bundled = await bundle({ entryPoint: './src/index.ts' });

// Select composition
const composition = await selectComposition({
  serveUrl: bundled,
  id: 'MyVideo',
  inputProps: { title: 'Hello' },
});

// Render full video
await renderMedia({
  composition,
  serveUrl: bundled,
  codec: 'h264',
  outputLocation: 'out/video.mp4',
  inputProps: { title: 'Hello' },
  imageFormat: 'jpeg',        // 'jpeg' | 'png' | 'webp'
  jpegQuality: 80,
  audioBitrate: '128k',
  videoBitrate: '5M',
  crf: 18,                    // constant rate factor (lower = better quality)
  everyNthFrame: 1,
  numberOfGifLoops: null,
  onProgress: ({ progress }) => console.log(`${(progress * 100).toFixed(0)}%`),
});

// Render still
await renderStill({
  composition,
  serveUrl: bundled,
  output: 'out/thumb.png',
  frame: 30,
  imageFormat: 'png',
});
```

---

## 22. Install Whisper (`@remotion/install-whisper-cpp`)

```tsx
import { installWhisperCpp, transcribe, convertToCaptions } from '@remotion/install-whisper-cpp';

// Install whisper.cpp binary
await installWhisperCpp({ to: '.whisper', model: 'medium' });

// Transcribe audio
const { transcription } = await transcribe({
  inputPath: 'audio.wav',
  whisperPath: '.whisper',
  model: 'medium',
  tokenLevelTimestamps: true,
});

// Convert to Remotion captions
const { captions } = convertToCaptions({ transcription });
```

---

## Common Patterns

### Scene Component Template
```tsx
import { AbsoluteFill, useCurrentFrame, useVideoConfig, interpolate, spring } from 'remotion';

export const Scene: React.FC<{ title: string }> = ({ title }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const titleOpacity = interpolate(frame, [0, 20], [0, 1], { extrapolateRight: 'clamp' });
  const titleY = spring({ frame, fps, config: { damping: 200 } }) * -50 + 50;

  return (
    <AbsoluteFill style={{ backgroundColor: '#0f0f0f', justifyContent: 'center', alignItems: 'center' }}>
      <h1 style={{
        color: '#fff',
        fontSize: 72,
        fontWeight: 700,
        opacity: titleOpacity,
        transform: `translateY(${titleY}px)`,
      }}>
        {title}
      </h1>
    </AbsoluteFill>
  );
};
```

### Stagger Animation Pattern
```tsx
const items = ['One', 'Two', 'Three'];
const staggerDelay = 8; // frames between each item

{items.map((item, i) => {
  const delay = i * staggerDelay;
  const itemOpacity = interpolate(frame, [delay, delay + 15], [0, 1], {
    extrapolateLeft: 'clamp', extrapolateRight: 'clamp',
  });
  const itemX = interpolate(frame, [delay, delay + 15], [-30, 0], {
    extrapolateLeft: 'clamp', extrapolateRight: 'clamp',
    easing: Easing.out(Easing.ease),
  });
  return (
    <div key={i} style={{ opacity: itemOpacity, transform: `translateX(${itemX}px)` }}>
      {item}
    </div>
  );
})}
```

### Audio Visualization Pattern
```tsx
import { useCurrentFrame, useVideoConfig, staticFile } from 'remotion';
import { getAudioData, visualizeAudio } from '@remotion/media-utils';
import { useEffect, useState } from 'react';

const AudioViz: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const [audioData, setAudioData] = useState(null);
  const [handle] = useState(() => delayRender());

  useEffect(() => {
    getAudioData(staticFile('music.mp3'))
      .then(d => { setAudioData(d); continueRender(handle); });
  }, [handle]);

  if (!audioData) return null;
  const viz = visualizeAudio({ fps, frame, audioData, numberOfSamples: 64 });
  return (
    <div style={{ display: 'flex', gap: 4, alignItems: 'flex-end', height: 200 }}>
      {viz.map((v, i) => (
        <div key={i} style={{ width: 8, height: v * 200, backgroundColor: '#fff', borderRadius: 4 }} />
      ))}
    </div>
  );
};
```

### Dynamic Duration via calculateMetadata
```tsx
<Composition
  id="DynamicVideo"
  component={DynamicVideo}
  width={1080}
  height={1920}
  fps={30}
  durationInFrames={300} // fallback
  schema={z.object({ items: z.array(z.string()) })}
  defaultProps={{ items: ['a', 'b', 'c'] }}
  calculateMetadata={async ({ props }) => ({
    durationInFrames: props.items.length * 90 + 60, // 90 frames per item + 60 outro
  })}
/>
```

### Font Loading Pattern
```tsx
import { loadFont } from '@remotion/google-fonts/Poppins';
import { delayRender, continueRender } from 'remotion';

const { fontFamily, waitUntilDone } = loadFont('normal', {
  weights: ['400', '600', '700'],
  subsets: ['latin'],
});

export const MyComp: React.FC = () => {
  const [handle] = useState(() => delayRender('Loading font'));
  useEffect(() => { waitUntilDone().then(() => continueRender(handle)); }, [handle]);

  return <div style={{ fontFamily, fontWeight: 700 }}>Loaded!</div>;
};
```
