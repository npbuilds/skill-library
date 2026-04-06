# Master Artificer Research Report
## Comprehensive Research on Advanced Web Artifact Techniques

*Compiled: 2026-03-25*

---

## Table of Contents

1. [Advanced Web Artifact Techniques](#1-advanced-web-artifact-techniques)
2. [Creative Coding and Generative Art](#2-creative-coding-and-generative-art)
3. [Data Visualization as Art](#3-data-visualization-as-art)
4. [Interactive Narrative and Experience Design](#4-interactive-narrative-and-experience-design)
5. [Micro-interactions and UX Delight](#5-micro-interactions-and-ux-delight)
6. [AI-Assisted Creative Tools](#6-ai-assisted-creative-tools)
7. [Cross-Cutting Principles](#7-cross-cutting-principles)

---

## 1. Advanced Web Artifact Techniques

### 1.1 CSS Houdini and Custom Paint Worklets

**What it is:** The CSS Painting API (part of CSS Houdini) lets developers write JavaScript functions that draw directly into an element's background, border, or content. Worklets run off the main thread for high performance.

**Key Techniques:**
- Register worklets via `CSS.paintWorklet.addModule()` with a two-step process
- Use `inputProperties` to specify which CSS properties (including custom properties) feed into the worklet
- Create custom backgrounds with patterns, gradients, and complex textures generated on the fly
- Build interactive borders that change based on user input (hover effects, etc.)
- Use CSS custom properties for themeable designs without multiple image assets

**Performance:** Worklets are painted off the main thread by the browser rendering engine, making them extremely performant.

**Resource:** [Houdini.how](https://web.dev/articles/houdini-how) provides a library of ready-to-use paint worklets.

**Code Pattern (Paint Worklet):**
```javascript
// my-paint.js
class MyPainter {
  static get inputProperties() { return ['--my-color', '--my-size']; }
  paint(ctx, size, properties) {
    const color = properties.get('--my-color').toString();
    const s = parseInt(properties.get('--my-size'));
    ctx.fillStyle = color;
    // Draw pattern using canvas-like API
    for (let x = 0; x < size.width; x += s) {
      for (let y = 0; y < size.height; y += s) {
        ctx.beginPath();
        ctx.arc(x, y, s/3, 0, Math.PI * 2);
        ctx.fill();
      }
    }
  }
}
registerPaint('my-paint', MyPainter);

// main.js
CSS.paintWorklet.addModule('my-paint.js');
```
```css
.element {
  --my-color: hotpink;
  --my-size: 20;
  background-image: paint(my-paint);
}
```

### 1.2 CSS Scroll-Driven Animations

**What it is:** CSS-native animations tied to scroll position rather than time, eliminating the need for JavaScript scroll listeners. Two timeline types exist: Scroll Progress Timeline (linked to scroll position) and View Progress Timeline (linked to element visibility within a scroll container).

**Key Techniques:**
- `animation-timeline: scroll()` links animation to the nearest scrollable ancestor
- `animation-timeline: view()` triggers animation based on element entering/exiting viewport
- Named scroll timelines via `scroll-timeline-name` for targeting specific scrollers
- `animation-range` to specify exactly when in the scroll/view timeline the animation plays
- Combine with standard `@keyframes` for familiar authoring

**Browser Support (2025-2026):** Chrome (stable since Dec 2024), Firefox (flag-enabled, full support emerging), Safari 26+.

**Performance:** Runs off the main thread, unlike JavaScript-based scroll listeners. No risk of blocking the main thread.

**Code Pattern:**
```css
@keyframes fade-in {
  from { opacity: 0; transform: translateY(50px); }
  to   { opacity: 1; transform: translateY(0); }
}

.card {
  animation: fade-in linear both;
  animation-timeline: view();
  animation-range: entry 0% entry 100%;
}

/* Named scroll timeline */
.scroller {
  scroll-timeline-name: --my-scroller;
  overflow-y: scroll;
}
.progress-bar {
  animation: grow-width linear both;
  animation-timeline: --my-scroller;
}
```

### 1.3 View Transitions API

**What it is:** Native browser API for smooth animated transitions between DOM states (same-document) or between pages (cross-document). Reached Baseline Newly Available in Oct 2025.

**Key Techniques:**
- `document.startViewTransition(callback)` for same-document transitions
- `view-transition-name` CSS property to identify elements that should morph between states
- `view-transition-class` for grouping transition behaviors
- `view-transition-name: match-element` for auto-naming (no manual names needed)
- `::view-transition-old()` and `::view-transition-new()` pseudo-elements for styling
- Scoped view transitions via `element.startViewTransition()` on any HTMLElement (Chrome 140+)

**2025-2026 Developments:**
- React integration moving into `react@canary` for core support
- Multiple simultaneous view transitions via scoped transitions
- Interop 2026 focus area

**Code Pattern:**
```javascript
// Simple view transition
document.startViewTransition(() => {
  // Update the DOM
  container.innerHTML = newContent;
});
```
```css
/* Name elements for morphing */
.card { view-transition-name: card-hero; }

/* Customize the transition animation */
::view-transition-old(card-hero) {
  animation: fade-out 0.3s ease-out;
}
::view-transition-new(card-hero) {
  animation: fade-in 0.3s ease-in;
}
```

### 1.4 CSS Container Queries

**What it is:** Component-level responsive design where elements adapt based on their container's size rather than the viewport. Fully supported in all browsers as of 2025.

**Key Techniques:**
- `container-type: inline-size` to establish containment contexts
- `@container` rules for component-level breakpoints
- Container query length units (`cqw`, `cqh`, `cqi`, `cqb`)
- Combine with media queries: media queries for page-level layout + container queries for component internals

**Best Practice:** Use media queries for page-level concerns (column layouts, dark mode, reduced motion). Use container queries inside components for self-contained adaptive behavior.

**Code Pattern:**
```css
.card-wrapper {
  container-type: inline-size;
  container-name: card;
}

@container card (min-width: 400px) {
  .card { display: grid; grid-template-columns: 1fr 2fr; }
}

@container card (max-width: 399px) {
  .card { display: flex; flex-direction: column; }
}
```

### 1.5 WebGL / Three.js for 3D Artifacts

**What it is:** Real-time 3D rendering in the browser using WebGL (via Three.js as the dominant abstraction).

**Key Techniques:**
- Interactive 3D card scenes using GLB models loaded into Three.js
- Scroll-revealed WebGL galleries syncing Three.js planes with HTML elements (GSAP + Three.js + Barba.js)
- Procedural geometry for generating meshes algorithmically
- Shader-based visual effects (GLSL vertex/fragment shaders)
- Post-processing pipeline (bloom, depth of field, chromatic aberration)
- Integration with DOM via CSS3DRenderer for hybrid 2D/3D experiences

**Performance Best Practices:**
- Use lightweight, optimized assets (Blender decimate modifier, online compressors)
- Reduce polygon count without losing visual quality
- Implement level-of-detail (LOD) systems
- Use instanced meshes for repeated objects
- Leverage GPU instancing and buffer geometry

**Emerging: WebGPU (2025)**
WebGPU is now production-ready for creative applications:
- Compute shaders enable GPU-parallel simulations (fluid dynamics, particle systems)
- Material Point Method (MPM) for realistic physics in the browser
- Node-based visual shader editors compiling to GPU code
- Local AI inference via WebGPU compute shaders
- Three.js Shading Language (TSL) provides a higher-level abstraction for WebGPU shaders

### 1.6 Canvas API Creative Coding

**What it is:** The HTML Canvas 2D rendering context for drawing graphics via JavaScript.

**Key Techniques:**
- Generative art using loops and randomness as core primitives
- Procedural backgrounds (gradients, noise-based textures, geometric patterns)
- Pixel manipulation via `getImageData` / `putImageData` for effects
- Off-screen canvases and Web Workers for heavy computation
- Frame-based animation with `requestAnimationFrame`
- Compositing operations (`globalCompositeOperation`) for blending effects

**Libraries:**
- **p5.js**: Beginner-friendly wrapper over Canvas API, designed for artists
- **Fabric.js**: Advanced Canvas manipulation with object model
- **ZIM**: Framework for creative coding on canvas with interactive features

### 1.7 GSAP Animation Techniques

**What it is:** GreenSock Animation Platform -- the industry standard JavaScript animation library. Now free for all uses since Webflow's acquisition in 2024.

**Key Techniques:**
- **ScrollTrigger**: Link animations to scroll position with scrubbing, pinning, snapping, and batch processing
- **Scrubbing**: Animation progress directly tied to scrollbar position with optional smoothing
- **Pinning**: Fix elements in place while content scrolls past
- **MotionPath**: Animate along SVG or custom paths
- **3D Scroll Animations**: CSS 3D transforms driven by ScrollTrigger
- **ScrollSmoother**: Layered zoom and parallax scroll effects
- **Curved Path Animations**: Responsive scroll-triggered motion along curves
- **Stagger**: Sequential animations across element groups with configurable delays

**Code Pattern:**
```javascript
gsap.to('.element', {
  scrollTrigger: {
    trigger: '.section',
    start: 'top center',
    end: 'bottom center',
    scrub: 1,       // Smooth scrubbing
    pin: true,       // Pin during animation
    snap: 0.25,      // Snap to quarter points
  },
  x: 400,
  rotation: 360,
  scale: 1.5,
});
```

### 1.8 Framer Motion (now Motion) Advanced Patterns

**What it is:** React animation library, rebranded to "Motion" in mid-2025 (v12). Package changed from `framer-motion` to `motion`, import from `motion/react`.

**Key Techniques:**
- **Variant propagation**: Parent defines `animate` prop, children define variant behaviors -- variants "flow down" automatically
- **Layout animations**: `layout` prop for automatic FLIP animations
- **useAnimation hook**: Programmatic control over animation sequences
- **Gesture animations**: `whileHover`, `whileTap`, `whileDrag` with spring physics
- **AnimatePresence**: Enter/exit animations for conditional rendering
- **Hardware-accelerated scroll**: `useScroll` with GPU acceleration (v12)
- **Spring physics**: `type: "spring"` with `stiffness`, `damping`, `mass` controls
- **Keyframe arrays**: Multi-step animations via array values

**v12 Features:** oklch/oklab color support, full React 19 concurrent rendering compatibility.

---

## 2. Creative Coding and Generative Art

### 2.1 p5.js Advanced Techniques

**Core Concepts:**
- p5.js wraps the Canvas API to make coding accessible for artists and designers
- Built-in Perlin noise via `noise()` function (1D, 2D, 3D)
- Frame-based animation loop (`draw()`) with state management (`setup()`)

**Advanced Patterns:**
- **Flow Fields**: Create a grid the size of the canvas, store a vector at each point, use Perlin noise to determine angles. Particles dropped at random locations follow the field, leaving colored trails.
- **Noise Orbits**: Use polar coordinates with Perlin noise to create smooth, organic circular patterns
- **Particle Systems**: Emit, update, and cull particles with physics (gravity, wind, attraction)
- **Recursive Structures**: Fractal trees, Sierpinski triangles, Koch snowflakes via recursive drawing

**Key Code Pattern (Flow Field):**
```javascript
let particles = [];
let flowField;
let cols, rows;
const scale = 20;
let zoff = 0;

function setup() {
  createCanvas(800, 800);
  cols = floor(width / scale);
  rows = floor(height / scale);
  flowField = new Array(cols * rows);
  for (let i = 0; i < 1000; i++) particles.push(new Particle());
  background(0);
}

function draw() {
  // Generate flow field from Perlin noise
  let yoff = 0;
  for (let y = 0; y < rows; y++) {
    let xoff = 0;
    for (let x = 0; x < cols; x++) {
      let angle = noise(xoff, yoff, zoff) * TWO_PI * 2;
      flowField[x + y * cols] = p5.Vector.fromAngle(angle);
      xoff += 0.1;
    }
    yoff += 0.1;
  }
  zoff += 0.005;

  // Update and display particles
  particles.forEach(p => {
    p.follow(flowField);
    p.update();
    p.edges();
    p.show();
  });
}
```

### 2.2 Generative Art Algorithms

**Flow Fields:**
- Grid of force vectors across canvas
- Perlin noise determines angle at each grid point
- Particles follow vectors, creating organic, non-overlapping curves
- Variation: Use simplex noise for smoother results (avoids Perlin's directional artifacts)

**L-Systems (Lindenmayer Systems):**
- String rewriting system: axiom + production rules iterated N times
- Turtle graphics interpretation: F=forward, +=turn left, -=turn right, [=push state, ]=pop state
- Variations: stochastic (random rule selection), parametric (rules with parameters), context-sensitive
- Applications: botanical structures, fractal patterns, branching networks, road networks

**Perlin Noise Landscapes:**
- 2D noise for terrain heightmaps
- 3D noise (x, y, time) for animated landscapes
- Layered octaves (fractal Brownian motion / fBm) for natural-looking detail
- Domain warping: feed noise output back as input coordinates for psychedelic effects

### 2.3 Nature-Inspired Algorithms

**Flocking (Boids):**
- Three rules: separation, alignment, cohesion
- Each agent (boid) steers based on nearby neighbors
- Produces emergent swarm behavior from simple local rules

**Reaction-Diffusion (Gray-Scott Model):**
- Two chemicals: activator and inhibitor, diffusing at different rates
- Feed rate (f) and kill rate (k) parameters control pattern type
- Produces spots, stripes, spirals, and labyrinthine patterns
- Can be computed on GPU for large-scale real-time simulations

**Physarum (Slime Mold) Simulation:**
- Agent-based model: thousands of particles with heading, sensor angle, sensor distance
- Each agent: sense, rotate toward strongest trail, deposit chemical, move forward
- Trail diffuses and evaporates each frame
- Produces organic network structures resembling biological transport networks
- WebGL implementations available for real-time performance

**Other Nature Algorithms:**
- Differential growth (expanding curves that avoid self-intersection)
- Space colonization (branching toward attractors)
- Voronoi tessellation / Delaunay triangulation
- Diffusion-limited aggregation (DLA)

### 2.4 Shader Art (GLSL Fragment Shaders)

**What it is:** Programs executed for every pixel simultaneously on the GPU. Written in GLSL, run via WebGL or WebGPU.

**Key Techniques:**
- **Signed Distance Fields (SDFs)**: Define shapes mathematically, combine with boolean operations (union, intersection, subtraction)
- **Ray Marching**: Step through 3D space using SDFs to render complex scenes
- **Fractals**: Mandelbrot, Julia sets, fractal flame algorithms
- **Domain Repetition**: `mod()` to repeat shapes infinitely
- **Smooth Min/Max**: Blend between SDFs for organic merging
- **Noise Functions**: Perlin, simplex, Worley noise implemented in GLSL for textures and effects

**Platforms:** ShaderToy, twigl (live coding with sound shaders), The Book of Shaders (learning resource).

**Performance:** Massively parallel -- every pixel computed simultaneously. Ideal for real-time effects in single-file artifacts.

### 2.5 Algorithmic Composition and Visual Music

**Web Audio API Capabilities:**
- `AudioContext` and `OscillatorNode` for sound synthesis
- `AnalyserNode` with FFT for frequency analysis and visualization
- `GainNode`, `BiquadFilterNode`, `ConvolverNode` for effects
- Audio scheduling via `AudioContext.currentTime` for precise timing

**Visual-Audio Synchronization:**
- FFT frequency data mapped to visual properties (size, color, position)
- Time-domain waveform data for amplitude-reactive visuals
- Beat detection via energy thresholding on frequency bands
- `requestAnimationFrame` loop reading `AnalyserNode` data each frame

**Libraries:**
- **p5.sound**: Audio extension for p5.js (FFT, amplitude, synthesis)
- **Tone.js**: Full-featured Web Audio framework with musical abstractions
- **Konduktiva**: Live coding JavaScript library for algorithmic composition

---

## 3. Data Visualization as Art

### 3.1 D3.js Artistic Visualization

**Core Philosophy:** D3 provides low-level primitives (selections, scales, shapes, transitions) rather than chart types, enabling completely bespoke visualizations.

**Artistic Techniques:**
- **Force-directed layouts**: Simulate physics for organic node arrangements
- **Voronoi diagrams**: Interactive region-based visualizations
- **Chord diagrams**: Show relationships between groups with flowing curves
- **Radial layouts**: Sunburst, radial tree, circular packing
- **Geographic projections**: Artistic map distortions and custom projections
- **Transition chaining**: Sequential, overlapping animations for data storytelling
- **Canvas rendering**: Switch from SVG to Canvas for large datasets (100K+ elements)

**Performance Tips:**
- Use Canvas rendering for >10K elements
- Data aggregation for large datasets
- Virtual scrolling for long lists
- Debounce interactions

### 3.2 Observable Notebooks

**What it is:** Reactive notebook platform where cells reference each other and automatically update. Ideal for prototyping data visualizations with D3.

**Key Features:**
- Reactive programming model (cells auto-update when dependencies change)
- Built-in D3 integration
- Shareable, forkable notebooks
- Import cells from other notebooks for composition

### 3.3 Scrollytelling for Data

**Architecture Pattern:**
1. Sticky visualization container (fixed/sticky position)
2. Text/narrative steps that scroll past
3. Step detection via Intersection Observer (Scrollama) or ScrollTrigger (GSAP)
4. Visualization state updates triggered by active step

**Key Frameworks:**
- **Scrollama**: Lightweight, IntersectionObserver-based step detection
- **GSAP ScrollTrigger**: More powerful, scrubbing and pinning support
- **Closeread (Quarto)**: Data-driven scrollytelling in R/Python documents

**Best Practice:** Break stories into discrete stages. Use animations to highlight specific data points. Provide annotated versions with legends. Evaluate on: narrative quality, scrollytelling appropriateness, visual polish, technical accomplishment.

**Engagement Stat:** Scroll-driven stories achieve 400% higher engagement than static content.

### 3.4 Physical Data Visualization Concepts

**Principles applied to web:**
- Tangibility through 3D rendering (height = value, texture = category)
- Spatial arrangement leveraging WebGL for depth and perspective
- Material metaphors (glass transparency for uncertainty, weight/mass for importance)
- Environmental context (placing data in recognizable spatial contexts)

---

## 4. Interactive Narrative and Experience Design

### 4.1 Interactive Storytelling Engines

**Established Tools:**
- **Twine** (v2.11.1, Nov 2025): Open-source, node-based story editor. Exports self-contained HTML files. Formats: Harlowe (beginner-friendly), SugarCube (powerful), Chapbook
- **InkGameScript**: Based on Inkle's Ink scripting language. Deep branching with variables, conditions, and state
- **Narrat**: No-code game engine for narrative games with RPG features and visual novel support

**Modern JavaScript Approaches:**
- **StoryPlay** (2026): Twine-inspired visual builder with node-based editing, playable preview, variables, conditions, JSON export
- **Route Engine**: Lightweight JS visual novel engine with branching storylines
- **Iffy**: Blends branching narratives with AI-powered dynamic storytelling

**Core Narrative Patterns:**
- Branching trees (choices lead to divergent paths)
- Hub-and-spoke (central location with explorable branches)
- Parallel paths (multiple storylines converging)
- Quality-based narrative (state variables determine available options)
- Procedural narrative (AI/algorithm-generated story elements)

### 4.2 Scrollytelling Frameworks

**Scrollama:**
- Built on IntersectionObserver API
- Triggers events based on element position relative to viewport
- Lightweight, well-documented
- Combines with D3.js for data-driven storytelling

**GSAP ScrollTrigger:**
- Industry standard for scroll-based animations
- Scrubbing, pinning, snapping, batch processing
- Now free for all use cases

### 4.3 Immersive Web Experiences

**Awwwards-Winning Techniques:**
- WebGL mouse flow (cursor movements influence visual elements)
- Lottie animations combined with WebGL
- Scroll-triggered parallax with depth layers
- Full-screen video/canvas backgrounds with interactive overlays
- Gamified navigation and exploration
- Sound design synchronized with scroll/interaction states

**Technical Stack Patterns:**
- Three.js + GSAP + Barba.js for page transitions
- WebGL shader effects triggered by scroll position
- Hybrid DOM/WebGL rendering (CSS3DRenderer)

---

## 5. Micro-interactions and UX Delight

### 5.1 Micro-interaction Design Patterns

**Core Principles:**
- Micro-interactions are a communication language between user and interface
- Ideal duration: 200-500ms (noticed but doesn't break flow)
- Must provide clarity, build trust, and create emotional connection
- Always pair with visual or audio cues (never vibration alone)

**Common Patterns:**
- Button state transitions (idle -> hover -> active -> success/error)
- Form validation feedback (shake, color change, icon morph)
- Loading/progress indicators with personality
- Toggle switches with physics-based motion
- Pull-to-refresh with branded animation
- Scroll progress indicators
- Like/favorite heart burst animations

### 5.2 Spring-Based Animation Physics

**Physics Model:**
Three properties control spring behavior:
- **Mass**: Heavier = slower, more momentum
- **Stiffness**: Higher = snappier response (good for buttons, micro-interactions)
- **Damping**: Controls bounce -- low damping = bouncy attention-grabbers, high damping = smooth professional motion

**Implementation:**
```javascript
// Spring physics core
function spring(current, target, velocity, stiffness, damping, mass) {
  const force = -stiffness * (current - target);
  const dampingForce = -damping * velocity;
  const acceleration = (force + dampingForce) / mass;
  velocity += acceleration;
  current += velocity;
  return { current, velocity };
}
```

Libraries: Framer Motion (`type: "spring"`), React Spring, GSAP (with custom ease), Popmotion.

### 5.3 Haptic Feedback on Web

**Vibration API:** `Navigator.vibrate(pattern)` triggers device vibration.
- Single pulse: `navigator.vibrate(200)` (200ms)
- Pattern: `navigator.vibrate([100, 50, 100])` (vibrate, pause, vibrate)
- Best for: button confirmations, form validation, game feedback
- Duration: 50-200ms is ideal
- Browser support: Chrome, Firefox; limited Safari support

**Best Practices:**
- Always pair with visual/audio feedback
- Use sparingly to avoid fatigue
- Keep vibrations short (50-200ms)
- User consent may be required on mobile

### 5.4 Cursor-Driven Interactions

**Techniques:**
- **Magnetic cursors**: Elements attract/stick to cursor with elastic snap-back
- **Swirl/vortex cursors**: Particles spiral behind pointer movement
- **Spotlight cursors**: Circular area reveals hidden content as cursor moves
- **Flashlight effect**: Dark overlay with cursor-positioned cutout
- **Parallax on hover**: Elements shift based on cursor position within container
- **Trail effects**: Fading copies of cursor or particles following mouse path

**Technical Foundation:**
- Linear interpolation (lerp) for smooth cursor following: `current += (target - current) * factor`
- `requestAnimationFrame` for smooth 60fps tracking
- CSS `transform` for GPU-accelerated movement
- Pointer events API for unified mouse/touch/pen input

### 5.5 Spatial UI Design

**Patterns:**
- Depth layers using `transform: translateZ()` and `perspective`
- Parallax scroll layers at different speeds
- 3D card flips and rotations on hover
- Spatial audio positioning tied to visual elements
- Focus-based depth of field (blur elements based on distance from cursor)

---

## 6. AI-Assisted Creative Tools

### 6.1 AI Agents for Creative Coding

**Current Landscape (2025-2026):**
- "Vibe coding" (coined by Andrej Karpathy, Feb 2025): Natural language prompts guide AI to generate functional code
- Visual prompting: Wireframes/mockups as input for AI code generation
- Y Combinator Winter 2025: 25% of startups had codebases 95% AI-generated

**AI-Assisted Workflow:**
1. Describe desired artifact in natural language
2. AI generates initial implementation
3. Iterate via conversation (refine, add features, fix issues)
4. Human provides creative direction; AI handles implementation

### 6.2 Prompt-to-Artifact Patterns

**Effective Prompt Structure:**
- Specify the experience type (visualization, game, tool, art piece)
- Define the interaction model (scroll, click, hover, drag)
- Describe the visual aesthetic (minimal, lush, retro, futuristic)
- List technical constraints (single file, no dependencies, specific framework)
- Reference inspirations (but describe the effect, don't just name the site)

**Anti-patterns to Avoid ("AI Slop"):**
- Excessive centered layouts
- Purple/blue gradients everywhere
- Uniform rounded corners on everything
- Default Inter font
- Generic placeholder content
- Over-reliance on card grids

**Quality Markers:**
- Intentional typography hierarchy
- Purposeful color palette with meaning
- Micro-interactions that reinforce the concept
- Responsive behavior that adapts gracefully
- Performance optimization (no jank, smooth animations)

### 6.3 Creative Constraint-Based Design

**Principle:** Constraints enable creativity rather than limiting it. Problem solving within constraints is itself a highly creative act.

**Framework for Artifact Design:**
1. **Define the design space**: What parameters can vary? (colors, shapes, timing, layout)
2. **Set constraints**: What rules must be followed? (single file, specific palette, max load time)
3. **Establish objectives**: What should the artifact achieve? (delight, inform, provoke, soothe)
4. **Iterate algorithmically**: Let the system explore variations within the constraint space
5. **Curate**: Select the most effective results from generated possibilities

**Applying to Design Systems:**
- Constraining possible values reduces cognitive load
- Enforces consistency and predictability
- Enables rapid exploration within safe boundaries
- Parametric models allow systematic variation

---

## 7. Cross-Cutting Principles for a Master Artificer

### 7.1 Single-File Artifact Architecture

**HTML ROMs Concept:** Self-contained applications in a single HTML file that work offline with no network dependency.

**Technical Requirements:**
- All CSS, JavaScript, and assets inlined in one HTML file
- Base64-encode images and fonts
- Use CDN links for large libraries (Three.js, D3, GSAP) or inline them
- No external file dependencies

**Bundling Strategy:**
- Develop with standard tooling (separate files, modules)
- Bundle with Parcel + html-inline for single-file output
- Alternative: Write directly as single file for simpler artifacts

### 7.2 Performance Hierarchy

1. **CSS-only** (transforms, transitions, scroll-driven animations) -- best performance
2. **CSS + minimal JS** (View Transitions API, Container Queries) -- excellent
3. **Canvas 2D** (generative art, pixel manipulation) -- good for 2D
4. **WebGL / Three.js** (3D scenes, shader effects) -- good with optimization
5. **WebGPU** (compute shaders, massive parallelism) -- cutting edge, best raw performance

### 7.3 Animation Principles for Web

- **Duration**: 200-500ms for micro-interactions, 300-800ms for transitions, 1-3s for reveals
- **Easing**: Use spring physics or cubic-bezier for natural motion; avoid linear for UI
- **Stagger**: 30-80ms between sequential element animations
- **Reduced motion**: Always respect `prefers-reduced-motion` media query
- **60fps target**: Use `transform` and `opacity` for GPU-composited animations

### 7.4 Technique Selection Matrix

| Goal | Primary Technique | Fallback |
|------|------------------|----------|
| Scroll-driven effects | CSS scroll-timeline | GSAP ScrollTrigger |
| Page/state transitions | View Transitions API | GSAP + manual DOM |
| 3D scenes | Three.js (WebGL) | CSS 3D transforms |
| Generative art | p5.js or Canvas API | SVG + D3 |
| Data visualization | D3.js | Chart.js + custom |
| Interactive narrative | Ink/Twine pattern | Custom state machine |
| Particle systems | WebGL shaders | Canvas 2D |
| Spring animations | Motion (Framer) | CSS spring() or GSAP |
| Audio-visual | Web Audio API + Canvas | Tone.js + p5.sound |
| GPU compute | WebGPU | WebGL compute via texture |

### 7.5 Creative Coding Recipe Book

**Recipe: Ambient Generative Background**
- Perlin noise flow field + particle system
- Low alpha trails (don't clear canvas, draw semi-transparent background)
- Slowly evolving z-offset for temporal variation
- Color palette mapped to noise value

**Recipe: Data-Driven Scrollytelling**
- Scrollama for step detection
- D3.js for visualization
- Sticky container + scrolling text steps
- GSAP for transition animations between data states

**Recipe: Interactive 3D Product Showcase**
- Three.js scene with OrbitControls
- GLB model with optimized geometry
- Environment map for realistic reflections
- Scroll-driven camera animation
- DOM overlay for text/UI elements

**Recipe: Musical Visualization**
- Web Audio API AnalyserNode for FFT data
- Canvas or WebGL rendering
- Map frequency bands to visual properties
- Beat detection for rhythmic effects
- User mic input or audio file playback

**Recipe: Immersive Narrative Experience**
- Full-viewport sections with snap scroll
- View Transitions between story beats
- Ambient audio synchronized to position
- Cursor-driven parallax within sections
- Progressive reveal via scroll-driven animations

---

## Sources

### CSS Houdini
- [Houdini APIs - MDN](https://developer.mozilla.org/en-US/docs/Web/API/Houdini_APIs)
- [Cross-browser Paint Worklets - web.dev](https://web.dev/articles/houdini-how)
- [CSS Painting API - MDN](https://developer.mozilla.org/en-US/docs/Web/API/CSS_Painting_API)

### Scroll-Driven Animations
- [CSS Scroll-Driven Animations - MDN](https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Scroll-driven_animations)
- [Mastering CSS Scroll Timeline - DEV Community](https://dev.to/softheartengineer/mastering-css-scroll-timeline-a-complete-guide-to-animation-on-scroll-in-2025-3g7p)
- [Scroll-Driven Animations - Smashing Magazine](https://www.smashingmagazine.com/2024/12/introduction-css-scroll-driven-animations/)
- [Chrome DevDocs - Scroll-driven Animations](https://developer.chrome.com/docs/css-ui/scroll-driven-animations)

### View Transitions API
- [View Transition API - MDN](https://developer.mozilla.org/en-US/docs/Web/API/View_Transition_API)
- [View Transitions 2025 Update - Chrome Blog](https://developer.chrome.com/blog/view-transitions-in-2025)
- [View Transitions SPA Without Framework - DebugBear](https://www.debugbear.com/blog/view-transitions-spa-without-framework)

### Three.js / WebGL
- [3D Cards with Three.js - Codrops](https://tympanus.net/codrops/2025/05/31/building-interactive-3d-cards-in-webflow-with-three-js/)
- [WebGL Portfolio - Codrops](https://tympanus.net/codrops/2025/11/27/letting-the-creative-process-shape-a-webgl-portfolio/)
- [Scroll-Revealed WebGL Gallery - Codrops](https://tympanus.net/codrops/2026/02/02/building-a-scroll-revealed-webgl-gallery-with-gsap-three-js-astro-and-barba-js/)
- [Three.js Journey](https://threejs-journey.com/)

### WebGPU
- [Best of WebGPU May 2025](https://www.webgpuexperts.com/best-webgpu-updates-may-2025/)
- [Field Guide to TSL and WebGPU - Maxime Heckel](https://blog.maximeheckel.com/posts/field-guide-to-tsl-and-webgpu/)
- [Galaxy Simulation with WebGPU Compute](https://threejsroadmap.com/blog/galaxy-simulation-webgpu-compute-shaders)

### GSAP
- [GSAP ScrollTrigger Guide - GSAPify](https://gsapify.com/gsap-scrolltrigger)
- [Layered Zoom Scroll - Codrops](https://tympanus.net/codrops/2025/10/29/building-a-layered-zoom-scroll-effect-with-gsap-scrollsmoother-and-scrolltrigger/)
- [3D Scroll-Driven Text - Codrops](https://tympanus.net/codrops/2025/11/04/creating-3d-scroll-driven-text-animations-with-css-and-gsap/)
- [Curved Path Animations - Codrops](https://tympanus.net/codrops/2025/12/17/building-responsive-scroll-triggered-curved-path-animations-with-gsap/)

### Framer Motion / Motion
- [Advanced Patterns - Maxime Heckel](https://blog.maximeheckel.com/posts/advanced-animation-patterns-with-framer-motion/)
- [Motion.dev](https://motion.dev/)
- [Advanced Techniques 2025 - LuxisDesign](https://www.luxisdesign.io/blog/advanced-framer-motion-animation-techniques-for-2025)

### Generative Art
- [Flow Fields and Noise - DEV Community](https://dev.to/nyxtom/flow-fields-and-noise-algorithms-with-p5-js-5g67)
- [Morphogenesis Resources - GitHub](https://github.com/jasonwebb/morphogenesis-resources)
- [Reaction-Diffusion Playground](https://jasonwebb.github.io/reaction-diffusion-playground/)
- [The Book of Shaders](https://thebookofshaders.com/04/)
- [Flocking Simulation - The Coding Train](https://thecodingtrain.com/challenges/124-flocking-simulation/)
- [Physarum Simulation - GitHub](https://github.com/nicoptere/physarum)
- [L-Systems in Generative Art - Cratecode](https://cratecode.com/info/l-systems-in-generative-art)

### Data Visualization
- [D3.js](https://d3js.org/)
- [Observable D3 Gallery](https://medium.com/@tjanmichela/exploring-data-visualization-with-observable-d3-gallery-b02cfe91b7e8)
- [Scrollytelling for Observable](https://observablehq.com/@pstuffa/scrollytelling-for-observable)
- [Scrollytelling Guide 2025 - UI Deploy](https://ui-deploy.com/blog/complete-scrollytelling-guide-how-to-create-interactive-web-narratives-2025)

### Interactive Narrative
- [Twine](https://twinery.org/)
- [InkGameScript](https://inkgamescript.online/)
- [Narrat Engine](https://narrat.dev/)
- [Scrollama Intro - Erik Driessen](https://www.edriessen.com/2023/04/24/an-introduction-to-scrollytelling-data-storytelling-using-scrollama-js-d3-js-and-html-css/)

### Micro-interactions
- [Micro Interactions 2025 - Stan Vision](https://www.stan.vision/journal/micro-interactions-2025-in-web-design)
- [UI/UX Evolution 2026 - PrimoTech](https://primotech.com/ui-ux-evolution-2026-why-micro-interactions-and-motion-matter-more-than-ever/)
- [Spring Animations - Patricio Reyes](https://medium.com/@patoreyes23/designing-interaction-spring-animations-c8b8788a4b2a)
- [Cursor Interactions - Awwwards](https://www.awwwards.com/awwwards/collections/hovers-cursors-and-cute-interactions/)

### Haptic Feedback
- [Vibration API - MDN](https://developer.mozilla.org/en-US/docs/Web/API/Vibration_API)
- [Haptic Feedback for Web Apps - OpenReplay](https://blog.openreplay.com/haptic-feedback-for-web-apps-with-the-vibration-api/)

### AI-Assisted Creative Coding
- [AI-Generated Design Systems - The New Stack](https://thenewstack.io/from-prompt-to-production-a-guide-to-ai-generated-design-systems/)
- [Visual Prompting for Vibe Coding - MockFlow](https://resources.mockflow.com/visual-prompting-for-vibe-coding-the-future-of-ai-powered-development)
- [HTML ROMs: Self-contained Web Apps](https://conroy.org/self-contained-web-apps)
- [AI Co-Artist GLSL Framework - arXiv](https://arxiv.org/html/2512.08951v1)

### Container Queries
- [CSS Container Queries 2025 - Caisy](https://caisy.io/blog/css-container-queries)
- [Container Queries 2026 - LogRocket](https://blog.logrocket.com/container-queries-2026/)

### Canvas API
- [Canvas API - MDN](https://developer.mozilla.org/en-US/docs/Web/API/Canvas_API)
- [Generative Art with Canvas - DEV Community](https://dev.to/shayo_victor_c02f1777210e/generative-art-with-javascript-and-canvas-a-beginners-playground-2cb8)

### Web Audio
- [Generative Music Web Audio - GitHub](https://github.com/pparocza/generative-music-web-audio)
- [Algorithmic Composition on p5.js - Processing Foundation](https://medium.com/processing-foundation/a-platform-for-algorithmic-composition-on-p5-js-271cd872d648)
