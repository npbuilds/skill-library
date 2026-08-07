#!/usr/bin/env python3
"""Regression tests for the aggregate-only evolution pipeline."""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from audit_evolution_daily import audit_documents, plan_repairs  # noqa: E402
from check_firestore_divergence import strict_sync_error  # noqa: E402
from build_infra_manifest import build_manifest  # noqa: E402
from evolution_daily import (  # noqa: E402
    build_daily_aggregate,
    build_historical_aggregates,
    validate_daily_document,
)


REGISTRY = {
    "network": {
        "domains": {
            "design": ["alpha", "beta"],
            "research": ["gamma"],
        }
    },
    "skills": {
        "alpha": {"composite_score": 80},
        "beta": {"composite_score": 90},
        "gamma": {"composite_score": 0},
        "unmapped": {"composite_score": 70},
    },
}


def test_builds_one_daily_document_directly_from_registry():
    document = build_daily_aggregate(REGISTRY, "2026-08-04")
    assert document == {
        "date": "2026-08-04",
        "count": 4,
        "domains": {"design": 85.0, "research": 0.0, "unknown": 70.0},
    }


def test_builder_is_deterministic_and_does_not_emit_skill_rows():
    first = build_daily_aggregate(REGISTRY, "2026-08-04")
    second = build_daily_aggregate(REGISTRY, "2026-08-04")
    assert first == second
    assert set(first) == {"date", "count", "domains"}
    assert "skills" not in first


def test_runtime_paths_do_not_write_raw_evolution_history():
    runtime_paths = [
        ROOT / "scripts" / "snapshot_to_firestore.py",
        ROOT / "scripts" / "migrate_to_firestore.py",
        ROOT / "hooks" / "skill-file-watcher.sh",
        ROOT / "scripts" / "skillopt" / "optimize.py",
    ]
    combined = "\n".join(path.read_text() for path in runtime_paths)
    assert 'collection("evolution")' not in combined
    assert "collection('evolution')" not in combined
    assert "snapshot_evolution.py" not in combined
    assert "EVOLUTION_LOG" not in combined


def test_rejects_invalid_registry_and_date():
    invalid_cases = [
        ({"skills": []}, "2026-08-04"),
        (REGISTRY, "08/04/2026"),
        ({**REGISTRY, "skills": {"bad": {"composite_score": "80"}}}, "2026-08-04"),
        ({**REGISTRY, "skills": {"bad": {"composite_score": True}}}, "2026-08-04"),
        ({**REGISTRY, "skills": {"bad": {}}}, "2026-08-04"),
    ]
    for registry, day in invalid_cases:
        try:
            build_daily_aggregate(registry, day)
            raised = False
        except ValueError:
            raised = True
        assert raised


def test_daily_document_validation():
    valid = build_daily_aggregate(REGISTRY, "2026-08-04")
    assert validate_daily_document("2026-08-04", valid) == []
    invalid = {
        "date": "wrong",
        "count": -1,
        "domains": {"design": 101, "": True},
    }
    errors = validate_daily_document("not-a-date", invalid)
    assert len(errors) == 6, errors


def test_collection_audit_reports_only_invalid_documents():
    documents = {
        "2026-08-04": build_daily_aggregate(REGISTRY, "2026-08-04"),
        "2026-08-05": {"date": "2026-08-05", "count": "four", "domains": {}},
    }
    errors = audit_documents(documents)
    assert errors == ["2026-08-05: count must be a non-negative integer"]
    assert audit_documents({}) == ["evolution_daily: collection is empty"]


def test_historical_rebuild_uses_latest_row_once_per_skill_and_date():
    raw = [
        {"skill": "alpha", "date": "2026-08-04T08:00:00+00:00", "composite_score": 70},
        {"skill": "alpha", "date": "2026-08-04T12:00:00+00:00", "composite_score": 90},
        {"skill": "beta", "date": "2026-08-04T09:00:00Z", "composite_score": 80},
        {"skill": "gamma", "date": "2026-08-05T09:00:00+00:00", "composite_score": 50},
    ]
    assert build_historical_aggregates(raw, REGISTRY) == [
        {"date": "2026-08-04", "count": 2, "domains": {"design": 85.0}},
        {"date": "2026-08-05", "count": 1, "domains": {"research": 50.0}},
    ]


def test_repair_plan_changes_only_raw_backed_dates():
    computed = [{"date": "2026-08-04", "count": 2, "domains": {"design": 85.0}}]
    existing = {
        "2026-08-04": {"date": "2026-08-04", "count": 3, "domains": {"design": 80}},
        "2026-08-05": {"date": "2026-08-05", "count": 4, "domains": {}},
    }
    assert plan_repairs(computed, existing) == computed
    assert plan_repairs(computed, {**existing, "2026-08-04": computed[0]}) == []


def test_strict_sync_gate_requires_exact_head_before_writes():
    assert strict_sync_error("head", "head") is None
    assert strict_sync_error("head", None)
    assert strict_sync_error("head", "older")

    workflow = (ROOT / ".github" / "workflows" / "daily-firestore.yml").read_text()
    check_at = workflow.index("check_firestore_divergence.py")
    aggregate_at = workflow.index("snapshot_to_firestore.py")
    health_at = workflow.index("health-report.py")
    assert "--require-head" in workflow
    assert check_at < aggregate_at < health_at

    audit_source = (ROOT / "scripts" / "audit_evolution_daily.py").read_text()
    assert "if args.push:" in audit_source
    assert "strict_sync_error(head, synced_sha)" in audit_source


def test_retired_raw_collection_remains_visible_until_deletion():
    manifest = build_manifest()
    assert "evolution" in manifest["firestore_collections"]
    assert manifest["retired_firestore_collections"] == ["evolution"]
    infra = (ROOT / "app" / "infra.html").read_text()
    assert "retired_firestore_collections" in infra
    assert "pending verified backup and controlled deletion" in infra


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
