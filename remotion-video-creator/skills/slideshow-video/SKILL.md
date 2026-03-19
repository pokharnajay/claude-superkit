---
name: slideshow-video
description: Create photo montages, image slideshows, portfolio showcases, and presentation videos. Use when user wants to turn images into an animated video with transitions.
---

# Slideshow Video

Transform static images into cinematic video with Ken Burns effects, transitions, and text overlays.

## When to Use

- User wants to turn photos into a video
- User asks for a slideshow, montage, or photo reel
- User wants a portfolio showcase, real estate tour, or product gallery
- User mentions Ken Burns, image transitions, or photo animation
- User wants to convert a presentation or deck into video

## Common Formats

- Photo slideshow (travel, wedding, event recap)
- Portfolio showcase (design, photography, architecture)
- Real estate tour (property photos with room labels)
- Product gallery (e-commerce showcase, catalog video)
- Presentation slides (deck-to-video conversion)
- Memorial/tribute video (photos + music + captions)
- Year-in-review (photo highlights with dates)

## Image Handling Rules

**Always** use Remotion's `<Img>` component, never native `<img>`:

```tsx
import { Img, staticFile } from "remotion";

// For images in public/ folder
<Img src={staticFile("photos/beach.jpg")} style={{ width: "100%", height: "100%", objectFit: "cover" }} />

// For remote URLs
<Img src="https://example.com/photo.jpg" style={{ width: "100%", height: "100%", objectFit: "cover" }} />
```

**Why:** `<Img>` waits for the image to load before rendering the frame, preventing blank frames during render.

## Ken Burns Effect

The signature slideshow animation: slow zoom + pan on static images creates the illusion of camera motion.

```tsx
const KenBurnsImage: React.FC<{
  src: string;
  zoomDirection?: "in" | "out";
  panX?: number;
  panY?: number;
}> = ({ src, zoomDirection = "in", panX = -30, panY = -20 }) => {
  const frame = useCurrentFrame();
  const { durationInFrames } = useVideoConfig();

  const startScale = zoomDirection === "in" ? 1 : 1.15;
  const endScale = zoomDirection === "in" ? 1.15 : 1;

  const scale = interpolate(frame, [0, durationInFrames], [startScale, endScale], {
    extrapolateRight: "clamp",
  });
  const translateX = interpolate(frame, [0, durationInFrames], [0, panX], {
    extrapolateRight: "clamp",
  });
  const translateY = interpolate(frame, [0, durationInFrames], [0, panY], {
    extrapolateRight: "clamp",
  });

  return (
    <AbsoluteFill style={{ overflow: "hidden" }}>
      <Img
        src={src}
        style={{
          width: "100%",
          height: "100%",
          objectFit: "cover",
          transform: `scale(${scale}) translate(${translateX}px, ${translateY}px)`,
        }}
      />
    </AbsoluteFill>
  );
};
```

**Rules for Ken Burns:**
- Max zoom: 1.15x (anything higher looks jarring)
- Pan range: -30px to +30px per axis
- Alternate zoom direction per slide for visual variety
- Duration: at least 3 seconds per image (90 frames at 30fps)

## Layout Options

| Layout | Description | Best For |
|--------|-------------|----------|
| Full-bleed | Image fills entire frame | Immersive photo slideshows |
| Framed | Image with border/padding | Elegant, formal presentations |
| Grid-to-single | Grid of thumbnails, one zooms full | Portfolio reveals |
| Split screen | Two images side by side | Before/after, comparisons |
| Collage | Multiple images in creative layout | Event recaps, social media |
| Polaroid | White border, caption below | Casual, nostalgic feel |

## Duration Planning

| Image Count | Per Image | Total Duration | Transitions |
|-------------|-----------|----------------|-------------|
| 5 images | 5s | ~27s | 4 x 0.5s fade |
| 10 images | 4s | ~45s | 9 x 0.5s fade |
| 20 images | 3s | ~63s | 19 x 0.4s fade |
| 30+ images | 2.5s | ~80s+ | 0.3s crossfade |

