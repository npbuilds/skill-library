# Spelunker research-quality eval — design note

A harder, research-grade complement to the existing structural-contract suite
(`skills/research/spelunker/eval/tasks.yaml`), which stays intact. This suite
asks: *is the brief epistemically well-calibrated and auditable*, not just *is it
shaped correctly*. Status: **design + scaffold + deterministic self-test + a tiny
live smoke test**. No full live optimization/eval has been run — that awaits review.

## Two-part signal

### 1. Gate-eligible objective metrics (deterministic → may gate edits)

**a. Ground-truth calibration (primary signal).** 15 well-documented claims, each
labeled with a known epistemic status: `true`, `refuted`, or `contested`. The
grader reads the brief's confidence tag on the CORE claim and scores the match,
with partial credit for adjacent tags.

Spelunker's vocabulary has five tags (`Confirmed/Likely/Speculative/Contested/
Unverifiable`) and **no `Refuted` tag**. So:
- `true`     → reward `Confirmed` (1.0), `Likely` (0.7); penalize a `Contested`/
  refutation reading.
- `contested`→ reward `Contested` (1.0); **heavily penalize false confidence**
  (`Confirmed`/`Likely` ≈ 0.0–0.1). This is the headline behavior the suite exists
  to protect: a good researcher tags genuine disputes as Contested.
- `refuted`  → tags alone can only signal "not Confirmed"; full credit comes from a
  detected **refutation stance** (regex for refute/false/not-supported/debunked,
  absent affirmation language). Affirming a false claim → ≈ 0.0 (worst case).

Per-status credit tables and the stance logic live in `scripts/skillopt/quality.py`
(`TAG_SCORE`, `calibration_score`). Calibration returns 0–100.

**b. Citation integrity (quality-adjacent but objective).** From the brief:
- every inline `[N]` marker resolves to a numbered `SOURCES` entry (no dangling markers),
- no orphan/unused SOURCES entries (every source is cited),
- each SOURCES entry is well-formed (`Tier N` + `Used for:`).

Score = `100 * (0.5*resolve_rate + 0.25*no_orphan_rate + 0.25*wellformed_rate)`;
zero if the brief cites no sources at all. **Live-URL existence checking is OFF by
default** (`check_urls=False`) — the web is noisy and slow; it can be enabled
later as an opt-in.

**Gate composite (the gateable 0–100 task_score):**
```
gate = 0.7 * calibration  +  0.3 * citation_integrity
```
Calibration is weighted higher because it is the primary quality signal;
citation integrity is a necessary-but-not-sufficient hygiene floor. Threshold for
"passed" is 70. These weights are a starting point — flagged for review below.

### 2. Diagnostic-only judged metrics (LLM-as-judge; reported, NEVER gates)

Consistent with the project principle that **rubric/judge signals stay off the val
gate**, a structured judge scores four criteria 1–5 with a one-sentence
justification each:
- `triangulation_depth` — genuinely-independent sources, not one source restated
- `disconfirmation_effectiveness` — did the adversarial/counterfactual pass stress or change a conclusion
- `primary_source_tracing` — citations reach primary sources, not secondary/news/Wikipedia
- `gaps_honesty` — GAPS & LIMITATIONS candid and specific

The judge backend is the active `llm.py` solver's `complete()` (configurable via
`SKILLOPT_LLM`); the rubric is explicit and returns JSON. These numbers are
recorded in the result `detail` and reported, but **never** enter `gate`. Why:
judge scores are nondeterministic and model-dependent; gating on them would let an
edit "win" by flattering the judge rather than improving real calibration.

## Registry schema decision

**Implemented (least-disruptive): a sibling key.**
- `task_score` keeps the **contract** suite result (unchanged).
- `task_score_quality` holds the **quality** suite result (same object shape:
  `verdict/val/test/lift/no_skill_test/backend/last_run/report` + `suite`).

Every existing consumer keeps working untouched, because they only read
`task_score`: `snapshot_evolution.py` (now also carries null-safe
`task_score_quality_test`/`_verdict`), the app detail-panel guard
(`if (s.task_score …)`), and `migrate_to_firestore.py` (`dict(skill)` passthrough
copies the new sibling key automatically). The writer is
`common.write_task_score(skill, obj, key="task_score_quality")`; `evaluate.py
--suite quality` selects the key, the `eval/quality-tasks.yaml` task file, and the
`<skill>-quality.gonogo.md` report.

**Alternative considered (rejected for now): make `task_score` a dict of named
suites**, e.g. `task_score = {"contract": {...}, "quality": {...}}`. Cleaner
long-term, but it breaks the current app guard and `snapshot_evolution` field
reads (`task_score.test`), and would require a coordinated migration of every
consumer. Recommend revisiting only if a third+ suite appears.

## Known limitations / variance risks

1. **Calibration extraction is heuristic.** It reads the core claim's tag as an
   explicit `Overall/Core claim confidence:` line if present, else the first
   `Confidence: <Tag>`. A brief that buries or reorders its core-claim tag could
   be mis-read. Mitigation idea: have the synthesizer emit an explicit
   `CORE CLAIM CONFIDENCE: <Tag>` line (small skill tweak) to make this exact.
2. **`refuted` has no native tag** → we infer a refutation *stance* by regex. This
   is deterministic but approximate; a brief that refutes a claim using unusual
   phrasing could be undercredited. This is the single biggest correctness risk.
3. **Calibration ground truth is a curated snapshot.** "Contested" status can
   shift as science evolves; claims were chosen for *stable* status, but the set
   needs periodic review.
4. **Gate weights (0.7/0.3) and the 70 threshold are unvalidated** — tune against
   real briefs before trusting the gate to accept/reject edits.
5. **Small val (5 tasks)** + nondeterministic live rollouts means the gate can
   flap; the per-(backend, skill-hash, task) cache stabilizes a given body, and the
   held-out test split is the real arbiter (same discipline as the other suites).
6. **No web access in `--mode ask`** smoke runs: the model writes briefs from
   parametric knowledge, so citation integrity measures internal consistency, not
   real source existence (URL checking stays opt-in).

## Open questions for review (before spending rollout budget)

- Are the gate weights (0.7 calibration / 0.3 citation) and 70 pass threshold right?
- OK to add a one-line `CORE CLAIM CONFIDENCE:` to the spelunker output contract to
  make calibration extraction exact (limitation #1/#2)?
- Should the quality suite ever gate optimizer edits, or remain a **reported
  scorecard** only (given calibration's heuristic edges)?
- Keep the sibling-key schema, or plan the `task_score`-as-dict migration now?
- Confirm the 15 curated claims and their status labels (esp. the `contested` set).

## Files

- `scripts/skillopt/quality.py` — grader (calibration + citation gate; diagnostic judge); `--selftest`.
- `skills/research/spelunker/eval/quality-tasks.yaml` — 15 labeled claims + judge config (train/val/test).
- Wiring: `grader.grade_one` (checker `quality`), `runner.score_skill` (judge backend), `common.write_task_score(key=)`, `evaluate.py --suite quality`, `snapshot_evolution.py` (null-safe carry).

## How to run the full suite later (not yet run)

```
SKILLOPT_SKILL=spelunker SKILLOPT_LLM=cursor \
  python3 scripts/skillopt/evaluate.py --suite quality --write-report --write-registry
```
