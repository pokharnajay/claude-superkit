#!/usr/bin/env python3
"""
Instagram Carousel Generator — Claude SuperKit Series
5 posts × 5 slides = 25 images at 1080×1080px
"""

import os
from pathlib import Path
from playwright.sync_api import sync_playwright

FONTS_DIR = Path("/Users/jaypokharna/.claude/skills/canvas-design/canvas-fonts")
OUT_DIR = Path("/Users/jaypokharna/Desktop/Shared Folder/Shared Folder/python/claude-skills/posts/instagram/assets")
OUT_DIR.mkdir(exist_ok=True)

# Claude brand palette — slightly lifted for brightness & shine
BG      = "#1C1A18"   # warm charcoal (claude.com bg — keep deep)
BG2     = "#2E2B28"   # card surface — lifted for contrast (was #242220)
BG3     = "#353230"   # alt card — lifted (was #2A2826)
ACCENT  = "#E0844E"   # claude orange — more vivid/saturated (was #D97849)
ACCENT2 = "#EDD0AA"   # lighter warm peach — brighter (was #E8C09A)
WHITE   = "#FAFAF7"   # near-pure white — max brightness (was #F5F0EB)
GRAY    = "#807B76"   # lifted warm gray (was #6B6762)
LGRAY   = "#C6C1BB"   # bright body text (was #AEA9A3)
BORDER  = "#403D37"   # more visible border (was #333028)

def ff(name, file, weight="normal", style="normal"):
    p = FONTS_DIR / file
    return f"@font-face{{font-family:'{name}';src:url('file://{p}');font-weight:{weight};font-style:{style};}}"

# Gloock = closest match to Claude's display serif
# InstrumentSans = closest match to Claude's UI sans
# GeistMono = closest to Claude's mono labels
FONTS = "\n".join([
    ff("Gloock",  "Gloock-Regular.ttf"),
    ff("ISans",   "InstrumentSans-Regular.ttf"),
    ff("ISans",   "InstrumentSans-Bold.ttf",    weight="bold"),
    ff("GMono",   "GeistMono-Regular.ttf"),
    ff("GMono",   "GeistMono-Bold.ttf",         weight="bold"),
    ff("ISerif",  "InstrumentSerif-Regular.ttf"),
    ff("ISerif",  "InstrumentSerif-Italic.ttf", style="italic"),
])

def asterisk(size=40, color=ACCENT, op=1.0):
    return f"""<svg width="{size}" height="{size}" viewBox="0 0 48 48" fill="none"
      xmlns="http://www.w3.org/2000/svg" style="opacity:{op};flex-shrink:0;">
      <line x1="24" y1="3"  x2="24" y2="45" stroke="{color}" stroke-width="3.5" stroke-linecap="round"/>
      <line x1="3"  y1="13" x2="45" y2="35" stroke="{color}" stroke-width="3.5" stroke-linecap="round"/>
      <line x1="45" y1="13" x2="3"  y2="35" stroke="{color}" stroke-width="3.5" stroke-linecap="round"/>
    </svg>"""

def accentbar(w=72):
    return f'<div style="width:{w}px;height:3px;background:linear-gradient(90deg,{ACCENT},{ACCENT2});border-radius:2px;box-shadow:0 0 14px rgba(224,132,78,0.55);"></div>'

def tag(text):
    return f'<span style="font-family:GMono;font-size:11px;color:{ACCENT};letter-spacing:2.2px;text-transform:uppercase;text-shadow:0 0 16px rgba(224,132,78,0.45);">{text}</span>'

def render(html, filename):
    path = OUT_DIR / filename
    with sync_playwright() as p:
        br = p.chromium.launch()
        pg = br.new_page(viewport={"width":1080,"height":1080})
        pg.set_content(html)
        pg.wait_for_timeout(500)
        pg.screenshot(path=str(path), clip={"x":0,"y":0,"width":1080,"height":1080})
        br.close()
    print(f"  ✓ {filename}")

