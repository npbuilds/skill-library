---
name: info-designer
description: >
  Design optimal information disclosure policies for strategic settings. Use when the user needs
  to determine what information to reveal, to whom, and when — for platforms, regulators,
  organizations, or any sender who controls information flow. Produces concrete signal structures
  with commitment and incentive analysis.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
allowed-tools: Read Write Glob
---

# Info Designer — The Revealer

Take an information design problem — "what should we show users?", "how much should the regulator disclose?", "what rating system maximizes trust?" — and produce a concrete information policy with optimal properties. This skill applies Bayesian persuasion, cheap talk, and disclosure theory to practical design questions.

## How to Run

### Input

The user provides:
1. **The information setting** — who is the sender, receiver, what state is uncertain
2. **Commitment power** — can the sender commit to a disclosure policy, or is communication cheap talk?
3. **Objective** — what does the sender want the receiver to do?
4. **Constraints** — verifiability, privacy, legal requirements, computational limits

### Steps

#### Step 1 — Classify the Information Problem

| Dimension | Options | Framework |
|-----------|---------|-----------|
| **Commitment** | Sender commits ex ante / No commitment | Bayesian persuasion / Cheap talk |
| **Verifiability** | Messages verifiable / Not verifiable | Disclosure / Cheap talk or persuasion |
| **Receivers** | Single / Multiple (non-interacting) / Multiple (interacting) | Standard BP / Multi-receiver BP / Information design in games |
| **Timing** | One-shot / Dynamic (sequential revelation) | Static / Dynamic persuasion |
| **Sender's information** | Sender knows the state / Sender designs experiment | Disclosure / Experiment design |

#### Step 2 — Model the Decision Problem

Formalize:
- **State space** Ω = {ω₁, ω₂, ...} with prior μ₀
- **Receiver's action space** A = {a₁, a₂, ...}
- **Receiver's utility** uR(a, ω) — the receiver best-responds to beliefs
- **Sender's utility** uS(a, ω) — depends on the receiver's action

Identify the **receiver's optimal action** for each possible posterior belief μ. This gives the receiver's best-response function a*(μ).

#### Step 3 — Compute the Sender's Value Function

V(μ) = uS(a*(μ), ω) evaluated at belief μ

Plot V(μ) over the belief simplex. The shape of V determines the optimal signal:
- **V is concave**: Full disclosure is optimal (or any signal — concavification doesn't help)
- **V is convex somewhere**: Strategic information withholding improves the sender's payoff
- **V has flat regions**: Pooling (partial information) is optimal over those regions

#### Step 4 — Design the Optimal Signal

**For binary states** (Ω = {0, 1}):
Concavify V on [0,1]. The optimal signal induces posteriors at the points where the concave closure touches V.

**For multiple states**:
The concavification is over the belief simplex. Optimal posteriors lie on the extreme points of the concave closure. Linear programming or geometric methods apply.

**For cheap talk** (no commitment):
Solve for partition equilibria. Find the most informative equilibrium (maximum number of intervals). The partition boundaries satisfy Crawford-Sobel conditions.

#### Step 5 — Specify the Information Policy

```
INFORMATION POLICY SPECIFICATION
─────────────────────────────────
Name: [descriptive name]
Setting: [sender, receiver, state, actions]

Commitment: [Full / Partial / None]

Signal Structure:
  - Signals: [list of possible signal realizations]
  - For each state ω:
    - P(signal | ω) = [probability distribution over signals]

Induced Posteriors:
  - Signal s₁ → posterior μ₁ → receiver action a₁
  - Signal s₂ → posterior μ₂ → receiver action a₂
  [...]

Sender's Expected Payoff: [value]
  vs. Full Disclosure: [comparison]
  vs. No Disclosure: [comparison]

Incentive Properties:
  - Receiver optimality: [receiver best-responds at each posterior]
  - Sender's commitment: [is the sender's commitment credible?]
  - Robustness: [how sensitive to model assumptions?]
```

#### Step 6 — Practical Deployment

Address implementation concerns:
- **Commitment credibility**: How does the sender credibly commit? (Legal requirements, algorithmic transparency, reputation)
- **Receiver sophistication**: Will receivers correctly update beliefs? If not, adjust for bounded rationality
- **Multiple receivers**: Does information leak between receivers? Does this change the optimal signal?
- **Dynamic considerations**: Does revealing information now affect future interactions?
- **Ethical considerations**: Is the information policy manipulative? Does it respect receiver autonomy?

### Output

```
## Information Design: [Problem Name]

### Problem
[Sender, receiver, state uncertainty, objectives]

### Framework
[Bayesian persuasion / Cheap talk / Disclosure — with justification]

### Optimal Information Policy
[Full signal specification]

### Payoff Analysis
[Sender payoff under optimal policy vs. full/no disclosure benchmarks]

### Implementation
[How to deploy: commitment mechanism, receiver interface, dynamic considerations]

### Robustness
[Sensitivity to assumptions: prior, receiver rationality, commitment]
```

## Error Handling

**Commitment is ambiguous**: Ask the user. The commitment assumption is the master switch between frameworks. "Can you lock in your information policy before seeing the data?" If yes → persuasion. If no → cheap talk or signaling.

**Receiver's decision is unclear**: The entire framework depends on knowing how the receiver will act at each belief. If the receiver's problem is complex, simplify (binary action, threshold rule) or model the receiver's problem first.

**Multiple equilibria in cheap talk**: Present the most informative equilibrium as the focal one, but note that less informative equilibria (including babbling) also exist. In practice, which equilibrium prevails depends on the communication context.

**Ethical concerns**: If the optimal signal is manipulative (e.g., the prosecutor example — designed to convict innocents), note this explicitly. Information design is a powerful tool; its ethical status depends on the objective and context.
