# Algorithm Catalog — Implementation Patterns for Creative Coding

## Flow Fields

**Concept:** A grid of vectors across the canvas. Particles placed on the grid follow the vector at their position, creating organic streaming curves.

**Core algorithm:**
1. Create a grid of vectors (cols = width/scale, rows = height/scale)
2. For each grid cell, compute angle from noise: `angle = noise(x*freq, y*freq, z) * TWO_PI * 2`
3. Convert angle to vector: `Vector.fromAngle(angle)`
4. For each particle: look up the vector at its grid position, add to velocity, update position
5. Draw a line or point at the particle's position (don't clear canvas for trails)
6. Increment z (time offset) slowly each frame for evolution

**Key parameters:**
- `noiseScale` (0.001-0.1): Controls how quickly the field changes spatially. Lower = smoother flows
- `noiseSpeed` (0.001-0.01): How quickly the field evolves over time
- `particleCount` (100-5000): Density of the output
- `particleSpeed` (1-5): How fast particles traverse the field
- `trailAlpha` (0.01-0.1): Background overlay opacity = trail length

**Variations:**
- **Curl noise:** Use the curl of 3D noise for divergence-free flow (particles never converge to a point)
- **Multi-scale:** Layer multiple flow fields at different scales
- **Attractor fields:** Add point attractors/repulsors that distort the flow
- **Image-guided:** Use image brightness to modify noise, creating portraits from flow

---

## Particle Systems

**Concept:** Emitters produce particles with initial properties. Each frame, forces are applied, positions updated, and expired particles removed.

**Core algorithm:**
1. Emitter creates particles with: position, velocity, color, life, size
2. Each frame: apply forces (gravity, wind, attraction, noise), update velocity, update position
3. Decrease life each frame. Remove dead particles.
4. Render each particle (point, circle, line from previous position, sprite)

**Key parameters:**
- `emitRate` (1-100 per frame): How many particles spawn
- `lifespan` (30-300 frames): How long particles live
- `gravity` (0-0.5): Downward acceleration
- `initialVelocity` (1-10): Launch speed (with angle range)
- `drag` (0.95-0.999): Velocity multiplier each frame (friction)

**Force types:**
- **Gravity:** Constant downward force
- **Wind:** Constant directional force (can vary with noise)
- **Attraction:** `force = direction * (strength / distance²)` toward a point
- **Repulsion:** Same as attraction but negated
- **Noise field:** Apply flow field vectors as forces
- **Vortex:** Tangential force around a center point

---

## Boids (Flocking)

**Concept:** Each agent (boid) follows three simple rules based on nearby neighbors. Complex swarm behavior emerges.

**Three rules:**
1. **Separation:** Steer away from nearby boids (avoid crowding)
2. **Alignment:** Steer toward the average heading of nearby boids
3. **Cohesion:** Steer toward the average position of nearby boids

**Neighbor detection:** Only consider boids within a perception radius and field of view angle.

**Key parameters:**
- `perceptionRadius` (30-100px): How far each boid can see
- `separationWeight` (1-3): How strongly boids avoid each other
- `alignmentWeight` (0.5-2): How strongly boids match direction
- `cohesionWeight` (0.5-2): How strongly boids group together
- `maxSpeed` (2-8): Speed limit
- `maxForce` (0.1-0.5): Steering force limit (higher = snappier turns)

**Performance:** Naive neighbor check is O(n²). Use spatial hashing for >200 boids:
- Divide space into grid cells of size = perceptionRadius
- Only check neighbors in same and adjacent cells

---

## Reaction-Diffusion (Gray-Scott Model)

**Concept:** Two chemicals (A and B) diffuse across a grid at different rates. A feeds B's growth, B inhibits itself. The interplay produces organic patterns.

**Core equations (per cell, per timestep):**
```
A' = A + (dA * laplacian(A) - A*B*B + f*(1-A)) * dt
B' = B + (dB * laplacian(B) + A*B*B - (k+f)*B) * dt
```

**Key parameters:**
- `f` (feed rate, 0.01-0.08): Rate at which A is replenished
- `k` (kill rate, 0.045-0.07): Rate at which B dies off
- `dA` (1.0): Diffusion rate of A
- `dB` (0.5): Diffusion rate of B (must be less than dA)

**Pattern map (f, k values):**
- Spots: f=0.035, k=0.065
- Stripes: f=0.025, k=0.06
- Spirals: f=0.014, k=0.054
- Labyrinth: f=0.029, k=0.057
- Mitosis (splitting dots): f=0.028, k=0.062

