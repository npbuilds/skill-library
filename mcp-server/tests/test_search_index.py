"""Regression tests for HybridSearchIndex internals."""

import json
import os
import time

import pytest

np = pytest.importorskip("numpy")

from search_index import _atomic_write_npy, _get_registry_hash  # noqa: E402


def test_atomic_write_npy_round_trip(tmp_path):
    """np.save auto-appends '.npy'; ensure the atomic helper doesn't leave
    an empty stub at the target path while the real array lands at a sibling."""
    target = tmp_path / "embeddings.npy"
    arr = np.arange(12, dtype=np.float32).reshape(3, 4)

    _atomic_write_npy(target, arr)

    assert target.stat().st_size > 0, f"target wrote 0 bytes; orphans: {list(tmp_path.iterdir())}"
    assert np.array_equal(np.load(target), arr)
    assert list(tmp_path.iterdir()) == [target], "stray tempfile left behind"


def test_registry_hash_invariant_to_mtime(tmp_path):
    """The cache key must depend on registry CONTENT, not its filesystem
    mtime. Otherwise the embedding cache pre-built into a Docker image is
    invalidated at runtime when overlayfs reports a different mtime."""
    reg = tmp_path / "registry.json"
    reg.write_text('{"skills": {}}')
    h1 = _get_registry_hash(tmp_path)

    # Mutate mtime without changing content (touch). The hash must not change.
    later = time.time() + 3600
    os.utime(reg, (later, later))
    h2 = _get_registry_hash(tmp_path)

    assert h1 == h2 != ""


def test_registry_hash_changes_with_content(tmp_path):
    """The cache key must invalidate when the registry's content changes."""
    reg = tmp_path / "registry.json"
    reg.write_text('{"skills": {"a": 1}}')
    h1 = _get_registry_hash(tmp_path)

    reg.write_text('{"skills": {"a": 2}}')
    h2 = _get_registry_hash(tmp_path)

    assert h1 != h2 and h1 and h2


def test_registry_hash_missing_file_returns_empty(tmp_path):
    """A missing registry returns an empty string — the cache check below
    treats that as a miss, forcing a rebuild rather than silently using a
    stale cache."""
    assert _get_registry_hash(tmp_path) == ""


# ---------------------------------------------------------------------------
# Single-signal RRF floor (silent-degradation regression)
# ---------------------------------------------------------------------------

from pathlib import Path  # noqa: E402

from search_index import HybridSearchIndex, _MIN_RRF_SCORE  # noqa: E402


@pytest.fixture(autouse=True)
def _no_real_model(monkeypatch):
    """Keep build() from loading a real SentenceTransformer in these tests.
    Tests that exercise the embedding path inject a fake via idx._model and
    call _build_or_load_embeddings directly (it doesn't gate on HAS_VECTORS)."""
    import search_index as si
    monkeypatch.setattr(si, "HAS_VECTORS", False)


def _make_index(tmp_path, names=("alpha-skill", "beta-skill", "gamma-skill")):
    """Index over a tiny on-disk registry; signals controlled by the test."""
    skills = {}
    for n in names:
        loc = f"skills/test/{n}/SKILL.md"
        f = tmp_path / loc
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text(f"# {n}\n\nBody of {n}.\n")
        skills[n] = {
            "name": n,
            "description": f"The {n} description.",
            "location": loc,
            "status": "active",
            "depends_on": [],
            "referenced_by": [],
        }
    # Wire a chain so graph proximity has edges: alpha — beta — gamma
    skills["alpha-skill"]["depends_on"] = ["beta-skill"]
    skills["beta-skill"]["depends_on"] = ["gamma-skill"]

    data_dir = tmp_path / "data"
    data_dir.mkdir(exist_ok=True)
    (data_dir / "registry.json").write_text("{}")

    return HybridSearchIndex(
        skills_dir=tmp_path / "skills",
        registry={"skills": skills},
        data_dir=data_dir,
    )


