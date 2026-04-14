---
name: pipeline-mapper
description: >
  Map the competitive pipeline for a therapeutic area, target, or mechanism of action
  using ClinicalTrials.gov, SEC filings, and conference abstracts. Produces a structured
  competitive landscape matrix with differentiation axes, timeline analysis, and
  first-mover vs fast-follower positioning. Activate when evaluating what else is in
  development, who the competitors are, and where an asset sits in the competitive field.
metadata:
  author: nirav
  version: "1.0"
  parent: competitive-intelligence
compatibility: Designed for Claude Code
allowed-tools: Read, WebSearch, WebFetch
---

# Pipeline Mapper — Competitive Landscape Construction

You cannot assess differentiation without knowing the competitive set. Pipeline mapping is the foundation of competitive intelligence — it answers the question "who else is working on this, how far along are they, and when will they get there?" Every downstream assessment (differentiation, market share, peak sales) depends on the accuracy and completeness of this map.

The most dangerous error in competitive intelligence is not knowing about a competitor. The second most dangerous is mischaracterizing their stage or timeline. This skill produces comprehensive, evidence-based landscape matrices that prevent both.

## How to Run

### Input

| Parameter | Source | Required? |
|---|---|---|
| Therapeutic area or disease | User | Yes |
| Target or mechanism of action | User | Recommended |
| Modality filter (mAb, small molecule, gene therapy, etc.) | User | Optional |
| Phase filter (Phase 1+, Phase 2+, etc.) | User | Optional |
| Geography (US, global, China-only) | User | Optional (default: global) |

### Steps

#### Step 1 — Define the Competitive Boundary

Define what counts as a competitor. This is the most consequential analytical decision:

**Narrow boundary:** Same target, same modality, same indication
- Use when: Target-specific differentiation matters (e.g., selectivity, binding site)
- Example: All anti-PD-1 monoclonal antibodies in advanced melanoma

**Medium boundary:** Same mechanism class, any modality, same indication
- Use when: Mechanism-level competition is the relevant frame
- Example: All checkpoint inhibitors (PD-1, PD-L1, CTLA-4, LAG-3, TIGIT) in NSCLC

**Broad boundary:** Any mechanism, same indication
- Use when: Standard-of-care competition is the relevant frame
- Example: All systemic therapies in moderate-to-severe atopic dermatitis

Always map at medium boundary, then expand or narrow based on user needs. A narrow-only map misses cross-mechanism competitors that could redefine the standard of care.

#### Step 2 — Query ClinicalTrials.gov

Primary data source for clinical-stage programs. Querying strategy:

```
SEARCH STRATEGY — ClinicalTrials.gov

Query 1 (Condition-based):
  Condition: [disease/indication]
  Status: Recruiting, Active not recruiting, Enrolling by invitation, Completed
  Phase: Phase 1, Phase 2, Phase 3, Phase 4
  Study Type: Interventional

Query 2 (Intervention-based):
  Intervention: [target name OR mechanism name]
  Status: Same as above
  Phase: Same as above

Query 3 (Sponsor-based):
  Sponsor: [known competitor company names]
  Condition: [disease/indication]

Cross-reference all three queries to catch:
  - Programs using non-standard disease terminology (Query 1 miss)
  - Programs registered under broad indication categories (Query 2 catch)
  - Programs not yet on ClinicalTrials.gov but disclosed by sponsors (Query 3 catch)
```

**Critical filters:**
- Exclude withdrawn, suspended, and terminated studies unless analyzing attrition signals
- Note "not yet recruiting" studies — these represent upcoming competitive entries
- Check "estimated primary completion date" for timeline intelligence

#### Step 3 — Supplement with Non-Clinical Sources

ClinicalTrials.gov captures ~80% of the landscape. Close the gap with:

**SEC Filings (10-K, 10-Q, S-1):**
- Pipeline tables in annual reports often disclose programs not yet on ClinicalTrials.gov
- S-1 filings from IPOs contain detailed pipeline descriptions with timelines
- Search: EDGAR full-text search for [target name] or [indication]

**Conference Abstracts:**
- ASCO, AACR, ASH, ESMO, AAN, ACR — search abstract databases for target/indication
- Conference presentations often precede ClinicalTrials.gov registration by 6-12 months
- Preclinical data at conferences signal clinical entries within 12-24 months

