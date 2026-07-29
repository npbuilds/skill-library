#!/usr/bin/env python3
"""Regression tests for authoritative investing graph wiring."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "scripts" / "wire-investing-graph.py"
SPEC = importlib.util.spec_from_file_location("wire_investing_graph", SCRIPT)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def test_committed_registry_matches_declared_investing_edges():
    registry = json.loads((ROOT / "data" / "registry.json").read_text())
    skills = registry["skills"]
    for name, declared in MODULE.DEPENDENCY_MAP.items():
        assert name in skills
        expected = MODULE.desired_dependencies(skills[name], declared)
        assert skills[name].get("depends_on", []) == expected, (
            f"{name} dependency drift: "
            f"{skills[name].get('depends_on', [])} != {expected}"
        )


def test_committed_reverse_index_is_authoritative():
    registry = json.loads((ROOT / "data" / "registry.json").read_text())
    skills = registry["skills"]
    expected = MODULE.derive_referenced_by(skills)
    actual = {
        name: sorted(entry.get("referenced_by") or [])
        for name, entry in skills.items()
    }
    assert actual == expected


def test_reverse_index_drops_stale_edges_and_includes_parent():
    skills = {
        "root": {
            "parent": None,
            "depends_on": [],
            "referenced_by": ["child", "stale"],
        },
        "child": {
            "parent": "root",
            "depends_on": [],
            "referenced_by": [],
        },
        "stale": {
            "parent": None,
            "depends_on": [],
            "referenced_by": [],
        },
    }
    assert MODULE.derive_referenced_by(skills) == {
        "root": ["child"],
        "child": [],
        "stale": [],
    }


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
