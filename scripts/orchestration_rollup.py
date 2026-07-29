#!/usr/bin/env python3
"""Validate and roll up orchestration practice reps.

Companion to the practice plan v1.2 (vault: skill-lab/2026-07-25-orchestration-mastery-practice-plan.md).
The plan prescribes a scoring loop; this is the instrument that reads it back.

    python3 scripts/orchestration_rollup.py                  # validate + monthly rollup
    python3 scripts/orchestration_rollup.py --new full       # emit a blank full-comparison run card
    python3 scripts/orchestration_rollup.py --new compact    # emit a blank prediction-only run card
    python3 scripts/orchestration_rollup.py --audit-template # emit the Phase 2 baseline scorecard

Exit codes: 0 clean, 1 validation failure.
"""

import argparse
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REPS = ROOT / "data" / "orchestration-reps.jsonl"
SCHEMA = ROOT / "data" / "orchestration-reps.schema.json"

FACULTIES = ["S1", "S2", "S3", "S4", "S5", "S6"]
FACULTY_NAMES = {
    "S1": "Verification & eval design",
    "S2": "Decomposition & spec authoring",
    "S3": "Context management",
    "S4": "Delegation & architecture calibration",
    "S5": "Review under satisficing",
    "S6": "Trust, calibration & recovery",
}
COMPARED = ("full", "audited_prediction")
EXTERNAL_GRADERS = ("outcome_check", "human_blind")


def load_reps(path=None):
    path = path or REPS
    if not path.exists():
        return []
    reps = []
    for i, line in enumerate(path.read_text().splitlines(), 1):
        line = line.strip()
        if not line or line.startswith("//"):
            continue
        try:
            reps.append(json.loads(line))
        except json.JSONDecodeError as e:
            sys.exit(f"FAIL {path.name}:{i} is not valid JSON — {e}")
    return reps


def validate(reps):
    """Schema-validate every record. The plan's own S1 lesson applied to the plan."""
    try:
        import jsonschema
    except ImportError:
        print("! jsonschema not installed — skipping schema validation (pip install jsonschema)")
        return True
    schema = json.loads(SCHEMA.read_text())
    validator = jsonschema.Draft7Validator(schema)
    ok = True
    for i, rep in enumerate(reps, 1):
        for err in sorted(validator.iter_errors(rep), key=lambda e: e.path):
            loc = "/".join(str(p) for p in err.path) or "(root)"
            print(f"FAIL rep {i} [{rep.get('rung', '?')}] {loc}: {err.message}")
            ok = False
    return ok


def pct(n, d):
    return f"{100 * n / d:.0f}%" if d else "n/a"


def case_observations(reps):
    """Non-protocol records that still carry real, artifact-verified evidence.

    protocol_rep is a single boolean, but auditability is not: reps 1-2 have complete artifact
    bundles for every claim EXCEPT the cost clause, which needs a human-attention measurement
    nobody took. Excluding them from Gate A is right; making them invisible is not - it hides
    two fault-injection cases and two decided comparisons. Reported here, counted nowhere.
    """
    cases = [r for r in reps if not r.get("protocol_rep")
             and (r.get("comparison_mode") in COMPARED or r.get("recovery_result"))]
    if not cases:
        return []
    out = []
    w = out.append
    w("### Case observations (evidence, not protocol reps)")
    w("")
    w("Artifact-verified but excluded from every Gate A count above. Present so the ledger and the "
      "written record agree.")
    w("")
    for r in cases:
        w(f"- `{r['rung']}` {r['ts']} · {r['faculty']}@{r['surface']} · {r['task_family']} · "
          f"scored {r['score']}/5")
        if r.get("comparison_mode") in COMPARED:
            w(f"  - predicted **{r['predicted_winner']}** at {r['prediction_confidence']}% → "
              f"observed **{r.get('observed_class')}** (grader: {r.get('grader_type')}"
              f"{', blinded' if r.get('grader_blinded') else ''})")
        rr = r.get("recovery_result") or {}
        if rr:
            w(f"  - recovery: detected {rr.get('detected')}, recovered {rr.get('recovered')}, "
              f"move `{rr.get('move')}`, escaped final review {rr.get('escaped_final_review')}")
        cost = r.get("cost") or {}
        if cost.get("human_min") is None:
            w(f"  - ⚠ `human_min` {cost.get('human_min_basis', 'missing')} — no cost-clause claim "
              f"can rest on this rep")
    w("")
    return out


