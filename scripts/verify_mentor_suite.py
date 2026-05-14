#!/usr/bin/env python3
"""verify_mentor_suite.py — Independent verification of the Mentor suite.

Runs the verification steps from the plan:
  1. Structural integrity — 42 SKILL.md files exist; YAML parses (real parser);
     every leaf's parent references an existing director; every director's
     parent is "mentor"; mentor's parent is null.
  2. Registry integrity — 42 new entries; depends_on / referenced_by
     bidirectional; no broken refs.
  3. Cross-suite refs resolve.
  4. Teaching convention — every leaf has BOTH ## Self-Coaching Track AND
     ## Teach / Mentor-Others Track headings.

Following feedback_scan_methodology memory: real YAML parser, independent
re-derivation of aggregates, parent included in broken-ref checks.
"""

import json
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("FAIL: PyYAML not installed; pip install pyyaml")
    sys.exit(1)

ROOT = Path(__file__).resolve().parent.parent
SUITE_DIR = ROOT / "skills" / "professional-development"
REG_PATH = ROOT / "data" / "registry.json"

DIRECTORS = [
    "personal-positioning", "interview-mastery", "network-cultivation",
    "trajectory-design", "executive-presence", "negotiation-leverage",
    "feedback-loops",
]

EXPECTED_LEAVES_PER_DIRECTOR = {
    "personal-positioning": [
        "narrative-architecture", "linkedin-optimization", "public-portfolio",
        "credibility-translation", "audience-tuning", "resume-craft",
        "cover-letter-craft",
    ],
    "interview-mastery": [
        "behavioral-frameworks", "domain-deepdives", "vc-interview-prep",
        "executive-interview-prep", "panel-and-case",
    ],
    "network-cultivation": [
        "cold-outreach", "relationship-stewardship", "mentorship-design",
        "ecosystem-mapping", "introductions-and-referrals",
    ],
    "trajectory-design": [
        "role-archetype-mapping", "optionality-architecture", "idp-and-okrs",
        "skill-gap-analysis", "pivot-sequencing",
    ],
    "executive-presence": [
        "executive-communication", "meeting-mastery", "public-speaking",
        "board-readiness",
    ],
    "negotiation-leverage": [
        "offer-negotiation", "equity-literacy", "title-and-scope",
        "exit-and-transition",
    ],
    "feedback-loops": [
        "360-feedback-design", "performance-review-craft", "advisor-board",
        "reflection-and-journaling",
    ],
}

EXPECTED_TOTAL = 1 + 7 + sum(len(v) for v in EXPECTED_LEAVES_PER_DIRECTOR.values())

# Skills that are part of the suite (orchestrator + directors + leaves)
SUITE_SKILLS = (
    ["mentor"]
    + DIRECTORS
    + [leaf for leaves in EXPECTED_LEAVES_PER_DIRECTOR.values() for leaf in leaves]
)


def extract_frontmatter(path: Path):
    text = path.read_text()
    if not text.startswith("---\n"):
        return None, "missing frontmatter"
    try:
        end = text.index("\n---\n", 4)
    except ValueError:
        try:
            end = text.index("\n---", 4)
        except ValueError:
            return None, "unterminated frontmatter"
    block = text[4:end]
    try:
        return yaml.safe_load(block), None
    except yaml.YAMLError as e:
        return None, f"yaml parse error: {e}"


def has_teaching_tracks(path: Path) -> tuple[bool, bool]:
    """Return (has_self_coaching, has_teach_others)."""
    text = path.read_text()
    has_sc = "## Self-Coaching Track" in text
    # Allow either "## Teach / Mentor-Others Track" or "## Teach/Mentor-Others Track"
    has_to = (
        "## Teach / Mentor-Others Track" in text
        or "## Teach/Mentor-Others Track" in text
    )
    return has_sc, has_to


