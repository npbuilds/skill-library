# Sources — Learning in Games

## Primary Texts

**Fudenberg, D. & Levine, D.K. *The Theory of Learning in Games* (MIT Press, 1998)**
The standard reference for classical learning models in games. Covers fictitious play, stochastic fictitious play, best-response dynamics, and convergence results.
→ Used for: fictitious play, convergence theorems, connection between learning and equilibrium.

**Cesa-Bianchi, N. & Lugosi, G. *Prediction, Learning, and Games* (Cambridge, 2006)**
The definitive reference on online learning and no-regret algorithms. Covers multiplicative weights, regret bounds, and connections to game theory.
→ Used for: MWU, EXP3, regret bounds, online learning framework.

**Shoham, Y. & Leyton-Brown, K. *Multiagent Systems* (Cambridge, 2009)**
Chapters on learning in games, no-regret learning, and multi-agent reinforcement learning. Integrated CS-economics perspective.
→ Used for: algorithmic descriptions, MARL foundations.

## Key Papers — Classical Learning

**Brown, G.W. (1951)** "Iterative Solution of Games by Fictitious Play." In *Activity Analysis of Production and Allocation*, Wiley.
→ Introduces fictitious play. Shows convergence for zero-sum games.

**Robinson, J. (1951)** "An Iterative Method of Solving a Game." *Annals of Mathematics* 54: 296-301.
→ Proves fictitious play converges in zero-sum games.

**Shapley, L.S. (1964)** "Some Topics in Two-Person Games." In *Advances in Game Theory*, Princeton.
→ Famous example where fictitious play does NOT converge (3×3 game with cycling beliefs).

## Key Papers — No-Regret Learning

**Freund, Y. & Schapire, R.E. (1999)** "Adaptive Game Playing Using Multiplicative Weights." *Games and Economic Behavior* 29: 79-103.
→ Multiplicative Weights Update algorithm applied to games. Establishes the connection between online learning and equilibrium computation.

**Hart, S. & Mas-Colell, A. (2000)** "A Simple Adaptive Procedure Leading to Correlated Equilibrium." *Econometrica* 68: 1127-1150.
→ Regret matching algorithm. No-internal-regret → convergence to correlated equilibrium. The foundational algorithm for practical equilibrium computation.

**Auer, P., Cesa-Bianchi, N., Freund, Y. & Schapire, R.E. (2002)** "The Nonstochastic Multiarmed Bandit Problem." *SIAM Journal on Computing* 32: 48-77.
→ EXP3 algorithm for adversarial bandits. Essential for partial-information learning.

## Key Papers — MARL and AI

**Silver, D. et al. (2016)** "Mastering the Game of Go with Deep Neural Networks and Tree Search." *Nature* 529: 484-489.
→ AlphaGo. Deep RL + MCTS. First program to beat a professional Go player.

**Silver, D. et al. (2018)** "A General Reinforcement Learning Algorithm that Masters Chess, Shogi, and Go through Self-Play." *Science* 362: 1140-1144.
→ AlphaZero. Tabula rasa learning through self-play in chess, shogi, and Go.

**Brown, N. & Sandholm, T. (2019)** "Superhuman AI for Multiplayer Poker." *Science* 365: 885-890.
→ Pluribus. Self-play for 6-player no-limit Texas hold'em. First superhuman performance in a major multiplayer imperfect-information game.

**Lanctot, M. et al. (2017)** "A Unified Game-Theoretic Approach to Multiagent Reinforcement Learning." *NeurIPS 2017*.
→ Introduces PSRO (Policy Space Response Oracles). Meta-algorithm for multi-agent learning that generalizes fictitious play and double oracle.

## Key Papers — Mean Field Games

**Lasry, J.-M. & Lions, P.-L. (2007)** "Mean Field Games." *Japanese Journal of Mathematics* 2: 229-260.
→ Foundational paper (with Huang, Malhame & Caines 2006). Introduces the mean field game framework for large-population games.

**Huang, M., Malhame, R.P. & Caines, P.E. (2006)** "Large Population Stochastic Dynamic Games: Closed-Loop McKean-Vlasov Systems and the Nash Certainty Equivalence Principle." *Communications in Information and Systems* 6: 221-252.
→ Independent development of mean field games from the control theory perspective.

## Surveys

**Zhang, K., Yang, Z. & Basar, T. (2021)** "Multi-Agent Reinforcement Learning: A Selective Overview of Theories and Algorithms." *Handbook of Reinforcement Learning and Control*, Springer.
→ Comprehensive MARL survey. Covers cooperative, competitive, and mixed settings.
