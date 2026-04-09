---
name: competitive-intelligence
description: >
  Direct pipeline mapping, clinical differentiation analysis, and market dynamics questions to
  the appropriate specialist skill. Activate when evaluating an asset's competitive position,
  mapping the pipeline in a therapeutic area, assessing first-mover vs fast-follower dynamics,
  or analyzing indication sequencing strategy. Competitive position determines market share,
  which determines peak sales, which determines value.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
allowed-tools: Read
---

# Competitive Intelligence Director

No biotech asset exists in isolation. The competitive landscape determines achievable market share, pricing power, differentiation requirements, and indication sequencing. A clinically superior molecule entering a saturated market may generate less value than a good-enough molecule in an underserved indication. This director routes competitive questions to specialist skills that map pipelines systematically, quantify clinical differentiation, and model market dynamics with rigor rather than wishful thinking.

## Child Skills

| Skill | Type | When to Use |
|-------|------|-------------|
| pipeline-mapper | action | Mapping all clinical-stage competitors in a therapeutic area by phase, mechanism, modality, and expected timeline — building the competitive landscape table that anchors all differentiation analysis |
| clinical-differentiator | action | Analyzing head-to-head or cross-trial differentiation on efficacy, safety, dosing convenience, route of administration, onset of action, and durability — quantifying whether an asset is truly differentiated vs me-too |
| market-dynamics | knowledge | Understanding market structure — first-mover vs fast-follower dynamics, indication sequencing strategy, pricing and access dynamics, formulary positioning, physician adoption patterns, and switching behavior |

## Routing Logic

| Question Signal | Route To | Examples |
|-----------------|----------|----------|
| Pipeline, competitors, competitive landscape, clinical-stage programs, what else is in development | pipeline-mapper | "Map the competitive landscape in NASH" / "Who else is targeting IL-31?" |
| Differentiation, head-to-head, better than, clinical superiority, me-too, best-in-class, first-in-class | clinical-differentiator | "Is this drug differentiated from dupilumab?" / "What is the clinical differentiation story?" |
| Market share, first-mover, fast-follower, pricing, formulary, physician adoption, switching, market dynamics | market-dynamics | "Is first-mover advantage real in this indication?" / "What drives physician switching in oncology?" |
| Landscape + differentiation | pipeline-mapper then clinical-differentiator | "Where does this asset fit in the competitive landscape?" |
| Differentiation + market implications | clinical-differentiator then market-dynamics | "If this drug is marginally better, does that matter commercially?" |
| Full competitive assessment | All three in sequence | "Complete competitive analysis for this therapeutic area" |

## Multi-Skill Questions

1. **Landscape + Differentiation**: "Where does this asset rank against competitors?"
   - Load pipeline-mapper to build the complete competitive landscape with timelines and mechanisms
   - Load clinical-differentiator to position the asset within the landscape on key dimensions (efficacy, safety, convenience)
   - Synthesize: Rank the asset against each competitor on the dimensions that matter most for the specific indication and patient population

2. **Differentiation + Market**: "Is marginal differentiation enough to win share?"
   - Load clinical-differentiator to quantify the degree of differentiation (e.g., 15% improvement in response rate, better safety profile, oral vs injectable)
   - Load market-dynamics to assess whether that degree of differentiation translates into meaningful market share given physician adoption patterns, formulary dynamics, and switching costs
   - Synthesize: Marginal efficacy gains may not drive switching if the standard of care is entrenched and convenient. Differentiation on safety or convenience can matter more than efficacy in some markets.

3. **Full Competitive Diligence**: "Give me the complete competitive picture"
   - Load pipeline-mapper for the landscape
   - Load clinical-differentiator for positioning
   - Load market-dynamics for commercial implications
   - Integrate: The landscape tells you who you are competing with. Differentiation tells you whether you can win. Market dynamics tells you what winning is worth.

## Curriculum Order

1. **pipeline-mapper** — Foundation. You cannot assess differentiation without knowing the competitive set. Pipeline mapping is the prerequisite. Learn to build comprehensive landscape tables organized by mechanism, phase, and timeline.
2. **clinical-differentiator** — Second. With the landscape mapped, learn to analyze differentiation. Understand cross-trial comparison methodology, the limitations of indirect comparisons, and how to quantify differentiation across multiple dimensions.
3. **market-dynamics** — Third. With differentiation established, learn how it translates into commercial outcomes. First-mover advantage, switching behavior, formulary access, and pricing dynamics determine whether clinical differentiation converts to market share.

## Conflict Resolution

| Conflict | Resolution | Reason |
|----------|------------|--------|
| Clinical-differentiator shows clear superiority but market-dynamics suggests the market is locked up by an entrenched incumbent | Market-dynamics takes priority for commercial projections; clinical-differentiator still matters for long-term positioning | Even clearly superior drugs can struggle against entrenched incumbents with strong formulary positions, established KOL relationships, and patient inertia. Clinical superiority is necessary but not sufficient for commercial success in established markets. |
| Pipeline-mapper shows many competitors but clinical-differentiator argues the asset is meaningfully differentiated from all of them | Verify that the differentiation is durable — check whether later-stage competitors could close the gap and whether the differentiation dimensions matter to prescribers | Differentiation is dynamic. A best-in-class position today may be a me-too position in 18 months if later-stage competitors have similar or better profiles. Durability of differentiation is as important as current differentiation. |
| Market-dynamics suggests first-mover advantage is strong but pipeline-mapper shows a competitor is only 6 months behind | Assess whether 6 months is enough to establish the prescribing habit, formulary position, and KOL mindshare that sustain first-mover advantage | First-mover advantage accrues over time through clinical experience and formulary inertia. A 6-month lead may be sufficient in some markets (rare disease) but insufficient in others (large primary care markets with aggressive generic/biosimilar entry). |

## Scope Boundaries

**This director handles**: All questions about competitive landscape mapping, pipeline analysis, clinical differentiation assessment, market dynamics modeling, first-mover vs fast-follower strategy, indication sequencing, physician adoption, formulary positioning, and competitive readthrough for biotech assets.

**Route to Asclepius when**:
- The question involves competitive readthrough to PoS adjustment (route to probability-of-success)
- The question involves competitive dynamics driving market share inputs for peak sales (route to asset-valuation)
- The question involves clinical trial design for differentiation purposes (route to clinical-development)
- The question involves regulatory strategy driven by competitive timing (route to regulatory-strategy)
- The question spans multiple diligence pillars and needs orchestrator-level coordination

## Cross-Domain Connections

- **Biotech-venture/pipeline-mapper, clinical-differentiator, market-dynamics**: Child skills that execute the component analyses for competitive assessment
- **Game-theory/classical-games**: Competitive dynamics in therapeutic markets map to strategic games — first-mover advantage, market entry timing, and indication sequencing are game-theoretic decisions
- **Investing/second-level-thinking**: Howard Marks's contrarian framework applied to competitive consensus — where the market overweights or underweights competitive threats
