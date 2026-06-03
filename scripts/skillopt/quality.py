#!/usr/bin/env python3
"""quality.py — research-QUALITY grader for the `spelunker` skill.

A harder complement to the structural-contract suite (which stays intact). Two
parts, by design:

  GATE-ELIGIBLE (deterministic, 0-100 — may gate edits):
    - calibration:  does the brief's confidence tag on the CORE claim match the
                    claim's known epistemic status? Partial credit for adjacent
                    tags; contested claims are rewarded for being tagged
                    Contested (not Confirmed) and penalized for false confidence.
                    Spelunker has no `Refuted` tag, so for refuted claims we
                    detect a refutation STANCE instead of a tag.
    - citation_integrity: every inline [N] resolves to a SOURCES entry, no
                    orphan/unused entries, entries well-formed (Tier N + Used for:).
                    Optional live-URL existence checking is OFF by default.

  DIAGNOSTIC-ONLY (LLM-as-judge, reported but NEVER gates — consistent with the
  project's "rubric stays off the val gate" principle):
    triangulation_depth, disconfirmation_effectiveness, primary_source_tracing,
    gaps_honesty — each scored 1-5 with a justification by a configurable judge.

Gate composite (default): 0.7 * calibration + 0.3 * citation_integrity.
"""
from __future__ import annotations

import json
import re
from typing import Callable

CONF_TAGS = ("Confirmed", "Likely", "Speculative", "Contested", "Unverifiable")

# Per-status credit for the core claim's confidence tag (0-1). Adjacent tags get
# partial credit; over-confidence on contested/refuted claims is punished hard.
TAG_SCORE: dict[str, dict[str, float]] = {
    "true": {
        "Confirmed": 1.0, "Likely": 0.7, "Speculative": 0.3,
        "Contested": 0.1, "Unverifiable": 0.2,
    },
    "contested": {
        "Contested": 1.0, "Speculative": 0.5, "Unverifiable": 0.4,
        "Likely": 0.1, "Confirmed": 0.0,
    },
    "refuted": {
        # No `Refuted` tag exists; tags alone can at best signal "not Confirmed".
        # The refutation STANCE check below is what earns full credit.
        "Confirmed": 0.0, "Likely": 0.15, "Speculative": 0.5,
        "Contested": 0.5, "Unverifiable": 0.4,
    },
}

_REFUTE_RX = re.compile(
    r"\b(refut\w*|debunk\w*|false|not supported|unsupported|no (?:credible |good )?evidence"
    r"|contradicted|disconfirm\w*|does not hold|fails to|myth|incorrect|disproven?)\b", re.I)
_AFFIRM_RX = re.compile(
    r"\b(confirmed|well[- ]established|robust evidence|strongly supported|holds up"
    r"|consensus supports|is true|well[- ]supported)\b", re.I)

# PRIMARY signal: the explicit graded contract line `CORE CLAIM CONFIDENCE: <Tag>`.
_CORE_RX = re.compile(r"CORE CLAIM CONFIDENCE:\s*\[?(" + "|".join(CONF_TAGS) + r")", re.I)
# Secondary heuristics (used only if the explicit line is absent).
_OVERALL_RX = re.compile(
    r"(?:overall|core claim|core)\s+confidence:\s*\[?(" + "|".join(CONF_TAGS) + r")", re.I)
_CONF_RX = re.compile(r"Confidence:\s*\[?(" + "|".join(CONF_TAGS) + r")", re.I)


def _canon_tag(s: str | None) -> str | None:
    if not s:
        return None
    s = s.strip().lower()
    for t in CONF_TAGS:
        if t.lower() == s:
            return t
    return None


