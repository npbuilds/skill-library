# Artifact Taxonomy — Classification of Forge Types

## Primary Archetypes

### Generative — The Living Canvas

Artifacts where code produces visual beauty through algorithms, noise, and controlled randomness.

**Subcategories:**
- **Flow fields** — Particle systems following Perlin/simplex noise vector grids
- **Organic growth** — L-systems, differential growth, space colonization, reaction-diffusion
- **Geometric** — Tessellations, fractals, recursive structures, symmetry systems
- **Textural** — Noise landscapes, domain warping, shader-driven surfaces
- **Swarm** — Boids/flocking, physarum simulation, agent-based emergent patterns
- **Audio-reactive** — Visuals driven by FFT frequency data, beat detection, amplitude

**Typical tech:** p5.js, Canvas 2D, WebGL/GLSL shaders, Web Audio API
**Typical wow moment:** Emergent beauty from simple rules, infinite non-repeating variation

---

### Narrative — The Story Weaver

Artifacts that unfold information, stories, or explanations through paced, sequential experience.

**Subcategories:**
- **Scrollytelling** — Scroll-driven narrative with sticky visualizations and step transitions
- **Branching narrative** — Choice-driven stories with divergent paths and state tracking
- **Progressive reveal** — Content that unveils layer by layer through interaction
- **Explainer** — Complex concepts made tangible through interactive metaphor
- **Timeline** — Temporal narratives with scrubbing, zooming, and contextual detail

**Typical tech:** Scrollama/GSAP ScrollTrigger, View Transitions API, CSS scroll-driven animations, state machines
**Typical wow moment:** The moment understanding clicks — when abstract becomes tangible

---

### Data — The Truth Sculptor

Artifacts that transform raw data into visual insight, ranging from clear charts to data-as-art.

**Subcategories:**
- **Analytical** — Charts, dashboards, comparisons optimized for clarity and decision-making
- **Explorable** — Interactive data landscapes the user navigates and discovers
- **Artistic** — Data encoded as texture, motion, sound, or organic form
- **Relational** — Force-directed graphs, chord diagrams, network visualizations
- **Geographic** — Maps with custom projections, overlays, and spatial narratives
- **Real-time** — Live data streams visualized as flowing, breathing systems

**Typical tech:** D3.js, Canvas (for large datasets), WebGL (for 3D data), CSS Grid (for dashboards)
**Typical wow moment:** Seeing a pattern you couldn't see in the raw numbers

---

### Interactive — The Toymaker

Artifacts built for play, exploration, and direct manipulation. Tools, instruments, and toys.

**Subcategories:**
- **Instruments** — Sound generators, visual synthesizers, creative tools
- **Configurators** — Build-your-own experiences with real-time preview
- **Physics toys** — Draggable, throwable, stackable objects with realistic physics
- **Spatial interfaces** — 3D navigation, depth-based UI, zoomable canvases
- **Drawing/painting** — Creative tools with brushes, effects, and export

**Typical tech:** Canvas 2D, WebGL, Web Audio API, Pointer Events, spring physics
**Typical wow moment:** "I can DO things" — the moment agency clicks

---

### Simulation — The World Builder

Artifacts that model systems — physical, biological, social, or abstract.

**Subcategories:**
- **Particle systems** — Gravity, collision, attraction/repulsion, fluid dynamics
- **Cellular automata** — Conway's Life, Langton's Ant, custom rule sets
- **Ecosystem** — Predator-prey, evolution, resource competition
- **Physics** — Rigid body, soft body, cloth, fluid, verlet integration
- **Agent-based** — Autonomous entities with local rules producing global behavior
- **Climate/weather** — Atmospheric, terrain erosion, water flow

**Typical tech:** WebGL compute, Canvas 2D, requestAnimationFrame loops, spatial hashing
**Typical wow moment:** Emergence — complex behavior from simple rules

---

### Immersive — The Atmosphere Smith

Full-sensory experiences designed to envelop. Mood and environment are the primary medium.

**Subcategories:**
- **Atmospheric** — Mood pieces with ambient visuals, sound, and slow motion
- **Spatial** — 3D environments to explore, virtual galleries, architectural spaces
- **Cinematic** — Scroll or time-driven visual sequences with filmic pacing
- **Meditative** — Calming, repetitive, breathing-pace experiences designed to soothe
- **Confrontational** — Deliberately uncomfortable, challenging, or provocative experiences

**Typical tech:** Three.js, WebGL, GSAP, Web Audio API, fullscreen API
**Typical wow moment:** Losing track of time — full immersion

---

## Hybrid Patterns

Most ambitious artifacts combine archetypes. Common hybrids:

| Hybrid | Example |
|--------|---------|
| Narrative + Data | Scrollytelling data story |
| Generative + Interactive | User-controlled flow field |
| Simulation + Data | Live ecosystem with population graphs |
| Immersive + Narrative | Scroll-driven atmospheric story |
| Interactive + Generative | Musical instrument that paints |
| Data + Simulation | Agent-based model visualizing real data |

When classifying hybrids, identify the **primary** archetype (the one that defines the core experience) and **supporting** archetypes (the ones that enrich it).

---

## Classification Signals

| User says... | Likely archetype |
|-------------|-----------------|
| "visualize", "chart", "dashboard", "graph", "metrics" | Data |
| "generative", "procedural", "algorithmic", "random", "organic" | Generative |
| "story", "explain", "scroll", "reveal", "timeline" | Narrative |
| "play", "toy", "instrument", "tool", "drag", "build" | Interactive |
| "simulate", "model", "physics", "ecosystem", "particles" | Simulation |
| "mood", "atmosphere", "ambient", "cinematic", "immersive" | Immersive |
| "surprise me", "something cool", "blow my mind" | Hybrid (Artificer's choice) |
