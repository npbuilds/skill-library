# Sources — Algorithmic Game Theory

## Primary Texts

**Nisan, N., Roughgarden, T., Tardos, E. & Vazirani, V.V. (eds.) *Algorithmic Game Theory* (Cambridge, 2007)**
The definitive reference. 29 chapters covering computational complexity of equilibria, mechanism design, cost-sharing, online mechanisms, network games, and more.
→ Used for: all major topics in the field.

**Roughgarden, T. *Twenty Lectures on Algorithmic Game Theory* (Cambridge, 2016)**
Accessible lecture-based treatment. Covers mechanism design, PoA, smoothness, sponsored search, and learning in games. Excellent for building intuition.
→ Used for: smoothness framework, selfish routing, algorithmic mechanism design.

**Shoham, Y. & Leyton-Brown, K. *Multiagent Systems* (Cambridge, 2009)**
Covers game theory from a computational perspective. Game representations, computing equilibria, mechanism design, and learning. Integrated CS-economics perspective.
→ Used for: computational representations, graphical games, algorithm descriptions.

## Key Papers — Complexity

**Daskalakis, C., Goldberg, P.W. & Papadimitriou, C.H. (2009)** "The Complexity of Computing a Nash Equilibrium." *SIAM Journal on Computing* 39: 195-259.
→ PPAD-completeness of Nash equilibrium for 3-player games. Extended by Chen, Deng & Teng to 2-player games.

**Chen, X., Deng, X. & Teng, S.-H. (2009)** "Settling the Complexity of Computing Two-Player Nash Equilibria." *Journal of the ACM* 56: Article 14.
→ PPAD-completeness for 2-player games. Completed the complexity picture: even 2-player Nash is hard.

**Papadimitriou, C.H. (1994)** "On the Complexity of the Parity Argument and Other Inefficient Proofs of Existence." *Journal of Computer and System Sciences* 48: 498-532.
→ Defines the PPAD complexity class. The foundational paper for the entire PPAD-completeness program.

## Key Papers — Efficiency

**Koutsoupias, E. & Papadimitriou, C.H. (1999)** "Worst-Case Equilibria." *STACS 1999*.
→ Introduces the Price of Anarchy concept. Analyzes load balancing games.

**Roughgarden, T. & Tardos, E. (2002)** "How Bad Is Selfish Routing?" *Journal of the ACM* 49: 236-259.
→ Price of anarchy for selfish routing with linear latency functions is exactly 4/3. Braess's paradox analysis.

**Roughgarden, T. (2015)** "Intrinsic Robustness of the Price of Anarchy." *Journal of the ACM* 62: Article 32.
→ The smoothness framework. Unifies PoA bounds across equilibrium concepts (pure, mixed, correlated, coarse correlated, no-regret).

## Key Papers — Structure

**Rosenthal, R.W. (1973)** "A Class of Games Possessing Pure-Strategy Nash Equilibria." *International Journal of Game Theory* 2: 65-67.
→ Congestion games and the potential function argument. Pure NE existence.

**Monderer, D. & Shapley, L.S. (1996)** "Potential Games." *Games and Economic Behavior* 14: 124-143.
→ General theory of potential games. Equivalence between congestion games and potential games.

**Aumann, R.J. (1974)** "Subjectivity and Correlation in Randomized Strategies." *Journal of Mathematical Economics* 1: 67-96.
→ Introduces correlated equilibrium. Later shown to be computable in polynomial time.

## Nobel Prize Context

**2012 Nobel in Economics**: Alvin Roth and Lloyd Shapley — includes Shapley's contributions to game theory that underpin potential games and cooperative game theory.
