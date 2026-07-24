---
name: patent-analyzer
description: >
  Analyze patent landscape and IP risk for biotech assets including patent type taxonomy,
  patent life calculation with extensions, Orange/Purple Book analysis, Paragraph IV
  dynamics, biosimilar BPCIA exclusivity, patent thicket assessment, and freedom-to-operate
  methodology. Activate when evaluating IP protection strength, loss of exclusivity timing,
  or generic/biosimilar entry risk.
metadata:
  author: nirav
  version: "1.0"
  parent: manufacturing-ip
compatibility: Designed for Claude Code
allowed-tools: Read, WebSearch, WebFetch
---

# Patent Analyzer — IP Landscape and Risk Assessment

Patent protection determines how long a drug generates premium revenue before generic or biosimilar competition erodes pricing power. For biotech venture investors, patent life is the single largest determinant of the revenue tail in rNPV models. A composition-of-matter patent expiring in 2038 vs 2031 can mean the difference between a $2B and $800M rNPV. Yet patent analysis in biotech diligence is often superficial — "they have patents until 2035" — without examining patent type, vulnerability to challenge, or freedom-to-operate risk.

This skill provides the methodology for rigorous patent landscape analysis.

> **LOE precedents & statutory clocks:** exclusivity terms, patent-life math, and verified generic/biosimilar erosion precedents are in `references/loe-precedents.md`; full erosion curves in market-dynamics' `launch-and-erosion-benchmarks.md`.

## How to Run

### Input

| Parameter | Source | Required? |
|---|---|---|
| Asset name / active ingredient | User | Yes |
| Modality (small molecule, biologic, etc.) | User | Yes |
| Patent numbers (if known) | User / Orange Book / SEC filings | Recommended |
| Company name (for patent assignment search) | User | Yes |
| Therapeutic indication | User | Recommended |

### Steps

#### Step 1 — Patent Type Taxonomy

Not all patents are equal. Classify each patent by type and assess its protective strength:

| Patent Type | Protection Strength | Vulnerability | Duration |
|---|---|---|---|
| Composition of Matter (CoM) | Strongest — covers the molecule itself | Hardest to design around | Filing date + 20 years + PTE |
| Salt / Polymorph | Strong — covers specific forms | Designable if alternative forms exist | Filing + 20 + PTE |
| Formulation | Moderate — covers delivery method | Generics can reformulate | Filing + 20 + PTE |
| Method of Use | Moderate — covers specific indication | Does not prevent off-label use of generic; skinny label strategies | Filing + 20 + PTE |
| Dosing Regimen | Weak-Moderate — covers specific dose/schedule | Difficult to enforce; physicians may prescribe off-label | Filing + 20 |
| Process / Manufacturing | Weakest for exclusivity — covers how to make it | Alternative processes usually possible | Filing + 20 |
| Combination | Variable — covers specific drug combinations | Only protects the combination, not individual components | Filing + 20 + PTE |

**Assessment rule:** An asset protected only by method-of-use and dosing patents (no CoM) faces significantly higher generic entry risk. A strong IP estate has CoM as the anchor with formulation and method-of-use as reinforcement.

#### Step 2 — Patent Life Calculation

Calculate effective patent life from filing date through all adjustments:

```
PATENT LIFE CALCULATION

Base Term:
  Filing date: [date]
  Base expiry: Filing + 20 years = [date]

Patent Term Adjustment (PTA) — 35 USC 271:
  USPTO prosecution delay: +[X] days
  Applicant delay offset: -[X] days
  Net PTA: +[X] days → Adjusted expiry: [date]

Patent Term Extension (PTE) — 35 USC 156:
  Eligible? [Y/N — only one patent per product; must be first commercial use]
  Regulatory review period: [X] months
  PTE = 50% of clinical testing time + 100% of regulatory review time
  Maximum PTE: 5 years
  Cannot extend total patent life beyond 14 years from approval
  PTE grant: +[X] months → PTE-adjusted expiry: [date]

Supplementary Protection Certificate (SPC) — EU:
  Duration: Time between patent filing and marketing authorization - 5 years
  Maximum: 5 years (+ 6 months with pediatric extension)
  SPC expiry: [date]

Effective Patent Expiry: [latest of US/EU dates]
```

