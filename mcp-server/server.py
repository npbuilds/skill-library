"""
Skill Library MCP Server
Exposes your skill library to Claude Desktop via the Model Context Protocol.

Supports two modes:
  - Local (default): stdio transport, all tools (read + write). Used by Claude Desktop.
  - Remote: HTTP transport, read-only tools. Used by claude.ai (web + mobile).

Usage:
  python server.py                              # local stdio (default)
  python server.py --remote                     # remote HTTP on port 8742
  python server.py --remote --port 9000         # remote HTTP on custom port
  MCP_REMOTE=true python server.py              # remote via env var
"""

import fcntl
import json
import logging
import os
import sys
import uuid
from collections import Counter, deque
from datetime import datetime, timezone
from pathlib import Path
from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.server import TransportSecuritySettings

# One UUID per server process. Stamped onto every log event so downstream
# scripts (derive_coactivation, etc.) can group co-retrievals by session.
# Process == session; restart resets. Stdio: one session per Claude Desktop
# run. HTTP: one session per Cloud Run instance lifetime (with concurrent
# requests sharing the same id — coactivation tolerates an approximate signal).
_SERVER_SESSION_ID = uuid.uuid4().hex

# ---------------------------------------------------------------------------
# Remote mode detection — must happen before tool registration
# ---------------------------------------------------------------------------

REMOTE_MODE = os.environ.get("MCP_REMOTE", "false").lower() == "true"

# ---------------------------------------------------------------------------
# Setup
# ---------------------------------------------------------------------------

from shared import (
    PROJECT_ROOT, REGISTRY_PATH, SKILLS_DIR, DATA_DIR,
    USAGE_LOG, GAPS_LOG, FEEDBACK_LOG,
    load_log, iter_skill_uses,
    atomic_write_registry,
    compute_auto_score,
    score_structure, score_depth, score_connectivity,
    score_freshness, score_usage, score_feedback,
    blast_radius, _get_domain,
)


