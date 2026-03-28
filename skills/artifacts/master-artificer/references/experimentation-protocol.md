# Experimentation Protocol — The Forge Dial Engine

## Core Principles

Ten principles govern experimentation in the forge. Each is drawn from research across creative studios, generative art, product experimentation, and cognitive psychology.

| # | Principle | Origin |
|---|-----------|--------|
| 1 | Separate divergent and convergent phases — never polish and experiment simultaneously | Google Design Sprints, IDEO |
| 2 | Measure by experiment volume, not success rate | Tom Kelley (IDEO) |
| 3 | Engineer controlled chaos — strict in some dimensions, loose in others | Tyler Hobbs (Fidenza) |
| 4 | Always Be Iterating — prioritize iteration over novelty | Zach Lieberman |
| 5 | Every experiment needs a hypothesis | Lean Startup, Airbnb experimentation culture |
| 6 | Explore the adjacent possible — one step beyond current state | Kauffman / Steven Johnson |
| 7 | Use constraints as creative fuel (1-3 per experiment) | Stanford d.school, design psychology research |
| 8 | Co-create with the user — propose surprises, invite redirection | Human-AI co-creation research |
| 9 | Frame failures as data — psychological safety enables risk-taking | Creativity psychology research |
| 10 | Design for flow — clear micro-goals, rapid feedback, right challenge | Csikszentmihalyi |

---

## The Experimentation Loop

```
    ┌─────────────────────────────────────────────┐
    │                                             │
    │   1. SENSE                                  │
    │   What's at the edge of the adjacent        │
    │   possible? What constraints could          │
    │   fuel creativity here?                     │
    │              │                              │
    │              ▼                              │
    │   2. HYPOTHESIZE                            │
    │   "If I [change X], I expect [Y]            │
    │   because [Z]"                              │
    │   Set 1-3 meaningful constraints            │
    │              │                              │
    │              ▼                              │
    │   3. DIVERGE  ← Chaos Phase                 │
    │   Generate multiple variations rapidly      │
    │   Controlled randomness / parameter play    │
    │   Volume over quality. No judgment.         │
    │   Leave space for happy accidents.          │
    │              │                              │
    │              ▼                              │
    │   4. EVALUATE                               │
    │   Review against hypothesis                 │
    │   Identify surprises and unexpected beauty  │
    │   Separate "interesting failures"           │
    │   from "dead ends"                          │
    │              │                              │
    │              ▼                              │
    │   5. CONVERGE  ← Control Phase              │
    │   Select promising directions               │
    │   Refine with technical excellence           │
    │   QA the output space (Hobbs method)        │
    │   Polish without losing experimental spark  │
    │              │                              │
    │              ▼                              │
    │   6. INTEGRATE                              │
    │   Merge findings into the artifact          │
    │   Update the adjacent possible map          │
    │   Feed learnings back to Step 1             │
    │                                             │
    └─────────────────────────────────────────────┘
```

---

## Forge Dial Modes — Detailed Behavior

### Precise — The Watchmaker

**Philosophy:** Zero surprises. Maximum craft. Every pixel intentional.

**Behavior:**
- Skip the experimentation loop entirely
- Use proven techniques and established patterns
- Follow best practices to the letter
- Concept Alchemist proposes the clearest, most direct interpretation
- No parameter variation — use known-good values
- Anti-slop codex enforced strictly

**When to use:** Client deliverables with strict requirements. Reproductions. Technical demonstrations. When the user says "I know exactly what I want."

---

### Refined — The Goldsmith (Default)

**Philosophy:** Technical excellence with creative taste. The best version of the obvious approach.

**Behavior:**
- Light experimentation — try 1-2 variations during construction
- Concept Alchemist elevates but doesn't transform — finds the elegant version
- Standard technique selection from the matrix
- Anti-slop codex enforced
- One clear wow moment, tastefully integrated

**When to use:** Default. Most artifacts. When the user wants something great but hasn't asked for wild.

---

### Adventurous — The Explorer

**Philosophy:** Push one boundary. Keep everything else solid.

**Behavior:**
- Run one loop of the experimentation cycle
- Concept Alchemist proposes one safe option + one "what if" alternative
- One deliberate constraint is applied (see Constraint Library below)
- Hypothesis is documented: "What if we [X] instead of the conventional [Y]?"
- If the experiment fails, fall back to the safe option gracefully
- Present both options to the user with clear reasoning

**When to use:** When the user is open to something different. "Surprise me a little."

---

### Experimental — The Alchemist

**Philosophy:** Multiple controlled risks. Happy accidents welcomed. The forge runs hot.

