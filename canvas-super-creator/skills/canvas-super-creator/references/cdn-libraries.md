# Available CDN Libraries — Complete Reference Catalog

These libraries can be loaded in HTML files rendered via Playwright for screenshot capture. Since we take static screenshots, the key technique is **pausing animations at a specific frame** before capturing.

---

## 1. p5.js — Generative Art

**CDN URL:**
```html
<script src="https://cdnjs.cloudflare.com/ajax/libs/p5.js/1.9.4/p5.min.js"></script>
```

**What it does:** Creative coding library for generative art — particles, flow fields, noise landscapes, geometric patterns, data visualization.

**Example — Flow Field:**
```html
<!DOCTYPE html>
<html>
<head>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/p5.js/1.9.4/p5.min.js"></script>
  <style>
    body { margin: 0; overflow: hidden; }
    canvas { display: block; }
  </style>
</head>
<body>
<script>
let particles = [];
const NUM = 500;
const SCALE = 20;
let cols, rows;

function setup() {
  createCanvas(1200, 675);
  cols = floor(width / SCALE);
  rows = floor(height / SCALE);
  for (let i = 0; i < NUM; i++) {
    particles.push(createVector(random(width), random(height)));
  }
  background(15, 15, 30);

  // Run simulation for N frames then stop
  for (let frame = 0; frame < 200; frame++) {
    drawFrame();
  }
  noLoop(); // Stop — ready for screenshot
}

function drawFrame() {
  for (let p of particles) {
    let angle = noise(p.x / SCALE * 0.1, p.y / SCALE * 0.1, frameCount * 0.005) * TWO_PI * 2;
    let vel = p5.Vector.fromAngle(angle).mult(1.5);
    stroke(
      map(p.x, 0, width, 100, 255),
      map(p.y, 0, height, 50, 200),
      200,
      15
    );
    strokeWeight(1);
    point(p.x, p.y);
    p.add(vel);
    if (p.x < 0 || p.x > width || p.y < 0 || p.y > height) {
      p.set(random(width), random(height));
    }
  }
}

function draw() {}
</script>
</body>
</html>
```

**Playwright screenshot technique:**
```js
// p5 uses noLoop() to stop. Wait for canvas to be ready:
await page.waitForFunction(() => {
  const canvas = document.querySelector('canvas');
  return canvas && canvas.width > 0;
});
// Optional: wait a moment for rendering to finish
await page.waitForTimeout(500);
await page.screenshot({ path: 'output.png' });
```

**Common p5 recipes:**
- Particle systems: `for` loop + `createVector` + noise-based velocity
- Flow fields: 2D noise grid → angle → particle movement
- Geometric patterns: `for` loops + `rotate()` + `polygon()`
- Gradient backgrounds: pixel-level `set()` or overlapping shapes

---

## 2. Three.js — 3D Backgrounds

**CDN URL:**
```html
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
```

**What it does:** 3D rendering library. Use for particle spheres, abstract 3D shapes, terrain meshes, and cinematic 3D backgrounds.

**Example — Particle Sphere:**
```html
<!DOCTYPE html>
<html>
<head>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
  <style>body { margin: 0; overflow: hidden; background: #0a0a0a; }</style>
</head>
<body>
<script>
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, 1200/675, 0.1, 1000);
const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
renderer.setSize(1200, 675);
renderer.setPixelRatio(2);
document.body.appendChild(renderer.domElement);

// Create particle sphere
const geometry = new THREE.BufferGeometry();
const count = 5000;
const positions = new Float32Array(count * 3);
const colors = new Float32Array(count * 3);

for (let i = 0; i < count; i++) {
  const phi = Math.acos(2 * Math.random() - 1);
  const theta = Math.random() * Math.PI * 2;
  const r = 3 + Math.random() * 0.5;
  positions[i * 3] = r * Math.sin(phi) * Math.cos(theta);
  positions[i * 3 + 1] = r * Math.sin(phi) * Math.sin(theta);
  positions[i * 3 + 2] = r * Math.cos(phi);
  colors[i * 3] = 0.3 + Math.random() * 0.7;
  colors[i * 3 + 1] = 0.5 + Math.random() * 0.5;
  colors[i * 3 + 2] = 1.0;
}

geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
geometry.setAttribute('color', new THREE.BufferAttribute(colors, 3));

const material = new THREE.PointsMaterial({
  size: 0.03,
  vertexColors: true,
  transparent: true,
  opacity: 0.8
});

const points = new THREE.Points(geometry, material);
scene.add(points);

camera.position.z = 6;

// Rotate to a specific angle (no animation loop needed)
points.rotation.x = 0.3;
points.rotation.y = 0.8;

renderer.render(scene, camera);

// Signal ready for screenshot
window.__THREE_READY__ = true;
</script>
</body>
</html>
```

