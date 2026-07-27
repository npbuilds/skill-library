#!/usr/bin/env python3
"""Pure regression tests for the Firestore-native evolution rollup repair."""

from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
spec = importlib.util.spec_from_file_location(
    "aggregate_evolution_daily",
    ROOT / "scripts" / "aggregate_evolution_daily.py",
)
assert spec and spec.loader
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def test_plan_repair_identifies_missing_changed_and_stale():
    computed = [
        {"date": "2026-07-01", "count": 2, "domains": {"design": 80}},
        {"date": "2026-07-02", "count": 3, "domains": {"design": 81}},
    ]
    existing = {
        "2026-07-01": {"date": "2026-07-01", "count": 1, "domains": {"design": 80}},
        "2026-06-30": {"date": "2026-06-30", "count": 5, "domains": {}},
    }
    upserts, stale = module.plan_repair(computed, existing)
    assert [doc["date"] for doc in upserts] == ["2026-07-01", "2026-07-02"]
    assert stale == ["2026-06-30"]


def test_plan_repair_is_idempotent_and_ignores_operational_fields():
    computed = [{"date": "2026-07-01", "count": 2, "domains": {"design": 80}}]
    existing = {
        "2026-07-01": {
            **computed[0],
            "updated_at": "server timestamp not part of rollup semantics",
        }
    }
    assert module.plan_repair(computed, existing) == ([], [])


def test_backup_contains_only_exact_touched_documents():
    existing = {
        "changed": {"count": 1},
        "stale": {"count": 2},
        "untouched": {"count": 3},
    }
    with tempfile.TemporaryDirectory() as directory:
        path = module.write_backup(
            Path(directory),
            "test-project",
            1000,
            [{"date": "changed", "count": 4, "domains": {}}],
            ["stale"],
            existing,
        )
        payload = json.loads(path.read_text())
        assert payload["upsert_ids"] == ["changed"]
        assert payload["delete_ids"] == ["stale"]
        assert set(payload["before"]) == {"changed", "stale"}


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
