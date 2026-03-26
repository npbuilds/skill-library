"""
Skill Library MCP Server
Exposes your skill library to Claude Desktop via the Model Context Protocol.
"""

import json
from datetime import datetime, timezone
from pathlib import Path
from mcp.server.fastmcp import FastMCP

# ---------------------------------------------------------------------------
# Setup
# ---------------------------------------------------------------------------

# The project root is one level up from this server file
PROJECT_ROOT = Path(__file__).resolve().parent.parent
REGISTRY_PATH = PROJECT_ROOT / "data" / "registry.json"
SKILLS_DIR = PROJECT_ROOT / "skills"

DATA_DIR = PROJECT_ROOT / "data"
USAGE_LOG = DATA_DIR / "usage.jsonl"
GAPS_LOG = DATA_DIR / "gaps.jsonl"
FEEDBACK_LOG = DATA_DIR / "feedback.jsonl"


def _log_event(path: Path, event: dict) -> None:
    """Append a JSON event to a JSONL log file."""
    record = {**event, "timestamp": datetime.now(timezone.utc).isoformat()}
    try:
        with open(path, "a") as f:
            f.write(json.dumps(record) + "\n")
    except OSError:
        pass  # Never let logging break a tool call


def _load_log(path: Path) -> list[dict]:
    """Load all events from a JSONL log file."""
    if not path.exists():
        return []
    events = []
    for line in path.read_text().splitlines():
        line = line.strip()
        if line:
            try:
                events.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return events


mcp = FastMCP(
    "Skill Library",
    instructions=(
        "This server provides access to a local skill library organized in a "
        "hierarchical domain structure. Use list_skills to browse what's available, "
        "search_skills to find relevant skills by keyword, get_skill to read a "
        "skill's full content, and get_system_overview for a bird's-eye view of "
        "the entire library. Always check the library before answering questions "
        "that might match a skill's domain."
    ),
)


