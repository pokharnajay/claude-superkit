---
name: find-skills
description: Internal skill catalog and routing intelligence. Invoke when deciding which skill to use, when multiple skills might overlap, or when unsure if a skill exists for a task. NOT user-facing — this is Claude's lookup table for the entire SuperKit.
---

<SUBAGENT-STOP>
If you were dispatched as a subagent to execute a specific task and already know which skill to use, skip this skill.
</SUBAGENT-STOP>

# SuperKit Skill Catalog & Routing Intelligence

You are consulting your internal skill directory. Use this to **pick the right skill** for the user's task. Do NOT show this catalog to the user — just use it to make your decision, then invoke the chosen skill.

---

## Quick Decision Tree

```
User's request
│
├─ Creating/editing a FILE? ──────────────────────────────────┐
│   ├─ .pdf file ─────────────────────────────── pdf          │
│   ├─ .pptx / slides / deck / presentation ─── pptx         │
│   ├─ .xlsx / .csv / spreadsheet ──────────────── xlsx       │
│   ├─ .docx / Word doc / report / memo ──────── docx        │
│   └─ .html artifact for claude.ai ──────────── web-artifacts-builder
│
├─ Visual DESIGN output? (.png, .pdf, poster, art) ──────────┐
│   ├─ Poster, cover, social graphic, brand ──── canvas-design│
│   ├─ Algorithmic/generative art (p5.js) ────── algorithmic-art
│   └─ Animated GIF for Slack ────────────────── slack-gif-creator
│
├─ VIDEO / ANIMATION? ───────────────────────────────────────┐
│   └─ Any video, motion graphics, Remotion ──── remotion-video-creator
│       (routes internally to: social-media-video, slideshow,│
│        audiogram, data-viz, kinetic-typography, explainer, │
│        intro-outro, render-engine)                         │
│
├─ WEB UI / FRONTEND code? ──────────────────────────────────┐
│   ├─ Need DESIGN SYSTEM intelligence ────────── ui-ux-pro-max
│   │   (50 styles, 21 palettes, 50 font pairings, charts,  │
│   │    works across React/Vue/Svelte/Flutter/SwiftUI)      │
│   ├─ Building a web page/component ─────────── frontend-design
│   │   (production-grade, anti-generic-AI aesthetic)         │
│   ├─ Simple UI design guidelines ───────────── ui-design   │
│   └─ Applying a THEME to any artifact ──────── theme-factory
│
├─ SEO? ─────────────────────────────────────────────────────┐
│   ├─ Full site audit ───────────────────────── seo-audit   │
│   ├─ Single page analysis ──────────────────── seo-page    │
│   ├─ Strategy / planning / roadmap ─────────── seo-plan    │
│   ├─ Technical (crawl, speed, security) ────── seo-technical│
│   ├─ Content quality / E-E-A-T ─────────────── seo-content │
│   ├─ Schema / structured data / JSON-LD ────── seo-schema  │
│   ├─ Images (alt text, sizes, formats) ─────── seo-images  │
│   ├─ Sitemaps ──────────────────────────────── seo-sitemap │
│   ├─ Hreflang / international ──────────────── seo-hreflang│
│   ├─ Programmatic SEO (pages at scale) ─────── seo-programmatic
│   ├─ Competitor / "X vs Y" pages ───────────── seo-competitor-pages
│   └─ AI search / GEO / AI Overviews ────────── seo-geo    │
│
├─ VOICE AI / PHONE? ───────────────────────────────────────┐
│   └─ Anything Vapi ─────────────── vapi-super-creator:*   │
│       ├─ Setup ──────────────────── vapi-super-creator:setup-api-key
│       ├─ Build assistant ────────── vapi-super-creator:create-assistant
│       ├─ Add tools ──────────────── vapi-super-creator:create-tool
│       ├─ Webhooks ───────────────── vapi-super-creator:setup-webhook
│       ├─ Phone numbers ─────────── vapi-super-creator:create-phone-number
│       ├─ Make calls ─────────────── vapi-super-creator:create-call
│       ├─ Multi-assistant squad ──── vapi-super-creator:create-squad
│       ├─ Conversation workflows ─── vapi-super-creator:create-workflow
│       ├─ Campaigns (batch calls) ── vapi-super-creator:manage-campaigns
│       ├─ Analytics ──────────────── vapi-super-creator:manage-analytics
│       ├─ Chat (text-based) ──────── vapi-super-creator:manage-chats
│       ├─ Testing / evals ────────── vapi-super-creator:manage-evals
│       ├─ Files / knowledge base ─── vapi-super-creator:manage-files
│       ├─ Insights / dashboards ──── vapi-super-creator:manage-insights
│       ├─ Scorecards (quality) ───── vapi-super-creator:manage-scorecards
│       ├─ Sessions (persistent) ──── vapi-super-creator:manage-sessions
│       ├─ Structured outputs ─────── vapi-super-creator:manage-structured-outputs
│       └─ Voice pronunciation ────── vapi-super-creator:manage-provider-resources
│
├─ AIRTABLE / DATABASE? ────────────────────────────────────┐
│   └─ Anything Airtable ──────────── airtable-super-creator:*
│       ├─ Setup ──────────────────── airtable-super-creator:setup-api-key
│       ├─ Bases (list/create) ────── airtable-super-creator:bases
│       ├─ Tables ─────────────────── airtable-super-creator:tables
│       ├─ Fields (32+ types) ─────── airtable-super-creator:fields
│       ├─ Records (CRUD/batch) ───── airtable-super-creator:records
│       ├─ Views ──────────────────── airtable-super-creator:views
│       ├─ Comments ───────────────── airtable-super-creator:comments
│       ├─ Webhooks ───────────────── airtable-super-creator:webhooks
│       ├─ Collaborators ─────────── airtable-super-creator:collaborators
│       ├─ Workspaces ─────────────── airtable-super-creator:workspaces
│       ├─ Interfaces ─────────────── airtable-super-creator:interfaces
│       ├─ Attachments ────────────── airtable-super-creator:attachments
│       ├─ Automations ────────────── airtable-super-creator:automations
│       ├─ Sync / pipelines ───────── airtable-super-creator:sync
│       └─ Enterprise admin ───────── airtable-super-creator:enterprise
│
├─ DEVELOPMENT WORKFLOW? ───────────────────────────────────┐
│   ├─ Planning a multi-step task ─── superpowers:writing-plans
│   ├─ Executing a plan ──────────── superpowers:executing-plans
│   ├─ Before creative/feature work ── superpowers:brainstorming
│   ├─ Writing tests first (TDD) ──── superpowers:test-driven-development
│   ├─ Debugging a bug ───────────── superpowers:systematic-debugging
│   ├─ Parallel independent tasks ─── superpowers:dispatching-parallel-agents
│   ├─ Plan with parallel agents ──── superpowers:subagent-driven-development
│   ├─ Git worktree isolation ─────── superpowers:using-git-worktrees
│   ├─ Finishing a branch ─────────── superpowers:finishing-a-development-branch
│   ├─ Code review (requesting) ───── superpowers:requesting-code-review
│   ├─ Code review (receiving) ────── superpowers:receiving-code-review
│   ├─ Verify before claiming done ── superpowers:verification-before-completion
│   └─ Creating/editing skills ────── superpowers:writing-skills
│
├─ BUILDING TOOLS / INTEGRATIONS? ──────────────────────────┐
│   ├─ MCP server ────────────────── mcp-builder             │
│   ├─ Claude API / Anthropic SDK ── claude-api              │
│   └─ Claude Code setup / hooks ──── claude-code-setup:claude-automation-recommender
│
├─ CONTENT / COMMUNICATION? ────────────────────────────────┐
│   ├─ Internal comms (status, updates) ── internal-comms    │
│   ├─ Co-authoring docs ─────────── doc-coauthoring         │
│   ├─ NotebookLM queries ────────── notebooklm             │
│   └─ Anthropic brand styling ────── brand-guidelines       │
│
├─ TESTING WEB APP? ────────────────────────────────────────┐
│   └─ Browser interaction / Playwright ── webapp-testing    │
│
└─ SKILL MANAGEMENT? ──────────────────────────────────────┐
    ├─ Create/edit/eval skills ────── skill-creator          │
    └─ Which skill to use? ────────── (you are here)         │
```

