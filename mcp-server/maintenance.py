"""
Maintenance HTTP router (Layer 2).

Exposes scheduled-maintenance endpoints alongside the MCP server:
  GET  /health                -> liveness check
  POST /maint/recalibrate     -> run recalibrate_scores.py; open bot PR if drift
  POST /maint/validate        -> spot-check skill structure; return report (no PR)
  POST /maint/snapshot        -> run snapshot_evolution.py; open bot PR
  POST /maint/sentinel        -> run health-report.py; open bot PR with report

Only mounted when REMOTE_MODE is true. Intended to be triggered by
Cloud Scheduler with OIDC-authenticated POSTs.

Write-back pattern: maintenance jobs NEVER touch main directly. They
clone the repo, run a script, commit to a maintenance/* branch, push,
and open a PR. CI + (eventually) auto-merge.yml handle the landing.

Conservative autonomy (v1 default): PRs open with label `maint:green`
and wait for manual merge. Auto-merge workflow comes in a later slice.
"""

import json
import logging
import os
import random
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

from notifier import get_notifier

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Config (all overridable via env; defaults are safe)
# ---------------------------------------------------------------------------

GITHUB_REPO = os.environ.get("GITHUB_BOT_REPO", "npbuilds/skill-library")
VAULT_REPO = os.environ.get("GITHUB_VAULT_REPO", "npbuilds/skill-library-vault")
BASE_BRANCH = os.environ.get("GITHUB_BASE_BRANCH", "main")
BOT_PAT_ENV = "GITHUB_BOT_PAT"
BOT_EMAIL = os.environ.get("BOT_EMAIL", "skill-library-bot@users.noreply.github.com")
BOT_NAME = os.environ.get("BOT_NAME", "skill-library-bot")
KB_REFRESH_LIMIT = int(os.environ.get("KB_REFRESH_LIMIT", "5"))


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _run(cmd, cwd=None, capture=False, redact=None, env=None):
    """Run a subprocess. Raises CalledProcessError on non-zero exit.

    `redact`, if provided, is a string replaced with <REDACTED> in any
    error message we surface (to avoid leaking the bot PAT).
    `env`, if provided, replaces the subprocess environment.
    """
    try:
        return subprocess.run(
            cmd,
            cwd=cwd,
            check=True,
            capture_output=capture,
            text=capture,
            env=env,
        )
    except subprocess.CalledProcessError as e:
        cmd_str = " ".join(str(x) for x in e.cmd) if isinstance(e.cmd, (list, tuple)) else str(e.cmd)
        if redact and redact in cmd_str:
            cmd_str = cmd_str.replace(redact, "<REDACTED>")
        stderr = (e.stderr or "") if capture else ""
        if redact and redact in stderr:
            stderr = stderr.replace(redact, "<REDACTED>")
        logger.error("subprocess failed: %s\nstderr: %s", cmd_str, stderr)
        raise subprocess.CalledProcessError(
            e.returncode, cmd_str, output=(e.output if capture else None), stderr=stderr
        ) from None


def _pat() -> str | None:
    return os.environ.get(BOT_PAT_ENV) or None


def _ts() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H-%M-%SZ")


def _require_pat() -> str | JSONResponse:
    """Return the PAT string or a 503 JSONResponse if unavailable."""
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
    return pat


def _subprocess_error(e: subprocess.CalledProcessError) -> JSONResponse:
    return JSONResponse(
        {
            "error": "subprocess_failed",
            "cmd": e.cmd,
            "returncode": e.returncode,
            "stderr": (e.stderr or "").strip() if isinstance(e.stderr, str) else None,
        },
        status_code=500,
    )


def _github_api_error(e) -> JSONResponse:
    return JSONResponse(
        {"error": "github_api", "status": e.response.status_code, "body": e.response.text},
        status_code=502,
    )


# ---------------------------------------------------------------------------
# _BotPR — shared lifecycle for clone → branch → mutate → PR endpoints
# ---------------------------------------------------------------------------

