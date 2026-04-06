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

## What This Observer Does NOT Do

- Ask the user questions (all inference is behavioral)
- Override the user's explicit creative direction
- Delete or downgrade dimensions (only decay confidence)
- Make creative decisions (only updates the profile that other skills read)

## Scope Boundaries

This observer covers **visual aesthetic evolution only**. Prose style tracking belongs to the writing domain's style-dna/style-analyzer system. If both visual and prose dimensions are relevant (e.g., a narrative visualization), each domain's observer tracks its own axes independently.
