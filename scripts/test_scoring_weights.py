#!/usr/bin/env python3
"""
test_scoring_weights.py — Pin the composite weights to a single source of truth.

The weights used to be written out three times: shared.compute_auto_score,
recalibrate_scores.py's inline formula, and the "Scoring Model" panel in
app/infra.html. The only thing keeping them in step was a code comment reading
"update both together" — and when usage went from 10% to 0%, the HTML copy was
missed, so the live dashboard advertised a 10% Usage bar and the tooltip "How
often this skill gets loaded via MCP tools" for an axis contributing nothing.

shared.SCORE_WEIGHTS is now the single source; recalibrate imports it via
combine_scores. The browser cannot import Python, so infra.html necessarily
keeps a display copy — this test parses that copy and fails if it disagrees,
which is the enforcement a comment could not provide.

Run: python3 scripts/test_scoring_weights.py
"""

import json
import re
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "mcp-server"))

from shared import (  # noqa: E402
    SCORE_WEIGHTS, combine_scores, compute_auto_score, load_log, iter_skill_uses,
    score_structure, score_depth, score_connectivity, score_freshness,
    score_usage, score_feedback,
)

INFRA_HTML = ROOT / "app" / "infra.html"
REGISTRY = ROOT / "data" / "registry.json"


def parse_infra_weights() -> dict:
    """Extract the scoringFactors display array from app/infra.html.

    Deliberately strict: if the array cannot be found the test fails rather
    than passing vacuously, because a silent no-op here is how the drift this
    test exists to catch got shipped in the first place.
    """
    src = INFRA_HTML.read_text()
    block = re.search(r"const scoringFactors\s*=\s*\[(.*?)\];", src, re.S)
    assert block, "could not find `const scoringFactors = [...]` in app/infra.html"
    pairs = re.findall(r"name:\s*'([^']+)'\s*,\s*pct:\s*(\d+)", block.group(1))
    assert pairs, "found the scoringFactors array but no name/pct pairs in it"
    return {name.lower(): int(pct) for name, pct in pairs}


def test_weights_sum_to_one():
    total = sum(SCORE_WEIGHTS.values())
    assert abs(total - 1.0) < 1e-9, f"SCORE_WEIGHTS sums to {total}, not 1.0"


def test_usage_is_unweighted():
    """Guards the decision itself: usage is retained but must contribute 0.

    If someone re-weights usage they have to change this test, which is the
    point — it makes re-coupling scores to a mutable multi-writer log a
    deliberate act rather than a one-character edit.
    """
    assert SCORE_WEIGHTS["usage"] == 0.0, SCORE_WEIGHTS
    assert "usage" in SCORE_WEIGHTS, "usage must stay present, just unweighted"


def test_infra_panel_matches_source_of_truth():
    shown = parse_infra_weights()
    expected = {k: round(v * 100) for k, v in SCORE_WEIGHTS.items()}
    assert shown == expected, (
        f"app/infra.html scoringFactors disagrees with shared.SCORE_WEIGHTS.\n"
        f"  dashboard shows : {shown}\n"
        f"  source of truth : {expected}"
    )
    assert sum(shown.values()) == 100, f"displayed percentages sum to {sum(shown.values())}"


def test_combine_scores_requires_every_weighted_axis():
    """A missing axis must raise, not silently score as zero."""
    full = {k: 100 for k in SCORE_WEIGHTS}
    assert combine_scores(full) == 100
    for omit in SCORE_WEIGHTS:
        partial = {k: v for k, v in full.items() if k != omit}
        try:
            combine_scores(partial)
        except KeyError:
            continue
        raise AssertionError(f"combine_scores silently tolerated a missing '{omit}' axis")


def test_recalibrate_and_compute_auto_score_agree_on_every_skill():
    """The two scoring paths must produce identical composites for the real
    registry. They are separate call sites (recalibrate needs the per-axis
    breakdown for its U:/F: output), so this is the behavioural check that they
    stay one formula."""
    registry = json.loads(REGISTRY.read_text())["skills"]
    counts = Counter(e["skill"] for e in iter_skill_uses(load_log(ROOT / "data" / "usage.jsonl")))
    max_usage = max(counts.values()) if counts else 1
    ratings: dict = {}
    for e in load_log(ROOT / "data" / "feedback.jsonl"):
        if e.get("skill") and "rating" in e:
            ratings.setdefault(e["skill"], []).append(e["rating"])
    now = datetime(2026, 7, 26, tzinfo=timezone.utc)  # fixed: freshness is time-dependent

    mismatches = []
    for name, entry in registry.items():
        metrics = entry.get("metrics", {})
        breakdown = combine_scores({
            "structure": score_structure(metrics),
            "depth": score_depth(metrics),
            "connectivity": score_connectivity(entry),
            "freshness": score_freshness(entry, now),
            "usage": score_usage(name, counts, max_usage),
            "feedback": score_feedback(name, ratings),
        })
        direct = compute_auto_score(entry, counts, max_usage, ratings, now)
        if breakdown != direct:
            mismatches.append((name, breakdown, direct))
    assert not mismatches, f"{len(mismatches)} skills score differently: {mismatches[:5]}"
    assert len(registry) > 100, f"only {len(registry)} skills checked — registry looks truncated"


def test_usage_cannot_change_any_score():
    """End-to-end proof of the decision: no usage distribution changes a score.

    This is the property that decouples scoring from the telemetry log, so a
    corrupt or inflated usage row can no longer move the registry.
    """
    registry = json.loads(REGISTRY.read_text())["skills"]
    now = datetime(2026, 7, 26, tzinfo=timezone.utc)
    sample = list(registry.items())[:60]
    for name, entry in sample:
        none = compute_auto_score(entry, Counter(), 1, {}, now)
        heavy = compute_auto_score(entry, Counter({name: 10_000}), 10_000, {}, now)
        assert none == heavy, (
            f"{name}: usage moved the score {none} -> {heavy}; usage must be inert"
        )


def main() -> None:
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    failed = 0
    for t in tests:
        try:
            t()
            print(f"  ✓ {t.__name__}")
        except AssertionError as e:
            print(f"  ✗ {t.__name__}: {e}")
            failed += 1
    print(f"\n{len(tests) - failed}/{len(tests)} passed")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
