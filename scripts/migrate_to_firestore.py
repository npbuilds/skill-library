#!/usr/bin/env python3
"""
migrate_to_firestore.py — Push local data files into Firestore.

Reads:
  data/registry.json   → Firestore 'skills' collection + 'meta/registry' doc
  data/changelogs.json → Firestore 'changelogs' collection
  data/evolution.jsonl → Firestore 'evolution' collection (legacy; file retired)
                       → Firestore 'evolution_daily' collection (per-date rollup;
                         what the dashboards read, so a page load costs ~90 reads
                         instead of the full ~27k evolution docs)
  data/usage.jsonl     → Firestore 'usage' collection    (--include-telemetry only)
  data/gaps.jsonl      → Firestore 'gaps' collection     (--include-telemetry only)

Usage:
  pip install google-cloud-firestore
  python3 scripts/migrate_to_firestore.py [--project skill-library-prod] [--dry-run]

CI mode (sync-firestore.yml runs this on every merge to main):
  python3 scripts/migrate_to_firestore.py --registry-only --prune --sha <git-sha>

Flags:
  --registry-only     Sync only skills + changelogs + meta/registry (the
                      merge-triggered CI subset; skips evolution + telemetry).
  --prune             With --registry-only: delete Firestore skills/changelogs
                      docs whose IDs are no longer in the registry. Refuses to
                      run if the registry holds fewer than PRUNE_SAFETY_FLOOR
                      skills (protects against a truncated registry wiping the
                      collection).
  --sha SHA           Git commit SHA stamped into meta/registry.synced_sha —
                      the divergence check in daily-firestore.yml compares it
                      against origin/main.
  --include-telemetry ⚠ Push local usage.jsonl/gaps.jsonl with AUTO-GENERATED
                      doc IDs. Re-running DUPLICATES those collections, and
                      after the telemetry pull loop (Phase 3) local jsonl
                      contains rows that ORIGINATED in Firestore — pushing
                      them back double-counts dashboard usage. Backfill/
                      recovery only; never run from CI.

Write ordering (failure-honest): skills + changelogs are upserted first, prune
runs only if every upsert batch committed, and meta/registry is written LAST as
the commit marker. A mid-run failure leaves meta/registry describing the
previous complete snapshot.

Requires either:
  - GOOGLE_APPLICATION_CREDENTIALS env var pointing to a service account key, OR
  - gcloud auth application-default login (ADC), OR
  - a gcloud CLI login (access-token fallback)
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path

try:
    import google.oauth2.credentials as oauth2_creds
except ImportError:
    oauth2_creds = None

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"

# --prune refuses to delete anything if the registry holds fewer skills than
# this — a truncated/corrupt registry must never be able to empty the live
# collection. Library is 522 skills as of 2026-07; revisit if it ever shrinks
# legitimately below this.
PRUNE_SAFETY_FLOOR = 100

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


def list_doc_ids(db, collection: str) -> set[str]:
    """Stream only document IDs from a collection (empty projection — no field
    reads billed beyond the doc scan)."""
    return {snap.id for snap in db.collection(collection).select([]).stream()}


def prune_collection(db, collection: str, keep_ids: set[str], dry_run=False) -> list[str]:
    """Delete docs whose IDs are not in keep_ids. Returns the pruned IDs."""
    existing = list_doc_ids(db, collection)
    stale = sorted(existing - keep_ids)
    if not stale:
        print(f"  {collection}: nothing to prune ({len(existing)} docs all current)")
        return []
    batch = db.batch()
    batch_count = 0
    for i, doc_id in enumerate(stale):
        batch.delete(db.collection(collection).document(doc_id))
        batch_count += 1
        if batch_count >= 500 or i == len(stale) - 1:
            if not dry_run:
                batch.commit()
            batch = db.batch()
            batch_count = 0
    for doc_id in stale:
        print(f"  {collection}: pruned '{doc_id}'{' (dry-run)' if dry_run else ''}")
    print(f"  ✓ {collection}: {len(stale)} stale docs pruned{' (dry-run)' if dry_run else ''}")
    return stale


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


def evo_id(doc: dict) -> str:
    """Deterministic Firestore doc ID for an evolution row: skill_date_event.
    Same key `build_evolution_daily` dedupes on, so the raw `evolution`
    collection and the daily rollup stay consistent."""
    skill = doc.get("skill", "unknown")
    date = (doc.get("date") or "unknown")[:10]
    event = doc.get("event", "snapshot")
    return f"{skill}_{date}_{event}"


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


def build_meta_doc(registry: dict, synced_sha: str | None = None) -> dict:
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
    if synced_sha:
        meta_doc["synced_sha"] = synced_sha
    # `skills` has its own collection; `network` is denormalized above.
    HANDLED = {"schema_version", "plugin_version", "last_scan", "skills", "network"}
    for key, value in registry.items():
        if key not in HANDLED and key not in meta_doc:
            meta_doc[key] = value
    return meta_doc


def load_changelog_docs() -> list[dict]:
    """data/changelogs.json ({skill: entries}) → [{skill, entries}] docs."""
    changelog_path = DATA / "changelogs.json"
    if not changelog_path.exists():
        print("  ⚠ changelogs.json not found, skipping")
        return []
    changelogs = json.loads(changelog_path.read_text())
    return [{"skill": name, "entries": data} for name, data in changelogs.items()]


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


def sync_registry(db, registry: dict, args) -> dict:
    """Upsert skills + changelogs, optionally prune, then write meta/registry
    LAST as the commit marker. Returns summary counts."""
    skill_docs = build_skill_docs(registry)
    print(f"  Found {len(skill_docs)} skills")
    batch_write(db, "skills", skill_docs, id_fn=lambda d: d["name"], dry_run=args.dry_run)

    print("\n▸ Loading changelogs.json...")
    changelog_docs = load_changelog_docs()
    batch_write(db, "changelogs", changelog_docs,
                id_fn=lambda d: d["skill"], dry_run=args.dry_run)

    pruned = []
    if args.prune:
        print("\n▸ Pruning stale docs...")
        if len(skill_docs) < PRUNE_SAFETY_FLOOR:
            print(f"  ✗ REFUSING to prune: registry has only {len(skill_docs)} skills "
                  f"(safety floor: {PRUNE_SAFETY_FLOOR}). Is the registry truncated?")
            sys.exit(1)
        keep_skills = {d["name"] for d in skill_docs}
        pruned += prune_collection(db, "skills", keep_skills, dry_run=args.dry_run)
        if changelog_docs:
            keep_logs = {d["skill"] for d in changelog_docs}
            pruned += prune_collection(db, "changelogs", keep_logs, dry_run=args.dry_run)

    # meta/registry written LAST: the commit marker. If anything above raised,
    # this never runs and the dashboard's headline metadata still describes the
    # previous complete snapshot.
    meta_doc = build_meta_doc(registry, synced_sha=args.sha)
    if not args.dry_run:
        db.collection("meta").document("registry").set(meta_doc)
    print(f"  ✓ meta/registry: written {'(dry-run)' if args.dry_run else ''}"
          f"{f' [synced_sha={args.sha[:12]}…]' if args.sha else ''}")

    return {"skills": len(skill_docs), "changelogs": len(changelog_docs),
            "pruned": len(pruned)}


def main():
    parser = argparse.ArgumentParser(description="Migrate local skill data to Firestore")
    parser.add_argument("--project", default="skill-library-prod", help="GCP project ID")
    parser.add_argument("--dry-run", action="store_true", help="Parse and validate without writing")
    parser.add_argument("--registry-only", action="store_true",
                        help="Sync only skills + changelogs + meta/registry (CI merge subset)")
    parser.add_argument("--prune", action="store_true",
                        help="With --registry-only: delete Firestore docs no longer in the registry")
    parser.add_argument("--sha", default=None,
                        help="Git commit SHA to stamp into meta/registry.synced_sha")
    parser.add_argument("--include-telemetry", action="store_true",
                        help="⚠ Push usage.jsonl/gaps.jsonl (auto-ID docs — re-running "
                             "DUPLICATES them; backfill only, never CI)")
    args = parser.parse_args()

    if args.prune and not args.registry_only:
        parser.error("--prune requires --registry-only")
    if args.include_telemetry and args.registry_only:
        parser.error("--include-telemetry conflicts with --registry-only")

    print(f"═══ Neural Observatory → Firestore Migration ═══")
    print(f"Project: {args.project}")
    print(f"Data dir: {DATA}")
    print(f"Mode: {'registry-only' if args.registry_only else 'full'}"
          f"{' + prune' if args.prune else ''}")
    print(f"Dry run: {args.dry_run}")
    print()

    # Initialize Firestore client — try ADC, fall back to gcloud token
    db = get_db(args.project)

    # ── 1. Registry → skills + changelogs + meta (meta LAST) ─────
    print("▸ Loading registry.json...")
    registry_path = DATA / "registry.json"
    if not registry_path.exists():
        print("  ERROR: registry.json not found!")
        sys.exit(1)
    registry = json.loads(registry_path.read_text())
    summary = sync_registry(db, registry, args)

    usage, gaps, evolution, evolution_daily = [], [], [], []
    if not args.registry_only:
        # ── 2. Evolution snapshots (legacy local file; Firestore-native
        # via daily-firestore.yml — this is a no-op when the file is gone)
        print("\n▸ Loading evolution.jsonl...")
        evolution = parse_jsonl(DATA / "evolution.jsonl")
        batch_write(db, "evolution", evolution, id_fn=evo_id, dry_run=args.dry_run)

        # Per-date rollup the dashboards actually read (keeps a page load at
        # ~90 reads instead of the full evolution collection).
        evolution_daily = build_evolution_daily(evolution, registry)
        batch_write(db, "evolution_daily", evolution_daily,
                    id_fn=lambda d: d["date"], dry_run=args.dry_run)

        # ── 3. Telemetry (opt-in only — auto-ID docs duplicate on re-run,
        # and post-Phase-3 local jsonl contains rows that ORIGINATED in
        # Firestore; pushing them back double-counts dashboard usage) ──
        if args.include_telemetry:
            print("\n  ⚠ --include-telemetry: pushing usage/gaps with auto-generated IDs.")
            print("    Re-running this duplicates those collections. Backfill only.")
            # Skill-load events only; search events (type=search, no skill
            # field) stay local. Keeps dashboard `usage` semantics intact.
            print("\n▸ Loading usage.jsonl...")
            usage = [e for e in parse_jsonl(DATA / "usage.jsonl") if e.get("skill")]
            batch_write(db, "usage", usage, dry_run=args.dry_run)

            print("\n▸ Loading gaps.jsonl...")
            gaps = parse_jsonl(DATA / "gaps.jsonl")
            batch_write(db, "gaps", gaps, dry_run=args.dry_run)

    # ── Summary ───────────────────────────────────────────────────
    print()
    print("═══ Migration Summary ═══")
    print(f"  Skills:     {summary['skills']}")
    print(f"  Changelogs: {summary['changelogs']}")
    if args.prune:
        print(f"  Pruned:     {summary['pruned']}")
    if not args.registry_only:
        print(f"  Evolution:  {len(evolution)} raw → {len(evolution_daily)} daily rollup")
        if args.include_telemetry:
            print(f"  Usage:      {len(usage)}")
            print(f"  Gaps:       {len(gaps)}")
    if args.dry_run:
        print("\n  ⚠ DRY RUN — no data was written to Firestore")
        print("  Remove --dry-run to execute the migration")
    else:
        print("\n  ✓ All data written to Firestore!")
        print(f"  Project: {args.project}")
        print(f"  Console: https://console.firebase.google.com/project/{args.project}/firestore")


if __name__ == "__main__":
    main()
