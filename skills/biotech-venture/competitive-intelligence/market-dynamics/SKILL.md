---
name: market-dynamics
description: >
  Therapeutic market dynamics frameworks including game-theoretic competitive modeling,
  market archetypes, launch sequence impact, class saturation signals, payer adoption
  curves, and biosimilar erosion patterns. Apply mechanism-design from game theory to
  model indication sequencing as strategic games and first-mover vs fast-follower
  equilibria. Activate when assessing how clinical differentiation translates into
  commercial outcomes.
metadata:
  author: nirav
  version: "1.0"
  parent: competitive-intelligence
  innovation: "Game-theoretic competitive dynamics — mechanism-design applied to indication sequencing and patent races"
compatibility: Designed for Claude Code
allowed-tools: Read, WebSearch, WebFetch
---

# Market Dynamics — How Competition Shapes Value

Clinical superiority is necessary but not sufficient for commercial success. The translation of differentiation into market share depends on market structure — physician adoption patterns, formulary dynamics, switching costs, and competitive timing. A drug that is 15% more effective than the standard of care may capture 60% market share in one market and 15% in another, depending entirely on these dynamics.

This skill provides the frameworks for understanding why markets behave the way they do and predicting how a new entrant will perform.

## Market Archetypes

### Archetype 1 — First-in-Class Land Grab

**Characteristics:** No approved therapies for the condition; unmet need is high; physician eagerness for any effective treatment.

**Dynamics:** The first approved drug captures the entire addressable market. Early adopter physicians become KOL advocates. Guidelines incorporate the drug rapidly. Payers have limited leverage (no alternatives). Market share starts at 100% and declines only when competitors arrive.

**Examples:** Spinraza in SMA (before Zolgensma/Evrysdi); Keytruda in 1L NSCLC (initial approval); sofosbuvir in HCV.

**Value implication:** Maximum peak sales potential but highest competitive risk if followed quickly. The key question: how durable is the first-mover position?

**First-mover durability factors:**
- Physician inertia (1-3 years of prescribing habit formation)
- Formulary entrenchment (payer contracts with rebate commitments)
- Real-world evidence accumulation (safety database, outcomes data)
- Patient switching reluctance (stable patients resist change)

### Archetype 2 — Fast-Follower Differentiation

**Characteristics:** First-in-class exists but has meaningful limitations (safety signals, inconvenient dosing, suboptimal efficacy in subpopulations). Market is partially penetrated.

**Dynamics:** Fast-follower does not need to be globally superior — it needs to be better on the specific dimension that matters most to residual non-adopters. Often this is safety (fewer adverse events), convenience (oral vs injectable, less frequent dosing), or access to a subpopulation the first-in-class misses.

**Examples:** Dupixent displacing topical steroids in AD; oral JAK inhibitors vs injectable biologics in RA; Opdivo vs Keytruda (first-mover advantage reversed through indication strategy).

**Value implication:** Lower commercial launch risk (proven market exists) but smaller addressable share. Fast-follower must articulate the clinical story for switching or for treatment-naive patients.

### Archetype 3 — Best-in-Class Displacement

**Characteristics:** Established market with multiple approved options. New entrant claims superiority on efficacy, safety, or both, supported by head-to-head data.

**Dynamics:** Displacement requires head-to-head trial data showing clinically meaningful superiority. Marginal improvements (5-10% relative efficacy gains) rarely drive switching from an entrenched standard of care. Safety differentiation drives faster switching than efficacy differentiation. Guideline updates lag clinical data by 12-24 months.

**Examples:** Entresto displacing ACE inhibitors in HFrEF; direct oral anticoagulants displacing warfarin; GLP-1 agonists displacing older diabetes/obesity treatments.

**Value implication:** Highest commercial ceiling if differentiation is compelling, but requires significant launch investment and time to shift prescribing behavior. COGS and pricing must be competitive.

### Archetype 4 — Class Saturation

**Characteristics:** >5 approved options in the same mechanism class. Guidelines treat the class as interchangeable. Payer leverage is high.

**Dynamics:** New entrants face formulary exclusion, mandatory step therapy, and price competition. Differentiation claims are met with skepticism. Payers use competitive dynamics to extract rebates from all manufacturers. Market share is determined by contracting, not clinical data.

**Value implication:** Avoid unless the new entrant has a genuinely novel attribute (new indication, fundamentally different safety profile, dramatically lower price). Late entrants to saturated classes destroy value.

## Game-Theoretic Competitive Dynamics

### Indication Sequencing as Strategic Games

Each company's choice of which indication to pursue first is a strategic decision that considers competitors' likely moves. This is a multi-player sequential game with imperfect information.

**Nash Equilibrium in Indication Selection:**

When multiple companies share a target (e.g., anti-PD-1), indication sequencing becomes a coordination/competition game:

| Scenario | Game Structure | Equilibrium |
|---|---|---|
| Two companies, one large indication | Prisoner's Dilemma — both race to the same indication | Both enter; first-mover wins disproportionate share |
| Two companies, two viable indications | Coordination Game — both better off choosing different indications | Often converge on same indication anyway (information asymmetry) |
| One company ahead by 12+ months | Stackelberg Leader-Follower — leader commits, follower adapts | Follower should differentiate on indication or combination |
| Many companies, many indications | Free-for-all — clustering on validated indications | Contrarian strategy (underserved indications) can generate alpha |

**Application:** When mapping a competitive landscape, assess each competitor's indication strategy as a move in this game. The optimal response depends on your position (leader vs follower), your data (strength across indications), and competitors' likely reactions.

### Patent Race Dynamics

Patent races in biotech follow a winner-take-most structure modified by regulatory exclusivity:

