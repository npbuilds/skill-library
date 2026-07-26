#!/usr/bin/env python3
"""
log_skill_invocation.py — Capture plugin-native skill loads into usage telemetry.

Only the MCP server's get_skill tool logs usage (server.py, _log_event →
data/usage.jsonl). Skills invoked through Claude Code's native Skill tool or a
slash command (/diligence, /six-eyes, a Hermes strategist load) never touch the
MCP server, so they were invisible to recalibrate_scores.py and to the
dashboard. A 2026-07-26 audit found biotech-venture at 1 recorded load despite
heavy daily plugin use.

This is the PostToolUse side of that fix: Claude Code pipes the hook payload on
stdin, we resolve the invoked name against the registry, and append one event to
the same JSONL stream the MCP server writes.

Schema (compatible with shared.iter_skill_uses and pull_telemetry_from_firestore):

    {"session_id": ..., "skill": "asclepius", "type": "orchestrator",
     "source": "plugin", "invoked_as": "diligence",
     "timestamp": "2026-07-26T12:00:00+00:00"}

`source` is new and segments the stream: "plugin" here, "mcp" from server.py.
Legacy rows carry neither and are read as "mcp" (shared.event_source).

Name resolution — deliberately strict, because scoring divides by the max:
  recalibrate_scores.py computes max_usage over every name in usage.jsonl, so a
  foreign plugin name (codex:review sits at 31 invocations) would become the
  denominator and deflate every real skill's usage score. Resolution order:
    1. exact registry name           (six-eyes, cursed-speech, rebalancer)
    2. data/skill_aliases.json       (diligence → asclepius)
    3. our own plugin prefix         (skill-binding-vow:six-eyes → six-eyes)
  Anything unresolved is written WITHOUT a `skill` key — it keeps `skill_raw`
  instead. iter_skill_uses skips it, migrate_to_firestore's e.get("skill")
  filter skips it, so it can never pollute a score or the dashboard; it stays
  in the log as the audit trail of what still needs an alias (--report).

Firestore: this writes local jsonl only. CI syncs Firestore with
--registry-only, and pull_telemetry_from_firestore.py only appends rows
carrying an _fs_id, so local rows never round-trip into duplicates.

Never raises in hook mode: a telemetry failure must not fail the user's tool
call. Exit is always 0 unless --strict is passed (tests, manual debugging).

Usage:
  ... | python3 scripts/log_skill_invocation.py          # PostToolUse hook
  python3 scripts/log_skill_invocation.py --report       # unmapped names seen
  python3 scripts/log_skill_invocation.py --dry-run < payload.json
"""

import argparse
import fcntl
import json
import os
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(os.environ.get("SKILL_LIBRARY_ROOT", Path(__file__).resolve().parent.parent))
DATA = ROOT / "data"
REGISTRY_PATH = DATA / "registry.json"
ALIASES_PATH = DATA / "skill_aliases.json"
USAGE_LOG = DATA / "usage.jsonl"

SOURCE = "plugin"

# Mirrors pull_telemetry_from_firestore.py's --session-daily-cap default. A
# runaway agent loop calling the same skill hundreds of times in one session is
# not 300 units of evidence that the skill is valuable.
SESSION_DAILY_CAP = 50

# Only scan the tail of the log for the cap check — the whole file is loaded
# nowhere in the hot path, and this keeps the hook O(1) as history grows.
CAP_SCAN_LINES = 2000


def load_registry_skills() -> dict:
    """Return registry["skills"], or {} if the registry is unreadable."""
    try:
        return json.loads(REGISTRY_PATH.read_text()).get("skills", {})
    except (OSError, json.JSONDecodeError):
        return {}


def load_aliases() -> dict:
    """Return the invocation-name → registry-name alias map."""
    try:
        return json.loads(ALIASES_PATH.read_text()).get("aliases", {})
    except (OSError, json.JSONDecodeError):
        return {}


def local_plugin_names(skills: dict) -> set[str]:
    """Plugin names owned by this library (registry `plugin` field).

    Used to decide whether a "prefix:name" invocation is ours to strip.
    `skill-binding-vow:six-eyes` is ours; `codex:review` and
    `anthropic-skills:docx` are somebody else's and must stay unresolved.
    """
    return {p for p in (e.get("plugin") for e in skills.values()) if p}


def resolve_skill(raw: str, skills: dict, aliases: dict) -> str | None:
    """Map an invoked name onto a registry skill name, or None if foreign."""
    if not raw:
        return None
    if raw in skills:
        return raw
    aliased = aliases.get(raw)
    if aliased in skills:
        return aliased
    if ":" in raw:
        prefix, _, suffix = raw.rpartition(":")
        if prefix in local_plugin_names(skills):
            if suffix in skills:
                return suffix
            aliased = aliases.get(suffix)
            if aliased in skills:
                return aliased
    return None


