---
name: diligence-scorecard
description: >
  Generate a comprehensive 8-pillar investment diligence scorecard for a therapeutic
  asset or biotech company by synthesizing clinical, regulatory, competitive,
  manufacturing, IP, financial, team, and computational infrastructure assessments
  into a structured scoring framework with an investment recommendation. Activate
  when producing a complete diligence deliverable or synthesizing all prior analyses
  into a single decision framework.
metadata:
  author: nirav
  version: "1.0"
  innovation: "8th pillar (Computational Infrastructure) reflects $1B+ AI science factory mega-rounds"
compatibility: Designed for Claude Code
allowed-tools: Read, WebSearch, WebFetch
---

# Diligence Scorecard — The Integration Engine

This is the capstone skill of the Asclepius domain. Every other skill produces a component analysis; the diligence scorecard synthesizes all of them into the artifact that venture investors actually produce — a structured, scored assessment with an explicit recommendation. No open-source biotech diligence scorecard exists.

The 8-pillar framework is deliberately opinionated. Seven pillars are standard in biotech diligence. The 8th — Computational Infrastructure — reflects the $1B+ mega-rounds flowing to AI science factories (Xaira $1B, Isomorphic $600M, Lila Sciences $350M) and the growing requirement that founding teams have computational expertise (Dimension Capital). This is where your Formation Bio experience creates maximum differentiation.

## How to Run

### Input

The scorecard consumes outputs from all other Asclepius skills:

| Input Source | Pillar(s) Fed |
|---|---|
| pos-calculator | Pillar 1 (Clinical Strength) |
| endpoint-selection | Pillar 1, Pillar 2 |
| trial-design-optimizer | Pillar 1 |
| regulatory-precedent + pathway-analyzer | Pillar 2 (Regulatory Positioning) |
| regulatory-risk-scorer | Pillar 2 |
| clinical-differentiator + pipeline-mapper | Pillar 3 (Competitive Position) |
| market-dynamics | Pillar 3 |
| cmc-risk-assessor + modality-manufacturing | Pillar 4 (Manufacturing Feasibility) |
| patent-analyzer + ip-valuation | Pillar 5 (IP Fortress) |
| rnpv-modeler + peak-sales-forecaster + deal-economics | Pillar 6 (Financial Attractiveness) |
| User assessment / public information | Pillar 7 (Team & Execution) |
| User assessment / public information | Pillar 8 (Computational Infrastructure) |

If upstream analyses haven't been run, the scorecard can operate with partial information — but must flag which pillars are scored on limited data.

### Steps

#### Step 1 — Score Each Pillar (1-10)

Use the scoring calibration in `references/scoring-calibration.md` for criteria at each level.

**Pillar 1: Clinical Strength (Weight: 20%)**
Assess: PoS from pos-calculator, endpoint quality from endpoint-selection, data maturity, biomarker strategy.
Key question: "Is the clinical evidence compelling enough to justify Phase 3 investment?"

**Pillar 2: Regulatory Positioning (Weight: 15%)**
Assess: Pathway from pathway-analyzer, regulatory risk from regulatory-risk-scorer, designation status, precedent depth.
Key question: "Does the regulatory path to approval have precedent and manageable risk?"

**Pillar 3: Competitive Position (Weight: 15%)**
Assess: Differentiation from clinical-differentiator, landscape from pipeline-mapper, market dynamics.
Key question: "Can this asset win meaningful market share against current and future competitors?"

**Pillar 4: Manufacturing Feasibility (Weight: 10%)**
Assess: CMC risk from cmc-risk-assessor, COGS from modality-manufacturing, scalability.
Key question: "Can this drug be manufactured reliably at commercial scale at acceptable COGS?"

**Pillar 5: IP Fortress (Weight: 10%)**
Assess: Patent landscape from patent-analyzer, IP contribution from ip-valuation, exclusivity periods.
Key question: "Is the IP strong enough to protect commercial returns through peak sales?"

**Pillar 6: Financial Attractiveness (Weight: 15%)**
Assess: rNPV from rnpv-modeler, peak sales from peak-sales-forecaster, deal terms from deal-economics.
Key question: "Does the risk-adjusted return justify the capital at risk?"

**Pillar 7: Team & Execution (Weight: 10%)**
Assess: Management experience, board composition, operational capability, capital adequacy.
Key question: "Can this team execute the development plan and navigate setbacks?"

**Pillar 8: Computational Infrastructure (Weight: 5%)**
Assess: AI/ML platform maturity, proprietary data assets, wet-lab/dry-lab integration, computational team depth.
Key question: "Does this company have computational capabilities that accelerate development or create data moats?"

