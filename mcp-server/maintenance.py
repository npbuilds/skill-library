"""
Maintenance HTTP router (Layer 2, slice 1).

Exposes scheduled-maintenance endpoints alongside the MCP server:
  GET  /health                -> liveness check
  POST /maint/recalibrate     -> run recalibrate_scores.py; open bot PR if drift

Only mounted when REMOTE_MODE is true. Intended to be triggered by
Cloud Scheduler with OIDC-authenticated POSTs.

Write-back pattern: maintenance jobs NEVER touch main directly. They
clone the repo, run a script, commit to a maintenance/* branch, push,
and open a PR. CI + (eventually) auto-merge.yml handle the landing.

Conservative autonomy (v1 default): PRs open with label `maint:green`
and wait for manual merge. Auto-merge workflow comes in a later slice.
"""

import logging
import os
import shutil
import subprocess
import tempfile
from datetime import datetime, timezone
from pathlib import Path

try:
    import httpx
except ImportError:  # pragma: no cover - surfaced at deploy time if missing
    httpx = None

from starlette.requests import Request
from starlette.responses import JSONResponse

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Config (all overridable via env; defaults are safe)
# ---------------------------------------------------------------------------

GITHUB_REPO = os.environ.get("GITHUB_BOT_REPO", "npbuilds/skill-library")
BASE_BRANCH = os.environ.get("GITHUB_BASE_BRANCH", "main")
BOT_PAT_ENV = "GITHUB_BOT_PAT"
BOT_EMAIL = os.environ.get("BOT_EMAIL", "skill-library-bot@users.noreply.github.com")
BOT_NAME = os.environ.get("BOT_NAME", "skill-library-bot")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _run(cmd, cwd=None, capture=False, redact=None):
    """Run a subprocess. Raises CalledProcessError on non-zero exit.

    `redact`, if provided, is a string replaced with <REDACTED> in any
    error message we surface (to avoid leaking the bot PAT).
    """
    try:
        return subprocess.run(
            cmd,
            cwd=cwd,
            check=True,
            capture_output=capture,
            text=capture,
        )
    except subprocess.CalledProcessError as e:
        cmd_str = " ".join(str(x) for x in e.cmd) if isinstance(e.cmd, (list, tuple)) else str(e.cmd)
        if redact and redact in cmd_str:
            cmd_str = cmd_str.replace(redact, "<REDACTED>")
        stderr = (e.stderr or "") if capture else ""
        if redact and redact in stderr:
            stderr = stderr.replace(redact, "<REDACTED>")
        logger.error("subprocess failed: %s\nstderr: %s", cmd_str, stderr)
        # Re-raise with sanitized message in args[0]
        raise subprocess.CalledProcessError(
            e.returncode, cmd_str, output=(e.output if capture else None), stderr=stderr
        ) from None


def _pat() -> str | None:
    return os.environ.get(BOT_PAT_ENV) or None


def _ts() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H-%M-%SZ")


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

