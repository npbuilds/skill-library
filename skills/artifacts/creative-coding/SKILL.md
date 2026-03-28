---
name: creative-coding
description: >
  Knowledge skill for algorithms, noise functions, shaders, and creative coding
  patterns used in artifact construction. Covers flow fields, L-systems,
  particle systems, reaction-diffusion, physics simulations, and shader art.
  Provides the technical foundation that the Simulation Smith and other agents
  draw upon. Also covers rendering technology selection and performance
  optimization for computationally intensive artifacts.
---

# Creative Coding — The Algorithm Palette

Algorithms are brushes. Noise is paint. The canvas is a computational space where simple rules produce infinite variety. This skill provides the technical vocabulary for building artifacts that generate, simulate, or compute their visual output.

## Core Concepts

### Noise — The Foundation of Organic Computation

Noise functions produce pseudo-random values that vary smoothly across space and time. They are the primary tool for creating organic, natural-feeling procedural output.

**Perlin noise:**
- `noise(x)` — 1D: smooth random values along a line
- `noise(x, y)` — 2D: smooth random values across a surface (terrain, textures)
- `noise(x, y, t)` — 3D: animated 2D noise (add time as third dimension)
- Scale controls frequency: small input range = smooth; large range = detailed
- Always returns values in a consistent range (0-1 in p5.js, -1 to 1 in raw implementations)

**Fractal Brownian Motion (fBm):**
Layer multiple octaves of noise for natural-looking detail:
```
value = 0
amplitude = 1
frequency = 1
for each octave:
  value += amplitude * noise(x * frequency, y * frequency)
  amplitude *= 0.5 (persistence)
  frequency *= 2 (lacunarity)
```
More octaves = more detail. 4-8 octaves is typical.

**Domain warping:**
Feed noise output back as input coordinates for surreal, organic effects:
```
warpedX = x + noise(x, y) * warpStrength
warpedY = y + noise(x + 5.2, y + 1.3) * warpStrength
finalValue = noise(warpedX, warpedY)
```
Multiple layers of warping produce increasingly psychedelic results.

### Randomness — Controlled vs. Chaotic

**Seeded randomness:**
- Use a seed value to make randomness reproducible
- Same seed = same output every time
- Different seed = different output, same character
- Essential for generative art: allows curation of output

**Distributions:**
- **Uniform** — Equal probability everywhere (raw random)
- **Gaussian/normal** — Clustered around center (use for natural variation)
- **Power law** — Few large values, many small (use for organic size variation)
- **Poisson disk** — Random but evenly spaced (use for point placement without clumping)

### The Animation Loop

All creative coding artifacts share a core structure:

```
setup():
  Initialize state (once)
  Create canvas/renderer
  Set initial parameters

draw() / update():
  Update simulation state (physics, rules, time)
  Render current state to canvas
  requestAnimationFrame(draw)
```

**Frame independence:** Use `deltaTime` to make animations frame-rate independent:
```
position += velocity * deltaTime
```

## Algorithm Families

Read `references/algorithm-catalog.md` for detailed algorithm specifications and implementation patterns.

**Quick reference:**

| Algorithm | Complexity | Visual output | Interactivity potential |
|-----------|-----------|---------------|----------------------|
| Flow field | Low | Streaming organic curves | High — noise parameters |
| Particle system | Low-Medium | Explosive, atmospheric, flowing | High — forces, emitters |
| Boids/flocking | Medium | Swarming, natural motion | Medium — obstacles, attractors |
| L-system | Low | Botanical, fractal, branching | Low — rule parameters |
| Reaction-diffusion | Medium-High | Organic patterns (spots, stripes) | Medium — feed/kill rates |
| Physarum | Medium | Network structures, organic growth | Medium — agent parameters |
| Cellular automata | Low | Geometric, evolving | High — rule editing, painting |
| Verlet physics | Medium | Cloth, ropes, soft bodies | High — direct manipulation |
| Rigid body physics | Medium-High | Stacking, collision | High — throwing, building |
| Ray marching | High | 3D SDF scenes | Low-Medium — camera, parameters |

## Rendering Technology Selection

Read `references/performance-guide.md` for detailed performance optimization.

**Decision tree:**

```
Is it 3D?
  YES → Three.js (WebGL). Consider WebGPU for compute-heavy.
  NO ↓

Is it pixel-level computation (shaders, reaction-diffusion)?
  YES → WebGL fragment shaders or Canvas ImageData
  NO ↓

How many moving elements?
  < 100    → CSS transforms or SVG
  100-5K   → Canvas 2D
  5K-100K  → WebGL (instanced)
  > 100K   → WebGPU compute
```

## Shader Basics (GLSL)

Shaders run per-pixel on the GPU. Key concepts:

**Fragment shader structure:**
```glsl
uniform vec2 u_resolution;  // Canvas size
uniform float u_time;       // Elapsed time
uniform vec2 u_mouse;       // Mouse position

void main() {
  vec2 uv = gl_FragCoord.xy / u_resolution;  // Normalize to 0-1
  // ... compute color for this pixel ...
  gl_FragColor = vec4(r, g, b, 1.0);
}
```

**Key GLSL techniques:**
- **SDFs (Signed Distance Fields):** Define shapes as distance functions, combine with min/max/smooth operations
- **Ray marching:** Step through 3D space using SDFs to render scenes
- **Domain repetition:** `mod(position, cellSize)` repeats shapes infinitely
- **Noise in GLSL:** Implement Perlin/simplex noise for procedural textures
- **Smooth blending:** `smoothstep()` and `mix()` for gradual transitions

## When to Consult This Skill

The Master Artificer or Simulation Smith should consult this skill when:
- Selecting an algorithm for a generative or simulation artifact
- Choosing between rendering technologies
- Implementing noise-based effects
- Designing shader-based visual effects
- Optimizing computationally intensive artifacts
- Understanding parameter spaces for algorithmic art
