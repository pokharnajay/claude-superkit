# Font Pairings for Video Production

50 curated font pairings for Remotion video projects. All fonts are available via `@remotion/google-fonts`.

---

## How to Load Fonts in Remotion

```tsx
// Import pattern — use aliased imports for heading + body
import { loadFont as loadHeading } from '@remotion/google-fonts/BebasNeue';
import { loadFont as loadBody } from '@remotion/google-fonts/Inter';

const { fontFamily: headingFont } = loadHeading();
const { fontFamily: bodyFont } = loadBody();

// Use in JSX
<h1 style={{ fontFamily: headingFont }}>Heading Text</h1>
<p style={{ fontFamily: bodyFont }}>Body text goes here.</p>
```

---

## Bold / Impact Pairings (1-8)

Strong, attention-grabbing headings for high-energy content.

| # | Heading Font | Body Font | Mood | Best For |
|---|-------------|-----------|------|----------|
| 1 | Bebas Neue | Inter | Bold cinematic | Trailers, intros, countdowns |
| 2 | Oswald | Lato | Strong editorial | News, sports, announcements |
| 3 | Anton | Roboto | Maximum impact | Social ads, event promos |
| 4 | Raleway | Open Sans | Bold modern | Startup pitches, product launches |
| 5 | Montserrat | Source Sans 3 | Geometric power | Brand videos, marketing |
| 6 | Archivo Black | Work Sans | Heavy industrial | Manufacturing, automotive |
| 7 | Black Ops One | DM Sans | Military/gaming | Gaming trailers, action content |
| 8 | Teko | Nunito | Tall condensed | Stats, data reveals, sports |

```tsx
// #1 Bebas Neue + Inter
import { loadFont as loadHeading } from '@remotion/google-fonts/BebasNeue';
import { loadFont as loadBody } from '@remotion/google-fonts/Inter';
const { fontFamily: heading } = loadHeading();
const { fontFamily: body } = loadBody();

// #2 Oswald + Lato
import { loadFont as loadHeading } from '@remotion/google-fonts/Oswald';
import { loadFont as loadBody } from '@remotion/google-fonts/Lato';

// #3 Anton + Roboto
import { loadFont as loadHeading } from '@remotion/google-fonts/Anton';
import { loadFont as loadBody } from '@remotion/google-fonts/Roboto';

// #4 Raleway + Open Sans
import { loadFont as loadHeading } from '@remotion/google-fonts/Raleway';
import { loadFont as loadBody } from '@remotion/google-fonts/OpenSans';

// #5 Montserrat + Source Sans 3
import { loadFont as loadHeading } from '@remotion/google-fonts/Montserrat';
import { loadFont as loadBody } from '@remotion/google-fonts/SourceSans3';

// #6 Archivo Black + Work Sans
import { loadFont as loadHeading } from '@remotion/google-fonts/ArchivoBlack';
import { loadFont as loadBody } from '@remotion/google-fonts/WorkSans';

// #7 Black Ops One + DM Sans
import { loadFont as loadHeading } from '@remotion/google-fonts/BlackOpsOne';
import { loadFont as loadBody } from '@remotion/google-fonts/DMSans';

// #8 Teko + Nunito
import { loadFont as loadHeading } from '@remotion/google-fonts/Teko';
import { loadFont as loadBody } from '@remotion/google-fonts/Nunito';
```

---

## Elegant Pairings (9-16)

Serif headings with clean body text for a sophisticated, premium feel.

| # | Heading Font | Body Font | Mood | Best For |
|---|-------------|-----------|------|----------|
| 9 | Playfair Display | Source Sans 3 | Classic luxury | Fashion, wine, luxury brands |
| 10 | Cormorant Garamond | Montserrat | Refined contrast | Weddings, editorials, art |
| 11 | Libre Baskerville | Lora | Literary warmth | Book trailers, storytelling |
| 12 | DM Serif Display | DM Sans | Modern serif | Portfolio, design showcases |
| 13 | Crimson Pro | Inter | Warm academic | Education, research, lectures |
| 14 | EB Garamond | Karla | Old-world meets new | History, heritage, museums |
| 15 | Bodoni Moda | Outfit | High fashion | Fashion shows, beauty, editorial |
| 16 | Spectral | Nunito Sans | Gentle serif | Wellness, meditation, calm content |

