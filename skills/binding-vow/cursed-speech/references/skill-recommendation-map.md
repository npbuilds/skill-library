# Skill Recommendation Map (Static)

Canonical task-type → Archon-skill mapping that `cursed-speech` consults when recommending which downstream skills the formulated prompt should invoke. This is the offline-friendly half of the hybrid recommendation strategy; runtime `mcp__skill-library__search_skills` queries provide the dynamic half.

This map is seeded from the current 377-skill library state. **Maintenance:** [[growth-architect]] (neocortex) is the designated maintainer. When a new skill lands that fits a task type below, append a row.

The format is deliberately flat — task type → recommended skill(s) + one-line rationale.

---

## Research and Investigation

| Task signal | Recommended skill(s) | Rationale |
|---|---|---|
| "Investigate X", "research X", "verify X", "fact-check X" | `spelunker` (research) | Full research orchestrator with confidence-tagged findings |
| "Break this down into atomic claims" | `claim-decomposer` (research) | Atomic decomposition with dependency graph + priority tags |
| "Verify this single claim" | `source-triangulator` (research) | Per-claim evidence gathering and triangulation |
| "What's the best approach to X?" (generative) | `agentic-researcher` (research) | Evolutionary candidate generation + evaluation |
| "Synthesize the evidence" | `evidence-synthesizer` (research) | Confidence-tagged research brief assembly |

## Reasoning and Analysis

| Task signal | Recommended skill(s) | Rationale |
|---|---|---|
| "Is this argument valid?" | `argument-analyst` (philosophy/logic) | Validity, soundness, fallacy detection |
| "What hidden assumptions does this make?" | `assumption-excavator` (philosophy/logic) | 6-category assumption surfacing |
| "Challenge this reasoning" | `socratic-examiner` (philosophy/dialectical-tools) | Structured Socratic questioning |
| "What's the strongest opposing view?" | `steel-man-forge` (philosophy/dialectical-tools) | Strongest counter-position |
| "Run thesis/antithesis/synthesis" | `dialectic-engine` (philosophy/dialectical-tools) | Multi-round point-counterpoint |
| "Is this evidence reliable?" | `evidence-evaluator` (philosophy/epistemology) | Source-quality and epistemic-weight assessment |
| "Is this falsifiable?" / "Is this scientific?" | `demarcation-judge` (philosophy/philosophy-of-science) | Popperian falsifiability assessment |
| "What paradigm is operating here?" | `paradigm-analyst` (philosophy/philosophy-of-science) | Kuhn/Lakatos/Popper framework analysis |
| "Whose interests are centered?" | `values-excavator` (philosophy/ethics) | Stakeholder + values surfacing |
| "Map the stakeholders" | `stakeholder-mapper` (philosophy/ethics) | Affected-party identification |

## Decision Theory and Strategic Reasoning

| Task signal | Recommended skill(s) | Rationale |
|---|---|---|
| "Help me decide under uncertainty" | `decision-architect` (philosophy/decision-theory) | Choice structuring, option enumeration |
| "What biases might be affecting me?" | `bias-detector` (philosophy/decision-theory) | Bias-pattern checklist |
| "Run a Bayesian update" | `bayesian-reasoner` (philosophy/decision-theory) | Prior + evidence → posterior |
| "Is this position consistent?" | `belief-auditor` (philosophy/epistemology) | Belief coherence checking |
| "Find a counterfactual" | `counterfactual-reasoner` (philosophy/decision-theory) | Structured what-if analysis |

## Investing and Markets

| Task signal | Recommended skill(s) | Rationale |
|---|---|---|
| "Build / evaluate an investment thesis" | `archon` orchestrator (investing) | Full investing workflow |
| "Construct / rebalance a portfolio" | `portfolio-construction` (investing) | Allocation, sizing, hedging routing |
| "Assess regime / macro environment" | `regime-intelligence` subdomain (investing) | Cycle, monetary, fiscal context |
| "Evaluate market microstructure" | `market-microstructure` (investing) | Flow, dealer hedging, liquidity dynamics |
| "Find special situations" | `special-situations` (investing) | Idiosyncratic risk-reward |

## Biotech / Clinical / Drug Development

| Task signal | Recommended skill(s) | Rationale |
|---|---|---|
| "Evaluate a biotech asset / deal" | `asclepius` (biotech-venture orchestrator) | Full diligence workflow |
| "Assess clinical-trial probability of success" | `probability-of-success` subdomain (biotech-venture) | POS scoring framework |
| "Evaluate regulatory strategy" | `regulatory-strategy` subdomain (biotech-venture) | FDA/EMA pathway analysis |
| "Score competitive intelligence" | `competitive-intelligence` subdomain (biotech-venture) | Comp landscape and positioning |
| "Generate IC memo" | `investment-memo-writer` (biotech-venture) | Memo template with scorecard inputs |

