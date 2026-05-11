# Grader Axes — Calibrated 1-5 Rubrics

The full six-axis rubric. Each axis has five score levels with concrete example statements at each level. Score 3 is the action-ready threshold; below 3 triggers the re-state loop.

When in doubt between two adjacent scores, default to the lower. Strict scoring saves loop iterations downstream.

---

## Axis 1 — Specificity

**Question:** Is the statement precise enough to act on?

**Failure signal:** Vague verbs (improve, optimize, enhance), fuzzy nouns (engagement, performance, things), undefined terms.

| Score | Description | Example |
|---|---|---|
| **5** | Every term is operationally defined; no ambiguity for a downstream solver | "Reduce p95 API latency on the /v2/orders endpoint from 850ms to <300ms by Q3, measured against the existing benchmark suite." |
| **4** | Concrete with one or two terms that imply rather than define | "Reduce checkout latency by half this quarter, measured at p95." |
| **3** | Action-ready but with notable ambiguity; a solver could proceed but might solve a slightly different problem | "Make the checkout flow faster." |
| **2** | Vague enough that two competent solvers would interpret it differently | "Improve checkout performance." |
| **1** | Cannot be acted on without major reformulation | "Make things better." |

---

## Axis 2 — Falsifiability

**Question:** Could observation prove this wrong?

**Failure signal:** Tautology, circular definition, immune to evidence, "no true Scotsman" structure.

| Score | Description | Example |
|---|---|---|
| **5** | Makes risky predictions; specifies what observation would falsify | "Customers who experience >2 outages in a 30-day window have 60% lower 12-month retention than the baseline cohort." |
| **4** | Falsifiable but the falsifying observation is implicit | "Outages cause meaningful churn." |
| **3** | Falsifiable in principle but the test is impractical | "We could be a category leader if we doubled our investment." |
| **2** | Difficult to falsify; structure is mostly assertional | "Our customers value reliability." |
| **1** | Unfalsifiable — tautology, circular, or values-statement masquerading as fact | "Our product is the best because customers who choose it are getting the best." |

---

## Axis 3 — Scope

**Question:** Are time/population/context boundaries explicit?

**Failure signal:** Implicit "everyone, always, everywhere" — universal statements without explicit bounds.

| Score | Description | Example |
|---|---|---|
| **5** | Time, population, and context all explicit and defensible | "For US enterprise customers in Q3 2026, on accounts with >50 seats, in regions where we have local support." |
| **4** | Two of three boundaries explicit | "For enterprise customers this quarter." |
| **3** | One boundary explicit; others can be inferred | "For enterprise customers." |
| **2** | All boundaries implicit; reader must guess | "Customers want reliability." |
| **1** | Universal claim with no bounds; almost certainly wrong if generalized | "People always prefer simpler products." |

---

## Axis 4 — Audience-fit

**Question:** Does the statement match its target audience's frame?

**Failure signal:** Wrong shape — LLM gets prose narrative, exec gets recursive decomposition, peer gets BLUF without context.

| Score | Description | Example (audience: exec) |
|---|---|---|
| **5** | Perfectly fits the audience's structural and cognitive frame | "BOTTOM LINE: Approve $2M for onboarding rebuild in Q3. RECOMMENDATION: Allocate 4 engineers full-time. RISK IF DEFERRED: 12% churn becomes 18%." |
| **4** | Fits the audience but with one structural misstep | "We should rebuild onboarding because churn is up. The plan would take 4 engineers a quarter and cost ~$2M." |
| **3** | Audience-appropriate but suboptimally shaped | "Onboarding is a churn driver and we should consider rebuilding it this quarter with significant resources." |
| **2** | Wrong shape for the stated audience but adjacent | "Let me walk you through the customer journey, which begins with..." (to a time-pressured exec) |
| **1** | Fundamentally mismatched to the audience | A 5,000-word narrative case-study delivered to an exec; a one-line BLUF delivered to an LLM expecting context |