**Playwright screenshot technique:**
```js
// Wait for Three.js to finish rendering
await page.waitForFunction(() => window.__THREE_READY__ === true);
await page.screenshot({ path: 'output.png' });
```

---

## 3. Rough.js — Hand-Drawn Style

**CDN URL:**
```html
<script src="https://cdn.jsdelivr.net/npm/roughjs@4.6.6/bundled/rough.js"></script>
```

**What it does:** Renders shapes with a hand-drawn, sketchy appearance. Perfect for whimsical, organic, or draft-style graphics.

**Example — Hand-Drawn Shapes:**
```html
<!DOCTYPE html>
<html>
<head>
  <script src="https://cdn.jsdelivr.net/npm/roughjs@4.6.6/bundled/rough.js"></script>
  <style>body { margin: 0; background: #faf8f5; }</style>
</head>
<body>
<canvas id="canvas" width="1200" height="675"></canvas>
<script>
const rc = rough.canvas(document.getElementById('canvas'));

// Hand-drawn rectangle
rc.rectangle(100, 100, 400, 300, {
  stroke: '#2d3436',
  strokeWidth: 2,
  roughness: 1.5,
  fill: '#dfe6e9',
  fillStyle: 'hachure',
  fillWeight: 1.5,
  hachureAngle: 45,
  hachureGap: 8
});

// Hand-drawn circle
rc.circle(800, 300, 250, {
  stroke: '#e17055',
  strokeWidth: 2.5,
  roughness: 2,
  fill: '#fab1a0',
  fillStyle: 'cross-hatch',
  fillWeight: 1,
  hachureGap: 6
});

// Hand-drawn line
rc.line(150, 500, 1050, 500, {
  stroke: '#636e72',
  strokeWidth: 2,
  roughness: 1.2
});

// Hand-drawn ellipse
rc.ellipse(500, 550, 300, 100, {
  stroke: '#0984e3',
  strokeWidth: 2,
  roughness: 1.8,
  fill: '#74b9ff',
  fillStyle: 'zigzag',
  fillWeight: 1
});

window.__ROUGH_READY__ = true;
</script>
</body>
</html>
```

**Playwright screenshot technique:**
```js
await page.waitForFunction(() => window.__ROUGH_READY__ === true);
await page.screenshot({ path: 'output.png' });
```

**Fill styles available:** `hachure`, `solid`, `zigzag`, `cross-hatch`, `dots`, `dashed`, `zigzag-line`

---

## 4. Anime.js — Animation (Frame Capture)

**CDN URL:**
```html
<script src="https://cdnjs.cloudflare.com/ajax/libs/animejs/3.2.2/anime.min.js"></script>
```

**What it does:** Lightweight animation library. For our screenshot workflow, we create the animation then seek to a specific frame.

