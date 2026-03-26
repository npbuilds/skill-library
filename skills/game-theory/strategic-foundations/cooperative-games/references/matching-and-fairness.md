# Matching Theory and Fair Division

## Two-Sided Matching

### The Stable Matching Problem

**Setting**: Two disjoint sets of agents (e.g., students and schools, residents and hospitals) with preferences over agents on the other side. Goal: find a matching that is **stable** — no unmatched pair would prefer each other to their current assignments.

### Gale-Shapley Deferred Acceptance Algorithm (1962)

**Proposer-optimal version** (proposers = side that makes offers):

```
Initialize: all agents unmatched
Repeat:
  Each unmatched proposer proposes to their most-preferred
    partner they haven't proposed to yet
  Each receiver:
    - Tentatively accepts the best proposal received
      (including possibly their current tentative match)
    - Rejects all others
Until: no rejected proposers remain (or all have exhausted their lists)
```

**Properties**:
- **Always terminates** in at most n² rounds (n = number of agents per side)
- **Always produces a stable matching** (no blocking pair exists)
- **Proposer-optimal**: every proposer gets their best achievable partner across ALL stable matchings
- **Receiver-pessimal**: every receiver gets their worst stable match
- **Strategy-proof for proposers**: truth-telling is a dominant strategy
- **NOT strategy-proof for receivers**: receivers may benefit from misreporting preferences

**The lattice structure of stable matchings** (Conway 1976, Knuth 1976): The set of stable matchings forms a distributive lattice. The proposer-optimal and receiver-optimal matchings are the two extremes.

### Real-World Matching Systems

**National Resident Matching Program (NRMP)**

The NRMP matches ~35,000 medical graduates to residency positions annually. Uses the Roth-Peranson algorithm (1999), an extension of Gale-Shapley that handles:
- Couples who want to be matched to the same city
- Programs with multiple positions
- Supplemental offer rounds

History: The original NRMP (1952) predated Gale-Shapley by a decade. Roth (1984) showed it was equivalent to hospital-proposing DA. In 1995, the algorithm was redesigned to be applicant-proposing (applicant-optimal) — a direct application of the lattice theory.

**School Choice**

Three prominent mechanisms:
1. **Boston mechanism** (immediate acceptance): Students apply to first choice; schools accept best applicants, reject others. Rejected students apply to second choice, etc. NOT strategy-proof — parents must strategize about which schools to list.
2. **Gale-Shapley DA** (student-proposing): Strategy-proof for students. Used in NYC and Boston after 2003 redesign.
3. **Top Trading Cycles (TTC)**: Students "own" a school slot, trade via Shapley-Scarf cycles. Strategy-proof and Pareto efficient for students (unlike DA). Used in New Orleans.

Source: Abdulkadiroglu & Sonmez (2003) "School Choice: A Mechanism Design Approach."

**Kidney Exchange**

Problem: A patient needs a kidney, their willing donor is incompatible. Solution: find cycles or chains of incompatible patient-donor pairs who can "swap."

Key innovation — **non-simultaneous extended altruistic donor (NEAD) chains** (Roth, Sonmez & Unver 2004, Rees et al. 2009): A chain starts with an altruistic (non-directed) donor, who gives to a patient whose paired donor gives to the next patient, etc. Chains can be very long because they don't require simultaneous surgery.

Impact: ~550 transplants/year in the US via exchange (2020s), up from near-zero before 2004. The Alliance for Paired Kidney Donation and the National Kidney Registry run the largest programs.

### One-Sided Matching

**Housing market (Shapley & Scarf 1974)**: Each agent "owns" an object and has preferences over all objects. Top Trading Cycles (TTC) finds the unique core allocation.

**Random assignment**: When no initial endowment exists, the Probabilistic Serial mechanism (Bogomolnaia & Moulin 2001) achieves ordinally efficient and envy-free (in expectation) assignments.

## Fair Division

### Divisible Goods (Cake-Cutting)

**Model**: A heterogeneous divisible resource ("cake") must be divided among n agents with different valuations over different parts.

**Fairness criteria**:
- **Proportionality**: each agent values their piece at ≥ 1/n of the whole
- **Envy-freeness**: no agent prefers another's piece (strictly stronger than proportionality for n ≥ 3)
- **Equitability**: all agents assign the same value to their piece
- **Pareto efficiency**: no reallocation makes someone better off without making another worse off

**Key results**:
| n | Proportional | Envy-Free | Efficient + EF |
|---|-------------|-----------|----------------|
| 2 | Cut-and-choose (ancient) | Cut-and-choose | Yes (same) |
| 3 | Last diminisher (Steinhaus 1948) | Selfridge-Conway (1960) | Requires continuous procedures |
| n | Last diminisher | Aziz & Mackenzie (2016) | Open problem for discrete protocols |

**The Aziz-Mackenzie result** (2016): Proved the first bounded envy-free cake-cutting protocol for any number of agents. Previously, only unbounded protocols (potentially requiring infinite steps) were known for n ≥ 4.

### Indivisible Goods

**Challenge**: Envy-freeness may be impossible (you can't split an indivisible item).

**Relaxations**:
- **EF1 (Envy-Free up to one good)**: After removing one item from the envied bundle, no envy remains. Always exists, computed by round-robin picking with any ordering.
- **EFX (Envy-Free up to any good)**: After removing *any* item from the envied bundle, no envy remains. Existence for general valuations is a major open problem (as of 2025).
- **MMS (Maximin Share)**: Each agent gets at least the value they could guarantee by dividing items into n bundles and taking the worst. Does not always exist, but 3/4-MMS allocations always exist (Ghodsi et al. 2021).

**Practical mechanisms**:
- **Adjusted Winner** (Brams & Taylor 1996): Two agents allocate items by point-spending. Produces envy-free, efficient, and equitable allocations.
- **Spliddit.org**: Web platform implementing various fair division algorithms (Caragiannis et al. 2019). Demonstrates practical deployment.

### Fair Division with Money

When monetary transfers are allowed (TU setting):
- **Rent division**: Assign rooms and prices so that each tenant prefers their own room at their price. Always achievable (Svensson 1983). The Rental Harmony theorem guarantees existence.
- **Cost sharing**: Divide shared costs fairly. Shapley value provides the standard solution (each agent pays their marginal cost averaged over orderings).

## Connections Between Matching and Cooperative Game Theory

**Matching as a cooperative game**: A matching market can be modeled as a TU game where v(S) = the maximum total "match value" achievable by coalition S. The core of this game corresponds exactly to the set of stable matchings with equilibrium prices (Shapley & Shubik 1971).

**Assignment game** (Shapley & Shubik 1971): One-to-one matching with transferable utility. The core is always non-empty and equals the set of competitive equilibrium prices. The proposer-optimal and receiver-optimal stable matchings correspond to the two extreme points of the core.
