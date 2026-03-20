# Slideshow Video — Code Patterns

Dense, copy-paste-ready component patterns for image slideshows. All use `<Img>` from Remotion and `staticFile()` for local assets.

---

## Ken Burns Component (Configurable)

Full control over zoom direction, start/end positions, and pan.

```tsx
const KenBurns: React.FC<{
  src: string;
  startScale?: number;
  endScale?: number;
  startX?: number;
  endX?: number;
  startY?: number;
  endY?: number;
}> = ({
  src,
  startScale = 1,
  endScale = 1.15,
  startX = 0,
  endX = -30,
  startY = 0,
  endY = -20,
}) => {
  const frame = useCurrentFrame();
  const { durationInFrames } = useVideoConfig();

  const scale = interpolate(frame, [0, durationInFrames], [startScale, endScale], {
    extrapolateRight: "clamp",
  });
  const x = interpolate(frame, [0, durationInFrames], [startX, endX], {
    extrapolateRight: "clamp",
  });
  const y = interpolate(frame, [0, durationInFrames], [startY, endY], {
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
          transform: `scale(${scale}) translate(${x}px, ${y}px)`,
        }}
      />
    </AbsoluteFill>
  );
};
```

---

## Image Transition Carousel

Loop through images using TransitionSeries with configurable transitions.

```tsx
import { TransitionSeries, linearTiming } from "@remotion/transitions";
import { fade } from "@remotion/transitions/fade";
import { slide } from "@remotion/transitions/slide";
import { wipe } from "@remotion/transitions/wipe";

const ImageCarousel: React.FC<{
  images: string[];
  perImageFrames?: number;
  transitionFrames?: number;
  transitionType?: "fade" | "slide" | "wipe";
}> = ({ images, perImageFrames = 120, transitionFrames = 15, transitionType = "fade" }) => {
  const getTransition = () => {
    switch (transitionType) {
      case "slide": return slide({ direction: "from-right" });
      case "wipe": return wipe({ direction: "from-left" });
      default: return fade();
    }
  };

  return (
    <TransitionSeries>
      {images.map((src, i) => (
        <React.Fragment key={i}>
          <TransitionSeries.Sequence durationInFrames={perImageFrames}>
            <AbsoluteFill style={{ backgroundColor: "#000" }}>
              <Img src={src} style={{ width: "100%", height: "100%", objectFit: "cover" }} />
            </AbsoluteFill>
          </TransitionSeries.Sequence>
          {i < images.length - 1 && (
            <TransitionSeries.Transition
              presentation={getTransition()}
              timing={linearTiming({ durationInFrames: transitionFrames })}
            />
          )}
        </React.Fragment>
      ))}
    </TransitionSeries>
  );
};
```

---

## Grid-to-Single Zoom

Show a grid of thumbnails, then one image zooms to fill the screen.

```tsx
const GridToSingle: React.FC<{
  images: string[];
  focusIndex: number;
  columns?: number;
}> = ({ images, focusIndex, columns = 3 }) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames, width, height } = useVideoConfig();

  const gridPhase = durationInFrames * 0.4; // 40% grid, 60% zoom
  const isZooming = frame > gridPhase;

  const zoomProgress = isZooming
    ? spring({ frame: frame - gridPhase, fps, config: { damping: 14, stiffness: 120 } })
    : 0;

  const rows = Math.ceil(images.length / columns);
  const cellW = width / columns;
  const cellH = height / rows;

  // Target cell position
  const focusRow = Math.floor(focusIndex / columns);
  const focusCol = focusIndex % columns;
  const targetX = focusCol * cellW;
  const targetY = focusRow * cellH;

  return (
    <AbsoluteFill style={{ backgroundColor: "#000" }}>
      <div
        style={{
          width: width * columns,
          height: height * rows,
          transform: isZooming
            ? `scale(${interpolate(zoomProgress, [0, 1], [1, columns])}) translate(${interpolate(zoomProgress, [0, 1], [0, -targetX])}px, ${interpolate(zoomProgress, [0, 1], [0, -targetY])}px)`
            : undefined,
          transformOrigin: "0 0",
          display: "grid",
          gridTemplateColumns: `repeat(${columns}, ${cellW}px)`,
          gridTemplateRows: `repeat(${rows}, ${cellH}px)`,
        }}
      >
        {images.map((src, i) => (
          <div key={i} style={{ overflow: "hidden", border: "2px solid #111" }}>
            <Img src={src} style={{ width: "100%", height: "100%", objectFit: "cover" }} />
          </div>
        ))}
      </div>
    </AbsoluteFill>
  );
};
```

---

## Photo Frame Component

Image with border, shadow, and slight rotation for a physical photo look.