**Press Releases:**
- IND filings, clinical trial initiations, partnership announcements
- Regulatory designations (Fast Track, Breakthrough, Orphan) as pipeline signals

**Patent Applications:**
- PCT/WO applications filed 18 months before publication reveal undisclosed programs
- Freedom-to-operate filings suggest clinical development intent

#### Step 4 — Construct the Landscape Matrix

Organize all competitors into a structured matrix:

```
COMPETITIVE LANDSCAPE — [Therapeutic Area]
Date: [assessment date]
Boundary: [narrow/medium/broad — defined above]

| Company | Asset | Target/MoA | Modality | Phase | Trial (NCT#) | N | Primary Endpoint | Est. Data | Differentiation Claim |
|---------|-------|------------|----------|-------|--------------|---|------------------|-----------|----------------------|
| [Co. A] | [Drug]| [target]   | [type]   | Ph 3  | NCT0XXXXXXX  |500| [endpoint]       | Q2 2025   | [claim]              |
| [Co. B] | [Drug]| [target]   | [type]   | Ph 2  | NCT0XXXXXXX  |200| [endpoint]       | Q4 2025   | [claim]              |
| ...     |       |            |          |       |              |   |                  |           |                      |
```

Sort by: Phase (descending), then by estimated data readout (ascending). Phase 3 assets are the most competitively relevant; earlier-phase assets with near-term data are next.

#### Step 5 — Analyze Differentiation Axes

For each competitor in the matrix, assess positioning on key axes:

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

#### Step 6 — Map Competitive Timing

Timeline analysis determines first-mover vs fast-follower dynamics:

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

Key timing questions:
- How many competitors will be approved before the asset under review?
- Is there a window of exclusivity, and how long?
- Do any competitors have accelerated pathways (Breakthrough, Fast Track)?

### Output

```
COMPETITIVE PIPELINE MAP — [Therapeutic Area / Target]
Date: [assessment date]
Competitive Boundary: [definition]

Summary Statistics:
  Total programs identified: [N]
  Phase 3: [N]  |  Phase 2: [N]  |  Phase 1: [N]  |  Preclinical (disclosed): [N]

Competitive Landscape Matrix: [full table from Step 4]

Differentiation Assessment: [axes analysis from Step 5]

Timeline Map: [timeline from Step 6]

Key Competitive Insights:
1. [Most advanced competitor and expected timeline]
2. [Degree of crowding — low (<3 competitors), moderate (3-6), high (>6)]
3. [Dominant mechanism(s) vs novel approaches]
4. [First-mover vs fast-follower positioning of the asset under review]

First-Mover vs Fast-Follower Assessment:
  Position: [1st / 2nd / 3rd+ to market]
  Lead/Lag: [+/- months vs nearest competitor]
  First-mover advantage strength: [Strong / Moderate / Weak]
  Rationale: [why — based on indication-specific switching dynamics]

Red Flags:
  - [Any competitor with superior data and earlier timeline]
  - [Any Big Pharma entrant with commercial infrastructure advantage]
  - [Any competitor with Breakthrough Therapy Designation]

White Space Opportunities:
  - [Underserved patient populations within the indication]
  - [Combination strategies not yet explored]
  - [Geographic markets with less competition]
```

## Error Handling

| Scenario | Response |
|---|---|
| Very few competitors found | Expand the competitive boundary; check for programs under different terminology |
| Too many competitors (>20 in matrix) | Tier the landscape: Tier 1 (Phase 2b+), Tier 2 (Phase 1-2a), Tier 3 (preclinical) |
| No ClinicalTrials.gov results | Check international registries (EU CTR, CTRI, ChiCTR); search SEC and conference sources |
| Competitor timeline uncertain | Flag uncertainty explicitly; use estimated completion dates with confidence ranges |
| Undisclosed programs suspected | Note the gap; monitor conference schedules and patent filings for signals |

## Cross-Domain Connections

- **competitive-intelligence/market-dynamics**: Pipeline density feeds market archetype classification — crowded vs white space
- **clinical-development/endpoint-selection**: Competitor endpoint choices constrain or inform endpoint strategy
- **regulatory-strategy/regulatory-precedent**: Competitor regulatory pathways (BTD, accelerated approval) set precedent
- **asset-valuation/peak-sales-forecaster**: Number and timing of competitors directly determines achievable market share
- **deal-synthesis/diligence-scorecard**: Competitive position is Pillar 3 of the 8-pillar scorecard
