---
name: investment-memo-writer
description: >
  Generate structured investment committee memos from diligence scorecard outputs.
  Template covers Executive Summary through Recommendation with assertion-led writing,
  quantified claims, and explicit assumptions. Translates quantitative pillar scores
  into persuasive narrative with clear thesis, risk/mitigant framework, and actionable
  recommendation. Activate when producing the written investment deliverable.
metadata:
  author: nirav
  version: "1.0"
  parent: deal-synthesis
compatibility: Designed for Claude Code
allowed-tools: Read, WebSearch, WebFetch
---

# Investment Memo Writer — From Scorecard to Narrative

The investment memo is the communication layer of diligence. A diligence scorecard quantifies risk across pillars; the memo translates that quantification into a narrative that conveys conviction, acknowledges uncertainty, and provides a clear recommendation. The best memos do not merely report findings — they argue a thesis, identify what has to go right, and make the investment committee's decision easier.

Writing convention: assertion-led, quantified, explicit about assumptions. Every paragraph opens with the conclusion, not the evidence. Numbers before adjectives. State what you assumed, not just what you concluded.

## How to Run

### Input

| Parameter | Source | Required? |
|---|---|---|
| Completed diligence scorecard | diligence-scorecard | Yes |
| Asset name and company | User | Yes |
| Deal terms (if available) | User / deal-economics | Recommended |
| Portfolio context (if available) | portfolio-analyzer | Optional |
| Investment thesis or hypothesis | User | Recommended |

### Steps

#### Step 1 — Assemble the Memo Structure

The IC memo follows a fixed 12-section template. Each section has specific content requirements and writing conventions:

```
INVESTMENT MEMORANDUM — [Company / Asset Name]
Date: [date]
Author: [analyst]
Recommendation: [Strong Buy / Buy / Hold / Pass]

TABLE OF CONTENTS
1.  Executive Summary
2.  Investment Thesis
3.  Science Overview
4.  Clinical Development Plan
5.  Regulatory Strategy
6.  Competitive Landscape
7.  Commercial Opportunity
8.  Financial Model Summary
9.  Key Risks and Mitigants
10. Team Assessment
11. Deal Terms
12. Recommendation
```

#### Step 2 — Write Each Section

**Section 1 — Executive Summary (1 page max)**

The executive summary must be self-contained — a reader who reads only this page should understand the asset, the thesis, the key risk, and the recommendation.

Structure:
- Opening assertion: One sentence stating the recommendation and why
- Asset description: Molecule, target, modality, indication, current phase (2-3 sentences)
- Key value drivers: The 2-3 reasons this is attractive (or not)
- Key risk: The single most important risk (1-2 sentences)
- Financial summary: rNPV, peak sales, deal terms, implied return
- Scorecard summary: Aggregate score and pillar highlights

Writing rule: No more than 300 words. Every sentence must earn its place.

**Section 2 — Investment Thesis (0.5 pages)**

The thesis is the core argument — why this investment should (or should not) be made. Frame as:

```
WHAT HAS TO GO RIGHT:
1. [Clinical milestone] — [probability and timeline]
2. [Regulatory milestone] — [pathway and precedent]
3. [Commercial milestone] — [market share assumption and basis]

WHAT COULD GO WRONG:
1. [Key clinical risk] — [impact if realized]
2. [Key competitive risk] — [impact if realized]
3. [Key execution risk] — [impact if realized]
```

**Section 3 — Science Overview (1-1.5 pages)**

Cover the biological rationale, mechanism of action, and preclinical evidence. Write for a sophisticated non-specialist: the IC member is an investor, not a biologist.

Requirements:
- Target and pathway biology in 3-4 sentences (accessible language)
- Mechanism of action — how the drug works (avoid jargon where possible)
- Preclinical evidence supporting the mechanism (efficacy signals, biomarker data)
- Key scientific uncertainty — what remains unproven
- Translation risk — how well does preclinical signal predict clinical success for this target class?

**Section 4 — Clinical Development Plan (1-1.5 pages)**

Summarize clinical program status and forward plan:
- Completed trials: Design, N, key efficacy and safety results
- Ongoing trials: Phase, enrollment status, expected data readout
- Planned trials: Registration strategy, pivotal trial design
- Endpoint analysis: Primary endpoint, clinical meaningfulness, regulatory acceptability
- Patient population: Size, identification, enrollment feasibility

Pull from: clinical-development and endpoint-selection skills.

**Section 5 — Regulatory Strategy (0.5-1 page)**

- Regulatory pathway: Standard NDA/BLA, 505(b)(2), accelerated approval, breakthrough
- Designations: Fast Track, Breakthrough, Orphan, REMS
- Precedent: Similar drugs approved via this pathway? Advisory committee dynamics
- Timeline: Expected filing date and approval date
- Risk: Key regulatory uncertainty (endpoint acceptance, safety requirements, label scope)

Pull from: regulatory-strategy and regulatory-precedent skills.

**Section 6 — Competitive Landscape (1-1.5 pages)**

