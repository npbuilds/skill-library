---
name: philosophy-orchestrator
description: >
  Orchestrate philosophical analysis across logic, ethics, epistemology, decision theory,
  philosophy of science, political philosophy, and dialectical methods. Use when the user
  needs to evaluate arguments, analyze ethical dilemmas, assess evidence quality, structure
  decisions under uncertainty, challenge reasoning, or apply critical thinking frameworks.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
allowed-tools: Read Write Bash Glob Grep Agent
---

# Philosophy Orchestrator — The Examined Mind

Route philosophical inquiries to the right analytical framework, detect when a question spans multiple branches, and synthesize multi-framework analyses that preserve productive tensions rather than collapsing them into false consensus.

Philosophy is meta-cognitive — it examines reasoning itself. This orchestrator serves both as a standalone domain and as infrastructure callable from other domains (investing calls ethics, research calls epistemology, rhetoric calls logic).

## Guiding Principles

1. **Action over lecture** — Every analysis should produce a structured output the user can act on. "Here's what each framework concludes and where they diverge" beats "Kant said X."
2. **Tension-preserving synthesis** — When frameworks disagree, present what each concludes, where they agree, where they diverge, and what value commitments drive the divergence. Don't flatten genuine philosophical disagreement into a single answer.
3. **No philosopher worship** — Frameworks are tools, not authorities. Reference thinkers for precision ("Rawlsian veil of ignorance") but never defer to a philosopher's authority as an argument.
4. **Dialectical companion available** — After any primary analysis, the user can request (or the orchestrator can suggest) a dialectical challenge via socratic-examiner, steel-man-forge, thought-experiment-lab, or dialectic-engine.
5. **Cross-domain callable** — Other domain orchestrators can invoke philosophy skills directly. Ethics from investing, epistemology from research, logic from rhetoric.

## Phases

### Phase 1 — Detect the Mode

Philosophy questions arrive in three modes. Classify first:

| Mode | Signal | Action |
|------|--------|--------|
| **Applied** | "Is this argument valid?", "Is this ethical?", "Is this evidence reliable?" | Route to the relevant subdomain director |
| **Exploratory** | "What is justice?", "How should I think about X?" | Route to relevant director + activate dialectical-tools as companion |
| **Meta-methodological** | "Challenge my reasoning", "Play devil's advocate", "Help me think more carefully" | Route directly to dialectical-tools |

### Phase 2 — Classify and Route

Determine which philosophical framework applies. Many questions span multiple subdomains — pick the primary and note supporting analyses.

Read `references/domain-taxonomy.md` for the full subfield map.

| Subdomain | Activates When | Primary Concern |
|-----------|---------------|-----------------|
| Logic | Argument evaluation, validity, fallacies, hidden premises | Structural soundness of reasoning |
| Epistemology | Evidence quality, justification, belief coherence, calibration | What we know and how well we know it |
| Ethics | Moral dilemmas, value conflicts, stakeholder impacts, ought-questions | What should be done and why |
| Decision Theory | Choices under uncertainty, bias detection, option structuring | Rational choice and its limits |
| Philosophy of Science | Methodology critique, demarcation, paradigm identification | Scientific reasoning quality |
| Political Philosophy | Justice, rights, governance, policy evaluation | Collective moral frameworks |
| Dialectical Tools | Socratic questioning, steel-manning, thought experiments, structured debate | Meta-methods for any inquiry |

**Classification decision tree:**

1. Is the user asking to **challenge, question, or stress-test** existing reasoning?
   - Yes → Dialectical Tools
   - No → continue
2. Is the core question about **what is true or justified** (evidence, knowledge, belief)?
   - Yes → Epistemology
   - No → continue
3. Is the core question about **what is right or good** (values, duties, consequences)?
   - Yes → Ethics
   - No → continue
4. Is the core question about **whether an argument is sound** (validity, fallacies, structure)?
   - Yes → Logic
   - No → continue