def _log_event(path: Path, event: dict) -> None:
    """Append a JSON event to a JSONL log file (with file locking).

    Every record carries session_id (server-process UUID) and timestamp.
    Caller can override session_id via the event dict but normally shouldn't.
    """
    record = {
        "session_id": _SERVER_SESSION_ID,
        **event,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    try:
        with open(path, "a") as f:
            fcntl.flock(f, fcntl.LOCK_EX)
            try:
                f.write(json.dumps(record) + "\n")
                f.flush()
            finally:
                fcntl.flock(f, fcntl.LOCK_UN)
    except OSError as e:
        # Never let logging break a tool call — but don't lose the failure
        # either. stderr is captured by Cloud Logging in remote mode.
        print(
            f"skill-library: failed to write log {path.name}: {e}",
            file=sys.stderr,
        )


_load_log = load_log  # backward-compatible alias


mcp = FastMCP(
    "Skill Library",
    instructions=(
        "This server provides access to a local skill library organized in a "
        "hierarchical domain structure. Use list_skills to browse what's available, "
        "search_skills to find relevant skills by keyword, get_skill to read a "
        "skill's full content, and get_system_overview for a bird's-eye view of "
        "the entire library. Always check the library before answering questions "
        "that might match a skill's domain.\n\n"
        "IMPORTANT — Adapting skills to your environment:\n"
        "Skills were written for Claude Code and may reference tools like WebSearch, "
        "Agent, Bash, Grep, Read, or Write. When running outside Claude Code "
        "(e.g. on claude.ai web or mobile), adapt the methodology to tools you "
        "DO have available:\n"
        "- WebSearch/WebFetch → use your built-in web search\n"
        "- Agent → do the work inline instead of delegating\n"
        "- Bash/Grep/Read/Write → skip or ask the user for that info\n"
        "- Multi-phase skills → follow the phases conceptually, substituting "
        "available capabilities\n"
        "The skill content is methodology and thinking frameworks — the value is "
        "in the approach, not the specific tool calls. Follow the spirit of the "
        "skill even when you can't use the exact tools it names."
    ),
    # In remote mode, accept requests from any host (Cloud Run, Cloudflare, etc.)
    transport_security=TransportSecuritySettings(
        enable_dns_rebinding_protection=not REMOTE_MODE,
    ),
    # Cloud Run has cpu-throttling enabled, which stalls the long-lived task
    # group + SSE streams that stateful streamable-http relies on between
    # requests — clients see the connection hang after `initialize`. Stateless
    # mode makes each request a fresh transport with no cross-request state,
    # which is the FastMCP-recommended config for serverless platforms.
    # json_response avoids SSE framing entirely (simple JSON request/response).
    stateless_http=REMOTE_MODE,
    json_response=REMOTE_MODE,
)


_registry_cache_snapshot: tuple[tuple[str, float], dict] | None = None

# Hybrid search index (lazy-loaded, invalidated by registry mtime)
_search_index = None  # type: ignore[assignment]
_search_index_mtime: float = 0.0


def load_registry() -> dict:
    """Load registry, cached by (path, mtime) — picks up changes instantly after writes."""
    global _registry_cache_snapshot
    try:
        with open(REGISTRY_PATH) as f:
            # Use fstat on the open fd to avoid TOCTOU race
            stat = os.fstat(f.fileno())
            key = (str(REGISTRY_PATH), stat.st_mtime)
            if _registry_cache_snapshot is not None and key == _registry_cache_snapshot[0]:
                return _registry_cache_snapshot[1]
            data = json.load(f)
    except FileNotFoundError:
        raise RuntimeError(
            f"Registry not found at {REGISTRY_PATH}. "
            "Make sure data/registry.json exists."
        )
    except json.JSONDecodeError as e:
        raise RuntimeError(
            f"Registry has invalid JSON: {e}. Check data/registry.json for syntax errors."
        )
    # Atomic snapshot update — both key and data in one tuple assignment
    _registry_cache_snapshot = (key, data)
    return data


def _get_search_index():
    """Return the hybrid search index, rebuilding if registry changed."""
    global _search_index, _search_index_mtime
    try:
        from search_index import HybridSearchIndex
    except ImportError:
        return None

    try:
        mtime = REGISTRY_PATH.stat().st_mtime
    except OSError:
        return None

    if _search_index is not None and mtime == _search_index_mtime:
        return _search_index

    try:
        registry = load_registry()
        idx = HybridSearchIndex(SKILLS_DIR, registry, DATA_DIR)
        idx.build()
        _search_index = idx
        _search_index_mtime = mtime
        return idx
    except Exception as e:
        logging.getLogger(__name__).warning("Failed to build search index: %s", e)
        return None


def resolve_skill_path(entry: dict, skill_name: str) -> str | None:
    """Resolve a skill's location to an absolute path.

    Registry locations may be relative (from project root) or absolute.
    Falls back to searching the skills directory if the stored path doesn't exist.
    Returns None if the skill file cannot be found.
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
    if matches:
        return str(matches[0])
    return None


def read_file_safe(path: str) -> str:
    """Read a file, returning a friendly message if it doesn't exist."""
    try:
        return Path(path).read_text()
    except (FileNotFoundError, PermissionError, OSError) as e:
        return f"(could not read file: {path} — {e})"


# ---------------------------------------------------------------------------
# Tools
# ---------------------------------------------------------------------------


@mcp.tool(meta={"anthropic/maxResultSizeChars": 500000})
def list_skills(
    domain: str | None = None,
    skill_type: str | None = None,
    subdomain: str | None = None,
    limit: int = 100,
    offset: int = 0,
) -> str:
    """List all available skills in the library.

    Args:
        domain: Optional filter — only show skills in this domain (e.g. "design", "infrastructure").
        skill_type: Optional filter — only show this type ("knowledge", "action", "director", "orchestrator", or "observer").
        subdomain: Optional filter — only show skills in this subdomain (e.g. "visual-communication").
        limit: Max skills per page (default 100). Pass 0 for no limit.
        offset: Number of matching skills to skip — use with limit to paginate.
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

    # Deterministic order so offset-based pagination is stable across calls.
    results.sort(key=lambda s: (s["domain"], s["name"]))

    total = len(results)
    offset = max(0, offset)
    if offset >= total:
        return (
            f"Found {total} skill(s), but offset={offset} is past the end. "
            f"Use offset < {total}."
        )
    page = results[offset:offset + limit] if limit > 0 else results[offset:]
    end = offset + len(page)

    # Build a readable summary
    lines = [f"Found {total} skill(s), showing {offset + 1}–{end}:\n"]
    for s in page:
        parent_info = f", parent: {s['parent']}" if s["parent"] else ""
        lines.append(
            f"  [{s['type']}] {s['name']}  "
            f"(domain: {s['domain']}, health: {s['health']}, score: {s['score']}{parent_info})"
        )
        lines.append(f"    {s['description'].strip()}")
        lines.append("")

    if end < total:
        lines.append(
            f"({total - end} more — call again with offset={end} for the next page.)"
        )

    # List available domains/subdomains for discoverability, first page only
    # so paginated follow-ups stay lean.
    if offset == 0:
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


def _match_score(name: str, entry: dict, query: str) -> int:
    """Return a relevance score (0 = no match) for ranked search results."""
    q = query.lower()
    score = 0

    # Name matches (highest weight — most specific signal)
    name_l = name.lower()
    if name_l == q:
        score += 100
    elif name_l.startswith(q + "-") or name_l.endswith("-" + q):
        score += 80
    elif f"-{q}-" in name_l:
        score += 65
    elif q in name_l:
        score += 50

    # Description word-boundary matches
    desc_l = entry.get("description", "").lower()
    desc_words = set(desc_l.replace(",", " ").replace(".", " ").split())
    if q in desc_words:
        score += 40
    elif q in desc_l:
        score += 15

    # Tag matches — exact tag value (after colon) scores higher than substring
    tags = entry.get("tags", [])
    for tag in tags:
        tag_val = tag.split(":")[-1].lower()
        if tag_val == q:
            score += 35
            break
        elif q in tag_val:
            score += 10
            break

    # Type match (e.g. query="director")
    if q == entry.get("type", "").lower():
        score += 25

    return score


@mcp.tool(meta={"anthropic/maxResultSizeChars": 500000})
def search_skills(query: str) -> str:
    """Search the skill library by keyword. Matches against skill names, descriptions, and tags.

    Uses hybrid search (BM25 + semantic vectors + graph proximity) when
    available, falling back to keyword matching otherwise.

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

    # --- Try hybrid search first ---
    idx = _get_search_index()
    if idx is not None and idx.is_ready:
        # Get recent skills for graph proximity signal
        recent_skills: list[str] = []
        try:
            usage_events = load_log(USAGE_LOG)
            seen: set[str] = set()
            for e in reversed(usage_events):
                s = e.get("skill", "")
                if s and s not in seen:
                    seen.add(s)
                    recent_skills.append(s)
                if len(recent_skills) >= 10:
                    break
        except Exception:
            pass

        hybrid_results = idx.search(query, recent_skills=recent_skills, limit=20)

        if hybrid_results:
            lines = [f"Found {len(hybrid_results)} skill(s) matching '{query}' "
                     f"(hybrid: {idx.signal_count} signals):\n"]
            for r in hybrid_results:
                entry = skills.get(r["name"], {})
                stype = entry.get("type", "unknown")
                desc = entry.get("description", "").strip()
                tags = entry.get("tags", [])
                cscore = entry.get("composite_score")
                sig_flags = []
                if r["signals"].get("bm25"):
                    sig_flags.append("bm25")
                if r["signals"].get("vector"):
                    sig_flags.append("vec")
                if r["signals"].get("graph"):
                    sig_flags.append("graph")
                sig_str = "+".join(sig_flags) if sig_flags else "?"
                lines.append(f"  [{stype}] {r['name']}  "
                             f"(score: {cscore}, rrf: {r['rrf_score']:.4f}, signals: {sig_str})")
                lines.append(f"    {desc}")
                lines.append(f"    tags: {', '.join(tags)}")
                lines.append("")

            if len(hybrid_results) <= 2:
                _log_event(GAPS_LOG, {"query": query, "result_count": len(hybrid_results)})
            _log_event(USAGE_LOG, {"type": "search", "query": query, "result_count": len(hybrid_results)})

            return "\n".join(lines)

    # --- Fallback: keyword matching ---
    matches = []
    for name, entry in skills.items():
        rel = _match_score(name, entry, query)
        if rel > 0:
            matches.append({
                "name": name,
                "type": entry.get("type", "unknown"),
                "description": entry.get("description", "").strip(),
                "tags": entry.get("tags", []),
                "score": entry.get("composite_score"),
                "_rel": rel,
            })

    if not matches:
        _log_event(GAPS_LOG, {"query": query, "result_count": 0})
        _log_event(USAGE_LOG, {"type": "search", "query": query, "result_count": 0})
        return f"No skills found matching '{query}'. Use the list_skills tool to see all available skills."

    # Sort by relevance desc, then composite score desc
    matches.sort(key=lambda m: (-m["_rel"], -(m["score"] or 0)))

    if len(matches) <= 2:
        _log_event(GAPS_LOG, {"query": query, "result_count": len(matches)})
    _log_event(USAGE_LOG, {"type": "search", "query": query, "result_count": len(matches)})

    lines = [f"Found {len(matches)} skill(s) matching '{query}' (keyword):\n"]
    for m in matches:
        lines.append(f"  [{m['type']}] {m['name']}  (score: {m['score']}, relevance: {m['_rel']})")
        lines.append(f"    {m['description']}")
        lines.append(f"    tags: {', '.join(m['tags'])}")
        lines.append("")

    return "\n".join(lines)


@mcp.tool()
def rebuild_search_index() -> str:
    """Force rebuild of the hybrid search index (BM25 + vector embeddings + graph proximity).

    Run this after bulk skill changes or if search results seem stale.
    The index auto-rebuilds when the registry changes, but this forces an
    immediate rebuild and reports status.
    """
    global _search_index, _search_index_mtime

    try:
        from search_index import HybridSearchIndex
    except ImportError:
        return (
            "Hybrid search requires optional dependencies.\n"
            "Install with:  pip install rank-bm25 sentence-transformers numpy\n"
            "Or:  pip install 'skill-library[search]'\n\n"
            "Search will continue to use keyword matching as fallback."
        )

    try:
        registry = load_registry()
    except RuntimeError as e:
        return str(e)

    idx = HybridSearchIndex(SKILLS_DIR, registry, DATA_DIR)
    status = idx.build()

    try:
        _search_index = idx
        _search_index_mtime = REGISTRY_PATH.stat().st_mtime
    except OSError:
        pass

    lines = [
        "=== Search Index Rebuilt ===",
        f"Skills indexed: {status['skills_indexed']}",
        f"BM25: {'ready' if status['bm25'] else 'unavailable (pip install rank-bm25)'}",
        f"Vectors: {'ready' if status['vectors'] else 'unavailable (pip install sentence-transformers numpy)'}",
        f"Graph proximity: ready",
        f"Build time: {status['build_time_ms']}ms",
    ]
    return "\n".join(lines)


@mcp.tool(meta={"anthropic/maxResultSizeChars": 500000})
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
    if skill_path is None:
        return f"Skill file not found for '{skill_name}' — check registry location field."

    content = read_file_safe(skill_path)
    parts = [f"=== SKILL: {skill_name} ===\n\n{content}"]

    # Read reference files if requested
    if include_references:
        refs_dir = Path(skill_path).parent / "references"
        if refs_dir.exists():
            ref_files = sorted(refs_dir.rglob("*.md"))
            if ref_files:
                parts.append(f"\n\n=== REFERENCE DOCUMENTS ({len(ref_files)}) ===")
                for ref_file in ref_files:
                    label = ref_file.relative_to(refs_dir)
                    parts.append(f"\n--- {label} ---\n")
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


@mcp.tool(meta={"anthropic/maxResultSizeChars": 500000})
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


@mcp.tool(meta={"anthropic/maxResultSizeChars": 500000})
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
        if domain_name == "_meta":
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
        if domain_name == "_meta":
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
def update_skill_metadata(
    skill_name: str,
    manual_rating: int | None = None,
    manual_notes: str | None = None,
    health_status: str | None = None,
    status: str | None = None,
    parent: str | None = None,
) -> str:
    """Update a skill's metadata fields in the registry.

    Use this to set a manual quality rating, override health status, change
    a skill's parent, or mark a skill as deprecated. Only the fields you
    provide are updated — everything else stays the same.

    Args:
        skill_name: The skill to update (e.g. "color-theory").
        manual_rating: Manual quality score 1-100 (overrides auto_score in composite).
        manual_notes: Short note explaining the manual rating.
        health_status: Override health — "healthy", "warning", or "critical".
            This is a manual override that recalibrate_scores.py will preserve
            (it won't be silently overwritten by auto-classification). Pass
            "auto" to clear the override and hand health back to the classifier.
        status: Lifecycle status — "active" or "deprecated".
        parent: Name of the parent skill (must exist in registry, or pass "" to clear).
    """
    VALID_HEALTH = {"healthy", "warning", "critical"}
    # "auto" is an input-only sentinel that clears a manual override.
    VALID_HEALTH_INPUT = VALID_HEALTH | {"auto"}
    VALID_STATUS = {"active", "deprecated"}

    # Validate inputs before touching the registry
    if manual_rating is not None and not 1 <= manual_rating <= 100:
        return "manual_rating must be between 1 and 100."
    if health_status is not None and health_status not in VALID_HEALTH_INPUT:
        return f"health_status must be one of: {', '.join(sorted(VALID_HEALTH_INPUT))}."
    if status is not None and status not in VALID_STATUS:
        return f"status must be one of: {', '.join(sorted(VALID_STATUS))}."

    try:
        registry = _load_registry_mutable()
    except RuntimeError as e:
        return str(e)
    skills = registry.get("skills", {})

    if skill_name not in skills:
        return f"Skill '{skill_name}' not found in registry."

    if parent is not None and parent != "" and parent not in skills:
        return f"Parent '{parent}' not found in registry."

    entry = skills[skill_name]
    changes = []

    if manual_rating is not None:
        entry["manual_rating"] = manual_rating
        # Recompute composite: 60% auto + 40% manual when manual is set
        auto = entry.get("auto_score", 50)
        entry["composite_score"] = int(auto * 0.6 + manual_rating * 0.4)
        changes.append(f"manual_rating={manual_rating}, composite_score={entry['composite_score']}")

    if manual_notes is not None:
        entry["manual_notes"] = manual_notes
        changes.append(f"manual_notes set")

    if health_status is not None:
        if health_status == "auto":
            # Clear the manual override; recalibrate_scores.py will recompute
            # health from score/usage/freshness on its next run.
            entry["manual_health"] = None
            changes.append("health_status=auto (manual override cleared)")
        else:
            # Record the override so the auto-classifier preserves it.
            entry["manual_health"] = health_status
            entry["health_status"] = health_status
            changes.append(f"health_status={health_status} (manual override)")

    if status is not None:
        entry["status"] = status
        if status == "active":
            # Clear stale deprecation metadata so get_skill_details won't show
            # contradictory data (e.g. status=active + deprecated_date=yesterday).
            entry["deprecated_date"] = None
            entry["deprecation_reason"] = None
            entry["replacement_skill"] = None
        changes.append(f"status={status}")

    if parent is not None:
        old_parent = entry.get("parent")
        new_parent = parent if parent != "" else None
        entry["parent"] = new_parent
        # Maintain the denormalized referenced_by index on both old and new parents.
        # Without this the parent→child back-reference silently drifts — see the
        # same pattern in add_skill_dependency (line ~2056) and scaffold_skill.
        if old_parent and old_parent in skills and old_parent != new_parent:
            refs = skills[old_parent].get("referenced_by", [])
            if skill_name in refs:
                refs.remove(skill_name)
        if new_parent and new_parent in skills and old_parent != new_parent:
            refs = skills[new_parent].setdefault("referenced_by", [])
            if skill_name not in refs:
                refs.append(skill_name)
        changes.append(f"parent={'(cleared)' if parent == '' else parent}")

    if not changes:
        return "No fields provided to update. Pass at least one keyword argument."

    try:
        atomic_write_registry(registry)
    except OSError as e:
        return f"Failed to write registry: {e}"

    return f"Updated {skill_name}: {', '.join(changes)}."


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


@mcp.tool(meta={"anthropic/maxResultSizeChars": 500000})
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

    # usage.jsonl mixes skill loads and search events; "no analytics" must
    # reflect the skill-load subset, not the raw event stream.
    if not list(iter_skill_uses(usage_events)) and not feedback_events and not gap_events:
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

    # Usage counts — skill loads only; search events are excluded
    skill_uses = list(iter_skill_uses(usage_events))
    usage_counts: dict[str, int] = {}
    for e in skill_uses:
        s = e["skill"]
        usage_counts[s] = usage_counts.get(s, 0) + 1

    if usage_counts:
        sorted_usage = sorted(usage_counts.items(), key=lambda x: x[1], reverse=True)
        lines.append(f"Total skill loads: {len(skill_uses)}")
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

        for s, ratings in sorted(fb_by_skill.items(), key=lambda x: sum(x[1]) / max(len(x[1]), 1), reverse=True):
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
# Impact analysis
# ---------------------------------------------------------------------------

_TIER_LABELS = {1: "WILL BREAK", 2: "LIKELY AFFECTED", 3: "MAY NEED REVIEW"}


@mcp.tool()
def analyze_impact(
    skill_name: str,
    direction: str = "upstream",
    max_depth: int = 3,
) -> str:
    """Analyze the blast radius of changing or deprecating a skill.

    Traces the dependency graph to find all skills that would be affected.
    Use before making significant changes to highly-connected skills.

    Args:
        skill_name: The skill to analyze.
        direction:  "upstream" (default) — who depends on me?
                    "downstream" — what do I depend on?
        max_depth:  How many hops to trace (1-5, default 3).
    """
    if direction not in ("upstream", "downstream"):
        return "direction must be 'upstream' or 'downstream'."

    try:
        registry = load_registry()
    except RuntimeError as e:
        return str(e)
    skills = registry.get("skills", {})

    if skill_name not in skills:
        return f"Skill '{skill_name}' not found in registry."

    result = blast_radius(skills, skill_name, direction, max_depth)

    lines = [
        f"=== Impact Analysis: {skill_name} ({direction}) ===",
        f"Risk level: {result['risk']}",
        f"Total affected: {result['total_affected']} skill(s) across {result['domains_hit']} domain(s)",
        "",
    ]

    if not result["tiers"]:
        lines.append("No skills affected — this skill has no " +
                      ("dependents." if direction == "upstream" else "dependencies."))
        return "\n".join(lines)

    for depth in sorted(result["tiers"]):
        label = _TIER_LABELS.get(depth, f"DEPTH {depth}")
        tier_entries = result["tiers"][depth]
        lines.append(f"--- Tier {depth}: {label} ({len(tier_entries)} skill(s)) ---")
        for e in sorted(tier_entries, key=lambda x: x["domain"]):
            lines.append(f"  [{e['domain']}] {e['skill']}  (via {e['via']})")
        lines.append("")

    if result["risk"] in ("HIGH", "CRITICAL"):
        lines.append(
            "Recommendation: Review all Tier 1 skills before proceeding. "
            "Consider updating dependents or providing a replacement skill."
        )

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Community detection
# ---------------------------------------------------------------------------

@mcp.tool()
def detect_communities() -> str:
    """Detect algorithmic communities in the skill dependency graph using Leiden.

    Compares emergent communities against manual domain assignments to surface
    fragmented domains, natural cross-domain bridges, and cohesion issues.
    Requires python-igraph and leidenalg (pip install python-igraph leidenalg).
    """
    try:
        import igraph as ig
        import leidenalg
    except ImportError:
        return (
            "Community detection requires optional dependencies.\n"
            "Install with:  pip install python-igraph leidenalg\n"
            "Or:  pip install 'skill-library[graph]'"
        )

    try:
        registry = load_registry()
    except RuntimeError as e:
        return str(e)
    skills = registry.get("skills", {})

    # Build node list (active skills only)
    names = [n for n, e in skills.items() if e.get("status") == "active"]
    if len(names) < 3:
        return "Too few active skills to detect communities."

    name_to_idx = {n: i for i, n in enumerate(names)}
    name_set = set(names)

    # Build undirected edges
    edges = set()
    for name in names:
        entry = skills[name]
        for dep in entry.get("depends_on", []):
            if dep in name_set:
                a, b = name_to_idx[name], name_to_idx[dep]
                edges.add((min(a, b), max(a, b)))
        for ref in entry.get("referenced_by", []):
            if ref in name_set:
                a, b = name_to_idx[name], name_to_idx[ref]
                edges.add((min(a, b), max(a, b)))

    G = ig.Graph(n=len(names), edges=list(edges), directed=False)
    partition = leidenalg.find_partition(
        G, leidenalg.RBConfigurationVertexPartition, resolution_parameter=1.0
    )

    # Analyze communities
    communities = []
    community_members_all: set[str] = set()
    for comm_id, members in enumerate(partition):
        if len(members) < 2:
            continue
        member_names = [names[i] for i in members]
        community_members_all.update(member_names)
        domains = Counter(_get_domain(skills[n]) for n in member_names)

        subgraph = G.subgraph(members)
        internal_edges = subgraph.ecount()
        total_incident = sum(G.degree(m) for m in members)
        external_edges = total_incident - 2 * internal_edges
        total = internal_edges + external_edges
        cohesion = internal_edges / total if total > 0 else 0.0

        communities.append({
            "id": comm_id,
            "size": len(members),
            "members": sorted(member_names),
            "cohesion": round(cohesion, 3),
            "dominant_domain": domains.most_common(1)[0][0],
            "domain_mix": dict(domains.most_common()),
            "is_cross_domain": len(domains) > 1,
        })

    communities.sort(key=lambda c: -c["size"])
    singletons = [n for n in names if n not in community_members_all]

    # Domain alignment
    domain_skills: dict[str, list[str]] = {}
    for n in names:
        d = _get_domain(skills[n])
        domain_skills.setdefault(d, []).append(n)

    # Format output
    lines = [
        f"=== Community Detection Report ===",
        f"Skills: {len(names)}, Edges: {len(edges)}, "
        f"Communities: {len(communities)}, Singletons: {len(singletons)}, "
        f"Modularity: {partition.modularity:.4f}",
        "",
    ]

    for c in communities:
        cross = " [CROSS-DOMAIN]" if c["is_cross_domain"] else ""
        lines.append(
            f"Community {c['id']}: {c['size']} skills, "
            f"cohesion {c['cohesion']:.2f}{cross}"
        )
        lines.append(f"  Domains: {c['domain_mix']}")
        shown = c["members"][:8]
        lines.append(
            f"  Members: {', '.join(shown)}"
            + (f" (+{c['size'] - 8} more)" if c["size"] > 8 else "")
        )
        lines.append("")

    lines.append("--- Domain Alignment ---")
    for domain, d_skills in sorted(domain_skills.items()):
        comm_assignments: Counter = Counter()
        for s in d_skills:
            for c in communities:
                if s in c["members"]:
                    comm_assignments[c["id"]] += 1
                    break
        if comm_assignments:
            dominant = comm_assignments.most_common(1)[0][1]
            alignment = dominant / len(d_skills)
        else:
            alignment = 0.0
        frag = " FRAGMENTED" if len(comm_assignments) >= 3 else ""
        lines.append(
            f"  {domain}: {len(d_skills)} skills, "
            f"alignment {alignment:.0%}, "
            f"{len(comm_assignments)} communities{frag}"
        )

    if singletons:
        lines.append(f"\nIsolates ({len(singletons)}): {', '.join(singletons[:10])}"
                      + ("..." if len(singletons) > 10 else ""))

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Write tools
# ---------------------------------------------------------------------------

import copy
import re
import shutil
import subprocess
import tempfile
from datetime import date


_SLUG_RE = re.compile(r"^[a-z][a-z0-9-]*[a-z0-9]$")
_FILENAME_RE = re.compile(r"^[a-zA-Z0-9][a-zA-Z0-9._-]*\.md$")
_VALID_TYPES = {"knowledge", "director", "orchestrator", "action", "observer"}
_TEMPLATE_MAP = {
    "knowledge": "knowledge-skill.md",
    "action": "action-skill.md",
    "director": "director-skill.md",
    "orchestrator": "orchestrator-skill.md",
    "observer": "knowledge-skill.md",  # fallback — no dedicated template exists
}
_SCRIPTS_DIR = PROJECT_ROOT / "scripts"
_TEMPLATES_DIR = SKILLS_DIR / "infrastructure" / "skill-scaffold" / "templates"


def _load_registry_mutable() -> dict:
    """Return a deep copy of the registry for write tools.

    Write tools must never mutate the cached registry object directly.
    If a write fails after in-place mutation, the cache would be poisoned
    with uncommitted changes for the rest of the process lifetime.
    Deep-copying means mutations only affect the local copy; the cache is
    invalidated naturally by mtime after a successful atomic write.
    """
    return copy.deepcopy(load_registry())


def _run_script(
    script_name: str,
    *args,
    timeout: int = 15,
    errors: list | None = None,
) -> dict | None:
    """Run a bash script and return parsed JSON stdout, or None on failure.

    Pass a list as `errors` to capture failure details (stderr or exception
    message). Callers can then include these in their return strings.
    """
    try:
        result = subprocess.run(
            ["bash", str(_SCRIPTS_DIR / script_name), *args],
            capture_output=True, text=True, timeout=timeout,
        )
        if errors is not None and result.stderr.strip():
            errors.append(result.stderr.strip())
        if result.returncode != 0:
            if errors is not None:
                errors.append(f"{script_name} exited with code {result.returncode}")
            return None
        return json.loads(result.stdout)
    except (subprocess.TimeoutExpired, json.JSONDecodeError, OSError) as e:
        if errors is not None:
            errors.append(str(e))
        return None


def _write_file_atomic(path: Path, content: str) -> None:
    """Write content to path atomically (temp file in same dir + os.replace)."""
    tmp_path = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", dir=path.parent, suffix=".tmp", delete=False
        ) as tmp:
            tmp.write(content)
            tmp_path = tmp.name
        os.replace(tmp_path, path)
    except OSError:
        if tmp_path:
            try:
                os.unlink(tmp_path)
            except Exception:
                pass
        raise


