---
name: explainer-video
description: Create product demos, tutorial videos, feature walkthroughs, and how-to content. Use for educational or marketing video content that explains a product, service, or concept with clear visual storytelling.
---

# Explainer Video

Product demos, tutorials, and feature walkthroughs with clear visual storytelling and structured narratives.

## When to Use

- User wants a product demo or software walkthrough
- User asks for a tutorial, how-to, or explainer video
- User wants to showcase features or compare options
- User mentions onboarding video, welcome video, or setup guide
- User wants a marketing or promotional explainer

## Common Formats

| Format | Description | Typical Duration | Aspect |
|---|---|---|---|
| Product demo | Software walkthrough with UI mockups | 30-90s | 16:9 |
| Feature showcase | Highlight 3-5 key features | 30-60s | 16:9 or 9:16 |
| Tutorial/how-to | Step-by-step guide | 60-180s | 16:9 |
| Comparison | Us vs competitors side-by-side | 30-60s | 16:9 |
| Onboarding flow | Welcome + setup guide | 30-60s | 16:9 |
| Pitch deck video | Animated pitch slides | 60-120s | 16:9 |

## Standard Scene Structure

| Scene | Duration | Content | Animation |
|---|---|---|---|
| Intro | 5-8s (150-240 frames) | Brand logo + hook question | Fade in, scale spring |
| Problem | 8-12s (240-360 frames) | Pain point illustration | Slide in, text reveal |
| Solution | 10-15s (300-450 frames) | Product/feature reveal | Zoom, mockup reveal |
| Features | 15-30s (3-5 features x 5-8s) | Individual feature demos | Staggered cards, callouts |
| CTA | 5-8s (150-240 frames) | Call to action + URL | Pulse, fade |

## Animation Approach

- **Moderate pacing**: 5-10s per scene, slower than social media
- **Smooth transitions**: fade and slide, 15-20 frames duration
- **Callout annotations**: arrows, circles, highlights to draw attention
- **Zoom-to-detail**: scale + translate to focus on a region
- **Step indicators**: 1/3, 2/3, 3/3 with progress
- **Consistent motion direction**: left-to-right flow for progression

## Workflow

1. Read `references/explainer-patterns.md` for component patterns
2. Read `../../references/color-palettes.md` and `../../references/font-pairings.md`
3. Define the narrative structure: Problem -> Solution -> Features -> CTA
4. Choose format (landscape 16:9 or vertical 9:16)
5. Design scene components using mockup patterns
6. Add callout annotations for feature highlighting
7. Register composition and render

## Starter Template (Product Demo)

