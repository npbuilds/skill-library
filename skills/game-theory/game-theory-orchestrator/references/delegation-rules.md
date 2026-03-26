# Delegation Rules — Subdomain Routing Logic

## Single-Subdomain Routing

When the problem clearly maps to one framework, route directly to that subdomain's director.

**Signal → Subdomain mapping:**

| User Signal | Route To | Why |
|-------------|----------|-----|
| "Nash equilibrium", "best response", "dominant strategy", "payoff matrix" | Strategic Foundations | Classical non-cooperative analysis |
| "coalition", "fair division", "Shapley value", "bargaining", "negotiate" | Strategic Foundations (cooperative) | Cooperative game theory |
| "repeated game", "reputation", "punishment strategy", "long-run" | Strategic Foundations (repeated/dynamic) | Temporal strategic interaction |
| "auction", "bidding", "reserve price", "revenue maximization" | Mechanism Design | Auction theory |
| "matching", "allocation", "school choice", "kidney exchange", "assignment" | Mechanism Design | Market/matching design |
| "voting", "election", "Arrow's theorem", "manipulation", "social welfare" | Mechanism Design | Social choice theory |
| "incentive compatible", "truthful", "mechanism", "rules design" | Mechanism Design | Mechanism design proper |
| "evolution", "fitness", "ESS", "replicator", "mutation", "invasion" | Evolutionary Dynamics | Evolutionary game theory |
| "population", "species", "adaptation", "natural selection" | Evolutionary Dynamics | Population dynamics |
| "signal", "screening", "adverse selection", "moral hazard", "hidden info" | Information Economics | Information asymmetry |
| "persuasion", "disclosure", "cheap talk", "Bayesian", "belief" | Information Economics | Information design |
| "price of anarchy", "computational complexity", "algorithm", "PPAD" | Computational Strategy | Algorithmic game theory |
| "bounded rationality", "level-k", "behavioral", "cognitive bias" | Computational Strategy | Behavioral game theory |
| "multi-agent", "self-play", "MARL", "adversarial", "AI alignment" | Computational Strategy | AI/ML game theory |

## Multi-Subdomain Routing

Many real-world problems span subdomains. Analyze in dependency order:

### Typical sequences:

**Market entry problem:** Strategic Foundations → Mechanism Design
- Analyze the competitive game first → then design optimal entry/pricing mechanisms

**Platform design:** Mechanism Design → Information Economics → Computational Strategy
- Design the rules → analyze information flows → check computational feasibility

**Biological competition:** Evolutionary Dynamics → Strategic Foundations
- Model population dynamics → check if equilibria align with ESS predictions

**Negotiation with private information:** Information Economics → Strategic Foundations
- Analyze information structure → find equilibrium of the resulting Bayesian game

**AI system design:** Computational Strategy → Mechanism Design → Strategic Foundations
- Assess computational constraints → design incentive-compatible mechanisms → verify equilibrium properties

**DAO/crypto governance:** Mechanism Design → Computational Strategy → Strategic Foundations
- Design voting/allocation rules → check for manipulation/Sybil resistance → analyze resulting game

## When NOT to Delegate

Handle directly in the orchestrator when:
- The user needs a quick classification ("is this a prisoner's dilemma?") — just answer
- The situation needs formalization before any subdomain applies — do Phase 3 first
- The user is exploring and needs a conversation about which framework fits — discuss, don't delegate
- The problem is simple enough that the orchestrator's knowledge suffices (2-player, 2-strategy, complete info)

## Context Threading

When routing to sequential subdomains, pass a **Strategic Context Block**:

```
STRATEGIC CONTEXT
─────────────────
Problem: [1-2 sentence situation summary]
Players: [who is involved]
Key tension: [what makes this strategic — conflicting interests, information asymmetry, etc.]
Game type: [classification from Phase 2]
Formalization: [game representation from Phase 3]
Prior analysis: [summary of what earlier subdomain established]
User's question: [what they actually want to know]
```

## Escalation Within Subdomains

If a subdomain director encounters a question outside its scope:
- Strategic Foundations → escalates mechanism design, evolutionary, information, or computational questions
- Mechanism Design → escalates pure equilibrium analysis (no design element) back to Strategic Foundations
- Evolutionary Dynamics → escalates individual rational-agent questions to Strategic Foundations
- Information Economics → escalates mechanism design questions where information is a tool, not the object
- Computational Strategy → escalates questions where computational limits don't bind