def _count_refs(refs_dir: Path) -> int:
    """Count non-.gitkeep files in a references/ directory (recurses into subdirs)."""
    if not refs_dir.exists():
        return 0
    return sum(1 for f in refs_dir.rglob("*") if f.is_file() and f.name != ".gitkeep")


def _parse_frontmatter_description(content: str) -> str:
    """Extract the description value from SKILL.md YAML frontmatter."""
    in_fm = False
    fm_lines = []
    count = 0
    for line in content.splitlines():
        if line.strip() == "---":
            count += 1
            if count == 1:
                in_fm = True
                continue
            else:
                break
        if in_fm:
            fm_lines.append(line)

    # Find description field (may be multi-line with > or |)
    desc_lines = []
    in_desc = False
    for line in fm_lines:
        if re.match(r"^description\s*:", line):
            # Inline value after the colon
            # Strip the YAML block scalar indicator (> or |) only when it
            # appears at the end of the line (followed only by whitespace).
            # This avoids corrupting inline descriptions that start with '>'.
            rest = re.sub(r"^description\s*:\s*(?:[>|](?=\s*$))?\s*", "", line).strip()
            if rest:
                desc_lines.append(rest)
            in_desc = True
        elif in_desc:
            if line.startswith(" ") or line.startswith("\t"):
                desc_lines.append(line.strip())
            else:
                break

    return " ".join(desc_lines).strip()