```tsx
const PhotoFrame: React.FC<{
  src: string;
  rotation?: number;
  borderWidth?: number;
  borderColor?: string;
  shadowSize?: number;
}> = ({ src, rotation = -2, borderWidth = 12, borderColor = "#ffffff", shadowSize = 30 }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const entrance = spring({ frame, fps, config: { damping: 14, stiffness: 100 } });

  return (
    <AbsoluteFill style={{ justifyContent: "center", alignItems: "center", backgroundColor: "#1a1a1a" }}>
      <div
        style={{
          transform: `rotate(${rotation}deg) scale(${entrance})`,
          border: `${borderWidth}px solid ${borderColor}`,
          boxShadow: `0 ${shadowSize / 2}px ${shadowSize}px rgba(0,0,0,0.5)`,
          width: "70%",
          aspectRatio: "4/3",
          overflow: "hidden",
        }}
      >
        <Img src={src} style={{ width: "100%", height: "100%", objectFit: "cover" }} />
      </div>
    </AbsoluteFill>
  );
};
```

---

## Polaroid-Style Card

White border with caption area below the image.

```tsx
const PolaroidCard: React.FC<{
  src: string;
  caption: string;
  rotation?: number;
}> = ({ src, caption, rotation = -3 }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const drop = spring({ frame, fps, config: { damping: 10, stiffness: 80 } });

  return (
    <AbsoluteFill style={{ justifyContent: "center", alignItems: "center", backgroundColor: "#2a2a2a" }}>
      <div
        style={{
          transform: `rotate(${rotation}deg) translateY(${interpolate(drop, [0, 1], [-200, 0])}px)`,
          opacity: drop,
          backgroundColor: "#ffffff",
          padding: "20px 20px 60px 20px",
          boxShadow: "0 20px 60px rgba(0,0,0,0.4)",
          width: 600,
        }}
      >
        <Img src={src} style={{ width: "100%", aspectRatio: "1/1", objectFit: "cover", display: "block" }} />
        <div
          style={{
            marginTop: 16,
            fontSize: 28,
            fontFamily: "'Caveat', cursive",
            color: "#333",
            textAlign: "center",
          }}
        >
          {caption}
        </div>
      </div>
    </AbsoluteFill>
  );
};
```

---

## Text Strip Overlay

Semi-transparent bar with title/date overlaid on the image.

```tsx
const TextStrip: React.FC<{
  text: string;
  subtext?: string;
  position?: "top" | "bottom";
  bgColor?: string;
}> = ({ text, subtext, position = "bottom", bgColor = "rgba(0,0,0,0.6)" }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const slideIn = spring({ frame, fps, config: { damping: 15 } });

  return (
    <div
      style={{
        position: "absolute",
        [position]: 0,
        left: 0,
        right: 0,
        backgroundColor: bgColor,
        backdropFilter: "blur(8px)",
        padding: "24px 40px",
        transform: `translateY(${interpolate(slideIn, [0, 1], [position === "bottom" ? 100 : -100, 0])}px)`,
        opacity: slideIn,
      }}
    >
      <div style={{ color: "#fff", fontSize: 36, fontWeight: 700, fontFamily: "Inter, sans-serif" }}>
        {text}
      </div>
      {subtext && (
        <div style={{ color: "rgba(255,255,255,0.7)", fontSize: 24, fontWeight: 500, fontFamily: "Inter, sans-serif", marginTop: 6 }}>
          {subtext}
        </div>
      )}
    </div>
  );
};
```

---

## Image Reveal Animation

Clip-path expanding to reveal the image underneath.

```tsx
const ImageReveal: React.FC<{
  src: string;
  direction?: "center" | "left" | "top";
}> = ({ src, direction = "center" }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const progress = spring({ frame, fps, config: { damping: 14, stiffness: 100 } });

  const getClipPath = () => {
    switch (direction) {
      case "left":
        return `inset(0 ${interpolate(progress, [0, 1], [100, 0])}% 0 0)`;
      case "top":
        return `inset(0 0 ${interpolate(progress, [0, 1], [100, 0])}% 0)`;
      case "center":
      default:
        const inset = interpolate(progress, [0, 1], [50, 0]);
        return `inset(${inset}% ${inset}% ${inset}% ${inset}%)`;
    }
  };

  return (
    <AbsoluteFill>
      <Img
        src={src}
        style={{
          width: "100%",
          height: "100%",
          objectFit: "cover",
          clipPath: getClipPath(),
        }}
      />
    </AbsoluteFill>
  );
};
```

---

## Parallax Image Layers

Foreground and background layers moving at different speeds for depth.