For LLM audience: see [[cursed-speech-foundations]] in skill-lab for the Anthropic-canonical structural order. LLM audience-fit means role + context + longform-data-first + examples + numbered instructions + self-check.

---

## Axis 5 — Answerability

**Question:** Could any evidence resolve this?

**Failure signal:** Values-disguised-as-fact; no evidence pathway exists; definitionally circular.

| Score | Description | Example |
|---|---|---|
| **5** | Specific evidence type would resolve; that evidence exists or is collectible | "Did the Q2 onboarding rebuild reduce 30-day churn? Compare cohorts pre/post launch using the existing analytics pipeline." |
| **4** | Evidence type is specifiable but data may not exist yet | "Does our onboarding cause more churn than competitors'?" |
| **3** | Evidence pathway is conceptually valid but operationally hard | "Are our customers more loyal than the industry average?" |
| **2** | Evidence type is unclear; the question may be values-shaped | "Do customers feel cared for?" |
| **1** | Unanswerable in principle — values masquerading as fact, or definitionally circular | "Are we the kind of company customers truly love?" |

The threshold-3 case is the most common in practice: questions that *could* be answered with a serious empirical effort but are usually treated as if they had obvious answers.

---

## Axis 6 — Root-vs-symptom

**Question:** Is this addressing the actual cause or a downstream effect?

**Failure signal:** XY pattern — statement is one level too shallow; the real problem is upstream of the stated one.

| Score | Description | Example |
|---|---|---|
| **5** | Statement names the cause; intervention at this level resolves the symptoms | "Onboarding fails to communicate the value proposition in the first 90 seconds, causing 12% of trials to abandon before reaching the activation event." |
| **4** | Statement is upstream of the symptom but not at the root; one level of decomposition would expose the root | "Onboarding is failing to convert trials." |
| **3** | Statement is at the symptom level; root is implicit but not named | "Trial-to-paid conversion is dropping." |
| **2** | Statement is downstream of the symptom; intervention here treats noise | "Q3 revenue is below plan." |
| **1** | Pure XY — statement is an attempted solution to an unstated underlying problem | "How do I add a tutorial video to onboarding?" (when the actual problem is that the value proposition isn't landing in 90 seconds) |

The XY-detector skill specifically targets score-1 cases; root-vs-symptom score 1 should always trigger XY-detector inspection.

---

## Calibration Rules

1. **Score axes independently.** Don't let a high score on one axis anchor another upward.
2. **Default to lower when uncertain.** Strict scoring saves re-state loop iterations.
3. **A 5 is rare.** Most action-ready statements score 3-4 across the board. A statement that scores 5 across all six axes is exemplary; if you see this, double-check for anchoring.
4. **A 1 is also rare.** Score 1 is reserved for catastrophic failures; most "bad" statements are 2 or 3.
5. **Recalibrate periodically.** When the rubric drifts (same statement scoring differently across runs), re-read this document.

## Edge Cases

| Pattern | How to score |
|---|---|
| Statement is a question, not an assertion | Score the question's *answerability* and *specificity* axes; treat falsifiability as N/A and assign 3 |
| Statement is purely descriptive ("Our customers are X") | Score scope, specificity, falsifiability normally; root-vs-symptom often 3 (descriptive ≠ symptom) |
| Statement is a values claim ("We should X") | Falsifiability and answerability cap at 2 unless paired with an empirical claim that would justify the values position |
| Statement is a constraint ("We can't do Y") | Specificity and scope are primary; falsifiability tests whether the constraint is real or assumed |

## Sources

- Score 1/5 anchors derived from canonical examples in:
  - Mitroff & Kilmann 1978 (Type III errors)
  - Raymond's *Jargon File* (XY problem)
  - Kahneman 2011 (attribute substitution; vague-question patterns)
- Score 5/5 anchors derived from worked examples in [[binding-vow-research-findings]]
- Calibration approach inspired by Spelunker's confidence framework (`confidence-framework.md` in research domain)
