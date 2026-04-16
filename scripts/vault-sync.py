#!/usr/bin/env python3
"""Sync the skill library to a living Obsidian vault (Layer 3).

Reads data/registry.json + skills/ SKILL.md files and writes/updates
notes in a numbered folder structure:

    00-maps/              MOCs + index
    10-domains/<domain>/  T0/T1 skill-derived notes

Auto-generated content lives inside fenced blocks:
    <!-- auto:begin:<name> --> ... <!-- auto:end:<name> -->
Everything outside fences is preserved (your manual annotations).

On first run (new vault), creates all notes from templates.
On subsequent runs, only updates fenced blocks — manual edits survive.

Usage:
    python3 scripts/vault-sync.py --vault-dir /path/to/vault
    python3 scripts/vault-sync.py --vault-dir /path/to/vault --dry-run

Replaces the old one-shot export-obsidian.sh with idempotent diff-merge.
"""

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path

_here = Path(__file__).resolve().parent
PROJECT_ROOT = _here.parent
REGISTRY_PATH = PROJECT_ROOT / "data" / "registry.json"
SKILLS_DIR = PROJECT_ROOT / "skills"

# Fenced block regex: captures name and content between markers
FENCE_RE = re.compile(
    r"(<!-- auto:begin:(\w[\w-]*) -->)\n(.*?)\n(<!-- auto:end:\2 -->)",
    re.DOTALL,
)

NOW = datetime.now(timezone.utc).strftime("%Y-%m-%d")


# ---------------------------------------------------------------------------
# Fenced block update
# ---------------------------------------------------------------------------

def update_fenced_blocks(existing: str, blocks: dict[str, str]) -> str:
    """Replace content inside auto-fenced blocks. Preserves everything else.

    `blocks` maps fence name → new content (without the fence markers).
    If a fence exists in the file, its content is replaced.
    If a fence doesn't exist, it's appended at the end.
    """
    updated = existing
    used_names = set()

    def replacer(m):
        name = m.group(2)
        used_names.add(name)
        if name in blocks:
            return f"{m.group(1)}\n{blocks[name]}\n{m.group(4)}"
        return m.group(0)  # no update for this fence

    updated = FENCE_RE.sub(replacer, updated)

    # Append any blocks that weren't found in the existing file
    for name, content in blocks.items():
        if name not in used_names:
            updated = updated.rstrip() + (
                f"\n\n<!-- auto:begin:{name} -->\n{content}\n<!-- auto:end:{name} -->\n"
            )

    return updated


# ---------------------------------------------------------------------------
# Note generators
# ---------------------------------------------------------------------------

def domain_from_location(loc: str) -> str:
    """Extract domain name from skill location path (skills/<domain>/...)."""
    parts = loc.split("/")
    return parts[1] if len(parts) >= 3 else "unknown"


def generate_skill_note(name: str, entry: dict, skill_md_path: Path | None) -> str:
    """Generate a full skill note (for new notes that don't exist yet)."""
    domain = domain_from_location(entry.get("location", ""))
    desc = entry.get("description", "").strip()
    score = entry.get("composite_score", 0)
    health = entry.get("health_status", "unknown")
    skill_type = entry.get("type", "knowledge")
    word_count = entry.get("metrics", {}).get("word_count", 0)
    depends = entry.get("depends_on", [])
    refs = entry.get("referenced_by", [])

    # Read first ~200 words of SKILL.md body for content preview
    preview = ""
    if skill_md_path and skill_md_path.exists():
        text = skill_md_path.read_text(errors="replace")
        # Strip YAML frontmatter
        if text.startswith("---"):
            end = text.find("---", 3)
            if end > 0:
                text = text[end + 3:].strip()
        # Strip title line
        lines = text.split("\n")
        if lines and lines[0].startswith("# "):
            lines = lines[1:]
        body = "\n".join(lines).strip()
        words = body.split()
        preview = " ".join(words[:200])
        if len(words) > 200:
            preview += " ..."

    # Wiki-links for cross-refs
    dep_links = ", ".join(f"[[{d}]]" for d in depends) if depends else "none"
    ref_links = ", ".join(f"[[{r}]]" for r in refs) if refs else "none"

    return f"""---
type: skill-summary
skill: {name}
domain: {domain}
tier: T1
generated_at: {NOW}
generated_by: vault-sync
publish: false
tags: [kb/skill-summary, domain/{domain}]
---

# {name.replace("-", " ").title()}

<!-- auto:begin:description -->
{desc}
<!-- auto:end:description -->

<!-- auto:begin:registry-sync -->
Composite score: {score} · Health: {health} · Type: {skill_type} · Words: {word_count}
Last synced: {NOW}
<!-- auto:end:registry-sync -->

## Content

<!-- auto:begin:content -->
{preview if preview else "_No content preview available._"}
<!-- auto:end:content -->

<!-- auto:begin:cross-refs -->
**Depends on**: {dep_links}
**Used by**: {ref_links}
**Domain**: [[MOC-{domain}]]
<!-- auto:end:cross-refs -->
"""