```tsx
// #9 Playfair Display + Source Sans 3
import { loadFont as loadHeading } from '@remotion/google-fonts/PlayfairDisplay';
import { loadFont as loadBody } from '@remotion/google-fonts/SourceSans3';

// #10 Cormorant Garamond + Montserrat
import { loadFont as loadHeading } from '@remotion/google-fonts/CormorantGaramond';
import { loadFont as loadBody } from '@remotion/google-fonts/Montserrat';

// #11 Libre Baskerville + Lora
import { loadFont as loadHeading } from '@remotion/google-fonts/LibreBaskerville';
import { loadFont as loadBody } from '@remotion/google-fonts/Lora';

// #12 DM Serif Display + DM Sans
import { loadFont as loadHeading } from '@remotion/google-fonts/DMSerifDisplay';
import { loadFont as loadBody } from '@remotion/google-fonts/DMSans';

// #13 Crimson Pro + Inter
import { loadFont as loadHeading } from '@remotion/google-fonts/CrimsonPro';
import { loadFont as loadBody } from '@remotion/google-fonts/Inter';

// #14 EB Garamond + Karla
import { loadFont as loadHeading } from '@remotion/google-fonts/EBGaramond';
import { loadFont as loadBody } from '@remotion/google-fonts/Karla';

// #15 Bodoni Moda + Outfit
import { loadFont as loadHeading } from '@remotion/google-fonts/BodoniModa';
import { loadFont as loadBody } from '@remotion/google-fonts/Outfit';

// #16 Spectral + Nunito Sans
import { loadFont as loadHeading } from '@remotion/google-fonts/Spectral';
import { loadFont as loadBody } from '@remotion/google-fonts/NunitoSans';
```

---

## Modern Pairings (17-24)

Clean geometric sans-serifs and contemporary type for tech-forward content.

| # | Heading Font | Body Font | Mood | Best For |
|---|-------------|-----------|------|----------|
| 17 | Space Grotesk | Inter | Space-age clean | Tech products, AI, data |
| 18 | DM Sans | DM Serif Display | Reversed modern | Creative agencies, design |
| 19 | Plus Jakarta Sans | Inter | Warm geometric | SaaS, mobile apps, UI demos |
| 20 | Outfit | Spectral | Modern + classic | Architecture, luxury tech |
| 21 | Sora | Work Sans | Rounded modern | Friendly tech, fintech |
| 22 | Urbanist | Inter | Ultra clean | Minimal websites, product demos |
| 23 | Epilogue | Outfit | Variable weight | Branding, motion graphics |
| 24 | Albert Sans | Lora | Neo-humanist | Healthcare tech, edtech |

```tsx
// #17 Space Grotesk + Inter
import { loadFont as loadHeading } from '@remotion/google-fonts/SpaceGrotesk';
import { loadFont as loadBody } from '@remotion/google-fonts/Inter';

// #18 DM Sans + DM Serif Display
import { loadFont as loadHeading } from '@remotion/google-fonts/DMSans';
import { loadFont as loadBody } from '@remotion/google-fonts/DMSerifDisplay';

// #19 Plus Jakarta Sans + Inter
import { loadFont as loadHeading } from '@remotion/google-fonts/PlusJakartaSans';
import { loadFont as loadBody } from '@remotion/google-fonts/Inter';

// #20 Outfit + Spectral
import { loadFont as loadHeading } from '@remotion/google-fonts/Outfit';
import { loadFont as loadBody } from '@remotion/google-fonts/Spectral';

// #21 Sora + Work Sans
import { loadFont as loadHeading } from '@remotion/google-fonts/Sora';
import { loadFont as loadBody } from '@remotion/google-fonts/WorkSans';

// #22 Urbanist + Inter
import { loadFont as loadHeading } from '@remotion/google-fonts/Urbanist';
import { loadFont as loadBody } from '@remotion/google-fonts/Inter';

// #23 Epilogue + Outfit
import { loadFont as loadHeading } from '@remotion/google-fonts/Epilogue';
import { loadFont as loadBody } from '@remotion/google-fonts/Outfit';

// #24 Albert Sans + Lora
import { loadFont as loadHeading } from '@remotion/google-fonts/AlbertSans';
import { loadFont as loadBody } from '@remotion/google-fonts/Lora';
```

---

## Playful Pairings (25-30)

Fun, expressive type for casual and youth-oriented content.

| # | Heading Font | Body Font | Mood | Best For |
|---|-------------|-----------|------|----------|
| 25 | Bangers | Comic Neue | Comic book pop | Meme videos, fun explainers |
| 26 | Fredoka | Nunito | Rounded friendly | Kids content, education |
| 27 | Baloo 2 | Quicksand | Bubbly warm | Food, family, pets |
| 28 | Lilita One | Patrick Hand | Handmade bold | Crafts, DIY, casual vlogs |
| 29 | Bubblegum Sans | Comfortaa | Sweet retro | Candy brands, retro content |
| 30 | Luckiest Guy | Rubik | Cartoon punch | Gaming, comedy, shorts |

