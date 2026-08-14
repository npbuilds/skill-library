#!/usr/bin/env python3
"""Regression tests for the Mentor-suite registry patch.

Guards against the DEPS-vs-registry drift that made patch_mentor_suite.py
unsafe to re-run (its table predated the parent-strip convention, so a rerun
rewrote all 43 depends_on lists and reintroduced deliberately-removed edges).
"""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "scripts" / "patch_mentor_suite.py"
SPEC = importlib.util.spec_from_file_location("patch_mentor_suite", SCRIPT)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def _registry_skills() -> dict:
    return json.loads((ROOT / "data" / "registry.json").read_text())["skills"]


def test_all_deps_targets_resolve():
    skills = _registry_skills()
    for name, declared in MODULE.DEPS.items():
        assert name in skills, f"{name} in DEPS but not in registry"
        dead = [d for d in declared if d not in skills]
        assert not dead, f"{name} declares unresolvable deps: {dead}"


def test_committed_registry_matches_declared_mentor_edges():
    skills = _registry_skills()
    known = set(skills)
    for name, declared in MODULE.DEPS.items():
        expected = MODULE.desired_dependencies(skills[name], declared, known)
        actual = sorted(skills[name].get("depends_on") or [])
        assert actual == expected, (
            f"{name} dependency drift: {actual} != {expected} "
            "(reconcile DEPS with data/registry.json)"
        )


def test_parent_overrides_hold():
    skills = _registry_skills()
    assert skills["mentor"].get("parent") is None
    for d in MODULE.DIRECTORS:
        assert skills[d].get("parent") == "mentor", (
            f"{d} parent is {skills[d].get('parent')!r}, expected 'mentor'"
        )


def test_no_mutual_pairs_in_canonical_edges():
    """depends_on is a directional DAG (STYLE_GUIDE #6) — no A↔B pairs."""
    skills = _registry_skills()
    known = set(skills)
    canonical = {
        name: set(MODULE.desired_dependencies(skills[name], declared, known))
        for name, declared in MODULE.DEPS.items()
    }
    mutual = [
        tuple(sorted([a, b]))
        for a, deps in canonical.items()
        for b in deps
        if b in canonical and a in canonical[b]
    ]
    assert not mutual, f"mutual dependency pairs in DEPS: {sorted(set(mutual))}"


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
