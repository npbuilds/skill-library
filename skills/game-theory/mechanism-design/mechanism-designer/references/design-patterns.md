# Mechanism Design Patterns — Common Problems and Solutions

## Pattern 1: Single-Item Allocation with Money

**Problem**: Allocate one item to one of n bidders with private values.

**If revenue is primary**:
→ Myerson optimal auction: second-price with optimal reserve r* where ψ(r*) = 0
→ For uniform [0,1] values: r* = 1/2

**If efficiency is primary**:
→ Vickrey (second-price, no reserve): allocates to highest-valued bidder, DSIC, efficient
→ Revenue ≤ Myerson optimal but no deadweight loss

**If simplicity is primary**:
→ English (ascending) auction: equivalent to Vickrey under IPV, behaviorally simpler
→ Under affiliated values, English strictly dominates Vickrey on revenue

## Pattern 2: Multiple Homogeneous Items

**Problem**: Allocate k identical items to n bidders (k < n), each wanting at most one.

**Uniform-price auction**: All winners pay the same price (highest losing bid or lowest winning bid). Simple, approximately efficient. Strategic demand reduction possible.

**Vickrey (pay-as-bid VCG)**: Each winner pays the externality they impose. DSIC, efficient. But may generate low revenue and be vulnerable to collusion.

**Discriminatory (pay-as-bid)**: Winners pay their own bids. Revenue-advantaged when bidders are risk-averse. Used in some Treasury auctions.

## Pattern 3: Multiple Heterogeneous Items (Combinatorial)

**Problem**: Allocate multiple distinct items to bidders who have values over bundles.

**Combinatorial VCG**: Truthful, efficient. But:
- Winner determination is NP-hard
- Revenue can be zero (even negative if budget balance is required)
- Vulnerable to group manipulation

**Combinatorial clock auction**: Practical alternative. Clock phase for price discovery, supplementary round for fine-tuning. Core-selecting payment rules approximate VCG.

**Proxy auctions (Ausubel-Milgrom)**: Bidders report valuations to proxy agents. Ascending auction between proxies. Core-selecting outcomes when goods are substitutes.

## Pattern 4: Bilateral Trade

**Problem**: One buyer, one seller, private values. Should they trade?

**Myerson-Satterthwaite impossibility**: No mechanism is simultaneously efficient, DSIC, IR, and budget-balanced.

**Best available mechanisms**:
- **Posted price**: Seller sets a price. Simple, but misses some efficient trades.
- **k-double auction**: Both submit bids, trade at average if buyer > seller. At k = 1/2, maximizes expected surplus among IC, IR, BB mechanisms.
- **Broker mechanism**: A third party subsidizes trade. Can achieve efficiency if budget balance isn't required.

## Pattern 5: Public Goods Provision

**Problem**: A group benefits from a public good. Each member has a private value for it. Should it be provided? How should costs be shared?

**VCG (Clarke pivot mechanism)**: Each agent pays the externality they impose. Truthful, efficient provision decision. But runs a surplus (not budget-balanced).

**Expected externality mechanism (d'Aspremont & Gerard-Varet 1979)**: BIC, efficient, budget-balanced. But not DSIC and not ex post IR.

**Practical approach**: Contribution games with thresholds (provision point mechanisms). If contributions meet the threshold, the good is provided; otherwise, contributions are refunded. Approximates efficiency for large groups.

## Pattern 6: Assignment Without Money

**Problem**: Assign n objects to n agents. No money.

**Random Serial Dictatorship (RSD)**: Random ordering, each agent picks top remaining. Strategy-proof, ex ante fair.

**Probabilistic Serial (PS)**: Agents "eat" preferred objects simultaneously at equal speed. Ordinally efficient, envy-free in expectation, but not strategy-proof.

**Top Trading Cycles (TTC)**: If agents have initial endowments. Strategy-proof, Pareto efficient, unique core outcome.

**Choice of mechanism depends on**: whether initial endowments exist (TTC), whether probabilistic outcomes are acceptable (PS), and whether simplicity dominates (RSD).

## Pattern 7: Two-Sided Matching

**Problem**: Match agents on two sides (students/schools, residents/hospitals).

**Stability primary → DA**: Stable, strategy-proof for proposing side. Not efficient.

**Efficiency primary → TTC**: Efficient for one side, strategy-proof for all. Not stable.

**Compromise → Hybrid**: Theoretical work on "approximately stable and approximately efficient" mechanisms exists but is not yet widely deployed.

## Pattern 8: Repeated/Dynamic Allocation

**Problem**: Allocate resources over time. Agents arrive and depart.

**Challenges**: Agents can misreport arrival/departure times, wait strategically, or manipulate based on learning.

**Online mechanisms**: Process agents as they arrive. Can't wait for full information. Competitive ratio analysis (how close to the offline optimum?).

**Dynamic VCG (Bergemann & Valimaki 2010)**: Extends VCG to dynamic settings. Truthful reporting of all private information (values, arrivals, departures) is a dominant strategy. But computationally demanding and requires commitment to future payment rules.

## Pattern 9: DAO/Crypto Governance

**Problem**: Decentralized decision-making with token-weighted voting, Sybil resistance, and no trusted central authority.

**Challenges unique to DAOs**:
- **Sybil attacks**: Creating multiple identities to gain disproportionate influence. One-person-one-vote requires identity verification.
- **Vote buying**: On-chain votes are observable, enabling vote markets. Dark DAOs can buy votes anonymously.
- **Plutocracy**: Token-weighted voting gives disproportionate power to large holders.

**Mechanism options**:
- **Quadratic voting**: Mitigates plutocracy by making marginal vote influence decrease. Each additional vote costs quadratically more tokens.
- **Conviction voting**: Preferences are expressed continuously; conviction (stake × time) accumulates. Discourages last-minute manipulation.
- **Optimistic governance**: Proposals pass unless challenged. Reduces participation burden. Relies on bonded challengers for oversight.
- **Futarchy**: Decisions made by prediction markets. "Vote on values, bet on beliefs." Theoretically appealing but practically challenging.

## Meta-Pattern: The Impossibility-Constructive Cycle

Every mechanism design problem follows this arc:

1. **State the objective** — what properties do you want?
2. **Check impossibilities** — which combinations are provably unachievable?
3. **Choose tradeoffs** — which properties do you sacrifice?
4. **Find the optimal mechanism** — within the feasible space, which mechanism maximizes your priority?
5. **Check practical constraints** — is it implementable, understandable, robust?
6. **Iterate** — if practical constraints bind, relax some properties and redesign
