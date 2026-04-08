#!/usr/bin/env bash
# Export the skill library into an Obsidian-optimized vault with wikilinks and MOCs.
# Usage: export-obsidian.sh [--output <dir>]
# Output: Flat vault in <dir> (default: exports/obsidian-vault)

set -euo pipefail

# --- Parse args ---
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
export PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
export SKILLS_DIR="$PROJECT_DIR/skills"
export REGISTRY="$PROJECT_DIR/data/registry.json"
export OUTPUT_DIR="$PROJECT_DIR/exports/obsidian-vault"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --output) export OUTPUT_DIR="$2"; shift 2 ;;
    *) echo "Unknown option: $1" >&2; exit 1 ;;
  esac
done

# --- Validate ---
if [ ! -f "$REGISTRY" ]; then
  echo "ERROR: Registry not found at $REGISTRY" >&2
  exit 1
fi

echo "Exporting skill library to Obsidian vault: $OUTPUT_DIR"

# --- Clean output ---
rm -rf "$OUTPUT_DIR"
mkdir -p "$OUTPUT_DIR"

# --- Use Python for all JSON-dependent export logic ---
python3 << 'PYEOF'
import json, os, sys, shutil

project_dir = os.environ.get("PROJECT_DIR", "")
skills_dir = os.environ.get("SKILLS_DIR", "")
output_dir = os.environ.get("OUTPUT_DIR", "")
registry_path = os.environ.get("REGISTRY", "")

with open(registry_path, "r") as f:
    registry = json.load(f)

skills = registry.get("skills", {})

# --- Step 1: Copy each SKILL.md as <skill-name>.md and inject relationships ---
exported_skills = {}
for skill_name, meta in skills.items():
    location = meta.get("location", "")
    src_path = os.path.join(project_dir, location)
    if not os.path.isfile(src_path):
        print(f"  SKIP (missing): {skill_name}", file=sys.stderr)
        continue

    with open(src_path, "r") as f:
        content = f.read()

    # Inject domain and type tags into YAML frontmatter for Obsidian graph coloring
    domain_tag = next((t.split(":")[1] for t in meta.get("tags", []) if t.startswith("domain:")), "unknown")
    if content.startswith("---"):
        # Find end of frontmatter (use find to avoid ValueError on malformed files)
        end_fm = content.find("---", 3)
        if end_fm == -1:
            print(f"  WARN (malformed frontmatter): {skill_name}", file=sys.stderr)
            end_fm = 3  # treat as no frontmatter
        fm_block = content[3:end_fm]
        after_fm = content[end_fm:]
        # Add tags if not already present
        if "tags:" not in fm_block:
            fm_block = fm_block.rstrip("\n") + f"\ntags: [{domain_tag}, {meta.get('type', 'unknown')}]\n"
        content = "---" + fm_block + after_fm

    # Build relationships section
    depends = meta.get("depends_on", [])
    referenced_by = meta.get("referenced_by", [])
    shares_refs = meta.get("shares_references_with", [])
    parent = meta.get("parent")
    skill_type = meta.get("type", "unknown")
    domain_tag = next((t.split(":")[1] for t in meta.get("tags", []) if t.startswith("domain:")), "unknown")
    health = meta.get("health_status", "unknown")
    score = meta.get("composite_score", "?")

    rel_lines = []
    rel_lines.append(f"\n\n---\n")
    rel_lines.append(f"## Metadata\n")
    rel_lines.append(f"- **Type:** {skill_type}")
    rel_lines.append(f"- **Domain:** {domain_tag}")
    rel_lines.append(f"- **Health:** {health} ({score}/100)")
    if parent:
        rel_lines.append(f"- **Parent:** [[{parent}]]")

    if depends or referenced_by or shares_refs:
        rel_lines.append(f"\n## Relationships\n")
        if depends:
            rel_lines.append("**Depends on:**")
            for dep in depends:
                rel_lines.append(f"- [[{dep}]]")
        if referenced_by:
            rel_lines.append("\n**Referenced by:**")
            for ref in referenced_by:
                rel_lines.append(f"- [[{ref}]]")
        if shares_refs:
            rel_lines.append("\n**Shares references with:**")
            for sr in shares_refs:
                rel_lines.append(f"- [[{sr}]]")

    enriched = content + "\n".join(rel_lines) + "\n"

    dst_path = os.path.join(output_dir, f"{skill_name}.md")
    with open(dst_path, "w") as f:
        f.write(enriched)
    exported_skills[skill_name] = meta

print(f"  Exported {len(exported_skills)} of {len(skills)} skills")

