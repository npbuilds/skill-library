"""CLI regressions for privacy-safe telemetry displays."""

import json

from click.testing import CliRunner

import cli


def test_gaps_command_labels_redacted_remote_events(tmp_path, monkeypatch):
    gap_log = tmp_path / "gaps.jsonl"
    gap_log.write_text(
        json.dumps(
            {
                "type": "search",
                "query_redacted": True,
                "result_count": 0,
                "timestamp": "2026-07-19T12:00:00Z",
            }
        )
        + "\n"
    )
    monkeypatch.setattr(cli, "GAPS_LOG", gap_log)

    result = CliRunner().invoke(cli.gaps)

    assert result.exit_code == 0
    assert "1 redacted events" in result.output
    assert "[redacted remote queries]" in result.output
    assert '"?"' not in result.output
