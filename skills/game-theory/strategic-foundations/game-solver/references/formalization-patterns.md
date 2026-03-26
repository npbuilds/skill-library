# Formalization Patterns — Real-World to Game Mappings

A lookup table for mapping informal strategic situations to formal game structures. Each pattern includes the canonical game model, the key strategic insight, and what to watch for.

## Market and Business Strategy

### Price Competition

**Situation**: Two or more firms selling similar products choose prices.
**Model**: Bertrand Competition
**Players**: Firms
**Strategies**: Price levels (continuous)
**Key insight**: With identical products, the unique equilibrium is price = marginal cost, even with only two firms (Bertrand paradox). Differentiation, capacity constraints, or search costs restore positive profits.
**Variations**:
- Product differentiation → Hotelling model (spatial competition)
- Capacity constraints → Edgeworth model (Bertrand + capacity)
- Repeated interaction → Tacit collusion possible via folk theorem

### Quantity Competition

**Situation**: Firms choose production quantities; market price adjusts.
**Model**: Cournot Competition
**Players**: Firms
**Strategies**: Quantity levels (continuous)
**Key insight**: Equilibrium output is between monopoly and competitive levels. More firms → more output → lower prices. Leader-follower timing → Stackelberg model.
**When to use Cournot vs. Bertrand**: Cournot when capacity/quantity decisions are the strategic variable (oil production, airline seats). Bertrand when firms set prices and can serve any demand (retail, software).

### Market Entry

**Situation**: A potential entrant considers entering a market with an incumbent.
**Model**: Entry Deterrence Game (sequential)
**Players**: Incumbent, Entrant
**Strategies**: Entrant: Enter/Stay Out. Incumbent: Accommodate/Fight.
**Key insight**: "Fight if you enter" is credible only if backed by irreversible investment (capacity, reputation). Without commitment, accommodation is the subgame perfect outcome. With commitment (sunk capacity), deterrence can be credible.
**Variations**:
- Limit pricing: incumbent sets low price to signal low costs
- Predatory pricing: incumbent prices below cost to drive out entrant
- Multiple entrants: sequential entry with learning

### Platform Competition

**Situation**: Two-sided market where platforms compete for users on both sides.
**Model**: Two-sided market game (network externalities)
**Players**: Platforms, users on side A, users on side B
**Key insight**: Winner-take-all dynamics possible due to cross-side network effects. Subsidize the "money" side to attract the "subsidy" side. Chicken dynamics between platforms (first to establish critical mass wins).
**Formalization**: Often modeled as coordination game with network externalities.

### Make vs. Buy / Outsourcing

**Situation**: Firm decides whether to produce internally or contract with a supplier.
**Model**: Principal-Agent / Hold-up Game
**Key insight**: Relationship-specific investments create hold-up risk. Without complete contracts, underinvestment occurs. Vertical integration solves hold-up but loses market incentives.
**Source**: Williamson's transaction cost economics, formalized by Hart & Moore (1990).

## Negotiation and Bargaining

### Bilateral Negotiation

**Situation**: Two parties negotiate over terms (salary, price, treaty).
**Model**: Nash Bargaining / Rubinstein Alternating Offers
**Key parameters**: Disagreement point (BATNA), discount factors (patience), outside options.
**Key insight**: Your BATNA determines your negotiating power more than anything else. Improving your outside option improves your negotiated outcome.
**Practical mapping**: Identify each side's BATNA → compute Nash bargaining solution → the predicted split is proportional to bargaining power.

### Multi-Party Negotiation

**Situation**: Three or more parties must agree on a joint decision.
**Model**: Coalitional game + legislative bargaining (Baron-Ferejohn)
**Key insight**: Minimum winning coalitions form — the proposer includes only enough partners to pass, giving them the minimum necessary. Excluded parties get nothing.
**Practical mapping**: Compute Shapley values for each party's voting power. Power depends on who you can form winning coalitions with, not just your vote share.

### Negotiation with Deadlines

**Situation**: Negotiation with a known end date.
**Model**: Finite-horizon Rubinstein bargaining
**Key insight**: The party who loses more from deadline expiration has less bargaining power. Backward induction from the deadline determines the equilibrium offer at every stage.

