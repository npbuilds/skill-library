---
name: regulatory-strategy
description: >
  Direct FDA/EMA pathway analysis, designation eligibility assessment, regulatory precedent
  research, and regulatory risk scoring to the appropriate specialist skill. Activate when
  evaluating a regulatory strategy for a therapeutic asset, assessing eligibility for expedited
  programs, or scoring regulatory risk for diligence purposes. Regulatory strategy can accelerate
  or derail a clinical program — this director ensures pathway choices are grounded in precedent.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
allowed-tools: Read
---

# Regulatory Strategy Director

Regulatory strategy is the bridge between clinical data and market access. The right pathway can cut years off development timelines and hundreds of millions from budgets — Breakthrough Therapy Designation, Accelerated Approval, Priority Review, Orphan Drug designation, and RMAT each offer distinct advantages but come with specific eligibility criteria, post-marketing obligations, and strategic tradeoffs. This director routes regulatory questions to specialist skills that analyze pathways through the lens of precedent rather than aspiration.

## Child Skills

| Skill | Type | When to Use |
|-------|------|-------------|
| pathway-analyzer | action | Analyzing optimal regulatory pathway (505(b)(1), 505(b)(2), BLA), recommending expedited program strategies, modeling timeline impact of different pathway choices, assessing pediatric and global filing strategies |
| regulatory-precedent | knowledge | Researching prior FDA/EMA decisions on the same indication, endpoint, modality, or mechanism — approval histories, complete response letters, advisory committee outcomes, labeling decisions |
| regulatory-risk-scorer | action | Scoring regulatory risk across dimensions (endpoint acceptance risk, CMC risk, safety signal risk, advisory committee risk, post-marketing commitment risk) and producing an aggregate regulatory risk score for diligence |

## Routing Logic

| Question Signal | Route To | Examples |
|-----------------|----------|----------|
| Regulatory pathway, 505(b)(1), 505(b)(2), BLA, NDA, filing strategy, timeline, pediatric, global filing | pathway-analyzer | "What is the fastest path to approval?" / "Should we file a 505(b)(2)?" |
| BTD, Breakthrough Therapy, Fast Track, Accelerated Approval, Orphan, RMAT, Priority Review, designation | pathway-analyzer | "Does this asset qualify for BTD?" / "What are the post-marketing requirements for Accelerated Approval?" |
| Prior approvals, FDA precedent, advisory committee, CRL, labeling, regulatory history | regulatory-precedent | "Has FDA accepted this surrogate endpoint before?" / "What happened at the AdCom for the last drug in this class?" |
| Regulatory risk, risk scoring, regulatory diligence, CMC risk, safety signals, post-marketing risk | regulatory-risk-scorer | "What is the regulatory risk for this asset?" / "Score the regulatory dimensions for diligence" |
| Full regulatory assessment | pathway-analyzer then regulatory-precedent then regulatory-risk-scorer | "Give me a complete regulatory strategy assessment" |

## Multi-Skill Questions

1. **Pathway + Precedent**: "Should we pursue Accelerated Approval for this oncology asset using ORR as the endpoint?"
   - Load regulatory-precedent to research FDA's history of granting Accelerated Approval in the specific tumor type and line of therapy, and whether ORR has been accepted as a surrogate
   - Load pathway-analyzer to model the timeline and strategic implications — Accelerated Approval grants faster access but requires a confirmatory trial, and recent FDA scrutiny has increased the bar
   - Synthesize: Precedent determines feasibility; pathway analysis determines whether it is strategically optimal given the confirmatory trial burden and competitive dynamics

2. **Designation + Risk**: "This company claims BTD eligibility — is that realistic, and what is the regulatory risk profile?"
   - Load pathway-analyzer to assess BTD eligibility against the four criteria (serious condition, substantial improvement, preliminary clinical evidence, available therapies)
   - Load regulatory-risk-scorer to evaluate the full regulatory risk profile beyond just designation eligibility
   - Synthesize: BTD eligibility is necessary but not sufficient. Even with BTD, regulatory risk may be high if the endpoint is novel, the safety database is thin, or CMC is immature.

3. **Full Regulatory Diligence**: "Assess the complete regulatory landscape for this program"
   - Load regulatory-precedent first to establish the historical context
   - Load pathway-analyzer to recommend the optimal strategy given precedent
   - Load regulatory-risk-scorer to produce the quantitative risk assessment
   - Sequence matters: precedent informs pathway choice, and both inform risk scoring

## Curriculum Order

1. **regulatory-precedent** — Foundation. Before recommending any strategy, learn what FDA and EMA have done before. Precedent is the strongest predictor of future regulatory decisions. Know the approval histories, the CRL patterns, the advisory committee dynamics.
2. **pathway-analyzer** — Second. With precedent as context, learn to analyze and recommend regulatory pathways. Understand the eligibility criteria, timeline implications, and strategic tradeoffs of each expedited program.
3. **regulatory-risk-scorer** — Third. With pathway and precedent literacy, learn to quantify regulatory risk across multiple dimensions and produce actionable risk scores for investment diligence.

## Conflict Resolution

| Conflict | Resolution | Reason |
|----------|------------|--------|
| Pathway-analyzer recommends Accelerated Approval but regulatory-precedent shows FDA recently rejected confirmatory data in the same indication | Precedent takes priority — if FDA is signaling skepticism, the Accelerated Approval pathway carries higher conversion risk even if technically eligible | Recent precedent is a stronger signal than eligibility criteria. FDA behavior is path-dependent — a recent rejection in the same space raises the bar for subsequent applicants. |
| Regulatory-risk-scorer gives low risk but pathway-analyzer identifies a novel endpoint with no prior acceptance | Elevate the risk score — novel endpoint acceptance is a binary risk that the aggregate score may underweight | Aggregate risk scores can mask binary risks. Endpoint acceptance is a gate function, not a continuous variable. If the endpoint is rejected, the program must redesign regardless of other risk dimensions. |
| Pathway-analyzer recommends a faster pathway but regulatory-risk-scorer shows the faster path carries higher post-marketing risk | Present both options with explicit tradeoff analysis — speed vs post-marketing burden | Accelerated pathways trade pre-market certainty for post-market obligations. The right choice depends on competitive dynamics, capital position, and the company's ability to run confirmatory trials while commercializing. |

## Scope Boundaries

**This director handles**: All questions about regulatory pathway selection, FDA/EMA strategy, expedited program eligibility, regulatory precedent research, advisory committee analysis, regulatory risk scoring, designation strategy, and post-marketing obligation assessment.

**Route to Asclepius when**:
- The question involves clinical trial design choices driven by regulatory requirements (route to clinical-development)
- The question involves endpoint selection beyond regulatory precedent — i.e., clinical validity (route to clinical-development)
- The question involves regulatory timeline impact on valuation (route to asset-valuation)
- The question involves CMC regulatory risk from a manufacturing perspective (route to manufacturing-ip)
- The question spans multiple diligence pillars and needs orchestrator-level coordination

## Cross-Domain Connections

- **Biotech-venture/pathway-analyzer, regulatory-precedent, regulatory-risk-scorer**: Child skills that execute specialist regulatory analyses
- **Investing/macro-cycles**: Regulatory regimes have cycles — permissive eras (e.g., accelerated approval expansion) alternate with restrictive eras (e.g., post-Aduhelm scrutiny), and recognizing the current regime is critical for pathway strategy
- **Research/spelunker**: Deep research on specific regulatory precedents, advisory committee transcripts, and Complete Response Letter patterns
