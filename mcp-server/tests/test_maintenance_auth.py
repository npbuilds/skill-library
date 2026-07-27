"""Tests for the maintenance-router caller-side token check.

The /maint/* endpoints sit on a publicly-invokable Cloud Run service, so a
shared secret in the X-Maint-Token header is the only barrier between an
anonymous caller and the server's GitHub bot PAT. These tests pin the three
behaviors that matter: token missing, token wrong, token correct.
"""

import asyncio
from unittest.mock import MagicMock

from starlette.responses import JSONResponse

from maintenance import (
    MAINT_TOKEN_ENV,
    MAINT_TOKEN_HEADER,
    _check_maint_token,
    _health,
)


def _request_with_header(value: str | None) -> MagicMock:
    req = MagicMock()
    req.headers.get.side_effect = lambda key, default="": (
        value if value is not None and key == MAINT_TOKEN_HEADER else default
    )
    return req


def test_no_server_token_configured_returns_503(monkeypatch):
    """Fail closed: if the server has no token in env, refuse all callers."""
    monkeypatch.delenv(MAINT_TOKEN_ENV, raising=False)
    resp = _check_maint_token(_request_with_header("any-value"))
    assert isinstance(resp, JSONResponse) and resp.status_code == 503


def test_missing_header_returns_401(monkeypatch):
    monkeypatch.setenv(MAINT_TOKEN_ENV, "secret123")
    resp = _check_maint_token(_request_with_header(None))
    assert isinstance(resp, JSONResponse) and resp.status_code == 401


def test_wrong_header_returns_401(monkeypatch):
    monkeypatch.setenv(MAINT_TOKEN_ENV, "secret123")
    resp = _check_maint_token(_request_with_header("wrong"))
    assert isinstance(resp, JSONResponse) and resp.status_code == 401


def test_correct_header_passes(monkeypatch):
    monkeypatch.setenv(MAINT_TOKEN_ENV, "secret123")
    assert _check_maint_token(_request_with_header("secret123")) is None


def test_public_health_supports_observatory_cors(monkeypatch):
    monkeypatch.setenv("GITHUB_BOT_PAT", "configured")
    resp = asyncio.run(_health(MagicMock()))
    assert resp.status_code == 200
    assert resp.headers["access-control-allow-origin"] == "*"
    assert resp.headers["cache-control"] == "no-store"