**Behavior:**
- Run 2-3 loops of the experimentation cycle
- Concept Alchemist generates 3 divergent concepts with explicit hypotheses
- 2-3 constraints applied from the Constraint Library
- Controlled chaos: strict in some dimensions (palette, typography), loose in others (layout, interaction model, animation choreography)
- Document all experiments in the Experiment Log
- Present the most promising result + the most surprising result to the user
- Interesting failures are shared as "experiments that didn't land but revealed something"

**When to use:** When the user says "go for it", "try something weird", "I want to see what's possible."

---

### Unbound — The Chaos Mage

**Philosophy:** Conventions are optional. Maximum creative latitude. This may produce brilliance or beautiful failure.

**Behavior:**
- Run unlimited experimentation loops
- Concept Alchemist goes wild — cross-domain mashups, convention-breaking, anti-pattern inversion
- Maximum constraint application — 3+ unusual constraints stacked
- Technique selection deliberately ignores the "lightest technology" rule — pick the most *interesting*
- Anti-slop codex inverted — some "slops" become materials (what if we ONLY use gradients? what if EVERYTHING is centered but in a deliberately confrontational way?)
- Full experiment log with detailed learning
- Present with explicit framing: "This is experimental. Here's what worked, what didn't, and what I learned."

**When to use:** Creative R&D. Art for art's sake. When the user explicitly invites chaos. "Break the rules." "Go absolutely wild."

---

## The Constraint Library

Constraints fuel creativity. Apply 1-3 per experiment in Adventurous+ modes.

### Technique Constraints
- **No JavaScript** — pure CSS/HTML only
- **No color** — monochrome, grayscale, or single-hue only
- **No text** — communicate entirely through visual/interactive means
- **Single element** — the entire artifact lives in one DOM element (or one canvas)
- **Under 100 lines** — extreme economy of code
- **No rectangles** — every shape must be non-rectangular

### Conceptual Constraints
- **Synesthesia** — represent one sense through another (sound as color, data as texture, time as spatial position)
- **Inversion** — do the opposite of convention (scroll up, light-to-dark, big-to-small)
- **Living** — the artifact must feel alive (breathing, responding, growing, decaying)
- **Hidden depth** — the surface is simple; interaction reveals layers
- **Temporal** — the artifact changes meaningfully over time (minutes, hours, visits)
- **Physical metaphor** — the digital artifact must feel like a physical material (paper, water, sand, glass, fabric)

### Process Constraints
- **Speed run** — concept to completion in one pass, no revision
- **Additive only** — build up, never delete or redo
- **Remix** — start from an existing artifact and transform it
- **Mashup** — combine two unrelated archetypes (simulation + narrative, data + instrument)

---

## The Experiment Log Format

Document every experiment when Forge Dial is Adventurous or above:

```
EXPERIMENT LOG
──────────────
Forge Dial: [mode]
Artifact: [name/description]

Experiment 1:
  Hypothesis: "If I [change X], I expect [Y] because [Z]"
  Constraints applied: [list]
  What happened: [brief description]
  Surprise: [what was unexpected — even if the experiment "failed"]
  Verdict: KEPT | MODIFIED | DISCARDED
  Why: [reasoning]

Experiment 2:
  ...

Adjacent Possible:
  This work opens the door to: [list of new experiment ideas this generated]

Key Learning:
  [1-2 sentences about what this experimentation session taught]
```

---

## The Adjacent Possible Map

Track how each experiment expands what's possible next. After completing an artifact:

```
CURRENT STATE → ADJACENT POSSIBLE
─────────────────────────────────
[What we built] →
  • [New thing now possible because we built this]
  • [Technique we discovered that could apply elsewhere]
  • [Question this raised that could drive next experiment]
  • [Constraint that worked well and could be reused]
```

This map grows over time, creating a web of creative possibility that informs future work.

---

## Anti-Patterns in Experimentation

Avoid these failure modes:

| Anti-pattern | Description | Fix |
|-------------|-------------|-----|
| **Infinite divergence** | Experimenting forever, never converging | Set a hard limit: max 3 loops, then converge |
| **Polished experiments** | Over-refining during divergent phase | Keep experiments rough. Polish comes in convergence. |
| **Hypothesis-free chaos** | Random variation with no theory | Every experiment needs "If X then Y because Z" |
| **Timid exploration** | Experiments that barely differ from the default | Push further. If it doesn't feel risky, it's not experimental. |
| **Result attachment** | Falling in love with an experiment and ignoring its flaws | The experiment log forces honest evaluation |
| **Solo creation** | Not involving the user in experimental decisions | Present options. The user's surprise is part of the data. |
