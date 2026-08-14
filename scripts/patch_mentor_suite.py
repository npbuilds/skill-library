#!/usr/bin/env python3
"""patch_mentor_suite.py — Post-sync patches for the Mentor suite.

After scripts/sync-registry.py --apply, this script:
  1. Sets mentor's parent to null (orchestrator)
  2. Sets each director's parent to "mentor"
  3. Populates depends_on lists per the plan's cross-suite integration table
  4. Rebuilds the referenced_by reverse index from the full graph

DEPS lists may include a skill's own parent for readability; the apply pass
strips it (same convention as scripts/wire-investing-graph.py), because the
`parent` field is the canonical hierarchy encoding (STYLE_GUIDE #7) and
echoing it in depends_on creates cycles.

Run:
    python3 scripts/patch_mentor_suite.py          # dry-run
    python3 scripts/patch_mentor_suite.py --apply  # write registry.json
"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REG = ROOT / "data" / "registry.json"

# Map of skill_name -> list of depends_on entries
DEPS = {
    # Orchestrator
    "mentor": [],

    # Directors
    "personal-positioning": ["mentor"],
    "interview-mastery": ["mentor"],
    "network-cultivation": ["mentor"],
    "trajectory-design": ["mentor"],
    "executive-presence": ["mentor"],
    "negotiation-leverage": ["mentor"],
    "feedback-loops": ["mentor"],

    # Standalone action leaves (parent: mentor via sync-registry inference).
    "ariadne": ["vault-writer"],

    # personal-positioning leaves
    "narrative-architecture": [
        "personal-positioning", "brand-foundations", "brand-voice", "minto-scqa"
    ],
    "linkedin-optimization": [
        "personal-positioning", "narrative-architecture", "credibility-translation",
        "audience-tuning", "prose-editor", "audience-classifier"
    ],
    "public-portfolio": [
        "personal-positioning", "narrative-architecture", "linkedin-optimization",
        "credibility-translation", "prose-editor", "asclepius", "the-loom", "spelunker"
    ],
    "credibility-translation": [
        "personal-positioning", "narrative-architecture", "asclepius", "audience-classifier"
    ],
    "audience-tuning": [
        "personal-positioning", "audience-classifier", "narrative-architecture",
        "credibility-translation", "cover-letter-craft", "behavioral-frameworks",
        "prose-editor"
    ],
    "resume-craft": [
        "personal-positioning", "narrative-architecture", "credibility-translation",
        "audience-tuning", "linkedin-optimization", "cover-letter-craft", "prose-editor",
        "asclepius"
    ],
    "cover-letter-craft": [
        "personal-positioning", "spelunker", "credibility-translation",
        "narrative-architecture", "bluf-shaper", "audience-classifier", "prose-editor",
        "asclepius"
    ],

    # interview-mastery leaves
    "behavioral-frameworks": [
        "interview-mastery", "credibility-translation", "narrative-architecture",
        "minto-scqa", "asclepius"
    ],
    "domain-deepdives": [
        "interview-mastery", "asclepius", "clinical-development", "regulatory-strategy",
        "asset-valuation", "probability-of-success", "deal-synthesis", "vc-interview-prep",
        "executive-interview-prep", "behavioral-frameworks", "spelunker",
        "credibility-translation", "the-loom"
    ],
    "vc-interview-prep": [
        "interview-mastery", "asclepius", "deal-synthesis", "probability-of-success",
        "asset-valuation", "regulatory-strategy", "behavioral-frameworks",
        "credibility-translation", "cover-letter-craft", "spelunker", "ecosystem-mapping"
    ],
    "executive-interview-prep": [
        "interview-mastery", "executive-communication", "behavioral-frameworks",
        "asclepius", "credibility-translation", "role-archetype-mapping"
    ],
    "panel-and-case": [
        "interview-mastery", "vc-interview-prep", "executive-interview-prep",
        "behavioral-frameworks", "domain-deepdives", "asclepius", "deal-synthesis",
        "asset-valuation", "executive-communication", "bluf-shaper", "minto-scqa"
    ],

    # network-cultivation leaves
    "cold-outreach": [
        "network-cultivation", "relationship-stewardship", "ecosystem-mapping",
        "credibility-translation", "cover-letter-craft", "prose-editor", "spelunker"
    ],
    "relationship-stewardship": [
        "network-cultivation", "ecosystem-mapping", "the-loom", "prose-editor"
    ],
    "mentorship-design": [
        "network-cultivation", "cold-outreach", "relationship-stewardship",
        "ecosystem-mapping", "advisor-board", "role-archetype-mapping", "the-loom"
    ],
    "ecosystem-mapping": [
        "network-cultivation", "spelunker", "source-triangulator", "cover-letter-craft",
        "asclepius", "the-loom"
    ],
    "introductions-and-referrals": [
        "network-cultivation", "ecosystem-mapping", "relationship-stewardship",
        "cold-outreach", "credibility-translation", "narrative-architecture",
        "audience-tuning", "prose-editor"
    ],

    # trajectory-design leaves
    "role-archetype-mapping": [
        "trajectory-design", "narrative-architecture", "ecosystem-mapping",
        "vc-interview-prep"
    ],
    "optionality-architecture": [
        "trajectory-design", "role-archetype-mapping", "archon", "the-loom"
    ],
    "idp-and-okrs": ["trajectory-design", "role-archetype-mapping", "the-loom"],
    "skill-gap-analysis": [
        "trajectory-design", "role-archetype-mapping", "idp-and-okrs", "advisor-board",
        "public-portfolio"
    ],
    "pivot-sequencing": [
        "trajectory-design", "role-archetype-mapping", "skill-gap-analysis",
        "optionality-architecture", "idp-and-okrs", "public-portfolio", "ecosystem-mapping"
    ],

    # executive-presence leaves
    "executive-communication": [
        "executive-presence", "bluf-shaper", "executive-distiller", "minto-scqa",
        "audience-classifier", "cover-letter-craft", "prose-editor"
    ],
    "meeting-mastery": [
        "executive-presence", "executive-communication", "board-readiness",
        "panel-and-case", "bluf-shaper", "audience-classifier", "the-loom"
    ],
    "public-speaking": [
        "executive-presence", "executive-communication", "meeting-mastery",
        "public-portfolio", "audience-tuning", "minto-scqa", "prose-editor"
    ],
    "board-readiness": [
        "executive-presence", "executive-communication", "equity-literacy",
        "executive-interview-prep", "archon", "asclepius", "role-archetype-mapping"
    ],

    # negotiation-leverage leaves
    "offer-negotiation": [
        "negotiation-leverage", "optionality-architecture", "archon", "bluf-shaper"
    ],
    "equity-literacy": [
        "negotiation-leverage", "offer-negotiation", "archon", "asset-valuation",
        "optionality-architecture"
    ],
    "title-and-scope": [
        "negotiation-leverage", "offer-negotiation", "equity-literacy",
        "role-archetype-mapping", "optionality-architecture", "board-readiness",
        "narrative-architecture"
    ],
    "exit-and-transition": [
        "negotiation-leverage", "equity-literacy", "offer-negotiation",
        "optionality-architecture", "narrative-architecture", "relationship-stewardship"
    ],

    # feedback-loops leaves
    "360-feedback-design": [
        "feedback-loops", "advisor-board", "reflection-and-journaling",
        "skill-gap-analysis", "idp-and-okrs"
    ],
    "performance-review-craft": [
        "feedback-loops", "resume-craft", "credibility-translation", "audience-tuning",
        "360-feedback-design", "reflection-and-journaling", "idp-and-okrs", "prose-editor"
    ],
    "advisor-board": ["feedback-loops", "relationship-stewardship", "idp-and-okrs", "the-loom"],
    "reflection-and-journaling": [
        "feedback-loops", "the-loom", "advisor-board", "idp-and-okrs", "prose-editor"
    ],

}

# Director parent overrides (the auto-inference makes them parent=domain;
# we want them to be parent=mentor)
DIRECTORS = [
    "personal-positioning", "interview-mastery", "network-cultivation",
    "trajectory-design", "executive-presence", "negotiation-leverage",
    "feedback-loops",
]


def desired_dependencies(entry: dict, declared: list[str], known: set[str]) -> list[str]:
    """Return canonical capability edges: resolved, parent-stripped, sorted."""
    desired = {d for d in declared if d in known}
    parent = entry.get("parent")
    if parent:
        desired.discard(parent)
    return sorted(desired)


def derive_referenced_by(skills: dict[str, dict]) -> dict[str, list[str]]:
    """Rebuild the exact reverse index from parent and capability edges."""
    reverse: dict[str, set[str]] = {name: set() for name in skills}
    for source, entry in skills.items():
        targets = set(entry.get("depends_on") or [])
        parent = entry.get("parent")
        if parent:
            targets.add(parent)
        for target in targets:
            if target in reverse and target != source:
                reverse[target].add(source)
    return {name: sorted(referrers) for name, referrers in reverse.items()}


def main():
    dry_run = "--apply" not in sys.argv

    with open(REG) as f:
        reg = json.load(f)
    skills = reg["skills"]
    known = set(skills)

    changes: list[str] = []
    missing_deps = []

    # 1. Mentor: parent = None (orchestrator root)
    if "mentor" in skills and skills["mentor"].get("parent") is not None:
        changes.append(f"  mentor: parent {skills['mentor'].get('parent')!r} → None")
        skills["mentor"]["parent"] = None

    # 2. Directors: parent = mentor
    for d in DIRECTORS:
        if d in skills and skills[d].get("parent") != "mentor":
            changes.append(f"  {d}: parent {skills[d].get('parent')!r} → 'mentor'")
            skills[d]["parent"] = "mentor"

    # 3. depends_on for each Mentor-suite skill (canonical: parent-stripped, sorted)
    for skill_name, deps in DEPS.items():
        if skill_name not in skills:
            missing_deps.append(skill_name)
            continue
        entry = skills[skill_name]
        unresolved = [d for d in deps if d not in known]
        if unresolved:
            print(f"  WARN: {skill_name} has unresolved deps: {unresolved}")
        canonical = desired_dependencies(entry, deps, known)
        old = sorted(entry.get("depends_on") or [])
        if old != canonical:
            changes.append(f"  {skill_name}: depends_on {old} → {canonical}")
        entry["depends_on"] = canonical

    # 4. referenced_by is denormalized data. Rebuild it from the complete
    # graph so removed edges cannot survive as stale referrers.
    for target_name, referrers in derive_referenced_by(skills).items():
        entry = skills[target_name]
        if sorted(entry.get("referenced_by") or []) != referrers:
            changes.append(
                f"  {target_name}: referenced_by "
                f"{sorted(entry.get('referenced_by') or [])} → {referrers}"
            )
        entry["referenced_by"] = referrers

    if missing_deps:
        print(f"  WARN: {len(missing_deps)} skills in DEPS not in registry: {missing_deps}")

    print(f"{'DRY RUN — ' if dry_run else ''}Mentor-suite patch")
    print(f"  Skills in DEPS: {len(DEPS)}")
    print(f"  Registry modifications: {len(changes)}")
    for line in changes[:40]:
        print(line)
    if len(changes) > 40:
        print(f"  ... and {len(changes) - 40} more")

    if not dry_run:
        with open(REG, "w") as f:
            json.dump(reg, f, indent=2)
            f.write("\n")
        print("\nRegistry updated.")
    else:
        print("\nRun with --apply to write changes.")


if __name__ == "__main__":
    main()