**Example — Animated Elements at Specific Frame:**
```html
<!DOCTYPE html>
<html>
<head>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/animejs/3.2.2/anime.min.js"></script>
  <style>
    body { margin: 0; background: #1a1a2e; overflow: hidden; }
    .box {
      width: 60px; height: 60px;
      background: #e94560;
      border-radius: 8px;
      position: absolute;
    }
  </style>
</head>
<body>
<div id="container"></div>
<script>
// Create elements
const container = document.getElementById('container');
for (let i = 0; i < 20; i++) {
  const box = document.createElement('div');
  box.className = 'box';
  box.style.left = (50 + i * 55) + 'px';
  box.style.top = '300px';
  container.appendChild(box);
}

// Create animation
const anim = anime({
  targets: '.box',
  translateY: [-200, 0],
  scale: [0, 1],
  rotate: [180, 0],
  opacity: [0, 1],
  delay: anime.stagger(50),
  duration: 1000,
  easing: 'easeOutElastic(1, 0.5)',
  autoplay: false  // Don't auto-play
});

// Seek to 70% through the animation (where it looks best)
anim.seek(anim.duration * 0.7);

window.__ANIME_READY__ = true;
</script>
</body>
</html>
```

**Playwright screenshot technique:**
```js
await page.waitForFunction(() => window.__ANIME_READY__ === true);
await page.screenshot({ path: 'output.png' });
```

**Key API for frame capture:**
- `autoplay: false` — prevent automatic playback
- `anim.seek(timeInMs)` — jump to exact millisecond
- `anim.seek(anim.duration * 0.5)` — jump to 50% progress
- `anim.seek(anim.duration)` — jump to final state

---

## 5. GSAP — Advanced Animation Timeline

**CDN URL:**
```html
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js"></script>
```

**What it does:** Professional-grade animation with timeline control. Excellent for complex multi-step animations that you want to capture at specific moments.

**Example — Timeline at Specific Progress:**
```html
<!DOCTYPE html>
<html>
<head>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js"></script>
  <style>
    body { margin: 0; background: #0f0f23; overflow: hidden; }
    .card {
      width: 280px; padding: 24px; border-radius: 16px;
      background: rgba(255,255,255,0.08);
      border: 1px solid rgba(255,255,255,0.12);
      position: absolute; color: #fff; font-family: system-ui;
    }
    h2 { margin: 0 0 8px; font-size: 20px; }
    p { margin: 0; opacity: 0.7; font-size: 14px; }
  </style>
</head>
<body>
<div class="card" id="card1" style="left:50px; top:200px;">
  <h2>Design</h2><p>Creative visual systems</p>
</div>
<div class="card" id="card2" style="left:400px; top:200px;">
  <h2>Develop</h2><p>Production-ready code</p>
</div>
<div class="card" id="card3" style="left:750px; top:200px;">
  <h2>Deploy</h2><p>Ship with confidence</p>
</div>

<script>
// Create a paused timeline
const tl = gsap.timeline({ paused: true });

tl.from('#card1', { y: 100, opacity: 0, duration: 0.6, ease: 'power3.out' })
  .from('#card2', { y: 100, opacity: 0, duration: 0.6, ease: 'power3.out' }, '-=0.3')
  .from('#card3', { y: 100, opacity: 0, duration: 0.6, ease: 'power3.out' }, '-=0.3')
  .from('.card h2', { x: -20, opacity: 0, duration: 0.4, stagger: 0.1 }, '-=0.4')
  .from('.card p', { x: -20, opacity: 0, duration: 0.4, stagger: 0.1 }, '-=0.3');

// Jump to specific progress (0 to 1)
tl.progress(1); // fully complete — all elements visible

window.__GSAP_READY__ = true;
</script>
</body>
</html>
```

**Playwright screenshot technique:**
```js
await page.waitForFunction(() => window.__GSAP_READY__ === true);
await page.screenshot({ path: 'output.png' });
```

**Key API for frame capture:**
- `gsap.timeline({ paused: true })` — create paused timeline
- `tl.progress(0.5)` — seek to 50% (0 to 1 range)
- `tl.time(1.5)` — seek to 1.5 seconds
- `tl.seek(label)` — seek to a named label
- `gsap.set(target, { props })` — set without animation (instant)

**GSAP `set()` for static positioning (no animation needed):**
```js
// Position elements exactly where you want them — no timeline needed
gsap.set('#card1', { x: 0, y: 0, opacity: 1, scale: 1 });
gsap.set('#card2', { x: 50, y: 20, opacity: 0.8, rotation: 5 });
```

---

## 6. Chart.js — Data Visualization