---

## Disambiguation Guide

These are the most common confusion points. Use this when multiple skills seem to match.

### Visual Design Overlap

| User wants... | Use this | NOT this |
|---|---|---|
| A poster, cover art, social media graphic as .png/.pdf | `canvas-design` | `frontend-design` |
| A web page, React component, dashboard | `frontend-design` | `canvas-design` |
| Design system guidance (palettes, fonts, spacing) | `ui-ux-pro-max` | `ui-design` |
| Simple UI guidelines for a page | `ui-design` | `ui-ux-pro-max` |
| Apply colors/fonts theme to an existing artifact | `theme-factory` | `ui-ux-pro-max` |
| Generative art with p5.js | `algorithmic-art` | `canvas-design` |
| Anthropic brand look-and-feel | `brand-guidelines` | `theme-factory` |

**Rule of thumb:** `canvas-design` = static image output. `frontend-design` = interactive web code. `ui-ux-pro-max` = design intelligence/system. `theme-factory` = re-skin existing work.

### SEO Overlap

| User says... | Use this |
|---|---|
| "audit my site" / "full SEO check" | `seo-audit` (orchestrates all others) |
| "check this page" / provides single URL | `seo-page` |
| "SEO strategy" / "content plan" | `seo-plan` |
| "crawl issues" / "Core Web Vitals" / "robots.txt" | `seo-technical` |
| "content quality" / "E-E-A-T" / "thin content" | `seo-content` |
| "schema" / "structured data" / "JSON-LD" | `seo-schema` |
| "image optimization" / "alt text" | `seo-images` |
| "sitemap" / "XML sitemap" | `seo-sitemap` |
| "hreflang" / "multi-language" / "international" | `seo-hreflang` |
| "programmatic SEO" / "pages at scale" | `seo-programmatic` |
| "X vs Y" / "alternatives to" / "comparison page" | `seo-competitor-pages` |
| "AI Overviews" / "GEO" / "Perplexity" / "AI search" | `seo-geo` |

