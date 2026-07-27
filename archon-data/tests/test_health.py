"""Tests for data-source metadata and composite health scoring."""

from processors.health import collect_health, wrap_with_meta


def test_wrap_with_meta_preserves_dict_payload():
    result = wrap_with_meta(
        {"value": 3},
        "FRED",
        status="degraded",
        degraded_reason="cached",
        cache_age_seconds=90,
    )
    assert result["value"] == 3
    assert result["_meta"]["source"] == "FRED"
    assert result["_meta"]["status"] == "degraded"
    assert result["_meta"]["degraded_reason"] == "cached"


def test_wrap_with_meta_boxes_list_payload():
    result = wrap_with_meta([1, 2], "list-source")
    assert result["data"] == [1, 2]
    assert result["_meta"]["status"] == "ok"


def test_collect_health_scores_status_and_staleness():
    results = {
        "fresh": wrap_with_meta({}, "fresh", cache_age_seconds=0),
        "stale": wrap_with_meta({}, "stale", cache_age_seconds=90_000),
        "very_stale": wrap_with_meta({}, "very-stale", cache_age_seconds=180_000),
        "degraded": wrap_with_meta({}, "degraded", status="degraded"),
        "failed": wrap_with_meta({}, "failed", status="failed"),
    }
    health = collect_health(results)
    assert health["source_count"] == 5
    assert health["sources"]["fresh"]["score"] == 100
    assert health["sources"]["stale"]["score"] == 80
    assert health["sources"]["very_stale"]["score"] == 60
    assert health["sources"]["degraded"]["score"] == 50
    assert health["sources"]["failed"]["score"] == 0
    assert health["composite_score"] == 58


def test_collect_health_marks_uninstrumented_result_unknown():
    health = collect_health({"legacy": {"value": 1}})
    assert health["sources"]["legacy"] == {"status": "unknown", "age": "?"}
    assert health["source_count"] == 0
    assert health["composite_score"] == 0
    assert "legacy: ?" in health["status_line"]


def test_age_boundaries_are_visible_in_status_line():
    results = {
        "live": wrap_with_meta({}, "live", cache_age_seconds=59),
        "minutes": wrap_with_meta({}, "minutes", cache_age_seconds=120),
        "hours": wrap_with_meta({}, "hours", cache_age_seconds=7_200),
        "days": wrap_with_meta({}, "days", cache_age_seconds=172_800),
    }
    line = collect_health(results)["status_line"]
    assert "live: OK (live)" in line
    assert "minutes: OK (2m)" in line
    assert "hours: OK (2h)" in line
    assert "days: OK (2d)" in line
