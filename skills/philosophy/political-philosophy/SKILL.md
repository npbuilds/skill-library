---
name: political-philosophy
description: >
  Direct the political philosophy subdomain — route justice, rights, and governance questions
  to the right specialist. Use when evaluating policy through justice frameworks, analyzing
  competing rights claims, assessing governance structures, or understanding why reasonable
  people disagree about political arrangements.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
allowed-tools: Read Glob
---

# Political Philosophy Director

The department head for justice, rights, and governance within the philosophy domain. Routes questions about collective moral arrangements to the right specialist.

Political philosophy is where ethics meets institutions. Where ethics asks "what's right for individuals?", political philosophy asks "what's right for societies?" — how should power be distributed, what do we owe each other, and what legitimizes authority?

## Child Skills

| Skill | Path | Type | Purpose |
|-------|------|------|---------|
| justice-analyst | `justice-analyst/SKILL.md` | Action | Evaluate a policy or situation through Rawlsian, libertarian, utilitarian, and communitarian lenses simultaneously |
| rights-reasoner | `rights-reasoner/SKILL.md` | Action | Analyze competing rights claims, distinguish negative from positive rights, identify where rights frameworks conflict |

## Routing Logic

| Question Pattern | Route To | Why |
|-----------------|----------|-----|
| "Is this policy fair?", "Is this just?", "Who benefits and who loses?" | justice-analyst | Distributive justice analysis |
| "What does fairness require here?", "Compare these policy options" | justice-analyst | Multi-framework policy evaluation |
| "Do people have a right to X?", "Whose rights take priority?" | rights-reasoner | Rights claim analysis |
| "Does this violate anyone's rights?", "Is this a positive or negative right?" | rights-reasoner | Rights framework application |
| "Is this ethical?" (individual morality, not collective arrangements) | Escalate to orchestrator → Ethics | Personal ethics vs. political philosophy |
| "Design a political system for my fictional world" | Escalate to orchestrator → cross-domain to Worldbuilding | Applied political philosophy for fiction |

### Multi-Skill Sequences

**"Is this policy justified?"**
1. justice-analyst → evaluate through multiple justice frameworks
2. rights-reasoner → check whether any rights are violated
3. Synthesize: a policy can be just by one framework and rights-violating by another — surface the tension

## Conflict Resolution

| Conflict | Resolution | Reason |
|----------|-----------|--------|
| Rawlsian analysis favors redistribution; libertarian analysis opposes it | Present both with the foundational value driving each (equality of opportunity vs. property rights). This is not resolvable by analysis — it's a genuine value disagreement | The frameworks disagree because they prioritize different values |
| Positive rights (right to healthcare) conflict with negative rights (right to not be taxed) | Map the conflict precisely. Show what each framework demands and what must be sacrificed | Rights conflicts are the core problem of political philosophy, not a bug |
| Justice for current generation conflicts with justice for future generations | Present the intergenerational dimension explicitly. Most justice frameworks were designed for contemporaneous agents — flag this limitation | Temporal scope is a known blind spot in traditional frameworks |

## Scope Boundaries

**This director handles**: Justice, rights, governance, collective moral arrangements, policy evaluation, legitimacy of authority, distributive questions.

**Escalate to the orchestrator when**:
- The question is about individual morality, not collective arrangements (Ethics)
- The question is about strategic interaction between political actors (cross-domain to Game Theory / social choice)
- The question is about argument validity, not political justice (Logic)
- The user wants to build a fictional political system (cross-domain to Worldbuilding)

## Cross-Domain Connections

- **Game Theory**: justice-analyst connects to `game-theory/mechanism-design/social-choice` (Arrow's theorem, voting systems, fairness criteria). rights-reasoner connects to `game-theory/strategic-foundations/cooperative-games` (coalition formation, fair division).
- **Worldbuilding**: justice-analyst connects to `worldbuilding/faction-design` (factions embody different justice theories). rights-reasoner connects to `worldbuilding/cultures-societies` (cultures instantiate different rights frameworks).
- **Investing**: justice-analyst connects to `investing/geopolitical-overlay` (policy evaluation through justice lenses).
