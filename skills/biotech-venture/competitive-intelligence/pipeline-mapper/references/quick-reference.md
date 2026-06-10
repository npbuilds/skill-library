# Pipeline Mapper — Quick Reference


## Input

| Parameter | Source | Required? |
|---|---|---|
| Therapeutic area or disease | User | Yes |
| Target or mechanism of action | User | Recommended |
| Modality filter (mAb, small molecule, gene therapy, etc.) | User | Optional |
| Phase filter (Phase 1+, Phase 2+, etc.) | User | Optional |
| Geography (US, global, China-only) | User | Optional (default: global) |

## Quick Reference

| Company | Asset | Target/MoA | Modality | Phase | Trial (NCT#) | N | Primary Endpoint | Est. Data | Differentiation Claim |
|---------|-------|------------|----------|-------|--------------|---|------------------|-----------|----------------------|
| [Co. A] | [Drug]| [target]   | [type]   | Ph 3  | NCT0XXXXXXX  |500| [endpoint]       | Q2 2025   | [claim]              |
| [Co. B] | [Drug]| [target]   | [type]   | Ph 2  | NCT0XXXXXXX  |200| [endpoint]       | Q4 2025   | [claim]              |
| ...     |       |            |          |       |              |   |                  |           |                      |

## Error Handling

| Scenario | Response |
|---|---|
| Very few competitors found | Expand the competitive boundary; check for programs under different terminology |
| Too many competitors (>20 in matrix) | Tier the landscape: Tier 1 (Phase 2b+), Tier 2 (Phase 1-2a), Tier 3 (preclinical) |
| No ClinicalTrials.gov results | Check international registries (EU CTR, CTRI, ChiCTR); search SEC and conference sources |
| Competitor timeline uncertain | Flag uncertainty explicitly; use estimated completion dates with confidence ranges |
| Undisclosed programs suspected | Note the gap; monitor conference schedules and patent filings for signals |

## Formula / Pseudocode

```
DIFFERENTIATION AXES

                Efficacy    Safety    Convenience    Onset    Durability    Cost
Asset Under    
  Review:       [rating]   [rating]   [rating]    [rating]   [rating]   [rating]

Competitor A:   [rating]   [rating]   [rating]    [rating]   [rating]   [rating]
Competitor B:   [rating]   [rating]   [rating]    [rating]   [rating]   [rating]
Competitor C:   [rating]   [rating]   [rating]    [rating]   [rating]   [rating]

Rating: ++ (clearly superior), + (modestly better), = (equivalent), 
        - (modestly worse), -- (clearly inferior), ? (insufficient data)
```

## Formula / Pseudocode

```
COMPETITIVE TIMELINE — [Therapeutic Area]

2024    2025    2026    2027    2028    2029
  |-------|-------|-------|-------|-------|
  Co.A ████ Ph3 data ▼ Filing ▼ Launch
  Co.B     ████ Ph2 data   ████ Ph3     ▼ Filing
  Co.C           ████ Ph1b/2    ████ Ph2b  ████ Ph3
  [Asset]    ████ Ph2 data ▼   ████ Ph3      ▼ Filing

▼ = Milestone    ████ = Active trial period
```
