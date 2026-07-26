#!/usr/bin/env python3
"""
test_migrate_to_firestore.py — Tests for the Firestore migration.

Covers: pass-through of unknown fields (future schema additions land in
Firestore without code changes), synced_sha stamping, and the failure-honest
sync_registry sequence (meta written LAST, prune gated on upsert success,
prune safety floor).

Run: python3 scripts/test_migrate_to_firestore.py
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import migrate_to_firestore as mig
from migrate_to_firestore import (
    build_skill_docs,
    build_meta_doc,
    prune_collection,
    sync_registry,
)


# ── Fake Firestore (records an ordered event log) ───────────────────

class FakeSnap:
    def __init__(self, doc_id):
        self.id = doc_id


class FakeQuery:
    def __init__(self, ids):
        self._ids = ids

    def stream(self):
        return [FakeSnap(i) for i in sorted(self._ids)]


class FakeDocRef:
    def __init__(self, db, collection, doc_id):
        self.db, self.collection, self.doc_id = db, collection, doc_id

    def set(self, doc):
        self.db.events.append(("set", self.collection, self.doc_id))
        self.db.store.setdefault(self.collection, {})[self.doc_id] = doc


class FakeCollection:
    def __init__(self, db, name):
        self.db, self.name = db, name

    def document(self, doc_id=None):
        return FakeDocRef(self.db, self.name, doc_id or f"auto-{len(self.db.events)}")

    def select(self, _fields):
        return FakeQuery(self.db.store.get(self.name, {}).keys())


class FakeBatch:
    def __init__(self, db):
        self.db = db
        self.ops = []

    def set(self, ref, doc):
        self.ops.append(("set", ref, doc))

    def delete(self, ref):
        self.ops.append(("delete", ref))

    def commit(self):
        if self.db.fail_collections & {ref.collection for _, ref, *_ in self.ops}:
            raise RuntimeError("simulated Firestore batch failure")
        for op in self.ops:
            if op[0] == "set":
                _, ref, doc = op
                ref.set(doc)
            else:
                _, ref = op
                self.db.events.append(("delete", ref.collection, ref.doc_id))
                self.db.store.get(ref.collection, {}).pop(ref.doc_id, None)
        self.ops = []


class FakeDB:
    def __init__(self, preexisting=None, fail_collections=None):
        self.store = {k: dict(v) for k, v in (preexisting or {}).items()}
        self.events = []  # ordered (op, collection, doc_id) log
        self.fail_collections = fail_collections or set()

    def collection(self, name):
        return FakeCollection(self, name)

    def batch(self):
        return FakeBatch(self)


def make_args(**overrides):
    defaults = dict(dry_run=False, prune=False, sha=None, registry_only=True)
    defaults.update(overrides)
    return argparse.Namespace(**defaults)


SYNTHETIC_REGISTRY = {
    "schema_version": 2,
    "plugin_version": "1.0.0",
    "last_scan": "2026-05-16T00:00:00Z",
    "_test_unknown_top_level": "passthrough_value",
    "network": {"domains": {"test-domain": ["sample-skill"]}},
    "skills": {
        "sample-skill": {
            "name": "sample-skill",
            "type": "knowledge",
            "_test_passthrough": True,
        },
    },
}


def test_skill_doc_passthrough():
    docs = build_skill_docs(SYNTHETIC_REGISTRY)
    assert len(docs) == 1
    doc = docs[0]
    assert doc["domain"] == "test-domain"
    assert doc.get("_test_passthrough") is True, (
        f"unknown skill field dropped; doc keys: {sorted(doc.keys())}"
    )


def test_meta_doc_passthrough():
    meta = build_meta_doc(SYNTHETIC_REGISTRY)
    assert meta["skill_count"] == 1
    assert meta["network_domains"] == {"test-domain": ["sample-skill"]}
    assert meta.get("_test_unknown_top_level") == "passthrough_value", (
        f"unknown top-level field dropped; meta keys: {sorted(meta.keys())}"
    )
    assert "skills" not in meta and "network" not in meta


def test_meta_doc_synced_sha():
    meta = build_meta_doc(SYNTHETIC_REGISTRY, synced_sha="abc123")
    assert meta["synced_sha"] == "abc123"
    meta_no_sha = build_meta_doc(SYNTHETIC_REGISTRY)
    assert "synced_sha" not in meta_no_sha, "synced_sha must be absent when not passed"


def _big_registry(n=150):
    """Registry above the prune safety floor."""
    return {
        "schema_version": 2,
        "network": {"domains": {"d": [f"skill-{i}" for i in range(n)]}},
        "skills": {f"skill-{i}": {"name": f"skill-{i}"} for i in range(n)},
    }


def _patched_changelogs(docs):
    """Temporarily replace load_changelog_docs (reads the real data dir)."""
    original = mig.load_changelog_docs
    mig.load_changelog_docs = lambda: docs
    return original


def test_meta_written_last():
    db = FakeDB()
    original = _patched_changelogs([{"skill": "skill-0", "entries": []}])
    try:
        sync_registry(db, _big_registry(), make_args(sha="deadbeef"))
    finally:
        mig.load_changelog_docs = original
    assert db.events, "no writes recorded"
    assert db.events[-1] == ("set", "meta", "registry"), (
        f"meta/registry must be the LAST write (commit marker); last was {db.events[-1]}"
    )
    assert db.store["meta"]["registry"]["synced_sha"] == "deadbeef"


def test_prune_removes_stale_and_spares_current():
    stale = {"skills": {"ghost-skill": {}, "skill-0": {}},
             "changelogs": {"ghost-skill": {}}}
    db = FakeDB(preexisting=stale)
    original = _patched_changelogs([{"skill": "skill-0", "entries": []}])
    try:
        summary = sync_registry(db, _big_registry(), make_args(prune=True))
    finally:
        mig.load_changelog_docs = original
    assert "ghost-skill" not in db.store["skills"]
    assert "ghost-skill" not in db.store["changelogs"]
    assert "skill-0" in db.store["skills"]
    assert summary["pruned"] == 2
    # prune events must precede the meta commit marker
    meta_idx = db.events.index(("set", "meta", "registry"))
    delete_idxs = [i for i, e in enumerate(db.events) if e[0] == "delete"]
    assert delete_idxs and max(delete_idxs) < meta_idx


def test_prune_safety_floor():
    db = FakeDB(preexisting={"skills": {"ghost": {}}})
    original = _patched_changelogs([])
    try:
        sync_registry(db, _big_registry(n=50), make_args(prune=True))
        raised = False
    except SystemExit:
        raised = True
    finally:
        mig.load_changelog_docs = original
    assert raised, "prune must refuse when registry is below the safety floor"
    assert "ghost" in db.store["skills"], "nothing may be deleted on refusal"
    assert "meta" not in db.store, "meta must not be written after a refused prune"


def test_upsert_failure_blocks_prune_and_meta():
    db = FakeDB(preexisting={"skills": {"ghost": {}}}, fail_collections={"skills"})
    original = _patched_changelogs([])
    try:
        sync_registry(db, _big_registry(), make_args(prune=True))
        raised = False
    except RuntimeError:
        raised = True
    finally:
        mig.load_changelog_docs = original
    assert raised, "batch failure must propagate"
    assert "ghost" in db.store["skills"], "prune must not run after a failed upsert"
    assert "meta" not in db.store, "meta commit marker must not be written on failure"


def test_prune_collection_noop_when_current():
    db = FakeDB(preexisting={"skills": {"a": {}, "b": {}}})
    pruned = prune_collection(db, "skills", keep_ids={"a", "b"})
    assert pruned == []
    assert set(db.store["skills"]) == {"a", "b"}


def test_parse_jsonl_enforces_list_of_dicts():
    """`"foo"`, `[1,2]`, `123`, `null` are valid JSON but not objects. Every
    consumer treats rows as mappings — build_usage_rollup's totals and
    pull_telemetry's `row.get("_fs_id")` dedupe (which runs in the nightly
    bot-PR job) both raise AttributeError on one — so the parse boundary drops
    them rather than each call site guarding separately."""
    import json as _json
    import tempfile
    from pathlib import Path as _Path
    from migrate_to_firestore import parse_jsonl

    with tempfile.TemporaryDirectory() as d:
        path = _Path(d) / "u.jsonl"
        path.write_text('{"a": 1}\n"bare"\n[1,2]\n123\nnull\ntrue\n{"broken\n{"b": 2}\n')
        rows = parse_jsonl(path)
        assert rows == [{"a": 1}, {"b": 2}], rows
        assert all(isinstance(r, dict) for r in rows)


def main():
    tests = [
        test_parse_jsonl_enforces_list_of_dicts,
        test_skill_doc_passthrough,
        test_meta_doc_passthrough,
        test_meta_doc_synced_sha,
        test_meta_written_last,
        test_prune_removes_stale_and_spares_current,
        test_prune_safety_floor,
        test_upsert_failure_blocks_prune_and_meta,
        test_prune_collection_noop_when_current,
    ]
    failed = 0
    for t in tests:
        try:
            t()
            print(f"  ✓ {t.__name__}")
        except AssertionError as e:
            print(f"  ✗ {t.__name__}: {e}")
            failed += 1
    print(f"\n{len(tests) - failed}/{len(tests)} passed")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