@mcp.tool()
def scaffold_skill(
    name: str,
    skill_type: str,
    domain: str,
    description: str,
    parent: str | None = None,
    subdomain: str | None = None,
) -> str:
    """Create a new skill directory with a SKILL.md scaffold and register it.

    Reads the appropriate template for the skill type, substitutes placeholders,
    writes the file atomically, computes initial metrics, and adds the skill to
    the registry and network.domains map.

    Args:
        name: Slug for the skill (lowercase, hyphens, e.g. "fermentation-chemistry").
        skill_type: One of "knowledge", "director", "orchestrator", "action", "observer".
        domain: Existing domain in the registry (e.g. "sommelier", "design").
        description: 15-100 word description starting with an action verb.
        parent: Optional parent skill name (must exist and be active in registry).
        subdomain: Optional subdomain tag (e.g. "tasting-evaluation").
    """
    # ── Validation ────────────────────────────────────────────────────────
    if not _SLUG_RE.match(name):
        return f"Name '{name}' is not a valid slug. Use lowercase letters, digits, and hyphens only (min 2 chars, no leading/trailing hyphens)."

    if skill_type not in _VALID_TYPES:
        return f"skill_type must be one of: {', '.join(sorted(_VALID_TYPES))}."

    try:
        registry = _load_registry_mutable()
    except RuntimeError as e:
        return str(e)
    skills = registry.get("skills", {})

    if name in skills:
        return f"Skill '{name}' already exists in the registry."

    existing = list(SKILLS_DIR.rglob(f"{name}/SKILL.md"))
    if existing:
        return f"Skill '{name}' already exists on disk at {existing[0]}."

    domains_map = registry.get("network", {}).get("domains", {})
    if domain not in domains_map:
        return f"Domain '{domain}' does not exist. Valid domains: {', '.join(sorted(domains_map))}."

    desc_words = len(description.split())
    if desc_words < 15:
        return f"Description is too short ({desc_words} words). Minimum is 15 words."
    if desc_words > 100:
        return f"Description is too long ({desc_words} words). Maximum is 100 words."

    if parent is not None:
        parent_entry = skills.get(parent)
        if parent_entry is None:
            return f"Parent '{parent}' not found in registry."
        if parent_entry.get("status") != "active":
            return f"Parent '{parent}' is deprecated and cannot be used as a parent."

    # ── Read template ──────────────────────────────────────────────────────
    template_file = _TEMPLATES_DIR / _TEMPLATE_MAP[skill_type]
    try:
        template = template_file.read_text()
    except OSError as e:
        return f"Could not read template for type '{skill_type}': {e}"

    observer_note = ""
    if skill_type == "observer":
        observer_note = " (Note: no dedicated observer template exists; used knowledge-skill.md as fallback.)"

    title = name.replace("-", " ").title()
    content = (
        template
        .replace("{{SKILL_NAME}}", name)
        .replace("{{DESCRIPTION}}", description)
        .replace("{{SKILL_TITLE}}", title)
        .replace("{{SKILL_SUBTITLE}}", "[Add subtitle]")
        .replace("{{DESCRIPTION_EXPANDED}}", "[Expand description here]")
        .replace("{{TOOLS}}", "Bash, Read, Write")
    )

    # ── Write SKILL.md ─────────────────────────────────────────────────────
    skill_dir = SKILLS_DIR / domain / name
    try:
        skill_dir.mkdir(parents=True, exist_ok=False)
    except FileExistsError:
        return f"Directory '{skill_dir}' already exists on disk."
    except OSError as e:
        return f"Failed to create skill directory: {e}"

    skill_path = skill_dir / "SKILL.md"
    try:
        _write_file_atomic(skill_path, content)
    except OSError as e:
        # Clean up the directory we just created
        try:
            shutil.rmtree(skill_dir)
        except Exception:
            pass
        return f"Failed to write SKILL.md: {e}"

    # ── Get initial metrics via analyze-skill.sh ───────────────────────────
    metrics_data = _run_script("analyze-skill.sh", str(skill_path))
    if metrics_data:
        metrics = {
            "word_count": metrics_data.get("word_count", 0),
            "body_words": metrics_data.get("body_words", 0),
            "section_count": metrics_data.get("section_count", 0),
            "reference_files": metrics_data.get("reference_files", 0),
            "example_files": metrics_data.get("example_files", 0),
            "script_files": metrics_data.get("script_files", 0),
            "template_files": metrics_data.get("template_files", 0),
            "estimated_tokens_total": metrics_data.get("estimated_tokens_total", 0),
            "description_words": metrics_data.get("description_words", desc_words),
        }
    else:
        metrics = {
            "word_count": 0, "body_words": 0, "section_count": 0,
            "reference_files": 0, "example_files": 0, "script_files": 0,
            "template_files": 0, "estimated_tokens_total": 0,
            "description_words": desc_words,
        }

    # ── Build registry entry ───────────────────────────────────────────────
    today = date.today().isoformat()
    tags = [f"domain:{domain}", f"level:{skill_type}"]
    if subdomain:
        tags.append(f"subdomain:{subdomain}")

    entry: dict = {
        "name": name,
        "description": description,
        "location": f"skills/{domain}/{name}/SKILL.md",
        "plugin": f"skill-{domain}",
        "type": skill_type,
        "source": "self",
        "context_mode": "inline",
        "invocation": "both",
        "version": "1.0.0",
        "metrics": metrics,
        "health_status": "healthy",
        "last_checked": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "status": "active",
        "deprecated_date": None,
        "replacement_skill": None,
        "deprecation_reason": None,
        "auto_score": 0,
        "manual_rating": None,
        "manual_notes": None,
        "composite_score": 0,
        "depends_on": [],
        "referenced_by": [],
        "shares_references_with": [],
        "forked_from": None,
        "forked_into": [],
        "tags": tags,
        "created": today,
        "last_modified": today,
        "parent": parent,
    }

    auto = compute_auto_score(entry, Counter(), 0, {})
    entry["auto_score"] = auto
    entry["composite_score"] = auto

    # ── Update registry ────────────────────────────────────────────────────
    skills[name] = entry
    domains_map[domain].append(name)

    # Maintain the denormalized referenced_by index on the parent.
    # Without this the parent silently loses track of its children — see
    # the same pattern in add_skill_dependency (line ~2056).
    if parent:
        parent_entry = skills.get(parent)
        if parent_entry is not None:
            refs = parent_entry.setdefault("referenced_by", [])
            if name not in refs:
                refs.append(name)

    try:
        atomic_write_registry(registry)
    except OSError as e:
        return (
            f"SKILL.md was written to {skill_path} but the registry update failed: {e}. "
            f"Run sync-registry.py --apply to recover."
        )

    # ── Post-write validation ──────────────────────────────────────────────
    val = _run_script("validate-structure.sh", str(skill_dir))
    issues_str = ""
    if val:
        issues = val.get("issues", [])
        if issues:
            lines = [f"\nValidation ({len(issues)} issue(s)):"]
            for iss in issues:
                sev = iss.get("severity", "info").upper()
                lines.append(f"  [{sev}] {iss.get('message', '')}")
            issues_str = "\n".join(lines)

    return (
        f"Created skill '{name}' ({skill_type}) in domain '{domain}'.\n"
        f"  Path:  {skill_path}\n"
        f"  Score: {auto} (auto)\n"
        f"  Words: {metrics['body_words']}, tokens: ~{metrics['estimated_tokens_total']}"
        + (f"\n  Observer note:{observer_note}" if observer_note else "")
        + issues_str
    )