# --- Step 2: Generate domain MOCs ---
# Group exported skills by domain (only count what was actually exported)
domains = {}
for skill_name, meta in exported_skills.items():
    domain = next((t.split(":")[1] for t in meta.get("tags", []) if t.startswith("domain:")), "other")
    domains.setdefault(domain, []).append(meta)

for domain, domain_skills in sorted(domains.items()):
    moc_lines = [f"# {domain.replace('-', ' ').title()}\n"]
    moc_lines.append(f"*{len(domain_skills)} skills in this domain*\n")

    # Group by type
    by_type = {}
    for s in domain_skills:
        t = s.get("type", "unknown")
        by_type.setdefault(t, []).append(s)

    type_order = ["orchestrator", "director", "knowledge", "action", "observer"]
    for t in type_order:
        if t not in by_type:
            continue
        moc_lines.append(f"\n## {t.title()}s\n")
        for s in sorted(by_type[t], key=lambda x: x["name"]):
            name = s["name"]
            desc = s.get("description", "").split(".")[0].strip()
            health = s.get("health_status", "?")
            icon = {"healthy": "ok", "degraded": "!!", "critical": "XX"}.get(health, "?")
            moc_lines.append(f"- [[{name}]] — {desc} `[{icon}]`")

    moc_path = os.path.join(output_dir, f"_MOC-{domain}.md")
    with open(moc_path, "w") as f:
        f.write("\n".join(moc_lines) + "\n")

print(f"  Generated {len(domains)} domain MOCs")

# --- Step 3: Generate root index ---
index_lines = ["# Skill Library Index\n"]
index_lines.append(f"*{len(exported_skills)} total skills across {len(domains)} domains*\n")
index_lines.append("## Domains\n")

for domain in sorted(domains.keys()):
    count = len(domains[domain])
    healthy = sum(1 for s in domains[domain] if s.get("health_status") == "healthy")
    index_lines.append(f"- [[_MOC-{domain}|{domain.replace('-', ' ').title()}]] — {count} skills ({healthy} healthy)")

# Health summary
total = len(exported_skills)
total_healthy = sum(1 for s in exported_skills.values() if s.get("health_status") == "healthy")
total_degraded = sum(1 for s in exported_skills.values() if s.get("health_status") == "degraded")
total_critical = sum(1 for s in exported_skills.values() if s.get("health_status") == "critical")

index_lines.append(f"\n## Health Summary\n")
index_lines.append(f"| Status | Count | % |")
index_lines.append(f"|--------|------:|--:|")
index_lines.append(f"| Healthy | {total_healthy} | {round(total_healthy/total*100) if total else 0}% |")
index_lines.append(f"| Degraded | {total_degraded} | {round(total_degraded/total*100) if total else 0}% |")
index_lines.append(f"| Critical | {total_critical} | {round(total_critical/total*100) if total else 0}% |")

# Type breakdown
types = {}
for s in exported_skills.values():
    t = s.get("type", "unknown")
    types[t] = types.get(t, 0) + 1

index_lines.append(f"\n## Skill Types\n")
for t in ["orchestrator", "director", "knowledge", "action", "observer"]:
    if t in types:
        index_lines.append(f"- **{t.title()}:** {types[t]}")

index_path = os.path.join(output_dir, "_Index.md")
with open(index_path, "w") as f:
    f.write("\n".join(index_lines) + "\n")

print(f"  Generated root index")

PYEOF

# --- Step 4: Copy .obsidian config ---
if [ -d "$SKILLS_DIR/.obsidian" ]; then
  # Copy config but skip workspace (volatile)
  mkdir -p "$OUTPUT_DIR/.obsidian"
  shopt -s nullglob
  for f in "$SKILLS_DIR/.obsidian"/*.json; do
    fname=$(basename "$f")
    if [[ "$fname" != "workspace.json" && "$fname" != "workspaces.json" ]]; then
      cp "$f" "$OUTPUT_DIR/.obsidian/$fname"
    fi
  done
  shopt -u nullglob
  # Copy templates
  if [ -d "$SKILLS_DIR/.obsidian/templates" ]; then
    cp -r "$SKILLS_DIR/.obsidian/templates" "$OUTPUT_DIR/.obsidian/templates"
  fi
  echo "  Copied .obsidian config"
fi

echo ""
echo "Done! Open '$OUTPUT_DIR' as an Obsidian vault."
echo "  Skills: $(find "$OUTPUT_DIR" -maxdepth 1 -name '*.md' ! -name '_*' | wc -l | tr -d ' ')"
echo "  MOCs:   $(find "$OUTPUT_DIR" -maxdepth 1 -name '_MOC-*.md' | wc -l | tr -d ' ')"
echo "  Index:  _Index.md"