def rollup(reps):
    protocol = [r for r in reps if r.get("protocol_rep")]
    excluded = len(reps) - len(protocol)
    out = []
    w = out.append

    w("## Orchestration practice rollup")
    w("")
    w(f"Records: **{len(reps)}** total · **{len(protocol)}** protocol reps"
      + (f" · {excluded} excluded (retrospective / pre-protocol)" if excluded else ""))
    w("")

    if not protocol:
        w("_No protocol reps logged yet. Gate A requires 10._")
        w("")
        if excluded:
            w("Pre-protocol records present (not counted):")
            for r in reps:
                if not r.get("protocol_rep"):
                    w(f"- `{r['rung']}` ({r['ts']}) — {r['faculty']} scored {r['score']}/5 — {r['change'][:110]}")
            w("")
        out.extend(case_observations(reps))
        return "\n".join(out)

    # --- practitioner (leading) ---
    w("### Practitioner measures (leading)")
    w("")
    w("| Faculty | Reps | Scores | Latest | Trend |")
    w("|---|---|---|---|---|")
    for f in FACULTIES:
        scored = [r for r in protocol if r["faculty"] == f]
        if not scored:
            w(f"| {f} {FACULTY_NAMES[f]} | 0 | — | — | — |")
            continue
        scores = [r["score"] for r in scored]
        trend = "—"
        if len(scores) >= 2:
            delta = scores[-1] - scores[0]
            trend = "rising" if delta > 0 else ("falling" if delta < 0 else "flat")
        w(f"| {f} {FACULTY_NAMES[f]} | {len(scores)} | {', '.join(map(str, scores))} | {scores[-1]}/5 | {trend} |")
    w("")

    # calibration — reported both ways, per v1.2
    compared = [r for r in protocol if r["comparison_mode"] in COMPARED]
    decisive = [r for r in compared if r.get("observed_class") in ("orchestrated_win", "simple_win")]
    inconclusive = [r for r in compared if r.get("observed_class") == "inconclusive"]

    def correct(r):
        return (r["predicted_winner"] == "orchestrated" and r["observed_class"] == "orchestrated_win") or \
               (r["predicted_winner"] == "simple" and r["observed_class"] == "simple_win")

    hits = [r for r in decisive if correct(r)]
    if compared:
        w(f"**Architecture-prediction accuracy** (both ways, per v1.2 — excluding inconclusives inflates it):")
        w("")
        w(f"- excluding inconclusive: **{pct(len(hits), len(decisive))}** ({len(hits)}/{len(decisive)})")
        w(f"- counting inconclusive as failures: **{pct(len(hits), len(compared))}** ({len(hits)}/{len(compared)})")
        brier = sum((r["prediction_confidence"] / 100 - (1.0 if correct(r) else 0.0)) ** 2 for r in decisive)
        if decisive:
            w(f"- Brier score (decisive only, lower is better): **{brier / len(decisive):.3f}**")
        w("")
    else:
        w("_No full comparisons yet — architecture-prediction accuracy is unmeasurable until a counterfactual is run._")
        w("")

    # review cost per accepted artifact — only over reps that actually measured it.
    # Summing null-as-zero would report a confident total built partly from reps that never held a stopwatch.
    measured = [r for r in protocol if (r.get("cost") or {}).get("human_min") is not None]
    unmeasured = len(protocol) - len(measured)
    art = sum(r.get("accepted_artifacts") or 0 for r in measured)
    human = sum((r.get("cost") or {}).get("human_min") or 0 for r in measured)
    if art:
        w(f"**Review cost per accepted artifact:** {human / art:.0f} human-min "
          f"({human:.0f} min / {art} artifacts, over {len(measured)} rep(s) that measured it)")
        w("")
    if unmeasured:
        w(f"⚠ **{unmeasured} protocol rep(s) never measured `human_min`.** Human attention is the binding "
          f"metric and the basis of every cost-clause win — a rep that did not time it cannot support one.")
        w("")

    # --- system (ultimate) ---
    w("### System measures (ultimate)")
    w("")
    classes = Counter(r.get("observed_class") for r in compared)
    w(f"- Full comparisons: **{len(compared)}** → "
      f"{classes.get('orchestrated_win', 0)} orchestrated · "
      f"{classes.get('simple_win', 0)} simple · "
      f"{classes.get('inconclusive', 0)} inconclusive")
    if compared:
        rate = len(inconclusive) / len(compared)
        flag = "  ← **S1 RED FLAG: grader design is not discriminating**" if rate >= 0.5 else ""
        w(f"- Inconclusive rate: **{pct(len(inconclusive), len(compared))}**{flag}")
    defects = sum(r.get("escaped_defects") or 0 for r in protocol)
    w(f"- Escaped defects: **{defects}**")
    w(f"- Total human attention: **{human:.0f} min**"
      + (f" (over {len(measured)}/{len(protocol)} reps; {unmeasured} unmeasured and excluded)" if unmeasured else ""))
    rec = [r for r in protocol if r.get("recovery_result")]
    if rec:
        recovered = sum(1 for r in rec if r["recovery_result"].get("recovered"))
        detected = sum(1 for r in rec if r["recovery_result"].get("detected"))
        w(f"- Recovery tests: **{len(rec)}** → detected {detected}, recovered **{recovered}** ({pct(recovered, len(rec))})")
    w("")

    # --- restraint (three-way, v1.2) ---
    verified_wins = [r for r in compared if r["predicted_winner"] == "simple" and r.get("observed_class") == "simple_win"]
    unverified = [r for r in protocol if r["comparison_mode"] == "prediction_only" and r["predicted_winner"] == "simple"]
    w("### Restraint (three-way — v1.2 keeps these separate)")
    w("")
    w(f"- **Verified no-orchestration wins: {len(verified_wins)}** (counterfactual actually run, simple predicted and observed to win)")
    w(f"- Unverified restraint: {len(unverified)} (simple chosen, counterfactual never run — calibration hypothesis, *not* a win)")
    w(f"- Inconclusive: {len(inconclusive)}")
    w("")

    # --- adaptive audit rate ---
    audits = [r for r in protocol if r["comparison_mode"] == "audited_prediction"]
    window = audits[-6:]
    MIN_WINDOW = 4  # never adapt the rate off a handful of audits — that is confidence outrunning accuracy
    if window:
        decisive_w = [r for r in window if r.get("observed_class") in ("orchestrated_win", "simple_win")]
        hits_w = sum(1 for r in decisive_w if correct(r))
        if len(decisive_w) < MIN_WINDOW:
            rec_rate = (f"1-in-3 (hold — only {len(decisive_w)} decisive audit(s) in the window; "
                        f"need {MIN_WINDOW} before adapting)")
        else:
            acc = hits_w / len(decisive_w)
            observed = f"{pct(hits_w, len(decisive_w))} accurate over last {len(decisive_w)} audits"
            if acc >= 0.8:
                rec_rate = f"**1-in-5** (relax — {observed})"
            elif acc < 0.6:
                rec_rate = f"**1-in-2** (tighten — {observed})"
            else:
                rec_rate = f"1-in-3 (hold — {observed})"
        w(f"**Adaptive audit rate:** {rec_rate}")
    else:
        w("**Adaptive audit rate:** 1-in-3 (default; no audits logged yet). Select audits *randomly* — "
          "choosing by feel audits the shaky predictions and inflates accuracy on the rest.")
    w("")

    # --- life-level (v1.4, Phase 0) — these outrank everything above ---
    w("### Life-level measures (v1.4 — these outrank practitioner and system layers)")
    w("")
    # craft floor (P12): solo reps per pursuit
    solo = [r for r in protocol if r.get("execution_mode") == "solo"]
    by_pursuit = defaultdict(int)
    for r in solo:
        by_pursuit[r.get("pursuit") or "unknown"] += 1
    w(f"- **P12 craft floor** — unaided (`solo`) reps logged: **{len(solo)}**"
      + (f" → {', '.join(f'{k}:{v}' for k, v in sorted(by_pursuit.items()))}" if solo else ""))
    if not solo:
        w("  - ⚠ no unaided reps logged. Floor is ≥1/month per kept domain, ≥2 for clinical judgment and prose. "
          "Deskilling is measured, not hypothetical — an empty solo column is a P12 breach, not a gap in bookkeeping.")
    w(f"- **Execution mode mix** — " + " · ".join(
        f"{m}: {sum(1 for r in protocol if r.get('execution_mode') == m)}"
        for m in ("delegated", "assisted", "solo")))
    # dormancy
    pursuits = sorted({r.get("pursuit") for r in protocol if r.get("pursuit")})
    if pursuits:
        latest = {p: max(r["ts"] for r in protocol if r.get("pursuit") == p) for p in pursuits}
        w("- **Dormancy** (plurality without forced abandonment — last touched):")
        for p in pursuits:
            w(f"  - {p}: {latest[p]}")
        w("  - Threshold: 4 weeks for the eligible four and health/family/relationship; one season for the rest. "
          "Compare against today's date manually — a dormant pursuit outranks any rubric gain.")
    # apparatus qualification (Codex amendment 4)
    app = [r for r in protocol if (r.get("pursuit") or "") == "apparatus"]
    if app:
        qual = sum(1 for r in app if r.get("apparatus_orchestrated"))
        w(f"- **Apparatus reps** — {len(app)} logged, **{qual} qualified** (build itself orchestrated). "
          f"Unqualified apparatus work is hand-coded construction: it does not score, and a large share of it "
          f"means construction has displaced practice.")
    w("")
    w("Not derivable from this log — track by hand: **protected-block survival rate** (P10; a block eaten by "
      "measurement work counts double).")
    w("")

    # --- reps 1-2 constraint experiment (v1.4) ---
    rp = [r for r in protocol if r.get("review_pressure")]
    sp = [r for r in protocol if r.get("switch_pressure")]
    if rp or sp:
        w("### Constraint experiment (reps 1–2): review pressure vs switching cost")
        w("")
        if rp:
            qd = [r["review_pressure"].get("queue_depth_at_session_end") for r in rp]
            qd = [x for x in qd if x is not None]
            dfr = sum((r["review_pressure"].get("accepted_without_full_review") or 0) for r in rp)
            w(f"- Review pressure — n={len(rp)} · queue depth {qd if qd else 'n/a'} · "
              f"accepted-without-full-review: {dfr}")
        if sp:
            pt = [r["switch_pressure"].get("pursuits_touched") for r in sp]
            pt = [x for x in pt if x is not None]
            ro = [r["switch_pressure"].get("reorientation_min") for r in sp]
            ro = [x for x in ro if x is not None]
            w(f"- Switching pressure — n={len(sp)} · pursuits touched {pt if pt else 'n/a'} · "
              f"re-orientation min {ro if ro else 'n/a'}")
        w("- **Discriminator:** if escaped defects track queue depth → review-bound (S5 is the leverage point). "
          "If they track switch count / re-orientation → switching-bound (batching + session architecture, mostly S3). "
          "If both rise together they are one constraint expressed twice — say so and stop measuring separately after rep 2.")
        w("")

    # --- Gate A progress ---
    families = {r["task_family"] for r in protocol}
    reviews = [r for r in protocol if r.get("grader_type") in EXTERNAL_GRADERS]
    recoveries = [r for r in protocol if (r.get("recovery_result") or {}).get("recovered")]
    w("### Gate A — personal-mastery evidence")
    w("")
    gates = [
        (f"1. >=10 scored reps", len(protocol) >= 10, f"{len(protocol)}/10"),
        (f"2. >=3 task families", len(families) >= 3, f"{len(families)}/3 ({', '.join(sorted(families)) or 'none'})"),
        (f"3. >=2 outcome-based or human external reviews", len(reviews) >= 2, f"{len(reviews)}/2"),
        (f"4. >=1 VERIFIED no-orchestration win", len(verified_wins) >= 1, f"{len(verified_wins)}/1"),
        (f"5. >=1 successful failure-recovery case", len(recoveries) >= 1, f"{len(recoveries)}/1"),
        (f"6. architecture predictions improving", None, "manual — see accuracy trend above"),
        (f"7. stable failure taxonomy from observed cases", None, "manual"),
    ]
    for label, met, detail in gates:
        mark = "[x]" if met else ("[ ]" if met is False else "[~]")
        w(f"- {mark} {label} — {detail}")
    w("")
    w("Gate B (publishable skill) is assessed separately: B1 cross-runtime portability, B2 human usability.")
    w("")
    out.extend(case_observations(reps))

    # --- changes ledger: the anti-ritual guard ---
    recent = protocol[-3:]
    empty = [r for r in recent if not r.get("change") or r["change"].strip().lower() in ("", "none", "n/a", "nothing")]
    w("### Anti-ritual guard")
    w("")
    if len(recent) == 3 and len(empty) == 3:
        w("**TRIGGERED — 3 consecutive reps produced no change worth making.** The loop has become compliance. "
          "Revise the AAR template or raise the significance threshold; do not keep scoring.")
    else:
        w(f"OK — {3 - len(empty)}/{len(recent)} of the last {len(recent)} reps produced a change.")
    w("")
    w("### Changes ledger (most recent first)")
    w("")
    for r in reversed(protocol[-8:]):
        w(f"- `{r['rung']}` {r['ts']} · {r['faculty']}@{r['surface']} · {r['score']}/5 — {r['change']}")
    w("")

    return "\n".join(out)


