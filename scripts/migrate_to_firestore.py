#!/usr/bin/env python3
"""
migrate_to_firestore.py — Push local data files into Firestore.

Reads:
  data/registry.json   → Firestore 'skills' collection + 'meta/registry' doc
  data/usage.jsonl     → Firestore 'usage' collection
  data/gaps.jsonl      → Firestore 'gaps' collection
  data/evolution.jsonl → Firestore 'evolution' collection
                       → Firestore 'evolution_daily' collection (per-date rollup;
                         what the dashboards read, so a page load costs ~90 reads
                         instead of the full ~27k evolution docs)
  data/changelogs.json → Firestore 'changelogs' collection

Usage:
  pip install firebase-admin
  python3 scripts/migrate_to_firestore.py [--project skill-library-prod] [--dry-run]

Requires either:
  - GOOGLE_APPLICATION_CREDENTIALS env var pointing to a service account key, OR
  - gcloud auth application-default login (ADC)
"""

import argparse
import json
import os
import sys
from pathlib import Path

import subprocess

# Soft-fail so test_migrate_to_firestore.py can import the helpers below
# without requiring firebase-admin. main() re-checks and exits if missing.
try:
    import firebase_admin
    from firebase_admin import credentials, firestore
except ImportError:
    firebase_admin = None

try:
    import google.oauth2.credentials as oauth2_creds
except ImportError:
    oauth2_creds = None

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"

# ── Helpers ──────────────────────────────────────────────────────────

def parse_jsonl(path: Path) -> list[dict]:
    """Parse a JSONL file into a list of dicts."""
    if not path.exists():
        print(f"  ⚠ {path.name} not found, skipping")
        return []
    entries = []
    for i, line in enumerate(path.read_text().strip().split("\n")):
        if not line.strip():
            continue
        try:
            entries.append(json.loads(line))
        except json.JSONDecodeError as e:
            print(f"  ⚠ {path.name} line {i+1}: {e}")
    return entries


def batch_write(db, collection: str, docs: list[dict], id_fn=None, dry_run=False):
    """Write docs to a Firestore collection in batches of 500."""
    total = len(docs)
    if total == 0:
        print(f"  {collection}: nothing to write")
        return

    written = 0
    batch = db.batch()
    batch_count = 0

    for i, doc in enumerate(docs):
        if id_fn:
            ref = db.collection(collection).document(id_fn(doc))
        else:
            ref = db.collection(collection).document()
        batch.set(ref, doc)
        batch_count += 1

        if batch_count >= 500 or i == total - 1:
            if not dry_run:
                batch.commit()
            written += batch_count
            print(f"  {collection}: {written}/{total} docs {'(dry-run)' if dry_run else 'written'}")
            batch = db.batch()
            batch_count = 0

    print(f"  ✓ {collection}: {total} docs total")


def build_skill_docs(registry: dict) -> list[dict]:
    """Per-skill docs: dict(skill) pass-through + domain/name enrichment."""
    skills = registry.get("skills", {})
    network_domains = registry.get("network", {}).get("domains", {})
    skill_domain_map = {}
    for domain, skill_names in network_domains.items():
        for sname in skill_names:
            skill_domain_map[sname] = domain
    docs = []
    for name, skill in skills.items():
        doc = dict(skill)
        doc["domain"] = skill_domain_map.get(name, "unknown")
        doc["name"] = name
        docs.append(doc)
    return docs