```tsx
import { AbsoluteFill, Sequence, useCurrentFrame, useVideoConfig, interpolate, spring, Img, staticFile } from "remotion";
import { TransitionSeries, linearTiming } from "@remotion/transitions";
import { fade } from "@remotion/transitions/fade";
import { slide } from "@remotion/transitions/slide";
import { loadFont } from "@remotion/google-fonts/Inter";

const { fontFamily } = loadFont();

const COLORS = {
  bg: "#fafafa",
  card: "#ffffff",
  text: "#1a1a1a",
  muted: "#6b7280",
  accent: "#3b82f6",
  accentLight: "#dbeafe",
};

// -- Intro Scene --
const IntroScene: React.FC<{ title: string; subtitle: string }> = ({ title, subtitle }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const titleScale = spring({ frame, fps, config: { damping: 12, stiffness: 200 } });
  const subtitleOpacity = interpolate(frame, [15, 30], [0, 1], { extrapolateRight: "clamp" });

  return (
    <AbsoluteFill style={{ backgroundColor: COLORS.bg, justifyContent: "center", alignItems: "center" }}>
      <div style={{ textAlign: "center" }}>
        <div
          style={{
            fontSize: 64,
            fontWeight: 800,
            fontFamily,
            color: COLORS.text,
            transform: `scale(${titleScale})`,
            marginBottom: 20,
          }}
        >
          {title}
        </div>
        <div
          style={{
            fontSize: 28,
            fontWeight: 500,
            fontFamily,
            color: COLORS.muted,
            opacity: subtitleOpacity,
          }}
        >
          {subtitle}
        </div>
      </div>
    </AbsoluteFill>
  );
};

// -- Problem Scene --
const ProblemScene: React.FC<{ problem: string; details: string[] }> = ({ problem, details }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  return (
    <AbsoluteFill style={{ backgroundColor: COLORS.bg, justifyContent: "center", padding: "0 120px" }}>
      <div
        style={{
          fontSize: 48,
          fontWeight: 800,
          fontFamily,
          color: COLORS.text,
          marginBottom: 40,
          opacity: interpolate(frame, [0, 15], [0, 1], { extrapolateRight: "clamp" }),
        }}
      >
        {problem}
      </div>
      {details.map((detail, i) => {
        const delay = 20 + i * 15;
        const s = spring({ frame: frame - delay, fps, config: { damping: 14 } });
        return (
          <div
            key={i}
            style={{
              fontSize: 28,
              fontWeight: 500,
              fontFamily,
              color: COLORS.muted,
              marginBottom: 16,
              opacity: s,
              transform: `translateX(${interpolate(s, [0, 1], [40, 0])}px)`,
              display: "flex",
              alignItems: "center",
              gap: 12,
            }}
          >
            <span style={{ color: "#ef4444", fontSize: 24 }}>&#x2717;</span>
            {detail}
          </div>
        );
      })}
    </AbsoluteFill>
  );
};

// -- Feature Card Scene --
const FeatureScene: React.FC<{
  title: string;
  description: string;
  index: number;
  total: number;
}> = ({ title, description, index, total }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const cardScale = spring({ frame, fps, config: { damping: 12, stiffness: 180 } });

  return (
    <AbsoluteFill style={{ backgroundColor: COLORS.bg, justifyContent: "center", alignItems: "center" }}>
      {/* Step counter */}
      <div
        style={{
          position: "absolute",
          top: 60,
          right: 80,
          fontSize: 20,
          fontWeight: 600,
          fontFamily,
          color: COLORS.muted,
        }}
      >
        {index + 1} / {total}
      </div>
      {/* Feature card */}
      <div
        style={{
          transform: `scale(${cardScale})`,
          backgroundColor: COLORS.card,
          borderRadius: 24,
          padding: "60px 80px",
          boxShadow: "0 4px 24px rgba(0,0,0,0.08)",
          maxWidth: 800,
          textAlign: "center",
        }}
      >
        <div style={{ fontSize: 44, fontWeight: 800, fontFamily, color: COLORS.text, marginBottom: 20 }}>
          {title}
        </div>
        <div style={{ fontSize: 24, fontWeight: 400, fontFamily, color: COLORS.muted, lineHeight: 1.5 }}>
          {description}
        </div>
      </div>
    </AbsoluteFill>
  );
};

// -- CTA Scene --
const CTAScene: React.FC<{ cta: string; url: string }> = ({ cta, url }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const btnScale = spring({ frame: frame - 10, fps, config: { damping: 10 } });
  const pulse = 1 + Math.sin(frame * 0.1) * 0.02;

  return (
    <AbsoluteFill style={{ backgroundColor: COLORS.bg, justifyContent: "center", alignItems: "center" }}>
      <div style={{ textAlign: "center" }}>
        <div
          style={{
            fontSize: 48,
            fontWeight: 800,
            fontFamily,
            color: COLORS.text,
            marginBottom: 40,
            opacity: interpolate(frame, [0, 15], [0, 1], { extrapolateRight: "clamp" }),
          }}
        >
          {cta}
        </div>
        <div
          style={{
            transform: `scale(${btnScale * pulse})`,
            backgroundColor: COLORS.accent,
            color: "#fff",
            fontSize: 28,
            fontWeight: 700,
            fontFamily,
            padding: "18px 48px",
            borderRadius: 12,
            display: "inline-block",
          }}
        >
          {url}
        </div>
      </div>
    </AbsoluteFill>
  );
};

// -- Main Composition --
export const ExplainerVideo: React.FC<{
  title: string;
  subtitle: string;
  problem: string;
  problemDetails: string[];
  features: { title: string; description: string }[];
  cta: string;
  url: string;
}> = ({ title, subtitle, problem, problemDetails, features, cta, url }) => (
  <TransitionSeries>
    <TransitionSeries.Sequence durationInFrames={180}>
      <IntroScene title={title} subtitle={subtitle} />
    </TransitionSeries.Sequence>
    <TransitionSeries.Transition presentation={fade()} timing={linearTiming({ durationInFrames: 15 })} />
    <TransitionSeries.Sequence durationInFrames={300}>
      <ProblemScene problem={problem} details={problemDetails} />
    </TransitionSeries.Sequence>
    <TransitionSeries.Transition presentation={slide({ direction: "from-right" })} timing={linearTiming({ durationInFrames: 15 })} />
    {features.map((feat, i) => (
      <>
        <TransitionSeries.Sequence key={i} durationInFrames={180}>
          <FeatureScene title={feat.title} description={feat.description} index={i} total={features.length} />
        </TransitionSeries.Sequence>
        <TransitionSeries.Transition presentation={fade()} timing={linearTiming({ durationInFrames: 12 })} />
      </>
    ))}
    <TransitionSeries.Sequence durationInFrames={180}>
      <CTAScene cta={cta} url={url} />
    </TransitionSeries.Sequence>
  </TransitionSeries>
);
```