Formula: `totalFrames = (imageCount * perImageFrames) - ((imageCount - 1) * transitionFrames)`

## Complete Starter Template

```tsx
import {
  AbsoluteFill,
  Img,
  Sequence,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
  interpolate,
  spring,
} from "remotion";
import { TransitionSeries, linearTiming } from "@remotion/transitions";
import { fade } from "@remotion/transitions/fade";

// -- Ken Burns Slide --
const KenBurnsSlide: React.FC<{
  src: string;
  caption?: string;
  index: number;
}> = ({ src, caption, index }) => {
  const frame = useCurrentFrame();
  const { durationInFrames, fps } = useVideoConfig();

  // Alternate zoom direction per slide
  const zoomIn = index % 2 === 0;
  const startScale = zoomIn ? 1 : 1.12;
  const endScale = zoomIn ? 1.12 : 1;
  const panDir = index % 2 === 0 ? -1 : 1;

  const scale = interpolate(frame, [0, durationInFrames], [startScale, endScale], {
    extrapolateRight: "clamp",
  });
  const translateX = interpolate(frame, [0, durationInFrames], [0, panDir * 25], {
    extrapolateRight: "clamp",
  });

  // Caption fade in
  const captionOpacity = caption
    ? interpolate(frame, [20, 35], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" })
    : 0;

  return (
    <AbsoluteFill style={{ backgroundColor: "#000000" }}>
      {/* Image with Ken Burns */}
      <AbsoluteFill style={{ overflow: "hidden" }}>
        <Img
          src={src}
          style={{
            width: "100%",
            height: "100%",
            objectFit: "cover",
            transform: `scale(${scale}) translateX(${translateX}px)`,
          }}
        />
      </AbsoluteFill>

      {/* Caption overlay */}
      {caption && (
        <div
          style={{
            position: "absolute",
            bottom: 80,
            left: 0,
            right: 0,
            textAlign: "center",
            opacity: captionOpacity,
          }}
        >
          <div
            style={{
              display: "inline-block",
              backgroundColor: "rgba(0, 0, 0, 0.6)",
              backdropFilter: "blur(8px)",
              padding: "16px 40px",
              borderRadius: 12,
            }}
          >
            <div
              style={{
                color: "#ffffff",
                fontSize: 36,
                fontWeight: 600,
                fontFamily: "Inter, sans-serif",
              }}
            >
              {caption}
            </div>
          </div>
        </div>
      )}
    </AbsoluteFill>
  );
};

// -- Main Slideshow Composition --
type SlideData = { src: string; caption?: string };

export const SlideshowVideo: React.FC<{
  slides: SlideData[];
  title?: string;
  transitionDuration?: number;
}> = ({ slides, title, transitionDuration = 15 }) => {
  const { fps } = useVideoConfig();
  const perSlideDuration = 4 * fps; // 4 seconds per slide

  return (
    <AbsoluteFill style={{ backgroundColor: "#000000" }}>
      {/* Title card */}
      {title && (
        <Sequence from={0} durationInFrames={3 * fps} name="Title">
          <TitleCard text={title} />
        </Sequence>
      )}

      {/* Photo slideshow with transitions */}
      <Sequence from={title ? 3 * fps : 0} name="Slideshow">
        <TransitionSeries>
          {slides.map((slide, i) => (
            <React.Fragment key={i}>
              <TransitionSeries.Sequence durationInFrames={perSlideDuration}>
                <KenBurnsSlide src={slide.src} caption={slide.caption} index={i} />
              </TransitionSeries.Sequence>
              {i < slides.length - 1 && (
                <TransitionSeries.Transition
                  presentation={fade()}
                  timing={linearTiming({ durationInFrames: transitionDuration })}
                />
              )}
            </React.Fragment>
          ))}
        </TransitionSeries>
      </Sequence>
    </AbsoluteFill>
  );
};

// -- Title Card --
const TitleCard: React.FC<{ text: string }> = ({ text }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const scale = spring({ frame, fps, config: { damping: 12, stiffness: 200 } });
  const opacity = interpolate(frame, [0, 15], [0, 1], { extrapolateRight: "clamp" });

  return (
    <AbsoluteFill
      style={{
        backgroundColor: "#000000",
        justifyContent: "center",
        alignItems: "center",
      }}
    >
      <div
        style={{
          transform: `scale(${scale})`,
          opacity,
          color: "#ffffff",
          fontSize: 64,
          fontWeight: 800,
          fontFamily: "Inter, sans-serif",
          textAlign: "center",
          padding: "0 80px",
          lineHeight: 1.2,
        }}
      >
        {text}
      </div>
    </AbsoluteFill>
  );
};
```