def tool_failed(payload: dict) -> bool:
    """True if the Skill call errored — PostToolUse fires either way.

    A successful Skill result is the string "Launching skill: <name>"; an
    unknown or unavailable skill errors instead, and logging that as a load
    would credit a skill that was never read.
    """
    resp = payload.get("tool_response")
    if isinstance(resp, dict):
        return bool(resp.get("is_error") or resp.get("error"))
    if isinstance(resp, str):
        return resp.lstrip().lower().startswith("error")
    return False


def build_event(payload: dict, skills: dict, aliases: dict) -> dict | None:
    """Build one usage event from a PostToolUse payload, or None to skip.

    Returns None for anything that is not a Skill tool invocation — the hook
    matcher already narrows this, but a mis-scoped matcher must not start
    logging Bash calls as skill loads.
    """
    if payload.get("tool_name") != "Skill" or tool_failed(payload):
        return None
    tool_input = payload.get("tool_input") or {}
    raw = (tool_input.get("skill") or "").strip()
    if not raw:
        return None

    event = {
        "session_id": payload.get("session_id", "unknown"),
        "source": SOURCE,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    resolved = resolve_skill(raw, skills, aliases)
    if resolved:
        event["skill"] = resolved
        event["type"] = skills[resolved].get("type", "unknown")
        if resolved != raw:
            event["invoked_as"] = raw
    else:
        # No `skill` key on purpose: unscored, un-synced, still auditable.
        event["skill_raw"] = raw
        event["type"] = "unresolved"
    return event


def _tail_lines(path: Path, limit: int) -> list[str]:
    try:
        with open(path, "rb") as f:
            f.seek(0, os.SEEK_END)
            size = f.tell()
            # ~200 bytes/event; read enough to cover `limit` events.
            window = min(size, limit * 400)
            f.seek(size - window)
            chunk = f.read().decode("utf-8", errors="ignore")
    except OSError:
        return []
    return chunk.splitlines()[-limit:]


def over_session_cap(event: dict, path: Path = USAGE_LOG, cap: int = SESSION_DAILY_CAP) -> bool:
    """True if this (session_id, UTC day) already has `cap` plugin events."""
    session = event.get("session_id")
    day = str(event.get("timestamp", ""))[:10]
    if not session or not day:
        return False
    seen = 0
    for line in _tail_lines(path, CAP_SCAN_LINES):
        line = line.strip()
        if not line:
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            continue
        if (
            row.get("source") == SOURCE
            and row.get("session_id") == session
            and str(row.get("timestamp", ""))[:10] == day
        ):
            seen += 1
            if seen >= cap:
                return True
    return False


def append_event(event: dict, path: Path = USAGE_LOG) -> None:
    """Append one event under an exclusive lock.

    The MCP server appends to this same file from its own process; flock is
    what keeps a hook firing mid-tool-call from interleaving a partial line.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "a") as f:
        fcntl.flock(f, fcntl.LOCK_EX)
        try:
            f.write(json.dumps(event) + "\n")
            f.flush()
        finally:
            fcntl.flock(f, fcntl.LOCK_UN)


def report_unresolved(path: Path = USAGE_LOG) -> str:
    """Summarise plugin invocations that never resolved to a registry skill."""
    if not path.exists():
        return "No usage log yet."
    unresolved: Counter = Counter()
    resolved: Counter = Counter()
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            continue
        if row.get("source") != SOURCE:
            continue
        if row.get("skill"):
            resolved[row["skill"]] += 1
        elif row.get("skill_raw"):
            unresolved[row["skill_raw"]] += 1

    lines = [f"Plugin-source events: {sum(resolved.values())} attributed, "
             f"{sum(unresolved.values())} unresolved."]
    if resolved:
        lines.append("\nAttributed:")
        lines += [f"  {n:<28} {c}" for n, c in resolved.most_common()]
    if unresolved:
        lines.append("\nUnresolved — add to data/skill_aliases.json if these load a library skill:")
        lines += [f"  {n:<28} {c}" for n, c in unresolved.most_common()]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    parser.add_argument("--dry-run", action="store_true",
                        help="Print the event that would be logged, write nothing")
    parser.add_argument("--report", action="store_true",
                        help="Summarise plugin events and unmapped invocation names")
    parser.add_argument("--strict", action="store_true",
                        help="Exit non-zero on failure (default swallows errors)")
    args = parser.parse_args()

    if args.report:
        print(report_unresolved())
        return 0

    try:
        payload = json.loads(sys.stdin.read() or "{}")
    except json.JSONDecodeError as e:
        if args.strict:
            print(f"skill-telemetry: bad hook payload: {e}", file=sys.stderr)
            return 1
        return 0

    try:
        skills = load_registry_skills()
        if not skills:
            # No registry (wrong checkout, mid-rebase) — logging names we
            # cannot verify would be worse than logging nothing.
            return 1 if args.strict else 0
        event = build_event(payload, skills, load_aliases())
        if event is None:
            return 0
        if args.dry_run:
            print(json.dumps(event))
            return 0
        if over_session_cap(event):
            return 0
        append_event(event)
    except Exception as e:  # never break the user's tool call
        print(f"skill-telemetry: {e}", file=sys.stderr)
        return 1 if args.strict else 0
    return 0


if __name__ == "__main__":
    sys.exit(main())