## Writing and Communication

| Task signal | Recommended skill(s) | Rationale |
|---|---|---|
| "Draft prose from a brief" | `prose-writer` (writing) | Voice + form-aware drafting |
| "Revise / polish prose" | `prose-orchestrator` (writing) | Full revision workflow |
| "Critique writing style" | `style-analyzer` (writing/revision-craft) | Sentence-level style diagnosis |
| "Build an argument structure" | `argument-structure` (writing/rhetoric) | Toulmin/Rogerian/classical |
| "Apply rhetorical appeals" | `rhetorical-appeals` (writing/rhetoric) | Ethos/pathos/logos/kairos |
| "Diagnose a sentence" | `sentence-craft` director (writing) | Routing to diction/syntax/rhythm |

## Data and Analysis

| Task signal | Recommended skill(s) | Rationale |
|---|---|---|
| "Run a data-science workflow" | `data-science-orchestrator` (data-science) | Full lifecycle from cleaning to modeling |
| "Wrangle messy data" | `data-wrangling` director (data-science) | Cleaning, transformation, encoding |
| "Build a statistical analysis" | `statistical-analysis` director (data-science) | Tests, intervals, effect sizes |
| "Evaluate a model" | `model-evaluation` (data-science/modeling) | Metrics, validation strategies, calibration |

## Game Theory and Strategic Interaction

| Task signal | Recommended skill(s) | Rationale |
|---|---|---|
| "Analyze a strategic game" | `game-theory-orchestrator` | Full game analysis routing |
| "Find Nash equilibrium" | `classical-games` (game-theory/strategic-foundations) | Equilibrium analysis |
| "Design a mechanism" | `mechanism-design` director (game-theory) | Auction, matching, incentive design |
| "Evaluate signaling/screening" | `signaling-screening` (game-theory/information-economics) | Asymmetric-info analysis |

## Design and User-Facing Work

| Task signal | Recommended skill(s) | Rationale |
|---|---|---|
| "Design something visual" | `design-orchestrator` (design) | Style, palette, typography routing |
| "Brand identity work" | `brand-identity` subdomain (design) | Voice, foundations, identity |

## Worldbuilding and Creative

| Task signal | Recommended skill(s) | Rationale |
|---|---|---|
| "Design a world / setting" | `worldbuilding-orchestrator` | Full worldbuilding workflow |
| "Build an ecosystem" | `ecology-design` (worldbuilding) | Biome + flora + fauna design |

## Meta and Library Management

| Task signal | Recommended skill(s) | Rationale |
|---|---|---|
| "Audit the skill library" | `architecture` director (neocortex) | Coverage, gaps, patterns |
| "Plan what to build next" | `growth-architect` (neocortex) | Sequenced build plans |
| "Translate concepts cross-domain" | `domain-translator` (neocortex) | Pattern transfer |
| "Create a new skill" | `skill-scaffold` (infrastructure) | Skill creation workflow |

## Problem-Statement (Self-Reference)

| Task signal | Recommended skill(s) | Rationale |
|---|---|---|
| "Help me state this problem clearly" | `six-eyes` (binding-vow) | Full problem-statement workflow |
| "Audit this problem statement" | `statement-grader` (binding-vow) | Six-axis grading |
| "Detect XY pattern" | `xy-detector` (binding-vow) | Solution-disguised-as-problem detection |
| "Compress this for an exec / LLM / peer" | `bluf-shaper` / `cursed-speech` / `scqa-formatter` (binding-vow) | Audience-fit compression |

---

## Recommendation Logic

When `cursed-speech` consults this map:

1. **Match on task signal first** — keyword overlap with the downstream task description
2. **Filter by domain availability** — if the user hasn't loaded a domain (e.g., biotech-venture), don't recommend its skills unless the task explicitly invokes them
3. **Cap recommendations at 4** — more than 4 is noise; pick the highest-relevance ones
4. **Prefer orchestrators when the task is broad** — recommend `spelunker` over `claim-decomposer` when the task is "investigate X" rather than "decompose this claim"
5. **Prefer specific skills when the task is narrow** — recommend `argument-analyst` over `philosophy-orchestrator` when the task is "evaluate this argument"

If the runtime `mcp__skill-library__search_skills` query produces a high-confidence skill not in this map, INCLUDE it in the recommendation and flag for [[growth-architect]] to add to the static map next maintenance pass.

---

## Sources

- Skill list current as of 2026-05-10 (377-skill library state, post-binding-vow Phase 4 build)
- Domain definitions from skill-library `mcp__skill-library__get_system_overview`
- [[growth-architect]] is the designated maintainer for additions/edits