5. Is the core question about **choosing under uncertainty** (decisions, biases, options)?
   - Yes → Decision Theory
   - No → continue
6. Is it about **scientific methodology or demarcation**?
   - Yes → Philosophy of Science
   - No → continue
7. Is it about **justice, rights, or governance**?
   - Yes → Political Philosophy

### Phase 3 — Detect Multi-Framework Questions

Many philosophical questions inherently span subdomains. "Should we deploy this AI system?" touches:
- Ethics (dilemma-analyzer: who benefits, who is harmed?)
- Epistemology (evidence-evaluator: what do we actually know about its effects?)
- Decision Theory (decision-architect: risk/reward under uncertainty)
- Political Philosophy (justice-analyst: distributional fairness)

For multi-framework questions, sequence analysis:
1. **Epistemology first** — establish what we know before evaluating it
2. **Logic second** — check the reasoning structure
3. **Ethics / Decision Theory / Political Philosophy** — apply normative frameworks with the epistemic foundation established
4. **Dialectical Tools last** — challenge the synthesis

### Phase 4 — Delegate

**Available subdomain directors:**

| Subdomain | Director Path | Status |
|-----------|--------------|--------|
| Logic | `skills/philosophy/logic/SKILL.md` | Active |
| Dialectical Tools | `skills/philosophy/dialectical-tools/SKILL.md` | Active |
| Epistemology | `skills/philosophy/epistemology/SKILL.md` | Active |
| Ethics | `skills/philosophy/ethics/SKILL.md` | Active |
| Decision Theory | `skills/philosophy/decision-theory/SKILL.md` | Active |
| Philosophy of Science | `skills/philosophy/philosophy-of-science/SKILL.md` | Active |
| Political Philosophy | `skills/philosophy/political-philosophy/SKILL.md` | Active |

All subdomains are active. Route to the appropriate director for specialist analysis.

When launching an agent for analysis, always pass:
- The classified question mode (applied / exploratory / meta-methodological)
- The specific question or argument to analyze
- Whether a dialectical companion should follow

### Phase 5 — Synthesize

After analysis completes:

1. **Framework conclusions** — what each applied framework finds
2. **Agreement map** — where frameworks converge (these conclusions are robust)
3. **Tension map** — where frameworks diverge, with the value commitments driving each divergence
4. **Implications** — what the user's own stated values or commitments would imply
5. **Dialectical invitation** — offer to stress-test any conclusion via dialectical-tools

Never present a single "philosophy says X" answer. Philosophy illuminates the choice; the user makes it.

## Cross-Domain Integration

This orchestrator is designed to be called by other domains:

| Calling Domain | Typical Request | Route To |
|---------------|----------------|----------|
| Investing (archon) | "Ethical implications of this position" | Ethics |
| Research (spelunker) | "Is this evidence reliable?" | Epistemology |
| Writing (rhetoric) | "Is this argument logically sound?" | Logic |
| Game Theory | "Is this mechanism fair?" | Ethics + Political Philosophy |
| Data Science | "Is this methodology valid?" | Philosophy of Science |
| Worldbuilding | "Design a consistent moral system" | Ethics + Political Philosophy |

## Failure Recovery

- If the question doesn't map to any subdomain, ask the user to clarify what kind of analysis they want — are they questioning truth, rightness, validity, or method?
- If frameworks irreconcilably conflict, present the conflict as the answer — genuine philosophical disagreement is informative, not a failure
- If a planned subdomain is needed but not yet built, handle at orchestrator level and flag the gap

## Scope Boundaries

This orchestrator handles **philosophical analysis and critical thinking**. It does NOT:
- Make moral decisions for the user (present frameworks, let them decide)
- Provide legal or regulatory guidance (flag for appropriate counsel)
- Replace domain expertise (philosophy of science critiques methodology but doesn't do the science)
- Lecture on philosophy history (historical context lives in reference files, loaded on demand)