def generate_fenced_blocks(name: str, entry: dict) -> dict[str, str]:
    """Generate the auto-fenced block contents for an existing note."""
    domain = domain_from_location(entry.get("location", ""))
    desc = entry.get("description", "").strip()
    score = entry.get("composite_score", 0)
    health = entry.get("health_status", "unknown")
    skill_type = entry.get("type", "knowledge")
    word_count = entry.get("metrics", {}).get("word_count", 0)
    depends = entry.get("depends_on", [])
    refs = entry.get("referenced_by", [])

    dep_links = ", ".join(f"[[{d}]]" for d in depends) if depends else "none"
    ref_links = ", ".join(f"[[{r}]]" for r in refs) if refs else "none"

    return {
        "description": desc,
        "registry-sync": (
            f"Composite score: {score} · Health: {health} · Type: {skill_type} · Words: {word_count}\n"
            f"Last synced: {NOW}"
        ),
        "cross-refs": (
            f"**Depends on**: {dep_links}\n"
            f"**Used by**: {ref_links}\n"
            f"**Domain**: [[MOC-{domain}]]"
        ),
    }


def generate_moc(domain: str, skills: list[tuple[str, dict]]) -> str:
    """Generate a Map of Content for a domain."""
    # Group by type
    by_type: dict[str, list[tuple[str, dict]]] = {}
    for name, entry in sorted(skills, key=lambda x: x[0]):
        t = entry.get("type", "knowledge")
        by_type.setdefault(t, []).append((name, entry))

    type_order = ["orchestrator", "director", "knowledge", "action", "observer"]

    sections = []
    for t in type_order:
        items = by_type.get(t, [])
        if not items:
            continue
        heading = t.replace("-", " ").title() + "s"
        lines = [f"## {heading}", ""]
        for name, entry in items:
            desc_short = (entry.get("description", "") or "")[:80]
            score = entry.get("composite_score", 0)
            lines.append(f"- [[{name}]] — {desc_short} `[{score}]`")
        sections.append("\n".join(lines))

    scores = [e.get("composite_score", 0) for _, e in skills]
    avg_score = round(sum(scores) / len(scores), 1) if scores else 0

    return f"""---
type: moc
domain: {domain}
generated_at: {NOW}
generated_by: vault-sync
publish: false
tags: [kb/moc, domain/{domain}]
---

# {domain.replace("-", " ").title()}

<!-- auto:begin:domain-stats -->
*{len(skills)} skills · avg score {avg_score}*
<!-- auto:end:domain-stats -->

{chr(10).join(sections)}

<!-- auto:begin:cross-refs -->
**See also**: [[_Index]]
<!-- auto:end:cross-refs -->
"""


def generate_index(domains: dict[str, list], total_active: int, total_deprecated: int) -> str:
    """Generate the vault index page."""
    domain_lines = []
    for domain in sorted(domains.keys()):
        skills = domains[domain]
        scores = [e.get("composite_score", 0) for _, e in skills]
        avg = round(sum(scores) / len(scores), 1) if scores else 0
        domain_lines.append(f"- [[MOC-{domain}|{domain.replace('-', ' ').title()}]] — {len(skills)} skills (avg {avg})")

    return f"""---
type: index
generated_at: {NOW}
generated_by: vault-sync
publish: false
tags: [kb/index]
---

# Skill Library

<!-- auto:begin:stats -->
*{total_active} active skills across {len(domains)} domains · {total_deprecated} deprecated*
<!-- auto:end:stats -->

## Domains

{chr(10).join(domain_lines)}

<!-- auto:begin:cross-refs -->
**Graph**: [[skill-library-map]]
<!-- auto:end:cross-refs -->
"""


# ---------------------------------------------------------------------------
# Main sync logic
# ---------------------------------------------------------------------------

