---
name: learning-in-games
description: >
  Learning dynamics in strategic settings covering fictitious play, no-regret learning, regret
  matching, multi-agent reinforcement learning, self-play, and convergence results. Reference when
  analyzing how agents adapt strategies over time, whether learning converges to equilibrium, or
  how AI systems learn to play games. Use when the question involves dynamic adaptation, not
  static analysis.
---

# Learning in Games — The Adapters

How do agents learn to play games? Classical game theory assumes players arrive at equilibrium. Learning theory asks *how* — through what process of trial, error, and adaptation do players (human, algorithmic, or artificial) converge to stable strategies? This question connects classical game theory to multi-agent AI, online learning, and the foundations of intelligence. Grounded primarily in Fudenberg & Levine (1998), Cesa-Bianchi & Lugosi (2006), and the modern MARL literature.

## Classical Learning Models

### Fictitious Play (Brown 1951)

Each player maintains beliefs about opponents' strategies based on the empirical frequency of past play. At each round, play a best response to these empirical frequencies.

**Convergence results**:
- **Converges** in: 2×2 games, zero-sum games, potential games, games with identical interests
- **Does NOT converge** in: Shapley's example (3×3 game where beliefs cycle). This was one of the earliest demonstrations that learning can fail to reach equilibrium.

**Key insight**: Fictitious play is a model of *belief-based* learning — players learn about opponents' strategies by observing their past actions. It's the simplest model of strategic learning but already reveals the convergence/non-convergence dichotomy.

### Best Response Dynamics

At each period, each player simultaneously switches to a best response against the current strategy profile. No memory, no learning — just myopic optimization.

**Convergence**: Converges in potential games (the potential function strictly increases at each step). Does NOT converge in general — can cycle in games without potential structure.

## No-Regret Learning

The central framework of modern algorithmic game theory. Instead of modeling how players learn, define a *performance guarantee*: the player's cumulative payoff should be nearly as good as the best fixed strategy in hindsight.

### Regret and No-Regret

**External regret** of a learning algorithm after T rounds:
R_T = max_a [Σₜ u(a, s₋ᵢᵗ)] - Σₜ u(aᵗ, s₋ᵢᵗ)

The gap between the best fixed action in hindsight and the algorithm's cumulative payoff. An algorithm has **no external regret** if R_T / T → 0 as T → ∞.

**Internal regret**: For every pair of actions (a, b), the algorithm doesn't regret not having played b every time it played a. Stronger than external regret.

### Key Algorithms

**Multiplicative Weights Update (MWU)** / Hedge (Freund & Schapire 1999):
Maintain a weight for each action. Update weights multiplicatively based on payoffs:
wᵢᵗ⁺¹ = wᵢᵗ × (1 + ε × payoffᵢᵗ)

Achieves O(√(T log n)) external regret — sublinear, meaning average regret → 0.

**Regret Matching** (Hart & Mas-Colell 2000):
At each round, play the action whose cumulative regret (against the current action) is highest, with probability proportional to that regret.

Achieves no internal regret. In two-player games, if both players use regret matching, the empirical frequency of play converges to the set of **correlated equilibria** (not Nash, but a weaker concept).

**EXP3** (Auer et al. 2002):
For the **bandit** setting (observe only the payoff of the chosen action, not other actions). Achieves O(√(Tn log n)) regret. Essential for settings where players can't observe the full payoff matrix.

### Convergence Results

**The Folk Theorem of Online Learning** (Hart & Mas-Colell 2000):
If all players use no-internal-regret algorithms, the empirical distribution of play converges to the set of **correlated equilibria**.

If all players use no-external-regret algorithms, convergence is to the set of **coarse correlated equilibria** (CCE) — even weaker than CE.

**In zero-sum games**: No-regret learning converges to Nash equilibrium (specifically, to the minimax value). This is the computational basis for solving two-player zero-sum games.

**In general games**: No-regret learning does NOT converge to Nash equilibrium. It converges to the larger set of CCE/CE. This is why CCE and CE are increasingly viewed as the "right" solution concepts for learning settings.

## Multi-Agent Reinforcement Learning (MARL)

When the game is complex and the payoff structure is unknown, agents use reinforcement learning — learning through direct experience of rewards.

### Self-Play

Train an agent by having it play against itself (or copies of itself). The agent improves by exploiting its own weaknesses.

**Landmarks**:
- **TD-Gammon** (Tesauro 1995): Self-play + temporal difference learning for backgammon. Reached expert-level play.
- **AlphaGo** (Silver et al. 2016): Monte Carlo tree search + deep RL. Beat world champion at Go.
- **AlphaZero** (Silver et al. 2018): Self-play from scratch (no human data) in chess, Go, and shogi. Tabula rasa learning.
- **Pluribus** (Brown & Sandholm 2019): Self-play for 6-player no-limit Texas hold'em. First AI to beat professionals in multiplayer poker.

### Policy Space Response Oracles (PSRO) (Lanctot et al. 2017)

A meta-algorithm for finding approximate Nash equilibria in large games:
1. Start with a small set of policies
2. Compute a Nash equilibrium over the current policy set (a "meta-game")
3. Train a new best-response policy against the meta-Nash mixture
4. Add the new policy to the set and repeat

PSRO generalizes both fictitious play (restricted to pure best responses) and double oracle (exact best responses). It's the current standard for training AI in complex multi-agent settings.

### Independent Learning vs. Centralized Training

| Approach | Description | Convergence | Scalability |
|----------|-------------|-------------|-------------|
| **Independent learners** | Each agent learns independently, treating others as part of the environment | Not guaranteed (non-stationarity) | High |
| **Centralized training, decentralized execution (CTDE)** | A central trainer coordinates learning; at deployment, each agent acts independently | Better convergence guarantees | Medium |
| **Fully centralized** | Joint policy optimization | Best convergence | Low (exponential in # agents) |

### Mean Field Games (Lasry & Lions 2007, Huang, Malhame & Caines 2006)

When the number of agents is very large, individual interactions become negligible. Each agent interacts with the **mean field** — the aggregate distribution of all agents' strategies.

**Key simplification**: Instead of N interacting agents (exponential state space), solve a representative agent's problem against the population distribution, then verify that the resulting distribution is self-consistent (a fixed point).

**Applications**: Traffic flow, crowd dynamics, financial markets with many small traders, epidemic modeling, network congestion with many users.

## AI and Game Theory Frontier

**LLM alignment as a game**: The interaction between an AI system and its human overseers can be modeled as a principal-agent game with information asymmetry. RLHF (Reinforcement Learning from Human Feedback) is a mechanism design problem — designing the reward structure so the AI's learned behavior aligns with human preferences.

**Adversarial robustness**: Adversarial attacks on ML models are a zero-sum game between attacker and defender. Training robust models ≈ finding mixed-strategy Nash equilibria.

**GANs as games**: Generative Adversarial Networks are a two-player zero-sum game between generator and discriminator. Training dynamics mirror learning in games — and suffer from the same convergence issues (mode collapse ≈ cycling).

## Sources

Read `references/sources.md` for the full bibliography — classical learning theory (Fudenberg & Levine), online learning (Cesa-Bianchi & Lugosi), and MARL references.

## When This Applies

- Predicting long-run outcomes when agents repeatedly interact and adapt
- Choosing or designing learning algorithms for multi-agent systems
- Understanding convergence properties — will a system of learning agents stabilize?
- Training AI agents in strategic settings (self-play, PSRO, MARL)
- Evaluating whether Nash equilibrium is a reasonable prediction when agents learn
