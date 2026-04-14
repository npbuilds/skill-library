---
name: game-theory-orchestrator
description: >
  Orchestrate game-theoretic analysis across strategic problems. Use when the user needs to
  analyze strategic interactions, find equilibria, design mechanisms or incentives, model
  evolutionary dynamics, evaluate information structures, or apply formal game theory to
  real-world scenarios in business, technology, politics, biology, or fiction.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
allowed-tools: Read Write bash Glob Grep Agent
---

# Game Theory Orchestrator — The Strategist

Formalize strategic problems, route them to the right analytical framework, and synthesize actionable insights. The core capability is **bridging informal situations to formal game structures** — taking "my competitor is undercutting me" and producing a rigorous Bertrand competition analysis with equilibrium predictions.

## Phases

### Phase 1 — Understand the Strategic Situation

Before any analysis, gather the essential elements of the strategic interaction:

- **Players** — Who are the decision-makers? (individuals, firms, governments, algorithms, biological populations)
- **Actions/Strategies** — What can each player do? Are strategy sets finite or continuous?
- **Timing** — Do players move simultaneously or sequentially? Is there repetition?
- **Information** — What does each player know? Is there private information? Can players observe past moves?
- **Payoffs** — What are players optimizing? (profit, utility, fitness, votes, welfare)
- **Commitments** — Can players make binding agreements? Are there enforceable contracts?

If the user describes a situation informally ("how should I price against a competitor?"), extract these elements through targeted questions. If the user presents a formal game, validate the specification.

### Phase 2 — Classify and Route

Determine which game-theoretic framework applies. A problem may span multiple subdomains — pick the primary and note supporting analyses.

Read `references/domain-taxonomy.md` for the full subfield map.

**Subdomain routing summary:**

| Subdomain | Activates When | Primary Concern |
|-----------|---------------|-----------------|
| Strategic Foundations | Standard games with known players, strategies, payoffs | Equilibrium analysis, strategic prediction |
| Mechanism Design | Designing rules, auctions, markets, or incentive systems | Incentive compatibility, efficiency, revenue |
| Evolutionary Dynamics | Large populations, adaptation, no central designer | Stability, invasion, long-run dynamics |
| Information Economics | Strategic communication, persuasion, signaling | Information revelation, belief manipulation |
| Computational Strategy | Algorithmic constraints, AI agents, behavioral limits | Computational tractability, bounded rationality |

**Classification decision tree:**

1. Is the question about **analyzing** an existing game, or **designing** rules/mechanisms?
   - Designing → Mechanism Design
   - Analyzing → continue
2. Are players **rational agents** making deliberate choices, or a **population** evolving over time?
   - Population/evolutionary → Evolutionary Dynamics
   - Rational agents → continue
3. Is the central issue **what players know** or **how information flows**?
   - Information is the core issue → Information Economics
   - Information is a feature but not the focus → continue
4. Are there **computational constraints** or **behavioral biases** that matter?
   - Yes → Computational Strategy
   - No → Strategic Foundations

### Phase 3 — Formalize

Before delegating, establish the analytical frame:

1. **Game representation** — choose the appropriate form:
   - Normal (strategic) form — for simultaneous-move games with finite strategies
   - Extensive form — for sequential games, games with information sets
   - Characteristic function form — for cooperative/coalitional games
   - Population game form — for evolutionary settings

2. **Solution concept** — select based on the game structure:
   - Complete info, simultaneous → Nash Equilibrium
   - Complete info, sequential → Subgame Perfect Equilibrium
   - Incomplete info → Bayesian Nash Equilibrium / Perfect Bayesian Equilibrium
   - Cooperative setting → Core, Shapley Value, or bargaining solution
   - Evolutionary setting → ESS, replicator dynamics
   - Repeated game → Folk theorem analysis

3. **Key assumptions** — document what we're assuming and what would change the analysis:
   - Rationality level (full, bounded, evolutionary)
   - Common knowledge assumptions
   - Commitment power
   - Discount factors for repeated games

4. **Analysis parameters** — what the user actually needs:
   - Equilibrium prediction ("what will happen?")
   - Strategic recommendation ("what should I do?")
   - Mechanism design ("what rules should I set?")
   - Robustness check ("what if assumptions change?")