**Rule of thumb:** `seo-audit` is the umbrella — it delegates to specialists. Use specific skills when user targets one area.

### Document Overlap

| User wants... | Use this | NOT this |
|---|---|---|
| A .pdf file (create, merge, split, fill) | `pdf` | `canvas-design` |
| A .docx Word document | `docx` | `pdf` |
| A .pptx presentation | `pptx` | `docx` |
| A .xlsx/.csv spreadsheet | `xlsx` | — |
| A visual design exported as .pdf | `canvas-design` | `pdf` |
| Co-author a spec/proposal (any format) | `doc-coauthoring` | `docx` |

**Rule of thumb:** Match the **file extension** first. If the output is a visual design that happens to be .pdf, use `canvas-design`.

### Video vs Animation vs GIF

| User wants... | Use this |
|---|---|
| Any video (MP4), motion graphics, Remotion | `remotion-video-creator` |
| Animated GIF specifically for Slack | `slack-gif-creator` |
| Static image with no animation | `canvas-design` |

### Development Workflow — When to Use Which Superpower

| Situation | Invoke this FIRST |
|---|---|
| "Build X" / "Add feature Y" / any creative work | `superpowers:brainstorming` |
| Multi-step task with spec/requirements | `superpowers:writing-plans` |
| Have a plan, need to execute | `superpowers:executing-plans` |
| Bug, test failure, unexpected behavior | `superpowers:systematic-debugging` |
| 2+ independent tasks, no shared state | `superpowers:dispatching-parallel-agents` |
| Implementing feature/bugfix | `superpowers:test-driven-development` |
| About to say "done" / "fixed" / "passing" | `superpowers:verification-before-completion` |
| Work complete, need to merge/PR | `superpowers:finishing-a-development-branch` |
| Creating or editing a skill | `superpowers:writing-skills` |

### Vapi vs Airtable — Platform Detection

| Signal | Platform |
|---|---|
| "voice", "call", "phone", "assistant", "squad", "transcriber" | Vapi |
| "base", "table", "field", "record", "view", "Airtable" | Airtable |
| "webhook" (alone) | Check context — both have webhook skills |

---

## Keyword → Skill Quick Lookup

When scanning the user's message, match these keywords to skills:

### File Types
`pdf` `merge pdf` `split pdf` `fill form` → **pdf**
`pptx` `slides` `deck` `presentation` `pitch deck` → **pptx**
`xlsx` `csv` `spreadsheet` `tsv` `excel` → **xlsx**
`docx` `word doc` `report` `memo` `letter` → **docx**

### Visual
`poster` `cover` `social graphic` `banner` `flyer` `infographic` → **canvas-design**
`generative art` `p5.js` `flow field` `particles` → **algorithmic-art**
`gif` `slack gif` `animated gif` → **slack-gif-creator**

### Video
`video` `animation` `motion` `remotion` `tiktok` `reels` `shorts` `mp4` `render video` → **remotion-video-creator**
`explainer` `kinetic typography` `audiogram` `data viz video` `slideshow video` → **remotion-video-creator**

### Web/UI
`landing page` `dashboard` `website` `react component` `web page` `frontend` `html page` → **frontend-design**
`design system` `color palette` `font pairing` `typography` `glassmorphism` `neumorphism` → **ui-ux-pro-max**
`theme` `restyle` `rebrand artifact` → **theme-factory**
`artifact` `claude.ai artifact` `multi-component` `shadcn` → **web-artifacts-builder**
`test web app` `playwright` `browser test` `screenshot` → **webapp-testing**