def build_evolution_daily(evolution: list[dict], registry: dict) -> list[dict]:
    """Roll up raw evolution rows into one summary doc per date.

    The dashboards only need, per date: a snapshot count and the average
    composite_score per domain (for the stacked growth chart). Reading the raw
    `evolution` collection (~27k docs and growing) on every page load is the
    dominant Firestore read cost; this rollup (~one doc per active day) is what
    they read instead.

    Semantics are kept identical to what the client used to compute from the raw
    docs: rows are first deduped by (skill, date, event) — the same key
    `evo_id()` uses, so the deduped set matches the Firestore `evolution`
    collection exactly — then grouped by date. `count` is the number of deduped
    rows that day; `domains[<domain>]` is the mean composite_score over that
    day's rows in that domain (missing scores count as 0, matching the old
    client `e.composite_score || 0`).

    Returns docs shaped: {date, count, domains: {<domain>: <avg>, ...}}.
    Use id_fn=lambda d: d["date"] when writing.
    """
    network_domains = registry.get("network", {}).get("domains", {})
    skill_domain = {}
    for domain, names in network_domains.items():
        for name in names:
            skill_domain[name] = domain

    # Dedup by (skill, date, event), last write wins — mirrors evo_id().
    deduped: dict[tuple, dict] = {}
    for row in evolution:
        skill = row.get("skill", "unknown")
        date = (row.get("date") or "")[:10]
        if not date:
            continue
        event = row.get("event", "snapshot")
        deduped[(skill, date, event)] = row

    # Group by date → per-domain score lists + total count.
    by_date: dict[str, dict] = {}
    for (skill, date, _event), row in deduped.items():
        bucket = by_date.setdefault(date, {"count": 0, "scores": {}})
        bucket["count"] += 1
        domain = skill_domain.get(skill, "unknown")
        bucket["scores"].setdefault(domain, []).append(row.get("composite_score") or 0)

    docs = []
    for date in sorted(by_date):
        bucket = by_date[date]
        domains = {
            d: round(sum(vals) / len(vals), 2)
            for d, vals in bucket["scores"].items()
            if vals
        }
        docs.append({"date": date, "count": bucket["count"], "domains": domains})
    return docs


def build_meta_doc(registry: dict) -> dict:
    """meta/registry doc with explicit/computed fields + pass-through for unknown top-level keys."""
    skills = registry.get("skills", {})
    network_domains = registry.get("network", {}).get("domains", {})
    meta_doc = {
        "schema_version": registry.get("schema_version"),
        "plugin_version": registry.get("plugin_version"),
        "last_scan": registry.get("last_scan"),
        "network_domains": network_domains,
        "skill_count": len(skills),
        "domain_count": len(network_domains),
    }
    # `skills` has its own collection; `network` is denormalized above.
    HANDLED = {"schema_version", "plugin_version", "last_scan", "skills", "network"}
    for key, value in registry.items():
        if key not in HANDLED and key not in meta_doc:
            meta_doc[key] = value
    return meta_doc


# ── Main ─────────────────────────────────────────────────────────────

def get_db(project: str):
    """Firestore client via ADC, falling back to a gcloud access token."""
    from google.cloud import firestore as gcloud_firestore
    try:
        db = gcloud_firestore.Client(project=project)
        db.collection("_ping").limit(1).get()  # test connectivity
        print("  ✓ Connected via Application Default Credentials")
        return db
    except Exception:
        print("  ℹ ADC not found, using gcloud access token...")
        token = subprocess.check_output(
            ["gcloud", "auth", "print-access-token"], text=True
        ).strip()
        gcred = oauth2_creds.Credentials(token=token)
        db = gcloud_firestore.Client(project=project, credentials=gcred)
        print("  ✓ Connected via gcloud token")
        return db


