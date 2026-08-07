#!/usr/bin/env python3
"""
check_firestore_divergence.py — Detect split-brain between git main and Firestore.

sync-firestore.yml stamps meta/registry.synced_sha on every successful sync.
This check (run daily from daily-firestore.yml) alerts when Firestore has
silently fallen behind git — the failure mode the sync workflow's failure
isolation deliberately allows but must never leave undetected.

Alerts (exit 1) iff:
  (a) synced_sha is not an ancestor of HEAD — foreign or rolled-back SHA, or
  (b) synced_sha != HEAD AND the newest commit is older than --max-age-hours —
      there was ample time to sync and it didn't happen. The age condition
      keeps the transient minutes-after-merge window from false-alarming.

A missing synced_sha passes with a notice (pre-rollout state; the first
successful sync-firestore.yml run stamps it).

With ``--require-head``, used as a pre-write safety gate, a missing or merely
lagging synced_sha fails immediately. This prevents a daily job from writing an
aggregate derived from newer Git data while Firestore skills/meta remain older.

Requires: full git history in the checkout (fetch-depth: 0) and Firestore read
access (WIF in CI, ADC/gcloud locally).

Usage:
  python3 scripts/check_firestore_divergence.py [--project skill-library-prod]
                                                [--max-age-hours 6]
                                                [--require-head]
"""

import argparse
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from migrate_to_firestore import get_db  # noqa: E402


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], text=True).strip()


def strict_sync_error(head: str, synced_sha: str | None) -> str | None:
    if not synced_sha:
        return "meta/registry.synced_sha is missing"
    if synced_sha != head:
        return f"meta/registry.synced_sha {synced_sha} does not exactly match HEAD {head}"
    return None


def main() -> None:
    parser = argparse.ArgumentParser(description="Check git↔Firestore sync divergence")
    parser.add_argument("--project", default="skill-library-prod", help="GCP project ID")
    parser.add_argument("--max-age-hours", type=float, default=6.0,
                        help="Alert only when HEAD is older than this and still unsynced")
    parser.add_argument(
        "--require-head",
        action="store_true",
        help="Fail unless meta/registry.synced_sha exactly equals HEAD",
    )
    args = parser.parse_args()

    head = git("rev-parse", "HEAD")
    snap = get_db(args.project).collection("meta").document("registry").get()
    synced_sha = (snap.to_dict() or {}).get("synced_sha") if snap.exists else None

    if args.require_head:
        error = strict_sync_error(head, synced_sha)
        if error:
            print(f"✗ PRE-WRITE DIVERGENCE: {error}. Re-run sync-firestore.yml.")
            sys.exit(1)
        print(f"✓ pre-write check: Firestore synced_sha exactly matches HEAD {head}.")
        return

    if not synced_sha:
        print("ℹ meta/registry.synced_sha not set — pre-rollout state, passing.")
        return

    print(f"HEAD:       {head}")
    print(f"synced_sha: {synced_sha}")

    if synced_sha == head:
        print("✓ Firestore is synced to HEAD.")
        return

    is_ancestor = subprocess.run(
        ["git", "merge-base", "--is-ancestor", synced_sha, head],
        capture_output=True,
    ).returncode == 0
    if not is_ancestor:
        print("✗ DIVERGENCE: synced_sha is not an ancestor of HEAD "
              "(foreign or rolled-back SHA). Re-run sync-firestore.yml.")
        sys.exit(1)

    head_age_hours = (time.time() - int(git("log", "-1", "--format=%ct", "HEAD"))) / 3600
    if head_age_hours > args.max_age_hours:
        behind = git("rev-list", "--count", f"{synced_sha}..{head}")
        print(f"✗ DIVERGENCE: Firestore is {behind} commit(s) behind HEAD, and HEAD "
              f"is {head_age_hours:.1f}h old (> {args.max_age_hours}h) — the sync "
              f"had ample time and didn't happen. Check sync-firestore.yml runs.")
        sys.exit(1)

    print(f"✓ Firestore trails HEAD but HEAD is only {head_age_hours:.1f}h old — "
          "within the normal post-merge window.")


if __name__ == "__main__":
    main()
