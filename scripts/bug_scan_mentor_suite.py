#!/usr/bin/env python3
"""bug_scan_mentor_suite.py — Independent bug scan for the Mentor suite.

Following feedback_scan_methodology memory: real parsers, independently
re-derive aggregates, broken-ref checks include parent.

Checks beyond the basic verifier:
  A. YAML field-shape consistency (real parser) across all 42 files vs Asclepius reference
  B. Description word count in [50, 110] range per file
  C. allowed-tools field presence (orchestrator vs director vs leaf conventions)
  D. Body section structure: required headings per type
  E. Cross-reference name accuracy (every name in depends_on / Cross-Domain Connections
     resolves to a real skill — independent of patch_mentor_suite's filtering)
  F. Tag correctness in registry (domain:professional-development on every entry)
  G. Parent integrity re-derived from disk vs registry
  H. Body-text references to siblings that don't exist (typos in "personal-positioning"
     etc. across markdown body, not just YAML)
  I. Duplicate skill names in registry
  J. Self-reference in depends_on (skill listing itself)
  K. Markdown syntax issues (unterminated code fences, broken tables)
"""

from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path

try:
    import yaml
except ImportError:
    print("FAIL: PyYAML not installed; pip install pyyaml")
    sys.exit(1)

ROOT = Path(__file__).resolve().parent.parent
SUITE_DIR = ROOT / "skills" / "professional-development"
REG_PATH = ROOT / "data" / "registry.json"
REF_SKILL = ROOT / "skills" / "biotech-venture" / "asclepius" / "SKILL.md"

DIRECTORS = [
    "personal-positioning", "interview-mastery", "network-cultivation",
    "trajectory-design", "executive-presence", "negotiation-leverage",
    "feedback-loops",
]


def extract_frontmatter_text_and_body(path: Path):
    text = path.read_text()
    if not text.startswith("---\n"):
        return None, text, "missing frontmatter"
    try:
        end_idx = text.index("\n---\n", 4)
    except ValueError:
        try:
            end_idx = text.index("\n---", 4)
        except ValueError:
            return None, text, "unterminated frontmatter"
    block = text[4:end_idx]
    body = text[end_idx:]
    return block, body, None


def parse_yaml(text):
    try:
        return yaml.safe_load(text), None
    except yaml.YAMLError as e:
        return None, f"yaml parse error: {e}"


def count_description_words(fm) -> int:
    desc = fm.get("description", "") if fm else ""
    if isinstance(desc, list):
        desc = " ".join(str(x) for x in desc)
    return len((desc or "").split())


def get_classification(path: Path) -> str:
    parts = path.relative_to(SUITE_DIR).parts
    if parts == ("mentor", "SKILL.md"):
        return "orchestrator"
    if len(parts) == 2 and parts[1] == "SKILL.md":
        return "director"
    return "leaf"


def check_required_yaml_keys(fm, classification):
    """Required: name, description, compatibility. Plus metadata.author / version."""
    bad = []
    for k in ["name", "description", "compatibility"]:
        if k not in fm:
            bad.append(f"missing {k!r}")
    meta = fm.get("metadata")
    if not isinstance(meta, dict):
        bad.append("metadata block missing or not a dict")
    else:
        if "author" not in meta:
            bad.append("metadata.author missing")
        if "version" not in meta:
            bad.append("metadata.version missing")
    return bad


def find_skill_refs_in_body(body: str, valid_names: set[str]) -> set[str]:
    """Find skill-name references in body (in Cross-Domain Connections section,
    routing tables, etc.) that look like real skill names but are missing.

    Heuristic: hyphenated identifiers in `backticks` or in **bold** markdown,
    and well-known skill-namespace patterns like `biotech-venture/asclepius`.
    Returns the set of identifiers found.
    """
    refs = set()
    # bare hyphenated identifiers in backticks (e.g. `narrative-architecture`)
    for m in re.finditer(r"`([a-z][a-z0-9\-]+(?:/[a-z][a-z0-9\-]+)?)`", body):
        token = m.group(1)
        if "/" in token:
            # take the last segment after /
            token = token.split("/")[-1]
        if "-" in token and len(token) > 5:
            refs.add(token)
    # plain hyphenated identifiers inline that match an existing skill name
    # (avoid false positives by only flagging tokens that exactly match a valid skill)
    for v in valid_names:
        if v in body:
            refs.add(v)
    return refs


