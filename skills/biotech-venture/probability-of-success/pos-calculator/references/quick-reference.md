# Pos Calculator — Quick Reference


## Quick Reference

| Parameter | Required? | Example |
|---|---|---|
| Therapeutic area | Yes | Oncology (NSCLC) |
| Current development phase | Yes | Phase 2 |
| Mechanism of action | Yes | PD-1/VEGF bispecific antibody |
| Target | Recommended | PD-1 + VEGF-A |
| Modality | Recommended | Bispecific antibody |
| Biomarker selection | If applicable | PD-L1 CPS >= 1 |
| Regulatory designations | If applicable | Breakthrough Therapy, Orphan |
| Prior clinical data | If available | Phase 1 ORR = 42%, DCR = 78% |
| Competitive context | Recommended | 3 approved IO agents in 1L NSCLC |
| Company capitalization | Optional | $800M market cap, $400M cash |

## Quick Reference

| Factor | Direction | Magnitude | Evidence Required |
|---|---|---|---|
| Genetic target validation (MR) | Upward | +20-30% relative | Published MR study with significant association |
| Validated target (approved drug in class) | Upward | +10-20% relative | Approved drug hitting same target |
| First-in-class (novel target) | Downward | -10-15% relative | No approved drug or advanced clinical data on target |
| Prior failure in same MOA | Downward | -15-25% relative | Phase 2/3 failure in same mechanism class |
| Strong preclinical-to-clinical translation | Upward | +5-10% relative | Species concordance, validated PK/PD model |
| Known mechanism toxicity | Downward | -5-15% relative | Class-effect safety signal documented |

## Step 4 — Apply Program-Specific Modifiers

| Modifier | Direction | Magnitude | Rationale |
|---|---|---|---|
| Breakthrough Therapy Designation | Upward | +10-15% relative | 54% of granted BTDs approved; 30% time savings |
| Orphan Drug Designation | Upward | +10-15% relative | Smaller trials, regulatory flexibility, 7yr exclusivity |
| Biomarker-selected population | Upward | +15-25% relative | Higher effect size, enriched responder population |
| Large unmet need (no approved SOC) | Upward | +5-10% relative | FDA more willing to accept surrogate endpoints |
| Positive Phase 2 data (above expectations) | Upward | +10-20% relative | Data de-risks efficacy hypothesis |
| Crowded indication (5+ competitors) | Downward | -5-10% relative | Higher bar for differentiation, enrollment challenges |
| Small/undercapitalized sponsor | Downward | -5-10% relative | Execution risk, may not fund pivotal trial adequately |

## Quick Reference

| Capital Position | Reflexivity Adjustment |
|---|---|
| Well-capitalized (>3yr runway, >$500M cash) | +5-10% relative |
| Adequately capitalized (1-3yr runway) | 0% (neutral) |
| Under-capitalized (<1yr runway without raise) | -10-15% relative |
| Pre-data capital raise completed | +5% relative (runway secured) |

## Error Handling

| Scenario | Response |
|---|---|
| Insufficient information for base rate | Use "All Indications" base rate with wider confidence range |
| No MR data available for target | Skip genetic validation adjustment; note as limitation |
| Conflicting adjustment factors | Apply both; net effect may partially cancel; document both |
| Ultra-rare disease (<200 patients) | Base rates unreliable; use rare disease rates with high uncertainty band |
| Platform technology (multiple indications) | Calculate PoS per indication; note that platform success in one indication may de-risk others |

## Formula / Pseudocode

```
Base PTRS = {P(current phase -> next), P(next -> next+1), ..., P(NDA -> Approval)}
Base LOA = Product of all remaining PTRS
```
