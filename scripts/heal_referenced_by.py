#!/usr/bin/env python3
"""heal_referenced_by.py — Re-derive each skill's `referenced_by` field from
the canonical sources (other skills' `depends_on` lists + `parent` fields).

Mirrors the logic in scripts/full_diagnostic_scan.py's referenced_by check:
for any skill X, X.referenced_by must include
  (a) every skill that lists X in its depends_on, AND
  (b) every skill whose parent is X.

This script makes those sets consistent. Idempotent. Run after any sync that
adds skills, or to clean up drift in existing entries.
"""

from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REG = ROOT / "data" / "registry.json"


def main():
    with open(REG) as f:
        reg = json.load(f)
    skills = reg["skills"]
    valid_ids = set(skills)

    # Re-derive: who depends_on X?
    derived_from_deps: dict[str, set[str]] = defaultdict(set)
    for sid, entry in skills.items():
        for dep in entry.get("depends_on") or []:
            if dep in valid_ids:
                derived_from_deps[dep].add(sid)

    # Re-derive: whose parent is X?
    derived_from_parent: dict[str, set[str]] = defaultdict(set)
    for sid, entry in skills.items():
        parent = entry.get("parent")
        if parent and parent in valid_ids:
            derived_from_parent[parent].add(sid)

    # Apply union; sort for determinism
    changes = 0
    for sid, entry in skills.items():
        derived = derived_from_deps[sid] | derived_from_parent[sid]
        stored = set(entry.get("referenced_by") or [])
        if derived != stored:
            entry["referenced_by"] = sorted(derived)
            changes += 1

    with open(REG, "w") as f:
        json.dump(reg, f, indent=2)
        f.write("\n")

    print(f"Healed referenced_by on {changes} skill(s).")


if __name__ == "__main__":
    main()