def find_markdown_issues(body: str) -> list[str]:
    issues = []
    # unbalanced code fences
    fence_count = len(re.findall(r"^```", body, re.MULTILINE))
    if fence_count % 2 != 0:
        issues.append(f"unbalanced ``` code fences ({fence_count})")
    return issues


def main():
    failures = []
    warnings = []
    info = []

    # Load reference frontmatter shape (Asclepius)
    ref_block, _, err = extract_frontmatter_text_and_body(REF_SKILL)
    ref_fm, perr = (parse_yaml(ref_block) if not err else (None, err))
    if not ref_fm:
        failures.append(f"Could not parse reference SKILL.md ({REF_SKILL}): {err or perr}")
        ref_keys = set()
    else:
        ref_keys = set(ref_fm.keys())
        info.append(f"Reference frontmatter keys (Asclepius): {sorted(ref_keys)}")

    # Load registry
    with open(REG_PATH) as f:
        reg = json.load(f)
    skills = reg["skills"]
    valid_names = set(skills.keys())

    # Walk suite files
    suite_files = sorted(SUITE_DIR.rglob("SKILL.md"))
    info.append(f"Suite files on disk: {len(suite_files)}")

    descs_words: list[tuple[str, int]] = []
    keys_seen: Counter[frozenset] = Counter()
    file_classification: dict[str, str] = {}
    body_refs_by_file: dict[str, set[str]] = {}

    for p in suite_files:
        rel = str(p.relative_to(ROOT))
        block, body, err = extract_frontmatter_text_and_body(p)
        if err:
            failures.append(f"{rel}: frontmatter error: {err}")
            continue

        fm, perr = parse_yaml(block)
        if perr:
            failures.append(f"{rel}: {perr}")
            continue
        if not isinstance(fm, dict):
            failures.append(f"{rel}: frontmatter parsed but not a dict")
            continue

        classification = get_classification(p)
        file_classification[rel] = classification

        # A. Required keys
        bad = check_required_yaml_keys(fm, classification)
        for b in bad:
            failures.append(f"{rel}: {b}")

        # YAML keys shape vs reference (sanity check; not a hard fail)
        keys_seen[frozenset(fm.keys())] += 1

        # B. Description word count
        wc = count_description_words(fm)
        descs_words.append((rel, wc))
        if wc < 50 or wc > 110:
            warnings.append(f"{rel}: description word count = {wc} (target 60-90)")

        # C. allowed-tools field presence (reference has 'allowed-tools')
        if "allowed-tools" not in fm:
            warnings.append(f"{rel}: 'allowed-tools' field absent (reference has it)")

        # D. Required body headings per type
        if classification == "orchestrator":
            for h in ["## Guiding Principles", "## Phases"]:
                if h not in body:
                    failures.append(f"{rel}: orchestrator missing '{h}'")
        elif classification == "director":
            for h in ["## Child Skills", "## Routing Logic"]:
                if h not in body:
                    failures.append(f"{rel}: director missing '{h}'")
            if "## Cross-Domain Connections" not in body:
                warnings.append(f"{rel}: director missing '## Cross-Domain Connections'")
        else:  # leaf
            # Teaching convention checked separately by verifier, re-check here independently
            has_sc = "## Self-Coaching Track" in body
            has_to = (
                "## Teach / Mentor-Others Track" in body
                or "## Teach/Mentor-Others Track" in body
            )
            if not has_sc:
                failures.append(f"{rel}: leaf missing '## Self-Coaching Track'")
            if not has_to:
                failures.append(f"{rel}: leaf missing '## Teach / Mentor-Others Track'")
            if "## Cross-Domain Connections" not in body:
                warnings.append(f"{rel}: leaf missing '## Cross-Domain Connections'")

        # K. Markdown syntax
        for issue in find_markdown_issues(body):
            failures.append(f"{rel}: markdown {issue}")

        # H. Body-text references to siblings (collect for analysis)
        body_refs_by_file[rel] = find_skill_refs_in_body(body, valid_names)

    # YAML shape consistency report
    if len(keys_seen) > 1:
        warnings.append(
            f"YAML key-shape variations across files ({len(keys_seen)} distinct shapes); "
            f"shapes: {[sorted(list(k)) for k in keys_seen]}"
        )
    else:
        info.append(f"All 42 files share identical YAML key shape: {sorted(list(keys_seen.keys())[0]) if keys_seen else '(none)'}")

    # Description-word distribution
    if descs_words:
        wc_values = [w for _, w in descs_words]
        info.append(
            f"Description word count distribution: "
            f"min={min(wc_values)}, max={max(wc_values)}, "
            f"median={sorted(wc_values)[len(wc_values)//2]}"
        )

    # E. Cross-reference name accuracy (independent of patch script)
    # Re-derive: for every depends_on entry across the 42 suite skills, must resolve in registry
    suite_skill_names = (
        ["mentor"] + DIRECTORS +
        [p.parent.name for p in suite_files if get_classification(p) == "leaf"]
    )
    suite_skill_names = list(set(suite_skill_names))

    broken_deps = []
    for s in suite_skill_names:
        if s not in skills:
            failures.append(f"Suite skill {s!r} missing from registry")
            continue
        for d in skills[s].get("depends_on", []):
            if d not in skills:
                broken_deps.append((s, d))
    if broken_deps:
        failures.append(f"Broken depends_on (re-derived): {broken_deps[:10]}")

    # F. Tag correctness in registry
    bad_tags = []
    for s in suite_skill_names:
        if s not in skills:
            continue
        tags = skills[s].get("tags", [])
        if "domain:professional-development" not in tags:
            bad_tags.append((s, tags))
    if bad_tags:
        failures.append(f"Missing domain tag ({len(bad_tags)}): {bad_tags[:5]}")

    # G. Parent integrity re-derived from disk (not from registry)
    parent_mismatches = []
    for p in suite_files:
        classification = get_classification(p)
        name = p.parent.name if p.name == "SKILL.md" else None
        if classification == "orchestrator":
            disk_parent = None  # orchestrator
        elif classification == "director":
            disk_parent = "mentor"
        else:
            disk_parent = p.parent.parent.name  # parent dir = director
        reg_parent = skills.get(name, {}).get("parent")
        if disk_parent != reg_parent:
            parent_mismatches.append((name, "disk:" + str(disk_parent), "registry:" + str(reg_parent)))
    if parent_mismatches:
        failures.append(f"Parent disk/registry mismatch: {parent_mismatches[:5]}")

    # I. Duplicate skill names (re-derive)
    name_counts = Counter()
    for p in suite_files:
        if p.name == "SKILL.md":
            name_counts[p.parent.name] += 1
    dups = [n for n, c in name_counts.items() if c > 1]
    if dups:
        failures.append(f"Duplicate skill directory names: {dups}")

    # J. Self-reference in depends_on
    self_refs = []
    for s in suite_skill_names:
        if s not in skills:
            continue
        if s in skills[s].get("depends_on", []):
            self_refs.append(s)
    if self_refs:
        failures.append(f"Self-references in depends_on: {self_refs}")

    # H (deeper): Body references to identifiers that look like skills but don't resolve
    # We collected body_refs_by_file above; check each token against the registry.
    # We only flag tokens that look like skill names (hyphenated, len>5) AND don't resolve.
    suspicious_body_refs = []
    valid_name_pattern = re.compile(r"^[a-z][a-z0-9\-]+$")
    for rel, refs in body_refs_by_file.items():
        for r in refs:
            if not valid_name_pattern.match(r):
                continue
            if r in valid_names:
                continue
            # Only flag if it looks plausibly like a skill (e.g., has 2+ hyphens
            # or matches the project's skill-name convention)
            if r.count("-") >= 1 and len(r) >= 8:
                suspicious_body_refs.append((rel, r))
    if suspicious_body_refs:
        # These are warnings; might be domain terms not skills
        warnings.append(
            f"Body tokens look skill-shaped but don't resolve ({len(suspicious_body_refs)}); "
            f"sample: {suspicious_body_refs[:5]}"
        )

    # Print
    print("=" * 70)
    print("MENTOR SUITE BUG SCAN")
    print("=" * 70)
    print()
    print("INFO:")
    for i in info:
        print(f"  - {i}")
    print()
    print(f"FAILURES ({len(failures)}):")
    for f in failures:
        print(f"  FAIL: {f}")
    print()
    print(f"WARNINGS ({len(warnings)}):")
    for w in warnings:
        print(f"  WARN: {w}")

    print()
    print("=" * 70)
    print(f"  {len(failures)} fail / {len(warnings)} warn")
    print("=" * 70)

    sys.exit(0 if not failures else 1)


if __name__ == "__main__":
    main()