@mcp.tool()
def add_reference_doc(
    skill_name: str,
    filename: str,
    content: str,
) -> str:
    """Add a markdown reference document to a skill's references/ directory.

    Reference docs provide supplementary material (quick-reference sheets,
    deep-dives, methodology notes) that keep the main SKILL.md concise.
    The skill's registry metrics are updated to reflect the new file count.

    Args:
        skill_name: The skill to add the reference to (e.g. "color-theory").
        filename: Filename ending in .md (e.g. "quick-reference.md").
        content: Full markdown content of the reference document.
    """
    # ── Validation ────────────────────────────────────────────────────────
    try:
        registry = _load_registry_mutable()
    except RuntimeError as e:
        return str(e)
    skills = registry.get("skills", {})
    entry = skills.get(skill_name)

    if not entry:
        return f"Skill '{skill_name}' not found in registry."
    if entry.get("status") == "deprecated":
        return f"Skill '{skill_name}' is deprecated. Cannot add reference docs to deprecated skills."

    if not _FILENAME_RE.match(filename):
        return (
            f"Invalid filename '{filename}'. Must end in .md and contain only "
            "alphanumeric characters, dots, underscores, or hyphens."
        )
    if not content.strip():
        return "Content must not be empty."

    skill_path = resolve_skill_path(entry, skill_name)
    if skill_path is None:
        return f"Skill file not found for '{skill_name}'."

    # ── Write file ─────────────────────────────────────────────────────────
    refs_dir = (Path(skill_path).parent / "references").resolve()
    if not refs_dir.is_relative_to(PROJECT_ROOT):
        return f"Refusing to write outside project root: {refs_dir}"
    refs_dir_was_new = not refs_dir.exists()
    refs_dir.mkdir(exist_ok=True)
    target = (refs_dir / filename).resolve()
    if not target.is_relative_to(refs_dir):
        return f"Refusing to write outside references directory: {target}"
    overwrite_note = " (overwrote existing file)" if target.exists() else ""

    try:
        _write_file_atomic(target, content)
    except OSError as e:
        # If we created the directory and the write failed, remove the empty dir
        if refs_dir_was_new:
            try:
                refs_dir.rmdir()
            except Exception:
                pass
        return f"Failed to write reference file: {e}"

    # ── Update registry metrics ────────────────────────────────────────────
    new_count = _count_refs(refs_dir)
    entry.setdefault("metrics", {})["reference_files"] = new_count
    entry["last_modified"] = date.today().isoformat()

    # ── Refresh health_status from validate-structure.sh ───────────────────
    # Without this, adding refs that fix structural warnings leaves stale
    # "warning" health flags from prior validations. Mirrors the convention
    # in update_skill_content (line ~1834): warning if any warnings else healthy.
    # Note: validate-structure.sh exits non-zero on critical issues but still
    # emits JSON — we parse stdout regardless of exit code, unlike _run_script.
    health_note = ""
    try:
        vresult = subprocess.run(
            ["bash", str(_SCRIPTS_DIR / "validate-structure.sh"), str(refs_dir.parent)],
            capture_output=True, text=True, timeout=15,
        )
        val = json.loads(vresult.stdout) if vresult.stdout.strip() else None
    except (subprocess.TimeoutExpired, json.JSONDecodeError, OSError):
        val = None
    if val:
        severities = {iss.get("severity") for iss in val.get("issues", [])}
        if "critical" in severities:
            new_health = "critical"
        elif "warning" in severities:
            new_health = "warning"
        else:
            new_health = "healthy"
        old_health = entry.get("health_status")
        entry["health_status"] = new_health
        if old_health != new_health:
            health_note = f"\n  Health: {old_health} → {new_health}"

    try:
        atomic_write_registry(registry)
    except OSError as e:
        return f"File written but registry update failed: {e}"

    return (
        f"Added '{filename}' to {skill_name}/references/{overwrite_note}.\n"
        f"  Reference files: {new_count}"
        f"{health_note}"
    )


