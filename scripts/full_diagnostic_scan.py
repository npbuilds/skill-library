#!/usr/bin/env python3
"""Full diagnostic / bug scan of the skill library.

Follows the project scan methodology:
  - Parse SKILL.md frontmatter with a real YAML parser (no regex shortcuts).
  - Independently re-derive aggregates (referenced_by, network blocks) from
    primary fields, then diff against what the registry has stored.
  - Include `parent` in broken-reference checks (not just depends_on).

Run from the project root.
"""
from __future__ import annotations

import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
REGISTRY = ROOT / "data" / "registry.json"
SKILLS_DIR = ROOT / "skills"

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*(\n|$)", re.DOTALL)


def load_registry():
    with REGISTRY.open() as f:
        return json.load(f)


def parse_frontmatter(path: Path):
    """Return (frontmatter_dict, body_text, error_or_None)."""
    try:
        text = path.read_text(encoding="utf-8")
    except Exception as e:
        return None, None, f"read_error: {e}"
    if not text.startswith("---"):
        return None, text, "missing_frontmatter"
    m = FRONTMATTER_RE.match(text)
    if not m:
        return None, text, "malformed_frontmatter_delimiters"
    raw = m.group(1)
    try:
        fm = yaml.safe_load(raw)
    except yaml.YAMLError as e:
        return None, text, f"yaml_error: {e}"
    if not isinstance(fm, dict):
        return None, text, "frontmatter_not_mapping"
    body = text[m.end():]
    return fm, body, None