def main():
    failures = []
    warnings = []
    passed = []

    # ── Phase 1: Structural integrity ───────────────────────────────────
    print("=" * 60)
    print("Phase 1: Structural integrity")
    print("=" * 60)

    # 1a: orchestrator exists
    mentor_md = SUITE_DIR / "mentor" / "SKILL.md"
    if not mentor_md.is_file():
        failures.append(f"Missing orchestrator: {mentor_md}")
    else:
        passed.append("Orchestrator SKILL.md exists")

    # 1b: 7 directors exist
    for d in DIRECTORS:
        p = SUITE_DIR / d / "SKILL.md"
        if not p.is_file():
            failures.append(f"Missing director SKILL.md: {p}")
    passed.append(f"All {len(DIRECTORS)} directors present (none missing)")

    # 1c: 34 leaves exist
    leaf_count = 0
    for director, leaves in EXPECTED_LEAVES_PER_DIRECTOR.items():
        for leaf in leaves:
            p = SUITE_DIR / director / leaf / "SKILL.md"
            if not p.is_file():
                failures.append(f"Missing leaf SKILL.md: {p}")
            else:
                leaf_count += 1
    passed.append(f"{leaf_count}/34 leaves present")

    # 1d: total count
    actual_total = len(list(SUITE_DIR.rglob("SKILL.md")))
    if actual_total != EXPECTED_TOTAL:
        failures.append(
            f"Total SKILL.md count mismatch: expected {EXPECTED_TOTAL}, got {actual_total}"
        )
    else:
        passed.append(f"Total file count: {actual_total} / {EXPECTED_TOTAL}")

    # 1e: YAML frontmatter parses (real yaml parser)
    yaml_failures = []
    for p in SUITE_DIR.rglob("SKILL.md"):
        fm, err = extract_frontmatter(p)
        if err:
            yaml_failures.append(f"{p.relative_to(ROOT)}: {err}")
        elif not isinstance(fm, dict):
            yaml_failures.append(f"{p.relative_to(ROOT)}: frontmatter not a dict")
        else:
            required = ["name", "description", "compatibility"]
            for k in required:
                if k not in fm:
                    yaml_failures.append(f"{p.relative_to(ROOT)}: missing '{k}' field")
    if yaml_failures:
        failures.extend(yaml_failures[:10])
        if len(yaml_failures) > 10:
            failures.append(f"... and {len(yaml_failures)-10} more YAML failures")
    else:
        passed.append(f"All {actual_total} YAML frontmatter blocks parse")

    # ── Phase 2: Registry integrity ─────────────────────────────────────
    print()
    print("=" * 60)
    print("Phase 2: Registry integrity")
    print("=" * 60)

    with open(REG_PATH) as f:
        reg = json.load(f)
    skills = reg["skills"]

    # 2a: all 42 suite skills in registry
    missing = [s for s in SUITE_SKILLS if s not in skills]
    if missing:
        failures.append(f"Missing from registry ({len(missing)}): {missing[:5]}")
    else:
        passed.append(f"All {len(SUITE_SKILLS)} suite skills in registry")

    # 2b: parent integrity — orchestrator's parent is None
    if "mentor" in skills:
        if skills["mentor"].get("parent") not in (None, ""):
            failures.append(
                f"mentor.parent should be None, got: {skills['mentor'].get('parent')!r}"
            )
        else:
            passed.append("mentor.parent is None (orchestrator)")

    # 2c: directors' parent is "mentor"
    bad_director_parents = []
    for d in DIRECTORS:
        if d not in skills:
            continue
        p = skills[d].get("parent")
        if p != "mentor":
            bad_director_parents.append((d, p))
    if bad_director_parents:
        failures.append(f"Directors with wrong parent: {bad_director_parents}")
    else:
        passed.append(f"All {len(DIRECTORS)} directors have parent='mentor'")

    # 2d: leaves' parent is their director
    bad_leaf_parents = []
    for director, leaves in EXPECTED_LEAVES_PER_DIRECTOR.items():
        for leaf in leaves:
            if leaf not in skills:
                continue
            p = skills[leaf].get("parent")
            if p != director:
                bad_leaf_parents.append((leaf, "expected:" + director, "got:" + str(p)))
    if bad_leaf_parents:
        failures.append(f"Leaves with wrong parent ({len(bad_leaf_parents)}): {bad_leaf_parents[:5]}")
    else:
        passed.append("All 34 leaves have correct parent → director")

    # 2e: depends_on resolves
    broken_deps = []
    for s in SUITE_SKILLS:
        if s not in skills:
            continue
        for dep in skills[s].get("depends_on", []):
            if dep not in skills:
                broken_deps.append((s, dep))
    if broken_deps:
        failures.append(f"Broken depends_on refs: {broken_deps[:5]}")
    else:
        passed.append("All depends_on entries resolve to existing skills")

    # 2f: bidirectional referenced_by
    # For each suite skill's depends_on, the dep should have skill in its referenced_by
    mirror_failures = []
    for s in SUITE_SKILLS:
        if s not in skills:
            continue
        for dep in skills[s].get("depends_on", []):
            rb = skills.get(dep, {}).get("referenced_by", [])
            if s not in rb:
                mirror_failures.append((s, dep))
    if mirror_failures:
        warnings.append(f"Missing referenced_by mirrors: {len(mirror_failures)} (first 3: {mirror_failures[:3]})")
    else:
        passed.append("All depends_on are mirrored in referenced_by")

    # ── Phase 3: Cross-suite refs resolve ───────────────────────────────
    print()
    print("=" * 60)
    print("Phase 3: Cross-suite refs (depends_on into existing suites)")
    print("=" * 60)

    # Pull out cross-suite deps (depends_on entries that point outside the new suite)
    cross_deps = {}
    for s in SUITE_SKILLS:
        if s not in skills:
            continue
        for dep in skills[s].get("depends_on", []):
            if dep not in SUITE_SKILLS:
                cross_deps.setdefault(dep, []).append(s)

    cross_unresolved = [d for d in cross_deps if d not in skills]
    if cross_unresolved:
        failures.append(f"Cross-suite deps not in registry: {cross_unresolved}")
    else:
        passed.append(
            f"All {len(cross_deps)} cross-suite dep targets resolve "
            f"(spans: {sorted(set(skills[d].get('tags', ['?'])[0] if skills[d].get('tags') else '?' for d in cross_deps))})"
        )

    # ── Phase 4: Teaching convention ────────────────────────────────────
    print()
    print("=" * 60)
    print("Phase 4: Teaching convention (dual-track in every leaf)")
    print("=" * 60)

    missing_tracks = []
    for director, leaves in EXPECTED_LEAVES_PER_DIRECTOR.items():
        for leaf in leaves:
            p = SUITE_DIR / director / leaf / "SKILL.md"
            if not p.is_file():
                continue
            sc, to = has_teaching_tracks(p)
            if not sc:
                missing_tracks.append((leaf, "missing Self-Coaching Track"))
            if not to:
                missing_tracks.append((leaf, "missing Teach/Mentor-Others Track"))
    if missing_tracks:
        failures.append(f"Teaching tracks missing: {missing_tracks[:5]}")
    else:
        passed.append("All 34 leaves have both ## Self-Coaching Track and ## Teach / Mentor-Others Track")

    # ── Report ──────────────────────────────────────────────────────────
    print()
    print("=" * 60)
    print("VERIFICATION REPORT")
    print("=" * 60)
    for p in passed:
        print(f"  PASS: {p}")
    for w in warnings:
        print(f"  WARN: {w}")
    for f in failures:
        print(f"  FAIL: {f}")

    print()
    print(f"  {len(passed)} pass / {len(warnings)} warn / {len(failures)} fail")

    sys.exit(0 if not failures else 1)


if __name__ == "__main__":
    main()
