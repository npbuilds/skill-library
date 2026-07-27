#!/usr/bin/env python3
"""Regression tests for every score-writing maintenance path."""

from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import sys
import tempfile
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "mcp-server"))

from shared import compute_auto_score, compute_composite_score  # noqa: E402


def load_script(name: str, filename: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / filename)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def sample_entry() -> dict:
    return {
        "name": "sample",
        "manual_rating": 100,
        "auto_score": 1,
        "composite_score": 1,
        "health_status": "healthy",
        "status": "active",
        "parent": None,
        "depends_on": [],
        "referenced_by": [],
        "last_modified": datetime.now(timezone.utc).date().isoformat(),
        "metrics": {
            "body_words": 700,
            "word_count": 700,
            "description_words": 35,
            "section_count": 5,
            "reference_files": 2,
        },
    }


def test_recalibrate_script_preserves_manual_rating():
    recalibrate = load_script("recalibrate_writer_test", "recalibrate_scores.py")
    entry = sample_entry()
    expected_auto = compute_auto_score(
        entry, Counter(), 1, {}, datetime.now(timezone.utc)
    )
    expected_composite = compute_composite_score(expected_auto, 100)

    with tempfile.TemporaryDirectory() as directory:
        data = Path(directory)
        registry_path = data / "registry.json"
        usage_path = data / "usage.jsonl"
        feedback_path = data / "feedback.jsonl"
        registry_path.write_text(json.dumps({"skills": {"sample": entry}}))
        usage_path.write_text("")
        feedback_path.write_text("")

        recalibrate.REGISTRY_PATH = registry_path
        recalibrate.USAGE_LOG = usage_path
        recalibrate.FEEDBACK_LOG = feedback_path
        recalibrate._shared.REGISTRY_PATH = registry_path
        old_argv = sys.argv
        sys.argv = ["recalibrate_scores.py"]
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                recalibrate.main()
        finally:
            sys.argv = old_argv

        written = json.loads(registry_path.read_text())["skills"]["sample"]
        assert written["manual_rating"] == 100
        assert written["auto_score"] == expected_auto
        assert written["composite_score"] == expected_composite


def test_autoresearch_uses_canonical_formula():
    autoresearch = load_script("autoresearch_formula_test", "autoresearch.py")
    entry = sample_entry()
    now = datetime.now(timezone.utc)
    score, breakdown = autoresearch.compute_composite(
        entry, now, Counter({"sample": 10_000}), 10_000, {}
    )
    expected_auto = compute_auto_score(
        entry, Counter({"sample": 10_000}), 10_000, {}, now
    )
    assert breakdown["auto_score"] == expected_auto
    assert score == compute_composite_score(expected_auto, 100)


def test_autoresearch_neutral_experiment_reverts_mutation():
    autoresearch = load_script("autoresearch_revert_test", "autoresearch.py")
    entry = sample_entry()

    with tempfile.TemporaryDirectory() as directory:
        registry_path = Path(directory) / "registry.json"
        registry_path.write_text(json.dumps({"skills": {"sample": entry}}))
        autoresearch.REGISTRY_PATH = registry_path

        def apply():
            registry = json.loads(registry_path.read_text())
            registry["skills"]["sample"]["transient"] = True
            registry_path.write_text(json.dumps(registry))
            return True

        def revert():
            registry = json.loads(registry_path.read_text())
            registry["skills"]["sample"].pop("transient", None)
            registry_path.write_text(json.dumps(registry))

        result = autoresearch.run_experiment(
            "sample",
            "NEUTRAL_TEST",
            apply,
            revert,
            datetime.now(timezone.utc),
            Counter(),
            1,
            {},
            False,
        )
        written = json.loads(registry_path.read_text())["skills"]["sample"]
        assert result["status"] == "neutral"
        assert "transient" not in written


def main() -> None:
    tests = [value for name, value in sorted(globals().items()) if name.startswith("test_")]
    failed = 0
    for test in tests:
        try:
            test()
            print(f"  ✓ {test.__name__}")
        except Exception as exc:
            print(f"  ✗ {test.__name__}: {exc}")
            failed += 1
    print(f"\n{len(tests) - failed}/{len(tests)} passed")
    raise SystemExit(1 if failed else 0)


if __name__ == "__main__":
    main()