def extract_core_tag(text: str) -> str | None:
    """The confidence tag applied to the core/headline claim.

    PRIMARY: the explicit graded contract line `CORE CLAIM CONFIDENCE: <Tag>`
    (exact parse). FALLBACK (only if that line is absent): a looser
    'Overall/Core ... confidence:' line, then the FIRST 'Confidence: <Tag>'
    (the core claim is decomposed/presented first).
    """
    text = text or ""
    for rx in (_CORE_RX, _OVERALL_RX, _CONF_RX):
        m = rx.search(text)
        if m:
            return _canon_tag(m.group(1))
    return None


def calibration_score(text: str, gold_status: str) -> dict:
    text = text or ""
    gold = str(gold_status if gold_status is not None else "").strip().lower()
    tag = extract_core_tag(text)
    refute = bool(_REFUTE_RX.search(text))
    affirm = bool(_AFFIRM_RX.search(text))
    base = TAG_SCORE.get(gold, {}).get(tag, 0.0)

    if gold == "refuted":
        if refute and not affirm:
            base = max(base, 0.9)
        elif affirm and not refute:
            base = min(base, 0.1)          # affirmed a false claim — worst case
    elif gold == "true":
        if affirm and tag in ("Confirmed", "Likely"):
            base = max(base, 0.9 if tag == "Confirmed" else base)
        elif refute and not affirm:
            base = min(base, 0.2)          # refuted a true claim
    elif gold == "contested":
        if tag == "Contested":
            base = 1.0
        elif tag in ("Confirmed", "Likely") and not (refute and affirm):
            base = min(base, 0.1)          # false confidence on a contested claim

    return {
        "score": round(base * 100, 1),
        "core_tag": tag,
        "gold_status": gold,
        "stance": {"refute": refute, "affirm": affirm},
    }


# ── Citation integrity ─────────────────────────────────────────────────────────

def _split_sources(text: str) -> tuple[str, str]:
    """Return (body_before_sources, sources_block). Bounds SOURCES..NEXT STEPS."""
    lines = text.splitlines()
    s_idx = n_idx = -1
    for i, ln in enumerate(lines):
        bare = ln.lstrip("#*->` \t")
        if s_idx < 0 and bare.startswith("SOURCES"):
            s_idx = i
        elif s_idx >= 0 and bare.startswith("NEXT STEPS"):
            n_idx = i
            break
    if s_idx < 0:
        return text, ""
    body = "\n".join(lines[:s_idx])
    end = n_idx if n_idx >= 0 else len(lines)
    return body, "\n".join(lines[s_idx + 1:end])


def citation_integrity(text: str, check_urls: bool = False) -> dict:
    """Deterministic citation hygiene, 0-100.

    - resolve:    inline [N] markers that map to a SOURCES entry N
    - no_orphans: every SOURCES entry is cited at least once
    - wellformed: every SOURCES entry carries 'Tier N' and 'Used for:'
    `check_urls` is intentionally OFF by default (web is noisy/slow).
    """
    text = text or ""
    body, sources_block = _split_sources(text)

    markers = [int(m) for m in re.findall(r"\[(\d+)\]", body)]
    src_nums, wellformed = [], 0
    for ln in sources_block.splitlines():
        m = re.match(r"\s*(\d+)\.\s+(.*)", ln.lstrip("#*->` \t"))
        if not m:
            continue
        num = int(m.group(1))
        src_nums.append(num)
        entry = m.group(2)
        # the entry may continue on following lines, but checking the head line is
        # a reasonable deterministic proxy for well-formedness.
        if re.search(r"Tier\s*\d+", entry, re.I) and re.search(r"Used for:", entry, re.I):
            wellformed += 1
    src_set = set(src_nums)

    marker_set = set(markers)
    resolved = sum(1 for m in marker_set if m in src_set)
    resolve_rate = resolved / len(marker_set) if marker_set else (1.0 if src_set else 0.0)
    used_sources = sum(1 for n in src_set if n in marker_set)
    no_orphan_rate = used_sources / len(src_set) if src_set else 0.0
    wellformed_rate = wellformed / len(src_nums) if src_nums else 0.0

    # No sources at all => zero integrity (a spelunker brief must cite).
    if not src_set:
        score = 0.0
    else:
        score = round(100.0 * (0.5 * resolve_rate + 0.25 * no_orphan_rate + 0.25 * wellformed_rate), 1)

    return {
        "score": score,
        "markers": sorted(marker_set),
        "sources": sorted(src_set),
        "unresolved_markers": sorted(m for m in marker_set if m not in src_set),
        "unused_sources": sorted(n for n in src_set if n not in marker_set),
        "wellformed_sources": wellformed,
        "url_check": "skipped" if not check_urls else "enabled",
    }


