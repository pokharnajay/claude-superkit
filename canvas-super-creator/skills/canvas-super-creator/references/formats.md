# Format Presets Reference

Standard canvas dimensions, safe zones, and typography scales for all supported output formats.

---

## Covers & Banners

| Format | Dimensions (px) | Aspect Ratio | Safe Zone (T/R/B/L px) | Platform Notes |
|---|---|---|---|---|
| GitHub Repository | 1280 x 640 | 2:1 | 60 / 60 / 60 / 60 | Displayed full-width on repo page. Dark mode inverts perceived contrast. Keep text centered vertically. |
| Notion Cover Wide | 1500 x 600 | 5:2 | 40 / 40 / 120 / 40 | Title text overlays bottom-left ~80px up. Avoid placing content in bottom 120px left half. Draggable repositioning crops unpredictably. |
| LinkedIn Personal Banner | 1584 x 396 | 4:1 | 60 / 60 / 60 / 260 | Profile photo overlaps bottom-left corner (~200px circle). Keep left 260px clear of critical content. Mobile crops to center 1080px. |
| LinkedIn Company Banner | 1128 x 191 | 5.9:1 | 30 / 30 / 30 / 30 | Extremely horizontal. Logo overlaps bottom-left on company page. Use horizontal text or simple pattern. |
| YouTube Channel Banner | 2560 x 1440 | 16:9 | 507 / 507 / 509 / 507 | Safe area is centered 1546 x 423. TV displays full image; desktop crops to ~2560x423; mobile crops to ~1546x423. Design critical content within safe area only. |
| Twitter/X Header | 1500 x 500 | 3:1 | 60 / 60 / 60 / 200 | Profile photo overlaps bottom-left ~150px. Mobile crops center. Avoid fine detail that compresses poorly. |

### Cover Typography Scales

| Format | Heading (pt) | Subheading (pt) | Body (pt) | Caption (pt) |
|---|---|---|---|---|
| GitHub Repository | 64 | 36 | 24 | 16 |
| Notion Cover Wide | 56 | 32 | 20 | 14 |
| LinkedIn Personal Banner | 48 | 28 | 18 | 12 |
| LinkedIn Company Banner | 32 | 20 | 14 | 10 |
| YouTube Channel Banner | 72 | 42 | 28 | 18 |
| Twitter/X Header | 52 | 30 | 20 | 14 |

---

## Social Media

| Format | Dimensions (px) | Aspect Ratio | Safe Zone (T/R/B/L px) | Platform Notes |
|---|---|---|---|---|
| Instagram Square | 1080 x 1080 | 1:1 | 50 / 50 / 50 / 50 | Feed display may crop to ~1:1 circle in grid view. High compression; use bold contrast. |
| Instagram Story/Reel | 1080 x 1920 | 9:16 | 200 / 50 / 250 / 50 | Top 200px obscured by story bar (username, time). Bottom 250px obscured by swipe-up/CTA buttons. Critical content lives in middle 1470px band. |
| Instagram Landscape | 1080 x 566 | 1.91:1 | 40 / 40 / 40 / 40 | Less common; feed crops to square preview. Ensure center 566x566 reads well standalone. |
| LinkedIn Post | 1200 x 627 | 1.91:1 | 50 / 50 / 50 / 50 | Feed image. High professional context. Avoid overly casual or meme aesthetics unless intentional. |
| Twitter/X Post | 1600 x 900 | 16:9 | 50 / 50 / 50 / 50 | Timeline crops to ~16:9 preview. Alt text recommended. JPEG compression is aggressive. |
| Facebook Post | 1200 x 630 | ~1.91:1 | 50 / 50 / 50 / 50 | Feed image. News Feed crops vary by device. Test center crop. |
| Pinterest Pin | 1000 x 1500 | 2:3 | 40 / 40 / 40 / 40 | Tall format. Grid display may cut bottom. Place key content in top 2/3. Text overlay performs well. |

