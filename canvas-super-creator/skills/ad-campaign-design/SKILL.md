---
name: ad-campaign-design
description: Digital ad banners in IAB standard sizes, Google Ads, Facebook Ads, and multi-size ad campaigns with visual consistency. Use when user asks for ad banners, display ads, retargeting creatives, or a multi-format ad campaign.
license: MIT
metadata:
  author: canvas-super-creator
  version: 4.0.0
---

# Ad Campaign Design — Digital Display Advertising

Create digital ad banners in IAB standard sizes with campaign-wide visual consistency. Ad design is the most constrained creative discipline: fixed sizes, strict element limits, and one goal — the click.

---

## IAB Standard Ad Sizes

| Format | Dimensions (px) | Aspect | Frequency |
|---|---|---|---|
| Leaderboard | 728 x 90 | 8.1:1 | Very high — top of page |
| Medium Rectangle | 300 x 250 | 1.2:1 | Highest — sidebar/in-content |
| Wide Skyscraper | 160 x 600 | 1:3.75 | High — sidebar |
| Billboard | 970 x 250 | 3.88:1 | High — premium placements |
| Large Rectangle | 336 x 280 | 1.2:1 | Medium — in-content |
| Half Page | 300 x 600 | 1:2 | Medium — high impact |
| Mobile Leaderboard | 320 x 50 | 6.4:1 | Very high — mobile |
| Mobile Interstitial | 320 x 480 | 1:1.5 | High — full screen mobile |
| Large Mobile | 320 x 100 | 3.2:1 | High — mobile |

**Full details:** Read `./canvas-super-creator/references/formats.md` for safe zones.

---

## Workflow

1. **Read references:**
   - `./canvas-super-creator/references/formats.md` — dimensions, safe zones
   - `./canvas-super-creator/references/color-palettes.md` — palette selection
   - `./canvas-super-creator/references/typography-pairings.md` — font pairing
   - `./canvas-super-creator/references/composition-guide.md` — layout technique
   - `./canvas-super-creator/references/anti-slop-checklist.md` — quality gates
   - `./html-design/references/css-techniques.md` — CSS technique catalog
   - `./ad-campaign-design/references/ad-patterns.md` — ad-specific recipes

2. **Design master ad (300x250)** — this is the canonical design. All other sizes adapt from it.

3. **Output specification** with format, palette, typography, CTA style, brand mark position

4. **Design with html-design patterns** — follow the 4-phase process

5. **Adapt to all required sizes** — maintain visual consistency across every format

6. **Render via render-engine** pipeline

---

## Campaign Consistency Rules

When creating a multi-size campaign, these elements MUST be identical across all sizes:

- **Color palette.** Same `--bg`, `--fg`, `--accent` custom properties across every ad.
- **Typography.** Same font families, same weight for headings and body.
- **CTA button style.** Same background color, border-radius, padding proportions, text style.
- **Brand mark.** Same logo or brand name in the same position relative to the layout (typically bottom-right or bottom-left).
- **Visual treatment.** If one ad uses a gradient background, all use it. If one uses a photo, all use the same photo (cropped for each size).

### Shared CSS Custom Properties

```css
:root {
    --brand-bg: #0C0C0F;
    --brand-fg: #E8ECF0;
    --brand-accent: #4A90D9;
    --brand-cta-bg: #E63B2E;
    --brand-cta-fg: #FFFFFF;
    --brand-font-heading: 'BricolageGrotesque', sans-serif;
    --brand-font-body: 'Outfit', sans-serif;
    --brand-font-cta: 'WorkSans', sans-serif;
    --brand-radius: 6px;
}
```

---

## The 3-Element Rule

Every ad has a maximum of three elements. This is a hard rule, not a guideline:

1. **Headline** — the value proposition in 5-8 words maximum
2. **Visual** — product image, hero graphic, or brand mark
3. **CTA** — one button with a clear action verb

### Element Priority by Size

| Size | Primary | Secondary | Tertiary |
|---|---|---|---|
| 728x90 | Headline | CTA | Logo |
| 300x250 | Visual | Headline + CTA | Logo |
| 160x600 | Logo + Visual | Headline | CTA |
| 970x250 | Visual + Headline | CTA | Logo |
| 300x600 | Visual | Headline | CTA |
| 320x50 | Headline | CTA | Logo (optional) |

---

## Size-Specific Layout Strategies

### 728x90 — Leaderboard

Horizontal flow: logo left, headline center, CTA right. Extremely limited vertical space.

```
+--[LOGO]--[--------- HEADLINE ---------]--[CTA BUTTON]--+
|          max 5 words, single line                        |
+---------------------------------------------------------+
```

- Font size: headline 24-28px, CTA 14-16px
- No body text. No subheadline. No paragraph.
- Logo max height: 40px
- CTA button height: 36px max

### 300x250 — Medium Rectangle

Vertical stack: visual top, headline middle, CTA bottom. The workhorse of digital advertising.

```
+-------------------------+
|                         |
|       [ VISUAL ]        |
|                         |
|  Headline Text Here     |
|  Short and punchy       |
|                         |
|     [ CTA Button ]      |
|              brand.com  |
+-------------------------+
```

- Font size: headline 28-36px, sub 16-18px, CTA 14px
- Visual zone: top 45-55%
- CTA zone: bottom 20%
- Brand mark: bottom-right corner, small

### 160x600 — Wide Skyscraper

Vertical scroll: logo top, visual middle, headline below, CTA at bottom. Long and narrow.

```
+----------+
| [LOGO]   |
|          |
| [VISUAL] |
|          |
| Headline |
| text     |
| here     |
|          |
| [CTA]    |
| brand    |
+----------+
```

