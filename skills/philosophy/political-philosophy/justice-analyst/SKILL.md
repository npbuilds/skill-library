---
name: justice-analyst
description: >
  Evaluate a policy, situation, or institutional arrangement through multiple justice
  frameworks simultaneously — Rawlsian, libertarian, utilitarian, communitarian, and
  capabilities. Use when the user needs to assess whether something is fair, compare policy
  options on justice grounds, or understand why different political perspectives reach
  different conclusions about the same situation.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
allowed-tools: Read Write
---

# Justice Analyst — The Magistrate

Convene the major justice frameworks, let each render its verdict on a policy or situation, and map where they converge and diverge. The magistrate does not pick a winner — justice is contested precisely because reasonable people weigh different values differently.

Read `references/justice-frameworks.md` for detailed framework descriptions.

## Input

From the political-philosophy director or directly:
- The policy, situation, or institutional arrangement to evaluate
- Context: who is affected? What are the existing arrangements?
- Scope: **quick** (top 3 frameworks) or **comprehensive** (all major frameworks)

## Process

### Step 1 — Frame the Justice Question

Identify precisely what's at stake:
- **What's being distributed?** (Resources, opportunities, rights, burdens, risks, recognition)
- **Among whom?** (Citizens, workers, nations, generations, species)
- **By what mechanism?** (Market, government, community, lottery, merit)
- **Compared to what baseline?** (Status quo, equality, historical entitlement, need)

### Step 2 — Apply Justice Frameworks

#### Rawlsian Justice (Justice as Fairness)
*Core test: Would this be chosen behind the veil of ignorance?*

- **Difference principle**: Inequalities are permitted only if they benefit the least-advantaged members of society
- **Equal basic liberties**: Everyone gets the same fundamental freedoms
- **Fair equality of opportunity**: Positions open to all under conditions of fair equal opportunity
- Evaluate: does the policy satisfy all three principles in lexical order (liberties first, then opportunity, then difference)?

#### Libertarian Justice (Nozick / Hayek)
*Core test: Does this respect individual rights and voluntary exchange?*

- **Self-ownership**: People own themselves and the fruits of their labor
- **Just acquisition**: Property acquired legitimately is justly held
- **Just transfer**: Voluntary exchange preserves justice
- **Rectification**: Past injustices in acquisition or transfer may justify correction
- Evaluate: does the policy respect property rights and voluntary choice, or does it coerce?

#### Utilitarian Justice (Bentham / Mill / Singer)
*Core test: Does this maximize aggregate well-being?*

- **Sum total**: Which arrangement produces the greatest total welfare?
- **Distribution-sensitive**: Does the distribution matter, or just the total? (Average vs. total utilitarianism)
- **Scope**: Whose welfare counts? (All sentient beings? Citizens only? Future generations?)
- Evaluate: does the policy increase total welfare, and at what distributional cost?

#### Communitarian Justice (Sandel / Walzer / MacIntyre)
*Core test: Does this respect community values and shared meanings?*

- **Social goods**: Different goods (healthcare, education, honor, money) belong to different distributive spheres
- **Shared understandings**: Justice depends on what a community understands its goods to mean
- **Constitutive community**: Identity is partially constituted by community membership
- Evaluate: does the policy respect the social meanings of the goods being distributed?

#### Capabilities Approach (Sen / Nussbaum)
*Core test: Does this expand real freedoms people have reason to value?*

- **Central capabilities**: Life, health, bodily integrity, imagination, emotion, practical reason, affiliation, other species, play, control over environment
- **Threshold**: Justice requires everyone above a minimum threshold for each capability
- **Agency**: People should choose how to use their capabilities, not be told
- Evaluate: does the policy expand or contract real human capabilities?

### Step 3 — Map Convergence and Divergence

| Framework | Verdict | Key Reason |
|-----------|---------|------------|
| Rawlsian | [supports/opposes/mixed] | [because...] |
| Libertarian | [supports/opposes/mixed] | [because...] |
| Utilitarian | [supports/opposes/mixed] | [because...] |
| Communitarian | [supports/opposes/mixed] | [because...] |
| Capabilities | [supports/opposes/mixed] | [because...] |

Identify:
- **Robust conclusions**: Where 4+ frameworks agree — these are strong justice claims
- **Contested conclusions**: Where frameworks split — these reveal genuine value conflicts
- **The driving tension**: What underlying value disagreement explains the split?

### Step 4 — Identify the Justice Crux

What is the single most important question whose answer determines whether this is just? Often:
- "Does fairness require equal outcomes or equal opportunity?"
- "Whose interests take priority when they conflict?"
- "Does the process matter, or only the result?"
- "What's the relevant community whose values should apply?"

## Output

```
JUSTICE ANALYSIS
────────────────
Subject: [policy/situation/arrangement]
Distribution at stake: [what's being distributed, among whom, by what mechanism]

Framework Verdicts:
  Rawlsian:       [verdict] — [key reason]
  Libertarian:    [verdict] — [key reason]
  Utilitarian:    [verdict] — [key reason]
  Communitarian:  [verdict] — [key reason]
  Capabilities:   [verdict] — [key reason]

Convergence: [where frameworks agree]
Divergence: [where they split and why]

Justice Crux: [the core value question]

If you prioritize [equality]: [what follows]
If you prioritize [liberty]: [what follows]
If you prioritize [welfare]: [what follows]
If you prioritize [community]: [what follows]
If you prioritize [capability]: [what follows]
```

## Error Handling

**Policy is clearly unjust by all frameworks:** Report the consensus. Not every question is genuinely contested — some policies are unjust from every perspective.

**User wants a single answer:** Explain the framework structure, then offer to help them identify their own justice priorities (route to ethics/values-excavator), which resolves the question for their specific value commitments.

**Policy involves non-human entities:** The capabilities approach extends most naturally to non-human animals (via Nussbaum's extension). Utilitarian frameworks also include non-human welfare. Note which frameworks can and cannot handle the expanded scope.
