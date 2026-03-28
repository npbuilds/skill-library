# Performance Guide — Making Artifacts Fast

## The 16ms Budget

At 60fps, each frame has 16.67ms. Budget it:

```
┌──────────────────────────────────────┐
│ Simulation update    ≤ 6ms           │
│ Render               ≤ 8ms           │
│ Browser overhead     ~ 2ms           │
│ Total               = 16ms           │
└──────────────────────────────────────┘
```

If you consistently exceed 16ms, you'll drop below 60fps. Options:
1. Reduce element count
2. Simplify per-element computation
3. Move computation to a Worker or GPU
4. Accept 30fps (target 33ms budget) for visually acceptable results

## Rendering Performance by Technology

### CSS Transforms and Opacity
**Cost:** Cheapest. Runs on the compositor thread. Does not trigger layout or paint.
**Safe properties:** `transform`, `opacity`, `filter`
**Unsafe properties:** `width`, `height`, `top`, `left`, `margin`, `padding` (trigger layout recalculation)
**Rule:** Animate only `transform` and `opacity` for GPU-composited animation.

### Canvas 2D
**Cost:** Moderate. Main thread CPU rendering.
**Optimization tips:**
- Use `requestAnimationFrame`, never `setInterval`
- Minimize `fillStyle`/`strokeStyle` changes (batch by color)
- Use `Path2D` objects for complex shapes (reusable)
- `drawImage()` is fast — pre-render complex elements to offscreen canvas
- `getImageData()`/`putImageData()` is expensive — minimize calls
- For trails: don't `clearRect`. Draw semi-transparent rect instead.

### SVG (via D3 or direct)
**Cost:** Moderate per element, but expensive at scale (each element is a DOM node).
**Limits:** Smooth up to ~5,000 elements. Above that, switch to Canvas.
**Optimization:** Use `<g>` grouping, minimize DOM mutations, batch transitions.

### WebGL (Three.js or raw)
**Cost:** Low per element (GPU-parallel), but setup overhead.
**Optimization tips:**
- Use **instanced meshes** for many identical objects (InstancedMesh, InstancedBufferGeometry)
- Minimize draw calls (merge geometries, use texture atlases)
- Use `BufferGeometry` with typed arrays, not standard Geometry
- Reduce shader complexity where possible
- LOD (Level of Detail): simpler geometry at distance
- Frustum culling: don't render off-screen objects

### WebGPU Compute
**Cost:** Lowest for massive parallelism, but cutting-edge API.
**Use when:** Simulation requires >100K parallel computations per frame.
**Pattern:** Compute shader updates simulation state in GPU buffers. Render pass draws from those buffers. Data never leaves the GPU.

## Memory Management

### Prevent Leaks
```javascript
// BAD: leaking event listeners
element.addEventListener('mousemove', handler);
// element is removed but handler reference keeps it alive

// GOOD: cleanup on removal
const controller = new AbortController();
element.addEventListener('mousemove', handler, { signal: controller.signal });
// Later: controller.abort() removes all listeners
```

### Object Pooling
```javascript
// Instead of: new Particle() each frame, delete when dead
// Use a pool:
const pool = new Array(MAX_PARTICLES).fill(null).map(() => new Particle());
let activeCount = 0;

function emit() {
  if (activeCount < MAX_PARTICLES) {
    pool[activeCount].reset(x, y, vx, vy);
    activeCount++;
  }
}

function removeAt(index) {
  // Swap with last active, decrement count
  [pool[index], pool[activeCount - 1]] = [pool[activeCount - 1], pool[index]];
  activeCount--;
}
```

### Typed Arrays
For large numerical data, use typed arrays instead of regular arrays:
```javascript
// Instead of: const positions = []
const positions = new Float32Array(MAX_PARTICLES * 2); // x,y pairs
// 4x less memory, faster iteration, transferable to Workers/GPU
```

## Web Worker Pattern

For heavy simulation computation:

```javascript
// main.js
const worker = new Worker('sim-worker.js');
const positions = new Float32Array(MAX_PARTICLES * 2);

worker.onmessage = (e) => {
  // Receive updated positions (zero-copy transfer)
  const updated = new Float32Array(e.data);
  renderParticles(updated);
  // Send buffer back for next frame
  worker.postMessage(updated.buffer, [updated.buffer]);
};

// sim-worker.js
self.onmessage = (e) => {
  const positions = new Float32Array(e.data);
  updateSimulation(positions); // Heavy computation here
  self.postMessage(positions.buffer, [positions.buffer]);
};
```

**Key:** Use `Transferable` objects (ArrayBuffer) to avoid copying data between threads.

## Adaptive Quality

Detect performance and adjust:

```javascript
let lastTime = performance.now();
let frameCount = 0;
let fps = 60;

function measureFPS() {
  frameCount++;
  const now = performance.now();
  if (now - lastTime >= 1000) {
    fps = frameCount;
    frameCount = 0;
    lastTime = now;
    adaptQuality(fps);
  }
}

function adaptQuality(currentFPS) {
  if (currentFPS < 30) {
    particleCount = Math.max(MIN_PARTICLES, particleCount * 0.7);
    // Or: reduce canvas resolution
    // Or: simplify per-particle computation
  } else if (currentFPS > 55 && particleCount < MAX_PARTICLES) {
    particleCount = Math.min(MAX_PARTICLES, particleCount * 1.1);
  }
}
```

## Reduced Motion Support

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

```javascript
const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

if (prefersReducedMotion) {
  // Show static version or very slow, simple animation
  // Don't disable functionality — just reduce motion
}
```

## Canvas Resolution for High-DPI

```javascript
function setupHighDPICanvas(canvas, width, height) {
  const dpr = window.devicePixelRatio || 1;
  canvas.width = width * dpr;
  canvas.height = height * dpr;
  canvas.style.width = width + 'px';
  canvas.style.height = height + 'px';
  const ctx = canvas.getContext('2d');
  ctx.scale(dpr, dpr);
  return ctx;
}
```

Without this, Canvas content appears blurry on Retina/HiDPI displays.

## Benchmarking Checklist

Before delivery, verify:
- [ ] Maintains 60fps on target device (or 30fps with acceptable visual quality)
- [ ] No memory growth over time (check with DevTools Memory tab)
- [ ] No jank spikes (check with DevTools Performance tab)
- [ ] Canvas resolution matches device pixel ratio
- [ ] Event listeners cleaned up on teardown
- [ ] Animation stops when tab is not visible (`document.hidden` check)
- [ ] Reduced motion preference respected
- [ ] Mobile performance acceptable (test on real device or throttled CPU)