### Social Media Typography Scales

| Format | Heading (pt) | Subheading (pt) | Body (pt) | Caption (pt) |
|---|---|---|---|---|
| Instagram Square | 72 | 42 | 28 | 18 |
| Instagram Story/Reel | 80 | 48 | 32 | 20 |
| Instagram Landscape | 56 | 32 | 22 | 14 |
| LinkedIn Post | 64 | 36 | 24 | 16 |
| Twitter/X Post | 64 | 36 | 24 | 16 |
| Facebook Post | 64 | 36 | 24 | 16 |
| Pinterest Pin | 72 | 42 | 28 | 18 |

---

## Posters

| Format | Dimensions (px) | DPI | Safe Zone (T/R/B/L px) | Platform Notes |
|---|---|---|---|---|
| A3 Portrait | 3508 x 4961 | 300 | 120 / 120 / 120 / 120 | 297 x 420 mm. Gallery, event, or promotional use. Bleed area not included; add 3mm (35px) for print bleed. |
| A4 Portrait | 2480 x 3508 | 300 | 80 / 80 / 80 / 80 | 210 x 297 mm. Standard document/flyer. Most common print format. Add 3mm (35px) bleed for print. |
| US Letter | 2550 x 3300 | 300 | 80 / 80 / 80 / 80 | 8.5 x 11 in. North American standard. Add 0.125in (38px) bleed for print. |
| Movie Poster 27x40 | 2700 x 4000 | ~100 | 100 / 100 / 100 / 100 | One-sheet standard. For digital display; print requires higher DPI. Title block typically bottom 25%. |
| Event Poster 11x17 | 3300 x 5100 | 300 | 100 / 100 / 100 / 100 | Tabloid size. Common for concerts, lectures, community events. Bold type at distance. |

### Poster Typography Scales

| Format | Heading (pt) | Subheading (pt) | Body (pt) | Caption (pt) |
|---|---|---|---|---|
| A3 Portrait | 144 | 72 | 36 | 24 |
| A4 Portrait | 96 | 56 | 28 | 18 |
| US Letter | 96 | 56 | 28 | 18 |
| Movie Poster 27x40 | 120 | 64 | 32 | 20 |
| Event Poster 11x17 | 128 | 68 | 34 | 22 |

---

## Thumbnails & Open Graph

| Format | Dimensions (px) | Aspect Ratio | Safe Zone (T/R/B/L px) | Platform Notes |
|---|---|---|---|---|
| YouTube Thumbnail | 1280 x 720 | 16:9 | 50 / 50 / 50 / 50 | Must read at 120x68 in sidebar. Use 3 or fewer words. Faces and high-contrast text perform best. Bottom-right 120x28 obscured by timestamp overlay. |
| Open Graph (OG) | 1200 x 630 | ~1.91:1 | 50 / 50 / 50 / 50 | Used by Slack, Discord, Facebook, Twitter link previews. Some platforms crop to square from center. Ensure 630x630 center reads independently. |

### Thumbnail Typography Scales

| Format | Heading (pt) | Subheading (pt) | Body (pt) | Caption (pt) |
|---|---|---|---|---|
| YouTube Thumbnail | 80 | 48 | 32 | 20 |
| Open Graph (OG) | 64 | 36 | 24 | 16 |

---

## Usage Notes

- **Safe zones** define the minimum margin from each edge where critical content (text, logos, faces) must not appear. Decorative elements may extend into or beyond safe zones.
- **Typography scales** are starting points. Adjust based on text length and visual weight. Fewer words allow larger type.
- **Mobile-first**: most social media is viewed on mobile. Test that text remains legible at 50% scale.
- **Compression**: platforms re-encode uploads. Use high-quality source files. Avoid thin lines under 2px and gradients with subtle transitions (banding risk).
- **Dark mode**: GitHub, Twitter/X, LinkedIn all have dark modes. Test that your design reads in both contexts if possible.