def load_registry() -> dict:
    """Load the registry fresh each time (picks up changes without restart)."""
    try:
        with open(REGISTRY_PATH, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        raise RuntimeError(
            f"Registry not found at {REGISTRY_PATH}. "
            "Make sure data/registry.json exists."
        )
    except json.JSONDecodeError as e:
        raise RuntimeError(
            f"Registry has invalid JSON: {e}. Check data/registry.json for syntax errors."
        )


def resolve_skill_path(entry: dict, skill_name: str) -> str:
    """Resolve a skill's location to an absolute path.

    Registry locations may be relative (from project root) or absolute.
    Falls back to searching the skills directory if the stored path doesn't exist.
    """
    location = entry.get("location", "")
    if location:
        # Try as relative path from project root first
        resolved = PROJECT_ROOT / location
        if resolved.exists():
            return str(resolved)
        # Try as absolute path
        if Path(location).exists():
            return location
    # Last resort: search for the skill by name
    matches = list(SKILLS_DIR.rglob(f"{skill_name}/SKILL.md"))
    if len(matches) == 1:
        return str(matches[0])
    if len(matches) > 1:
        # Multiple matches — return the first but warn
        return str(matches[0])
    # Nothing found anywhere
    return f"ERROR: skill file not found for '{skill_name}' — check registry location field"


def read_file_safe(path: str) -> str:
    """Read a file, returning a friendly message if it doesn't exist."""
    try:
        return Path(path).read_text()
    except (FileNotFoundError, PermissionError, OSError) as e:
        return f"(could not read file: {path} — {e})"


# ---------------------------------------------------------------------------
# Tools
# ---------------------------------------------------------------------------


@mcp.tool()
def list_skills(
    domain: str | None = None,
    skill_type: str | None = None,
    subdomain: str | None = None,
) -> str:
    """List all available skills in the library.

    Args:
        domain: Optional filter — only show skills in this domain (e.g. "design", "infrastructure").
        skill_type: Optional filter — only show this type ("knowledge", "action", "director", "orchestrator", or "observer").
        subdomain: Optional filter — only show skills in this subdomain (e.g. "visual-communication").
    """
    try:
        registry = load_registry()
    except RuntimeError as e:
        return str(e)
    skills = registry.get("skills", {})
    if not skills:
        return "The registry is empty or missing the 'skills' key."
    results = []

    for name, entry in skills.items():
        tags = entry.get("tags", [])

        # Apply domain filter
        if domain and f"domain:{domain}" not in tags:
            continue

        # Apply type filter
        if skill_type and entry.get("type") != skill_type:
            continue

        # Apply subdomain filter (excludes directors that own the subdomain)
        if subdomain:
            if f"subdomain:{subdomain}" not in tags:
                continue
            if entry.get("type") == "director":
                continue

        results.append(
            {
                "name": name,
                "type": entry.get("type", "unknown"),
                "description": entry.get("description", ""),
                "domain": next(
                    (t.split(":")[1] for t in tags if t.startswith("domain:")),
                    "untagged",
                ),
                "parent": entry.get("parent"),
                "health": entry.get("health_status", "unknown"),
                "score": entry.get("composite_score"),
            }
        )

    if not results:
        return "No skills found matching those filters."

    # Build a readable summary
    lines = [f"Found {len(results)} skill(s):\n"]
    for s in results:
        parent_info = f", parent: {s['parent']}" if s["parent"] else ""
        lines.append(
            f"  [{s['type']}] {s['name']}  "
            f"(domain: {s['domain']}, health: {s['health']}, score: {s['score']}{parent_info})"
        )
        lines.append(f"    {s['description'].strip()}")
        lines.append("")

    # Also list available domains and subdomains for discoverability
    all_domains = set()
    all_subdomains = set()
    for entry in skills.values():
        for tag in entry.get("tags", []):
            if tag.startswith("domain:"):
                all_domains.add(tag.split(":")[1])
            elif tag.startswith("subdomain:"):
                all_subdomains.add(tag.split(":")[1])
    lines.append(f"Available domains: {', '.join(sorted(all_domains))}")
    if all_subdomains:
        lines.append(f"Available subdomains: {', '.join(sorted(all_subdomains))}")

    return "\n".join(lines)


@mcp.tool()
def search_skills(query: str) -> str:
    """Search the skill library by keyword. Matches against skill names, descriptions, and tags.

    Args:
        query: The search term (e.g. "color", "testing", "design", "accessibility").
    """
    try:
        registry = load_registry()
    except RuntimeError as e:
        return str(e)
    skills = registry.get("skills", {})
    if not skills:
        return "The registry is empty or missing the 'skills' key."
    query_lower = query.lower()
    matches = []

    for name, entry in skills.items():
        searchable = " ".join(
            [
                name,
                entry.get("description", ""),
                " ".join(entry.get("tags", [])),
                entry.get("type", ""),
            ]
        ).lower()

        if query_lower in searchable:
            matches.append(
                {
                    "name": name,
                    "type": entry.get("type", "unknown"),
                    "description": entry.get("description", "").strip(),
                    "tags": entry.get("tags", []),
                    "score": entry.get("composite_score"),
                }
            )

    if not matches:
        # Log the gap — this query found nothing
        _log_event(GAPS_LOG, {"query": query, "result_count": 0})
        return f"No skills found matching '{query}'. Use the list_skills tool to see all available skills."

    # Log low-result searches too (1-2 results may indicate thin coverage)
    if len(matches) <= 2:
        _log_event(GAPS_LOG, {"query": query, "result_count": len(matches)})

    lines = [f"Found {len(matches)} skill(s) matching '{query}':\n"]
    for m in matches:
        lines.append(f"  [{m['type']}] {m['name']}  (score: {m['score']})")
        lines.append(f"    {m['description']}")
        lines.append(f"    tags: {', '.join(m['tags'])}")
        lines.append("")

    return "\n".join(lines)


@mcp.tool()
def get_skill(skill_name: str, include_references: bool = True) -> str:
    """Read a skill's full content, including its reference documents.

    This returns the complete SKILL.md file and optionally all reference files,
    giving you the full knowledge and methodology of the skill.

    Args:
        skill_name: The skill's name (e.g. "color-theory", "design-principles").
        include_references: Whether to also return reference documents (default: True).
    """
    try:
        registry = load_registry()
    except RuntimeError as e:
        return str(e)
    skills = registry.get("skills", {})
    entry = skills.get(skill_name)

    if not entry:
        available = ", ".join(sorted(skills.keys()))
        return f"Skill '{skill_name}' not found. Available skills: {available}"

    # Log usage
    _log_event(USAGE_LOG, {"skill": skill_name, "type": entry.get("type", "unknown")})

    skill_path = resolve_skill_path(entry, skill_name)
    content = read_file_safe(skill_path)
    parts = [f"=== SKILL: {skill_name} ===\n\n{content}"]

    # Read reference files if requested
    if include_references:
        refs_dir = Path(skill_path).parent / "references"
        if refs_dir.exists():
            ref_files = sorted(refs_dir.glob("*.md"))
            if ref_files:
                parts.append(f"\n\n=== REFERENCE DOCUMENTS ({len(ref_files)}) ===")
                for ref_file in ref_files:
                    parts.append(f"\n--- {ref_file.name} ---\n")
                    parts.append(read_file_safe(str(ref_file)))

    # Also read agent files for orchestrator skills
    if entry.get("type") == "orchestrator":
        agents_dir = Path(skill_path).parent / "agents"
        if agents_dir.exists():
            agent_files = sorted(agents_dir.glob("*.md"))
            if agent_files:
                parts.append(f"\n\n=== AGENT DEFINITIONS ({len(agent_files)}) ===")
                for agent_file in agent_files:
                    parts.append(f"\n--- {agent_file.name} ---\n")
                    parts.append(read_file_safe(str(agent_file)))

    return "".join(parts)


@mcp.tool()
def get_skill_details(skill_name: str) -> str:
    """Get metadata and metrics for a specific skill (without reading the full content).

    Returns health status, scores, dependencies, tags, and metrics.
    Use this for a quick overview before deciding whether to read the full skill.

    Args:
        skill_name: The skill's name (e.g. "color-theory").
    """
    try:
        registry = load_registry()
    except RuntimeError as e:
        return str(e)
    skills = registry.get("skills", {})
    entry = skills.get(skill_name)

    if not entry:
        available = ", ".join(sorted(skills.keys()))
        return f"Skill '{skill_name}' not found. Available skills: {available}"

    details = {
        "name": entry.get("name", skill_name),
        "type": entry.get("type"),
        "description": entry.get("description", "").strip(),
        "status": entry.get("status"),
        "health": entry.get("health_status"),
        "score": entry.get("composite_score"),
        "tags": entry.get("tags", []),
        "parent": entry.get("parent"),
        "depends_on": entry.get("depends_on", []),
        "referenced_by": entry.get("referenced_by", []),
        "metrics": entry.get("metrics", {}),
        "last_modified": entry.get("last_modified"),
    }

    return json.dumps(details, indent=2)


@mcp.tool()
def get_system_overview() -> str:
    """Get a bird's-eye view of the entire skill library.

    Returns domain coverage, maturity levels, detected gaps, cross-domain
    connections, and recommendations for what to build next. Use this when
    the user asks about the overall state of their library or wants guidance
    on priorities.
    """
    try:
        registry = load_registry()
    except RuntimeError as e:
        return str(e)
    skills = registry.get("skills", {})
    if not skills:
        return "The registry is empty."

    domains = registry.get("network", {}).get("domains", {})

    # Compute stats per domain
    lines = ["=== SKILL LIBRARY OVERVIEW ===\n"]

    # Overall counts by type
    type_counts: dict[str, int] = {}
    for entry in skills.values():
        t = entry.get("type", "unknown")
        type_counts[t] = type_counts.get(t, 0) + 1

    total = len(skills)
    type_summary = ", ".join(f"{c} {t}" for t, c in sorted(type_counts.items()))
    lines.append(f"Domains: {len(domains)}")
    lines.append(f"Total Skills: {total} ({type_summary})")
    lines.append("")

    # Per-domain analysis
    for domain_name, domain_skills in sorted(domains.items()):
        if domain_name == "meta":
            continue  # Skip meta domain in per-domain listing

        lines.append(f"--- {domain_name} ---")

        # Count types within domain
        d_types: dict[str, int] = {}
        has_orchestrator = False
        has_director = False
        d_health_issues = []

        for sname in domain_skills:
            entry = skills.get(sname, {})
            stype = entry.get("type", "unknown")
            d_types[stype] = d_types.get(stype, 0) + 1
            if stype == "orchestrator":
                has_orchestrator = True
            if stype == "director":
                has_director = True
            if entry.get("health_status") != "healthy":
                d_health_issues.append(sname)

        # Compute maturity score
        maturity_score = 0
        maturity_score += d_types.get("knowledge", 0)
        maturity_score += d_types.get("action", 0)
        maturity_score += d_types.get("director", 0) * 3
        maturity_score += 5 if has_orchestrator else 0

        if maturity_score == 0:
            level, bar = 0, "░░░░░░░░░░"
        elif maturity_score <= 3:
            level, bar = 1, "██░░░░░░░░"
        elif maturity_score <= 6:
            level, bar = 2, "████░░░░░░"
        elif maturity_score <= 10:
            level, bar = 3, "██████░░░░"
        elif maturity_score <= 20:
            level, bar = 4, "████████░░"
        else:
            level, bar = 5, "██████████"

        # Collect subdomains in this domain
        d_subdomains = set()
        for sname in domain_skills:
            for tag in skills.get(sname, {}).get("tags", []):
                if tag.startswith("subdomain:"):
                    d_subdomains.add(tag.split(":")[1])

        lines.append(f"  Maturity: Level {level}/5 {bar}")
        lines.append(f"  Orchestrator: {'Yes' if has_orchestrator else 'No'}")
        if d_subdomains:
            lines.append(f"  Subdomains: {', '.join(sorted(d_subdomains))}")
        else:
            lines.append(f"  Subdomains: none")
        lines.append(f"  Skills: {len(domain_skills)} ({', '.join(f'{c} {t}' for t, c in sorted(d_types.items()))})")

        # Detect gaps
        gaps = []
        if len(domain_skills) >= 3 and not has_orchestrator and domain_name != "infrastructure":
            gaps.append("No orchestrator (consider adding one for strategic coordination)")
        if d_types.get("knowledge", 0) >= 3 and not has_director:
            gaps.append("3+ knowledge skills but no director to organize them")
        if d_health_issues:
            gaps.append(f"Unhealthy skills: {', '.join(d_health_issues)}")

        lines.append(f"  Gaps: {'; '.join(gaps) if gaps else 'none detected'}")
        lines.append("")

    # Cross-domain analysis
    lines.append("--- Cross-Domain ---")

    # Check for orphan skills (no parent, not an orchestrator/observer, in a domain with directors)
    orphans = []
    for sname, entry in skills.items():
        if (
            entry.get("parent") is None
            and entry.get("type") in ("knowledge", "action")
            and any(
                skills.get(ds, {}).get("type") == "director"
                for ds in domains.get(
                    next((t.split(":")[1] for t in entry.get("tags", []) if t.startswith("domain:")), ""),
                    [],
                )
            )
        ):
            orphans.append(sname)

    # Check for untagged skills (no domain tag at all)
    untagged = [
        sname for sname, entry in skills.items()
        if not any(t.startswith("domain:") for t in entry.get("tags", []))
    ]

    if orphans:
        lines.append(f"  Orphan skills (no parent): {', '.join(orphans)}")
    else:
        lines.append("  Orphans: none")
    if untagged:
        lines.append(f"  Untagged skills (no domain): {', '.join(untagged)}")

    # Check for broken references
    broken = []
    for sname, entry in skills.items():
        for dep in entry.get("depends_on", []):
            if dep not in skills:
                broken.append(f"{sname} depends on missing '{dep}'")
        parent = entry.get("parent")
        if parent and parent not in skills:
            broken.append(f"{sname} has missing parent '{parent}'")

    if broken:
        lines.append(f"  Broken references: {'; '.join(broken)}")
    else:
        lines.append("  Broken references: none")
    lines.append("")

    # Recommendations
    lines.append("--- Recommendations ---")
    recs = []

    # Find domains that could use more structure
    for domain_name, domain_skills in sorted(domains.items()):
        if domain_name == "meta":
            continue
        d_types_r: dict[str, int] = {}
        for sname in domain_skills:
            stype = skills.get(sname, {}).get("type", "unknown")
            d_types_r[stype] = d_types_r.get(stype, 0) + 1

        if d_types_r.get("knowledge", 0) >= 3 and not d_types_r.get("director", 0):
            recs.append(f"Add a director to {domain_name} (3+ knowledge skills need routing)")
        if d_types_r.get("director", 0) >= 2 and not d_types_r.get("orchestrator", 0):
            recs.append(f"Add an orchestrator to {domain_name} (2+ directors need coordination)")

    if not recs:
        recs.append("Library is well-structured. Consider adding new domains or deepening existing ones.")

    for i, rec in enumerate(recs, 1):
        lines.append(f"  {i}. {rec}")

    return "\n".join(lines)


@mcp.tool()
def record_skill_feedback(skill_name: str, rating: int, note: str = "") -> str:
    """Record feedback on a skill you just used. Call this when the user shares
    their opinion on a skill's output quality.

    Args:
        skill_name: The skill that was used (e.g. "color-theory").
        rating: Quality rating from 1-5 (1=poor, 3=okay, 5=excellent).
        note: Optional short note on what worked or didn't.
    """
    try:
        registry = load_registry()
    except RuntimeError as e:
        return str(e)
    skills = registry.get("skills", {})
    if skill_name not in skills:
        return f"Skill '{skill_name}' not found in registry."

    if not 1 <= rating <= 5:
        return "Rating must be between 1 and 5."

    _log_event(FEEDBACK_LOG, {
        "skill": skill_name,
        "rating": rating,
        "note": note,
    })

    return f"Recorded: {skill_name} rated {rating}/5{f' — {note}' if note else ''}."


@mcp.tool()
def get_skill_stats(skill_name: str | None = None) -> str:
    """Get usage and quality stats for your skills.

    Without a skill_name, returns a summary of all skill activity —
    most used, least used, gaps (searches that found nothing), and
    feedback highlights. With a skill_name, returns detailed stats
    for that one skill.

    Args:
        skill_name: Optional — get stats for a specific skill.
    """
    usage_events = _load_log(USAGE_LOG)
    feedback_events = _load_log(FEEDBACK_LOG)
    gap_events = _load_log(GAPS_LOG)

    if not usage_events and not feedback_events and not gap_events:
        return "No analytics data yet. Use skills and give feedback to start building stats."

    # ── Single skill detail ──
    if skill_name:
        uses = [e for e in usage_events if e.get("skill") == skill_name]
        fb = [e for e in feedback_events if e.get("skill") == skill_name]

        lines = [f"=== Stats for {skill_name} ===\n"]
        lines.append(f"Total uses: {len(uses)}")

        if uses:
            first = uses[0].get("timestamp", "?")[:10]
            last = uses[-1].get("timestamp", "?")[:10]
            lines.append(f"First used: {first}")
            lines.append(f"Last used:  {last}")

            # Repeat usage signal: count uses within 7-day windows
            _ts = []
            for e in uses:
                try:
                    _ts.append(datetime.fromisoformat(e["timestamp"]).timestamp())
                except (KeyError, ValueError):
                    continue
            if len(_ts) >= 2:
                week = 7 * 86400
                repeat_count = sum(
                    1 for i in range(1, len(_ts)) if (_ts[i] - _ts[i - 1]) <= week
                )
                lines.append(f"Repeat uses (within 7 days): {repeat_count}")

        if fb:
            ratings = [e["rating"] for e in fb if "rating" in e]
            if ratings:
                avg = sum(ratings) / len(ratings)
                lines.append(f"\nFeedback: {len(fb)} ratings, avg {avg:.1f}/5")
                lines.append(f"  Ratings: {', '.join(str(r) for r in ratings)}")
            notes = [e["note"] for e in fb if e.get("note")]
            if notes:
                lines.append(f"  Notes:")
                for n in notes[-5:]:  # Last 5 notes
                    lines.append(f"    - {n}")
        else:
            lines.append("\nFeedback: none yet")

        return "\n".join(lines)

    # ── Summary view ──
    lines = ["=== SKILL ANALYTICS SUMMARY ===\n"]

    # Usage counts
    usage_counts: dict[str, int] = {}
    for e in usage_events:
        s = e.get("skill", "?")
        usage_counts[s] = usage_counts.get(s, 0) + 1

    if usage_counts:
        sorted_usage = sorted(usage_counts.items(), key=lambda x: x[1], reverse=True)
        lines.append(f"Total skill loads: {len(usage_events)}")
        lines.append(f"Unique skills used: {len(usage_counts)}\n")

        lines.append("Most used:")
        for name, count in sorted_usage[:10]:
            lines.append(f"  {name}: {count}")

        # Find unused skills (in registry but never loaded)
        try:
            registry = load_registry()
            all_skills = set(registry.get("skills", {}).keys())
            used_skills = set(usage_counts.keys())
            unused = sorted(all_skills - used_skills)
            if unused:
                lines.append(f"\nNever used ({len(unused)}):")
                for name in unused:
                    lines.append(f"  {name}")
        except RuntimeError:
            pass

    # Feedback summary
    if feedback_events:
        lines.append("\n--- Feedback ---")
        fb_by_skill: dict[str, list[int]] = {}
        for e in feedback_events:
            s = e.get("skill", "?")
            r = e.get("rating")
            if r is not None:
                fb_by_skill.setdefault(s, []).append(r)

        for s, ratings in sorted(fb_by_skill.items(), key=lambda x: sum(x[1]) / len(x[1]), reverse=True):
            avg = sum(ratings) / len(ratings)
            lines.append(f"  {s}: {avg:.1f}/5 ({len(ratings)} ratings)")

    # Gaps
    if gap_events:
        lines.append("\n--- Gaps (searches with poor/no results) ---")
        gap_queries: dict[str, int] = {}
        for e in gap_events:
            q = e.get("query", "?")
            gap_queries[q] = gap_queries.get(q, 0) + 1
        for q, count in sorted(gap_queries.items(), key=lambda x: x[1], reverse=True)[:10]:
            lines.append(f"  \"{q}\" — searched {count} time(s)")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Run
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    mcp.run()
