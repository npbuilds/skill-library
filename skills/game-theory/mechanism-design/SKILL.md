---
name: mechanism-design
description: >
  Direct the mechanism design subdomain — route questions about auction design, market rules,
  matching systems, voting mechanisms, incentive structures, and contract design to the right
  specialist skill. Use when the user needs to design rules or institutions, not just analyze
  an existing strategic interaction.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
allowed-tools: Read Glob
---

# Mechanism Design Director — The Architect

The department head for mechanism design within the game-theory domain. Mechanism design is "reverse game theory" — instead of analyzing a given game, you design the rules of the game to achieve a desired outcome. Routes questions to the right specialist, defines the learning order, and resolves conflicts between design objectives.

## Routing Logic

When a question arrives in this subdomain, classify it and route accordingly:

| Question Pattern | Route To | Why |
|-----------------|----------|-----|
| Auction formats, bidding, revenue maximization, reserve prices, winner determination | `auction-theory` | Auction-specific theory |
| Revenue equivalence, optimal auctions, Myerson's lemma, FCC spectrum, ad auctions | `auction-theory` | Auction design and analysis |
| Stable matching, Gale-Shapley, school choice, kidney exchange, two-sided markets | `matching-markets` | Matching and market design |
| Assignment problems, housing markets, top trading cycles | `matching-markets` | Allocation mechanisms |
| Voting rules, Arrow's theorem, Gibbard-Satterthwaite, social welfare functions | `social-choice` | Social choice theory |
| Strategy-proofness, manipulation, preference aggregation | `social-choice` | Incentive properties of voting |
| "Design a mechanism for X", "How should I structure incentives?" | `mechanism-designer` | Applied mechanism design |
| Revelation principle, VCG, incentive compatibility, individual rationality | `mechanism-designer` first, then relevant theory skill | Core mechanism design concepts applied |
| DAO governance, token incentives, smart contract mechanism design | `mechanism-designer` | Applied — crypto/decentralized |

### Multi-Skill Questions

Some questions need more than one skill. Load them in this priority:

1. `auction-theory` or `matching-markets` or `social-choice` — load the domain-specific theory first
2. `mechanism-designer` — apply the theoretical insights to the specific design problem

This order ensures theory constrains design — you understand the impossibility results and optimal benchmarks before attempting to build something.

**Example multi-skill question**: "Design a fair allocation mechanism for assigning parking spots to employees"
1. `matching-markets` → understand assignment mechanisms, TTC, serial dictatorship
2. `social-choice` → evaluate fairness criteria and impossibility constraints
3. `mechanism-designer` → synthesize into a concrete mechanism proposal with incentive analysis

## Curriculum Order

For learning or progressive loading:

1. **Auction Theory** (foundation) — The most concrete and well-understood branch. Revenue equivalence, optimal auctions, and common formats provide the clearest demonstration of mechanism design principles in action.

2. **Matching Markets** (extension) — Extends design thinking to settings without money. Stability, strategy-proofness, and the tension between fairness properties become central when transfers aren't available.

3. **Social Choice** (generalization) — The broadest perspective. Arrow's theorem and Gibbard-Satterthwaite set the fundamental impossibility boundaries within which all mechanism design operates.

### Level Progression
- **Foundational**: Auction Theory, Matching Markets, Social Choice
- **Intermediate**: (future) Contract Theory, Information Design as Mechanism Design
- **Advanced**: (future) Dynamic Mechanism Design, Combinatorial Mechanism Design, Automated Mechanism Design

## Conflict Resolution

When child skills give contradictory guidance:

| Conflict | Resolution | Reason |
|----------|-----------|--------|
| Auction theory says "use Vickrey" but the setting has budget constraints | Acknowledge impossibility — VCG may not be efficient under budget constraints; explore alternatives (clinching auctions, adaptive reserves) | Standard results assume quasi-linear utility; violations require specialized mechanisms |
| Matching theory says "use DA for stability" but social choice analysis shows it's manipulable for one side | Present the tradeoff — stability vs. full strategy-proofness. Note that TTC achieves strategy-proofness + efficiency but sacrifices stability | Different desiderata may be incompatible; the designer must choose which to prioritize |
| Revenue maximization (auction) conflicts with efficiency (VCG) | Flag the fundamental tradeoff — Myerson optimal auctions maximize revenue but exclude efficient trades; VCG maximizes efficiency but may sacrifice revenue | This is the Myerson-Satterthwaite impossibility in action; no mechanism achieves both simultaneously |
| Fairness criteria conflict with incentive compatibility | Impossibility results win — if a result says you can't have X and Y simultaneously, don't pretend otherwise | Arrow's theorem and GS theorem are hard constraints, not guidelines |

**General rule**: Impossibility theorems > design aspirations. When objectives conflict, present the tradeoff explicitly and let the user choose which properties to prioritize. Never promise a mechanism that violates a proven impossibility result.

## Scope Boundaries

**This director handles**: All questions about designing rules, institutions, auctions, markets, voting systems, allocation mechanisms, and incentive structures. The common thread is that someone has the power to set the rules, and wants to set them well.

**Escalate to the orchestrator when**:
- The question is about analyzing an existing game (not designing rules) → Strategic Foundations
- The question involves evolving populations without a designer → Evolutionary Dynamics
- The question is about strategic information revelation, not mechanism rules → Information Economics
- The question involves computational feasibility of mechanisms → Computational Strategy (but note: many mechanism design questions have computational dimensions — escalate only when computation is the primary concern)

## Cross-Domain Connections

- **Investing/market-microstructure**: Market structure IS mechanism design — exchanges design order matching rules, fee structures, and access tiers to balance liquidity provision, price discovery, and revenue. Market maker obligations, circuit breakers, and auction vs. continuous trading are all mechanism design decisions.
- **Investing/portfolio-construction**: Incentive alignment in systematic investing — factor selection rules, rebalancing triggers, and tax-loss harvesting thresholds are mechanisms that must be incentive-compatible with the investor's stated objectives.