BLANK_FULL = {
    "ts": "YYYY-MM-DD", "project": "", "rung": "calibration-1", "task_family": "research",
    "protocol_rep": True, "faculty": "S4", "surface": "Architect",
    "comparison_mode": "full", "execution_mode": "delegated", "pursuit": "job",
    "review_pressure": {"review_min": None, "queue_depth_at_session_end": None, "accepted_without_full_review": None},
    "switch_pressure": {"pursuits_touched": None, "reorientation_min": None, "reread_events": None},
    "architecture": "", "rejected_alt": "",
    "simple_baseline": "one capable agent, same brief + tools + sources + acceptance criteria, fair shot",
    "compute_control": None,
    "predicted_winner": "orchestrated", "architecture_prediction": "", "prediction_confidence": 50,
    "primary_outcome": "", "meaningful_margin": ">=1 full point on the 5-point blind rubric",
    "grader_type": "human_blind", "grader_blinded": True, "execution_order": "",
    "observed_class": "inconclusive",
    "score": 3, "evidence": "", "blind_grader_score": None,
    "recovery_test": None, "recovery_result": None,
    "cost": {"tokens": None, "model_calls": None, "elapsed_min": None, "human_min": 0, "rework_min": None},
    "accepted_artifacts": 0, "escaped_defects": 0, "change": "", "notes": None,
}

