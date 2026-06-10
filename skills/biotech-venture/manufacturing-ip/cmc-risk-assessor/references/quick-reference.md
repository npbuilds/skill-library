# Cmc Risk Assessor — Quick Reference


## Input

| Parameter | Source | Required? |
|---|---|---|
| Asset name and modality | User | Yes |
| Current development phase | User | Yes |
| Manufacturing process description (if available) | User / SEC filings | Recommended |
| CDMO vs in-house manufacturing | User | Recommended |
| Current batch scale and yield | User | Optional |
| Target commercial supply needs (doses/year) | peak-sales-forecaster | Optional |

## Quick Reference

| Score | Definition | Example |
|---|---|---|
| 1 | Negligible | Minor documentation finding; no product impact |
| 2 | Low | Process deviation requiring investigation; product unaffected |
| 3 | Moderate | Batch release delay; minor quality attribute deviation |
| 4 | High | Batch failure/rejection; clinical supply interruption |
| 5 | Critical | Patient safety event; clinical hold; program termination |

## Quick Reference

| Score | Definition | Example |
|---|---|---|
| 1 | Rare | <1% of batches; well-controlled process |
| 2 | Low | 1-5% of batches; occasional deviations |
| 3 | Moderate | 5-15% of batches; known process challenge |
| 4 | High | 15-30% of batches; process not fully controlled |
| 5 | Very High | >30% of batches; fundamental process limitation |

## Quick Reference

| Score | Definition | Example |
|---|---|---|
| 1 | Almost Certain | In-process control catches immediately; automated monitoring |
| 2 | High | Release testing catches reliably; validated analytical methods |
| 3 | Moderate | May not detect until stability testing or clinical use |
| 4 | Low | Limited analytical capability; novel product attributes |
| 5 | Very Low | No validated method exists; detected only by clinical outcome |

## Quick Reference

| RPN Range | Risk Level | Action Required |
|---|---|---|
| 1-15 | Low | Standard monitoring; no special mitigation |
| 16-40 | Moderate | Risk mitigation plan recommended; monitor trends |
| 41-75 | High | Active mitigation required; may impact timeline |
| 76-125 | Critical | Program-threatening risk; must resolve before advancement |

## Quick Reference

| Phase | COGS/Dose Estimate | Key Driver |
|---|---|---|
| Clinical supply | $[X] (typically 5-50x commercial) | Small batch, manual process |
| Launch (Year 1-2) | $[X] | Process optimization ongoing |
| Maturity (Year 3-5) | $[X] | Scale effects, yield improvement |
| Steady state (Year 5+) | $[X] | Optimized process, potential second source |

## Quick Reference

| Component | # Qualified Suppliers | Sole Source? | Lead Time | Criticality |
|---|---|---|---|---|
| API / Drug Substance | [N] | [Y/N] | [weeks] | [High/Med/Low] |
| Key Raw Material 1 | [N] | [Y/N] | [weeks] | [High/Med/Low] |
| Key Raw Material 2 | [N] | [Y/N] | [weeks] | [High/Med/Low] |
| Fill/Finish CDMO | [N] | [Y/N] | [weeks] | [High/Med/Low] |
| Specialized Equipment | [N] | [Y/N] | [weeks] | [High/Med/Low] |
| Testing Laboratory | [N] | [Y/N] | [weeks] | [High/Med/Low] |

## Quick Reference

| # | Failure Mode | S | O | D | RPN | Risk Level | Mitigation |
|---|-------------|---|---|---|-----|------------|------------|
| 1 | [mode]      | X | X | X | XX  | [level]    | [action]   |
| 2 | [mode]      | X | X | X | XX  | [level]    | [action]   |
| ...                                                          |