**Implementation:** Use two buffers (current and next), swap each frame. Compute the Laplacian using a 3x3 convolution kernel.

---

## L-Systems

**Concept:** Start with an axiom string. Apply production rules to rewrite it N times. Interpret the final string as drawing instructions.

**Turtle graphics interpretation:**
- `F` = move forward and draw
- `f` = move forward without drawing
- `+` = turn right by angle
- `-` = turn left by angle
- `[` = push position/angle to stack
- `]` = pop position/angle from stack

**Classic examples:**
- **Fractal plant:** Axiom: `X`, Rules: `X→F+[[X]-X]-F[-FX]+X`, `F→FF`, Angle: 25°
- **Koch curve:** Axiom: `F`, Rules: `F→F+F-F-F+F`, Angle: 90°
- **Sierpinski:** Axiom: `F-G-G`, Rules: `F→F-G+F+G-F`, `G→GG`, Angle: 120°
- **Dragon curve:** Axiom: `FX`, Rules: `X→X+YF+`, `Y→-FX-Y`, Angle: 90°

**Stochastic L-systems:** Multiple rules for the same symbol, chosen randomly. Produces natural variation between runs.

---

## Physarum (Slime Mold)

**Concept:** Thousands of agents move on a 2D canvas, depositing chemical trails. Each agent senses the trail ahead and steers toward the strongest concentration. Trails diffuse and evaporate over time.

**Agent behavior (per frame):**
1. **Sense:** Read trail values at three sensor positions (ahead-left, ahead, ahead-right)
2. **Rotate:** Turn toward the strongest signal (or random if equal)
3. **Move:** Step forward by move speed
4. **Deposit:** Add to the trail map at current position

**Trail behavior (per frame):**
1. **Diffuse:** Average each cell with its neighbors (box blur)
2. **Evaporate:** Multiply all values by decay factor (0.9-0.99)

**Key parameters:**
- `sensorAngle` (22.5°-45°): Angle between sensors
- `sensorDistance` (5-20px): How far ahead agents look
- `turnSpeed` (15°-90°): Maximum rotation per frame
- `moveSpeed` (1-3px): Forward speed
- `depositAmount` (1-5): Trail strength deposited
- `decayFactor` (0.9-0.99): Trail evaporation rate

**Implementation:** Trail map is a 2D float array (or texture in WebGL). Rendering = draw trail map as grayscale (or color-mapped) image.

---

## Cellular Automata

**Concept:** A grid of cells, each in one of N states. Every cell updates simultaneously based on its neighbors' states.

**Conway's Game of Life:**
- 2 states: alive (1), dead (0)
- Rules: alive with 2-3 neighbors → stays alive. Dead with exactly 3 → becomes alive. All else → dead.

**Beyond Life:**
- **Elementary (1D):** 8 possible 3-cell neighborhoods → 256 possible rule sets (Wolfram rules)
- **Multi-state:** More than 2 states create richer patterns
- **Continuous:** Values between 0-1 instead of discrete states (SmoothLife)
- **Custom rules:** Define your own neighbor count → state transitions

**Rendering:** Each cell is a pixel. Update a 2D array, render to Canvas ImageData.

---

## Verlet Integration (Physics)

**Concept:** Simulate physics using position-based dynamics. Store current and previous position; velocity is implicit.

**Core update:**
```
newPosition = currentPosition + (currentPosition - previousPosition) + acceleration * dt²
previousPosition = currentPosition
currentPosition = newPosition
```

**Constraints:** After updating positions, enforce constraints:
- **Distance constraint:** Two points must maintain a fixed distance (rods, rope links)
- **Pin constraint:** A point is fixed in space (anchor)
- **Collision constraint:** Points must stay outside/inside boundaries

**Iterate constraints** 3-5 times per frame for stability.

**Use for:** Cloth simulation, rope/chain, soft bodies, ragdoll, bridge builders

---

## Performance Patterns

**Spatial hashing (for neighbor queries):**
```
cellSize = perception radius
hash(x, y) = (floor(x/cellSize), floor(y/cellSize))
Only check entities in same and adjacent cells
```
Reduces O(n²) neighbor checks to near O(n).

**Object pooling (for particles):**
Don't create/destroy particles. Maintain a pool. "Dead" particles are recycled with new properties.

**Double buffering:**
For grid-based simulations (reaction-diffusion, cellular automata), use two arrays. Read from one, write to the other. Swap each frame.

**Web Worker offloading:**
Move simulation logic to a Worker thread. Send updated positions/colors to main thread via transferable ArrayBuffer. Main thread only renders.
