---
name: cmc-risk-assessor
description: >
  Assess chemistry, manufacturing, and controls risk using FMEA methodology with
  modality-specific failure modes, severity/occurrence/detection scoring, scalability
  assessment, COGS trajectory modeling, and supply chain single-point-of-failure
  analysis. Activate when evaluating whether a therapeutic program can be manufactured
  at commercial scale reliably and economically.
metadata:
  author: nirav
  version: "1.0"
  parent: manufacturing-ip
compatibility: Designed for Claude Code
allowed-tools: Read, WebSearch, WebFetch
---

# CMC Risk Assessor — Manufacturing Feasibility Through FMEA

Manufacturing risk is the most underweighted pillar in biotech venture diligence. Clinical data gets months of scrutiny; CMC gets a paragraph. Yet manufacturing failures have killed more late-stage programs than clinical failures — not because the drug does not work, but because it cannot be made consistently, at scale, at acceptable cost. Gene therapies with vector yield problems. Biologics with aggregation issues. Cell therapies with vein-to-vein logistics that collapse at scale.

This skill applies Failure Mode and Effects Analysis (FMEA) — the standard methodology from manufacturing quality engineering — to biotech CMC risk. Each failure mode is scored on Severity (patient/commercial impact), Occurrence (likelihood), and Detection (ability to catch before release), producing a Risk Priority Number (RPN) that prioritizes mitigation efforts.

## How to Run

### Input

| Parameter | Source | Required? |
|---|---|---|
| Asset name and modality | User | Yes |
| Current development phase | User | Yes |
| Manufacturing process description (if available) | User / SEC filings | Recommended |
| CDMO vs in-house manufacturing | User | Recommended |
| Current batch scale and yield | User | Optional |
| Target commercial supply needs (doses/year) | peak-sales-forecaster | Optional |

### Steps

#### Step 1 — Identify Modality-Specific Failure Modes

Each modality has characteristic manufacturing risks. Select the relevant failure mode set:

**Small Molecule:**
- Synthetic route complexity (number of steps, hazardous reagents, chiral centers)
- Polymorphism and crystal form control
- Impurity profile management (genotoxic impurities, nitrosamines)
- API sourcing concentration (single supplier risk)
- Formulation stability (degradation pathways, shelf life)

**Monoclonal Antibody (mAb):**
- Cell line stability and productivity (titer decline over passages)
- Aggregation and particulate formation
- Post-translational modification heterogeneity (glycosylation, deamidation, oxidation)
- Purification yield and purity (HCP, DNA removal)
- Cold chain requirements and formulation stability

**Viral Vector (AAV, Lentivirus):**
- Vector yield per batch (AAV: 1E14-1E16 vg target; often 10-100x shortfall)
- Full/empty capsid ratio (target >70% full; many programs at 30-50%)
- Scalability from adherent to suspension culture
- Potency assay development and qualification
- Raw material availability (plasmids, transfection reagents at GMP grade)

**Cell Therapy (Autologous):**
- Vein-to-vein time constraints (typically 3-6 weeks target)
- Manufacturing failure rate per patient batch (5-15% industry average)
- Starting material variability (patient-to-patient T cell quality)
- Cryopreservation and shipping logistics
- Chain of identity and chain of custody

**Cell Therapy (Allogeneic):**
- Donor cell sourcing and qualification
- Gene editing efficiency and off-target assessment
- Immune evasion durability (HLA knockout persistence)
- Scale-out from donor batch to commercial inventory
- Persistence vs dosing regimen (may need repeated dosing)

**mRNA-LNP:**
- mRNA integrity (% intact mRNA post-encapsulation; target >80%)
- LNP encapsulation efficiency and particle size consistency
- Lipid component sourcing (ionizable lipids often sole-source)
- Cold chain requirements (-20C or -70C storage)
- Scale-up of microfluidic mixing to commercial volumes

#### Step 2 — Score Each Failure Mode (FMEA)

Apply the 1-5 scoring system for Severity, Occurrence, and Detection:

**Severity (S) — Impact if the failure occurs:**

| Score | Definition | Example |
|---|---|---|
| 1 | Negligible | Minor documentation finding; no product impact |
| 2 | Low | Process deviation requiring investigation; product unaffected |
| 3 | Moderate | Batch release delay; minor quality attribute deviation |
| 4 | High | Batch failure/rejection; clinical supply interruption |
| 5 | Critical | Patient safety event; clinical hold; program termination |

**Occurrence (O) — Likelihood of the failure happening:**

| Score | Definition | Example |
|---|---|---|
| 1 | Rare | <1% of batches; well-controlled process |
| 2 | Low | 1-5% of batches; occasional deviations |
| 3 | Moderate | 5-15% of batches; known process challenge |
| 4 | High | 15-30% of batches; process not fully controlled |
| 5 | Very High | >30% of batches; fundamental process limitation |

**Detection (D) — Ability to catch the failure before it reaches patients:**

| Score | Definition | Example |
|---|---|---|
| 1 | Almost Certain | In-process control catches immediately; automated monitoring |
| 2 | High | Release testing catches reliably; validated analytical methods |
| 3 | Moderate | May not detect until stability testing or clinical use |
| 4 | Low | Limited analytical capability; novel product attributes |
| 5 | Very Low | No validated method exists; detected only by clinical outcome |

**Risk Priority Number:** RPN = S x O x D (range: 1-125)

| RPN Range | Risk Level | Action Required |
|---|---|---|
| 1-15 | Low | Standard monitoring; no special mitigation |
| 16-40 | Moderate | Risk mitigation plan recommended; monitor trends |
| 41-75 | High | Active mitigation required; may impact timeline |
| 76-125 | Critical | Program-threatening risk; must resolve before advancement |