**CDN URL:**
```html
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.7/dist/chart.umd.min.js"></script>
```

**What it does:** Beautiful, responsive charts — bar, line, doughnut, radar, polar, scatter, bubble, and more.

**Example — Styled Bar Chart:**
```html
<!DOCTYPE html>
<html>
<head>
  <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.7/dist/chart.umd.min.js"></script>
  <style>
    body { margin: 0; padding: 40px; background: #1a1a2e; }
    canvas { max-width: 1120px; max-height: 595px; }
  </style>
</head>
<body>
<canvas id="chart" width="1120" height="595"></canvas>
<script>
const ctx = document.getElementById('chart').getContext('2d');

const chart = new Chart(ctx, {
  type: 'bar',
  data: {
    labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
    datasets: [{
      label: 'Revenue',
      data: [12, 19, 8, 25, 15, 30],
      backgroundColor: [
        'rgba(102, 126, 234, 0.8)',
        'rgba(118, 75, 162, 0.8)',
        'rgba(240, 147, 251, 0.8)',
        'rgba(245, 87, 108, 0.8)',
        'rgba(255, 217, 61, 0.8)',
        'rgba(107, 203, 119, 0.8)'
      ],
      borderColor: [
        '#667eea', '#764ba2', '#f093fb', '#f5576c', '#ffd93d', '#6bcb77'
      ],
      borderWidth: 2,
      borderRadius: 8,
      borderSkipped: false
    }]
  },
  options: {
    responsive: false,
    animation: false, // Disable animation for instant render
    plugins: {
      legend: {
        labels: { color: '#ffffff', font: { size: 14 } }
      }
    },
    scales: {
      x: {
        ticks: { color: '#888' },
        grid: { color: 'rgba(255,255,255,0.05)' }
      },
      y: {
        ticks: { color: '#888' },
        grid: { color: 'rgba(255,255,255,0.05)' }
      }
    }
  }
});

window.__CHART_READY__ = true;
</script>
</body>
</html>
```

**Playwright screenshot technique:**
```js
await page.waitForFunction(() => window.__CHART_READY__ === true);
await page.screenshot({ path: 'output.png' });
```

**Key configuration for static rendering:**
- `animation: false` — renders chart instantly, no animation to wait for
- `responsive: false` — uses exact canvas dimensions
- Set explicit `width` and `height` on the `<canvas>` element

**Chart types:**
- `bar` / `horizontalBar` — bar charts
- `line` — line/area charts (set `fill: true` for area)
- `doughnut` / `pie` — circular charts
- `radar` — spider/radar charts
- `polarArea` — polar area charts
- `scatter` / `bubble` — point-based charts

---

## General Playwright Screenshot Pattern

For any CDN library, follow this pattern:

```html
<script>
// 1. Create your visual (library-specific)
// 2. If animated: pause or seek to desired frame
// 3. Signal ready:
window.__READY__ = true;
</script>
```

```js
// In Playwright:
await page.goto('file:///path/to/design.html');
await page.waitForFunction(() => window.__READY__ === true, { timeout: 10000 });
await page.screenshot({ path: 'output.png', fullPage: true });
```

### Handling CDN Load Failures
Always add error handling for CDN loads:
```html
<script src="https://cdn.example.com/lib.js"
        onerror="document.body.innerHTML='<p>CDN failed to load</p>'"></script>
```

### Offline Fallback
If CDN is unreliable, use the technique without external libraries — pure CSS/SVG/HTML can achieve most visual effects documented in the other reference files.

### Canvas vs DOM
- **p5.js / Three.js / Chart.js** render to `<canvas>` — Playwright captures these perfectly
- **Rough.js** renders to `<canvas>` or `<svg>` — both work
- **Anime.js / GSAP** animate DOM elements — Playwright captures the current state at screenshot time

### Recommended Canvas Sizes
| Format | Width | Height |
|--------|-------|--------|
| Social (1:1) | 1080 | 1080 |
| Landscape (16:9) | 1200 | 675 |
| Story (9:16) | 1080 | 1920 |
| Banner | 1200 | 400 |
| Open Graph | 1200 | 630 |