def main():
    issues = defaultdict(list)  # category -> list of issues
    counts = Counter()

    registry = load_registry()
    skills = registry["skills"]
    network = registry.get("network", {})

    # --- 1. File presence + frontmatter parse ---
    skill_files = {p for p in SKILLS_DIR.rglob("SKILL.md")}
    by_relpath = {str(p.relative_to(ROOT)): p for p in skill_files}
    counts["skill_files_on_disk"] = len(skill_files)
    counts["registry_entries"] = len(skills)

    parsed = {}  # skill_id -> frontmatter
    file_to_id = {}  # rel_path -> skill_id

    # Index registry by location
    location_to_id = {}
    for sid, entry in skills.items():
        loc = entry.get("location")
        if not loc:
            issues["registry_missing_location"].append(sid)
            continue
        if loc in location_to_id:
            issues["registry_duplicate_location"].append((loc, location_to_id[loc], sid))
        location_to_id[loc] = sid

    # Files referenced in registry but missing on disk
    for sid, entry in skills.items():
        loc = entry.get("location")
        if loc and not (ROOT / loc).is_file():
            issues["registry_points_to_missing_file"].append((sid, loc))

    # Files on disk not in registry
    on_disk = {str(p.relative_to(ROOT)) for p in skill_files}
    in_reg = set(location_to_id.keys())
    orphans_on_disk = sorted(on_disk - in_reg)
    for loc in orphans_on_disk:
        issues["file_on_disk_missing_from_registry"].append(loc)

    # Parse frontmatter for every file on disk
    for rel, p in by_relpath.items():
        fm, body, err = parse_frontmatter(p)
        sid = location_to_id.get(rel)
        if err:
            issues["frontmatter_parse_error"].append((sid or rel, err))
            continue
        if sid:
            parsed[sid] = (fm, body)
            file_to_id[rel] = sid

    # --- 2. Frontmatter required fields & registry/file mismatches ---
    REQUIRED_FM = {"name", "description"}
    for sid, (fm, body) in parsed.items():
        missing = [k for k in REQUIRED_FM if k not in fm or not fm[k]]
        if missing:
            issues["frontmatter_missing_required"].append((sid, missing))
        # Compare name & description with registry
        entry = skills[sid]
        if "name" in fm and fm["name"] != entry.get("name"):
            issues["frontmatter_name_mismatch_registry"].append(
                (sid, fm.get("name"), entry.get("name"))
            )
        # description match (allow whitespace differences)
        d_fm = (fm.get("description") or "").strip()
        d_reg = (entry.get("description") or "").strip()
        if d_fm and d_reg and d_fm != d_reg:
            issues["frontmatter_description_mismatch_registry"].append(sid)

    # --- 3. Broken-reference checks (parent + depends_on + referenced_by) ---
    valid_ids = set(skills.keys())

    for sid, entry in skills.items():
        # parent
        parent = entry.get("parent")
        if parent is not None and parent != "" and parent not in valid_ids:
            issues["broken_parent_ref"].append((sid, parent))
        # self-parent
        if parent == sid:
            issues["self_parent"].append(sid)
        # depends_on
        for dep in entry.get("depends_on") or []:
            if dep not in valid_ids:
                issues["broken_depends_on_ref"].append((sid, dep))
            if dep == sid:
                issues["self_depends_on"].append(sid)
        # referenced_by
        for ref in entry.get("referenced_by") or []:
            if ref not in valid_ids:
                issues["broken_referenced_by_ref"].append((sid, ref))

    # --- 4. Independently re-derive referenced_by from depends_on ---
    derived_referenced_by = defaultdict(set)
    for sid, entry in skills.items():
        for dep in entry.get("depends_on") or []:
            if dep in valid_ids:
                derived_referenced_by[dep].add(sid)

    # Also re-derive from `parent` field — children should be in parent's referenced_by
    derived_children = defaultdict(set)
    for sid, entry in skills.items():
        parent = entry.get("parent")
        if parent and parent in valid_ids:
            derived_children[parent].add(sid)

    for sid, entry in skills.items():
        stored = set(entry.get("referenced_by") or [])
        derived = derived_referenced_by[sid] | derived_children[sid]
        missing_from_stored = derived - stored
        extra_in_stored = stored - derived
        if missing_from_stored:
            issues["referenced_by_missing_entries"].append(
                (sid, sorted(missing_from_stored))
            )
        if extra_in_stored:
            issues["referenced_by_phantom_entries"].append(
                (sid, sorted(extra_in_stored))
            )

    # --- 5. Cycle detection on parent chain ---
    def find_parent_cycle(start):
        seen = []
        cur = start
        while cur is not None:
            if cur in seen:
                return seen + [cur]
            seen.append(cur)
            cur_entry = skills.get(cur)
            if not cur_entry:
                return None
            cur = cur_entry.get("parent")
        return None

    for sid in skills:
        cyc = find_parent_cycle(sid)
        if cyc and cyc[0] == cyc[-1] and len(cyc) > 1:
            # Only report once per cycle (smallest sid representative)
            canonical = tuple(sorted(set(cyc)))
            issues.setdefault("_parent_cycles_seen", set())
            if canonical not in issues["_parent_cycles_seen"]:
                issues["_parent_cycles_seen"].add(canonical)
                issues["parent_cycle"].append(cyc)

    issues.pop("_parent_cycles_seen", None)

    # --- 6. depends_on cycles (any length) ---
    # Tarjan SCC
    index_counter = [0]
    stack = []
    lowlinks = {}
    indexes = {}
    on_stack = set()
    sccs = []

    def strongconnect(v):
        indexes[v] = index_counter[0]
        lowlinks[v] = index_counter[0]
        index_counter[0] += 1
        stack.append(v)
        on_stack.add(v)
        for w in skills[v].get("depends_on") or []:
            if w not in skills:
                continue
            if w not in indexes:
                strongconnect(w)
                lowlinks[v] = min(lowlinks[v], lowlinks[w])
            elif w in on_stack:
                lowlinks[v] = min(lowlinks[v], indexes[w])
        if lowlinks[v] == indexes[v]:
            comp = []
            while True:
                w = stack.pop()
                on_stack.discard(w)
                comp.append(w)
                if w == v:
                    break
            if len(comp) > 1:
                sccs.append(comp)

    sys.setrecursionlimit(10000)
    for v in list(skills.keys()):
        if v not in indexes:
            strongconnect(v)

    for comp in sccs:
        issues["depends_on_cycle"].append(sorted(comp))

    # --- 7. Composite score sanity ---
    for sid, entry in skills.items():
        auto = entry.get("auto_score")
        comp = entry.get("composite_score")
        manual = entry.get("manual_rating")
        if auto is not None and not (0 <= auto <= 100):
            issues["score_out_of_range"].append((sid, "auto_score", auto))
        if comp is not None and not (0 <= comp <= 100):
            issues["score_out_of_range"].append((sid, "composite_score", comp))
        if manual is None and comp is not None and auto is not None and comp != auto:
            issues["composite_score_diverges_from_auto_when_no_manual"].append(
                (sid, auto, comp)
            )

    # --- 8. Network block independent re-derivation ---
    domains = network.get("domains") or {}
    # Re-derive domains from skill locations (skills/<domain>/<name>/SKILL.md)
    derived_domains = defaultdict(list)
    for sid, entry in skills.items():
        loc = entry.get("location") or ""
        parts = loc.split("/")
        if len(parts) >= 3 and parts[0] == "skills":
            derived_domains[parts[1]].append(sid)

    if isinstance(domains, dict):
        for dom, info in domains.items():
            stored_skills = set()
            if isinstance(info, dict):
                stored_skills = set(info.get("skills") or [])
            elif isinstance(info, list):
                stored_skills = set(info)
            derived = set(derived_domains.get(dom, []))
            missing = derived - stored_skills
            extra = stored_skills - derived
            if missing:
                issues["network_domain_missing_skills"].append((dom, sorted(missing)[:10], len(missing)))
            if extra:
                issues["network_domain_phantom_skills"].append((dom, sorted(extra)[:10], len(extra)))
        # domains present in derived but not in network
        for dom in derived_domains:
            if dom not in domains and dom != "_meta":
                issues["network_missing_domain"].append((dom, len(derived_domains[dom])))

    # --- 9. Tag sanity ---
    for sid, entry in skills.items():
        tags = entry.get("tags") or []
        if not isinstance(tags, list):
            issues["tags_not_list"].append(sid)
            continue
        for t in tags:
            if not isinstance(t, str):
                issues["tag_not_string"].append((sid, t))

    # --- 10. health_status enum ---
    valid_health = {"healthy", "warning", "critical", "deprecated", "stale", "unknown"}
    for sid, entry in skills.items():
        h = entry.get("health_status")
        if h not in valid_health and h is not None:
            issues["unknown_health_status"].append((sid, h))

    # --- 11. plugin/source/type/context_mode/invocation enum-ish presence ---
    for sid, entry in skills.items():
        for f in ("type", "source", "context_mode", "invocation", "plugin", "version"):
            if entry.get(f) in (None, ""):
                issues[f"missing_field:{f}"].append(sid)

    # --- 12. Body sanity: empty body, suspicious sizes ---
    for sid, (fm, body) in parsed.items():
        if not body or not body.strip():
            issues["empty_body"].append(sid)
        else:
            words = len(body.split())
            stored = (skills[sid].get("metrics") or {}).get("body_words")
            if stored is not None and abs(words - stored) > max(20, stored * 0.10):
                issues["body_word_count_drift"].append((sid, stored, words))

    # =================== REPORT ===================
    print("=" * 70)
    print("SKILL LIBRARY — FULL DIAGNOSTIC")
    print("=" * 70)
    print(f"Registry schema_version : {registry.get('schema_version')}")
    print(f"Registry plugin_version : {registry.get('plugin_version')}")
    print(f"Registry last_scan      : {registry.get('last_scan')}")
    print(f"Skills on disk          : {counts['skill_files_on_disk']}")
    print(f"Registry entries        : {counts['registry_entries']}")
    print()

    total_issues = sum(len(v) for v in issues.values())
    print(f"TOTAL ISSUES: {total_issues}")
    print()

    # Print by severity buckets
    SEVERITY = {
        # CRITICAL: registry/disk integrity
        "registry_missing_location": "CRITICAL",
        "registry_duplicate_location": "CRITICAL",
        "registry_points_to_missing_file": "CRITICAL",
        "frontmatter_parse_error": "CRITICAL",
        "broken_parent_ref": "CRITICAL",
        "broken_depends_on_ref": "CRITICAL",
        "broken_referenced_by_ref": "CRITICAL",
        "self_parent": "CRITICAL",
        "self_depends_on": "CRITICAL",
        "parent_cycle": "CRITICAL",
        "depends_on_cycle": "CRITICAL",
        # HIGH: aggregate drift / mismatched fields
        "frontmatter_missing_required": "HIGH",
        "frontmatter_name_mismatch_registry": "HIGH",
        "frontmatter_description_mismatch_registry": "HIGH",
        "referenced_by_missing_entries": "HIGH",
        "referenced_by_phantom_entries": "HIGH",
        "network_domain_missing_skills": "HIGH",
        "network_domain_phantom_skills": "HIGH",
        "network_missing_domain": "HIGH",
        "file_on_disk_missing_from_registry": "HIGH",
        "score_out_of_range": "HIGH",
        # MEDIUM: hygiene
        "composite_score_diverges_from_auto_when_no_manual": "MEDIUM",
        "body_word_count_drift": "MEDIUM",
        "unknown_health_status": "MEDIUM",
        "empty_body": "MEDIUM",
        # LOW
        "tags_not_list": "LOW",
        "tag_not_string": "LOW",
    }
    # missing_field:* is MEDIUM
    for k in list(issues.keys()):
        if k.startswith("missing_field:"):
            SEVERITY[k] = "MEDIUM"

    order = ["CRITICAL", "HIGH", "MEDIUM", "LOW"]
    by_sev = defaultdict(list)
    for k in issues:
        by_sev[SEVERITY.get(k, "MEDIUM")].append(k)

    for sev in order:
        cats = by_sev.get(sev, [])
        if not cats:
            continue
        print(f"\n{'='*60}\n  {sev}\n{'='*60}")
        for cat in sorted(cats):
            entries = issues[cat]
            print(f"\n[{cat}]  count={len(entries)}")
            sample = entries[:8]
            for e in sample:
                print(f"   - {e}")
            if len(entries) > 8:
                print(f"   ... ({len(entries) - 8} more)")

    print()
    print("=" * 70)
    print("Severity totals:")
    for sev in order:
        c = sum(len(issues[k]) for k in by_sev.get(sev, []))
        print(f"  {sev:9s}: {c}")
    print("=" * 70)


if __name__ == "__main__":
    main()