### Phase 4 — Delegate

Route to the appropriate subdomain director, passing the formalization from Phase 3. Read `references/delegation-rules.md` for detailed routing logic, multi-subdomain sequencing, and escalation rules.

**Available subdomain directors:**

| Subdomain | Director Path | Status |
|-----------|--------------|--------|
| Strategic Foundations | `skills/game-theory/strategic-foundations/SKILL.md` | Active |
| Mechanism Design | `skills/game-theory/mechanism-design/SKILL.md` | Active |
| Evolutionary Dynamics | `skills/game-theory/evolutionary-dynamics/SKILL.md` | Active |
| Information Economics | `skills/game-theory/information-economics/SKILL.md` | Active |
| Computational Strategy | `skills/game-theory/computational-strategy/SKILL.md` | Active |

For stub subdomains, handle the analysis directly using the orchestrator's knowledge and note which specialist would improve the analysis once built.

When launching an agent for analysis, always pass:
- The formalized game specification from Phase 3
- The specific question the user needs answered
- Relevant constraints or assumptions

For multi-subdomain problems, analyze sequentially — each analysis receives prior results to maintain coherence.

### Phase 5 — Synthesize and Present

After analysis completes:

1. **Plain-language interpretation** — translate equilibrium results into actionable strategic insight. "The Nash equilibrium predicts both firms will price at marginal cost" becomes "in a price war with identical products, neither firm can sustainably charge above cost — you need to differentiate."

2. **Sensitivity analysis** — identify which assumptions matter most. What changes the equilibrium? What's robust?

3. **Strategic recommendations** — if the user asked "what should I do?", provide ranked options with game-theoretic justification.

4. **Limitations** — flag where the model simplifies reality. All games are models — be explicit about what's left out.

5. **Cross-domain connections** — note when the analysis connects to other domains:
   - Worldbuilding: faction dynamics, political systems, economic structures
   - Design: choice architecture, nudge theory, UX as mechanism design
   - General: negotiation, competition, cooperation in any context

## Knowledge Layer

Route through the subdomain director first. The director handles routing to specific knowledge skills, curriculum order, and conflict resolution.

**Always route through the director:**

| Subdomain | Director | Consult When |
|-----------|----------|-------------|
| Strategic Foundations | `skills/game-theory/strategic-foundations/SKILL.md` | Equilibrium analysis, game classification, strategic prediction, bargaining, coalitions |
| Mechanism Design | `skills/game-theory/mechanism-design/SKILL.md` | Auction design, market rules, voting systems, incentive structures, matching |
| Evolutionary Dynamics | `skills/game-theory/evolutionary-dynamics/SKILL.md` | Population dynamics, evolutionary stability, adaptation, biological games |
| Information Economics | `skills/game-theory/information-economics/SKILL.md` | Signaling, screening, persuasion, information disclosure, belief updating |
| Computational Strategy | `skills/game-theory/computational-strategy/SKILL.md` | Algorithmic games, bounded rationality, AI/ML game theory, computational complexity |

**Direct knowledge skill paths** (prefer routing through the director):

| Knowledge Skill | Path |
|----------------|------|
| Classical Games | `skills/game-theory/strategic-foundations/classical-games/SKILL.md` |
| Cooperative Games | `skills/game-theory/strategic-foundations/cooperative-games/SKILL.md` |

## Failure Recovery

- If the user's situation doesn't cleanly map to a game, ask for clarification on players, strategies, and payoffs rather than forcing a fit
- If multiple equilibria exist (common), present all with intuitive selection criteria rather than picking one arbitrarily
- If a subdomain is still a stub, provide the best analysis possible from the orchestrator level and note what specialist depth would add
- If the user rejects an analysis, ask which assumption feels wrong rather than re-running the same model

## Scope Boundaries

This orchestrator handles **strategic analysis and game-theoretic reasoning**. It does NOT:
- Execute actual negotiations or transactions on behalf of the user
- Provide legal advice on contracts or agreements (flag for legal counsel)
- Make ethical judgments about strategic behavior (present the analysis, let the user decide)
- Simulate games computationally (delegate to action skills like game-solver or evo-simulator)