# ── shared shell ─────────────────────────────────────────────────────────────

def shell(body, pn, sn, total=5, warm=False):
    # Warm cover gradient matches claude.com dark with slight orange undertone
    grad = f"background:linear-gradient(135deg,#221a10 0%,{BG} 62%);" if warm else f"background:{BG};"
    return f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
{FONTS}
*{{margin:0;padding:0;box-sizing:border-box;}}
html,body{{width:1080px;height:1080px;overflow:hidden;background:{BG};}}
.c{{width:1080px;height:1080px;{grad}position:relative;overflow:hidden;
    display:flex;flex-direction:column;padding:72px 88px 64px;}}
.deco{{position:absolute;pointer-events:none;}}
</style></head><body><div class="c">
  <!-- deco: large ghosted asterisk top-right (claude brand signature) -->
  <div class="deco" style="top:-28px;right:-28px;opacity:.18;transform:rotate(10deg);">
    {asterisk(200,ACCENT,1)}</div>
  <div class="deco" style="bottom:-40px;left:-20px;opacity:.09;transform:rotate(-15deg);">
    {asterisk(160,ACCENT,1)}</div>
  <!-- warm spotlight — light source from upper-right -->
  <div class="deco" style="inset:0;background:radial-gradient(ellipse 70% 55% at 80% 10%,
       rgba(224,132,78,0.10) 0%,transparent 65%);pointer-events:none;"></div>
  <!-- subtle vignette edge (very light) -->
  <div class="deco" style="inset:0;background:radial-gradient(ellipse 110% 110% at 50% 50%,
       transparent 55%,rgba(0,0,0,.10) 100%);pointer-events:none;"></div>

  <!-- top bar -->
  <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:0;position:relative;z-index:1;">
    <div style="display:flex;align-items:center;gap:16px;">
      {tag("Building with Claude")}
      <span style="width:1px;height:12px;background:{BORDER};display:inline-block;"></span>
      <span style="font-family:GMono;font-size:11px;color:{GRAY};letter-spacing:.5px;">
        0{pn}/05 &nbsp;·&nbsp; {sn}/{total}</span>
    </div>
    <div style="display:flex;align-items:center;gap:7px;">
      {asterisk(17,ACCENT,0.95)}
      <span style="font-family:GMono;font-size:11px;color:{ACCENT};letter-spacing:2px;text-shadow:0 0 16px rgba(224,132,78,0.5);">CLAUDE</span>
    </div>
  </div>

  <!-- content -->
  <div style="flex:1;display:flex;flex-direction:column;justify-content:center;position:relative;z-index:1;">
    {body}
  </div>

  <!-- bottom bar -->
  <div style="display:flex;align-items:center;justify-content:space-between;position:relative;z-index:1;">
    <div style="width:40px;height:1px;background:{BORDER};"></div>
    <span style="font-family:GMono;font-size:10px;color:{LGRAY};letter-spacing:2px;">CLAUDE SUPERKIT</span>
    <div style="width:40px;height:1px;background:{BORDER};"></div>
  </div>