Register in `Root.tsx`:
```tsx
import { Composition } from "remotion";

<Composition
  id="SlideshowVideo"
  component={SlideshowVideo}
  durationInFrames={720}
  fps={30}
  width={1920}
  height={1080}
  defaultProps={{
    title: "Our Vacation 2025",
    slides: [
      { src: staticFile("photos/photo1.jpg"), caption: "Day 1 — Arrival" },
      { src: staticFile("photos/photo2.jpg"), caption: "The Beach" },
      { src: staticFile("photos/photo3.jpg"), caption: "Sunset" },
      { src: staticFile("photos/photo4.jpg"), caption: "Local Market" },
      { src: staticFile("photos/photo5.jpg") },
    ],
    transitionDuration: 15,
  }}
/>
```

## Dynamic Duration with calculateMetadata

For data-driven slideshows where length depends on image count:

```tsx
import { CalculateMetadataFunction } from "remotion";

type SlideshowProps = { slides: SlideData[]; title?: string; transitionDuration?: number };

export const calculateMetadata: CalculateMetadataFunction<SlideshowProps> = ({ props }) => {
  const fps = 30;
  const perSlide = 4 * fps; // 120 frames per slide
  const transition = props.transitionDuration ?? 15;
  const titleFrames = props.title ? 3 * fps : 0;
  const slideshowFrames = props.slides.length * perSlide - (props.slides.length - 1) * transition;
  return { durationInFrames: titleFrames + slideshowFrames, fps };
};
```

## Audio Integration

```tsx
import { Audio, staticFile } from "remotion";

// Background music — keep volume low
<Audio src={staticFile("music/ambient.mp3")} volume={0.3} />

// Transition sound effect
<Sequence from={transitionFrame}>
  <Audio src={staticFile("sfx/whoosh.mp3")} volume={0.5} />
</Sequence>
```

- Match image duration to music phrases for a polished feel
- Instrumental/ambient music works best (no vocals competing with captions)
- Add subtle whoosh or shutter SFX on transitions

## Quality Checklist

- [ ] All images use `<Img>` from remotion (not native `<img>`)
- [ ] All local images use `staticFile()` paths
- [ ] Ken Burns zoom is subtle (max 1.15x scale)
- [ ] Transitions are smooth (fade or crossfade, 0.3-0.5s)
- [ ] Text overlays readable over images (semi-transparent background)
- [ ] Caption text has sufficient contrast (dark overlay behind white text)
- [ ] Duration feels right (not too rushed, not too slow)
- [ ] Alternate zoom directions for visual variety
- [ ] Title card included if appropriate
- [ ] Background music volume does not overpower
- [ ] Used `spring()` for text animations
- [ ] All `Sequence` components have explicit `name` props

## Reference Files

- `references/slideshow-patterns.md` — Copy-paste component patterns for Ken Burns, grids, frames, captions
- `../../references/transition-catalog.md` — Transition effects catalog
- `../../references/color-palettes.md` — Curated color palettes
- `../../references/font-pairings.md` — Font pairing recommendations