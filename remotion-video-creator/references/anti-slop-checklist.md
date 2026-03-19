# Anti-Slop Checklist — Video Quality Gates

> Fill the spec template before writing code. Run the audit before delivering. No exceptions.

---

## Video Specification Template

**Fill this out BEFORE writing any Remotion code:**

```
Format:      [platform] [width]x[height] @ [fps]fps, [duration]s ([totalFrames] frames)
Palette:     [name] — bg: #hex, fg: #hex, accent: #hex, muted: #hex
Typography:  heading=[FontName] [weight], body=[FontName] [weight]
Scenes:      [count] scenes, transitions: [type] ([durationInFrames]f each)
Audio:       [bg music / voiceover / SFX / silent] — volume: [0-1]
Style:       [modern/corporate/playful/elegant/minimal/bold/tech/retro/cinematic]
Hook:        [What happens in first 3 seconds to grab attention]
CTA:         [What the viewer should do at the end]
```

### Example — Filled:
```
Format:      TikTok 1080x1920 @ 30fps, 15s (450 frames)
Palette:     Midnight — bg: #0a0a0f, fg: #ffffff, accent: #6366f1, muted: #4b5563
Typography:  heading=Inter 700, body=Inter 400
Scenes:      4 scenes, transitions: fade (12f each)
Audio:       bg music at 0.2, SFX whoosh on scene transitions
Style:       modern/tech
Hook:        Large animated stat counter "10x faster" with spring bounce
CTA:         "Follow for more" with animated arrow
```

---

## Banned Patterns — NEVER Do These

### Animation Anti-Patterns
| Banned | Why | Do Instead |
|--------|-----|------------|
| `Easing.linear` on everything | Mechanical, robotic feel | `Easing.out(Easing.ease)` or `spring()` |
| Same duration for all animations | No visual rhythm | Vary: 12f, 18f, 24f — create hierarchy |
| Text appearing instantly (no animation) | Jarring, amateur | Fade + slide/scale in over 10-20 frames |
| All elements animate at same time | Visual overload, no focus | Stagger by 5-10 frames per element |
| Jarring cuts (no transitions) | Feels broken | Use TransitionSeries with fade/slide |
| Animation on every single element | Distracting, slow | Animate key elements, let others be static |

### Code Anti-Patterns
| Banned | Why | Do Instead |
|--------|-----|------------|
| `<img>` tag | Won't work in Remotion rendering | `<Img>` from `remotion` |
| `<video>` tag | Won't sync with Remotion timeline | `<Video>` or `<OffthreadVideo>` from `remotion` |
| `<audio>` tag | Won't sync with Remotion timeline | `<Audio>` from `remotion` |
| CSS `transition` property | Not frame-accurate, breaks rendering | `useCurrentFrame()` + `interpolate()` |
| CSS `animation` / `@keyframes` | Not frame-accurate, breaks rendering | `useCurrentFrame()` + `interpolate()` |
| Tailwind `animate-*` classes | CSS animation under the hood | `useCurrentFrame()` + `interpolate()` |
| Tailwind `transition-*` classes | CSS transition under the hood | `useCurrentFrame()` + `interpolate()` |
| `requestAnimationFrame` | Conflicts with Remotion frame system | `useCurrentFrame()` |
| `setTimeout` / `setInterval` | Not deterministic, breaks rendering | `useCurrentFrame()` for timing |
| `useEffect` for animation state | Side effects break deterministic rendering | Derive everything from `useCurrentFrame()` |
| `Math.random()` | Non-deterministic across renders | `random('seed')` from `remotion` |
| Hardcoded pixel values for layout | Breaks on different resolutions | Use `%`, `useVideoConfig()`, or relative calc |

### Typography Anti-Patterns
| Banned | Why | Do Instead |
|--------|-----|------------|
| Font size < 20px at 1080p | Unreadable on mobile | Min 24px body, 36px+ headings |
| Using system fonts without loading | May not exist on render server | `@remotion/google-fonts` or `staticFile()` |
| Not calling `waitUntilDone()` | Font may not be loaded at render time | Always wait for font load with `delayRender` |
| More than 2-3 font families | Cluttered, unprofessional | 1 heading font + 1 body font max |
| Centered text longer than 40 chars | Hard to read centered long text | Left-align long text, center only short text |