## Technology and Standards

### Standard-Setting / Platform Adoption

**Situation**: Multiple players must coordinate on a standard, but prefer their own.
**Model**: Battle of the Sexes / Coordination Game
**Key insight**: Multiple equilibria exist. Focal points, first-mover advantage, and commitment matter. Network effects amplify coordination benefits.
**Examples**: VHS vs. Betamax, USB-C adoption, programming language ecosystems.

### Technology Arms Race

**Situation**: Firms or nations invest in competing technologies.
**Model**: All-Pay Auction or Prisoner's Dilemma (depending on structure)
**Key insight**: If spending is non-recoverable (R&D sunk costs), the game resembles an all-pay auction where expected returns may be negative. If mutual restraint is preferred but unilateral investment is tempting, it's a Prisoner's Dilemma / arms race.

### Open Source vs. Proprietary

**Situation**: Firms decide whether to open-source technology.
**Model**: Public Goods Game / Prisoner's Dilemma
**Key insight**: Open-sourcing benefits everyone but the contributor bears the cost. Repeated interaction, reputation, and complementary business models (services, premium features) sustain open-source contribution.

## Political and Institutional

### Voting and Elections

**Situation**: Voters choose between candidates; candidates choose platforms.
**Model**: Median Voter Theorem (Hotelling-Downs)
**Key insight**: In a single-dimensional policy space with majority rule, both candidates converge to the median voter's preferred position. Departures occur with: multiple dimensions, ideological primary voters, abstention, valence advantages.

### Legislative Bargaining

**Situation**: Legislature divides a budget or chooses a policy.
**Model**: Baron-Ferejohn (1989) — random proposer, majority rule
**Key insight**: The proposer captures a disproportionate share. Proposal power > voting power. Delay is costly, so responders accept offers below their "fair share."

### International Relations / Deterrence

**Situation**: Nations choose whether to escalate or back down.
**Model**: Chicken / Brinkmanship
**Key insight**: Credible commitment to escalation (burning bridges, delegation to hawks) gives bargaining advantage. But mutual commitment to escalation is catastrophic. Schelling's "rationality of irrationality."
**Variations**: Repeated deterrence games, reputation building, audience costs.

### Regulatory Games

**Situation**: Regulator sets rules; firms respond strategically.
**Model**: Stackelberg game (regulator leads) or mechanism design
**Key insight**: Firms will game any fixed rule. The regulator must anticipate strategic responses. Optimal regulation accounts for incentive compatibility.

## Interpersonal and Social

### Trust and Cooperation

**Situation**: Two parties can cooperate for mutual benefit, but cheating is tempting.
**Model**: Prisoner's Dilemma (one-shot or repeated)
**Key insight**: One-shot → defection. Repeated with long enough shadow of the future → cooperation sustainable via trigger strategies. Key parameter: discount factor (how much the future matters).

### Coordination Problems

**Situation**: Group members must coordinate actions but can't communicate (or communication is cheap talk).
**Model**: Stag Hunt / Coordination Game
**Key insight**: Even when coordination is Pareto-optimal, risk-dominance may select the safe (uncoordinated) outcome. Focal points, leadership, and conventions solve coordination.

### Information Sharing

**Situation**: One party has information that affects another's decision.
**Model**: Signaling Game (costly signals) or Cheap Talk (costless)
**Key insight**: Costless communication may not be credible (cheap talk allows partial but not full revelation). Costly signals (education in the job market, advertising spend for quality) can credibly convey private information.

## Formalization Checklist

When mapping a real-world situation to a game, verify:

- [ ] **Players are well-defined** — not "the market" but specific decision-makers
- [ ] **Strategies are actionable** — things players can actually choose, not outcomes
- [ ] **Payoffs capture what players actually care about** — not just money (reputation, fairness, long-term relationship)
- [ ] **Timing is specified** — simultaneous, sequential, or repeated?
- [ ] **Information structure is explicit** — what does each player observe?
- [ ] **The model simplification is documented** — what's left out, and does it matter?
