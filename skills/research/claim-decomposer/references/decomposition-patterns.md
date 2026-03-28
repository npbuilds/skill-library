# Decomposition Patterns — Common Question Structures

A catalog of recurring structures in complex questions, with examples showing how to split them into atomic claims.

## Pattern 1: Compound Conjunction

**Signal:** "and", "as well as", "both", "also", "plus"

**Example:**
> "Is intermittent fasting effective for weight loss and does it improve longevity?"

**Decomposition:**
1. Intermittent fasting leads to weight loss in clinical studies (Causal)
2. Intermittent fasting improves longevity markers in humans (Causal)
3. Intermittent fasting improves longevity in animal models (Causal)

**Why split:** Effectiveness for weight loss has strong RCT evidence. Longevity in humans is far less studied. Conflating them produces a misleading overall confidence.

## Pattern 2: Causal Chain

**Signal:** "because", "leads to", "causes", "results in", "therefore"

**Example:**
> "Does social media cause depression in teenagers?"

**Decomposition:**
1. Teenagers use social media at significant levels (Factual — establish baseline)
2. Heavy social media use correlates with higher depression rates in teens (Factual — correlation data)
3. The correlation is causal, not merely associative (Causal — requires experimental/quasi-experimental evidence)
4. The causal mechanism has been identified (Causal — mechanism explanation)

**Why split:** Correlation evidence is abundant (Claim 2 likely Confirmed). Causal evidence is contested (Claim 3 likely Contested). Confusing correlation for causation is the most common error.

## Pattern 3: Hidden Comparative

**Signal:** "best", "better", "most effective", "superior", "should I use X"

**Example:**
> "Is React the best framework for building web applications?"

**Decomposition:**
1. React is a widely-used framework for web applications (Factual)
2. React performs well on [specific metrics: performance, developer experience, ecosystem] (Comparative — needs criteria)
3. Alternative frameworks (Vue, Angular, Svelte) have comparable or different strengths (Comparative)
4. "Best" depends on the specific use case and priorities (Definitional — what does "best" mean here?)

**Hidden assumption surfaced:** "Best" is undefined. The question cannot be answered without criteria.

## Pattern 4: Scope Ambiguity

**Signal:** Broad terms without qualifiers — "safe", "effective", "good", "works"

**Example:**
> "Is creatine safe?"

**Decomposition:**
1. Creatine monohydrate is safe for healthy adults at recommended doses (5g/day) (Factual)
2. Creatine is safe for long-term use (1+ years) (Factual — different evidence base)
3. Creatine is safe for adolescents (Factual — different population, less studied)
4. Creatine is safe for people with kidney conditions (Factual — specific contraindication question)
5. Creatine has no significant side effects at standard doses (Factual)

**Hidden assumptions surfaced:**
- A1. "Safe" means "no significant health risks" (Definitional — common ground)
- A2. We're discussing creatine monohydrate specifically (Definitional — needs confirmation)
- A3. Standard supplementation doses, not megadoses (Scope — needs confirmation)

## Pattern 5: Existence Presupposition

**Signal:** "Why does X...", "How does X work...", "When did X..."

**Example:**
> "Why does the Mediterranean diet prevent heart disease?"

**Decomposition:**
1. The Mediterranean diet is associated with lower heart disease rates (Factual — the presupposition)
2. The association is causal (Causal — stronger claim than correlation)
3. Specific components of the diet drive the effect (olive oil, fish, vegetables, etc.) (Causal — mechanism)
4. The effect holds across different populations and contexts (Factual — generalizability)

**Hidden assumption surfaced:** The question presupposes that the Mediterranean diet DOES prevent heart disease. Claim 1 must be verified first — if it fails, the original question is based on a false premise.

## Pattern 6: Temporal Conflation

**Signal:** Questions about things that may have changed over time, or "still"

**Example:**
> "Is nuclear energy safe?"

**Decomposition:**
1. Historical nuclear accidents (Chernobyl, Fukushima) caused significant harm (Factual — historical)
2. Modern reactor designs have substantially different safety profiles than historical ones (Comparative — temporal)
3. The rate of serious incidents per unit of energy produced compares favorably/unfavorably to other energy sources (Comparative — normalized)
4. Nuclear waste storage presents long-term safety challenges (Factual — ongoing)
5. Regulatory frameworks are adequate to maintain safety (Evaluative — judgment-dependent)

**Why split:** "Nuclear energy" in 1986 and 2025 are fundamentally different technologies. Temporal conflation is one of the most common reasoning errors.

## Pattern 7: Multi-Stakeholder

**Signal:** Questions where the answer depends on perspective

**Example:**
> "Is remote work better than office work?"

**Decomposition:**
1. Remote work affects individual productivity (Comparative — by role type, industry)
2. Remote work affects team collaboration and communication (Comparative)
3. Remote work affects employee wellbeing and satisfaction (Comparative)
4. Remote work affects employer costs (Comparative)
5. Remote work affects career advancement opportunities (Comparative)
6. "Better" depends on which stakeholder's interests are prioritized (Definitional)

**Hidden assumption surfaced:** "Better" for whom? Employee, employer, team, society? Each may give a different answer.

## Meta-Rule: When to Stop Splitting

A claim is atomic when:
- It can be answered with a single type of evidence (one search strategy)
- Splitting it further would create trivial or definitional fragments
- It has a clear truth value (even if we don't yet know what it is)
- A person could reasonably agree or disagree with it as stated

Stop splitting when further decomposition adds precision without adding clarity.
