---
name: bayesian-persuasion
description: >
  Modern information design and strategic communication theory. Reference when analyzing how
  a sender optimally designs information to influence a receiver's actions, when studying cheap
  talk and strategic communication, or when evaluating disclosure policies. Use when the question
  is about designing what information to reveal, not what action to take.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
---

# Bayesian Persuasion — The Information Architect

The modern theory of strategic information design. Classical information economics asks "how do informed parties reveal or conceal what they know?" Bayesian persuasion flips this: "how should a sender *design* the information structure that a receiver will observe?" This reframing, formalized by Kamenica & Gentzkow (2011), has transformed how we think about media, regulation, recommendation systems, and platform design. Grounded primarily in Kamenica & Gentzkow (2011), Bergemann & Morris (2016), and Crawford & Sobel (1982).

## The Bayesian Persuasion Framework

### The Setup (Kamenica & Gentzkow 2011)

1. **A state of the world** ω is drawn from a known prior distribution
2. **A sender** designs a **signal** (experiment/test/information structure) before observing ω
3. The signal generates a **realization** that the **receiver** observes
4. The **receiver** updates beliefs (Bayes' rule) and takes an **action** that affects both players
5. The sender **commits** to the signal structure before the state is realized

**The key insight**: The sender chooses a distribution over the receiver's posterior beliefs, subject to the constraint that posteriors must be a mean-preserving spread of the prior (Bayes plausibility). The optimal signal is found by **concavification** — taking the concave closure of the sender's value function over the receiver's belief space.

### Concavification

The sender's problem reduces to geometry:

1. For each possible posterior belief μ, compute the sender's expected payoff V(μ) given the receiver's optimal action at belief μ
2. Take the **concave closure** (concavification) of V — the smallest concave function ≥ V
3. The sender's optimal payoff equals the concavified value at the prior belief
4. The **optimal signal** is any signal that induces posteriors on the concave closure, with the prior as their average

**Geometric intuition**: The sender can achieve any payoff that lies on or below the concave closure of V. The concavification represents the best the sender can do by "mixing" different information revelations.

### Example: The Prosecutor

A prosecutor wants a judge to convict. The judge convicts iff P(guilty) ≥ 0.5. The prior is P(guilty) = 0.3.

Without persuasion: judge acquits (0.3 < 0.5). The prosecutor's payoff is 0.

Optimal signal: design an "investigation" that sometimes produces "evidence of guilt" and sometimes "evidence of innocence." The optimal investigation:
- When guilty → always produce "evidence of guilt"
- When innocent → produce "evidence of guilt" with probability 3/7, "evidence of innocence" with probability 4/7

Result: when "evidence of guilt" is produced, P(guilty | evidence) = exactly 0.5 → judge convicts. This happens with probability 0.3(1) + 0.7(3/7) = 0.6. The prosecutor gets conviction 60% of the time, up from 0%.

## Cheap Talk — Crawford & Sobel (1982)

Strategic communication **without commitment**. The sender observes the state and sends a costless message. The receiver takes an action.

**Key difference from Bayesian persuasion**: In cheap talk, the sender talks *after* observing the state. There's no commitment — the sender can say whatever they want. Credibility comes only from the equilibrium structure.

### The Crawford-Sobel Model

- State ω ~ Uniform[0,1]
- Sender prefers the receiver's action to be biased upward by b > 0 relative to what the receiver wants
- Equilibrium: the state space is partitioned into intervals. The sender reports which interval contains the state, but not the exact state.

**Key results**:
- Only **partition equilibria** exist — the sender reports "the state is in interval [aₖ, aₖ₊₁]"
- More intervals (more informative communication) when sender-receiver **interests are more aligned** (b is small)
- As b → 0, communication approaches full revelation
- As b → ∞, no information is transmitted (babbling equilibrium only)
- Multiple equilibria exist; the most informative equilibrium has the most intervals

**Applications**: Expert advice to decision-makers, political communication, analyst recommendations, lobbying.

## Verifiable Disclosure

An intermediate model: the sender can choose whether to disclose verifiable information (but cannot lie).

### Unraveling Theorem (Grossman 1981, Milgrom 1981)

If information is verifiable and all types can disclose:
- The best type discloses (to separate from the rest)
- The second-best type, now worst among non-disclosers, also discloses
- **Cascade**: Full unraveling → everyone discloses

**When unraveling fails**:
- Disclosure costs (small costs can sustain non-disclosure)
- Uncertainty about whether the sender *has* information
- Multi-dimensional information (disclosing one dimension obscures another)
- Naive receivers who don't penalize non-disclosure

## Information Design with Multiple Receivers

Bergemann & Morris (2016, 2019) generalize persuasion to multiple agents who interact strategically.

The information designer chooses a **Bayes correlated equilibrium (BCE)** — an information structure plus a strategy profile where each agent best-responds to their signal given the correlation structure. The set of BCE outcomes characterizes everything achievable through information design.

**Key insight**: Information design in games is equivalent to choosing a Bayes correlated equilibrium. This connects persuasion to correlated equilibrium and unlocks results from the equilibrium theory.

**Applications**:
- **Platform design**: What should Uber show drivers about ride requests? What should Amazon show sellers about competitor prices?
- **Financial regulation**: How much should rating agencies reveal about asset quality?
- **Media and polarization**: How do media outlets' information design choices affect political polarization?
- **Stress tests**: Bank stress tests as Bayesian persuasion — regulators design the information revealed to markets

## Modern Extensions

**Dynamic Bayesian persuasion**: Sender reveals information over time. Timing matters — early revelation forecloses future options. Applications to clinical trials, news cycles, investment.

**Competition in persuasion**: Multiple senders compete to influence a receiver. The receiver benefits from competition (more information). Results connect to media economics and political advertising.

**Robust persuasion**: Sender designs signals when the prior is uncertain or when the receiver may have private information. Connects to robust mechanism design.

**Attention and persuasion**: The receiver has limited attention. The sender must design information that both informs and attracts attention. Models of clickbait, sensationalism, and media strategy.

## Sources

Read `references/sources.md` for the full bibliography — founding papers (Kamenica & Gentzkow, Crawford & Sobel, Bergemann & Morris), surveys, and modern extensions.

## When This Applies

- Designing what information to show users (recommendation systems, search results, ratings)
- Analyzing media strategy, political communication, or advertising
- Evaluating disclosure policies for regulators (stress tests, mandatory reporting)
- Platform information design (what drivers/sellers/buyers see)
- Any setting where a party chooses what information others observe
