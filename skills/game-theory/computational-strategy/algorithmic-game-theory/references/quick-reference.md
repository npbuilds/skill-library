# Algorithmic Game Theory — Quick Reference


## When Nash IS Tractable

| Game Class | Complexity | Key Property |
|------------|-----------|--------------|
| **Two-player zero-sum** | Polynomial (linear programming) | Minimax theorem, LP duality |
| **Potential games** | Best-response converges (but may be exponential in worst case) | Exists an exact potential function |
| **Congestion games** | PLS-complete (finding pure NE) | Special structure of payoff functions |
| **Correlated equilibrium** | Polynomial (linear programming) | Weaker concept than Nash |
| **Graphical games (bounded treewidth)** | Polynomial in n (exponential in treewidth) | Sparse interaction structure |
| **Symmetric games** | Polynomial for constant # of strategies | Symmetry reduces dimensionality |