```
PATENT RACE FRAMEWORK

                Early Leader    Close Second    Distant Third
Market Share:     50-70%          20-35%           5-15%
Pricing Power:    High            Moderate         Low (payer leverage)
Guideline:        First-line      Alternative      Not mentioned
KOL Mindshare:    Dominant        Growing          Minimal
```

**First-mover advantage decay rate:**
- Rare disease: Slow decay (3-5 year advantage persists; small physician community, high switching cost)
- Specialty care: Moderate decay (2-3 year advantage; specialist adoption curves)
- Primary care: Fast decay (1-2 year advantage; rapid payer-driven switching, high rep access)

### First-Mover vs Fast-Follower Equilibria

The optimal strategy depends on market characteristics:

**First-mover dominates when:**
- Disease is rare (small prescriber community, strong KOL influence)
- Treatment is chronic (patient switching reluctance compounds over time)
- Regulatory pathway gives exclusivity (orphan drug, pediatric)
- Safety database matters (physicians prefer longest track record)

**Fast-follower dominates when:**
- First-mover has significant safety signal (black box warning, REMS)
- Convenience difference is large (oral vs injectable in primary care)
- Market is large enough for multiple winners (oncology, immunology)
- Payer dynamics favor competition (rebate extraction requires alternatives)

## Payer Adoption Curves

Payer behavior determines realized revenue, not just prescriptions written. Model payer adoption in three phases:

**Phase 1 — Formulary Review (Month 0-6 post-approval):**
- P&T committee review period; limited access during this window
- Specialty drugs: prior authorization required from Day 1
- Typical initial tier placement based on clinical data and competitive context

**Phase 2 — Access Expansion (Month 6-18):**
- Gradual expansion of access criteria as real-world data accumulates
- Contracting negotiations set rebate levels for 1-3 year terms
- Competitor entry during this phase shifts payer leverage significantly

**Phase 3 — Steady State (Month 18+):**
- Formulary position stabilizes; changes driven by new data, competitor entry, or contract renegotiation
- LOE approaching shifts payer strategy toward generic/biosimilar preparation

**Net price erosion benchmarks:**
- Year 1-3 post-launch: 5-15% annual net price erosion (competitive rebating)
- Competitive class entry: Additional 10-20% erosion event
- Biosimilar entry: 30-50% price erosion over 3 years (biologics); 80-90% erosion over 2 years (small molecule generics)

## Biosimilar Erosion Patterns

Post-LOE dynamics differ fundamentally by modality:

**Small Molecule Generics:**
- Day 1 erosion: 20-30% market share to generics
- Year 1: 70-80% of volume switches to generic
- Year 2: 85-95% generic substitution
- Branded revenue retention: 5-15% (loyal patients, authorized generics)

**Biosimilar Competition:**
- Year 1: 15-25% erosion (physician switching reluctance, interchangeability questions)
- Year 2-3: 30-50% cumulative erosion
- Year 5: 50-70% cumulative erosion (slower than generics due to prescriber education, formulary inertia)
- Interchangeability designation accelerates erosion by ~30%

**Specialty Pharmacy vs Retail:**
- Specialty-dispensed products erode faster post-LOE (payer-controlled, mandatory substitution)
- Retail products erode at standard rates (pharmacy-level substitution laws)

## Guideline Incorporation Timelines

Treatment guidelines lag clinical data and drive adoption inflection points:

| Guideline Body | Typical Lag from Pivotal Data | Impact on Prescribing |
|---|---|---|
| NCCN (oncology) | 3-6 months | Rapid; oncologists follow NCCN closely |
| AHA/ACC (cardiology) | 12-18 months | Moderate; cardiologists are evidence-conservative |
| ACR (rheumatology) | 18-24 months | Slow; strong preference for established agents |
| AAN (neurology) | 12-18 months | Moderate; high unmet need accelerates incorporation |
| IDSA (infectious disease) | 6-12 months | Fast when resistance data is compelling |

**Value inflection:** Guideline incorporation typically drives a 15-30% increase in new prescriptions for the recommended therapy within 6 months. First-line guideline placement is worth 2-3x the commercial impact of second-line placement.

## Class Saturation Signals

Recognize when a market is approaching saturation before committing capital:

| Signal | Interpretation |
|---|---|
| >5 approved agents in same mechanism class | High saturation risk |
| Payer-mandated step therapy through older agents | Market access deteriorating |
| Head-to-head trials showing equivalence | Class becoming interchangeable |
| Generic/biosimilar entry in the class | Price floor established |
| Guidelines recommending "any agent in class" | Clinical differentiation no longer recognized |
| KOL fatigue ("another one?") | Physician mindshare saturated |
| Declining clinical trial enrollment | Patient recruitment competing across programs |

## Error Handling

| Scenario | Response |
|---|---|
| No approved competitors (white space) | Use Archetype 1 framework; model market creation dynamics |
| Rapidly evolving landscape (>3 approvals expected in 2 years) | Model dynamic market share with sequential entry scenarios |
| Cross-class competition (different mechanisms, same indication) | Expand analysis to mechanism-agnostic; assess switching triggers |
| Biosimilar timing uncertain | Model 2 scenarios: on-time LOE and 2-year delayed biosimilar entry |

## Cross-Domain Connections

- **competitive-intelligence/pipeline-mapper**: Pipeline density determines which archetype applies
- **asset-valuation/peak-sales-forecaster**: Market archetype and share dynamics directly set peak sales
- **regulatory-strategy/regulatory-precedent**: Regulatory pathway determines first-mover timing
- **manufacturing-ip/ip-valuation**: Patent life determines duration of competitive moat
- **deal-synthesis/diligence-scorecard**: Market dynamics assessment feeds Pillar 3 (Competitive Position)
