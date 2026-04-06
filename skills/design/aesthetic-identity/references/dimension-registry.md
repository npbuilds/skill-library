# Dimension Registry

The canonical list of active aesthetic dimensions. Each dimension is a spectrum with two named poles, a current position (0.0–1.0), a confidence score (0.0–1.0), and a data point count.

Dimensions are grouped by category. New dimensions discovered by the observer are appended to the appropriate category or to "Discovered" if they don't fit.

---

## Spatial

### Density
**Sparse/Minimal** ◄────────────────► **Rich/Layered**
- Position: 0.72 | Confidence: 0.23 | Data points: 1
- What it measures: How much visual information occupies the canvas. Few elements with generous whitespace vs. many elements creating texture and complexity.
- Evidence: Archon dashboard — dense data presentation with gauges, tables, sector heat maps, yield curves, SVG charts. Accepted and praised without density complaints.

### Symmetry
**Symmetric/Balanced** ◄────────────────► **Asymmetric/Dynamic**
- Position: 0.40 | Confidence: 0.23 | Data points: 1
- What it measures: Whether compositions favor equilibrium or deliberate imbalance. Centered, mirrored arrangements vs. off-axis, tension-creating layouts.
- Evidence: Grid-based dashboard layout with symmetric gauge row and balanced card columns. Slightly structured/ordered preference.

### Depth
**Flat/Planar** ◄────────────────► **Dimensional/Layered**
- Position: 0.55 | Confidence: 0.23 | Data points: 1
- What it measures: Use of visual depth cues — shadows, overlapping planes, parallax, blur, z-axis layering vs. single-plane, flat design.
- Evidence: Subtle panel layering, CRT vignette overlay, gauge ring depth, but not heavy shadow/parallax. Moderate depth.

---

## Chromatic

### Temperature
**Cool** ◄────────────────► **Warm**
- Position: 0.30 | Confidence: 0.23 | Data points: 1
- What it measures: Dominant color temperature across outputs. Blues/greens/violets vs. reds/oranges/ambers/earth tones.
- Evidence: Light mode palette is blue-gray backgrounds (#e8ecf2), deep teal accents (#1a7070). Cool-dominant with warm accent pops (amber, red used for data signaling only).

### Chromatic Range
**Monochromatic** ◄────────────────► **Polychromatic**
- Position: 0.55 | Confidence: 0.23 | Data points: 1
- What it measures: How many distinct hues appear in a typical output. Single-hue with value variation vs. full-spectrum color use.
- Evidence: Multi-hue but restrained — teal, amber, magenta, red, green all present but muted and purposeful (each color signals different data categories).

### Contrast
**Subtle/Muted** ◄────────────────► **Bold/High-Impact**
- Position: 0.35 | Confidence: 0.23 | Data points: 1
- What it measures: Value contrast and saturation levels. Soft, close-valued palettes vs. dramatic light/dark and vivid saturation.
- Evidence: "Faded neon" was the explicit brief. Light mode uses muted, desaturated accent colors against soft backgrounds. User praised this. Not washed out, but deliberately restrained.

---

## Form

### Geometry
**Geometric/Rectilinear** ◄────────────────► **Organic/Flowing**
- Position: 0.20 | Confidence: 0.23 | Data points: 1
- What it measures: Shape language. Hard edges, straight lines, circles/rectangles vs. freeform curves, natural forms, irregular boundaries.
- Evidence: Dashboard uses grid layout, rectangular cards, circular gauge rings, straight-line charts, bar charts. Strongly geometric vocabulary.

### Precision
**Mechanical/Exact** ◄────────────────► **Expressive/Handmade**
- Position: 0.15 | Confidence: 0.23 | Data points: 1
- What it measures: Finish quality. Pixel-perfect, machine-made feel vs. visible hand, intentional imperfection, textures that suggest physical media.
- Evidence: Monospace typography (Share Tech Mono, Orbitron), pixel-precise alignment, consistent spacing tokens, data-table precision. Very mechanical.

---

## Temporal

### Motion Feel
**Static/Calm** ◄────────────────► **Kinetic/Energetic**
- Position: 0.45 | Confidence: 0.23 | Data points: 1
- What it measures: Presence and intensity of animation and motion. Still compositions vs. persistent movement, particles, transitions, animated state.
- Evidence: Subtle animation — header line pulse, CSS digital rain, logo flicker. Present but understated. User praised the overall design including these subtle motions.

### Temporal Register
**Retro/Classic** ◄────────────────► **Futuristic/Novel**
- Position: 0.55 | Confidence: 0.23 | Data points: 1
- What it measures: The era the aesthetic evokes. Vintage palettes, established patterns, nostalgia vs. bleeding-edge techniques, speculative forms, unfamiliar materiality.
- Evidence: User explicitly requested "cyberpunk but lived in. Vintage feel." CRT scanlines + Orbitron font = retro-futuristic blend. Not purely retro, not purely futuristic — a synthesis.

---

## Emotional

### Emotional Register
**Serious/Austere** ◄────────────────► **Playful/Whimsical**
- Position: 0.25 | Confidence: 0.23 | Data points: 1
- What it measures: The emotional tone conveyed by visual choices. Formal, restrained, dignified vs. lighthearted, surprising, delightful.
- Evidence: Investment intelligence dashboard — serious data presentation with atmospheric styling. Not austere (has personality), but firmly on the serious side.

### Information Stance
**Data-Forward** ◄────────────────► **Atmosphere-Forward**
- Position: 0.35 | Confidence: 0.23 | Data points: 1
- What it measures: Priority balance between conveying information and creating a feeling. Clarity and legibility first vs. mood and immersion first.
- Evidence: Dashboard is data-first (14 API feeds, tables, charts, metrics) but wrapped in strong atmospheric cyberpunk theming. Data leads, atmosphere supports.

---

## Discovered

### Light/Dark Preference
**Light Backgrounds** ◄────────────────► **Dark Backgrounds**
- Position: 0.25 | Confidence: 0.23 | Data points: 1
- What it measures: Preference for background luminance. Light, airy backgrounds vs. dark, immersive backgrounds.
- Discovery evidence: User was presented with both dark cyberpunk and light mode. Explicitly praised light mode: "i really love the light background design and theme and colors and everything."
- Discovered: 2026-03-28

<!--
FORMAT FOR NEW DIMENSIONS:
### [Dimension Name]
**[Pole A]** ◄────────────────► **[Pole B]**
- Position: X.XX | Confidence: X.XX | Data points: N
- What it measures: [description]
- Discovery evidence: [what pattern triggered this]
- Discovered: [date]
-->
