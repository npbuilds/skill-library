# Evaluation Methods — Agentic Researcher Reference

Detailed guidance for candidate generation, evaluation, and the evolutionary loop. The main SKILL.md references this for the specifics.

## Candidate Generation Strategies

### Established Options
Survey existing practice. What solutions already exist for this class of problem?
- Search for "[problem] best practices", "[problem] comparison", "[problem] approaches"
- Check if authoritative sources (textbooks, standards bodies, major practitioners) recommend specific approaches
- These form the baseline — every evaluation should include at least one established option

### Analogical Transfer
Find solutions from domains with structural parallels.
- Identify the *abstract structure* of the problem (e.g., "resource allocation under uncertainty" rather than "database selection")
- Search for that abstract structure in other domains
- Adapt the solution to the current domain's constraints
- Example: Sommelier's tasting grid structure → applied as a code review rubric (systematic evaluation with multiple dimensions)

### Constraint Inversion
Ask: "What if the hardest constraint didn't exist?"
- This reveals solutions blocked by assumptions, not by fundamental limits
- Often surfaces creative approaches the user hasn't considered
- Always label these clearly: "This option becomes viable if [constraint] can be relaxed"

### Extreme Positions
Optimize for a single criterion at the expense of everything else.
- These are rarely the recommendation, but they map the Pareto frontier
- They show the user what maximum performance on each dimension looks like
- They help calibrate expectations: "You can get X-level performance on speed, but only by sacrificing Y"

### Hybrid Construction
After the first evaluation round, combine strengths from top candidates.
- Take Candidate A's approach to criterion X + Candidate B's approach to criterion Y
- Only viable after at least one evaluation — you need to know what works before combining
- Watch for integration costs: sometimes combining approaches creates complexity that negates the individual strengths

## Evaluation Matrix Detailed Guide

### Scoring Scales

For **measurable** criteria (latency, cost, token count):
- Use actual numbers with units and source citations
- Normalize to a common scale if comparing across different units

For **comparable** criteria (better/worse relative ranking):
- Use a 1-5 scale: 1 = significantly worse, 3 = adequate, 5 = significantly better
- Anchor the scale: define what 1 and 5 look like for this specific criterion
- Cite evidence for the ranking

For **judgmental** criteria (elegance, maintainability):
- Use the same 1-5 scale but explicitly flag as "judgment-based"
- Provide reasoning (2-3 sentences) for each score
- Note if the judgment depends on assumptions the user should validate

### Weighting Criteria

Default weights when the user doesn't specify:
1. Hard requirements → pass/fail (candidates that fail are eliminated, not scored)
2. Primary preferences → 40% of remaining weight
3. Secondary preferences → 35%
4. Nice-to-haves → 25%

When unsure how to weight: make all soft criteria equal-weight and note this in the sensitivity analysis. Often, the recommendation is robust to moderate weight changes — and if it isn't, that's the most valuable finding.

### Trade-Off Visualization

For 3-4 candidates across 3-5 criteria, use this format:

```
                  Speed   Cost    Simplicity   Scalability
                  ─────   ────    ──────────   ───────────
Candidate A       ████░   ███░░   █████        ██░░░
Candidate B       ██░░░   █████   ███░░        ████░
Candidate C       ███░░   ███░░   ███░░        ███░░
```

The visual pattern reveals trade-offs faster than a number table. Candidate C above is the "balanced but doesn't excel" archetype.

## Evolutionary Loop Details

### Mutation Operators

When mutating a selected candidate:

1. **Weakness repair** — Identify the candidate's lowest-scoring criterion and modify the approach to address it. Ask: "What would need to change about this candidate to score 1 point higher on [weakest criterion]?"

2. **Strength import** — Take the highest-scoring aspect of a different candidate and graft it onto the selected one. Check for compatibility: does the imported element conflict with the selected candidate's core approach?

3. **Constraint tightening** — Add a constraint the user mentioned but hasn't fully enforced. This pressure-tests the candidate under more realistic conditions.

4. **Scale shift** — What happens to this candidate at 10x the intended scale? At 1/10th? Scale sensitivity reveals hidden brittleness or unexpected robustness.

### Convergence Detection

Stop iterating when ANY of these hold:
- The top candidate's aggregate score changed by less than 5% from the previous round
- The ranking of the top 2 candidates hasn't changed for 2 consecutive rounds
- You've exhausted the iteration budget for the depth mode
- A new mutation scored worse than its parent on the criterion it was supposed to improve (the solution space is locally optimal)

### When the Loop Fails

If after maximum iterations no candidate meets all hard requirements:
- Report this explicitly: "No candidate satisfies all constraints"
- Show which constraints are in tension (the impossible triangle)
- Suggest which constraint to relax and what that unlocks
- This is a valuable finding — the user learns their constraints are contradictory