def sync(vault_dir: Path, dry_run: bool = False) -> dict:
    """Sync registry to vault. Returns summary stats."""
    reg = json.loads(REGISTRY_PATH.read_text())
    skills = reg.get("skills", {})

    active = {n: s for n, s in skills.items() if s.get("status") != "deprecated"}
    deprecated_count = len(skills) - len(active)

    # Group by domain
    domains: dict[str, list[tuple[str, dict]]] = {}
    for name, entry in active.items():
        domain = domain_from_location(entry.get("location", ""))
        domains.setdefault(domain, []).append((name, entry))

    stats = {"created": 0, "updated": 0, "unchanged": 0, "mocs_written": 0}

    # --- Skill notes ---
    for name, entry in active.items():
        domain = domain_from_location(entry.get("location", ""))
        note_path = vault_dir / "10-domains" / domain / f"{name}.md"

        # Find SKILL.md on disk
        loc = entry.get("location", "")
        skill_md = PROJECT_ROOT / loc if loc else None

        if note_path.exists():
            # Update fenced blocks only
            existing = note_path.read_text()
            blocks = generate_fenced_blocks(name, entry)
            updated = update_fenced_blocks(existing, blocks)
            if updated != existing:
                if not dry_run:
                    note_path.write_text(updated)
                stats["updated"] += 1
            else:
                stats["unchanged"] += 1
        else:
            # Create new note
            content = generate_skill_note(name, entry, skill_md)
            if not dry_run:
                note_path.parent.mkdir(parents=True, exist_ok=True)
                note_path.write_text(content)
            stats["created"] += 1

    # --- MOCs ---
    maps_dir = vault_dir / "00-maps"
    if not dry_run:
        maps_dir.mkdir(parents=True, exist_ok=True)

    for domain, domain_skills in domains.items():
        moc_path = maps_dir / f"MOC-{domain}.md"
        if moc_path.exists():
            existing = moc_path.read_text()
            # For MOCs, regenerate the domain-stats and cross-refs blocks
            scores = [e.get("composite_score", 0) for _, e in domain_skills]
            avg = round(sum(scores) / len(scores), 1) if scores else 0
            blocks = {
                "domain-stats": f"*{len(domain_skills)} skills · avg score {avg}*",
                "cross-refs": "**See also**: [[_Index]]",
            }
            updated = update_fenced_blocks(existing, blocks)
            if updated != existing:
                if not dry_run:
                    moc_path.write_text(updated)
                stats["mocs_written"] += 1
        else:
            content = generate_moc(domain, domain_skills)
            if not dry_run:
                moc_path.write_text(content)
            stats["mocs_written"] += 1

    # --- Index (with idempotency check to avoid spurious generated_at diffs) ---
    index_path = maps_dir / "_Index.md"
    content = generate_index(domains, len(active), deprecated_count)
    if not dry_run:
        if not index_path.exists() or index_path.read_text() != content:
            index_path.write_text(content)

    # --- Create empty structure dirs ---
    if not dry_run:
        for d in ["20-syntheses", "30-research", "40-reference", "50-journal",
                   "99-public", "_templates", "_attachments", "_meta"]:
            (vault_dir / d).mkdir(parents=True, exist_ok=True)
            gitkeep = vault_dir / d / ".gitkeep"
            if not gitkeep.exists():
                gitkeep.write_text("")

    return stats


def main():
    parser = argparse.ArgumentParser(description="Sync skill library to Obsidian vault")
    parser.add_argument("--vault-dir", required=True, help="Path to the vault directory")
    parser.add_argument("--dry-run", action="store_true", help="Show what would change without writing")
    args = parser.parse_args()

    vault_dir = Path(args.vault_dir).resolve()
    print(f"Syncing to: {vault_dir}")
    print(f"Registry: {REGISTRY_PATH}")
    print(f"Dry run: {args.dry_run}")
    print()

    stats = sync(vault_dir, dry_run=args.dry_run)

    print(f"Results:")
    print(f"  Notes created:   {stats['created']}")
    print(f"  Notes updated:   {stats['updated']}")
    print(f"  Notes unchanged: {stats['unchanged']}")
    print(f"  MOCs written:    {stats['mocs_written']}")
    print(f"  Total active:    {stats['created'] + stats['updated'] + stats['unchanged']}")

    if args.dry_run:
        print("\n(dry run — no files written)")


if __name__ == "__main__":
    main()