@mcp.tool()
def recalibrate_scores(
    skill_names: list[str] | None = None,
    dry_run: bool = False,
) -> str:
    """Recompute auto_score and composite_score using the multi-factor model.

    Factors: structure (20%), depth (25%), connectivity (20%),
    freshness (15%), usage (10%), feedback (10%).

    Never overwrites manual_rating or manual_notes. When manual_rating is set,
    composite_score = auto*0.6 + manual*0.4; otherwise composite_score = auto_score.

    Args:
        skill_names: Skills to recalibrate. If omitted, recalibrates all skills.
        dry_run: If True, compute and return the diff table without writing.
    """
    try:
        registry = _load_registry_mutable()
    except RuntimeError as e:
        return str(e)
    skills = registry.get("skills", {})

    if skill_names is not None:
        unknown = [n for n in skill_names if n not in skills]
        if unknown:
            return f"Unknown skill(s): {', '.join(unknown)}."
        targets = skill_names
    else:
        targets = list(skills.keys())

    # Build analytics lookups
    usage_events = load_log(USAGE_LOG)
    feedback_events = load_log(FEEDBACK_LOG)
    usage_counts: Counter = Counter(e["skill"] for e in iter_skill_uses(usage_events))
    feedback_ratings: dict[str, list[int]] = {}
    for e in feedback_events:
        s, r = e.get("skill"), e.get("rating")
        if s and r is not None:
            feedback_ratings.setdefault(s, []).append(r)
    max_usage = max(usage_counts.values(), default=1)
    now = datetime.now(timezone.utc)  # computed once, consistent across all skills

    changes = []
    for name in targets:
        entry = skills[name]
        metrics = entry.get("metrics", {})

        s_struct = score_structure(metrics)
        s_depth = score_depth(metrics)
        s_conn = score_connectivity(entry)
        s_fresh = score_freshness(entry, now)
        s_usage = score_usage(name, usage_counts, max_usage)
        s_fb = score_feedback(name, feedback_ratings)

        new_auto = round(
            s_struct * 0.20 + s_depth * 0.25 + s_conn * 0.20
            + s_fresh * 0.15 + s_usage * 0.10 + s_fb * 0.10
        )
        manual = entry.get("manual_rating")
        new_composite = int(new_auto * 0.6 + manual * 0.4) if manual is not None else new_auto
        old_composite = entry.get("composite_score", 0)

        changes.append({
            "name": name,
            "old": old_composite,
            "new": new_composite,
            "delta": new_composite - old_composite,
            "breakdown": [s_struct, s_depth, s_conn, s_fresh, s_usage, s_fb],
        })

        if not dry_run:
            entry["auto_score"] = new_auto
            entry["composite_score"] = new_composite

    changed = [c for c in changes if c["delta"] != 0]

    if not dry_run and changed:
        try:
            atomic_write_registry(registry)
        except OSError as e:
            return f"Failed to write registry: {e}"

    # Build output
    changed.sort(key=lambda c: abs(c["delta"]), reverse=True)
    lines = [
        f"Recalibrated {len(targets)} skill(s) — {len(changed)} changed"
        + (" (dry run)" if dry_run else "") + ".\n"
    ]
    if changed:
        lines.append(f"{'Skill':<40} {'Old':>4} {'New':>4} {'Δ':>5}  [S   D   C   F   U  Fb]")
        lines.append("-" * 75)
        for c in changed[:30]:
            b = c["breakdown"]
            sign = "+" if c["delta"] > 0 else ""
            lines.append(
                f"{c['name']:<40} {c['old']:>4} {c['new']:>4} {sign}{c['delta']:>4}  "
                f"[{b[0]:>3} {b[1]:>3} {b[2]:>3} {b[3]:>3} {b[4]:>3} {b[5]:>3}]"
            )
        if len(changed) > 30:
            lines.append(f"  ... and {len(changed) - 30} more")
    else:
        lines.append("No score changes needed.")

    return "\n".join(lines)