```tsx
const ParallaxLayers: React.FC<{
  bgSrc: string;
  fgSrc: string;
}> = ({ bgSrc, fgSrc }) => {
  const frame = useCurrentFrame();
  const { durationInFrames } = useVideoConfig();

  const bgX = interpolate(frame, [0, durationInFrames], [0, -20], { extrapolateRight: "clamp" });
  const fgX = interpolate(frame, [0, durationInFrames], [0, -60], { extrapolateRight: "clamp" });

  return (
    <AbsoluteFill>
      {/* Background — slow movement */}
      <AbsoluteFill style={{ overflow: "hidden" }}>
        <Img
          src={bgSrc}
          style={{
            width: "110%",
            height: "110%",
            objectFit: "cover",
            transform: `translateX(${bgX}px) scale(1.1)`,
          }}
        />
      </AbsoluteFill>
      {/* Foreground — faster movement */}
      <AbsoluteFill style={{ overflow: "hidden" }}>
        <Img
          src={fgSrc}
          style={{
            width: "120%",
            height: "120%",
            objectFit: "cover",
            transform: `translateX(${fgX}px) scale(1.1)`,
          }}
        />
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
```

---

## Auto-Duration Composition

Calculate composition duration based on image count using `calculateMetadata`.

```tsx
import { CalculateMetadataFunction } from "remotion";

type SlideshowProps = {
  images: string[];
  secondsPerImage?: number;
  transitionFrames?: number;
  includeTitle?: boolean;
};

export const calculateSlideshowMetadata: CalculateMetadataFunction<SlideshowProps> = ({
  props,
}) => {
  const fps = 30;
  const perImage = (props.secondsPerImage ?? 4) * fps;
  const transition = props.transitionFrames ?? 15;
  const titleFrames = props.includeTitle ? 3 * fps : 0;

  const slideshowFrames =
    props.images.length * perImage - (props.images.length - 1) * transition;

  return {
    durationInFrames: titleFrames + slideshowFrames,
    fps,
    width: 1920,
    height: 1080,
  };
};
```

---

## Image Array Composition

Data-driven slideshow that takes an array of image objects and renders them sequentially.

```tsx
type ImageData = {
  src: string;
  caption?: string;
  durationSeconds?: number;
};

const DataDrivenSlideshow: React.FC<{ images: ImageData[] }> = ({ images }) => {
  const { fps } = useVideoConfig();

  let currentFrame = 0;
  const transitionFrames = 15;

  return (
    <AbsoluteFill style={{ backgroundColor: "#000" }}>
      {images.map((img, i) => {
        const dur = (img.durationSeconds ?? 4) * fps;
        const from = currentFrame;
        currentFrame += dur - (i < images.length - 1 ? transitionFrames : 0);

        return (
          <Sequence key={i} from={from} durationInFrames={dur} name={`Slide ${i + 1}`}>
            <KenBurns
              src={img.src}
              startScale={i % 2 === 0 ? 1 : 1.12}
              endScale={i % 2 === 0 ? 1.12 : 1}
            />
            {img.caption && <TextStrip text={img.caption} />}
          </Sequence>
        );
      })}
    </AbsoluteFill>
  );
};
```

---

## Caption Overlay Component

Positioned in the safe zone with readable styling over any image.

```tsx
const CaptionOverlay: React.FC<{
  text: string;
  position?: "top" | "center" | "bottom";
  style?: "bar" | "floating" | "minimal";
}> = ({ text, position = "bottom", style = "bar" }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const fadeIn = interpolate(frame, [10, 25], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  const positionStyle: Record<string, React.CSSProperties> = {
    top: { top: 60, left: 0, right: 0 },
    center: { top: "50%", left: 0, right: 0, transform: "translateY(-50%)" },
    bottom: { bottom: 60, left: 0, right: 0 },
  };

  const textStyle: Record<string, React.CSSProperties> = {
    bar: {
      backgroundColor: "rgba(0,0,0,0.6)",
      backdropFilter: "blur(8px)",
      padding: "16px 32px",
      textAlign: "center" as const,
    },
    floating: {
      textAlign: "center" as const,
      textShadow: "0 2px 12px rgba(0,0,0,0.9), 0 0 4px rgba(0,0,0,0.5)",
    },
    minimal: {
      textAlign: "center" as const,
      padding: "8px 24px",
    },
  };

  return (
    <div
      style={{
        position: "absolute",
        ...positionStyle[position],
        opacity: fadeIn,
        zIndex: 10,
      }}
    >
      <div
        style={{
          color: "#ffffff",
          fontSize: 32,
          fontWeight: 600,
          fontFamily: "Inter, sans-serif",
          ...textStyle[style],
        }}
      >
        {text}
      </div>
    </div>
  );
};
```