def test_degraded_install_results_survive_floor(tmp_path):
    """With BM25 unavailable, signals rarely corroborate: rank-1 RRF = 1/61
    ≈ 0.0164 < 0.02. The old fixed floor filtered every result, so search()
    returned [] and the server fell back to weak keyword matching. The
    scaled floor must let top hits through in this degraded mode."""
    idx = _make_index(tmp_path)
    idx.build()
    # Degraded install: no BM25, no vectors — graph proximity only.
    idx._bm25 = None
    idx._embeddings = None

    results = idx.search("anything", recent_skills=["alpha-skill"])
    assert results, "degraded-install search must not be filtered to empty"
    assert results[0]["name"] == "beta-skill"  # 1 hop from alpha


def test_full_floor_with_two_ranking_signals(tmp_path):
    """When ≥2 signals produce rankings, the full 0.02 floor applies — a
    lone single-list long-tail match stays filtered so gap detection keeps
    firing on out-of-scope queries."""
    idx = _make_index(tmp_path)
    idx.build()
    idx._embeddings = None
    if idx._bm25 is None:
        pytest.skip("rank-bm25 not installed")

    # BM25 matches alpha (query term in body); graph ranks beta/gamma from
    # alpha seed. Two signals rank, but no skill appears in BOTH lists, so
    # every fused score is single-list: rank-1 = 0.0164 < 0.02 — all filtered
    # under the full (≥2-signal) floor.
    results = idx.search("alpha", recent_skills=["alpha-skill"])
    for r in results:
        assert r["rrf_score"] >= _MIN_RRF_SCORE


def test_bm25_only_single_signal_survives_floor(tmp_path):
    """BM25 as the SOLE ranking signal (vectors absent, no graph seed — the
    mode the CI eval runs in) must return real matches, not be filtered to
    empty by the full floor. Regression guard for the CI 0.000-recall bug."""
    idx = _make_index(tmp_path)
    idx.build()
    idx._embeddings = None
    if idx._bm25 is None:
        pytest.skip("rank-bm25 not installed")

    # No recent_skills → graph inert. BM25 is the only signal.
    results = idx.search("alpha", recent_skills=None)
    assert any(r["name"] == "alpha-skill" for r in results), \
        "single-signal BM25 match must survive the floor"


# ---------------------------------------------------------------------------
# Embedding rebuild locking
# ---------------------------------------------------------------------------


class _FakeModel:
    """Stands in for SentenceTransformer; counts encode calls."""

    def __init__(self, delay=0.05):
        self.delay = delay
        self.calls = 0

    def encode(self, texts, show_progress_bar=False):
        self.calls += 1
        time.sleep(self.delay)
        return np.zeros((len(texts), 8), dtype=np.float32)


def test_concurrent_rebuild_encodes_once(tmp_path):
    """Two concurrent builders must serialize on the lock file; the second
    must find the first's cache (double-checked) instead of re-encoding."""
    import threading

    idx_a = _make_index(tmp_path)
    idx_b = _make_index(tmp_path)
    idx_a.build()
    idx_b.build()
    # _names must match for cache validity across the two builders
    assert idx_a._names == idx_b._names

    model = _FakeModel()
    idx_a._model = model
    idx_b._model = model

    corpus = [f"{n}: text" for n in idx_a._names]
    keys = [(n, "desc") for n in idx_a._names]
    results = [None, None]

    def run(idx, slot):
        results[slot] = idx._build_or_load_embeddings(corpus, keys)

    t1 = threading.Thread(target=run, args=(idx_a, 0))
    t2 = threading.Thread(target=run, args=(idx_b, 1))
    t1.start(); t2.start()
    t1.join(); t2.join()

    assert results[0] is not None and results[1] is not None
    assert model.calls == 1, "second builder should hit the cache, not re-encode"


def test_rebuild_lock_releases_on_failure(tmp_path):
    """A failed rebuild must not leave the lock held or a partial cache."""
    idx = _make_index(tmp_path)
    idx.build()

    class _Boom:
        def encode(self, texts, show_progress_bar=False):
            raise RuntimeError("encode failed")

    idx._model = _Boom()
    assert idx._build_or_load_embeddings(["x"], [("x", "desc")]) is None

    # Lock must be reacquirable: a healthy rebuild succeeds afterwards.
    idx2 = _make_index(tmp_path)
    idx2.build()
    idx2._model = _FakeModel()
    corpus = [f"{n}: text" for n in idx2._names]
    keys = [(n, "desc") for n in idx2._names]
    assert idx2._build_or_load_embeddings(corpus, keys) is not None


