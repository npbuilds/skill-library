#!/usr/bin/env python3
"""
test_migrate_to_firestore.py — Pass-through smoke test for the Firestore migration.

Verifies that unknown fields on skills and at the top-level of registry both
reach the migration's output, so future schema additions land in Firestore
without code changes.

Run: python3 scripts/test_migrate_to_firestore.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from migrate_to_firestore import build_skill_docs, build_meta_doc


SYNTHETIC_REGISTRY = {
    "schema_version": 2,
    "plugin_version": "1.0.0",
    "last_scan": "2026-05-16T00:00:00Z",
    "_test_unknown_top_level": "passthrough_value",
    "network": {"domains": {"test-domain": ["sample-skill"]}},
    "skills": {
        "sample-skill": {
            "name": "sample-skill",
            "type": "knowledge",
            "_test_passthrough": True,
        },
    },
}


def test_skill_doc_passthrough():
    docs = build_skill_docs(SYNTHETIC_REGISTRY)
    assert len(docs) == 1
    doc = docs[0]
    assert doc["domain"] == "test-domain"
    assert doc.get("_test_passthrough") is True, (
        f"unknown skill field dropped; doc keys: {sorted(doc.keys())}"
    )


def test_meta_doc_passthrough():
    meta = build_meta_doc(SYNTHETIC_REGISTRY)
    assert meta["skill_count"] == 1
    assert meta["network_domains"] == {"test-domain": ["sample-skill"]}
    assert meta.get("_test_unknown_top_level") == "passthrough_value", (
        f"unknown top-level field dropped; meta keys: {sorted(meta.keys())}"
    )
    assert "skills" not in meta and "network" not in meta


def main():
    tests = [test_skill_doc_passthrough, test_meta_doc_passthrough]
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
