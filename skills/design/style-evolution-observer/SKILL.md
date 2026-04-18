---
name: style-evolution-observer
description: >
  Observe creative outputs and infer aesthetic preferences from user behavior — acceptance,
  revision patterns, explicit praise, and abandonment. Update the aesthetic-identity profile
  with dimensional shifts, confidence changes, and discovered dimensions. Activates after
  any creative output (artifact, design, visualization) to capture what was built and how
  the user responded.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
allowed-tools: Read Write Glob Grep
---

# Style Evolution Observer — The Silent Curator

Watch. Measure. Learn. Update.

This observer tracks the user's evolving aesthetic by reading behavioral signals — not asking questions. The goal: after enough outputs, the aesthetic-identity profile should predict the user's preferences before they state them.

## When to Activate

After any creative output that involves visual/aesthetic decisions:
- Artifact creation (master-artificer)
- Design direction (design-orchestrator)
- Generative art
- Dashboard or visualization styling
- Any output where palette, composition, typography, or motion choices were made

## The Inference Protocol

### Signal Types (strongest → weakest)

**Strong positive signals:**
- User explicitly praises an aspect: "love this palette", "the motion is perfect"
- Output is used without modification
- User shares or references the output later

**Moderate positive signals:**
- User accepts the output with unrelated changes (content edits, not style edits)
- User builds on the output in subsequent requests
- No revision requested — silence after delivery

**Moderate negative signals:**
- User asks for specific style changes: "make it warmer", "too busy", "less playful"
- User provides alternative references: "more like X instead"
- User adjusts palette, density, or motion after delivery

**Strong negative signals:**
- User rejects the direction entirely: "start over", "not what I had in mind"
- User abandons the output without using it
- User overrides creative direction with very specific instructions (implies defaults were wrong)

### Mapping Signals to Dimensions

Each signal maps to one or more dimensions:

| Signal | Dimension(s) affected | Direction |
|--------|----------------------|-----------|
| "too busy" / "too much" | Density | → Sparse |
| "too empty" / "needs more" | Density | → Rich |
| "make it warmer" / "too cold" | Temperature | → Warm |
| "more contrast" / "pops more" | Contrast | → Bold |
| "too flashy" / "tone it down" | Contrast, Emotional Register | → Muted, → Serious |
| "love the animation" | Motion Feel | reinforce current |
| "too much movement" | Motion Feel | → Static |
| Chose geometric shapes | Geometry | → Geometric |
| Chose organic/natural forms | Geometry | → Organic |
| Used monospace/grid layout | Precision | → Mechanical |
| Used handwritten/textured feel | Precision | → Expressive |
| Referenced retro/vintage | Temporal Register | → Retro |
| Referenced futuristic/novel | Temporal Register | → Futuristic |

This table is not exhaustive — the observer should map any aesthetic feedback to the most relevant dimension(s). If feedback doesn't fit existing dimensions, flag it as a candidate for dimension discovery.

## Update Protocol

### After Each Output

1. **Capture** — record the output's aesthetic position
   - What palette was used? (hex values, temperature, contrast level)
   - What composition approach? (density, symmetry, depth)
   - What motion? (amount, speed, easing)
   - What typography? (classification, weight, precision)
   - What mood? (emotional register, information stance)

2. **Observe** — read the user's response
   - Did they accept, modify, or reject?
   - What specific changes did they request?
   - What language did they use? (capture to mood vocabulary)
   - Did they reference any influences?

3. **Map** — translate observations to dimensional updates
   - For each affected dimension, calculate the signal strength and direction
   - Positive signals: move position toward the output's value, increase confidence
   - Negative signals: move position away from the output's value, increase confidence
   - No signal: slight confidence decay (recency weighting)

4. **Update** — write changes to the aesthetic-identity references
   - Update `dimension-registry.md` positions and confidence scores
   - Update `current-profile.md` narrative summary if any dimension crossed a threshold
   - Append to `evolution-log.md` if a meaningful change occurred
   - Update the Palette Library table in `current-profile.md` if a new palette was used
   - Add to mood vocabulary if new terms appeared
   - Add to influences if new references were cited

### Confidence Scoring

```
volume      = log(n + 1) / log(21)          # 0→0, 5→0.42, 12→0.67, 20→1.0
consistency = 1 - stdev(observations) / 0.5  # 1.0 if all identical, 0.0 if spread ≥0.5
recency     = weighted avg where weight = 0.5^(age / 10)  # half-life of 10 outputs

confidence  = min(1.0, volume * max(0, consistency) * recency)
```

- `n` = total observations for this dimension
- `observations` = list of dimensional positions (0.0–1.0) from each output
- `age` = number of outputs ago (0 = most recent)