#### Step 3 — Orange Book / Purple Book Analysis

**Small Molecules — Orange Book (FDA):**

The Orange Book lists patents and exclusivities for approved drugs. Analyze:

- **Listed patents:** Which patents are listed? CoM, formulation, method of use?
- **Use codes:** What specific indications are patent-protected?
- **Exclusivity codes:**
  - NCE (New Chemical Entity): 5 years — no ANDA filing permitted
  - New Clinical Investigation: 3 years — ANDAs can be filed but not approved
  - Orphan Drug: 7 years — no approval of same drug for same indication
  - Pediatric: +6 months added to all existing exclusivities and patents
  - QIDP (Qualified Infectious Disease Product): +5 years added to exclusivity
  - 180-day First Filer Exclusivity: First Paragraph IV filer gets 180 days generic exclusivity

**Biologics — Purple Book (FDA):**

- **Reference product listing:** Is the asset listed as a reference product?
- **Biosimilar applications:** Any 351(k) applications filed?
- **Interchangeability:** Any interchangeable biosimilar approved?
- **BPCIA exclusivity:**
  - 12-year data exclusivity from first licensure (no biosimilar approval)
  - 4-year filing exclusivity (no biosimilar application accepted)
  - First interchangeable biosimilar: 1 year market exclusivity

#### Step 4 — Paragraph IV / Patent Challenge Assessment

For small molecules, assess vulnerability to Paragraph IV (generic) challenge:

**Paragraph IV Risk Factors:**

| Factor | Low Risk | High Risk |
|---|---|---|
| CoM patent strength | Strong, validated CoM | No CoM; only method-of-use/formulation |
| Prior art | Clean prosecution history | Multiple rejections, narrow claims |
| Peak sales | <$500M (limited generic incentive) | >$1B (strong generic incentive) |
| Patent scope | Broad genus claims covering analogs | Narrow species claims |
| Litigation history | No IPR challenges; clean IPR record | IPR losses; claim narrowing |
| Number of generic filers | 0-1 ANDA filers | Multiple ANDA filers |

**30-Month Stay:** When a Paragraph IV certification is filed, the brand gets an automatic 30-month stay of FDA approval while litigation proceeds. This stay is critical — it provides ~2.5 years of protected revenue even if the patent is ultimately invalidated.

**Authorized Generic Strategy:** Companies can launch an authorized generic (AG) at patent expiry or upon Paragraph IV loss to capture generic market share and reduce the economic incentive for independent generics.

#### Step 5 — Biosimilar Entry Analysis (BPCIA)

For biologics, model the biosimilar entry timeline:

```
BIOSIMILAR ENTRY TIMELINE

12-Year Exclusivity Clock:
  BLA approval date: [date]
  4-year mark (earliest biosimilar filing): [date]
  12-year mark (earliest biosimilar approval): [date]

Patent Dance (BPCIA):
  Phase 1: Biosimilar applicant provides application + manufacturing info
  Phase 2: Reference product sponsor identifies relevant patents
  Phase 3: Negotiation of patents for immediate litigation
  Phase 4: Litigation on agreed patents
  Phase 5: Remaining patents available for later litigation

Practical Biosimilar Entry:
  Earliest possible: 12-year exclusivity expiry
  Most likely: 12 years + 2-4 years (patent litigation resolution)
  Delayed: Key CoM patent extends beyond 12-year exclusivity
```

**Interchangeability impact:** An interchangeable biosimilar can be substituted at the pharmacy without physician intervention, accelerating erosion dramatically. Non-interchangeable biosimilars require physician prescribing, slowing switching.

#### Step 6 — Patent Thicket Assessment

A "patent thicket" is a dense web of overlapping patents designed to extend effective exclusivity beyond the core CoM patent:

