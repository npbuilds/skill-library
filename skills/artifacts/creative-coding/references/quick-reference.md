# Creative Coding — Quick Reference


## Quick Reference

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

## Formula / Pseudocode

```
value = 0
amplitude = 1
frequency = 1
for each octave:
  value += amplitude * noise(x * frequency, y * frequency)
  amplitude *= 0.5 (persistence)
  frequency *= 2 (lacunarity)
```

## Formula / Pseudocode

```
warpedX = x + noise(x, y) * warpStrength
warpedY = y + noise(x + 5.2, y + 1.3) * warpStrength
finalValue = noise(warpedX, warpedY)
```

## Formula / Pseudocode

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

## Formula / Pseudocode

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

## Formula / Pseudocode

```
uniform vec2 u_resolution;  // Canvas size
uniform float u_time;       // Elapsed time
uniform vec2 u_mouse;       // Mouse position

void main() {
  vec2 uv = gl_FragCoord.xy / u_resolution;  // Normalize to 0-1
  // ... compute color for this pixel ...
  gl_FragColor = vec4(r, g, b, 1.0);
}
```
