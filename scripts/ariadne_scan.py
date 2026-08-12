#!/usr/bin/env python3
"""ariadne_scan.py — deterministic stale-thread scanner for the ariadne skill.

Reads a user-level config (never committed; see
skills/professional-development/ariadne/references/setup-and-config.md),
sweeps each configured vault's ideas folder, and reports open threads whose
last deliberate touch is older than the staleness threshold.

Staleness source of truth: the `last_touched` frontmatter field (stamped by
ariadne on every triage decision). File mtime is only a fallback for notes
that predate ariadne — mtime alone is unreliable because vault sync and bulk
edits rewrite it wholesale.

Exit code is 0 in every non-crash case, including missing config — the
SessionStart hook depends on that to stay silent rather than failing a
session. Machine consumers should check the `configured` / `matched` fields.

Usage:
  ariadne_scan.py                    # human-readable table, all vaults
  ariadne_scan.py --json             # machine output (used by hook + skill)
  ariadne_scan.py --vault <label>    # restrict to one vault (label or path substring)
  ariadne_scan.py --cwd <path>       # restrict to the vault containing <path>, if any
  ariadne_scan.py --config <file>    # config override (default: $ARIADNE_CONFIG
                                     # or ~/.config/ariadne/config.json)
"""

import argparse
import json
import os
import re
import sys
from datetime import date, datetime
from pathlib import Path

try:
    import yaml  # PyYAML preferred; a real parser, not field-scraping
except ImportError:
    yaml = None

DEFAULT_IDEAS_DIR = "Ideas"
DEFAULT_INDEX_FILE = "_index.md"
DEFAULT_STALE_DAYS = 21
OPEN_STATUSES = {"open", "in-progress"}

FRONTMATTER_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*\n", re.DOTALL)


def parse_frontmatter(text: str) -> dict:
    m = FRONTMATTER_RE.match(text)
    if not m:
        return {}
    block = m.group(1)
    if yaml is not None:
        try:
            data = yaml.safe_load(block)
            return data if isinstance(data, dict) else {}
        except yaml.YAMLError:
            return {}
    # Fallback without PyYAML: top-level scalar keys only, which covers the
    # thread-note contract (type/status/next_step/last_touched/snooze_until).
    data = {}
    for line in block.splitlines():
        kv = re.match(r"^(\w[\w-]*):\s*(.*)$", line)
        if kv:
            data[kv.group(1)] = kv.group(2).strip().strip("\"'")
    return data


def as_date(value) -> date | None:
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    if isinstance(value, str):
        try:
            return datetime.strptime(value.strip()[:10], "%Y-%m-%d").date()
        except ValueError:
            return None
    return None


def scan_vault(vault: dict, global_stale_days: int, today: date) -> dict:
    vault_path = Path(os.path.expanduser(vault["path"]))
    label = vault.get("label") or vault_path.name
    ideas_dir = vault_path / (vault.get("ideas_dir") or DEFAULT_IDEAS_DIR)
    index_file = vault.get("index_file") or DEFAULT_INDEX_FILE
    stale_days = vault.get("stale_days") or global_stale_days

    result = {
        "label": label,
        "path": str(vault_path),
        "exists": ideas_dir.is_dir(),
        "open_count": 0,
        "snoozed_count": 0,
        "stale": [],
    }
    if not result["exists"]:
        return result

    for note in sorted(ideas_dir.glob("*.md")):
        if note.name == index_file or note.name.startswith("_"):
            continue
        try:
            meta = parse_frontmatter(note.read_text(errors="replace"))
        except OSError:
            continue
        if str(meta.get("type", "")).strip() != "idea":
            continue
        status = str(meta.get("status", "")).strip()
        if status not in OPEN_STATUSES:
            continue
        result["open_count"] += 1

        snooze = as_date(meta.get("snooze_until"))
        if snooze and snooze > today:
            result["snoozed_count"] += 1
            continue

        touched = as_date(meta.get("last_touched"))
        touched_source = "last_touched"
        if touched is None:
            touched = date.fromtimestamp(note.stat().st_mtime)
            touched_source = "mtime"
        days_stale = (today - touched).days
        if days_stale < stale_days:
            continue

        result["stale"].append(
            {
                "thread": note.stem,
                "file": str(note),
                "status": status,
                "days_stale": days_stale,
                "next_step": str(meta.get("next_step", "")).strip(),
                "touched_source": touched_source,
                "snooze_wakes": str(snooze) if snooze else None,
            }
        )

    result["stale"].sort(key=lambda t: -t["days_stale"])
    return result


def is_within(child: str, parent: str) -> bool:
    child_r = os.path.realpath(os.path.expanduser(child))
    parent_r = os.path.realpath(os.path.expanduser(parent))
    return child_r == parent_r or child_r.startswith(parent_r + os.sep)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--config", default=os.environ.get(
        "ARIADNE_CONFIG", os.path.expanduser("~/.config/ariadne/config.json")))
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    ap.add_argument("--vault", help="restrict to vault by label or path substring")
    ap.add_argument("--cwd", help="restrict to the vault containing this path")
    args = ap.parse_args()

    def emit(payload: dict, human: str) -> int:
        print(json.dumps(payload) if args.json else human)
        return 0

    config_path = Path(args.config)
    if not config_path.is_file():
        return emit({"configured": False},
                    f"ariadne: no config at {config_path} — see the skill's "
                    "references/setup-and-config.md to create one.")
    try:
        config = json.loads(config_path.read_text())
    except (OSError, json.JSONDecodeError) as e:
        return emit({"configured": False, "error": str(e)},
                    f"ariadne: unreadable config {config_path}: {e}")

    vaults = config.get("vaults", [])
    if args.vault:
        needle = args.vault.lower()
        vaults = [v for v in vaults
                  if needle in (v.get("label") or "").lower()
                  or needle in v.get("path", "").lower()]
    if args.cwd:
        vaults = [v for v in vaults if is_within(args.cwd, v.get("path", ""))]
        if not vaults:
            return emit({"configured": True, "matched": False, "stale_total": 0},
                        "ariadne: current directory is not a configured vault.")

    today = date.today()
    stale_days = config.get("stale_days") or DEFAULT_STALE_DAYS
    reports = [scan_vault(v, stale_days, today) for v in vaults]
    stale_total = sum(len(r["stale"]) for r in reports)
    oldest = max((t["days_stale"] for r in reports for t in r["stale"]), default=0)

    payload = {
        "configured": True,
        "matched": True,
        "generated": str(today),
        "stale_days": stale_days,
        "triage_cap": config.get("triage_cap", 5),
        "stale_total": stale_total,
        "oldest_days": oldest,
        "vaults": reports,
    }
    if args.json:
        print(json.dumps(payload, indent=2))
        return 0

    for r in reports:
        marker = "" if r["exists"] else "  (ideas folder missing)"
        print(f"[{r['label']}] open={r['open_count']} snoozed={r['snoozed_count']} "
              f"stale={len(r['stale'])}{marker}")
        for t in r["stale"]:
            print(f"  {t['days_stale']:>4}d  {t['thread']}  — {t['next_step'] or '(no next step)'}")
    print(f"\n{stale_total} stale thread(s) total"
          + (f", oldest {oldest}d" if stale_total else "") + ".")
    return 0


if __name__ == "__main__":
    sys.exit(main())
