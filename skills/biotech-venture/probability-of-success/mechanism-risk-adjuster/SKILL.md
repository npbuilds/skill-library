---
name: mechanism-risk-adjuster
description: >
  Assess mechanism-of-action-specific risk factors that modify base-rate PoS,
  evaluating target validation depth using Mendelian randomization evidence,
  preclinical translatability, competitive mechanism validation, safety class
  effects, and biotech reflexivity to produce auditable adjustment factors.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
allowed-tools: Read, WebSearch, WebFetch
---

# Mechanism Risk Adjuster — The Target Conviction Engine

Base-rate PoS tells you what the average drug does. But drugs are not average — they hit specific targets through specific mechanisms, and the depth of target validation is the single largest predictor of clinical success. A target with Mendelian randomization evidence has roughly 2x the likelihood of approval compared to targets without genetic support (Nelson et al., Nature Genetics 2015; King et al., Nature Communications 2020). This skill systematically evaluates mechanism-specific risk factors and produces adjustment multipliers that feed into the PoS Calculator.

The critical innovation here is combining genetic epidemiology (MR evidence), competitive intelligence (mechanism validation from other molecules), and capital market dynamics (reflexivity) into a single structured adjustment framework.

## How to Run

### Input

| Parameter | Required? | Example |
|---|---|---|
| Drug target(s) | Yes | PCSK9, GLP-1R, CD20 |
| Mechanism of action | Yes | Monoclonal antibody inhibition of PCSK9 |
| Therapeutic area + indication | Yes | Cardiovascular / hyperlipidemia |
| Competitive landscape (same mechanism) | Recommended | Evolocumab (approved), inclisiran (approved) |
| Genetic evidence for target | If available | MR: LDL-C lowering via PCSK9 LOF variants |
| Known class-effect safety signals | If available | Neurocognitive concerns (later refuted) |
| Company capital position | Recommended | $600M cash, 3.5yr runway |

### Steps

#### Step 1 — Score Target Validation Depth

Assign the target a tier on the validation ladder. Each tier carries a different base adjustment:

| Tier | Description | LOA Adjustment | Evidence Standard |
|---|---|---|---|
| **Tier 1: Genetic causality** | Human genetic evidence (MR, GWAS fine-mapping) directly links target to disease phenotype | +25-35% relative | Published MR study with colocalization, P < 5e-8, biological plausibility |
| **Tier 2: Human biology proof** | Human tissue/biomarker data confirms target engagement drives disease-relevant biology | +10-20% relative | Ex vivo human tissue, patient-derived samples, clinical biomarker correlation |
| **Tier 3: Competitive validation** | Another molecule hitting the same target has been approved or shown Phase 3 efficacy | +10-20% relative | Approved drug or Phase 3 with primary endpoint met |
| **Tier 4: Preclinical-only** | Target supported only by animal model data and in vitro pharmacology | 0% (baseline) | Animal efficacy models with PK/PD translation |
| **Tier 5: Hypothesis-driven** | Novel target based on pathway biology without direct disease linkage | -10-20% relative | Pathway analysis, computational prediction only |

**Mendelian Randomization deep-dive.** MR uses genetic variants (instruments) as natural experiments to test causal effects. For drug target validation:

- **Instrument selection**: Use eQTLs (expression) and pQTLs (protein) for the target gene as instruments. Variants must be genome-wide significant (P < 5e-8) and cis-acting (within 1Mb of gene).
- **Colocalization**: Run colocalization analysis (coloc or eCAVIAR) to confirm the genetic signal for target expression/protein level and the disease signal share the same causal variant. Posterior probability > 0.8 required.
- **Landmark validations**: PCSK9 loss-of-function variants (Cohen et al., NEJM 2006) predicted LDL-lowering efficacy years before evolocumab approval. NPC1L1 variants validated ezetimibe's mechanism. HMGCR variants predicted statin effects on LDL and diabetes risk simultaneously.
- **The 2x rule**: King et al. (Nature Communications 2020) showed that drug programs with supporting genetic evidence have approximately 2x higher probability of advancing from Phase 1 to approval compared to those without.

#### Step 2 — Assess Competitive Mechanism Derisking

Evaluate what other molecules targeting the same mechanism reveal about the target:

| Scenario | Adjustment | Rationale |
|---|---|---|
| Same-target drug approved | +10-20% relative | Mechanism fully validated in humans; remaining risk is molecule-specific |
| Same-target drug Phase 3 positive | +8-15% relative | Strong signal but regulatory/commercial risk remains |
| Same-target drug Phase 3 failure — molecule issue | 0% to +5% relative | Mechanism intact; failure due to PK, formulation, dosing, or patient selection |
| Same-target drug Phase 3 failure — mechanism issue | -15-25% relative | Efficacy hypothesis may be flawed; requires compelling differentiation rationale |
| Same-class drug safety-related withdrawal | -10-20% relative | Possible class effect; requires clear mechanistic differentiation |

**Critical distinction: molecule failure vs. mechanism failure.** When a competitor fails, determine whether the failure was due to the molecule (insufficient target engagement, poor PK, manufacturing issues, wrong patient population) or the mechanism (target inhibition does not produce the desired clinical effect). Only mechanism failures should penalize the target.

