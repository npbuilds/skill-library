"""Regression tests for HybridSearchIndex internals."""

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


def test_full_floor_when_bm25_present(tmp_path):
    """With BM25 available, the original 0.02 floor applies even when only
    one signal matched — single-signal long-tail noise stays filtered so
    gap detection keeps firing on out-of-scope queries."""
    idx = _make_index(tmp_path)
    idx.build()
    idx._embeddings = None
    if idx._bm25 is None:
        pytest.skip("rank-bm25 not installed")

    # BM25 matches alpha (query term in body); graph ranks beta/gamma from
    # alpha seed. No skill appears in both lists, so every fused score is
    # single-list: rank-1 = 0.0164 < 0.02 — all filtered under the 2-signal floor.
    results = idx.search("alpha", recent_skills=["alpha-skill"])
    for r in results:
        assert r["rrf_score"] >= _MIN_RRF_SCORE


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
    results = [None, None]

    def run(idx, slot):
        results[slot] = idx._build_or_load_embeddings(corpus)

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
    assert idx._build_or_load_embeddings(["x"]) is None

    # Lock must be reacquirable: a healthy rebuild succeeds afterwards.
    idx2 = _make_index(tmp_path)
    idx2.build()
    idx2._model = _FakeModel()
    corpus = [f"{n}: text" for n in idx2._names]
    assert idx2._build_or_load_embeddings(corpus) is not None
