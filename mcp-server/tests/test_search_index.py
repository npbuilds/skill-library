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