def main():
    parser = argparse.ArgumentParser(description="Migrate local skill data to Firestore")
    parser.add_argument("--project", default="skill-library-prod", help="GCP project ID")
    parser.add_argument("--dry-run", action="store_true", help="Parse and validate without writing")
    args = parser.parse_args()

    if firebase_admin is None:
        print("ERROR: firebase-admin not installed. Run: pip install firebase-admin")
        sys.exit(1)

    print(f"═══ Neural Observatory → Firestore Migration ═══")
    print(f"Project: {args.project}")
    print(f"Data dir: {DATA}")
    print(f"Dry run: {args.dry_run}")
    print()

    # Initialize Firestore client — try ADC, fall back to gcloud token
    db = get_db(args.project)

    # ── 1. Registry → skills collection + meta doc ────────────────
    print("▸ Loading registry.json...")
    registry_path = DATA / "registry.json"
    if not registry_path.exists():
        print("  ERROR: registry.json not found!")
        sys.exit(1)

    registry = json.loads(registry_path.read_text())
    skill_docs = build_skill_docs(registry)
    print(f"  Found {len(skill_docs)} skills")
    batch_write(db, "skills", skill_docs, id_fn=lambda d: d["name"], dry_run=args.dry_run)

    meta_doc = build_meta_doc(registry)
    if not args.dry_run:
        db.collection("meta").document("registry").set(meta_doc)
    print(f"  ✓ meta/registry: written {'(dry-run)' if args.dry_run else ''}")

    # ── 2. Usage events ───────────────────────────────────────────
    # Skill-load events only; search events (type=search, no skill field) stay
    # local. Keeps the Firestore `usage` collection's dashboard semantics intact.
    print("\n▸ Loading usage.jsonl...")
    usage = [e for e in parse_jsonl(DATA / "usage.jsonl") if e.get("skill")]
    batch_write(db, "usage", usage, dry_run=args.dry_run)

    # ── 3. Gaps ───────────────────────────────────────────────────
    print("\n▸ Loading gaps.jsonl...")
    gaps = parse_jsonl(DATA / "gaps.jsonl")
    batch_write(db, "gaps", gaps, dry_run=args.dry_run)

    # ── 4. Evolution snapshots ────────────────────────────────────
    print("\n▸ Loading evolution.jsonl...")
    evolution = parse_jsonl(DATA / "evolution.jsonl")
    # Give each evolution doc a deterministic ID: skill + date
    def evo_id(doc):
        skill = doc.get("skill", "unknown")
        date = doc.get("date", "unknown")[:10]
        event = doc.get("event", "snapshot")
        return f"{skill}_{date}_{event}"
    batch_write(db, "evolution", evolution, id_fn=evo_id, dry_run=args.dry_run)

    # Per-date rollup the dashboards actually read (keeps a page load at ~90
    # reads instead of the full evolution collection).
    evolution_daily = build_evolution_daily(evolution, registry)
    batch_write(db, "evolution_daily", evolution_daily,
                id_fn=lambda d: d["date"], dry_run=args.dry_run)

    # ── 5. Changelogs ─────────────────────────────────────────────
    print("\n▸ Loading changelogs.json...")
    changelog_path = DATA / "changelogs.json"
    if changelog_path.exists():
        changelogs = json.loads(changelog_path.read_text())
        # changelogs is a dict: { skill_name: changelog_data }
        changelog_docs = [
            {"skill": name, "entries": data}
            for name, data in changelogs.items()
        ]
        batch_write(db, "changelogs", changelog_docs,
                    id_fn=lambda d: d["skill"], dry_run=args.dry_run)
    else:
        print("  ⚠ changelogs.json not found, skipping")

    # ── Summary ───────────────────────────────────────────────────
    print()
    print("═══ Migration Summary ═══")
    print(f"  Skills:    {len(skill_docs)}")
    print(f"  Usage:     {len(usage)}")
    print(f"  Gaps:      {len(gaps)}")
    print(f"  Evolution: {len(evolution)} raw → {len(evolution_daily)} daily rollup")
    if changelog_path.exists():
        print(f"  Changelogs: {len(changelogs)}")
    if args.dry_run:
        print("\n  ⚠ DRY RUN — no data was written to Firestore")
        print("  Remove --dry-run to execute the migration")
    else:
        print("\n  ✓ All data written to Firestore!")
        print(f"  Project: {args.project}")
        print(f"  Console: https://console.firebase.google.com/project/{args.project}/firestore")


if __name__ == "__main__":
    main()
