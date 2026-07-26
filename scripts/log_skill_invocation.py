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

# (There is deliberately no scan-window constant. See over_session_cap: a fixed
# window made the cap fail open once the log outgrew it.)


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


def _iter_lines_backwards(path: Path, chunk_size: int = 65536):
    """Yield non-empty lines from the end of the file toward the start.

    Streams fixed-size chunks instead of loading the file. Backwards matters:
    the newest rows are the ones the cap check cares about, so the common case
    touches a single chunk no matter how large the log has grown.
    """
    try:
        with open(path, "rb") as f:
            f.seek(0, os.SEEK_END)
            pos = f.tell()
            carry = b""
            while pos > 0:
                step = min(chunk_size, pos)
                pos -= step
                f.seek(pos)
                buf = f.read(step) + carry
                parts = buf.split(b"\n")
                # parts[0] may be a partial line continued in the next (earlier)
                # chunk — hold it back rather than parsing a fragment.
                carry = parts[0]
                for part in reversed(parts[1:]):
                    if part.strip():
                        yield part.decode("utf-8", errors="ignore")
            if carry.strip():
                yield carry.decode("utf-8", errors="ignore")
    except OSError:
        return


def over_session_cap(event: dict, path: Path = USAGE_LOG, cap: int = SESSION_DAILY_CAP) -> bool:
    """True if this (session_id, UTC day) already has `cap` plugin events.

    Scans the whole log backwards, stopping the moment `cap` matches are found.
    Two things this deliberately does NOT do, both of which looked like free
    optimisations and are actually correctness bugs:

    - No fixed line/byte window. An earlier version scanned only the last 2000
      lines, so once a session's rows scrolled past that window the cap silently
      stopped applying — the runaway-loop guard failed open exactly when a
      runaway loop had made the log long. Since recalibrate_scores.py divides by
      max_usage, one inflated skill becomes the denominator and deflates every
      other skill's usage score, so failing open here is worse than the scan.
    - No early break when an older date appears. The log is append-ORDERED but
      not chronological: pull_telemetry_from_firestore.py appends cloud rows
      whose timestamps predate local rows already in the file, so "we reached
      yesterday" never implies "today's rows are all behind us".

    Cost is bounded in practice by the early exit. The worst case is an
    under-cap fire, which scans the whole log; measured on this machine that is
    0.4 ms at 500 rows, 4 ms at 5k, and 33 ms at 50k (~4.5 MB) — linear, and
    the hook fires once per plugin skill load from every project. If it ever
    matters, rotate the log into data/archive/ (the watermark makes rotation
    safe — see pull_telemetry_from_firestore.py); do NOT reintroduce a scan
    window, which is the bug this replaced.
    """
    session = event.get("session_id")
    day = str(event.get("timestamp", ""))[:10]
    if not session or not day:
        return False
    seen = 0
    for line in _iter_lines_backwards(path):
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            continue
        if not isinstance(row, dict):
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
