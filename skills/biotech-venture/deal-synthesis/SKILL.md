---
name: deal-synthesis
description: >
  Direct diligence scorecard generation, investment memo writing, and portfolio analysis to the
  appropriate specialist skill. Activate when synthesizing a complete investment view on a biotech
  asset, producing a diligence scorecard, drafting an investment memo, or analyzing portfolio-level
  risk and return. Deal synthesis is the capstone of biotech venture diligence — it integrates all
  prior pillar analyses into an actionable investment recommendation.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
allowed-tools: Read
---

# Deal Synthesis Director

Deal synthesis is where diligence becomes decision. Every prior pillar — clinical development, PoS, valuation, regulatory, competitive, manufacturing, and IP — produces component assessments. This director integrates those components into the artifacts that drive investment decisions: the 8-pillar diligence scorecard that quantifies risk across dimensions, the investment memo that articulates the thesis for or against an asset, and the portfolio analyzer that evaluates how an asset fits within an existing portfolio.

## Child Skills

| Skill | Type | When to Use |
|-------|------|-------------|
| diligence-scorecard | action | Building the 8-pillar diligence scorecard — scoring each pillar (clinical, PoS, valuation, regulatory, competitive, manufacturing, IP, team/execution) on a standardized scale, weighting pillars, producing an aggregate score with explicit assumptions |
| investment-memo-writer | action | Drafting investment memos in venture format — thesis statement, key risks, key catalysts, valuation summary, recommendation, and the "what has to go right" / "what could go wrong" framework that structures investment committee presentations |
| portfolio-analyzer | action | Analyzing how a new asset fits within an existing portfolio — correlation analysis, therapeutic area concentration, phase diversification, modality mix, PoS-weighted expected value contribution, and portfolio-level risk metrics |

## Routing Logic

| Question Signal | Route To | Examples |
|-----------------|----------|----------|
| Diligence scorecard, pillar scores, diligence scoring, risk scoring, aggregate score | diligence-scorecard | "Build me a diligence scorecard for this asset" / "Score this program across all pillars" |
| Investment memo, thesis, recommendation, investment committee, IC memo, deal memo | investment-memo-writer | "Write the investment memo for this asset" / "Draft the IC presentation" |
| Portfolio fit, portfolio analysis, concentration, diversification, portfolio risk, correlation | portfolio-analyzer | "How does this asset fit in our portfolio?" / "Are we overconcentrated in oncology?" |
| Scorecard + memo | diligence-scorecard then investment-memo-writer | "Full diligence package for IC" |
| Scorecard + portfolio | diligence-scorecard then portfolio-analyzer | "Score this deal and assess portfolio fit" |
| Complete deal package | All three in sequence | "Prepare the full investment package" |

## Multi-Skill Questions

1. **Scorecard + Memo**: "Prepare the IC materials for this asset"
   - Load diligence-scorecard to produce the quantitative assessment across all 8 pillars
   - Load investment-memo-writer to translate the scorecard into a narrative investment memo with thesis, risks, catalysts, and recommendation
   - Synthesize: The scorecard provides the analytical backbone; the memo provides the narrative that communicates the investment thesis to the committee. The memo must be consistent with the scorecard — a low-scoring pillar must appear as a key risk.

2. **Scorecard + Portfolio**: "Should we do this deal given our current portfolio?"
   - Load diligence-scorecard for the standalone asset assessment
   - Load portfolio-analyzer to evaluate portfolio fit — does this asset add diversification or increase concentration? What is the incremental portfolio-level expected value?
   - Synthesize: A strong standalone scorecard does not mean the deal is right for the portfolio. A portfolio already concentrated in the same therapeutic area, phase, or modality may benefit more from a lower-scoring but diversifying asset.

3. **Full Deal Package**: "Everything I need for the investment committee"
   - Load diligence-scorecard for quantitative assessment
   - Load portfolio-analyzer for portfolio context
   - Load investment-memo-writer to produce the final memo incorporating both standalone and portfolio perspectives
   - This is the complete deal synthesis workflow — scorecard grounds the analysis, portfolio provides context, memo delivers the recommendation

## Curriculum Order

1. **diligence-scorecard** — Foundation. Before writing memos or analyzing portfolios, learn to score assets rigorously. The scorecard framework forces structured thinking across all pillars and prevents anchoring on a single dimension (usually clinical data).
2. **investment-memo-writer** — Second. With scoring literacy, learn to translate quantitative assessment into persuasive narrative. The memo is the communication layer — it must convey conviction, acknowledge uncertainty, and provide a clear recommendation.
3. **portfolio-analyzer** — Third. With standalone assessment capability, learn to think at the portfolio level. Individual deal quality is necessary but not sufficient — portfolio construction, diversification, and capital allocation determine fund-level returns.

## Conflict Resolution

| Conflict | Resolution | Reason |
|----------|------------|--------|
| Diligence-scorecard gives a strong score but portfolio-analyzer shows high concentration risk | Present both assessments transparently — the deal may be strong standalone but wrong for the portfolio | Fund-level returns depend on portfolio construction, not just deal quality. A great deal that increases concentration in a failing therapeutic area may harm the portfolio. The IC needs both perspectives. |
| Investment-memo-writer recommends "pass" but diligence-scorecard gives above-threshold scores | Review whether the memo identified qualitative risks not captured in the scorecard (team, governance, capital structure) | The scorecard captures quantifiable dimensions but may miss qualitative factors. The memo writer may have identified deal-breakers (misaligned management incentives, litigation risk, governance concerns) that should be added to the scorecard framework. |
| Portfolio-analyzer suggests the asset adds diversification but diligence-scorecard shows weak fundamentals | Standalone quality takes priority over portfolio diversification — do not invest in weak assets for diversification | Diversification is a portfolio benefit, not an investment thesis. A weak asset diversifies the portfolio's risk exposure but also adds a negative expected value position. True diversification comes from finding strong assets in underrepresented areas. |

## Scope Boundaries

**This director handles**: All questions about diligence scorecard construction, investment memo drafting, portfolio fit analysis, investment recommendation synthesis, IC material preparation, deal evaluation, and portfolio-level risk and return assessment for biotech venture investments.

**Route to Asclepius when**:
- The question requires deeper analysis on any individual diligence pillar (route to the relevant director: clinical-development, probability-of-success, asset-valuation, regulatory-strategy, competitive-intelligence, or manufacturing-ip)
- The scorecard requires updated inputs from pillar-specific analysis
- The question involves general venture fund strategy beyond individual deal evaluation
- The question spans multiple diligence pillars and needs orchestrator-level coordination for the underlying analysis

## Cross-Domain Connections

- **Biotech-venture/diligence-scorecard, investment-memo-writer, portfolio-analyzer**: Child skills that produce the core deal synthesis artifacts
- **Investing/event-driven**: Deal analysis parallels event-driven investing — catalyst identification, binary outcome assessment, and asymmetric risk-reward framing
- **Investing/archon**: Deal synthesis is the biotech equivalent of investment thesis formation — integrating multiple analytical dimensions into an actionable recommendation
