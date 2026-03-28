# Delegation Rules — Agent and Skill Routing Logic

## Internal Agent Routing

### Single-Archetype Routing

When the artifact maps cleanly to one archetype, route to the primary agent:

| Archetype | Primary Agent | Supporting Agents |
|-----------|--------------|-------------------|
| Generative | Simulation Smith* | Motion Weaver (for animation timing) |
| Narrative | Narrative Engine | Motion Weaver (for scroll choreography) |
| Data | Data Sculptor | Motion Weaver (for transitions) |
| Interactive | Interaction Architect | Motion Weaver (for feedback), Simulation Smith (for physics) |
| Simulation | Simulation Smith | Data Sculptor (if visualizing sim data) |
| Immersive | Motion Weaver | Simulation Smith (for environmental effects), Narrative Engine (for pacing) |

*\*Note on Generative vs. Simulation:* The taxonomy separates these into distinct archetypes — Generative focuses on algorithmic beauty (flow fields, procedural textures, L-systems), while Simulation focuses on modeling systems (physics, ecosystems, agent-based models). Both route to **Simulation Smith** because the underlying technical skills overlap: noise algorithms, particle management, parameter tuning, and rendering optimization. The Simulation Smith adapts its approach based on the archetype — for Generative, it prioritizes visual aesthetics and the output space; for Simulation, it prioritizes emergent behavior and rule fidelity. If the generative artifact is purely visual with no system modeling, the Simulation Smith focuses on the algorithm catalog in `skills/artifacts/creative-coding/references/algorithm-catalog.md` and visual composition in `skills/artifacts/visual-composer/SKILL.md`.

### Multi-Archetype Routing (Dependency Order)

Launch agents sequentially. Each receives prior agents' output in the Artifact Blueprint.

**Narrative + Data (Scrollytelling):**
```
Data Sculptor → Narrative Engine → Motion Weaver
```
Data encoding first → story structure wraps it → motion polishes transitions.

**Generative + Interactive:**
```
Simulation Smith → Interaction Architect → Motion Weaver
```
Algorithm design first → interaction layer on top → motion smooths the feel.

**Immersive + Narrative:**
```
Narrative Engine → Motion Weaver → Simulation Smith (for environmental effects)
```
Story structure first → choreography second → ambient effects last.

**Data + Simulation:**
```
Simulation Smith → Data Sculptor → Motion Weaver
```
Model first → visualization layer → animation polish.

**Interactive + Generative (Instrument):**
```
Interaction Architect → Simulation Smith → Motion Weaver
```
Input system first → generative engine → responsive feedback.

---

## External Skill Routing

### When to Invoke External Skills

| Condition | External Skill | Why |
|-----------|---------------|-----|
| Artifact needs p5.js with seeded randomness and parameter exploration | `/algorithmic-art` | Specialized in p5.js creative patterns, seed management, and interactive parameter controls |
| Artifact is a multi-component React app with shadcn/ui, state management, routing | `/web-artifacts-builder` | Handles React + Tailwind + shadcn architecture that exceeds single-file scope |
| Artifact needs a cohesive design theme applied (colors, fonts, spacing system) | `/theme-factory` | Provides pre-set and custom themes with systematic color/font tokens |

### How to Pass Context to External Skills

When invoking an external skill, pass the Artifact Blueprint as prefixed context:

```
[MASTER ARTIFICER BLUEPRINT]
Concept: [elevated concept]
Archetype: [type]
Forge Dial: [mode]
The Wow Moment: [description]
Visual Direction: [palette, typography, density, motion]
Technical Approach: [rendering, animation, framework, delivery]
Constraints: [list]
Anti-patterns: [list]
Prior Agent Outputs: [summary of what specialists have established]
[END BLUEPRINT]

[Then the specific request for the external skill follows]
```

The external skill handles **construction**. The Artificer retains **creative direction**.

### Combining External Skills

Some artifacts need multiple external skills in sequence:

**Themed React App:**
```
/theme-factory (establish design tokens) → /web-artifacts-builder (build with those tokens)
```

**Themed Generative Art:**
```
/theme-factory (palette + aesthetic) → /algorithmic-art (build with that palette)
```

**Complex App with Generative Elements:**
```
/algorithmic-art (build generative component) → /web-artifacts-builder (integrate into React app) → /theme-factory (apply unified theme)
```

---

## Concept Alchemist — Special Routing

The Concept Alchemist is always invoked first (Phase 3) and is not part of the construction pipeline. It operates before routing decisions are made.

**Alchemist input:** Raw user request + archetype + Forge Dial
**Alchemist output:** Elevated concept(s) + wow moment + creative direction

The Alchemist's output feeds into the Artifact Blueprint, which then drives all subsequent routing.

---

## When NOT to Delegate

Handle directly in the orchestrator when:

- The user wants to brainstorm concepts (conversation, not construction)
- The artifact is a simple single-technique piece the Artificer can build directly (e.g., a CSS-only animation, a simple scroll effect)
- The user explicitly wants to pair-build step by step rather than receive a complete deliverable
- The request is primarily about modifying an existing artifact (read it first, then edit directly)

---

## Context Threading

When launching sequential agents, pass an **Artifact Context Block** to each. This wraps the Artifact Blueprint (from Phase 3) with additional inter-agent context:

```
ARTIFACT CONTEXT BLOCK
──────────────────────
Blueprint: [full Artifact Blueprint from Phase 3]
Forge Dial: [current mode]
Prior decisions:
  - [Agent 1]: [summary of what they established]
  - [Agent 2]: [summary of what they established]
Current task: [what this agent specifically needs to deliver]
Constraints from prior work: [anything established by earlier agents that constrains this agent]
```

Note: The Artifact Context Block contains the Artifact Blueprint plus prior agent decisions. When SKILL.md says agents receive "the full Artifact Blueprint," it means the Blueprint is included within this wrapping structure.

---

## Escalation

If a specialist agent's output conflicts with the Blueprint:
1. Identify the specific mismatch (mood? technique? density? interaction model?)
2. Re-launch with the constraint explicitly tightened in the Context Block
3. If conflict persists after re-launch, present both options to the user with clear tradeoffs
4. If the user's preference breaks a technical constraint, flag it honestly and propose the nearest achievable alternative