Register in `Root.tsx`:
```tsx
<Composition
  id="ExplainerVideo"
  component={ExplainerVideo}
  durationInFrames={1200}
  fps={30}
  width={1920}
  height={1080}
  defaultProps={{
    title: "Introducing ProductName",
    subtitle: "The better way to do X",
    problem: "The old way is broken",
    problemDetails: ["Takes too long", "Too expensive", "Too complicated"],
    features: [
      { title: "Fast Setup", description: "Get started in under 2 minutes with zero configuration." },
      { title: "Smart Automation", description: "AI handles the tedious work so you can focus on what matters." },
      { title: "Beautiful Results", description: "Professional output every time, no design skills needed." },
    ],
    cta: "Try it free today",
    url: "product.com/start",
  }}
/>
```

## UI Mockup Patterns

### Browser Chrome
Wrap content in a browser frame with URL bar. See `references/explainer-patterns.md` for the component.

### Phone Mockup
iPhone-style frame for mobile app demos. See references for component.

### App Screenshot with Zoom
Show full screen, then zoom into a specific feature area.

## Annotation Patterns

- **Callout arrow**: Animated SVG line from label to target
- **Circle highlight**: Pulsing circle around a UI element
- **Tooltip bubble**: Speech bubble with pointer
- **Checkmark list**: Items appear one by one with animated checkmarks

## Color Strategy for Explainers

- Light backgrounds (#fafafa, #f8f9fa) for professional look
- Dark text (#1a1a1a) for readability
- Single accent color for highlights and CTAs
- Muted gray for secondary text (#6b7280)
- Use brand colors if provided by user

## Quality Checklist

- [ ] Narrative follows Problem -> Solution -> Features -> CTA structure
- [ ] Each scene has clear purpose and information hierarchy
- [ ] Pacing is moderate (5-10s per scene, not rushed)
- [ ] Transitions are smooth (fade or slide, 12-15 frames)
- [ ] Text is readable (24px+ body, 44px+ headlines at 1920x1080)
- [ ] UI mockups have realistic chrome (browser frame or phone)
- [ ] Feature cards have consistent styling
- [ ] Step counter visible during feature sequence
- [ ] CTA is prominent with URL or action
- [ ] Brand colors consistent throughout
- [ ] Spring animations used for natural motion
- [ ] No more than 2 font families

## Reference Files

- `references/explainer-patterns.md` -- Mockup, callout, and annotation components
- `../../references/color-palettes.md` -- Color palettes
- `../../references/font-pairings.md` -- Font recommendations
- `../../references/transition-catalog.md` -- Transition effects