BLANK_COMPACT = {
    "ts": "YYYY-MM-DD", "project": "", "rung": "R1", "task_family": "infra",
    "protocol_rep": True, "faculty": "S1", "surface": "Judge",
    "comparison_mode": "prediction_only", "execution_mode": "delegated", "pursuit": "apparatus",
    "apparatus_orchestrated": True,
    "architecture": "", "rejected_alt": "",
    "predicted_winner": "orchestrated", "prediction_confidence": 50,
    "score": 3, "evidence": "",
    "cost": {"human_min": 0},
    "accepted_artifacts": 0, "change": "",
}

AUDIT_TEMPLATE = """## Phase 2 — baseline self-audit scorecard

**Step 1 — pre-register before scoring anything.** Weakest two faculties will be ______ and ______.
(This is calibration data point zero. Do not revise it after scoring.)

**Step 2 — score from transcript evidence only.** What actually happened, not what you remember
intending. One session, timeboxed. Unaided self-assessment correlates only r~0.26-0.33 with
objective performance, so the anchors below are the instrument — score against them, not vibes.

### Anchor crib (full anchors: skill-lab/2026-07-25-orchestration-mastery-practice-plan)

| | 1 | 3 | 5 |
|---|---|---|---|
| **S1** verification | no pass/fail criteria; accepts "done" narrative | criteria written before delegating; runs checks | ladder designed up front; demands artifacts; adversarial fresh-context reviewer |
| **S2** decomp/spec | mega-prompts; no spec; iterates in a degraded session | explores then plans; specs large tasks | interview-to-spec; decomposition matches dependency structure; watching optional |
| **S3** context | kitchen-sink sessions; corrects same agent 3+ times | clears between tasks; two-strikes restart | context budgeted end-to-end; isolation by design; artifacts over memory |
| **S4** delegation/arch | defaults to a favorite topology; no sizing; rides failures | sizes 1-6h; WIP 3-5; abandons early | selects among workflow/single/ensemble/manager-worker/handoff/**no-AI** and defends the rejected simpler alternative; predicts the winner |
| **S5** review | rubber-stamps fluent output, or line-reads everything | risk-weighted; aware of the 4 satisficing traps | review pipeline designed; cost per accepted artifact measured and engineered down |
| **S6** trust/recovery | global trust or distrust; failure = longer prompt | capability map; re-tests on version change; detects and stops | delegates more AND intervenes more; pre-registered predictions; bounded diagnostic + changed attempt |

### Scores

| Run | S1 verif | S2 decomp | S3 context | S4 deleg/arch | S5 review | S6 trust/recov |
|---|---|---|---|---|---|---|
| Archon v2.1 build | | | | | | |
| Scheherazade two-critic loop | | | | | | |
| conflict-design 106-agent round | | | | | | |
| dataviz round | | | | | | |
| book-1 four-lane Workflow | | | | | | |
| **median** | | | | | | |
| **blind grader** (score BEFORE reconciling) | | | | | | |

**Step 3 — blind grader.** Run the same transcripts past a fresh-context grader with the rubric
verbatim, architecture identity stripped. Record its row above *before* reconciling with yours.
Disagreement is not noise: it is direct S1 data and the first evidence on whether LLM-as-judge
works as a calibration anchor here.

### Codex's four questions, per run

| Run | Why this architecture? | Simpler alternative rejected? | End state independently verifiable? | What happened when it drifted? |
|---|---|---|---|---|
| Archon v2.1 build | | | | |
| Scheherazade two-critic loop | | | | |
| conflict-design 106-agent round | | | | |
| dataviz round | | | | |
| book-1 four-lane Workflow | | | | |

### Output

- **Weakest two (observed):** ______ and ______
- **Pre-registration correct?** yes / partly / no  → first calibration data point
- **Learner vs blind grader — largest gap:** ______ (which faculty, how many points, why)
- **Ladder reordering implied:** ______ (reorder R1-R6 so the weakest two get stressed first)
"""


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--new", choices=["full", "compact"], help="emit a blank run card as JSON")
    ap.add_argument("--audit-template", action="store_true", help="emit the Phase 2 scorecard")
    ap.add_argument("--json", action="store_true", help="machine-readable validation result only")
    ap.add_argument("--file", type=Path, help="read reps from an alternate JSONL (for testing)")
    args = ap.parse_args()

    if args.new:
        blank = BLANK_FULL if args.new == "full" else BLANK_COMPACT
        print(json.dumps(blank, indent=2))
        print("\n# append as one line:  python3 -c \"import json,sys;print(json.dumps(json.load(sys.stdin)))\""
              " < card.json >> data/orchestration-reps.jsonl", file=sys.stderr)
        return 0

    if args.audit_template:
        print(AUDIT_TEMPLATE)
        return 0

    reps = load_reps(args.file)
    ok = validate(reps)
    if args.json:
        print(json.dumps({"records": len(reps), "valid": ok}))
        return 0 if ok else 1
    if not ok:
        print("\nValidation failed — fix records before rolling up.")
        return 1
    print(f"[ok] {len(reps)} record(s) valid against {SCHEMA.name}\n")
    print(rollup(reps))
    return 0


if __name__ == "__main__":
    sys.exit(main())