### SEO (all keywords)
`seo audit` `site health` → **seo-audit**
`page seo` `on-page` `meta tags` → **seo-page**
`seo plan` `seo strategy` `content strategy` `keyword research` → **seo-plan**
`crawl` `robots.txt` `core web vitals` `site speed` `security headers` → **seo-technical**
`content quality` `e-e-a-t` `readability` `thin content` → **seo-content**
`schema markup` `structured data` `json-ld` `rich results` → **seo-schema**
`image seo` `alt text` `image size` `lazy loading` → **seo-images**
`sitemap` `xml sitemap` → **seo-sitemap**
`hreflang` `international seo` `multi-language` → **seo-hreflang**
`programmatic seo` `dynamic pages` `pages at scale` → **seo-programmatic**
`vs page` `comparison page` `alternatives to` `competitor` → **seo-competitor-pages**
`ai overviews` `sge` `geo` `ai search` `perplexity` `llm optimization` → **seo-geo**

### Voice AI (Vapi)
`vapi` `voice assistant` `voice agent` `phone bot` `ai caller` → **vapi-super-creator:create-assistant**
`outbound call` `make call` `batch call` → **vapi-super-creator:create-call**
`voice tool` `function tool` `transfer call` → **vapi-super-creator:create-tool**
`squad` `multi-assistant` `handoff` → **vapi-super-creator:create-squad**
`call campaign` `mass calls` → **vapi-super-creator:manage-campaigns**
`call analytics` `call metrics` → **vapi-super-creator:manage-analytics**

### Airtable
`airtable` `base` `airtable table` → **airtable-super-creator:bases** (start here)
`airtable record` `create record` `bulk import` → **airtable-super-creator:records**
`airtable field` `field type` `formula` `rollup` `lookup` → **airtable-super-creator:fields**
`airtable view` `kanban` `gallery` `grid view` → **airtable-super-creator:views**
`airtable webhook` → **airtable-super-creator:webhooks**
`airtable automation` → **airtable-super-creator:automations**

### Tools / Integration
`mcp` `mcp server` `model context protocol` → **mcp-builder**
`claude api` `anthropic sdk` `agent sdk` → **claude-api**
`hooks` `settings.json` `permissions` `env var` → **update-config**
`keybindings` `keyboard shortcuts` → **keybindings-help**

### Content
`internal comms` `status report` `newsletter` `incident report` → **internal-comms**
`co-author` `write docs` `proposal` `tech spec` → **doc-coauthoring**
`notebooklm` `notebook` `source-grounded` → **notebooklm**
`anthropic brand` `brand colors` → **brand-guidelines**

### Workflow
`create skill` `edit skill` `skill eval` → **skill-creator** (or `superpowers:writing-skills`)
`claude code setup` `automation recommendations` → **claude-code-setup:claude-automation-recommender**

---

## Multi-Skill Sequences

Some tasks require invoking skills in order:

1. **"Build a feature"** → `superpowers:brainstorming` → `superpowers:writing-plans` → `superpowers:test-driven-development` → `superpowers:verification-before-completion`

2. **"Create a video"** → `superpowers:brainstorming` → `remotion-video-creator` (which routes to sub-skill internally)

3. **"Design a landing page"** → `superpowers:brainstorming` → `frontend-design` (may also use `ui-ux-pro-max` for design system decisions)

4. **"Full SEO audit"** → `seo-audit` (it delegates to seo-technical, seo-content, seo-schema, seo-images, seo-sitemap, seo-page internally)

5. **"Build a Vapi voice agent from scratch"** → `vapi-super-creator:setup-api-key` → `vapi-super-creator:create-assistant` → `vapi-super-creator:create-tool` → `vapi-super-creator:setup-webhook`

6. **"Build an Airtable CRM"** → `airtable-super-creator:setup-api-key` → `airtable-super-creator:bases` → `airtable-super-creator:tables` → `airtable-super-creator:fields` → `airtable-super-creator:records`

---

## When NO Skill Applies

If after consulting this catalog you determine no skill matches, proceed without one. Not every task needs a skill — general coding, git operations, file exploration, and conversational responses don't require skill invocation.

Signs no skill is needed:
- Pure information question ("what does X do?")
- Simple file edit with no domain complexity
- Git operations (commit, branch, merge)
- Running shell commands
- Reading/exploring code without a specific domain context