- Font size: headline 22-28px, CTA 13px
- Logo zone: top 10%
- Visual zone: 20-55%
- Text zone: 55-80%
- CTA zone: bottom 20%

### 970x250 — Billboard

Hero visual left (40-50%), copy + CTA right. Premium format with room to breathe.

```
+----------------------------------------------------+
|                    |                                 |
|    [ HERO          |  Headline Text                  |
|      VISUAL ]      |  Supporting line                |
|                    |  [ CTA Button ]      [logo]    |
+----------------------------------------------------+
```

- Font size: headline 36-48px, sub 18-20px, CTA 16px
- Split: 40-50% visual / 50-60% text
- Brand mark: bottom-right

### 300x600 — Half Page

Expanded 300x250 with more breathing room. Same structure, more vertical space for visual impact.

```
+-------------------------+
| [logo]                  |
|                         |
|       [ VISUAL ]        |
|       (larger area)     |
|                         |
|  Headline Text Here     |
|  Subline with more      |
|  room to elaborate      |
|                         |
|     [ CTA Button ]      |
|              brand.com  |
+-------------------------+
```

- Font size: headline 32-42px, sub 18-20px, CTA 15px
- Visual zone: 30-55%
- Text zone: 55-80%

---

## CTA Design Rules

The CTA button is the entire purpose of the ad. It must be:

- **Visible.** High contrast against the background. Never blend with the palette.
- **Clear verb.** "Shop Now", "Learn More", "Get Started", "Try Free". Never vague ("Click Here").
- **Consistent.** Same CTA style across all ad sizes in a campaign.
- **Properly sized.** Minimum 36px height on desktop, 44px on mobile (touch target).
- **Bottom-positioned.** CTA goes at the bottom or bottom-right of the ad.

### CTA Sizing by Ad Format

| Format | Button Height | Font Size | Padding |
|---|---|---|---|
| 728x90 | 36px | 13px | 8px 24px |
| 300x250 | 40px | 14px | 10px 28px |
| 160x600 | 36px | 12px | 8px 20px |
| 970x250 | 44px | 15px | 12px 32px |
| 300x600 | 44px | 15px | 12px 32px |
| 320x50 | 30px | 11px | 6px 16px |
| 320x480 | 48px | 16px | 14px 36px |

---

## Border Rule

Every digital ad needs a 1px solid border for definition against white or light page backgrounds:

```css
.ad-container {
    border: 1px solid rgba(0, 0, 0, 0.1);
    /* Ensures the ad boundary is visible against any page background */
}
```

This is an IAB requirement for many ad networks. Always include it.

---

## Batch Workflow — Master to All Sizes

1. **Design the 300x250 first.** It is the most common size and the natural "master" shape for adaptation.
2. **Extract the visual system:** palette, fonts, CTA style, brand position into shared CSS custom properties.
3. **Adapt to horizontal formats (728x90, 970x250):** Rearrange elements into horizontal flow. Reduce headline to single line.
4. **Adapt to vertical formats (160x600, 300x600):** Stack elements vertically. Add breathing room between sections.
5. **Adapt to mobile formats (320x50, 320x100, 320x480):** Scale down aggressively. Mobile interstitial (320x480) gets the most design room.
6. **Audit all sizes together.** View them side by side. Do they look like the same campaign?

---

## Campaign Variant Guide — A/B Testing

Create variants for testing by changing ONE variable at a time:

### Color Variant
Same layout, different accent color on CTA button. Tests which color drives more clicks.

### CTA Text Variant
Same design, different CTA text. "Shop Now" vs "Get 20% Off" vs "Free Shipping".

### Layout Variant
Same content, different arrangement. Headline-first vs visual-first.

### Image Variant
Same layout and text, different hero image or product shot.

**Rule:** Only change ONE element per variant. Changing multiple elements makes test results meaningless.

---

## Font Loading

```css
@font-face {
    font-family: 'BricolageGrotesque';
    src: url('file:///Users/jaypokharna/Desktop/Shared%20Folder/Shared%20Folder/python/claude-skills/canvas-super-creator/skills/canvas-super-creator/canvas-fonts/BricolageGrotesque-Bold.ttf');
    font-weight: 700;
}
@font-face {
    font-family: 'WorkSans';
    src: url('file:///Users/jaypokharna/Desktop/Shared%20Folder/Shared%20Folder/python/claude-skills/canvas-super-creator/skills/canvas-super-creator/canvas-fonts/WorkSans-SemiBold.ttf');
    font-weight: 600;
}
@font-face {
    font-family: 'Outfit';
    src: url('file:///Users/jaypokharna/Desktop/Shared%20Folder/Shared%20Folder/python/claude-skills/canvas-super-creator/skills/canvas-super-creator/canvas-fonts/Outfit-Regular.ttf');
    font-weight: 400;
}
```

---

## Anti-Patterns Specific to Ad Design

- **More than 3 elements.** Headline + visual + CTA. That is the budget. A fourth element clutters.
- **Missing border.** Without the 1px border, ads on white pages look like page content, not ads.
- **Inconsistent CTA across sizes.** If the 300x250 has a red CTA and the 728x90 has a blue one, the campaign is broken.
- **Body text paragraphs.** No ad has room for paragraphs. Not even the 300x600.
- **Tiny CTA buttons.** Under 36px tall on desktop or 44px on mobile = missed clicks.
- **Different fonts per size.** Campaign consistency demands the same typography across all formats.
- **Vague CTA text.** "Click Here" says nothing. "Submit" is hostile. Use action verbs with value.
- **Logos larger than headlines.** The headline sells; the logo brands. Headline > logo in visual weight.
- **Cramming desktop layouts into mobile.** 320x50 gets a headline and CTA. That is it.
- **Forgetting the brand mark.** Every ad needs the brand name or logo, even at tiny sizes.