**Calibration targets** (assuming high consistency and recent data):
- ~5 data points → ~0.4 confidence
- ~12 data points → ~0.65 confidence
- ~20 data points → ~0.9 confidence

Low consistency (user oscillates) or stale data (no recent outputs engaging this dimension) will pull confidence down even with many data points.

### Drift Detection

Compare the last 5 outputs against the last 20. If a dimension's recent average diverges from its historical average by >0.15:

- **Gradual drift** — if the shift was incremental across outputs → update the profile, log as `drift`
- **Sudden pivot** — if the shift appeared in 1-2 outputs → hold. Wait for confirmation before updating. If the new direction persists for 3+ outputs, log as `pivot`

This prevents a single experimental output from overwriting an established profile.

## Dimension Discovery

When the observer detects a consistent pattern that doesn't map to any existing dimension:

1. **Evidence threshold** — the pattern must appear in 3+ outputs
2. **Describe the axis** — identify the two poles based on observed variation
3. **Propose** — add to the Discovered section of `dimension-registry.md` with status "proposed"
4. **Validate** — if the proposed dimension accumulates 5+ data points and confidence > 0.3, promote to active

**Discovery candidates to watch for:**
- Composition structure (grid-based vs. freeform)
- Edge treatment (sharp crops vs. bleeds/fades)
- Information hierarchy approach (progressive disclosure vs. everything visible)
- Texture use (clean/digital vs. gritty/tactile)
- Scale relationships (uniform vs. extreme size contrast)
- Narrative quality (does the design tell a story or present a state?)

## Tengan (天眼) Inspiration Analysis Mode

A second activation mode. While the primary mode observes *outputs* and infers from *behavior*, Tengan analyzes *inputs* — inspiration images the user explicitly shares — and proposes dimension updates directly.

**Name meaning:** 天眼 (tengan) — "heavenly eye" / "divine sight." A Buddhist concept of perceiving reality beyond surface appearance. Tengan sees the dimensional truth of an image across all 17 aesthetic axes.

### When to Activate

When the user shares an image with an explicit intent signal:

| Intent Signal | Examples | Action |
|--------------|---------|--------|
| **Absorb** | "absorb this", "add to my aesthetic", "Tengan, absorb this" | Full analysis → profile update at 0.7x weight |
| **Reference** | "I like this", "inspired by", "reference for next project" | Full analysis → profile update at 0.4x weight |
| **Analyze** | "what does Tengan see?", "analyze this", "map this to my dimensions" | Full analysis → report only, no profile update |
| **Avoid** | "not this", "anti-reference", "the opposite of what I want" | Full analysis → negative profile update at -0.5x weight |

### Signal Strength Multipliers

Inspiration signals carry less weight than output-based signals because liking something is not the same as wanting to create it. A user can admire a Vermeer without wanting their dashboards to look like Dutch Golden Age paintings.

| Signal Source | Multiplier | Data Point Weight | Rationale |
|---|:-:|:-:|---|
| Creative output (primary mode) | 1.0x | 1.0 | The user made this and accepted it — strongest signal |
| Inspiration "absorb" | 0.7x | 0.7 | Deliberate aesthetic expansion — strong but not output-equivalent |
| Inspiration "reference" | 0.4x | 0.4 | Appreciation — may not want to replicate fully |
| Inspiration "avoid" | -0.5x | 0.5 | Negative signal — push dimensions away |

**Why not 1.0x for inspiration?** 20 Pinterest saves shouldn't outweigh 5 actual creative outputs. The multiplier prevents passive consumption from overwriting active creation. This matches how Pinterest (PinnerSage) and Pento weight implicit vs. explicit signals in their taste models.

### Inspiration Analysis Protocol

When Tengan activates, analyze the image across **all 17 dimensions**:

#### Phase 1 — Dimensional Map

For each dimension, estimate the image's position (0.0–1.0):

```
TENGAN ANALYSIS — [Image description]
Date: [date]
Signal: [absorb / reference / analyze / avoid]

── SPATIAL ──
  Density:     [0.XX] — [brief justification]
  Symmetry:    [0.XX] — [brief justification]
  Depth:       [0.XX] — [brief justification]

── CHROMATIC ──
  Temperature:      [0.XX] — [brief justification]
  Chromatic Range:   [0.XX] — [brief justification]
  Contrast:          [0.XX] — [brief justification]

── FORM ──
  Geometry:    [0.XX] — [brief justification]
  Precision:   [0.XX] — [brief justification]

── TEMPORAL ──
  Motion Feel:       [0.XX] — [brief justification]
  Temporal Register: [0.XX] — [brief justification]

── EMOTIONAL ──
  Emotional Register:  [0.XX] — [brief justification]
  Information Stance:  [0.XX] — [brief justification]

── PHOTOGRAPHIC ──
  Light Character:   [0.XX] — [brief justification]
  Substrate/Grain:   [0.XX] — [brief justification]
  Atmosphere/Mood:   [0.XX] — [brief justification]

── DISCOVERED ──
  Light/Dark Pref:   [0.XX] — [brief justification]
  Sublime Scale:     [0.XX] — [brief justification]
```

