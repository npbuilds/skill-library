#!/usr/bin/env python3
"""sync-registry.py — Discover new skills on disk and add them to registry.json.

Usage:
    python3 scripts/sync-registry.py              # dry-run (shows what would change)
    python3 scripts/sync-registry.py --apply       # actually update registry.json

This script:
  1. Walks skills/ for every SKILL.md
  2. Extracts metadata (name, description, type) from heterogeneous formats
  3. Infers parent/domain/subdomain from directory structure
  4. Adds missing entries to registry.json
  5. Flags registry entries whose files no longer exist on disk
  6. Reports location mismatches for existing entries
"""

import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from functools import lru_cache
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = PROJECT_ROOT / "skills"
REGISTRY_PATH = PROJECT_ROOT / "data" / "registry.json"

SKIP_DIRS = {".obsidian", "references", "agents", "examples"}


def derive_referenced_by(skills: dict[str, dict]) -> dict[str, list[str]]:
    """Build the exact reverse index implied by parent and depends_on edges."""
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


@lru_cache(maxsize=1)
def _tracked_files() -> frozenset[str]:
    """POSIX-relative paths tracked by git (index + HEAD). Empty set if git fails."""
    try:
        out = subprocess.check_output(
            ["git", "-C", str(PROJECT_ROOT), "ls-files"],
            text=True,
            stderr=subprocess.DEVNULL,
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        return frozenset()
    return frozenset(out.splitlines())

# ── Metadata extraction ────────────────────────────────────────────────

def extract_yaml_frontmatter(text: str) -> dict | None:
    """Extract YAML frontmatter between --- delimiters using regex (no PyYAML dep)."""
    m = re.match(r"^---\s*\n(.*?)\n---", text, re.DOTALL)
    if not m:
        return None
    result = {}
    block = m.group(1)
    # Handle multi-line description (with > or |). The trailing newline on
    # the final line is optional — outer frontmatter regex consumes the \n
    # before the closing ---, so the last description line lacks one.
    desc_match = re.search(r"^description:\s*[>|]\s*\n((?:[ \t]+.+(?:\n|$))+)", block, re.MULTILINE)
    if desc_match:
        result["description"] = " ".join(
            line.strip() for line in desc_match.group(1).strip().split("\n")
        )
    for line in block.split("\n"):
        kv = re.match(r"^(\w[\w-]*):\s+(.+)$", line)
        if kv:
            key, val = kv.group(1).strip(), kv.group(2).strip()
            if key == "description" and "description" in result:
                continue  # Already handled multi-line
            result[key] = val
    return result if result else None


def extract_inline_metadata(text: str) -> dict:
    """Extract metadata from inline patterns like '## skill-metadata' blocks or bold labels."""
    meta = {}

    # Pattern 1: ## skill-metadata block with "- key: value" lines
    m = re.search(r"## skill-metadata\s*\n((?:- .+\n)+)", text)
    if m:
        for line in m.group(1).strip().split("\n"):
            kv = re.match(r"- ([\w-]+):\s*(.+)", line)
            if kv:
                key = kv.group(1).strip()
                val = kv.group(2).strip()
                if key == "skill-type":
                    meta["type"] = val
                elif key == "skill-id":
                    meta["skill_id"] = val
                elif key == "parent":
                    meta["parent_id"] = val

    # Pattern 2: **Type:** value  /  **Suite:** value
    for pattern, field in [
        (r"\*\*Type:\*\*\s*(\w+)", "type"),
        (r"\*\*Suite:\*\*\s*(\w+)", "suite"),
        (r"\*\*Skill Type\*\*\s*\n\*\*(\w+)\*\*", "type"),
    ]:
        m = re.search(pattern, text, re.IGNORECASE)
        if m:
            meta[field] = m.group(1).strip().lower()

    # Pattern 3: ## Skill Type\n**Knowledge**
    m = re.search(r"## Skill Type\s*\n\*\*(\w+)\*\*", text)
    if m:
        meta["type"] = m.group(1).strip().lower()

    # Extract description from ## description or ## Description section
    m = re.search(r"## [Dd]escription\s*\n(.+?)(?:\n##|\n---|\Z)", text, re.DOTALL)
    if m:
        desc = m.group(1).strip().split("\n")[0].strip()
        if desc:
            meta["description"] = desc

    return meta


def extract_description_from_header(text: str) -> str | None:
    """Fallback: grab first paragraph after the H1 header."""
    lines = text.split("\n")
    past_h1 = False
    for line in lines:
        if line.startswith("# ") and not past_h1:
            past_h1 = True
            continue
        if past_h1 and line.strip():
            # Skip if it's another header or metadata
            if line.startswith("#") or line.startswith("**") or line.startswith("---"):
                continue
            return line.strip()[:200]
    return None


def compute_metrics(text: str, skill_dir: Path) -> dict:
    """Compute the full canonical metrics block — schema mirrors
    analyze-skill.sh so downstream scorers (mcp-server/shared.py,
    autoresearch.py) see identical keys regardless of source.

    body_words counts body only (frontmatter excluded). The legacy
    body_words = len(full_text) bug is fixed here."""
    fm_match = re.match(r"^---\s*\n(.*?)\n---\s*(\n|$)", text, re.DOTALL)
    if fm_match:
        frontmatter = fm_match.group(1)
        body = text[fm_match.end():]
    else:
        frontmatter = ""
        body = text

    all_words = text.split()
    body_words = body.split()

    # description_words: words in the description: field, mirroring analyze-skill.sh
    desc_words = 0
    capture = False
    for line in frontmatter.split("\n"):
        if re.match(r"^description:", line):
            capture = True
            value = re.sub(r"^description:\s*[>|]?\s*", "", line)
            desc_words += len(value.split())
            continue
        if capture and re.match(r"^[A-Za-z_-]+:", line):
            break
        if capture:
            desc_words += len(line.split())

    # Section count: ## headings outside fenced code blocks (only body)
    section_count = 0
    in_code = False
    for line in body.split("\n"):
        if line.startswith("```"):
            in_code = not in_code
            continue
        if not in_code and line.startswith("## "):
            section_count += 1

    def _count(subdir: str) -> int:
        # Count only git-tracked files so a local apply with untracked files in this dir doesn't drift against CI's clean checkout.
        d = skill_dir / subdir
        if not d.is_dir():
            return 0
        tracked = _tracked_files()
        if not tracked:  # git unavailable — fall back to raw filesystem count
            return sum(1 for f in d.iterdir() if f.is_file() and f.name != ".gitkeep")
        return sum(
            1 for f in d.iterdir()
            if f.is_file() and f.name != ".gitkeep"
            and f.relative_to(PROJECT_ROOT).as_posix() in tracked
        )

    # Token estimate is bytes/4 (matches analyze-skill.sh's wc -c, which
    # counts bytes). UTF-8 multi-byte chars (em-dashes, curly quotes) need
    # the byte length, not Python's char count, to stay in sync.
    body_chars = len(body.encode("utf-8"))
    est_tokens_body = body_chars // 4
    est_tokens_metadata = (desc_words * 13 + 9) // 10
    est_tokens_total = est_tokens_metadata + est_tokens_body

    return {
        "word_count": len(all_words),
        "body_words": len(body_words),
        "description_words": desc_words,
        "section_count": section_count,
        "reference_files": _count("references"),
        "example_files": _count("examples"),
        "script_files": _count("scripts"),
        "template_files": _count("templates"),
        "estimated_tokens_metadata": est_tokens_metadata,
        "estimated_tokens_body": est_tokens_body,
        "estimated_tokens_total": est_tokens_total,
    }


# ── Structural inference ───────────────────────────────────────────────

TYPE_KEYWORDS = {
    "orchestrator": "orchestrator",
    "director": "director",
    "observer": "observer",
    "action": "action",
    "knowledge": "knowledge",
    "agent": "action",
}


def infer_type(name: str, text: str, meta: dict) -> str:
    """Infer skill type from metadata, name, or content."""
    # Explicit metadata wins
    if "type" in meta:
        t = meta["type"].lower()
        return TYPE_KEYWORDS.get(t, t)

    # Name-based inference
    for keyword, stype in TYPE_KEYWORDS.items():
        if keyword in name:
            return stype

    # Content-based inference. Check the orchestrator signal BEFORE the
    # director signal: orchestrators (six-eyes, neocortex, …) frequently also
    # contain a "## Routing Table" / "## Child Skills" section, and the director
    # check would otherwise win and mis-type them. That also drops them from
    # domain_orchestrators, which breaks parent inference for new skills in the
    # domain (new leaves get parent=None instead of the orchestrator). No
    # registry director uses "## phases"/"## delegate", so promoting on those
    # signals first is safe.
    text_lower = text.lower()
    # Match the orchestrator heading "## Phases" (plural). The singular
    # "## phase" collided with reference skills that document clinical-trial
    # phases (e.g. "## Phase Transition Probabilities"), mis-typing them.
    if "## delegate" in text_lower or "## phases" in text_lower:
        return "orchestrator"
    if "routing table" in text_lower or "child skills" in text_lower:
        return "director"

    return "knowledge"


def infer_structure(
    skill_path: Path,
    all_skill_dirs: set[Path] | None = None,
    domain_orchestrators: dict[str, str] | None = None,
) -> dict:
    """Infer domain, subdomain, parent from directory structure.

    The parent is the nearest ancestor directory that has its own SKILL.md.
    Organizational subdirectories (e.g., `horizontal/`, `vertical/` in the
    Collector suite) are skipped — they don't have their own SKILL.md so the
    walk passes through them looking for the next real skill above.

    If no ancestor SKILL.md exists, the skill is attributed to its domain's
    orchestrator (when one exists and isn't itself).
    """
    rel = skill_path.relative_to(SKILLS_DIR)
    parts = list(rel.parts[:-1])  # Remove SKILL.md

    info = {"domain": None, "subdomain": None, "parent": None}

    if len(parts) >= 1:
        info["domain"] = parts[0]
    if len(parts) >= 3:
        info["subdomain"] = parts[1]

    # Modern parent inference (preferred): walk up looking for an ancestor SKILL.md.
    # Falls back to the legacy heuristic when context isn't provided.
    if all_skill_dirs is not None:
        skill_dir = skill_path.parent
        current = skill_dir.parent
        skills_parent = SKILLS_DIR.parent
        while current != skills_parent and current != current.parent:
            if current in all_skill_dirs and current != skill_dir:
                info["parent"] = current.name
                return info
            current = current.parent

        # Fallback: attribute to domain orchestrator if one exists and isn't self.
        if domain_orchestrators and len(parts) >= 1:
            domain = parts[0]
            orchestrator = domain_orchestrators.get(domain)
            if orchestrator and orchestrator != skill_dir.name:
                info["parent"] = orchestrator
                return info

        return info

    # Legacy heuristic — preserved for backward compatibility on direct callers.
    if len(parts) >= 3:
        info["parent"] = parts[-2]
    elif len(parts) == 2:
        info["parent"] = parts[0] if parts[0] != parts[-1] else None
    return info


# ── Cross-reference detection ──────────────────────────────────────────

# H2/H3 headings whose body sections may contain explicit cross-skill routing.
# Conservative — only sections that describe handoffs / scope boundaries are scanned.
CROSS_REF_SECTION_KEYWORDS = (
    "scope and escalat",
    "scope boundar",
    "cross-domain",
    "cross-suite",
    "cross-axis",
    "cross-reference",
    "see also",
    "hand off",
    "hand-off",
    "escalat",  # "Escalations", "Cross-domain escalations"
    "related skills",
    "delegation",
    "routing",
)

# Matches `tokens-like-this` (single-line backtick-quoted identifiers).
_BACKTICK_REF_RE = re.compile(r"`([a-z][a-z0-9_-]+)`")
_HEADING_SPLIT_RE = re.compile(r"^(##+\s+[^\n]+)", re.MULTILINE)


def detect_cross_references(text: str, known_skill_names: set[str]) -> set[str]:
    """Find backtick-quoted skill names in escalation/scope sections.

    Conservative by design:
      - Only matches inside H2/H3 sections whose headings include a routing keyword.
      - Only matches tokens that are known registered skill names.
      - Ignores backtick uses in code blocks (those are dropped by the heading-split).
    """
    refs: set[str] = set()
    sections = _HEADING_SPLIT_RE.split(text)
    # split() yields: [preamble, heading1, body1, heading2, body2, ...]
    for i in range(1, len(sections), 2):
        heading = sections[i].lower()
        body = sections[i + 1] if i + 1 < len(sections) else ""
        if not any(kw in heading for kw in CROSS_REF_SECTION_KEYWORDS):
            continue
        for m in _BACKTICK_REF_RE.finditer(body):
            token = m.group(1)
            if token in known_skill_names:
                refs.add(token)
    return refs


# ── Main sync logic ────────────────────────────────────────────────────

def discover_skills() -> dict[str, dict]:
    """Walk disk and return {name: entry_data} for every SKILL.md found."""
    discovered = {}

    # First pass — collect every SKILL.md location and identify the orchestrator
    # per domain. Needed so `infer_structure` can resolve parents that skip
    # organizational subdirectories (e.g., `horizontal/`, `vertical/`).
    candidate_skill_mds: list[Path] = []
    all_skill_dirs: set[Path] = set()
    for skill_md in SKILLS_DIR.rglob("SKILL.md"):
        if any(part in SKIP_DIRS for part in skill_md.relative_to(SKILLS_DIR).parts[:-1]):
            continue
        candidate_skill_mds.append(skill_md)
        all_skill_dirs.add(skill_md.parent)

    domain_orchestrators: dict[str, str] = {}
    for skill_md in candidate_skill_mds:
        text = skill_md.read_text(errors="replace")
        yaml_meta = extract_yaml_frontmatter(text) or {}
        inline_meta = extract_inline_metadata(text)
        name = (yaml_meta.get("name") or "").strip() or skill_md.parent.name
        stype = infer_type(name, text, {**inline_meta, **yaml_meta})
        if stype == "orchestrator":
            rel_parts = skill_md.relative_to(SKILLS_DIR).parts
            if len(rel_parts) >= 1:
                domain_orchestrators[rel_parts[0]] = name

    # Second pass — build registry entries with the resolved context.
    for skill_md in candidate_skill_mds:
        skill_dir = skill_md.parent

        rel_path = str(skill_md.relative_to(PROJECT_ROOT))
        text = skill_md.read_text(errors="replace")

        # Extract metadata from all formats
        yaml_meta = extract_yaml_frontmatter(text) or {}
        inline_meta = extract_inline_metadata(text)
        structure = infer_structure(skill_md, all_skill_dirs, domain_orchestrators)

        # Skill key: prefer frontmatter `name` (handles non-conventional layouts
        # like skills/_meta/SKILL.md → sentinel-prime), fall back to directory.
        skill_name = (yaml_meta.get("name") or "").strip() or skill_dir.name

        # Merge: YAML > inline > inferred
        description = (
            yaml_meta.get("description", "").strip()
            or inline_meta.get("description", "")
            or extract_description_from_header(text)
            or f"{skill_name} skill"
        )

        skill_type = infer_type(skill_name, text, {**inline_meta, **yaml_meta})
        metrics = compute_metrics(text, skill_dir)

        # Build tags
        tags = []
        if structure["domain"]:
            tags.append(f"domain:{structure['domain']}")
        if structure["subdomain"]:
            tags.append(f"subdomain:{structure['subdomain']}")
        tags.append(f"layer:{skill_type}")

        today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

        discovered[skill_name] = {
            "name": skill_name,
            "description": description,
            "location": rel_path,
            "plugin": f"skill-{structure['domain']}" if structure["domain"] else "skill-infra",
            "type": skill_type,
            "source": "self",
            "context_mode": "inline",
            "invocation": "both",
            "version": "1.0.0",
            "metrics": metrics,
            "health_status": "healthy",
            "issues": [],
            "last_checked": f"{today}T00:00:00Z",
            "status": "active",
            "deprecated_date": None,
            "replacement_skill": None,
            "deprecation_reason": None,
            "auto_score": 50,  # Default score, needs calibration
            "manual_rating": None,
            "manual_notes": None,
            "composite_score": 50,
            "depends_on": [],
            "referenced_by": [],
            "shares_references_with": [],
            "forked_from": None,
            "forked_into": [],
            "tags": tags,
            "created": today,
            "last_modified": today,
            "changelog": [
                {
                    "date": today,
                    "action": "created",
                    "note": "Auto-discovered by sync-registry.py",
                }
            ],
            "parent": structure.get("parent"),
        }

    return discovered


def sync(apply: bool = False) -> None:
    with open(REGISTRY_PATH) as f:
        registry = json.load(f)

    existing = registry["skills"]
    discovered = discover_skills()

    # ── Find new skills (on disk, not in registry) ──
    new_names = sorted(set(discovered) - set(existing))
    # ── Find ghosts (in registry, not on disk) ──
    ghost_names = []
    for name, entry in existing.items():
        loc = entry.get("location", "")
        full = PROJECT_ROOT / loc
        if not full.exists():
            ghost_names.append(name)
    # ── Find location mismatches ──
    mismatches = []
    for name in set(discovered) & set(existing):
        disk_loc = discovered[name]["location"]
        reg_loc = existing[name].get("location", "")
        if disk_loc != reg_loc:
            mismatches.append((name, reg_loc, disk_loc))

    # ── Find description / metrics drift on existing entries ──
    drift_desc: list[tuple[str, str, str]] = []
    drift_metrics: list[str] = []
    for name in set(discovered) & set(existing):
        cur = existing[name]
        new = discovered[name]
        cur_desc = (cur.get("description") or "").strip()
        new_desc = (new.get("description") or "").strip()
        if new_desc and cur_desc != new_desc:
            drift_desc.append((name, cur_desc, new_desc))
        if cur.get("metrics") != new.get("metrics"):
            drift_metrics.append(name)

    # ── Cross-reference detection — scan SKILL.md text for backtick-quoted
    # references in escalation/scope sections and flag any new CROSS-DOMAIN
    # edges that aren't already recorded in depends_on. Same-domain edges
    # (director → its own leaves) are out of scope here: they're better
    # populated by analyze-skill.py's existing dependency-graph logic.
    # Purely additive: existing edges in depends_on are preserved.
    all_known_names = set(discovered) | set(existing)

    def _domain_of(skill_name: str) -> str | None:
        """Return the top-level domain (skills/<domain>/...) for a known skill."""
        entry = discovered.get(skill_name) or existing.get(skill_name) or {}
        loc = entry.get("location") or ""
        parts = loc.split("/")
        return parts[1] if len(parts) >= 2 and parts[0] == "skills" else None

    new_depends_on: dict[str, set[str]] = {}  # source skill → newly-detected targets
    for skill_md in SKILLS_DIR.rglob("SKILL.md"):
        if any(part in SKIP_DIRS for part in skill_md.relative_to(SKILLS_DIR).parts[:-1]):
            continue
        text = skill_md.read_text(errors="replace")
        yaml_meta = extract_yaml_frontmatter(text) or {}
        name = (yaml_meta.get("name") or "").strip() or skill_md.parent.name
        if name not in all_known_names:
            continue
        src_domain = _domain_of(name)
        detected = detect_cross_references(text, all_known_names) - {name}
        # Keep only cross-domain edges
        detected = {t for t in detected if _domain_of(t) and _domain_of(t) != src_domain}
        cur_dep = set(existing.get(name, {}).get("depends_on") or [])
        cur_dep |= set(discovered.get(name, {}).get("depends_on") or [])
        added = detected - cur_dep
        if added:
            new_depends_on[name] = added

    # Build the post-sync graph in memory so dry-run mode catches reverse-index
    # drift too. In particular, newly discovered child skills must immediately
    # appear in their parent's referenced_by list.
    prospective = {name: dict(entry) for name, entry in existing.items()}
    prospective.update({name: dict(discovered[name]) for name in new_names})
    for source, targets in new_depends_on.items():
        if source in prospective:
            prospective[source]["depends_on"] = sorted(
                set(prospective[source].get("depends_on") or []) | targets
            )
    expected_referenced_by = derive_referenced_by(prospective)
    referenced_by_drift = {
        name: refs
        for name, refs in expected_referenced_by.items()
        if sorted(prospective[name].get("referenced_by") or []) != refs
    }

    # ── Report ──
    print(f"Registry: {len(existing)} skills")
    print(f"On disk:  {len(discovered)} skills")
    print()

    if new_names:
        print(f"NEW ({len(new_names)}) — will be added:")
        for n in new_names:
            t = discovered[n]["type"]
            print(f"  + {n:<30s} [{t:<12s}] {discovered[n]['location']}")
    else:
        print("No new skills to add.")

    print()
    if ghost_names:
        print(f"GHOSTS ({len(ghost_names)}) — in registry but file missing:")
        for n in sorted(ghost_names):
            print(f"  ! {n:<30s} {existing[n].get('location', '?')}")
    else:
        print("No ghost entries.")

    print()
    if mismatches:
        print(f"LOCATION MISMATCHES ({len(mismatches)}):")
        for name, old, new in sorted(mismatches):
            print(f"  ~ {name}")
            print(f"      registry: {old}")
            print(f"      disk:     {new}")
    else:
        print("No location mismatches.")

    print()
    if drift_desc:
        print(f"DESCRIPTION DRIFT ({len(drift_desc)}):")
        for name, old, new in sorted(drift_desc)[:5]:
            print(f"  ~ {name}: {len(old)} → {len(new)} chars")
        if len(drift_desc) > 5:
            print(f"    ... and {len(drift_desc) - 5} more")
    if drift_metrics:
        print(f"METRICS DRIFT ({len(drift_metrics)} entries will be refreshed)")
    if new_depends_on:
        total_edges = sum(len(s) for s in new_depends_on.values())
        print(f"CROSS-REF DRIFT ({total_edges} new edges across {len(new_depends_on)} skills):")
        for src in sorted(new_depends_on)[:5]:
            targets = sorted(new_depends_on[src])
            print(f"  + {src} → {', '.join(targets)}")
        if len(new_depends_on) > 5:
            print(f"    ... and {len(new_depends_on) - 5} more")
    if referenced_by_drift:
        print(
            f"REFERENCED_BY DRIFT "
            f"({len(referenced_by_drift)} reverse-index entries will be rebuilt)"
        )

    # ── Apply changes ──
    if apply:
        print("\n── Applying changes ──")
        for n in new_names:
            existing[n] = discovered[n]
            print(f"  Added: {n}")

        for name, old, new in mismatches:
            existing[name]["location"] = new
            print(f"  Fixed location: {name}")

        for name, _, new_desc in drift_desc:
            existing[name]["description"] = new_desc
        if drift_desc:
            print(f"  Refreshed description on {len(drift_desc)} entries")

        for name in drift_metrics:
            existing[name]["metrics"] = discovered[name]["metrics"]
        if drift_metrics:
            print(f"  Refreshed metrics on {len(drift_metrics)} entries")

        # Cross-ref edges: additively merge new edges into depends_on, then
        # mirror into the target's referenced_by. Existing arrays are kept.
        added_edge_count = 0
        for src, targets in new_depends_on.items():
            if src not in existing:
                continue
            cur = existing[src].setdefault("depends_on", [])
            cur_set = set(cur)
            for t in sorted(targets):
                if t not in cur_set:
                    cur.append(t)
                    cur_set.add(t)
                    added_edge_count += 1
                # Mirror into target's referenced_by (additive)
                if t in existing:
                    rb = existing[t].setdefault("referenced_by", [])
                    if src not in set(rb):
                        rb.append(src)
        if added_edge_count:
            # Keep arrays sorted for stable diffs across runs.
            for name in new_depends_on:
                if name in existing:
                    existing[name]["depends_on"] = sorted(set(existing[name].get("depends_on", [])))
            for entry in existing.values():
                if "referenced_by" in entry:
                    entry["referenced_by"] = sorted(set(entry["referenced_by"]))
            print(f"  Added {added_edge_count} cross-reference edge(s)")

        # referenced_by is denormalized data, so rebuild it from the canonical
        # parent + depends_on edges after all additions and graph edits.
        rebuilt_referenced_by = derive_referenced_by(existing)
        reverse_updates = 0
        for name, refs in rebuilt_referenced_by.items():
            if sorted(existing[name].get("referenced_by") or []) != refs:
                reverse_updates += 1
            existing[name]["referenced_by"] = refs
        if reverse_updates:
            print(f"  Rebuilt referenced_by on {reverse_updates} entries")

        # Re-derive network.domains from on-disk paths so renames
        # (e.g., meta → _meta) propagate automatically.
        new_domains: dict[str, list[str]] = {}
        for name, entry in existing.items():
            parts = (entry.get("location") or "").split("/")
            if len(parts) >= 3 and parts[0] == "skills":
                new_domains.setdefault(parts[1], []).append(name)
        registry.setdefault("network", {})["domains"] = {
            dom: sorted(set(names)) for dom, names in sorted(new_domains.items())
        }
        print(f"  Re-derived network.domains: {len(new_domains)} domains")

        # Update timestamp
        registry["last_scan"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

        with open(REGISTRY_PATH, "w") as f:
            json.dump(registry, f, indent=2)
            f.write("\n")

        print(
            f"\nRegistry updated: {len(new_names)} added, "
            f"{len(mismatches)} locations fixed, "
            f"{len(drift_desc)} descriptions refreshed, "
            f"{len(drift_metrics)} metrics refreshed."
        )
        if ghost_names:
            print(f"NOTE: {len(ghost_names)} ghost(s) left in place — review manually:")
            for n in sorted(ghost_names):
                print(f"  ! {n}")
    else:
        total_changes = (
            len(new_names)
            + len(mismatches)
            + len(drift_desc)
            + len(drift_metrics)
            + sum(len(s) for s in new_depends_on.values())
            + len(referenced_by_drift)
        )
        if total_changes:
            print(f"\nDry run complete. {total_changes} change(s) pending.")
            print("Run with --apply to update registry.json")
        else:
            print("\nRegistry is in sync.")


if __name__ == "__main__":
    apply = "--apply" in sys.argv
    sync(apply=apply)
