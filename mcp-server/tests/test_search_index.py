"""Regression tests for HybridSearchIndex internals."""

import pytest

np = pytest.importorskip("numpy")

from search_index import _atomic_write_npy  # noqa: E402


def test_atomic_write_npy_round_trip(tmp_path):
    """np.save auto-appends '.npy'; ensure the atomic helper doesn't leave
    an empty stub at the target path while the real array lands at a sibling."""
    target = tmp_path / "embeddings.npy"
    arr = np.arange(12, dtype=np.float32).reshape(3, 4)

    _atomic_write_npy(target, arr)

    assert target.stat().st_size > 0, f"target wrote 0 bytes; orphans: {list(tmp_path.iterdir())}"
    assert np.array_equal(np.load(target), arr)
    assert list(tmp_path.iterdir()) == [target], "stray tempfile left behind"