#### Step 2 — Check for Red Flags

Red flags automatically cap the aggregate score at 4.0:
- Going concern risk (<6 months cash, no financing path)
- Data integrity concerns
- Regulatory rejection (CRL) without clear resubmission path
- Core patent invalidated
- Management exodus (CEO + CSO departed)

#### Step 3 — Check for Green Flags

Green flags add +0.5 to aggregate (cap at 10.0):
- Significant insider buying (>$500K open market)
- Top-tier VC validation (Arch, Flagship, Third Rock)
- Big pharma co-development partnership
- Platform with multiple advancing indications

#### Step 4 — Calculate Aggregate Score

```
Aggregate = Σ (Pillar Score × Weight) + Green Flag Bonus - Red Flag Cap
```

#### Step 5 — Generate Recommendation

| Aggregate | Recommendation | Position Sizing |
|---|---|---|
| 8.0-10.0 | **Strong Buy** | Maximum position (3-5% of fund) |
| 6.5-7.9 | **Buy** | Standard position (1-3% of fund) |
| 5.0-6.4 | **Hold** | Monitor for catalysts; small position if specific thesis |
| 3.5-4.9 | **Cautious** | Below average; avoid unless compelling contrarian thesis |
| 1.0-3.4 | **Avoid** | Fundamental concerns; do not invest |

### Output

```
DILIGENCE SCORECARD — [Company / Asset Name]
Indication: [therapeutic area + indication]
Current Phase: [development stage]
Date: [assessment date]
Analyst: [name]

═══════════════════════════════════════════════

PILLAR SCORES
                                          Score  Weight  Weighted
1. Clinical Strength                      [X/10]   20%    [X.X]
2. Regulatory Positioning                 [X/10]   15%    [X.X]
3. Competitive Position                   [X/10]   15%    [X.X]
4. Manufacturing Feasibility              [X/10]   10%    [X.X]
5. IP Fortress                            [X/10]   10%    [X.X]
6. Financial Attractiveness               [X/10]   15%    [X.X]
7. Team & Execution                       [X/10]   10%    [X.X]
8. Computational Infrastructure           [X/10]    5%    [X.X]
                                         ─────────────────────
                                 AGGREGATE: [X.X / 10.0]

Red Flags: [None / List]
Green Flags: [None / List]
Adjusted Aggregate: [X.X / 10.0]

═══════════════════════════════════════════════

RECOMMENDATION: [Strong Buy / Buy / Hold / Cautious / Avoid]

One-Line Thesis: [Single sentence investment thesis]

Key Catalysts:
  1. [Catalyst + expected date + value impact]
  2. [Catalyst + expected date + value impact]
  3. [Catalyst + expected date + value impact]

Key Risks:
  1. [Risk + probability + impact + mitigant]
  2. [Risk + probability + impact + mitigant]
  3. [Risk + probability + impact + mitigant]

Financial Summary:
  rNPV: $[X]M (range: $[low] - $[high])
  Peak Sales: $[X]B
  PoS (LOA): [X]%
  Next Value Inflection: [event] ([X]x potential)

Pillar-Level Detail:
  Strongest Pillar: [name] ([score]) — [why]
  Weakest Pillar: [name] ([score]) — [why, and what would improve it]

═══════════════════════════════════════════════

DATA COMPLETENESS
  Pillars with full upstream analysis: [list]
  Pillars scored on limited data: [list + what's missing]
  Confidence in aggregate: [High / Medium / Low]
```

## Error Handling

| Scenario | Response |
|---|---|
| Missing upstream analysis for a pillar | Score based on available information; flag as "limited data" in output; widen confidence range |
| Private company (limited public data) | Pillars 7-8 may rely on investor deck + news; note data source limitations |
| Pre-clinical company | Pillars 1, 2, 3 scored conservatively; emphasize platform/team over clinical data |
| Multi-asset company | Score lead asset as primary; note pipeline optionality as green flag |
| User disagrees with a pillar score | Pillar weights are configurable; user can adjust weight to 0% to exclude a pillar |

## Cross-Domain Connections

- **All biotech-venture skills**: This is the integration point — every other skill feeds into at least one pillar
- **Biotech-venture/investment-memo-writer**: Scorecard outputs feed directly into IC memo generation
- **Biotech-venture/portfolio-analyzer**: Individual scorecards feed portfolio-level analysis
- **Investing/archon**: Scorecard parallels Archon's investment thesis evaluation framework
- **Investing/second-level-thinking**: Red/green flag analysis applies contrarian lens
