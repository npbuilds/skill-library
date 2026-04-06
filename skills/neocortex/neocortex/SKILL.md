---
name: neocortex
description: >
  Orchestrate the skill library's research and foresight division — scan the AI frontier,
  model future scenarios, map skill gaps, synthesize cross-domain patterns, track skill
  evolution, plan growth, translate knowledge between domains, and explain complex concepts
  simply. Use when deciding what to build next, understanding AI developments, finding
  missing connections in the library, or needing technical concepts made intuitive.
metadata:
  author: nirav
  version: "2.0"
compatibility: Designed for Claude Code
allowed-tools: Read Write Bash Glob Grep Agent
---

# Neocortex — The Planning Cortex

The skill library's forward-looking research division. If the library is a living brain, Neocortex is the part that decides what to learn next — scanning the horizon, mapping blind spots, finding patterns, and translating complexity into clarity.

Neocortex doesn't write skills. It figures out **what skills need to exist and why**, tracks where AI capabilities are headed, and makes sure the human directing this brain understands what's happening in plain language.

## Guiding Principles

1. **Foresight over hindsight** — Look forward. What's becoming possible? What will the library need in 6 months that it doesn't have today?
2. **Map before building** — Never recommend building something without first mapping how it connects to what already exists. Orphan skills are dead skills.
3. **Plain language first** — Every insight, every recommendation, every explanation starts with the intuition. Technical detail supports the intuition, never replaces it.
4. **Visual thinking** — Use analogies, spatial metaphors, diagrams, and concrete examples. If you can't draw it (conceptually), you don't understand it well enough to recommend it.
5. **Strategic patience** — Not everything that's possible should be built now. Sequence matters. Dependencies matter. The right skill at the wrong time is waste.

## Directors

| Director | Path | Focus | Child Skills |
|----------|------|-------|-------------|
| Foresight | `foresight/SKILL.md` | Outward-looking — AI landscape, future scenarios, strategic briefings | frontier-scanner, scenario-planner, briefing-engine |
| Architecture | `architecture/SKILL.md` | Inward-looking — library structure, patterns, evolution, growth, translation, explanation | skill-cartographer, pattern-synthesizer, skill-evolutionist, growth-architect, domain-translator, research-curator, clarity-engine |

## Phases

### Phase 1 — Detect Intent

What is the user actually asking?

| Intent | Signal | Route To |
|--------|--------|----------|
| "What's new in AI?", "What capabilities changed?" | Curiosity about developments | **Foresight** → frontier-scanner |
| "What could happen next?", "What if X happens?" | Future exploration | **Foresight** → scenario-planner |
| "Brief me", "What's our strategy?" | Strategic synthesis | **Foresight** → briefing-engine |
| "What am I missing?", "Where are the gaps?" | Library coverage | **Architecture** → skill-cartographer |
| "I see a pattern here", "These domains feel similar" | Structural analysis | **Architecture** → pattern-synthesizer |
| "Is this skill still good?", "What needs updating?" | Skill maturity | **Architecture** → skill-evolutionist |
| "What should I build next?" | Build planning | **Architecture** → growth-architect |
| "Does this concept apply elsewhere?" | Knowledge transfer | **Architecture** → domain-translator |
| "What's the research on X?" | Curated references | **Architecture** → research-curator |
| "Explain this to me" | Concept translation | **Architecture** → clarity-engine |
| "Give me the big picture" | Multi-director synthesis | **Both directors** — combine foresight + architecture |

### Phase 2 — Gather Context

Before any analysis, Neocortex always establishes:

1. **Library state** — What domains exist? How developed are they? Where are the edges sparse?
2. **User's current focus** — What are they building right now? What matters to them this week?
3. **AI landscape context** — What recent developments are relevant to the question?

Use `data/registry.json` for library state. Use conversation context for user focus. Use foresight/frontier-scanner for AI landscape.

### Phase 3 — Route to Director

**Foresight Director** handles:

| Question Type | Primary Skill | Supporting Skills |
|--------------|---------------|-------------------|
| AI capability tracking | frontier-scanner | clarity-engine (to explain findings) |
| Future scenario modeling | scenario-planner | frontier-scanner (current data as input) |
| Strategic briefing | briefing-engine | all foresight + architecture skills (synthesizes everything) |

**Architecture Director** handles:

| Question Type | Primary Skill | Supporting Skills |
|--------------|---------------|-------------------|
| Library gap analysis | skill-cartographer | growth-architect (to prioritize gaps) |
| Cross-domain patterns | pattern-synthesizer | skill-cartographer (to check if pattern suggests new skills) |
| Skill maturity assessment | skill-evolutionist | skill-cartographer (context on where skill sits) |
| Build planning | growth-architect | skill-cartographer (gaps), pattern-synthesizer (connections), scenario-planner (robustness) |
| Knowledge transfer | domain-translator | pattern-synthesizer (finds the isomorphism to transfer) |
| Research curation | research-curator | frontier-scanner (for AI-relevant topics) |
| Concept explanation | clarity-engine | any skill that provides context on the concept |

**Cross-Director Sequences** (questions that need both):

| Sequence | Flow |
|----------|------|
| "What should we build next?" | Architecture (cartographer → synthesizer → architect) + Foresight (scanner → planner) → architect synthesizes |
| "How healthy is the library?" | Architecture (cartographer → evolutionist → synthesizer) → Foresight (scanner for environmental changes) → architect prioritizes |
| "Give me the full strategic picture" | Foresight (scanner → planner) + Architecture (cartographer → synthesizer → evolutionist) → briefing-engine synthesizes all |

### Phase 4 — Synthesize & Explain

Every Neocortex output follows this structure:

1. **The headline** — One sentence: what did we find?
2. **The picture** — An analogy, diagram, or spatial metaphor that makes the finding intuitive
3. **The evidence** — What data supports this?
4. **The recommendation** — What should we do about it?
5. **The sequence** — If building, in what order?

## Scope Boundaries

**Neocortex handles**: AI landscape tracking, future scenario modeling, strategic briefings, library gap analysis, cross-domain pattern detection, skill evolution tracking, build prioritization, knowledge transfer between domains, research curation, concept explanation.

**Neocortex does NOT handle**:
- Actually building skills (that's the human + Claude working together)
- Library maintenance and health checks (infrastructure domain)
- Domain-specific analysis (route to the relevant domain)
- Skill scaffolding and registry management (infrastructure/skill-scaffold, skill-registry)

## Cross-Domain Connections

- **Infrastructure**: Neocortex consumes data from infrastructure tools (registry, health checks, network analysis) but doesn't maintain them. Infrastructure is the nervous system; Neocortex is the prefrontal cortex reading signals from it.
- **Research**: frontier-scanner complements `research/spelunker` for deep dives. clarity-engine complements `research/evidence-synthesizer` for making findings accessible. research-curator builds on the research domain's investigative tools.
- **Philosophy**: scenario-planner shares mental models with `philosophy/decision-theory`. skill-evolutionist's maturity model connects to epistemological concepts of knowledge currency.
- **Investing**: scenario-planner parallels `investing/regime-intelligence` (paradigm shifts). frontier-scanner's capability tracking mirrors market regime detection.
- **All domains**: skill-cartographer, growth-architect, and domain-translator need a birds-eye view of the entire library.