```tsx
// #25 Bangers + Comic Neue
import { loadFont as loadHeading } from '@remotion/google-fonts/Bangers';
import { loadFont as loadBody } from '@remotion/google-fonts/ComicNeue';

// #26 Fredoka + Nunito
import { loadFont as loadHeading } from '@remotion/google-fonts/Fredoka';
import { loadFont as loadBody } from '@remotion/google-fonts/Nunito';

// #27 Baloo 2 + Quicksand
import { loadFont as loadHeading } from '@remotion/google-fonts/Baloo2';
import { loadFont as loadBody } from '@remotion/google-fonts/Quicksand';

// #28 Lilita One + Patrick Hand
import { loadFont as loadHeading } from '@remotion/google-fonts/LilitaOne';
import { loadFont as loadBody } from '@remotion/google-fonts/PatrickHand';

// #29 Bubblegum Sans + Comfortaa
import { loadFont as loadHeading } from '@remotion/google-fonts/BubblegumSans';
import { loadFont as loadBody } from '@remotion/google-fonts/Comfortaa';

// #30 Luckiest Guy + Rubik
import { loadFont as loadHeading } from '@remotion/google-fonts/LuckiestGuy';
import { loadFont as loadBody } from '@remotion/google-fonts/Rubik';
```

---

## Tech / Monospace Pairings (31-36)

Code-centric type for developer and technical content.

| # | Heading Font | Body Font | Mood | Best For |
|---|-------------|-----------|------|----------|
| 31 | JetBrains Mono | Inter | Dev professional | Code tutorials, dev tools |
| 32 | Fira Code | IBM Plex Sans | Open source | OSS demos, Linux content |
| 33 | Space Mono | Space Grotesk | Retro terminal | Hacker aesthetics, CLI tools |
| 34 | Roboto Mono | Roboto | Google-native | Android, Material UI demos |
| 35 | Ubuntu Mono | Ubuntu | Linux spirit | Ubuntu/Linux content, servers |
| 36 | Source Code Pro | Source Sans 3 | Adobe clean | Code walkthroughs, IDE demos |

```tsx
// #31 JetBrains Mono + Inter
import { loadFont as loadHeading } from '@remotion/google-fonts/JetBrainsMono';
import { loadFont as loadBody } from '@remotion/google-fonts/Inter';

// #32 Fira Code + IBM Plex Sans
import { loadFont as loadHeading } from '@remotion/google-fonts/FiraCode';
import { loadFont as loadBody } from '@remotion/google-fonts/IBMPlexSans';

// #33 Space Mono + Space Grotesk
import { loadFont as loadHeading } from '@remotion/google-fonts/SpaceMono';
import { loadFont as loadBody } from '@remotion/google-fonts/SpaceGrotesk';

// #34 Roboto Mono + Roboto
import { loadFont as loadHeading } from '@remotion/google-fonts/RobotoMono';
import { loadFont as loadBody } from '@remotion/google-fonts/Roboto';

// #35 Ubuntu Mono + Ubuntu
import { loadFont as loadHeading } from '@remotion/google-fonts/UbuntuMono';
import { loadFont as loadBody } from '@remotion/google-fonts/Ubuntu';

// #36 Source Code Pro + Source Sans 3
import { loadFont as loadHeading } from '@remotion/google-fonts/SourceCodePro';
import { loadFont as loadBody } from '@remotion/google-fonts/SourceSans3';
```

---

## Minimal Pairings (37-42)

Understated, content-first typography.

| # | Heading Font | Body Font | Mood | Best For |
|---|-------------|-----------|------|----------|
| 37 | Inter | Inter | Ultimate minimal | UI recordings, clean tutorials |
| 38 | Outfit | Instrument Serif | Modern contrast | Portfolio, gallery, art |
| 39 | Manrope | Inter | Geometric clean | SaaS, dashboards, analytics |
| 40 | Work Sans | Merriweather | Balanced duo | Blog content, articles, essays |
| 41 | Jost | Libre Baskerville | Bauhaus + serif | Architecture, design studios |
| 42 | Karla | Inconsolata | Clean + code | Technical blogs, mixed content |