async def _recalibrate(request: Request) -> JSONResponse:
    """Run recalibrate_scores.py in a fresh clone. If scores drift,
    commit to a maintenance branch, push, and open a labeled PR."""

    if httpx is None:
        return JSONResponse(
            {"error": "httpx not installed in this container"}, status_code=503
        )
    pat = _pat()
    if not pat:
        return JSONResponse(
            {"error": f"{BOT_PAT_ENV} not set — maintenance bot disabled"},
            status_code=503,
        )

    ts = _ts()
    branch = f"maintenance/recalibrate-{ts}"
    clone_url = f"https://x-access-token:{pat}@github.com/{GITHUB_REPO}.git"

    tmpdir = tempfile.mkdtemp(prefix="maint-recal-")
    try:
        # 1. Clone (shallow)
        _run(
            ["git", "clone", "--depth", "1", "--branch", BASE_BRANCH, clone_url, tmpdir],
            redact=pat,
        )

        # 2. Bot identity
        _run(["git", "config", "user.email", BOT_EMAIL], cwd=tmpdir)
        _run(["git", "config", "user.name", BOT_NAME], cwd=tmpdir)

        # 3. New branch
        _run(["git", "checkout", "-b", branch], cwd=tmpdir)

        # 4. Run the recalibrate script
        result = _run(
            ["python3", "scripts/recalibrate_scores.py"],
            cwd=tmpdir,
            capture=True,
        )
        stdout = (result.stdout or "").strip()

        # 5. No drift? return cleanly without a PR
        diff_check = subprocess.run(
            ["git", "diff", "--quiet", "--", "data/registry.json"],
            cwd=tmpdir,
        )
        if diff_check.returncode == 0:
            logger.info("recalibrate: no drift, skipping PR")
            return JSONResponse(
                {
                    "status": "no_changes",
                    "message": "Scores already in sync.",
                    "recalibrate_stdout": stdout,
                }
            )

        # 6. Commit + push
        commit_msg = (
            f"chore(maint): recalibrate scores {ts}\n\n"
            f"Automated recalibration via /maint/recalibrate.\n\n"
            f"{stdout}"
        )
        _run(["git", "add", "data/registry.json"], cwd=tmpdir)
        _run(["git", "commit", "-m", commit_msg], cwd=tmpdir)
        _run(["git", "push", "origin", branch], cwd=tmpdir, redact=pat)

        # 7. Open PR + label via GitHub API
        headers = {
            "Authorization": f"token {pat}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        }
        pr_body = (
            "Automated score recalibration.\n\n"
            "```\n"
            f"{stdout}\n"
            "```\n\n"
            "**Tier**: `maint:green` (mechanical, deterministic). "
            "Safe to auto-merge once CI passes.\n\n"
            "_Opened by `skill-library-bot` via `/maint/recalibrate`._"
        )

        async with httpx.AsyncClient(timeout=30.0) as client:
            pr_resp = await client.post(
                f"https://api.github.com/repos/{GITHUB_REPO}/pulls",
                headers=headers,
                json={
                    "title": f"chore(maint): recalibrate scores {ts}",
                    "body": pr_body,
                    "head": branch,
                    "base": BASE_BRANCH,
                },
            )
            pr_resp.raise_for_status()
            pr = pr_resp.json()

            label_resp = await client.post(
                f"https://api.github.com/repos/{GITHUB_REPO}/issues/{pr['number']}/labels",
                headers=headers,
                json={"labels": ["maint:green"]},
            )
            # Label failure shouldn't fail the job; log and move on
            if label_resp.status_code >= 400:
                logger.warning(
                    "failed to add label maint:green to PR #%s: %s",
                    pr["number"], label_resp.text,
                )

        return JSONResponse(
            {
                "status": "pr_opened",
                "pr_number": pr["number"],
                "pr_url": pr["html_url"],
                "branch": branch,
            }
        )

    except subprocess.CalledProcessError as e:
        return JSONResponse(
            {
                "error": "subprocess_failed",
                "cmd": e.cmd,
                "returncode": e.returncode,
                "stderr": (e.stderr or "").strip() if isinstance(e.stderr, str) else None,
            },
            status_code=500,
        )
    except httpx.HTTPStatusError as e:  # pragma: no cover - GitHub API error
        return JSONResponse(
            {"error": "github_api", "status": e.response.status_code, "body": e.response.text},
            status_code=502,
        )
    except Exception as e:  # pragma: no cover - unexpected
        logger.exception("unexpected error in /maint/recalibrate")
        return JSONResponse(
            {"error": "unexpected", "message": str(e)}, status_code=500
        )
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)


async def _health(_request: Request) -> JSONResponse:
    """Liveness probe. Not a deep health check — just confirms the
    container is up and the maintenance router is mounted.

    Layer 2 full-scope /status endpoint will be richer (last-runs,
    budget, open_failures) — this is a stepping stone."""
    return JSONResponse(
        {
            "status": "ok",
            "service": "skill-library-mcp",
            "maintenance_router": "mounted",
            "bot_pat_configured": bool(_pat()),
        }
    )


# ---------------------------------------------------------------------------
# Registration
# ---------------------------------------------------------------------------

def register(mcp) -> None:
    """Attach maintenance HTTP routes to the FastMCP instance.

    Uses FastMCP's `@custom_route` decorator to add routes to the
    Starlette app that serves the MCP protocol, so both live on one
    port in one container.
    """
    mcp.custom_route("/health", methods=["GET"])(_health)
    mcp.custom_route("/maint/recalibrate", methods=["POST"])(_recalibrate)
    logger.info("maintenance router mounted: /health, /maint/recalibrate")
