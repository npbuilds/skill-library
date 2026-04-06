---
name: domain-translator
description: >
  Transfer knowledge, frameworks, and mental models between domains in the skill library.
  Use when a concept from one domain could apply to another, when looking for cross-domain
  leverage, when wanting to understand how two domains relate structurally, or when
  pattern-synthesizer finds an isomorphism that should be actively exploited.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
allowed-tools: Read Glob Grep
---

# Domain Translator — The Linguist

Takes a concept native to one domain and translates it so another domain can use it. Not just noting that "these two things are similar" — actually doing the work of adaptation, reinterpretation, and quality control to make the transfer real.

Pattern-synthesizer finds the threads. Domain-translator pulls them through.

Think of it like translating between natural languages. You don't just swap words — you adapt idioms, restructure sentences, account for cultural context. "Second-level thinking" in investing doesn't translate to worldbuilding by changing "stocks" to "characters." The structural insight (think about what everyone else thinks) transfers, but the application is completely different.

## Core Function

Perform disciplined knowledge transfer between domains. Every translation answers:

1. **What's the source concept?** — The framework, model, or mental tool being transferred
2. **What's the structural core?** — The abstract principle that's domain-independent
3. **How does it apply in the target domain?** — Concrete adaptation, not vague analogy
4. **Where does the translation break?** — Honest limits prevent overextension
5. **What new insight does the transfer produce?** — The payoff: something the target domain didn't see before

## Translation Process

### Step 1 — Identify the Source Concept
Clearly articulate the concept in its native domain. Don't abstract too early — understand it concretely first.

| Component | What to Capture |
|-----------|----------------|
| **Name** | What it's called in the source domain |
| **Function** | What it does — what problem it solves |
| **Mechanism** | How it works — the internal logic |
| **Assumptions** | What has to be true for it to work |
| **Scope** | Where it applies and where it doesn't |

### Step 2 — Extract the Structural Core
Strip away domain-specific language and identify the abstract principle.

| Question | Purpose |
|----------|---------|
| If I removed all domain-specific nouns, what's the verb? | Finds the action/relationship at the core |
| Does this concept exist in other fields under a different name? | Tests whether the structure is truly general |
| What's the minimum description that preserves the insight? | Prevents carrying over domain-specific baggage |

**Example:**
- Source: "Reflexivity" (investing) — market prices influence fundamentals which influence prices, creating a feedback loop
- Structural core: **Self-referential feedback loops where the observation changes the observed**
- This core also appears in: sociology (observer effect), quantum physics (measurement problem), game theory (common knowledge), worldbuilding (prophecy that changes behavior)

### Step 3 — Adapt to Target Domain
Reinterpret the structural core using the target domain's language, concepts, and constraints.

| Adaptation Check | Question |
|-----------------|---------|
| **Language fit** | Does the translation use the target domain's natural vocabulary? |
| **Constraint fit** | Does the target domain have constraints that change how the concept applies? |
| **Scale fit** | Does the concept operate at the same scale in both domains? |
| **Mechanism fit** | Is the causal mechanism the same, or just the pattern? |

### Step 4 — Stress-Test the Translation
Where does the analogy hold, and where does it break?

| Test | Method |
|------|--------|
| **Edge cases** | Apply the translated concept to extreme scenarios in the target domain |
| **Counterexamples** | Look for cases where the target domain behaves differently than the source |
| **Mechanism check** | Is the underlying mechanism actually the same, or is this surface similarity? |
| **Practitioner test** | Would an expert in the target domain find this translation useful or forced? |

### Step 5 — Articulate the Payoff
What does the target domain gain from this translation?

| Payoff Type | Description |
|-------------|------------|
| **New question** | The translation suggests a question nobody in the target domain was asking |
| **New tool** | A methodology from the source domain can be adapted for the target |
| **Warning** | A known failure mode in the source domain might apply to the target |
| **Connection** | The translation creates a new cross-domain edge in the skill library |

## Output Format

```
DOMAIN TRANSLATION — [Source Concept] → [Target Domain]

Source:
  Concept: [name] from [domain]
  Function: [what it does in the source domain]

Structural Core:
  [The domain-independent principle in one sentence]

Translation:
  In [target domain], this maps to: [concrete adaptation]
  Target vocabulary: [how to express this in the target domain's language]

Where It Holds:
  - [Aspect 1 that transfers cleanly]
  - [Aspect 2 that transfers cleanly]

Where It Breaks:
  - [Aspect that doesn't transfer, and why]

Payoff:
  [What the target domain gains — new question, tool, warning, or connection]

Confidence: [High / Medium / Low — how clean is this translation?]
```

## Common Translation Patterns

Recurring transfers that work across many domain pairs:

| Pattern | Source Example | Transfers To | Core Structure |
|---------|--------------|-------------|---------------|
| **Feedback loops** | Market reflexivity (investing) | Narrative pacing (writing), population dynamics (game theory) | Output feeds back as input |
| **Multi-framework analysis** | Ethical dilemma analysis (philosophy) | Investment thesis evaluation (investing) | Apply N lenses, compare conclusions |
| **Stakeholder mapping** | Moral stakeholders (ethics) | Risk factor mapping (investing), character webs (worldbuilding) | Identify all affected parties and their claims |
| **Excavation** | Assumption-excavator (logic) | Values-excavator (ethics), bias-detector (decision-theory) | Surface what's hidden beneath the visible |
| **Quality hierarchies** | Evidence hierarchies (epistemology) | Data quality tiers (data-science), source reliability (research) | Rank inputs by reliability |
| **Regime detection** | Market regimes (investing) | Paradigm shifts (philosophy of science), narrative phases (writing) | Recognize which state the system is in |

## What This Skill Does NOT Do

- **Find patterns** — That's pattern-synthesizer's job. Domain-translator acts on patterns already identified.
- **Judge whether a transfer is good** — It performs the transfer and honestly reports where it breaks. The user decides if it's useful.
- **Force connections** — Not every domain pair has meaningful transfers. If the translation is forced, say so.

## Cross-Domain Connections

- **Neocortex/architecture/pattern-synthesizer**: Synthesizer identifies isomorphisms; translator operationalizes them
- **Neocortex/architecture/clarity-engine**: Translator explains how domains connect; clarity-engine makes the explanation intuitive
- **Neocortex/architecture/growth-architect**: Successful translations create new cross-domain edges that growth-architect should register
- **Philosophy/logic/assumption-excavator**: The excavation pattern is itself a transferable concept
- **Every domain pair**: Domain-translator is inherently cross-domain — it exists at the intersection of any two domains