```tsx
// #37 Inter + Inter (weight variation)
import { loadFont } from '@remotion/google-fonts/Inter';
const { fontFamily } = loadFont();
// Use fontWeight: 700 for headings, 400 for body

// #38 Outfit + Instrument Serif
import { loadFont as loadHeading } from '@remotion/google-fonts/Outfit';
import { loadFont as loadBody } from '@remotion/google-fonts/InstrumentSerif';

// #39 Manrope + Inter
import { loadFont as loadHeading } from '@remotion/google-fonts/Manrope';
import { loadFont as loadBody } from '@remotion/google-fonts/Inter';

// #40 Work Sans + Merriweather
import { loadFont as loadHeading } from '@remotion/google-fonts/WorkSans';
import { loadFont as loadBody } from '@remotion/google-fonts/Merriweather';

// #41 Jost + Libre Baskerville
import { loadFont as loadHeading } from '@remotion/google-fonts/Jost';
import { loadFont as loadBody } from '@remotion/google-fonts/LibreBaskerville';

// #42 Karla + Inconsolata
import { loadFont as loadHeading } from '@remotion/google-fonts/Karla';
import { loadFont as loadBody } from '@remotion/google-fonts/Inconsolata';
```

---

## Corporate Pairings (43-46)

Traditional, trustworthy combinations for business content.

| # | Heading Font | Body Font | Mood | Best For |
|---|-------------|-----------|------|----------|
| 43 | Libre Baskerville | Source Sans 3 | Classic business | Annual reports, whitepapers |
| 44 | Merriweather | Open Sans | Warm authority | Non-profit, government, education |
| 45 | Noto Serif | Noto Sans | Universal coverage | Multi-language, global brands |
| 46 | IBM Plex Serif | IBM Plex Sans | Enterprise cohesion | Enterprise, IBM ecosystem |

```tsx
// #43 Libre Baskerville + Source Sans 3
import { loadFont as loadHeading } from '@remotion/google-fonts/LibreBaskerville';
import { loadFont as loadBody } from '@remotion/google-fonts/SourceSans3';

// #44 Merriweather + Open Sans
import { loadFont as loadHeading } from '@remotion/google-fonts/Merriweather';
import { loadFont as loadBody } from '@remotion/google-fonts/OpenSans';

// #45 Noto Serif + Noto Sans
import { loadFont as loadHeading } from '@remotion/google-fonts/NotoSerif';
import { loadFont as loadBody } from '@remotion/google-fonts/NotoSans';

// #46 IBM Plex Serif + IBM Plex Sans
import { loadFont as loadHeading } from '@remotion/google-fonts/IBMPlexSerif';
import { loadFont as loadBody } from '@remotion/google-fonts/IBMPlexSans';
```

---

## Handwritten Pairings (47-50)

Script and handwritten headings paired with clean body fonts.

| # | Heading Font | Body Font | Mood | Best For |
|---|-------------|-----------|------|----------|
| 47 | Caveat | DM Sans | Casual annotation | Tutorial annotations, notes |
| 48 | Dancing Script | Lato | Flowing elegance | Invitations, celebrations |
| 49 | Pacifico | Montserrat | Surf retro | Lifestyle, beach, California vibes |
| 50 | Sacramento | Raleway | Delicate script | Wedding, luxury events, beauty |

```tsx
// #47 Caveat + DM Sans
import { loadFont as loadHeading } from '@remotion/google-fonts/Caveat';
import { loadFont as loadBody } from '@remotion/google-fonts/DMSans';

// #48 Dancing Script + Lato
import { loadFont as loadHeading } from '@remotion/google-fonts/DancingScript';
import { loadFont as loadBody } from '@remotion/google-fonts/Lato';

// #49 Pacifico + Montserrat
import { loadFont as loadHeading } from '@remotion/google-fonts/Pacifico';
import { loadFont as loadBody } from '@remotion/google-fonts/Montserrat';

// #50 Sacramento + Raleway
import { loadFont as loadHeading } from '@remotion/google-fonts/Sacramento';
import { loadFont as loadBody } from '@remotion/google-fonts/Raleway';
```

---

## Font Size Guide for Video

| Element | 1080p (px) | 4K (px) | Notes |
|---------|-----------|---------|-------|
| Main Title | 72-120 | 144-240 | Bold weight, center frame |
| Subtitle | 36-54 | 72-108 | Regular or medium weight |
| Body Text | 24-36 | 48-72 | Regular weight, max 60 chars/line |
| Caption | 18-24 | 36-48 | Light or regular, muted color |
| Lower Third Name | 32-42 | 64-84 | Semi-bold |
| Lower Third Title | 20-28 | 40-56 | Regular, smaller than name |
| Code Snippet | 20-28 | 40-56 | Monospace, letter-spacing: 0 |

## Typography Tips for Video

- **Line height:** Use 1.2-1.4 for headings, 1.5-1.7 for body text
- **Letter spacing:** Increase by 0.02-0.05em for uppercase headings
- **Max width:** Limit text blocks to 60-70% of frame width for readability
- **Contrast:** WCAG AAA (7:1) minimum for body text on video backgrounds
- **Weight:** Use at least medium (500) for body text — regular (400) can appear thin on video
- **Avoid:** Thin/light weights below 300 — they disappear during compression
