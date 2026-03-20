# Remotion Bridge — Connecting canvas-super-creator with remotion-super-creator

When remotion-super-creator needs a static graphic element (thumbnail, title card, background frame, social preview), it can invoke canvas-super-creator skills.

## Bridge Patterns

### Thumbnail for Video
Remotion needs a YouTube thumbnail for the video it just created:
→ Invoke `canvas-super-creator:thumbnail-design` with the video's title, palette, and mood

### Title Card Background
Remotion needs a static background for a title card scene:
→ Invoke `canvas-super-creator:html-design` at the video's resolution (e.g., 1920x1080)
→ Use the same palette and typography pairing as the video

### Social Media Preview Card
After video creation, generate matching social media cards:
→ Invoke `canvas-super-creator:social-media-design` for Instagram/LinkedIn/Twitter previews

### Brand Identity for Video
Video needs a logo or brand mark:
→ Invoke `canvas-super-creator:brand-assets` for logo mark

### Ad Campaign Graphics
Video needs matching display ads:
→ Invoke `canvas-super-creator:ad-campaign-design` for multi-size banner set

## Visual Consistency Rules

When generating graphics for a video project:
1. Use the **SAME palette** as the video
2. Use the **SAME typography pairing** as the video
3. Maintain the **SAME mood/aesthetic**
4. Reference the video's **creative brief** if one was created by creative-director

## Invocation Pattern

From remotion-super-creator context:
```
Skill tool → canvas-super-creator:thumbnail-design
Skill tool → canvas-super-creator:social-media-design
Skill tool → canvas-super-creator:html-design
Skill tool → canvas-super-creator:ad-campaign-design
```

## Shared Resources

Both plugins share design philosophy:
- Color palettes are compatible (canvas-super-creator has 25 palettes; remotion has 26)
- Typography pairings overlap (both use bundled Google Fonts)
- Anti-slop checklist principles apply to both static and motion design
- Creative-director agent can write briefs that serve both static and video deliverables