#### Step 3 — Evaluate Safety Class Effects

Score known mechanism-related safety risks:

| Safety Factor | Adjustment | Examples |
|---|---|---|
| Clean safety profile across class | 0% | GLP-1 RAs — well-characterized GI tolerability |
| Theoretical concern, no clinical signal | -3-5% relative | Anti-complement therapies and infection risk |
| Clinical signal in class, manageable | -5-10% relative | JAK inhibitors and VTE/MACE (boxed warning) |
| Clinical signal in class, severe | -15-25% relative | PPAR-gamma agonists and cardiovascular risk (rosiglitazone) |

#### Step 4 — Score Preclinical Translatability

| Factor | Score (0-3) | Criteria |
|---|---|---|
| Species concordance | 0-3 | Target homology, pathway conservation, disease model relevance |
| PK/PD translation | 0-3 | Human PK prediction accuracy, target engagement biomarkers |
| Biomarker availability | 0-3 | Validated pharmacodynamic biomarker exists for clinical use |
| Prior clinical precedent for modality | 0-3 | Same modality type has succeeded in this target class |

Composite translatability score (0-12): 0-3 = -10% adjustment, 4-6 = -5%, 7-9 = 0%, 10-12 = +5%.

#### Step 5 — Apply Biotech Reflexivity Adjustment

George Soros's reflexivity theory applied to drug development: market perception and capital position feed back into the fundamentals they are supposed to reflect. A company's ability to execute a clinical program is not independent of its stock price and cash position.

**The reflexivity loop in biotech:**
Positive Phase 2 data > stock price rises > easier capital raise > better-funded Phase 3 (more sites, faster enrollment, adaptive design) > higher genuine PoS > further stock appreciation.

This is not mere optimism bias — it reflects the real-world impact of capital constraints on trial execution quality.

| Capital Position | Score | Reflexivity Adjustment |
|---|---|---|
| Fortress balance sheet (>$1B cash, >4yr runway) | A | +8-12% relative |
| Well-capitalized (>$500M cash, >3yr runway) | B+ | +5-8% relative |
| Adequately capitalized (1-3yr runway through next catalyst) | B | 0% (neutral) |
| Capitalized through data readout only | C | -3-5% relative |
| Under-capitalized (<1yr runway, dilution imminent) | D | -10-15% relative |
| At-risk (potential going concern) | F | -20-30% relative |

#### Step 6 — Compile Adjustment Report

### Output

```
MECHANISM RISK ADJUSTMENT — [Target / MOA]
Indication: [disease]
Date: [assessment date]

TARGET VALIDATION:
  Tier: [1-5] — [description]
  Genetic evidence: [MR study citation or "None identified"]
  Adjustment: [+/- x%]

COMPETITIVE MECHANISM:
  Same-target status: [approved / Phase 3+ / Phase 2 / novel]
  Key precedent: [drug name, outcome]
  Molecule vs mechanism failure analysis: [if applicable]
  Adjustment: [+/- x%]

SAFETY CLASS EFFECT:
  Known signals: [description or "None identified"]
  Severity: [clean / theoretical / clinical-manageable / clinical-severe]
  Adjustment: [+/- x%]

TRANSLATABILITY:
  Composite score: [0-12]
  Limiting factor: [lowest-scoring dimension]
  Adjustment: [+/- x%]

REFLEXIVITY:
  Capital position: [A/B+/B/C/D/F]
  Cash: [$X], Runway: [Xyr]
  Adjustment: [+/- x%]

──────────────────────────────
COMPOSITE MECHANISM ADJUSTMENT: [+/- x%] relative to base rate
Evidence confidence: [High / Medium / Low]

Apply to PoS Calculator Step 3 as multiplicative adjustment.
```

### Error Handling

| Scenario | Response |
|---|---|
| No MR data available for target | Score as Tier 4 (preclinical-only); flag as key uncertainty; suggest checking Open Targets Genetics for available instruments |
| Target is completely novel (no prior clinical data in class) | Conservative Tier 5 scoring; emphasize confidence range width; note that novelty is not inherently negative but requires higher evidence bar |
| Conflicting competitive signals (one drug approved, another failed) | Analyze molecule vs mechanism failure for the failed drug; weight the approved drug more heavily if mechanism validated |
| Multi-target drug (bispecific, combination) | Assess each target independently; composite adjustment is the product of individual target adjustments weighted by contribution to efficacy |
| Rapidly evolving competitive landscape | Date-stamp all competitive assessments; flag that adjustment may change with upcoming data readouts; list key catalysts |
| Capital position unclear (private company) | Estimate from last fundraise, disclosed burn rate, and investor syndicate quality; apply wider uncertainty band |

## Cross-Domain Connections

- **Biotech-venture/pos-base-rates**: Provides the base rates this skill adjusts
- **Biotech-venture/pos-calculator**: Primary consumer — receives mechanism adjustment factors at Step 3
- **Biotech-venture/competitive-intelligence**: Feeds competitive mechanism data into Step 2
- **Biotech-venture/endpoint-selection**: Biomarker availability from Step 4 informs endpoint strategy
- **Investing/reflexivity-theory**: Theoretical foundation for the reflexivity adjustment in Step 5