#### Phase 2 — Confidence Modifiers

Not every dimension is equally expressed in every image. Rate how clearly the image expresses each dimension:

- **Strong expression** (1.0 modifier) — the image clearly demonstrates this dimension's position
- **Moderate expression** (0.6 modifier) — the dimension is present but not the image's defining quality
- **Weak expression** (0.3 modifier) — the dimension is barely relevant to this image
- **Not applicable** (0.0 modifier) — skip this dimension for this image

Apply: `effective_weight = signal_multiplier × confidence_modifier`

#### Phase 3 — Delta from Current Profile

Show the largest divergences between the image and the user's current profile:

```
LARGEST DIVERGENCES (Δ > 0.15):
  [Dimension]: current [X.XX] → image [Y.YY] (Δ [Z.ZZ])
  [Dimension]: current [X.XX] → image [Y.YY] (Δ [Z.ZZ])
  ...

REINFORCEMENTS (Δ < 0.10, same direction as profile):
  [Dimension]: current [X.XX] ≈ image [Y.YY] — confirms existing position
  ...
```

#### Phase 4 — Proposed Updates

If the signal is "absorb", "reference", or "avoid" (not "analyze"), propose profile updates:

```
PROPOSED UPDATES (signal: [type], multiplier: [X.Xx]):
  [Dimension]: [current] → [proposed] (conf: [current] → [proposed])
  ...
```

Apply the confidence scoring formula from the Update Protocol section, treating inspiration data points as fractional: an "absorb" = 0.7 data points, a "reference" = 0.4 data points.

### Photography-Specific Checklist

When the inspiration image is a photograph or photographic in nature, additionally analyze:

1. **Light** — Direction, quality, source. Natural vs. artificial. Time of day. Reference `photography-vocabulary.md` lighting table for dimensional mapping.
2. **Grain/Texture** — Film stock character, digital noise, processing artifacts. Reference `photography-vocabulary.md` substrate table.
3. **Atmosphere** — Weather, environmental conditions, haze, fog, smoke. Reference `photography-vocabulary.md` atmospheric conditions table.
4. **Color grading** — Natural vs. stylized. If graded: teal/orange, cool desaturation, warm amber, split-toned, cross-processed. Maps to Temperature + Contrast + Chromatic Range.
5. **Composition/Framing** — Focal length (wide/normal/tele), depth of field (deep/selective/shallow), framing pattern (negative space, centered, rule of thirds, fill). Reference `photography-vocabulary.md` composition tables.
6. **Genre** — Street, architectural, cinematic, editorial, other. Cross-reference with user's stated interests in the profile. Images in the user's interest genres carry full weight; images in anti-interest genres should be flagged but weighted at 0.0 unless the user explicitly signals otherwise.

### Evolution Log Entry Format

Inspiration analyses use a distinct change type in `evolution-log.md`:

```
## [Date] — inspiration ([absorb/reference/avoid])

**Trigger:** User shared [image description] with "[exact signal phrase]"
**Type:** `inspiration`
**Signal multiplier:** [0.7x / 0.4x / -0.5x]

**Dimensions shifted:**
- [Dimension]: [old] → [new] (confidence: [old] → [new])
- ...

**Dimension discovered:** [if applicable]

**Evidence:**
- [Brief description of the image and what it signals]
- Signal strength: [Strong/Moderate] — [rationale]

**Notes:** [Any observations about how this fits or expands the existing profile]
```

## What This Observer Does NOT Do

- Ask the user questions (all inference is behavioral)
- Override the user's explicit creative direction
- Delete or downgrade dimensions (only decay confidence)
- Make creative decisions (only updates the profile that other skills read)
- Analyze images the user hasn't explicitly asked to analyze — Tengan inspiration analysis mode only activates on explicit user intent signals
- Weight anti-interest genre images toward the profile (nature, fashion, portraits) unless the user explicitly overrides

## Scope Boundaries

This observer covers **visual aesthetic evolution only**. Prose style tracking belongs to the writing domain's style-dna/style-analyzer system. If both visual and prose dimensions are relevant (e.g., a narrative visualization), each domain's observer tracks its own axes independently.