# ── Diagnostic LLM-as-judge (NEVER gates) ───────────────────────────────────────

JUDGE_CRITERIA = {
    "triangulation_depth": "Are claims supported by multiple genuinely-independent sources (not the same source restated)?",
    "disconfirmation_effectiveness": "Did the adversarial/counterfactual pass actually stress or change a conclusion, or was it pro-forma?",
    "primary_source_tracing": "Do citations reach primary sources rather than stopping at secondary/news/Wikipedia?",
    "gaps_honesty": "Is the GAPS & LIMITATIONS section candid and specific about what could not be established?",
}


def judge_quality(text: str, judge_complete: Callable[[str, str], str] | None,
                  criteria: dict | None = None) -> dict | None:
    """Diagnostic-only structured rubric. Returns per-criterion 1-5 + justification.

    Reported, never gated. Returns None if no judge backend is wired.
    """
    if judge_complete is None:
        return None
    criteria = criteria or JUDGE_CRITERIA
    rubric = "\n".join(f"- {k}: {v}" for k, v in criteria.items())
    system = (
        "You are a strict research-methodology judge. Score a research brief on "
        "each criterion from 1 (poor) to 5 (excellent). Reply with ONLY a JSON "
        'object: {"<criterion>": {"score": <1-5>, "justification": "<one sentence>"}}.'
    )
    user = f"CRITERIA:\n{rubric}\n\nBRIEF:\n{text[:12000]}"
    try:
        raw = judge_complete(system, user)
        start, end = raw.index("{"), raw.rindex("}") + 1
        obj = json.loads(raw[start:end])
    except (ValueError, json.JSONDecodeError, Exception):  # noqa: BLE001 - diagnostic only
        return {"error": "judge did not return parseable JSON", "raw_excerpt": (raw[:200] if 'raw' in dir() else "")}
    out = {}
    for k in criteria:
        v = obj.get(k, {})
        if isinstance(v, dict):
            out[k] = {"score": v.get("score"), "justification": v.get("justification")}
        else:
            out[k] = {"score": v, "justification": None}
    return out


# ── Top-level scorer (the gate score is deterministic; judge is diagnostic) ─────

GATE_WEIGHTS = {"calibration": 0.7, "citation": 0.3}


def score_quality(task: dict, text: str, judge_complete: Callable | None = None,
                  check_urls: bool = False) -> dict:
    cal = calibration_score(text, task.get("epistemic_status", ""))
    cit = citation_integrity(text, check_urls=check_urls)
    gate = round(GATE_WEIGHTS["calibration"] * cal["score"]
                 + GATE_WEIGHTS["citation"] * cit["score"], 1)
    return {
        "score": gate,                         # gate-eligible, deterministic
        "passed": gate >= 70.0,
        "calibration": cal,
        "citation_integrity": cit,
        "weights": GATE_WEIGHTS,
        "judged": judge_quality(text, judge_complete),  # diagnostic-only / None
    }


# ── Self-check (no live calls) ──────────────────────────────────────────────────

