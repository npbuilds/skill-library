---
name: behavioral-game-theory
description: >
  Behavioral game theory foundations covering how real humans deviate from Nash equilibrium.
  Reference when analyzing level-k thinking, quantal response equilibrium, social preferences,
  experimental game theory results, or predicting actual human strategic behavior. Use when the
  question involves bounded rationality or empirical prediction, not normative analysis.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
---

# Behavioral Game Theory — The Empiricist

Classical game theory assumes players are perfectly rational, have unlimited computational power, and care only about their own payoffs. Behavioral game theory documents how real humans systematically deviate from these assumptions — and builds models that predict actual behavior. This is the empirical wing of game theory, grounded in laboratory experiments and field data. Grounded primarily in Camerer (2003), Crawford, Costa-Gomes & Iriberri (2013), and the experimental literature.

## Core Deviations from Nash

### 1. Limited Depth of Reasoning — Level-k and Cognitive Hierarchy

**The beauty contest** (Nagel 1995): Players choose a number from 0-100. The winner is closest to 2/3 of the average. Nash equilibrium: everyone chooses 0 (iterated elimination of dominated strategies). Actual median in experiments: around 33 (one step of reasoning) or 22 (two steps).

**Level-k model** (Stahl & Wilson 1994, 1995):
- **Level-0**: Randomizes uniformly (anchor point)
- **Level-1**: Best-responds to Level-0
- **Level-2**: Best-responds to Level-1
- **Level-k**: Best-responds to Level-(k-1)

Most experimental subjects appear to be Level-1 or Level-2. Very few reason beyond Level-3. This explains why equilibrium is rarely observed in one-shot games requiring deep iterated reasoning.

**Cognitive hierarchy** (Camerer, Ho & Chong 2004): Like level-k but each level best-responds to a distribution (Poisson) of lower levels, not just the level immediately below. Better fits data because higher levels account for the mixture of reasoning depths below them.

**Applications**: Auctions (overbidding in first-price), market entry games, guessing games, initial play in novel strategic situations.

### 2. Noisy Best Response — Quantal Response Equilibrium

**QRE** (McKelvey & Palfrey 1995): Players don't always best-respond — they choose better strategies *more often* but not *always*. The probability of choosing action a is proportional to exp(λ × payoff(a)), where λ captures rationality.

- λ = 0: Completely random (uniform over actions)
- λ → ∞: Perfect best response (Nash equilibrium)
- Intermediate λ: Stochastic choice with a bias toward better options

**Key result**: QRE explains several anomalies: overbidding in auctions, cooperation in one-shot PD, matching pennies data, and asymmetric play in symmetric games.

**Agent QRE (AQRE)**: Extends QRE to extensive-form games. Players make noisy choices at each decision node, not just at the game level. Better captures sequential reasoning errors.

### 3. Social Preferences — Beyond Self-Interest

Humans don't just maximize their own payoff. Experimental evidence shows:

**Inequality aversion** (Fehr & Schmidt 1999):
Utility = own payoff - α × max(other's payoff - mine, 0) - β × max(mine - other's payoff, 0)
People dislike both being behind (α) and being ahead (β), with α > β typically.

**Reciprocity** (Rabin 1993):
People are kind to those who are kind to them and unkind to those who are unkind. Utility depends on both material payoff and the *perceived intentions* of the other player.

**Evidence**:
- **Ultimatum game**: Proposers offer 40-50% (not the minimal amount Nash predicts). Respondents reject offers below ~20% (preferring nothing to unfairness).
- **Dictator game**: Even without strategic pressure, dictators give 20-30% on average. Pure self-interest predicts 0%.
- **Public goods game**: Initial contributions of 40-60% (not 0%). Contributions decline with repetition but punishment sustains cooperation.
- **Trust game**: Investors send ~50% and trustees return ~30-40% of the tripled amount. Both exceed Nash predictions.

### 4. Probability Weighting and Framing

**Prospect theory** (Kahneman & Tversky 1979) in games: Players overweight small probabilities and underweight large ones. Reference-point dependent: outcomes are evaluated as gains or losses relative to a reference point, with loss aversion (losses loom larger than equivalent gains).

**Framing effects**: The same game presented differently produces different behavior. "Cooperation game" framing increases cooperation vs. "Wall Street game" framing (same payoffs, different labels).

## Experimental Methodology

### Standard Experimental Games

| Game | Nash Prediction | Typical Experimental Result |
|------|-----------------|---------------------------|
| **Ultimatum** | Proposer offers minimum; responder accepts | 40-50% offers; rejection below ~20% |
| **Dictator** | Give nothing | Average 20-30% given |
| **Public goods** | Contribute nothing | 40-60% initial, declining without punishment |
| **Matching pennies** | 50-50 mix | Close to Nash, slight deviations |
| **Beauty contest** | Choose 0 | Median ~22-33, far from 0 |
| **Centipede** | Immediate stop | Many passes, especially early |
| **Prisoner's dilemma** | Defect | 40-60% cooperation in one-shot |
| **Traveler's dilemma** | Choose minimum ($2) | Average ~$180 (near maximum) |

### Key Design Principles

- **Real monetary incentives**: Subjects are paid based on outcomes (not hypothetical)
- **Anonymity**: Paired anonymously to eliminate reputation effects
- **Repetition**: One-shot vs. repeated games to test learning and convergence
- **Strategy method**: Subjects specify complete strategies (contingent plans) for all possible situations
- **Belief elicitation**: Subjects report beliefs about others' actions (incentivized)

## Predictive Models: Summary

| Model | Captures | Misses | Best For |
|-------|----------|--------|----------|
| **Level-k** | Initial play in novel games | Learning, repeated play | One-shot games with dominated strategies |
| **QRE** | Noisy behavior, interior probabilities | Systematic biases, social preferences | Games with mixed equilibria |
| **Inequality aversion** | Rejection in ultimatum, cooperation | Pure-strategy games without fairness component | Bargaining, public goods |
| **Reciprocity** | Trust, gift exchange, punishment | One-shot anonymous interactions | Repeated interactions, labor markets |
| **Prospect theory** | Risk behavior in games, framing | Social interaction effects | Games with lotteries, risk |

## Sources

Read `references/sources.md` for the full bibliography — primary texts (Camerer 2003), key experimental papers, and model specifications.

## When This Applies

- Predicting what real humans will actually do in a strategic situation (not what they "should" do)
- Explaining experimental results that deviate from Nash predictions
- Designing interfaces, contracts, or institutions that account for bounded rationality
- Evaluating whether a game-theoretic prediction is likely to hold with real human players
- Calibrating theoretical models with empirical behavior data

## Cross-Domain Connections

- **Investing/reflexivity-sentiment/market-psychology**: Level-k thinking explains market anomalies — most investors are level-1 thinkers (best-responding to naive expectations). Behavioral biases catalogued in market psychology (herding, anchoring, disposition effect) map directly to QRE and prospect theory in games. The beauty contest game IS the stock market.
- **Investing/risk-architecture/drawdown-psychology**: Prospect theory's loss aversion and probability weighting explain why investors hold losers too long and sell winners too early, and why tail-risk hedging is psychologically valuable beyond its expected return.



## Related Skills

- **bias-detector** — Behavioral-game-theory and bias-detector diagnose the same family of deviations from rational choice. Behavioral-game-theory frames them as strategic regularities; bias-detector frames them as epistemic distortions.
- **decision-architect** — Decision-architect designs choice environments that take behavioral-game-theory findings as constraints. The two are complementary: behavioral-game-theory predicts deviations; decision-architect intervenes on them.
