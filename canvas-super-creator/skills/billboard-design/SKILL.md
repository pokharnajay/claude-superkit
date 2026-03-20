---
name: billboard-design
description: Highway billboards, bus shelter ads, transit ads, and large-format outdoor advertising. Use when user asks for a billboard, outdoor ad, transit ad, or bus shelter design.
license: MIT
metadata:
  author: canvas-super-creator
  version: 4.0.0
---

# Billboard Design — Large-Format Outdoor Advertising

Create high-impact outdoor advertising for highways, transit shelters, bus wraps, and digital LED displays. Billboards are the most constrained design medium: you have 3 seconds, 7 words, and one idea.

---

## Format Quick Reference

| Format | Dimensions (px) | Aspect | Viewing Distance |
|---|---|---|---|
| Bulletin (14x48 ft) | 4800 x 1400 | 3.4:1 | 500+ ft, highway speed |
| Poster (10.5x22.8 ft) | 2460 x 1230 | 2:1 | 300-500 ft, arterial roads |
| Bus Shelter (4x6 ft) | 1380 x 2010 | ~2:3 | 5-15 ft, pedestrian |
| Bus King (2.5x12 ft) | 900 x 4320 | 4.8:1 | 10-50 ft, traffic |
| Digital LED (varies) | 1400 x 400 | 3.5:1 | 200-500 ft, highway |

**Full details:** Read `./canvas-super-creator/references/formats.md` for safe zones and bleed areas.

---

## Workflow

1. **Read references:**
   - `./canvas-super-creator/references/formats.md` — dimensions, safe zones, bleed
   - `./canvas-super-creator/references/color-palettes.md` — palette selection
   - `./canvas-super-creator/references/typography-pairings.md` — font pairing
   - `./canvas-super-creator/references/composition-guide.md` — layout technique
   - `./canvas-super-creator/references/anti-slop-checklist.md` — quality gates
   - `./html-design/references/css-techniques.md` — CSS technique catalog
   - `./billboard-design/references/billboard-patterns.md` — billboard-specific recipes

2. **Output specification** with format, palette, typography, composition, mood

3. **Create design philosophy** — billboards demand ruthless simplicity and brutal clarity

4. **Design with html-design patterns** — follow the 4-phase process

5. **Render via render-engine** pipeline

---

## The 3-Second Rule

A billboard is viewed from a moving vehicle at 55-65 mph. You get exactly 3 seconds:

- **Maximum 7 words.** This is not a guideline — it is a hard ceiling. Count them. If you have 8, cut one.
- **One visual element.** A single image, icon, or graphic. Not two. Not a collage.
- **One CTA.** A phone number, URL, or single action. "Exit 42" or "Call 555-0100" or "Open Sundays".
- **Zero paragraphs.** If there is body text on a billboard, the design has failed.

### The Billboard Equation

```
Billboard = 1 Headline + 1 Visual + 1 CTA
```

Nothing more. Every additional element halves effectiveness.

---

## Viewing Distance Typography

Billboard type must be legible from extreme distances. This changes every assumption about font sizing:

| Viewing Distance | Minimum Font Size | Use Case |
|---|---|---|
| 500+ ft (highway) | 200px+ | Bulletin headline |
| 300-500 ft (arterial) | 150px+ | Poster headline |
| 100-300 ft (approach) | 80px+ | Secondary text, CTA |
| 10-50 ft (bus/shelter) | 48px+ | Bus shelter headline |
| 5-15 ft (pedestrian) | 28px+ | Bus shelter body |

### Typography Rules

- **Sans-serif only for headlines.** Serifs lose definition at distance. Use heavy-weight sans-serif: BigShoulders, WorkSans 700, Boldonse.
- **Minimum weight: 600.** Thin fonts vanish against sky, buildings, and competing visual noise.
- **Tight tracking at large sizes.** Letter-spacing of -0.02em to -0.04em for display text.
- **ALL CAPS for highways.** Mixed case is harder to read at speed and distance.
- **No script fonts.** Ever. They are illegible at distance and speed.

### Font Loading

```css
@font-face {
    font-family: 'BigShoulders';
    src: url('file:///Users/jaypokharna/Desktop/Shared%20Folder/Shared%20Folder/python/claude-skills/canvas-super-creator/skills/canvas-super-creator/canvas-fonts/BigShouldersDisplay-Bold.ttf');
    font-weight: 700;
}
@font-face {
    font-family: 'WorkSans';
    src: url('file:///Users/jaypokharna/Desktop/Shared%20Folder/Shared%20Folder/python/claude-skills/canvas-super-creator/skills/canvas-super-creator/canvas-fonts/WorkSans-Bold.ttf');
    font-weight: 700;
}
```

---

## High-Contrast Outdoor Colors

Billboards compete with sunlight, sky, trees, buildings, and other signs. Color contrast is survival:

| Combination | Visibility Rating | Notes |
|---|---|---|
| Yellow on Black | 94% | Highest visibility. Warning/urgency. |
| White on Blue | 91% | Professional, authoritative. |
| White on Red | 89% | Urgent, retail, food. |
| White on Green | 88% | Natural, health, directions. |
| Black on Yellow | 87% | Bold, construction, caution. |
| Black on White | 84% | Clean, modern, minimal. |
| Red on White | 78% | Attention-grabbing, sales. |

### Color Rules

- **Never use light-on-light.** Cream on white, light blue on light gray — invisible at 300 feet.
- **Never use dark-on-dark.** Navy on black, dark green on charcoal — same problem.
- **Minimum contrast ratio: 7:1.** Higher than web accessibility standards because viewing conditions are hostile.
- **Limit palette to 2-3 colors max.** Background + text + accent. That is the budget.
- **Saturated colors carry farther.** Muted pastels disappear against real-world backgrounds.

---

## The 3-Element Maximum

Every billboard has exactly three elements. Period.

1. **Headline** — the message, 7 words or fewer
2. **Visual** — one image, icon, logo, or product shot
3. **CTA** — one actionable element (URL, phone, exit number, brand name)

### Layout Priority

```
+--------------------------------------------------+
|                                                    |
|   [ VISUAL ]        HEADLINE                      |
|                     Big, Bold, Brief               |
|                                                    |
|                              CTA ──→ bottom-right  |
+--------------------------------------------------+
```

The visual anchors. The headline delivers. The CTA directs.

---

## Billboard-Specific CSS Techniques

### Extreme Font Sizes

Billboard headlines must be enormous. This is not poster scale — it is architecture scale:

```css
.billboard-headline {
    font-family: 'BigShoulders', sans-serif;
    font-size: 280px;
    font-weight: 700;
    line-height: 0.9;
    letter-spacing: -0.03em;
    text-transform: uppercase;
    color: var(--fg);
}
.billboard-cta {
    font-family: 'WorkSans', sans-serif;
    font-size: 64px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: var(--accent);
}
```

### Ultra-Simplified Layouts

Billboard layouts use absolute positioning with massive margins. Content hugs edges or centers:

```css
body {
    --bg: #000000;
    --fg: #FFFFFF;
    --accent: #FFD700;
    position: relative;
    background: var(--bg);
}
.content {
    position: absolute;
    top: 0; left: 0; width: 100%; height: 100%;
    display: flex;
    align-items: center;
    padding: 80px 120px;
    z-index: 3;
}
```

### Dramatic Negative Space

Billboards need air. At least 30-40% of the canvas should be empty:

```css
.headline-zone {
    position: absolute;
    top: 50%;
    transform: translateY(-50%);
    right: 120px;
    max-width: 55%;
    z-index: 4;
}
/* Left 45% is visual or pure negative space */
```

### Solid Background for LED Displays

Digital LED boards have poor gradient reproduction. Use flat colors:

```css
body {
    background: #002855; /* Solid, saturated */
}
/* No gradients, no subtle blends — LEDs dither them into noise */
```

---

## Composition for Billboards

Billboards are extreme horizontals (Bulletin at 3.4:1) or moderate verticals (Bus Shelter at 2:3). This demands specific composition approaches:

### Horizontal Billboards (Bulletin, Bus King, Digital LED)

- **Left-to-right flow:** Visual left → Headline center → CTA right. Follows reading direction.
- **Asymmetric split:** 40/60 or 60/40. Never 50/50 — it creates static tension with no focal point.
- **Horizon line:** Keep primary content in the center 60% of height. Top and bottom 20% are often obscured by frame, structure, or viewing angle.

### Vertical Billboards (Bus Shelter)

- **Top-down flow:** Headline top → Visual center → CTA bottom.
- **Eye-level zone:** On a bus shelter, content at 3-5 feet height gets the most attention (pedestrian eye level).
- **Bottom 15% caution:** Bus shelter frames, snow, grime, and posters often obscure the very bottom.

---

## Anti-Patterns Specific to Billboards

- **More than 7 words.** If you are counting and it is 8, you have already failed. Cut.
- **Font size under 80px on a Bulletin.** It is invisible at highway speed. Period.
- **Complex layouts.** More than 3 elements means the viewer processes none of them.
- **Subtle gradients.** In direct sunlight, gentle color transitions wash out completely.
- **Script or decorative fonts.** Illegible at any distance over 50 feet.
- **Body text or paragraphs.** Nobody reads paragraphs at 65 mph.
- **Low-contrast color pairs.** Light gray on white, navy on black — invisible outdoors.
- **Centered-everything on horizontal formats.** Horizontal billboards need directional flow, not static center stacks.
- **Busy photographic backgrounds.** If the background image has detail, the text on top is unreadable.
- **QR codes.** On a highway billboard at 500 feet? No.