```
PATENT THICKET ANALYSIS

Total patents listed: [N]
Patent types:
  Composition of Matter: [N]  (expiry: [dates])
  Formulation:           [N]  (expiry: [dates])
  Method of Use:         [N]  (expiry: [dates])
  Dosing:                [N]  (expiry: [dates])
  Process:               [N]  (expiry: [dates])
  Combination:           [N]  (expiry: [dates])

Latest expiring patent: [date]
Earliest vulnerable entry: [date — when generics could enter with skinny label]
Effective exclusivity extension from thicket: [years beyond CoM expiry]

Thicket strength: [Strong / Moderate / Weak]
  Strong: Multiple overlapping types with staggered expiries; no skinny label path
  Moderate: Some protection beyond CoM but skinny label path exists
  Weak: CoM is the only meaningful barrier; ancillary patents easily designed around
```

#### Step 7 — Freedom-to-Operate (FTO) Analysis

Assess whether the asset infringes third-party patents:

| FTO Dimension | Assessment | Risk |
|---|---|---|
| Compound/composition | Does any third party hold CoM claims covering the molecule or genus? | [High/Med/Low] |
| Target biology | Are there patents on the biological target that could create royalty obligations? | [High/Med/Low] |
| Technology platform | Does the platform (mAb engineering, AAV capsid, LNP formulation) have IP encumbrances? | [High/Med/Low] |
| Manufacturing process | Do process patents create manufacturing method restrictions? | [High/Med/Low] |
| Formulation/delivery | Are there delivery technology patents that apply? | [High/Med/Low] |

**FTO risk levels:**
- **Clean FTO:** No identified third-party patent risks; freedom to develop and commercialize
- **Encumbered FTO:** Known patent risks requiring license or design-around; quantify royalty exposure (typically 2-8% of net sales)
- **Blocked FTO:** Third-party patent directly covers the asset; license is mandatory or development must halt

### Output

```
PATENT LANDSCAPE ANALYSIS — [Asset Name]
Date: [assessment date]

PATENT ESTATE SUMMARY:
| Patent # | Type | Filing Date | Expiry | PTE/PTA | Effective Expiry | Strength |
|----------|------|-------------|--------|---------|------------------|----------|
| US X,XXX | CoM  | [date]      | [date] | +[X]mo  | [date]           | Strong   |
| US X,XXX | MoU  | [date]      | [date] | N/A     | [date]           | Moderate |
| ...      |      |             |        |         |                  |          |

KEY DATES:
  Loss of Exclusivity (LOE): [date]
  Earliest generic/biosimilar entry: [date]
  Latest patent expiry: [date]
  Effective IP protection remaining: [X] years

PATENT THICKET: [Strong / Moderate / Weak]
FTO ASSESSMENT: [Clean / Encumbered / Blocked]
  Royalty exposure (if encumbered): [X]% of net sales

GENERIC/BIOSIMILAR ENTRY RISK:
  Timeline: [X] years from now
  Likelihood within 5 years: [Low / Moderate / High]
  Entry impact on revenue: [X]% erosion over [X] years

OVERALL IP RISK RATING: [Low / Moderate / High / Critical]
```

## Error Handling

| Scenario | Response |
|---|---|
| Patent numbers not available | Search USPTO, Espacenet, Google Patents by assignee + compound name |
| No Orange/Purple Book listing | Asset may be pre-approval; analyze patent applications and granted patents directly |
| International patent variations | Note US vs EU vs ROW expiry differences; model revenue by geography |
| Patent challenge pending (IPR/PGR) | Flag as active risk; model scenarios with and without challenged claims |

## Cross-Domain Connections

- **manufacturing-ip/ip-valuation**: Patent life directly determines IP value and revenue tail
- **asset-valuation/rnpv-modeler**: Patent expiry sets the revenue cutoff in rNPV models
- **competitive-intelligence/market-dynamics**: LOE timing determines biosimilar/generic erosion curve
- **regulatory-strategy**: Regulatory exclusivity interacts with patent protection (may extend or be redundant)
- **deal-synthesis/diligence-scorecard**: IP assessment feeds Pillar 5 (IP Fortress) of the 8-pillar scorecard
