# Mechanism Risk Adjuster — Quick Reference


## Input

| Parameter | Required? | Example |
|---|---|---|
| Drug target(s) | Yes | PCSK9, GLP-1R, CD20 |
| Mechanism of action | Yes | Monoclonal antibody inhibition of PCSK9 |
| Therapeutic area + indication | Yes | Cardiovascular / hyperlipidemia |
| Competitive landscape (same mechanism) | Recommended | Evolocumab (approved), inclisiran (approved) |
| Genetic evidence for target | If available | MR: LDL-C lowering via PCSK9 LOF variants |
| Known class-effect safety signals | If available | Neurocognitive concerns (later refuted) |
| Company capital position | Recommended | $600M cash, 3.5yr runway |

## Quick Reference

| Tier | Description | LOA Adjustment | Evidence Standard |
|---|---|---|---|
| **Tier 1: Genetic causality** | Human genetic evidence (MR, GWAS fine-mapping) directly links target to disease phenotype | +25-35% relative | Published MR study with colocalization, P < 5e-8, biological plausibility |
| **Tier 2: Human biology proof** | Human tissue/biomarker data confirms target engagement drives disease-relevant biology | +10-20% relative | Ex vivo human tissue, patient-derived samples, clinical biomarker correlation |
| **Tier 3: Competitive validation** | Another molecule hitting the same target has been approved or shown Phase 3 efficacy | +10-20% relative | Approved drug or Phase 3 with primary endpoint met |
| **Tier 4: Preclinical-only** | Target supported only by animal model data and in vitro pharmacology | 0% (baseline) | Animal efficacy models with PK/PD translation |
| **Tier 5: Hypothesis-driven** | Novel target based on pathway biology without direct disease linkage | -10-20% relative | Pathway analysis, computational prediction only |

## Quick Reference

| Scenario | Adjustment | Rationale |
|---|---|---|
| Same-target drug approved | +10-20% relative | Mechanism fully validated in humans; remaining risk is molecule-specific |
| Same-target drug Phase 3 positive | +8-15% relative | Strong signal but regulatory/commercial risk remains |
| Same-target drug Phase 3 failure — molecule issue | 0% to +5% relative | Mechanism intact; failure due to PK, formulation, dosing, or patient selection |
| Same-target drug Phase 3 failure — mechanism issue | -15-25% relative | Efficacy hypothesis may be flawed; requires compelling differentiation rationale |
| Same-class drug safety-related withdrawal | -10-20% relative | Possible class effect; requires clear mechanistic differentiation |

## Quick Reference

| Safety Factor | Adjustment | Examples |
|---|---|---|
| Clean safety profile across class | 0% | GLP-1 RAs — well-characterized GI tolerability |
| Theoretical concern, no clinical signal | -3-5% relative | Anti-complement therapies and infection risk |
| Clinical signal in class, manageable | -5-10% relative | JAK inhibitors and VTE/MACE (boxed warning) |
| Clinical signal in class, severe | -15-25% relative | PPAR-gamma agonists and cardiovascular risk (rosiglitazone) |

## Step 4 — Score Preclinical Translatability

| Factor | Score (0-3) | Criteria |
|---|---|---|
| Species concordance | 0-3 | Target homology, pathway conservation, disease model relevance |
| PK/PD translation | 0-3 | Human PK prediction accuracy, target engagement biomarkers |
| Biomarker availability | 0-3 | Validated pharmacodynamic biomarker exists for clinical use |
| Prior clinical precedent for modality | 0-3 | Same modality type has succeeded in this target class |

## Quick Reference

| Capital Position | Score | Reflexivity Adjustment |
|---|---|---|
| Fortress balance sheet (>$1B cash, >4yr runway) | A | +8-12% relative |
| Well-capitalized (>$500M cash, >3yr runway) | B+ | +5-8% relative |
| Adequately capitalized (1-3yr runway through next catalyst) | B | 0% (neutral) |
| Capitalized through data readout only | C | -3-5% relative |
| Under-capitalized (<1yr runway, dilution imminent) | D | -10-15% relative |
| At-risk (potential going concern) | F | -20-30% relative |

## Error Handling

| Scenario | Response |
|---|---|
| No MR data available for target | Score as Tier 4 (preclinical-only); flag as key uncertainty; suggest checking Open Targets Genetics for available instruments |
| Target is completely novel (no prior clinical data in class) | Conservative Tier 5 scoring; emphasize confidence range width; note that novelty is not inherently negative but requires higher evidence bar |
| Conflicting competitive signals (one drug approved, another failed) | Analyze molecule vs mechanism failure for the failed drug; weight the approved drug more heavily if mechanism validated |
| Multi-target drug (bispecific, combination) | Assess each target independently; composite adjustment is the product of individual target adjustments weighted by contribution to efficacy |
| Rapidly evolving competitive landscape | Date-stamp all competitive assessments; flag that adjustment may change with upcoming data readouts; list key catalysts |
| Capital position unclear (private company) | Estimate from last fundraise, disclosed burn rate, and investor syndicate quality; apply wider uncertainty band |