class _BotPR:
    """Manages the clone → branch → run → commit → push → PR lifecycle.

    Usage:
        bot = _BotPR(pat, "recalibrate")
        try:
            bot.clone()
            _run(["python3", "scripts/my-script.py"], cwd=bot.tmpdir, capture=True)
            if not bot.has_changes():
                return JSONResponse({"status": "no_changes"})
            pr = await bot.open_pr(title=..., body=..., labels=["maint:green"])
            return JSONResponse({"status": "pr_opened", **pr})
        finally:
            bot.cleanup()
    """

    def __init__(self, pat: str, job_name: str):
        self.pat = pat
        self.job_name = job_name
        self.ts = _ts()
        self.branch = f"maintenance/{job_name}-{self.ts}"
        self._clone_url = f"https://x-access-token:{pat}@github.com/{GITHUB_REPO}.git"
        self.tmpdir = tempfile.mkdtemp(prefix=f"maint-{job_name}-")

    def clone(self) -> None:
        """Shallow clone, configure bot identity, create branch."""
        _run(
            ["git", "clone", "--depth", "1", "--branch", BASE_BRANCH,
             self._clone_url, self.tmpdir],
            capture=True,
            redact=self.pat,
        )
        _run(["git", "config", "user.email", BOT_EMAIL], cwd=self.tmpdir)
        _run(["git", "config", "user.name", BOT_NAME], cwd=self.tmpdir)
        _run(["git", "checkout", "-b", self.branch], cwd=self.tmpdir)

    def has_changes(self) -> bool:
        """Stage all changes and return True if anything is staged."""
        _run(["git", "add", "-A"], cwd=self.tmpdir)
        diff = subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=self.tmpdir)
        return diff.returncode != 0

    async def open_pr(self, title: str, body: str, labels: list[str] | None = None) -> dict:
        """Commit staged changes, push, open PR, add labels.

        Returns: {"pr_number": int, "pr_url": str, "branch": str}
        """
        _run(["git", "commit", "-m", title], cwd=self.tmpdir)
        _run(
            ["git", "push", "origin", self.branch],
            cwd=self.tmpdir,
            capture=True,
            redact=self.pat,
        )

        headers = {
            "Authorization": f"token {self.pat}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        }
        async with httpx.AsyncClient(timeout=30.0) as client:
            pr_resp = await client.post(
                f"https://api.github.com/repos/{GITHUB_REPO}/pulls",
                headers=headers,
                json={
                    "title": title,
                    "body": body,
                    "head": self.branch,
                    "base": BASE_BRANCH,
                },
            )
            pr_resp.raise_for_status()
            pr = pr_resp.json()

            if labels:
                label_resp = await client.post(
                    f"https://api.github.com/repos/{GITHUB_REPO}/issues/{pr['number']}/labels",
                    headers=headers,
                    json={"labels": labels},
                )
                if label_resp.status_code >= 400:
                    logger.warning(
                        "failed to label PR #%s: %s", pr["number"], label_resp.text
                    )

        return {"pr_number": pr["number"], "pr_url": pr["html_url"], "branch": self.branch}

    def cleanup(self) -> None:
        shutil.rmtree(self.tmpdir, ignore_errors=True)


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

async def _health(_request: Request) -> JSONResponse:
    """Liveness probe. Confirms the container is up and the maintenance
    router is mounted."""
    return JSONResponse(
        {
            "status": "ok",
            "service": "skill-library-mcp",
            "maintenance_router": "mounted",
            "bot_pat_configured": bool(_pat()),
        }
    )


async def _recalibrate(request: Request) -> JSONResponse:
    """Run recalibrate_scores.py in a fresh clone. If scores drift,
    commit to a maintenance branch, push, and open a labeled PR."""
    pat = _require_pat()
    if isinstance(pat, JSONResponse):
        return pat

    notify = get_notifier()
    bot = _BotPR(pat, "recalibrate")
    try:
        bot.clone()
        result = _run(
            ["python3", "scripts/recalibrate_scores.py"],
            cwd=bot.tmpdir, capture=True,
        )
        stdout = (result.stdout or "").strip()

        if not bot.has_changes():
            notify.p2_log("recalibrate", {"status": "no_changes"})
            return JSONResponse({
                "status": "no_changes",
                "message": "Scores already in sync.",
                "recalibrate_stdout": stdout,
            })

        pr = await bot.open_pr(
            title=f"chore(maint): recalibrate scores {bot.ts}",
            body=(
                "Automated score recalibration.\n\n"
                f"```\n{stdout}\n```\n\n"
                "**Tier**: `maint:green` (mechanical, deterministic). "
                "Safe to auto-merge once CI passes.\n\n"
                "_Opened by `skill-library-bot` via `/maint/recalibrate`._"
            ),
            labels=["maint:green"],
        )
        notify.p2_log("recalibrate", {"status": "pr_opened", **pr})
        return JSONResponse({"status": "pr_opened", **pr})

    except subprocess.CalledProcessError as e:
        await notify.p1("recalibrate", e)
        return _subprocess_error(e)
    except httpx.HTTPStatusError as e:
        await notify.p1("recalibrate", e)
        return _github_api_error(e)
    except Exception as e:
        await notify.p0(f"Unexpected failure in recalibrate: {e}", {"job": "recalibrate"})
        return JSONResponse({"error": "unexpected", "message": str(e)}, status_code=500)
    finally:
        bot.cleanup()


async def _validate(request: Request) -> JSONResponse:
    """Spot-check 10 random skills with validate-structure.sh.
    Returns a JSON report. Does NOT open a PR (observation only)."""
    pat = _require_pat()
    if isinstance(pat, JSONResponse):
        return pat

    notify = get_notifier()
    bot = _BotPR(pat, "validate")
    try:
        bot.clone()

        reg = json.loads(Path(bot.tmpdir, "data/registry.json").read_text())
        skills = [
            (n, e) for n, e in reg.get("skills", {}).items()
            if e.get("status") != "deprecated" and e.get("location")
        ]
        sample = random.sample(skills, min(10, len(skills)))

        results = []
        for name, entry in sample:
            skill_dir = str(Path(bot.tmpdir) / Path(entry["location"]).parent)
            try:
                r = _run(
                    ["bash", "scripts/validate-structure.sh", skill_dir],
                    cwd=bot.tmpdir, capture=True,
                )
                data = json.loads(r.stdout)
                results.append({"skill": name, **data})
            except subprocess.CalledProcessError:
                results.append({"skill": name, "valid": False, "error": "validation script failed"})
            except json.JSONDecodeError:
                results.append({"skill": name, "valid": False, "error": "non-JSON output"})

        critical = [r for r in results if not r.get("valid", True)]
        status = "issues_found" if critical else "ok"
        notify.p2_log("validate", {"status": status, "checked": len(results), "critical_count": len(critical)})
        return JSONResponse({
            "status": status,
            "checked": len(results),
            "critical_count": len(critical),
            "results": results,
        })

    except subprocess.CalledProcessError as e:
        await notify.p1("validate", e)
        return _subprocess_error(e)
    except Exception as e:
        await notify.p0(f"Unexpected failure in validate: {e}", {"job": "validate"})
        return JSONResponse({"error": "unexpected", "message": str(e)}, status_code=500)
    finally:
        bot.cleanup()


async def _snapshot(request: Request) -> JSONResponse:
    """Run snapshot_evolution.py to append time-series data.
    Opens a maint:green PR if new entries were appended."""
    pat = _require_pat()
    if isinstance(pat, JSONResponse):
        return pat

    notify = get_notifier()
    bot = _BotPR(pat, "snapshot")
    try:
        bot.clone()
        result = _run(
            ["python3", "scripts/snapshot_evolution.py", "--event=scheduled"],
            cwd=bot.tmpdir, capture=True,
        )
        stdout = (result.stdout or "").strip()

        if not bot.has_changes():
            notify.p2_log("snapshot", {"status": "no_changes"})
            return JSONResponse({"status": "no_changes", "stdout": stdout})

        pr = await bot.open_pr(
            title=f"chore(maint): evolution snapshot {bot.ts}",
            body=(
                "Scheduled evolution snapshot.\n\n"
                f"```\n{stdout}\n```\n\n"
                "**Tier**: `maint:green` (append-only time-series data).\n\n"
                "_Opened by `skill-library-bot` via `/maint/snapshot`._"
            ),
            labels=["maint:green"],
        )
        notify.p2_log("snapshot", {"status": "pr_opened", **pr})
        return JSONResponse({"status": "pr_opened", **pr})

    except subprocess.CalledProcessError as e:
        await notify.p1("snapshot", e)
        return _subprocess_error(e)
    except httpx.HTTPStatusError as e:
        await notify.p1("snapshot", e)
        return _github_api_error(e)
    except Exception as e:
        await notify.p0(f"Unexpected failure in snapshot: {e}", {"job": "snapshot"})
        return JSONResponse({"error": "unexpected", "message": str(e)}, status_code=500)
    finally:
        bot.cleanup()


async def _sentinel(request: Request) -> JSONResponse:
    """Run health-report.py (sentinel lite) to scan registry for issues.
    Writes a dated JSON report to data/health/ and opens a maint:green PR.

    This is a lightweight stand-in for the full Sentinel Prime skill
    invocation which requires Agent SDK (Layer 4)."""
    pat = _require_pat()
    if isinstance(pat, JSONResponse):
        return pat

    notify = get_notifier()
    bot = _BotPR(pat, "sentinel")
    try:
        bot.clone()
        result = _run(
            ["python3", "scripts/health-report.py"],
            cwd=bot.tmpdir, capture=True,
        )
        stdout = (result.stdout or "").strip()

        if not bot.has_changes():
            notify.p2_log("sentinel", {"status": "no_changes"})
            return JSONResponse({"status": "no_changes", "stdout": stdout})

        pr = await bot.open_pr(
            title=f"chore(maint): sentinel health report {bot.ts}",
            body=(
                "Daily health sweep (sentinel lite).\n\n"
                f"```\n{stdout}\n```\n\n"
                "**Tier**: `maint:green` (mechanical registry scan).\n\n"
                "Full report in `data/health/` directory.\n\n"
                "_Opened by `skill-library-bot` via `/maint/sentinel`._"
            ),
            labels=["maint:green"],
        )
        notify.p2_log("sentinel", {"status": "pr_opened", **pr})
        return JSONResponse({"status": "pr_opened", **pr})

    except subprocess.CalledProcessError as e:
        await notify.p1("sentinel", e)
        return _subprocess_error(e)
    except httpx.HTTPStatusError as e:
        await notify.p1("sentinel", e)
        return _github_api_error(e)
    except Exception as e:
        await notify.p0(f"Unexpected failure in sentinel: {e}", {"job": "sentinel"})
        return JSONResponse({"error": "unexpected", "message": str(e)}, status_code=500)
    finally:
        bot.cleanup()


async def _kb_refresh(request: Request) -> JSONResponse:
    """Run the KB pipeline: vault-sync (T0) → gap detection → T1 enrichment.

    Manages TWO clones:
      1. skill-library (source: registry, skills, scripts)
      2. skill-library-vault (target: vault notes)

    Enriched vault notes are pushed to skill-library-vault directly
    (not via PR — the vault repo doesn't have CI gating).
    """
    pat = _require_pat()
    if isinstance(pat, JSONResponse):
        return pat

    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not api_key:
        return JSONResponse(
            {"error": "ANTHROPIC_API_KEY not set — T1 enrichment unavailable"},
            status_code=503,
        )

    notify = get_notifier()
    ts = _ts()
    source_dir = tempfile.mkdtemp(prefix="maint-kb-source-")
    vault_dir = tempfile.mkdtemp(prefix="maint-kb-vault-")

    try:
        # 1. Clone source repo (skill-library)
        _run(
            ["git", "clone", "--depth", "1", "--branch", BASE_BRANCH,
             f"https://x-access-token:{pat}@github.com/{GITHUB_REPO}.git", source_dir],
            capture=True, redact=pat,
        )

        # 2. Clone vault repo (skill-library-vault)
        _run(
            ["git", "clone", "--depth", "1", "--branch", BASE_BRANCH,
             f"https://x-access-token:{pat}@github.com/{VAULT_REPO}.git", vault_dir],
            capture=True, redact=pat,
        )
        _run(["git", "config", "user.email", BOT_EMAIL], cwd=vault_dir)
        _run(["git", "config", "user.name", BOT_NAME], cwd=vault_dir)

        # 3. Run kb-pipeline from the SOURCE clone (latest code on main)
        #    The pipeline reads registry + skills from source_dir,
        #    writes enriched notes to vault_dir.
        result = _run(
            [
                "python3", "scripts/kb-pipeline.py",
                "--vault-dir", vault_dir,
                "--limit", str(KB_REFRESH_LIMIT),
            ],
            cwd=source_dir,
            capture=True,
            env={
                **os.environ,
                "ANTHROPIC_API_KEY": api_key,
            },
        )
        stdout = (result.stdout or "").strip()

        # 4. Check if vault has changes
        _run(["git", "add", "-A"], cwd=vault_dir)
        diff = subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=vault_dir)

        if diff.returncode == 0:
            notify.p2_log("kb-refresh", {"status": "no_changes"})
            return JSONResponse({
                "status": "no_changes",
                "message": "No vault updates this cycle.",
                "pipeline_stdout": stdout,
            })

        # 5. Commit and push to vault repo (direct push, no PR)
        #    The vault repo doesn't have CI — it's a content repo.
        commit_msg = (
            f"chore(kb): enrich vault notes {ts}\n\n"
            f"Automated KB pipeline run via /maint/kb-refresh.\n\n"
            f"{stdout[-500:]}"
        )
        _run(["git", "commit", "-m", commit_msg], cwd=vault_dir)
        _run(
            ["git", "push", "origin", BASE_BRANCH],
            cwd=vault_dir, capture=True, redact=pat,
        )

        notify.p2_log("kb-refresh", {"status": "pushed", "stdout_tail": stdout[-200:]})
        return JSONResponse({
            "status": "pushed",
            "message": "Vault updated and pushed.",
            "pipeline_stdout": stdout,
        })

    except subprocess.CalledProcessError as e:
        await notify.p1("kb-refresh", e)
        return _subprocess_error(e)
    except Exception as e:
        await notify.p0(f"Unexpected failure in kb-refresh: {e}", {"job": "kb-refresh"})
        return JSONResponse({"error": "unexpected", "message": str(e)}, status_code=500)
    finally:
        shutil.rmtree(source_dir, ignore_errors=True)
        shutil.rmtree(vault_dir, ignore_errors=True)


# ---------------------------------------------------------------------------
# Registration
# ---------------------------------------------------------------------------

async def _status(_request: Request) -> JSONResponse:
    """System status — last-run-per-job, config, health signals.
    Reads from in-memory notifier state (resets on container restart;
    Cloud Logging is the durable substrate)."""
    notify = get_notifier()
    return JSONResponse(notify.status())


def register(mcp) -> None:
    """Attach maintenance HTTP routes to the FastMCP instance."""
    mcp.custom_route("/health", methods=["GET"])(_health)
    mcp.custom_route("/status", methods=["GET"])(_status)
    mcp.custom_route("/maint/recalibrate", methods=["POST"])(_recalibrate)
    mcp.custom_route("/maint/validate", methods=["POST"])(_validate)
    mcp.custom_route("/maint/snapshot", methods=["POST"])(_snapshot)
    mcp.custom_route("/maint/sentinel", methods=["POST"])(_sentinel)
    mcp.custom_route("/maint/kb-refresh", methods=["POST"])(_kb_refresh)
    logger.info(
        "maintenance router mounted: /health, /status, "
        "/maint/{recalibrate,validate,snapshot,sentinel,kb-refresh}"
    )