# ---------------------------------------------------------------------------
# Chunked multi-vector embeddings (PR2)
# ---------------------------------------------------------------------------

from search_index import (  # noqa: E402
    _split_passages,
    _extract_chunks,
    _EMBED_CACHE_SCHEMA,
)


def test_split_passages_respects_word_cap():
    body = " ".join(f"w{i}" for i in range(400))  # one 400-word section
    passages = _split_passages(body, max_words=150, max_chunks=8)
    assert all(len(p.split()) <= 150 for p in passages)
    assert len(passages) == 3  # 400 / 150 → 3 passages


def test_split_passages_caps_chunk_count():
    body = " ".join(f"w{i}" for i in range(5000))
    passages = _split_passages(body, max_words=150, max_chunks=8)
    assert len(passages) == 8  # hard cap honored


def test_split_passages_splits_on_headings():
    body = "## Intro\nalpha beta\n\n## Method\ngamma delta\n\n## Results\nepsilon"
    passages = _split_passages(body, max_words=150, max_chunks=8)
    # Three headings → three passages; heading text drops out, body words stay.
    assert len(passages) == 3
    assert any("alpha" in p for p in passages)
    assert any("epsilon" in p for p in passages)


def test_extract_chunks_desc_first(tmp_path):
    sd = tmp_path / "skills" / "x"
    sd.mkdir(parents=True)
    (sd / "SKILL.md").write_text("---\nname: x\n---\n## Body\nhello world here\n")
    chunks = _extract_chunks(sd, "x-skill", "the description")
    assert chunks[0][0] == "desc"
    assert chunks[0][1] == "x-skill: the description"
    assert any(k.startswith("body:") for k, _ in chunks)
    # Every chunk is name-prefixed so it carries skill identity.
    assert all(t.startswith("x-skill: ") for _, t in chunks)


def test_max_pool_returns_each_skill_once(tmp_path, monkeypatch):
    """A skill with multiple body chunks must appear exactly once in vector
    results, scored by its best-matching chunk."""
    import search_index as si

    monkeypatch.setattr(si, "HAS_VECTORS", True)
    idx = _make_index(tmp_path)

    # Deterministic fake model: encode returns a fixed 4-dim vector per text,
    # so we control which chunk is "closest" to the query.
    class _Model:
        def encode(self, texts, show_progress_bar=False):
            out = []
            for t in texts:
                if "query" in t:
                    out.append([1.0, 0.0, 0.0, 0.0])
                elif "beta-skill" in t:
                    out.append([0.9, 0.1, 0.0, 0.0])  # high sim to query
                else:
                    out.append([0.0, 1.0, 0.0, 0.0])  # orthogonal
            return np.array(out, dtype=np.float32)

    idx._model = _Model()
    idx.build()  # builds chunk embeddings via the fake model
    assert idx._embeddings is not None
    assert len(idx._chunk_skill_idx) == idx._embeddings.shape[0]
    assert len(idx._chunk_skill_idx) > len(idx._names)  # genuinely chunked

    results = idx.search("query", limit=10)
    names = [r["name"] for r in results]
    assert len(names) == len(set(names)), "max-pool must dedupe chunks to skills"