- Current standard of care and its limitations
- Pipeline competitors: phase, timeline, differentiation
- Competitive positioning matrix (from pipeline-mapper)
- First-mover vs fast-follower assessment
- Market archetype (from market-dynamics)

Pull from: competitive-intelligence director skills.

**Section 7 — Commercial Opportunity (1 page)**

- Total addressable market and penetration assumptions
- Peak sales estimate with explicit assumptions (patient population x treatment rate x price x market share)
- Revenue ramp profile and timeline to peak
- Pricing and reimbursement strategy
- Geographic revenue split (US / EU / ROW)

Pull from: peak-sales-forecaster and market-dynamics skills.

**Section 8 — Financial Model Summary (0.5-1 page)**

- rNPV base case and range (P25 / P50 / P75)
- Key input sensitivities (tornado diagram summary)
- Development cost remaining
- IRR at current deal terms
- Platform optionality value (if applicable)

Pull from: rnpv-modeler and deal-economics skills.

**Section 9 — Key Risks and Mitigants (1 page)**

Structure as a risk/mitigant table. Every risk must have a corresponding mitigant or acknowledgment that the risk is unmitigated.

```
| # | Risk | Severity | Probability | Mitigant | Residual Risk |
|---|------|----------|-------------|----------|---------------|
| 1 | [risk] | [H/M/L] | [H/M/L] | [mitigant or "Unmitigated"] | [assessment] |
| 2 | [risk] | [H/M/L] | [H/M/L] | [mitigant] | [assessment] |
```

Include risks from all 8 scorecard pillars. The top 3 risks should map to the lowest-scoring pillars. Red flags from the scorecard must appear here.

**Section 10 — Team Assessment (0.5 pages)**

- CEO and C-suite track record (prior exits, drug approvals, fundraising)
- Clinical development leadership (relevant therapeutic area experience)
- CMC/manufacturing leadership (relevant modality experience)
- Board composition (strategic investors, industry advisors)
- Key person risk (is the team dependent on a single individual?)

**Section 11 — Deal Terms (0.5 pages)**

- Deal structure: Equity (Series A/B/C), licensing, partnership, acquisition
- Valuation: Pre-money, post-money, price per share
- Terms: Liquidation preference, anti-dilution, board seats, protective provisions
- Capital sufficiency: Does this raise fund the company to the next value inflection?
- Implied ownership at exit (dilution modeling through subsequent rounds)

Pull from: deal-economics skill.

**Section 12 — Recommendation (0.5 pages)**

Clear, concise recommendation:
- Rating: Strong Buy / Buy / Hold / Pass
- Investment amount recommendation (if Buy/Strong Buy)
- Key catalyst that could change the recommendation
- Timeline for re-evaluation
- Conditions or contingencies (if any)

### Output

The complete memo as formatted text following the 12-section template. Target length: 8-12 pages total.

```
MEMO QUALITY CHECKLIST:
[ ] Executive summary is self-contained and <300 words
[ ] Thesis has explicit "what has to go right" / "what could go wrong"
[ ] Every quantitative claim has a stated source or assumption
[ ] Risk table includes mitigants for all identified risks
[ ] Recommendation is clear and actionable
[ ] Scorecard pillar scores are consistent with narrative
[ ] No unsubstantiated superlatives ("best-in-class" without data)
[ ] Formatting is consistent (headers, tables, numbering)
```

## Writing Conventions

**Assertion-led:** "Peak sales will reach $1.2B by Year 7 based on 25% share of a 120,000-patient market at $40K/year." NOT "After analyzing the market, we believe there may be potential for significant peak sales."

**Quantified:** "Phase 2 data showed 45% ORR vs 28% for SOC (p=0.003, N=180)." NOT "Phase 2 data was positive and exceeded the standard of care."

**Explicit assumptions:** "We assume 30% market share based on the Archetype 2 (fast-follower) framework, which benchmarks to dupilumab's penetration curve in atopic dermatitis." NOT "We assume reasonable market share."

**Risk-balanced:** For every bullish claim, acknowledge the bear case. For every risk, articulate the mitigant. The IC expects intellectual honesty, not salesmanship.

## Error Handling

| Scenario | Response |
|---|---|
| Scorecard not available | Cannot proceed — the memo requires scorecard as input. Generate scorecard first. |
| Missing pillar data (e.g., no team assessment) | Write the section with available information; flag gaps explicitly as "[Data not available — requires primary diligence]" |
| Conflicting signals across pillars | Present both sides transparently; do not resolve contradictions by ignoring one side |
| Deal terms not finalized | Write the memo with placeholder terms; note sensitivity of recommendation to final terms |

## Cross-Domain Connections

- **deal-synthesis/diligence-scorecard**: Primary input — scorecard provides the quantitative backbone
- **deal-synthesis/portfolio-analyzer**: Portfolio context adds a "fit" dimension to the recommendation
- **All pillar skills**: Each section draws from the relevant pillar skill's output
- **asset-valuation/deal-economics**: Deal terms section depends on deal economics analysis
