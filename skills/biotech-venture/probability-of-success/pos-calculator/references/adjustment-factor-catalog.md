# PoS Adjustment Factor Catalog

## Target Validation Ladder

Ordered from strongest to weakest evidence for target-disease causality:

| Level | Evidence Type | PoS Adjustment | Example |
|---|---|---|---|
| **5 — Genetic proof** | Mendelian randomization with significant causal effect; human LOF/GOF phenocopies disease | +25-30% relative | PCSK9 LOF → lower LDL → lower CV events |
| **4 — Human biology** | Human PK/PD data showing target engagement → biomarker change → clinical effect | +15-20% relative | Anti-VEGF → tumor shrinkage (angiogenesis) |
| **3 — Competitive validation** | Approved drug hitting same target in same/related indication | +10-20% relative | PD-1 validated by pembrolizumab/nivolumab |
| **2 — Preclinical with translation** | Strong preclinical data with validated biomarker bridge to humans | +5-10% relative | Good animal model concordance with human disease |
| **1 — Preclinical only** | In vitro / animal model data without human translation evidence | 0% (base rate) | Novel target with no human data |
| **0 — Unvalidated** | Target identified by screening/computational methods only | -10-15% relative | AI-predicted target without biological validation |

## Mendelian Randomization Evidence Assessment

When MR evidence is available for a target, assess using this checklist:

| MR Quality Check | Pass? | Impact if Missing |
|---|---|---|
| Cis-MR design (variants near target gene) | Required | Trans-MR has higher pleiotropy risk |
| Multiple instruments (≥3 independent SNPs) | Recommended | Single SNP may be weak instrument |
| F-statistic > 10 | Required | Weak instruments bias toward null |
| Consistent across MR methods (IVW, MR-Egger, weighted median) | Required | Inconsistency suggests pleiotropy |
| Colocalization probability > 80% | Recommended | Rules out confounding by LD |
| eQTL + pQTL concordance | Ideal | Both gene expression and protein levels |
| Replication in independent cohort | Ideal | Confirms robustness |

**Landmark examples:**
- **PCSK9**: LOF variants → 28% lower LDL → 88% lower CHD. Led directly to evolocumab/alirocumab approval.
- **NPC1L1**: Variants → lower LDL → lower CHD. Validated ezetimibe mechanism retroactively.
- **HMGCR**: Variants mimicking statin effect → lower CHD. Genetic validation of statin mechanism.
- **IL-6R**: Variants → lower CRP → lower CHD. Supported anti-IL-6 development (tocilizumab).

## Reflexivity Scoring Table

| Dimension | Score | Criteria |
|---|---|---|
| **Capital position** | | |
| +10% | | Cash > 3yr runway, recent raise at favorable terms |
| +5% | | Cash 2-3yr runway, adequate for pivotal program |
| 0% | | Cash 1-2yr runway, will need to raise during pivotal |
| -5% | | Cash < 1yr, uncertain financing |
| -10% | | Immediate dilution risk, may not complete trial |
| **Market sentiment** | | |
| +5% | | Stock at 52-week high, positive analyst coverage |
| 0% | | Stock near fair value, mixed coverage |
| -5% | | Stock at 52-week low, negative sentiment |
| **Operational capability** | | |
| +5% | | Experienced team, prior approvals, strong CRO relationships |
| 0% | | Adequate team, standard capabilities |
| -5% | | First-time team, limited regulatory experience |

## Competitive Context Adjustments

| Scenario | Adjustment | Rationale |
|---|---|---|
| First-in-class, validated target | +10-15% | Target proven but no direct competition yet |
| First-in-class, novel target | -10-15% | Unknown biology risk |
| Best-in-class (superior data to approved) | +10-20% | Clear differentiation + validated mechanism |
| Me-too (similar to approved) | -5-10% | Low regulatory risk but differentiation challenge |
| 4th+ entrant in crowded class | -10-15% | High bar for differentiation, enrollment challenges |
| Competitor Phase 3 failure in same MOA | -15-25% | May indicate mechanism problem, not just molecule |
| Competitor Phase 3 success in same MOA | +15-25% | Validates mechanism for entire class |

## Therapeutic Area-Specific Considerations

### Oncology
- Phase 2 ORR >30% for solid tumors significantly exceeds base rate expectations
- PFS hazard ratio <0.7 is clinically meaningful; <0.5 is exceptional
- Immunotherapy combinations: consider whether benefit is additive or synergistic

### CNS
- Placebo response rates of 30-50% in depression make Phase 3 highly unpredictable
- Blood-brain barrier penetration is a binary risk — either adequate or not
- Biomarker-defined populations (amyloid PET+) significantly improve CNS trial success

### Rare Disease
- Natural history data quality is the single largest PoS driver
- Smaller trials = higher variance in outcomes
- Gene therapy: manufacturing consistency is often the rate-limiting step, not efficacy