def _selftest() -> int:
    well = (
        "RESEARCH BRIEF\nKEY FINDINGS\n"
        "The claim is genuinely disputed: credible studies reach opposite conclusions [1][2].\n"
        "DETAILED FINDINGS\n"
        "Confidence: Contested because two bodies of high-quality evidence disagree [1][2].\n"
        "GAPS & LIMITATIONS\n- No RCT settles the question.\n"
        "SOURCES\n"
        "1. Smith 2019, Tier 1, Used for: pro position.\n"
        "2. Jones 2021, Tier 1, Used for: con position.\n"
        "NEXT STEPS\n- Run a trial.\n"
    )
    miscal = (
        "RESEARCH BRIEF\nKEY FINDINGS\n"
        "This is well-established and strongly supported [1].\n"
        "DETAILED FINDINGS\n"
        "Confidence: Confirmed because the evidence is robust [1][3].\n"  # [3] is orphan
        "GAPS & LIMITATIONS\n- none.\n"
        "SOURCES\n"
        "1. A blog post.\n"                                              # missing Tier/Used for
        "2. Unused 2020, Tier 2, Used for: nothing.\n"                   # unused source
        "NEXT STEPS\n- n/a.\n"
    )
    contested_task = {"epistemic_status": "contested"}
    r_well = score_quality(contested_task, well)
    r_mis = score_quality(contested_task, miscal)
    cases = [
        ("well calibration", r_well["calibration"]["score"], lambda v: v == 100.0),
        ("well citation", r_well["citation_integrity"]["score"], lambda v: v == 100.0),
        ("well gate >= 90", r_well["score"], lambda v: v >= 90.0),
        ("miscal calibration ~0", r_mis["calibration"]["score"], lambda v: v <= 10.0),
        ("miscal citation < 60", r_mis["citation_integrity"]["score"], lambda v: v < 60.0),
        ("miscal gate < 30", r_mis["score"], lambda v: v < 30.0),
        ("orphan detected", len(r_mis["citation_integrity"]["unresolved_markers"]), lambda v: v == 1),
        ("unused detected", len(r_mis["citation_integrity"]["unused_sources"]), lambda v: v == 1),
        ("judge none w/o backend", r_well["judged"], lambda v: v is None),
    ]
    # refuted-status stance check
    refuted_good = ("DETAILED FINDINGS\nConfidence: Contested because evidence refutes it; "
                    "the claim is false and not supported [1].\nSOURCES\n1. X, Tier 1, Used for: y.\n")
    refuted_bad = ("DETAILED FINDINGS\nConfidence: Confirmed because it is well-established [1].\n"
                   "SOURCES\n1. X, Tier 1, Used for: y.\n")
    cases.append(("refuted+refutation stance high",
                  calibration_score(refuted_good, "refuted")["score"], lambda v: v >= 90.0))
    cases.append(("refuted+affirm stance low",
                  calibration_score(refuted_bad, "refuted")["score"], lambda v: v <= 10.0))

    # Explicit CORE CLAIM CONFIDENCE line must take precedence over the first
    # 'Confidence:' (which here belongs to a sub-claim tagged Likely).
    explicit = (
        "RESEARCH BRIEF\nCORE CLAIM CONFIDENCE: Contested\n"
        "DETAILED FINDINGS\n"
        "Sub-claim A — Confidence: Likely because one strong source supports it [1].\n"
        "Core claim — Confidence: Contested because the literature genuinely disagrees [1][2].\n"
        "SOURCES\n1. X, Tier 1, Used for: a.\n2. Y, Tier 1, Used for: b.\n"
    )
    cases.append(("explicit core-confidence line wins", extract_core_tag(explicit) == "Contested", lambda v: v is True))
    cases.append(("explicit line calibration (contested)",
                  calibration_score(explicit, "contested")["score"], lambda v: v == 100.0))

    fails = 0
    for name, got, ok in cases:
        good = ok(got)
        print(f"  {'✓' if good else '✗'} {name}: {got}")
        fails += 0 if good else 1
    print("quality selftest:", "OK" if not fails else f"{fails} FAILURE(S)")
    return 1 if fails else 0


if __name__ == "__main__":
    import sys
    raise SystemExit(_selftest() if "--selftest" in sys.argv else (print(__doc__) or 0))