### Layout Anti-Patterns
| Banned | Why | Do Instead |
|--------|-----|------------|
| Content outside safe zones | Hidden behind platform UI | Check safe zone specs per platform |
| No background behind text | Text unreadable over busy visuals | Add semi-transparent backdrop or text shadow |
| Text on unsaturated background | Low contrast, accessibility fail | Ensure WCAG AA contrast (4.5:1 minimum) |
| Cramming too much on screen | Overwhelming, nothing is readable | Max 3-5 elements visible at once |

---

## Self-Audit Checklist — Run Before Delivering

### 1. Timing & Animation
- [ ] Animations have VARIETY — not all the same duration
- [ ] Enter animations decelerate (Easing.out or spring)
- [ ] Exit animations accelerate (Easing.in)
- [ ] Stagger delay between grouped elements (5-10f)
- [ ] No animation lasts longer than 30 frames unless intentional
- [ ] No animation is shorter than 5 frames (too fast to see)

### 2. Transitions
- [ ] Smooth transitions between ALL scenes (no hard cuts unless intentional)
- [ ] Transition duration matches video energy (fast=8-12f, corporate=15-20f)
- [ ] TransitionSeries used correctly (not overlapping Sequences manually)

### 3. Audio
- [ ] Audio volume appropriate (BG music 0.1-0.3, VO 0.7-1.0, SFX 0.3-0.6)
- [ ] Audio fades in at start (first 10-15 frames)
- [ ] Audio fades out at end (last 10-15 frames)
- [ ] SFX synced to visual events (hit frame matches animation start)
- [ ] No audio clipping or sudden volume changes

### 4. Typography
- [ ] All fonts loaded with `loadFont()` + `waitUntilDone()`
- [ ] Heading: minimum 36px at 1080p, bold weight
- [ ] Body: minimum 24px at 1080p, regular or medium weight
- [ ] Maximum 2 font families used
- [ ] Text has sufficient contrast against background (4.5:1+ ratio)
- [ ] Line height comfortable (1.2-1.5x font size)