@mcp.tool()
def update_skill_content(
    skill_name: str,
    new_content: str,
    change_note: str,
) -> str:
    """Replace a skill's SKILL.md content with validation gating.

    Validates the new content against structure rules before writing.
    Refuses to write if any critical issues are found (e.g. missing frontmatter,
    invalid description, word count over limit). Updates registry metrics
    and last_modified after writing.

    Args:
        skill_name: The skill to update (e.g. "color-theory").
        new_content: Full new SKILL.md content (complete replacement, not a diff).
        change_note: Brief description of what changed (for the return summary).
    """
    # ── Validation ────────────────────────────────────────────────────────
    try:
        registry = _load_registry_mutable()
    except RuntimeError as e:
        return str(e)
    skills = registry.get("skills", {})
    entry = skills.get(skill_name)

    if not entry:
        return f"Skill '{skill_name}' not found in registry."
    if entry.get("status") == "deprecated":
        return f"Skill '{skill_name}' is deprecated. Use update_skill_metadata to change its status first."

    # Parse frontmatter description
    description = _parse_frontmatter_description(new_content)
    if not description:
        return "Could not find a 'description' field in the frontmatter. Ensure SKILL.md has valid YAML frontmatter."

    desc_words = len(description.split())
    if desc_words < 15:
        return f"Description in frontmatter is too short ({desc_words} words). Minimum is 15."
    if desc_words > 100:
        return f"Description in frontmatter is too long ({desc_words} words). Maximum is 100."

    # Check name in frontmatter
    name_match = re.search(r"^name\s*:\s*(.+)$", new_content[:500], re.MULTILINE)
    if name_match:
        fm_name = name_match.group(1).strip().strip('"\'')
        if fm_name != skill_name:
            return f"Frontmatter 'name' field is '{fm_name}' but expected '{skill_name}'. They must match."

    skill_path_str = resolve_skill_path(entry, skill_name)
    if skill_path_str is None:
        return f"Skill file not found for '{skill_name}'."
    skill_path = Path(skill_path_str)

    # ── Pre-validation gate ────────────────────────────────────────────────
    # Name the inner dir after the skill so validate-structure.sh's
    # name-matches-directory check doesn't produce a false-positive warning.
    tmp_parent = None
    critical_issues = []
    warnings = []
    info_notes = []
    script_errors: list[str] = []
    try:
        tmp_parent = Path(tempfile.mkdtemp())
        tmp_dir = tmp_parent / skill_name
        tmp_dir.mkdir()
        (tmp_dir / "SKILL.md").write_text(new_content)

        # Copy existing references/ so the word-count/references warning is accurate
        refs_src = skill_path.parent / "references"
        if refs_src.exists():
            shutil.copytree(refs_src, tmp_dir / "references")

        val = _run_script("validate-structure.sh", str(tmp_dir), errors=script_errors)
        if val:
            for iss in val.get("issues", []):
                sev = iss.get("severity", "info")
                msg = iss.get("message", "")
                if sev == "critical":
                    critical_issues.append(msg)
                elif sev == "warning":
                    warnings.append(msg)
                else:
                    info_notes.append(msg)
        else:
            # Script unavailable or returned non-JSON — proceed but warn
            detail = f": {script_errors[0]}" if script_errors else ""
            warnings.append(f"validate-structure.sh could not be run{detail}; content written without validation.")
    finally:
        if tmp_parent:
            try:
                shutil.rmtree(tmp_parent)
            except Exception:
                pass

    if critical_issues:
        lines = [f"Cannot update '{skill_name}' — {len(critical_issues)} critical issue(s) found:"]
        for msg in critical_issues:
            lines.append(f"  [CRITICAL] {msg}")
        if warnings:
            lines.append(f"\nAdditional warnings (fix these too):")
            for msg in warnings:
                lines.append(f"  [WARNING] {msg}")
        return "\n".join(lines)

    # ── Write SKILL.md ─────────────────────────────────────────────────────
    try:
        _write_file_atomic(skill_path, new_content)
    except OSError as e:
        return f"Failed to write SKILL.md: {e}"

    # ── Update registry metrics ────────────────────────────────────────────
    metrics_data = _run_script("analyze-skill.sh", str(skill_path))
    if metrics_data:
        entry["metrics"] = {
            "word_count": metrics_data.get("word_count", 0),
            "body_words": metrics_data.get("body_words", 0),
            "section_count": metrics_data.get("section_count", 0),
            "reference_files": metrics_data.get("reference_files", 0),
            "example_files": metrics_data.get("example_files", 0),
            "script_files": metrics_data.get("script_files", 0),
            "template_files": metrics_data.get("template_files", 0),
            "estimated_tokens_total": metrics_data.get("estimated_tokens_total", 0),
            "description_words": metrics_data.get("description_words", desc_words),
        }

    entry["description"] = description
    entry["last_modified"] = date.today().isoformat()
    entry["health_status"] = "warning" if warnings else "healthy"

    try:
        atomic_write_registry(registry)
    except OSError as e:
        return f"SKILL.md written but registry update failed: {e}"

    metrics = entry.get("metrics", {})
    result_lines = [
        f"Updated '{skill_name}': {change_note}",
        f"  Words: {metrics.get('body_words', '?')}, tokens: ~{metrics.get('estimated_tokens_total', '?')}",
        f"  Health: {entry['health_status']}",
    ]
    if warnings:
        result_lines.append(f"  Warnings ({len(warnings)}):")
        for w in warnings:
            result_lines.append(f"    [WARNING] {w}")
    if info_notes:
        result_lines.append(f"  Notes ({len(info_notes)}):")
        for n in info_notes:
            result_lines.append(f"    [INFO] {n}")

    # Impact warning for highly-connected skills
    refs = entry.get("referenced_by", [])
    if len(refs) >= 4:
        impact = blast_radius(skills, skill_name, "upstream", max_depth=2)
        result_lines.append(
            f"\n  Heads up: {impact['total_affected']} skill(s) depend on this "
            f"({impact['risk']} risk). Run analyze_impact for full details."
        )

    return "\n".join(result_lines)


