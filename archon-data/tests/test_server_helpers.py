"""Failure-isolation and deadline tests for Archon collection helpers."""

import threading
import time

import server


def test_safe_collect_wraps_success():
    result = server._safe_collect("market", "source-a", lambda: {"value": 7})
    assert result["value"] == 7
    assert result["_meta"]["source"] == "source-a"
    assert result["_meta"]["status"] == "ok"


def test_safe_collect_degrades_explicit_error_payload():
    result = server._safe_collect(
        "market", "source-a", lambda: {"error": "upstream unavailable"}
    )
    assert result["_meta"]["status"] == "degraded"
    assert result["_meta"]["degraded_reason"] == "upstream unavailable"


def test_safe_collect_isolates_exception():
    def fail():
        raise RuntimeError("collector exploded")

    result = server._safe_collect("market", "source-a", fail)
    assert result["error"] == "collector exploded"
    assert result["_meta"]["status"] == "failed"


def test_parallel_collect_isolates_success_failure_and_deadline():
    release_slow_collector = threading.Event()

    def fail():
        raise ValueError("bad source")

    def slow():
        release_slow_collector.wait(timeout=1)
        return {"late": True}

    started = time.monotonic()
    results = server._parallel_collect(
        [
            ("ok", "fast", lambda: {"value": 1}),
            ("failed", "broken", fail),
            ("late", "slow", slow),
        ],
        deadline_seconds=0.01,
    )
    elapsed = time.monotonic() - started
    release_slow_collector.set()

    assert elapsed < 0.5
    assert results["ok"]["_meta"]["status"] == "ok"
    assert results["failed"]["_meta"]["status"] == "failed"
    assert results["late"]["_meta"]["status"] == "failed"
    assert "deadline" in results["late"]["error"]


def test_parallel_collect_empty_spec_is_safe():
    assert server._parallel_collect([]) == {}
