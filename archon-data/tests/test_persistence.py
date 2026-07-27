"""Snapshot I/O and decision-relevant delta regression tests."""

import json
import math
from datetime import date

from processors import persistence


def test_snapshot_round_trip_is_nan_safe(tmp_path, monkeypatch):
    monkeypatch.setattr(persistence, "SNAPSHOT_DIR", tmp_path)
    path = persistence.save_daily_snapshot(
        {"value": math.nan, "as_of": date(2026, 7, 27)},
        for_date="2026-07-27",
    )
    raw = json.loads(tmp_path.joinpath("2026-07-27.json").read_text())
    assert path == str(tmp_path / "2026-07-27.json")
    assert raw["data"]["value"] is None
    assert raw["data"]["as_of"] == "2026-07-27"
    assert persistence.load_snapshot("2026-07-27") == raw


def test_same_day_save_overwrites_with_latest_data(tmp_path, monkeypatch):
    monkeypatch.setattr(persistence, "SNAPSHOT_DIR", tmp_path)
    persistence.save_daily_snapshot({"value": 1}, for_date="2026-07-27")
    persistence.save_daily_snapshot({"value": 2}, for_date="2026-07-27")
    assert persistence.load_snapshot("2026-07-27")["data"]["value"] == 2
    assert len(list(tmp_path.glob("*.json"))) == 1


def test_prior_snapshot_selects_latest_earlier_date(tmp_path, monkeypatch):
    monkeypatch.setattr(persistence, "SNAPSHOT_DIR", tmp_path)
    for day in ("2026-07-20", "2026-07-25", "2026-07-27"):
        persistence.save_daily_snapshot({"day": day}, for_date=day)
    prior = persistence.get_prior_snapshot("2026-07-27")
    assert prior["_snapshot_date"] == "2026-07-25"
    assert persistence.get_prior_snapshot("2026-07-20") is None


def test_list_snapshots_is_sorted_and_sized(tmp_path, monkeypatch):
    monkeypatch.setattr(persistence, "SNAPSHOT_DIR", tmp_path)
    persistence.save_daily_snapshot({"value": 2}, for_date="2026-07-02")
    persistence.save_daily_snapshot({"value": 1}, for_date="2026-07-01")
    snapshots = persistence.list_snapshots()
    assert [item["date"] for item in snapshots] == ["2026-07-01", "2026-07-02"]
    assert all(item["size_kb"] > 0 for item in snapshots)


def test_compute_delta_detects_regime_threshold_and_market_move():
    prior = {
        "_snapshot_date": "2026-07-26",
        "data": {
            "market": {"indices": {"S&P 500": {"price": 100}}},
            "sentiment": {
                "raw": {"vix": {"spot": 19, "regime": "normal"}},
                "composite": {"score": 40, "label": "cautious"},
            },
            "regime": {"quadrant": "goldilocks"},
        },
    }
    current = {
        "data": {
            "market": {"indices": {"S&P 500": {"price": 101}}},
            "sentiment": {
                "raw": {"vix": {"spot": 31, "regime": "panic"}},
                "composite": {"score": 20, "label": "extreme_fear"},
            },
            "regime": {"quadrant": "stagflation"},
        }
    }
    delta = persistence.compute_delta(current, prior)
    assert delta["prior_date"] == "2026-07-26"
    assert any(change["type"] == "macro_regime" for change in delta["regime_changes"])
    assert any(
        crossing["metric"] == "VIX" and crossing["threshold"] == 20
        for crossing in delta["threshold_crossings"]
    )
    assert any(move["asset"] == "S&P 500" for move in delta["market_moves"])
    assert delta["summary_bullets"]
