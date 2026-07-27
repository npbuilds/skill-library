"""Deterministic tests for the regime and sentiment classifiers."""

from processors.regime import classify_regime
from processors.sentiment_score import compute_sentiment_score


def test_regime_reports_insufficient_data():
    result = classify_regime({}, {})
    assert result["quadrant"] == "insufficient_data"
    assert result["confidence"] == 0


def test_regime_classifies_reflation_from_positive_axes():
    macro = {
        "indicators": {
            "UNRATE": {"change": -0.2, "value": 3.8},
            "USSLIND": {"change": 0.3},
            "PCEPILFE": {"yoy_change": 3.5},
            "CPIAUCSL": {"yoy_change": 3.2},
            "T5YIE": {"value": 2.7},
        }
    }
    result = classify_regime(macro, {"spread_10y2y": 0.7})
    assert result["quadrant"] == "reflation"
    assert result["growth_score"] > 0
    assert result["inflation_score"] > 0
    assert 0 < result["confidence"] <= 1


def test_sentiment_defaults_to_neutral_without_components():
    result = compute_sentiment_score({}, {})
    assert result["score"] == 50
    assert result["label"] == "cautious"
    assert result["component_count"] == 0


def test_sentiment_renormalizes_available_components():
    result = compute_sentiment_score(
        {
            "fear_greed": {"score": 80},
            "vix": {"spot": 10},
        },
        {},
    )
    expected = round((80 * 0.30 + 100 * 0.25) / 0.55, 1)
    assert result["score"] == expected
    assert result["component_count"] == 2


def test_sentiment_components_are_clamped():
    result = compute_sentiment_score(
        {"vix": {"spot": 100, "term_structure": "backwardation", "term_spread": -20}},
        {"breadth_divergence": 100, "indices": {"S&P 500": {"ytd_pct": 100}}},
    )
    normalized = [item["normalized"] for item in result["components"].values()]
    assert all(0 <= value <= 100 for value in normalized)