</div></body></html>"""

# helpers
def h1(txt, size=80):
    return f'<p style="font-family:Gloock;font-size:{size}px;line-height:1.06;color:{WHITE};letter-spacing:-0.5px;text-shadow:0 2px 48px rgba(250,250,247,0.12);">{txt}</p>'

def h2(txt, size=52):
    return f'<p style="font-family:Gloock;font-size:{size}px;line-height:1.1;color:{WHITE};">{txt}</p>'

def body_text(txt, size=18, color=None):
    c = color or LGRAY
    return f'<p style="font-family:ISans;font-size:{size}px;color:{c};line-height:1.65;">{txt}</p>'

def italic_pull(txt, size=24):
    return f'<p style="font-family:ISerif;font-size:{size}px;color:{ACCENT2};font-style:italic;line-height:1.4;">{txt}</p>'

def card(content, accent_left=False):
    border = f"border-left:4px solid {ACCENT};" if accent_left else f"border:1px solid {BORDER};"
    radius = "border-radius:0 8px 8px 0;" if accent_left else "border-radius:8px;"
    shadow = f"box-shadow:0 0 28px rgba(217,120,73,0.09);" if accent_left else ""
    return f'<div style="padding:22px 26px;background:{BG2};{border}{radius}{shadow}">{content}</div>'

def pill_row(*items):
    """items = list of (label, desc)"""
    rows = ""
    for label, desc in items:
        rows += f"""
        <div style="display:flex;align-items:flex-start;gap:20px;padding:18px 22px;
                    background:{BG2};border-left:4px solid {ACCENT};border-radius:0 8px 8px 0;
                    box-shadow:0 0 20px rgba(217,120,73,0.07);">
          <span style="font-family:GMono;font-size:11px;color:{ACCENT};letter-spacing:1.5px;
                       min-width:84px;padding-top:2px;text-transform:uppercase;">{label}</span>
          <span style="font-family:ISans;font-size:16px;color:{LGRAY};line-height:1.5;">{desc}</span>
        </div>"""
    return f'<div style="display:flex;flex-direction:column;gap:10px;">{rows}</div>'

def steps(*items):
    rows = ""
    for i, (n, desc) in enumerate(items):
        bg = BG3 if i % 2 == 0 else BG2
        rows += f"""
        <div style="display:flex;align-items:center;gap:20px;padding:17px 22px;
                    background:{bg};border-radius:8px;">
          <span style="font-family:GMono;font-size:26px;color:{ACCENT};opacity:.82;min-width:44px;">{n}</span>
          <span style="font-family:ISans;font-size:16px;color:{LGRAY};line-height:1.45;">{desc}</span>
        </div>"""
    return f'<div style="display:flex;flex-direction:column;gap:8px;">{rows}</div>'

def stat_row(*pairs):
    cols = ""
    for i, (num, label) in enumerate(pairs):
        sep = f"border-right:1px solid {BORDER};" if i < len(pairs)-1 else ""
        cols += f"""
        <div style="flex:1;{sep}display:flex;flex-direction:column;align-items:center;gap:8px;padding:20px 0;">
          <p style="font-family:Gloock;font-size:56px;color:{ACCENT};text-shadow:0 0 40px rgba(224,132,78,0.50);">{num}</p>
          <p style="font-family:GMono;font-size:11px;color:{LGRAY};letter-spacing:1.8px;">{label}</p>
        </div>"""
    return f'<div style="display:flex;background:{BG2};border-radius:10px;">{cols}</div>'

def swipe_cta(text="SWIPE →"):
    return f'<span style="font-family:GMono;font-size:12px;color:{ACCENT};letter-spacing:2.5px;">{text}</span>'

# ═══════════════════════════════════════════════════════════════════════════════
# POST 1 — THE DISCOVERY
# ═══════════════════════════════════════════════════════════════════════════════

def p1s1():
    b = f"""<div style="display:flex;flex-direction:column;gap:38px;">
      {accentbar(84)}
      {h1("My jaw<br>dropped<br>when I<br>found this.", 82)}
      {body_text("I'd been using Claude for months.<br>Thought I knew everything it could do.")}
      {swipe_cta()}
    </div>"""
    render(shell(b,1,1,warm=True), "post-1-slide-1.png")

def p1s2():
    b = f"""<div style="display:flex;flex-direction:column;gap:36px;">
      {accentbar(60)}
      <div style="display:flex;flex-direction:column;gap:14px;">
        {tag("Then I found this.")}
        {h2("Claude has<br>a plugin system.", 60)}
      </div>
      {body_text("Here's what I didn't know —<br>Claude has a built-in extension framework.<br>One install away from an entirely new capability.")}
      {italic_pull("This changes everything.", 22)}
    </div>"""
    render(shell(b,1,2), "post-1-slide-2.png")

def p1s3():
    b = f"""<div style="display:flex;flex-direction:column;gap:36px;">
      {accentbar(60)}
      {h2("Three layers.<br>One system.", 54)}
      {pill_row(
        ("Plugin",  "One install — Claude gains an entirely new domain of capability"),
        ("Skills",  "Custom instructions that teach Claude exactly how to execute complex tasks"),
        ("Agents",  "Autonomous AI specialists that spin up, take ownership, and get things done"),
      )}
    </div>"""
    render(shell(b,1,3), "post-1-slide-3.png")

def p1s4():
    b = f"""<div style="display:flex;flex-direction:column;gap:40px;">
      {accentbar(60)}
      {h2("Think of it like<br>hiring a new employee.", 50)}
      {card(f"""
        <div style="display:flex;flex-direction:column;gap:10px;">
          {body_text("One command and they're in.", WHITE)}
          {body_text("Already trained. Already specialised. Ready to work.", LGRAY, )}
        </div>""", accent_left=True)}
      {italic_pull("Stack enough of them and Claude stops being a chatbot.<br>It becomes a system.", 22)}
    </div>"""
    render(shell(b,1,4), "post-1-slide-4.png")

def p1s5():
    b = f"""<div style="display:flex;flex-direction:column;gap:40px;">
      {accentbar(60)}
      {h2("What if I built<br>something actually<br>powerful myself?", 50)}
      {body_text("I went down a rabbit hole reading other people's plugins.<br>A thought hit me — something <em style='color:{WHITE};'>production-grade</em>.")}
      {card(f"""
        <div style="display:flex;flex-direction:column;gap:6px;">
          {body_text("I had no idea what I was getting myself into.", LGRAY)}
          <span style="font-family:GMono;font-size:12px;color:{ACCENT};letter-spacing:2px;margin-top:4px;">PART 2 NEXT →</span>
        </div>""")}
    </div>"""
    render(shell(b,1,5), "post-1-slide-5.png")

# ═══════════════════════════════════════════════════════════════════════════════
# POST 2 — THE FIRST BUILD
# ═══════════════════════════════════════════════════════════════════════════════

def p2s1():
    b = f"""<div style="display:flex;flex-direction:column;gap:38px;">
      {accentbar(84)}
      {h1("I decided<br>to build my<br>own Claude<br>skill.", 80)}
      {body_text("I had no idea what I was getting into.")}
      {swipe_cta()}
    </div>"""
    render(shell(b,2,1,warm=True), "post-2-slide-1.png")

def p2s2():
    b = f"""<div style="display:flex;flex-direction:column;gap:36px;">
      {accentbar(60)}
      {tag("What is a skill?")}
      {h2("Just a<br>markdown file.", 62)}
      {card(f"""
        <div style="display:flex;flex-direction:column;gap:10px;">
          {body_text("A set of instructions that tells Claude exactly how to behave when you invoke it.", LGRAY)}
          {italic_pull("Simple in theory. Humbling in practice.", 22)}
        </div>""", accent_left=True)}
      {body_text("That's it. That's the whole thing.", GRAY)}
    </div>"""
    render(shell(b,2,2), "post-2-slide-2.png")

def p2s3():
    b = f"""<div style="display:flex;flex-direction:column;gap:36px;">
      {accentbar(60)}
      {h2("My first one broke.<br>Then I fixed it,<br>and it broke again.", 48)}
      {body_text("Then I finally ran it — and Claude used it perfectly.")}
      {card(f"""
        <div style="display:flex;flex-direction:column;gap:8px;">
          {body_text("That moment felt like magic.", WHITE)}
          {italic_pull("Not because it was complex.<br>Because <em style='font-style:normal;color:{WHITE};'>I</em> built it. And it worked.", 20)}
        </div>""", accent_left=True)}
    </div>"""
    render(shell(b,2,3), "post-2-slide-3.png")

def p2s4():
    b = f"""<div style="display:flex;flex-direction:column;gap:32px;">
      {accentbar(60)}
      {h2("What I learned<br>building skill #1", 52)}
      {pill_row(
        ("Format",   "The format matters more than you think"),
        ("Context",  "Vague instructions give vague results — be specific"),
        ("Agents",   "They're not optional — they're what make skills feel alive"),
        ("Start",    "You don't need 10 skills. One working one changes everything"),
      )}
    </div>"""
    render(shell(b,2,4), "post-2-slide-4.png")

def p2s5():
    b = f"""<div style="display:flex;flex-direction:column;gap:40px;">
      {accentbar(60)}
      {h2("I built one.<br>Tested it obsessively.<br>Broke it on purpose.", 48)}
      {body_text("I didn't build 16 skills that week.<br>I built <em style='color:{WHITE};'>one</em>. And slowly started to see what was actually possible.")}
      {card(f"""
        <div style="display:flex;flex-direction:column;gap:6px;">
          {italic_pull("Then a thought hit me — what if I went bigger?", 21)}
          <span style="font-family:GMono;font-size:12px;color:{ACCENT};letter-spacing:2px;margin-top:4px;">PART 3 NEXT →</span>
        </div>""")}
    </div>"""
    render(shell(b,2,5), "post-2-slide-5.png")

# ═══════════════════════════════════════════════════════════════════════════════
# POST 3 — THE COMPOUNDING EFFECT
# ═══════════════════════════════════════════════════════════════════════════════

def p3s1():
    b = f"""<div style="display:flex;flex-direction:column;gap:38px;">
      {accentbar(84)}
      {h1("First skill:<br>3 days.<br>Second:<br>3 hours.", 80)}
      {italic_pull("By the fifth — I was in flow.", 24)}
      {swipe_cta()}
    </div>"""
    render(shell(b,3,1,warm=True), "post-3-slide-1.png")

def p3s2():
    b = f"""<div style="display:flex;flex-direction:column;gap:36px;">
      {accentbar(60)}
      {h2("The first one<br>is the hard part.<br>After that,<br>you can't stop.", 50)}
      {card(f"""
        <div style="display:flex;flex-direction:column;gap:8px;">
          {body_text("I use Airtable every day at work.", WHITE)}
          {body_text("So I wrote a skill for it. Then one for fields.<br>One for records. One for webhooks.", LGRAY)}
        </div>""", accent_left=True)}
    </div>"""
    render(shell(b,3,2), "post-3-slide-2.png")

def p3s3():
    b = f"""<div style="display:flex;flex-direction:column;gap:36px;">
      {accentbar(60)}
      {tag("Skill #5 — the realisation")}
      {h2("These skills<br>needed to talk<br>to each other.", 52)}
      {body_text("That's when <em style='color:{ACCENT2};font-family:ISerif;font-style:italic;'>agents</em> finally clicked for me.")}
      {italic_pull("Not just skills that do one thing — but specialists that own an entire domain and route work intelligently.", 20)}
    </div>"""
    render(shell(b,3,3), "post-3-slide-3.png")

def p3s4():
    b = f"""<div style="display:flex;flex-direction:column;gap:36px;">
      {accentbar(60)}
      {h2("One orchestrator.<br>Multiple specialists.<br>Each one an expert<br>in exactly one thing.", 46)}
      {pill_row(
        ("Orchestrator", "Routes the work — knows who to call and when"),
        ("Specialists",  "Own a full domain — fields, records, webhooks, views"),
        ("Together",     "A coordinated system, not a collection of one-trick tools"),
      )}
    </div>"""
    render(shell(b,3,4), "post-3-slide-4.png")

def p3s5():
    b = f"""<div style="display:flex;flex-direction:column;gap:36px;">
      {accentbar(60)}
      {h2("Airtable<br>Super Creator", 62)}
      {stat_row(("16","SKILLS"),("8","AGENTS"),("1","SUITE"))}
      {card(f"""
        <div style="display:flex;flex-direction:column;gap:6px;">
          {body_text("I didn't set out to build a Super Creator.", LGRAY)}
          {italic_pull("I set out to solve my own problems. One skill at a time.", 20)}
          <span style="font-family:GMono;font-size:12px;color:{ACCENT};letter-spacing:2px;margin-top:4px;">PART 4 NEXT →</span>
        </div>""")}
    </div>"""
    render(shell(b,3,5), "post-3-slide-5.png")

# ═══════════════════════════════════════════════════════════════════════════════
# POST 4 — I TAUGHT AI TO DESIGN
# ═══════════════════════════════════════════════════════════════════════════════

def p4s1():
    b = f"""<div style="display:flex;flex-direction:column;gap:38px;">
      {accentbar(84)}
      {h1("I still<br>couldn't make<br>Claude create<br>something<br>beautiful.", 72)}
      {swipe_cta()}
    </div>"""
    render(shell(b,4,1,warm=True), "post-4-slide-1.png")

def p4s2():
    b = f"""<div style="display:flex;flex-direction:column;gap:36px;">
      {accentbar(60)}
      {tag("The problem")}
      {h2("Every visual tool<br>produced the same<br>flat, ugly output.", 50)}
      {card(f"""
        <div style="display:flex;flex-direction:column;gap:8px;">
          {body_text("Flat colours. Bad layout.", WHITE)}
          {body_text("Output that looked like clip art from 2008.", LGRAY)}
        </div>""", accent_left=True)}
      {italic_pull("I spent a week trying Python libraries. All of them. All bad.", 21)}
    </div>"""
    render(shell(b,4,2), "post-4-slide-2.png")

def p4s3():
    b = f"""<div style="display:flex;flex-direction:column;gap:36px;">
      {accentbar(60)}
      {tag("The idea")}
      {h2("What if instead<br>of drawing pixels,<br>I wrote HTML<br>and CSS?", 50)}
      {body_text(f"CSS handles gradients, blur, glassmorphism,<br>custom fonts, layered compositions.<br><span style='color:{WHITE};'>Playwright can screenshot any webpage at any resolution.</span>")}
    </div>"""
    render(shell(b,4,3), "post-4-slide-3.png")

def p4s4():
    b = f"""<div style="display:flex;flex-direction:column;gap:32px;">
      {accentbar(60)}
      {h2("The pipeline.", 52)}
      {steps(
        ("01", "Claude writes the design as HTML/CSS"),
        ("02", "Loads from a bundle of 80+ custom fonts"),
        ("03", "Playwright renders and screenshots it"),
        ("04", "Output: a pristine, pixel-perfect PNG"),
      )}
      {body_text("The quality difference was night and day.", WHITE)}
    </div>"""
    render(shell(b,4,4), "post-4-slide-4.png")

def p4s5():
    b = f"""<div style="display:flex;flex-direction:column;gap:40px;">
      {accentbar(60)}
      {h2("Canvas Design", 70)}
      {italic_pull("Born from frustration. Pixel-perfect by design.", 24)}
      {card(f"""
        <div style="display:flex;flex-direction:column;gap:8px;">
          {body_text("Not from a grand plan —<br>from being genuinely frustrated with bad-looking output.", LGRAY)}
          {body_text("Sometimes the best tools come from solving your own problem<br>with whatever works.", WHITE)}
          <span style="font-family:GMono;font-size:12px;color:{ACCENT};letter-spacing:2px;margin-top:4px;">PART 5 NEXT →</span>
        </div>""")}
    </div>"""
    render(shell(b,4,5), "post-4-slide-5.png")

# ═══════════════════════════════════════════════════════════════════════════════
# POST 5 — THE ONE I ALMOST DIDN'T BUILD
# ═══════════════════════════════════════════════════════════════════════════════

def p5s1():
    b = f"""<div style="display:flex;flex-direction:column;gap:38px;">
      {accentbar(84)}
      {h1("I almost<br>didn't build<br>this one.", 82)}
      {body_text("Voice AI felt too complex. Too many moving parts.")}
      {italic_pull("I kept putting it off.", 24)}
      {swipe_cta()}
    </div>"""
    render(shell(b,5,1,warm=True), "post-5-slide-1.png")

def p5s2():
    b = f"""<div style="display:flex;flex-direction:column;gap:36px;">
      {accentbar(60)}
      {h2("Then one day<br>I just started.", 58)}
      {body_text("One skill. Then another.")}
      {card(f"""
        <div style="display:flex;flex-direction:column;gap:8px;">
          {body_text("And I realised —", WHITE)}
          {italic_pull("I'd done this before.<br>Same pattern. Same approach. Different domain.", 21)}
        </div>""", accent_left=True)}
      {pill_row(
        ("Assistant",  "Voice AI config & model setup"),
        ("Webhooks",   "Real-time event handling"),
        ("Squads",     "Multi-agent voice handoffs"),
      )}
    </div>"""
    render(shell(b,5,2), "post-5-slide-2.png")

def p5s3():
    b = f"""<div style="display:flex;flex-direction:column;gap:40px;">
      {accentbar(60)}
      {tag("Three weeks later")}
      {h2("Vapi Super<br>Creator.", 68)}
      {card(f"""
        <div style="display:flex;flex-direction:column;gap:10px;">
          {body_text("An AI that creates production-ready voice agents.", WHITE)}
          {body_text("From first prompt to live phone call —<br>every config validated before it ships.", LGRAY)}
        </div>""", accent_left=True)}
      {italic_pull("Not just voice agents. Production-ready ones.", 21)}
    </div>"""
    render(shell(b,5,3), "post-5-slide-3.png")

def p5s4():
    b = f"""<div style="display:flex;flex-direction:column;gap:36px;">
      {accentbar(60)}
      {h2("Three domains.<br>Same framework.<br>Same pattern.", 52)}
      {pill_row(
        ("Airtable Super Creator", "Database automation — 16 skills, 8 agents"),
        ("Canvas Design",          "AI-powered visual creation — HTML/CSS + Playwright"),
        ("Vapi Super Creator",     "Voice AI, end to end — from prompt to live call"),
      )}
      {italic_pull("Three completely different problems.<br>One way of thinking.", 20)}
    </div>"""
    render(shell(b,5,4), "post-5-slide-4.png")

def p5s5():
    b = f"""<div style="display:flex;flex-direction:column;gap:40px;">
      {accentbar(60)}
      {h2("Claude SuperKit", 68)}
      {italic_pull("One install. Three super-creators. Open source.", 24)}
      {card(f"""
        <div style="display:flex;flex-direction:column;gap:10px;">
          {body_text("This series started with me finding a plugin system<br>I didn't know existed.", LGRAY)}
          {body_text("It ends with me shipping one of my own.", WHITE)}
        </div>""")}
      <div style="padding:16px 24px;border:1px solid {ACCENT};border-radius:8px;display:inline-block;">
        <span style="font-family:GMono;font-size:14px;color:{ACCENT};letter-spacing:.5px;">
          github.com/pokharnajay/claude-superkit</span>
      </div>
    </div>"""
    render(shell(b,5,5), "post-5-slide-5.png")

# ═══════════════════════════════════════════════════════════════════════════════
# RUN
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("Generating 25 Instagram carousel slides (5 posts × 5 slides)…\n")

    print("── Post 1: The Discovery")
    p1s1(); p1s2(); p1s3(); p1s4(); p1s5()

    print("\n── Post 2: The First Build")
    p2s1(); p2s2(); p2s3(); p2s4(); p2s5()

    print("\n── Post 3: The Compounding Effect")
    p3s1(); p3s2(); p3s3(); p3s4(); p3s5()

    print("\n── Post 4: I Taught AI to Design")
    p4s1(); p4s2(); p4s3(); p4s4(); p4s5()

    print("\n── Post 5: The One I Almost Didn't Build")
    p5s1(); p5s2(); p5s3(); p5s4(); p5s5()

    print(f"\n✓ 25 slides → {OUT_DIR}")
