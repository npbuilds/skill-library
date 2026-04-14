# Cross-Domain Interfaces — How The Loom Engages Each Orchestrator

For each domain, this document specifies: what The Loom asks for, what context it provides, and the canonical engagement patterns.

---

## Design — `design-orchestrator`

**What The Loom asks for:** Aesthetic identity for a product surface, experience design briefs, visual/interaction design, brand expression, motion design.

**What The Loom provides:** Product thesis, target experience description (from vision-architect), emotional intent, competitive context, interface paradigm choice (from paradigm-designer).

**Canonical patterns:**
- `surface/experience-weaver` → design-orchestrator: "Here's what this intelligence should feel like. Design the visual/interaction layer."
- `envision/vision-architect` → design-orchestrator (aesthetic-identity): "What does this intelligence look like when it's thinking?"
- `envision/paradigm-designer` → design-orchestrator: "Which interaction paradigm has what aesthetic implications?"

---

## Data Science — `data-science-orchestrator`

**What The Loom asks for:** Metric definition, behavioral analysis, usage pattern analysis, statistical validation, visualization of product data.

**What The Loom provides:** Product hypothesis to validate, specific analytical questions, what "good" looks like, acceptable evidence thresholds.

**Canonical patterns:**
- `evolve/adaptation-observer` → data-science: "Here's usage data. What's the system doing? How has behavior changed?"
- `seed/feedback-architect` → data-science: "Design metrics for these feedback loops."
- `sense/capability-radar` → data-science (visualization): "Visualize the capability landscape."

---

## Investing — `archon`

**What The Loom asks for:** Market landscape analysis, timing intelligence, option-value thinking, risk assessment, reflexivity analysis on product-market dynamics.

**What The Loom provides:** Product category, comparable products/surfaces, revenue model, time horizon, competitive positioning.

**Canonical patterns:**
- `surface/value-architect` → archon: "What's the market context for pricing this intelligence surface?"
- `sense/signal-reader` → archon: "What market timing signals are relevant?"
- `envision/possibility-mapper` → archon (reflexivity): "Which product possibilities have self-reinforcing adoption dynamics?"

---

## Writing — `prose-orchestrator`

**What The Loom asks for:** Vision articulation, positioning language, launch copy, product narrative craft, documentation, experience voice/tone.

**What The Loom provides:** Product thesis, target audience, voice requirements, competitive context, the narrative to be told.

**Canonical patterns:**
- `envision/vision-architect` → prose-orchestrator: "Craft the vision narrative."
- `surface/experience-weaver` → prose-orchestrator: "Design the voice this intelligence speaks with."
- `synthesize/narrative-keeper` → prose-orchestrator: "Help refine the product narrative."

---

## Game Theory — `game-theory-orchestrator`

**What The Loom asks for:** Incentive analysis, mechanism design for pricing/value exchange, progressive disclosure design, competitive dynamics modeling, retention incentive architecture.

**What The Loom provides:** Player model (who are the agents), action spaces, payoff structures, information asymmetries, desired behavioral outcomes.

**Canonical patterns:**
- `surface/value-architect` → game-theory/mechanism-design: "Design the value exchange mechanism."
- `surface/exposure-strategist` → game-theory: "Design progressive disclosure incentives."
- `evolve/adaptation-observer` → game-theory: "Why are users behaving this way? What incentive is driving it?"
- `seed/constraint-sculptor` → game-theory/mechanism-design: "Design incentive-compatible constraints."

---

## Worldbuilding — `worldbuilding-orchestrator`

**What The Loom asks for:** Systems coherence checks, world-logic validation, scenario modeling for complex product systems.

**What The Loom provides:** System description, rules, constraint boundaries, behavioral expectations, actors.

**Canonical patterns:**
- `seed/condition-designer` → worldbuilding: "Is this system internally coherent? Do the rules produce the intended behaviors?"
- `envision/vision-architect` → worldbuilding: "Stress-test this vision for internal consistency."

---

## Research — `spelunker`

**What The Loom asks for:** Deep research on specific product questions with confidence-tagged evidence. Market data, technology feasibility, user behavior research, competitive intelligence.

**What The Loom provides:** Specific research question, required evidence quality (quick/standard/deep), time budget, what decisions depend on the answer.

**Canonical patterns:**
- `envision/thesis-forge` → spelunker: "Validate the critical assumption in this thesis."
- `sense/signal-reader` → spelunker: "Deep dive on this market signal."
- `sense/frontier-antenna` → spelunker: "Investigate this frontier development in detail."

---

## Neocortex — `neocortex`

**What The Loom asks for:** AI frontier intelligence, scenario planning for technology futures, library capability gap analysis, architecture recommendations.

**What The Loom provides:** Active initiatives, required capabilities, product timeline, what technology bets depend on.

**Canonical patterns:**
- `sense/frontier-antenna` → neocortex/frontier-scanner: "What's the latest? Translate through a product lens."
- `envision/possibility-mapper` → neocortex/scenario-planner: "Stress-test these possibilities against multiple futures."
- `sense/capability-radar` → neocortex/architecture (skill-cartographer): "Map the capability gaps relevant to active products."

---

## Infrastructure — `infrastructure-orchestrator`

**What The Loom asks for:** Registry data, skill health metrics, scaffolding for new skills, testing.

**What The Loom provides:** What product needs are driving the infrastructure request.

**Canonical patterns:**
- `sense/capability-radar` → infrastructure (skill-health, skill-registry): "What's the health of capabilities in domain X?"
- `evolve/pruning-engine` → infrastructure: "Deprecate this skill/capability."

---

## Sommelier — `bacchus`

**What The Loom asks for:** Wine domain expertise when a product touches wine.

**What The Loom provides:** Product context for wine-related features.

**Canonical patterns:**
- Direct routing when a product question is purely wine-related. The Loom adds no value to single-domain wine questions.

---

## Philosophy — `philosophy-orchestrator`

**What The Loom asks for:** Ethical analysis of product decisions, epistemological rigor for assumption testing, decision frameworks when values conflict.

**What The Loom provides:** Product decision context, stakeholders affected, competing values, the specific ethical question.

**Canonical patterns:**
- `envision/paradigm-designer` → philosophy: "What are the ethical implications of this interaction paradigm?"
- `seed/constraint-sculptor` → philosophy: "Are these constraints ethically sound?"
- `surface/interface-philosopher` → philosophy: "How should intelligence present itself to humans?"

---

## Artifacts — `master-artificer`

**What The Loom asks for:** Interactive prototypes, creative coding demonstrations, visual artifacts that show a capability combination in action.

**What The Loom provides:** Capability combination spec, desired demonstration, interaction model, what the prototype should reveal.

**Canonical patterns:**
- `seed/prototype-grower` → master-artificer: "Build a living demo of this capability combination."