#### Step 3 — Scalability Assessment

Evaluate the gap between current manufacturing scale and commercial requirements:

```
SCALABILITY ASSESSMENT

Current State:
  Batch scale: [current volume/dose count]
  Yield: [current yield metric]
  Batches/year capacity: [current]
  CDMO/In-house: [current arrangement]

Commercial Requirement:
  Annual doses needed: [from peak sales / patient population]
  Batch scale required: [calculated]
  Yield improvement needed: [X-fold from current]
  Facility investment: [estimated]

Scale-Up Risk:
  Low:  <3x scale increase; proven process platform
  Moderate: 3-10x; process transfer or tech improvements needed
  High: >10x; fundamental process redesign or new facility required
  Critical: Novel modality; no commercial-scale precedent exists
```

#### Step 4 — COGS Trajectory Modeling

> **Pull COGS baselines from `modality-manufacturing/references/modality-cogs-profiles.md`** (the single source) rather than re-embedding them here — then layer the FMEA occurrence/scalability adjustments on top. Respect its provenance tags: most per-modality COGS are internal estimates, not sourced benchmarks.

Project cost-of-goods from current state through commercial maturity:

| Phase | COGS/Dose Estimate | Key Driver |
|---|---|---|
| Clinical supply | $[X] (typically 5-50x commercial) | Small batch, manual process |
| Launch (Year 1-2) | $[X] | Process optimization ongoing |
| Maturity (Year 3-5) | $[X] | Scale effects, yield improvement |
| Steady state (Year 5+) | $[X] | Optimized process, potential second source |

**COGS benchmarks by modality:**
- Small molecule: $0.50-$50/dose (process-dependent)
- mAb: $50-$300/gram ($150-$3,000/dose depending on dose)
- ADC: $200-$500/gram (conjugation adds cost to mAb base)
- AAV gene therapy: $50,000-$500,000/dose (yield-dependent)
- Autologous cell therapy: $30,000-$100,000/dose (per-patient manufacturing)
- Allogeneic cell therapy: $5,000-$30,000/dose (batch manufacturing)
- mRNA-LNP: $2-$20/dose at pandemic scale; $50-$200/dose at rare disease scale

#### Step 5 — Supply Chain Single-Point-of-Failure Analysis

Identify supply chain vulnerabilities that could halt manufacturing:

| Component | # Qualified Suppliers | Sole Source? | Lead Time | Criticality |
|---|---|---|---|---|
| API / Drug Substance | [N] | [Y/N] | [weeks] | [High/Med/Low] |
| Key Raw Material 1 | [N] | [Y/N] | [weeks] | [High/Med/Low] |
| Key Raw Material 2 | [N] | [Y/N] | [weeks] | [High/Med/Low] |
| Fill/Finish CDMO | [N] | [Y/N] | [weeks] | [High/Med/Low] |
| Specialized Equipment | [N] | [Y/N] | [weeks] | [High/Med/Low] |
| Testing Laboratory | [N] | [Y/N] | [weeks] | [High/Med/Low] |

**Red flags:** Any critical component with a sole-source supplier AND >8-week lead time.

### Output

```
CMC RISK ASSESSMENT — [Asset Name]
Modality: [modality]
Phase: [current phase]
Date: [assessment date]

FMEA RISK MATRIX:
| # | Failure Mode | S | O | D | RPN | Risk Level | Mitigation |
|---|-------------|---|---|---|-----|------------|------------|
| 1 | [mode]      | X | X | X | XX  | [level]    | [action]   |
| 2 | [mode]      | X | X | X | XX  | [level]    | [action]   |
| ...                                                          |

TOP 3 MANUFACTURING RISKS:
1. [Highest RPN failure mode — description and mitigation timeline]
2. [Second highest — description and mitigation]
3. [Third highest — description and mitigation]

SCALABILITY: [Low / Moderate / High / Critical risk]
  Current → Commercial gap: [X-fold]
  Key bottleneck: [identified]
  Estimated timeline to commercial readiness: [months]

COGS TRAJECTORY:
  Clinical: $[X]/dose
  Launch:   $[X]/dose
  Mature:   $[X]/dose
  Gross margin at target price: [X]%

SUPPLY CHAIN:
  Single-point-of-failure risks: [N identified]
  Critical sole-source dependencies: [list]

OVERALL CMC RISK RATING: [Low / Moderate / High / Critical]
```

## Error Handling

| Scenario | Response |
|---|---|
| No manufacturing details available | Use modality defaults; flag as "estimated from modality benchmarks — high uncertainty" |
| Novel modality (no precedent) | Apply conservative scoring (O and D shifted up by 1 point); note absence of precedent |
| CDMO not disclosed | Flag as risk factor; CDMO selection impacts timeline and quality risk |
| COGS data unavailable | Use modality benchmark ranges; sensitivity test gross margin at low/mid/high COGS |

## Cross-Domain Connections

- **manufacturing-ip/ip-valuation**: COGS trajectory affects margin and thus IP-protected revenue value
- **asset-valuation/cost-estimator**: CMC complexity drives development cost estimates
- **asset-valuation/peak-sales-forecaster**: COGS determines gross margin from peak sales
- **regulatory-strategy**: CMC readiness affects filing timeline and regulatory risk
- **deal-synthesis/diligence-scorecard**: CMC risk is Pillar 4 (Manufacturing Feasibility) of the 8-pillar scorecard