def test_v1_cache_rejected_and_rebuilt(tmp_path, monkeypatch):
    """A pre-chunking (schema-v1) cache on disk must be ignored, not loaded
    with a mismatched row layout."""
    import search_index as si

    monkeypatch.setattr(si, "HAS_VECTORS", True)
    idx = _make_index(tmp_path)
    idx._model = _FakeModel()  # avoid loading a real model during build()
    idx.build()
    data_dir = tmp_path / "data"

    # Write a v1-style cache: names = flat skill list, key has no schema.
    np.save(str(data_dir / "skill_embeddings.npy"), np.zeros((3, 8), dtype=np.float32))
    (data_dir / "skill_embed_names.json").write_text(json.dumps(idx._names))
    (data_dir / "skill_embed_mtime.json").write_text(
        json.dumps({"hash": _get_registry_hash(data_dir)})
    )

    model = _FakeModel()
    idx._model = model
    corpus = [f"{n}: t" for n in idx._names for _ in range(2)]
    keys = [(n, f"body:{j}") for n in idx._names for j in range(2)]
    result = idx._build_or_load_embeddings(corpus, keys)
    assert result is not None
    assert model.calls == 1, "v1 cache must be rejected, forcing a rebuild"
    # New cache carries the v2 schema marker.
    meta = json.loads((data_dir / "skill_embed_mtime.json").read_text())
    assert meta["schema"] == _EMBED_CACHE_SCHEMA


# ---------------------------------------------------------------------------
# Synthetic query indexing (PR3)
# ---------------------------------------------------------------------------

from search_index import _load_synthetic_queries  # noqa: E402


def _write_synthetic(data_dir, mapping):
    """mapping: {skill: [index_queries]} → synthetic_queries.json on disk."""
    payload = {
        "version": 1,
        "generated_with": "test",
        "skills": {
            name: {"content_hash": "x", "index_queries": qs, "eval_queries": ["held"]}
            for name, qs in mapping.items()
        },
    }
    (data_dir / "synthetic_queries.json").write_text(json.dumps(payload))


def test_load_synthetic_queries_index_only(tmp_path):
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    _write_synthetic(data_dir, {"alpha-skill": ["how do I alpha", "alpha please"]})
    loaded = _load_synthetic_queries(data_dir)
    assert loaded == {"alpha-skill": ["how do I alpha", "alpha please"]}


def test_load_synthetic_queries_missing_file(tmp_path):
    (tmp_path / "data").mkdir()
    assert _load_synthetic_queries(tmp_path / "data") == {}


def test_synthetic_queries_added_as_chunks(tmp_path, monkeypatch):
    import search_index as si
    monkeypatch.setattr(si, "HAS_VECTORS", True)

    idx = _make_index(tmp_path)
    _write_synthetic(tmp_path / "data", {"beta-skill": ["tell me about beta", "beta help"]})
    idx._model = _FakeModel()
    idx.build()

    # beta-skill now has q:0 and q:1 chunks in addition to desc + body.
    beta_idx = idx._names.index("beta-skill")
    beta_kinds = [
        # reconstruct kinds by re-extracting isn't exposed; assert via counts:
        i for i, s in enumerate(idx._chunk_skill_idx) if s == beta_idx
    ]
    # alpha (no synthetic) vs beta (2 synthetic) — beta must have >= 2 more
    # chunks than its synthetic-free description+body baseline. Simplest check:
    # beta has more chunks than alpha (which has none).
    alpha_idx = idx._names.index("alpha-skill")
    alpha_chunks = sum(1 for s in idx._chunk_skill_idx if s == alpha_idx)
    assert len(beta_kinds) >= alpha_chunks + 2


def test_synthetic_queries_in_bm25_doc(tmp_path):
    """A distinctive synthetic-query term should make the skill findable via
    BM25 even if that term isn't in the description or body."""
    idx = _make_index(tmp_path)
    if idx._bm25 is None:
        pytest.skip("rank-bm25 not installed")
    _write_synthetic(tmp_path / "data", {"gamma-skill": ["xyzzy plugh frobnicate"]})
    idx.build()
    idx._embeddings = None  # isolate BM25

    results = idx.search("frobnicate")
    assert any(r["name"] == "gamma-skill" for r in results)


def test_synthetic_file_invalidates_cache_hash(tmp_path):
    """Regenerating synthetic queries must change the embedding cache key."""
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    (data_dir / "registry.json").write_text('{"skills": {}}')
    h_before = _get_registry_hash(data_dir)
    _write_synthetic(data_dir, {"alpha-skill": ["new query"]})
    h_after = _get_registry_hash(data_dir)
    assert h_before != h_after and h_before and h_after