### 5. Color & Visual
- [ ] Consistent palette across ALL scenes (max 4-5 colors)
- [ ] No pure white (#fff) on pure black (#000) — too harsh (use #f0f0f0 / #0a0a0a)
- [ ] Accent color used sparingly for emphasis only
- [ ] Backgrounds are not plain flat colors (add gradient, noise, or texture)

### 6. Layout & Platform
- [ ] Safe zones respected — no content behind platform UI
- [ ] Critical text in center 80% of frame
- [ ] Output dimensions match target platform
- [ ] FPS matches target platform (usually 30)
- [ ] Total durationInFrames = scenes * framesPerScene + transitions accounted

### 7. Code Quality
- [ ] No CSS transitions, animations, or Tailwind animate-* classes
- [ ] All animation derived from `useCurrentFrame()`
- [ ] Using `<Img>`, `<Video>`, `<Audio>` (NOT native HTML tags)
- [ ] Using `staticFile()` for public directory assets
- [ ] Using `random('seed')` instead of `Math.random()`
- [ ] `delayRender` / `continueRender` for async data loading
- [ ] No unused imports or dead code

### 8. Hook & CTA
- [ ] First 3 seconds grab attention (bold visual, surprising stat, question)
- [ ] Last 3-5 seconds have clear CTA (follow, subscribe, visit, share)
- [ ] CTA is animated to draw attention

### 9. Performance
- [ ] No more than ~20 animated elements simultaneously
- [ ] Images optimized (not raw 8K photos in a 1080p video)
- [ ] `<OffthreadVideo>` used instead of `<Video>` for rendering
- [ ] No infinite loops or recursive calculations in render function

### 10. Final Output
- [ ] Codec matches platform (H.264 MP4 for all social media)
- [ ] CRF appropriate (18-23 for social, 15-18 for YouTube)
- [ ] File size within platform limits
- [ ] Video renders without errors or warnings

---

## Refinement Protocol — After First Draft

### Step 1: Watch at 1x Speed
Do not scrub frame by frame. Watch the rendered video at actual playback speed. Does it feel right?

### Step 2: Check the Hook (0-3s)
- Does something visually striking happen immediately?
- Would you stop scrolling for this?
- Is the topic/value clear within 3 seconds?

### Step 3: Check the CTA (last 3-5s)
- Is there a clear next action for the viewer?
- Is the CTA visible and animated?
- Does the ending feel intentional, not abrupt?

### Step 4: Subtract Before Adding
- Can any element be removed without losing meaning?
- Are there redundant animations?
- Is any text unnecessary?
- Less is more. Every element should earn its place.

### Step 5: Adjust Timing Before Effects
Better timing with simple animations > bad timing with fancy effects.
- Tighten animations that feel slow
- Add breathing room where it feels rushed
- Ensure stagger creates readable flow, not chaos

### Step 6: Color and Contrast Pass
- Squint at the video. Can you still read everything?
- Screenshot a frame, convert to grayscale. Is hierarchy clear?
- Check contrast with a tool if uncertain

---

## Scene Timing Guidelines

| Scene Type | Recommended Duration | Frames @ 30fps |
|-----------|---------------------|----------------|
| Title/intro card | 2-3s | 60-90 |
| Key message / stat | 3-5s | 90-150 |
| Detail / explanation | 4-6s | 120-180 |
| Visual showcase | 3-4s | 90-120 |
| Transition (between scenes) | 0.3-0.7s | 8-20 |
| CTA / outro | 2-4s | 60-120 |
| Logo sting | 1-2s | 30-60 |

### Total Duration Planning
```
Example: 30-second TikTok (900 frames)
- Scene 1 (Hook):      90f  (3s)
- Transition:           12f  (0.4s)
- Scene 2 (Problem):    120f (4s)
- Transition:           12f  (0.4s)
- Scene 3 (Solution):   150f (5s)
- Transition:           12f  (0.4s)
- Scene 4 (Benefits):   120f (4s)
- Transition:           12f  (0.4s)
- Scene 5 (Social Proof): 120f (4s)
- Transition:           12f  (0.4s)
- Scene 6 (CTA):        90f  (3s)
- Transition overlaps:  -60f (reclaimed from overlapping transitions)
Total:                   900f = 30s ✓

Note: TransitionSeries handles transition overlap automatically.
When using TransitionSeries, durationInFrames of each Sequence is the
FULL duration including the transition overlap period.
```

---

## Quick Color Palettes — Tested for Video

| Name | Background | Foreground | Accent | Muted | Style |
|------|-----------|------------|--------|-------|-------|
| Midnight | #0a0a0f | #f0f0f0 | #6366f1 | #4b5563 | Modern/Tech |
| Ocean | #0c1222 | #e2e8f0 | #38bdf8 | #475569 | Clean/SaaS |
| Forest | #0a1612 | #ecfdf5 | #34d399 | #4b5563 | Nature/Health |
| Sunset | #1a0a0a | #fef2f2 | #f97316 | #6b7280 | Warm/Creative |
| Royal | #0f0720 | #f5f3ff | #a78bfa | #6b7280 | Premium/Luxury |
| Coral | #1a0505 | #fff1f2 | #fb7185 | #6b7280 | Playful/Social |
| Slate | #0f172a | #f8fafc | #94a3b8 | #475569 | Corporate/Neutral |
| Ember | #0c0a09 | #fafaf9 | #f59e0b | #78716c | Bold/Energy |
| Light Clean | #fafafa | #18181b | #2563eb | #a1a1aa | Minimal/Light |
| Light Warm | #fffbeb | #1c1917 | #d97706 | #a8a29e | Friendly/Light |