@mcp.tool()
def deprecate_skill(
    skill_name: str,
    reason: str,
    replacement_skill: str | None = None,
) -> str:
    """Safely deprecate a skill with orphan and dependent detection.

    Sets status to 'deprecated', records the reason and date, and optionally
    points to a replacement skill. Scans the registry for dependents (skills
    with this skill as their parent or in their depends_on) and surfaces them
    as warnings. Does NOT remove the skill from network.domains (preserves
    domain maturity history).

    Args:
        skill_name: The skill to deprecate.
        reason: Short explanation of why it's being deprecated.
        replacement_skill: Optional name of the skill that supersedes this one.
    """
    if not reason.strip():
        return "A reason is required for deprecation."

    try:
        registry = _load_registry_mutable()
    except RuntimeError as e:
        return str(e)
    skills = registry.get("skills", {})
    entry = skills.get(skill_name)

    if not entry:
        return f"Skill '{skill_name}' not found in registry."
    if entry.get("status") == "deprecated":
        return f"Skill '{skill_name}' is already deprecated."

    if replacement_skill is not None:
        rep_entry = skills.get(replacement_skill)
        if rep_entry is None:
            return f"Replacement skill '{replacement_skill}' not found in registry."
        if rep_entry.get("status") != "active":
            return f"Replacement skill '{replacement_skill}' is not active."

    # Scan for dependents
    parent_orphans = [
        n for n, e in skills.items()
        if e.get("parent") == skill_name and n != skill_name
    ]
    dep_users = [
        n for n, e in skills.items()
        if skill_name in e.get("depends_on", []) and n != skill_name
    ]

    # Compute blast radius before writing (so exceptions don't lose the report)
    impact = blast_radius(skills, skill_name, "upstream", max_depth=3)

    today = date.today().isoformat()
    entry["status"] = "deprecated"
    entry["health_status"] = "warning"
    entry["deprecated_date"] = today
    entry["deprecation_reason"] = reason
    entry["replacement_skill"] = replacement_skill
    entry["last_modified"] = today

    try:
        atomic_write_registry(registry)
    except OSError as e:
        return f"Failed to write registry: {e}"

    lines = [f"Deprecated '{skill_name}'."]
    lines.append(f"  Reason: {reason}")
    if replacement_skill:
        lines.append(f"  Replacement: {replacement_skill}")

    # Blast radius report
    if impact["total_affected"] > 0:
        lines.append(f"\n  Blast radius: {impact['risk']} — "
                      f"{impact['total_affected']} skill(s) across "
                      f"{impact['domains_hit']} domain(s)")
        for depth in sorted(impact["tiers"]):
            label = _TIER_LABELS.get(depth, f"Depth {depth}")
            names = [e["skill"] for e in impact["tiers"][depth]]
            lines.append(f"    Tier {depth} ({label}): {', '.join(names)}")

    if parent_orphans:
        lines.append(f"\n  Warning — {len(parent_orphans)} skill(s) have this as their parent:")
        for n in parent_orphans:
            lines.append(f"    {n}")
        lines.append("  Update their 'parent' field with update_skill_metadata.")
    if dep_users:
        lines.append(f"\n  Warning — {len(dep_users)} skill(s) depend on this skill:")
        for n in dep_users:
            lines.append(f"    {n}")
        lines.append("  Update their 'depends_on' with add_skill_dependency(remove=True).")

    return "\n".join(lines)


@mcp.tool()
def add_skill_dependency(
    skill_name: str,
    depends_on: str,
    remove: bool = False,
) -> str:
    """Add or remove a dependency relationship between two skills.

    Maintains the bidirectional graph atomically: updates both
    source["depends_on"] and target["referenced_by"] in a single write.
    Checks for circular dependencies before adding. Both operations are
    idempotent.

    Args:
        skill_name: The skill that depends on (or will no longer depend on) another.
        depends_on: The skill being depended upon.
        remove: If True, remove the relationship instead of adding it.
    """
    try:
        registry = _load_registry_mutable()
    except RuntimeError as e:
        return str(e)
    skills = registry.get("skills", {})

    if skill_name not in skills:
        return f"Skill '{skill_name}' not found in registry."
    if depends_on not in skills:
        return f"Skill '{depends_on}' not found in registry."
    if skill_name == depends_on:
        return "A skill cannot depend on itself."

    source = skills[skill_name]
    target = skills[depends_on]
    today = date.today().isoformat()

    if not remove:
        # Idempotency check
        if depends_on in source.get("depends_on", []):
            return f"Dependency already exists: {skill_name} → {depends_on}."

        # Circular dependency check (BFS from depends_on).
        # Mark nodes as visited on enqueue (not dequeue) to prevent a node
        # from being added to the queue multiple times on dense graphs.
        visited = {depends_on}
        queue = deque()
        for n in skills.get(depends_on, {}).get("depends_on", []):
            if n not in visited:
                visited.add(n)
                queue.append(n)
        while queue:
            node = queue.popleft()
            if node == skill_name:
                return (
                    f"Adding this dependency would create a cycle: "
                    f"{skill_name} → {depends_on} → ... → {skill_name}. "
                    f"Check the depends_on chain starting from '{depends_on}'."
                )
            for n in skills.get(node, {}).get("depends_on", []):
                if n not in visited:
                    visited.add(n)
                    queue.append(n)

        source.setdefault("depends_on", []).append(depends_on)
        target.setdefault("referenced_by", []).append(skill_name)
        action = f"Added dependency: {skill_name} → {depends_on}."
    else:
        # Idempotency check
        if depends_on not in source.get("depends_on", []):
            return f"Dependency not found: {skill_name} → {depends_on}."

        source["depends_on"].remove(depends_on)
        if skill_name in target.get("referenced_by", []):
            target["referenced_by"].remove(skill_name)
        action = f"Removed dependency: {skill_name} → {depends_on}."

    source["last_modified"] = today
    target["last_modified"] = today

    try:
        atomic_write_registry(registry)
    except OSError as e:
        return f"Failed to write registry: {e}"

    # Cross-domain warning
    def _domain(entry: dict) -> str:
        for tag in entry.get("tags", []):
            if tag.startswith("domain:"):
                return tag.split(":", 1)[1]
        return ""

    source_domain = _domain(source)
    target_domain = _domain(target)
    cross = (
        f"\n  Note: cross-domain dependency ({source_domain} → {target_domain})."
        if source_domain and target_domain and source_domain != target_domain
        else ""
    )

    return action + cross


# ---------------------------------------------------------------------------
# Remote mode: remove write tools (keeps read-only surface for claude.ai)
# ---------------------------------------------------------------------------

_WRITE_TOOLS = {
    "update_skill_metadata",
    "scaffold_skill",
    "add_reference_doc",
    "recalibrate_scores",
    "update_skill_content",
    "deprecate_skill",
    "add_skill_dependency",
}

if REMOTE_MODE:
    for _name in _WRITE_TOOLS:
        mcp.remove_tool(_name)


# ---------------------------------------------------------------------------
# Run
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Skill Library MCP Server")
    parser.add_argument(
        "--remote", action="store_true",
        help="Enable remote mode (HTTP transport, read-only tools)",
    )
    parser.add_argument(
        "--transport",
        choices=["stdio", "sse", "streamable-http"],
        default=None,
        help="Transport protocol (default: stdio local, streamable-http remote)",
    )
    parser.add_argument("--host", default="0.0.0.0", help="Bind host (default: 0.0.0.0)")
    parser.add_argument("--port", type=int, default=8742, help="Bind port (default: 8742)")
    args = parser.parse_args()

    # --remote flag also sets REMOTE_MODE for tool gating
    if args.remote and not REMOTE_MODE:
        REMOTE_MODE = True
        for _name in _WRITE_TOOLS:
            try:
                mcp.remove_tool(_name)
            except Exception:
                pass
        # Disable DNS rebinding protection (missed at import time)
        mcp.settings.transport_security = TransportSecuritySettings(
            enable_dns_rebinding_protection=False,
        )
        # Switch streamable-http into stateless / JSON-response mode so the
        # transport survives Cloud Run cpu-throttling. Settings are read when
        # the session manager is lazily constructed inside streamable_http_app(),
        # which happens during mcp.run(...) below — so this still takes effect.
        mcp.settings.stateless_http = True
        mcp.settings.json_response = True

    # Resolve transport: explicit flag wins, otherwise infer from mode
    transport = args.transport or ("streamable-http" if (args.remote or REMOTE_MODE) else "stdio")

    # In remote mode, mount the maintenance HTTP router (health + /maint/*).
    # Stdio mode skips this: no HTTP server exists for extra routes.
    if transport != "stdio":
        try:
            import maintenance
            maintenance.register(mcp)
        except Exception as _e:
            # Surface but don't prevent startup — MCP protocol still works.
            logging.warning("maintenance router failed to mount: %s", _e)

    if transport == "stdio":
        mcp.run()
    else:
        mcp.settings.host = args.host
        mcp.settings.port = args.port
        mcp.run(transport=transport)
