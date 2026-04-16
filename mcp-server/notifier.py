"""
Three-tier observability for the maintenance system.

Tiers:
  P0 — Critical: phone push (ntfy) + structured log. System-wide failures.
  P1 — Job failure: GitHub issue (deduplicated) + structured log.
  P2 — Info: structured log only. Success, no-ops, stats. Weekly digest reads these.

All tiers emit structured JSON to stdout (captured by Cloud Logging).
P0 and P1 additionally dispatch to external channels when configured.

Usage:
    from notifier import get_notifier
    notify = get_notifier()
    notify.p2_log("recalibrate", {"status": "no_changes"})
    await notify.p1("recalibrate", error)
    await notify.p0("PAT revoked", {"job": "recalibrate"})

The notifier also tracks last-run-per-job in memory for the /status
endpoint. This resets on container restart; Cloud Logging is the
durable substrate.
"""

import hashlib
import json
import logging
import os
import traceback
from datetime import datetime, timezone

logger = logging.getLogger("maintenance.notifier")

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

# P0: ntfy.sh or Pushover push URL. If unset, P0 only logs.
NOTIFY_P0_URL = os.environ.get("NOTIFY_P0_URL", "")

# P1: GitHub repo for issue creation. Uses GITHUB_BOT_PAT for auth.
NOTIFY_P1_REPO = os.environ.get("NOTIFY_P1_REPO", "npbuilds/skill-library")

# P2: email for weekly digest (used by scripts/weekly-digest.py, not by notifier directly)
NOTIFY_P2_EMAIL = os.environ.get("NOTIFY_P2_EMAIL", "")

# Escalation threshold: P1 → P0 after this many comments on one issue
P1_ESCALATION_THRESHOLD = 5


# ---------------------------------------------------------------------------
# Notifier class
# ---------------------------------------------------------------------------

class Notifier:
    """Singleton observability dispatcher for the maintenance system."""

    def __init__(self):
        self._last_runs: dict[str, dict] = {}
        self._p0_url = NOTIFY_P0_URL
        self._p1_repo = NOTIFY_P1_REPO
        self._p1_pat = os.environ.get("GITHUB_BOT_PAT", "")

    # -- Structured logging (all tiers) -----------------------------------

    def _emit(self, entry: dict) -> None:
        """Emit structured JSON to stdout → Cloud Logging."""
        record = {
            "ts": datetime.now(timezone.utc).isoformat(),
            **entry,
        }
        # MAINT_LOG prefix makes these greppable in Cloud Logging
        logger.info("MAINT_LOG %s", json.dumps(record, default=str))
        # Track last run per job
        job = entry.get("job", "unknown")
        self._last_runs[job] = record

    # -- P0: Critical (phone push) ----------------------------------------

    async def p0(self, msg: str, context: dict | None = None) -> None:
        """System-wide critical failure. Push notification + log."""
        entry = {"severity": "P0", "message": msg, **(context or {})}
        self._emit(entry)

        if self._p0_url:
            try:
                import httpx
                async with httpx.AsyncClient(timeout=10.0) as client:
                    resp = await client.post(
                        self._p0_url,
                        content=f"[P0] {msg}",
                        headers={"Title": "skill-library P0", "Priority": "urgent"},
                    )
                    if resp.status_code >= 400:
                        logger.warning("P0 push failed: %s %s", resp.status_code, resp.text[:200])
            except Exception as e:
                logger.error("P0 push dispatch failed: %s", e)
        else:
            logger.critical("P0 (no push URL configured): %s", msg)

    # -- P1: Job failure (GitHub issue) ------------------------------------

    async def p1(self, job: str, error: Exception, context: dict | None = None) -> None:
        """Single job failure. Creates or updates a GitHub issue + logs."""
        sig = self._error_signature(job, error)
        tb = "".join(traceback.format_exception(type(error), error, error.__traceback__))
        entry = {
            "severity": "P1",
            "job": job,
            "error": str(error),
            "error_type": type(error).__name__,
            "signature": sig,
            **(context or {}),
        }
        self._emit(entry)

        if self._p1_pat and self._p1_repo:
            try:
                await self._upsert_issue(sig, job, error, tb)
            except Exception as e:
                logger.error("P1 GitHub issue dispatch failed: %s", e)
        else:
            logger.error("P1 (no GitHub PAT/repo configured): %s: %s", job, error)

    async def _upsert_issue(self, sig: str, job: str, error: Exception, tb: str) -> None:
        """Find open issue with same signature → comment. Otherwise create new."""
        import httpx

        headers = {
            "Authorization": f"token {self._p1_pat}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        }
        marker = f"<!-- maint-sig:{sig} -->"
        now = datetime.now(timezone.utc).isoformat()

        async with httpx.AsyncClient(timeout=30.0) as client:
            # Search for existing open issue with this signature
            search_resp = await client.get(
                "https://api.github.com/search/issues",
                headers=headers,
                params={
                    "q": f"repo:{self._p1_repo} is:issue is:open label:maint:failed \"{sig}\" in:body",
                },
            )

            existing = None
            if search_resp.status_code == 200:
                items = search_resp.json().get("items", [])
                if items:
                    existing = items[0]

            if existing:
                # Comment on existing issue
                comment_body = (
                    f"**Recurrence** at `{now}`\n\n"
                    f"```\n{str(error)[:500]}\n```\n\n"
                    f"{marker}"
                )
                await client.post(
                    f"https://api.github.com/repos/{self._p1_repo}/issues/{existing['number']}/comments",
                    headers=headers,
                    json={"body": comment_body},
                )
                logger.info("P1 commented on issue #%s (sig: %s)", existing["number"], sig[:12])

                # Check escalation threshold
                comments_resp = await client.get(
                    f"https://api.github.com/repos/{self._p1_repo}/issues/{existing['number']}/comments",
                    headers=headers,
                    params={"per_page": 100},
                )
                if comments_resp.status_code == 200:
                    comment_count = len(comments_resp.json())
                    if comment_count >= P1_ESCALATION_THRESHOLD:
                        await self.p0(
                            f"P1→P0 escalation: issue #{existing['number']} has {comment_count} comments (job: {job})",
                            {"job": job, "issue": existing["number"], "escalated_from": "P1"},
                        )
            else:
                # Create new issue
                tb_truncated = tb[:2000] if len(tb) > 2000 else tb
                issue_body = (
                    f"**Job**: `{job}`\n"
                    f"**Error**: `{type(error).__name__}: {str(error)[:200]}`\n"
                    f"**Time**: `{now}`\n\n"
                    f"### Traceback\n```\n{tb_truncated}\n```\n\n"
                    f"### Signature\n{marker}\n`{sig}`\n\n"
                    f"_Created by maintenance notifier (P1)._"
                )
                create_resp = await client.post(
                    f"https://api.github.com/repos/{self._p1_repo}/issues",
                    headers=headers,
                    json={
                        "title": f"[maint:failed] {job}: {type(error).__name__}",
                        "body": issue_body,
                        "labels": ["maint:failed"],
                    },
                )
                if create_resp.status_code in (200, 201):
                    issue = create_resp.json()
                    logger.info("P1 created issue #%s for job %s", issue["number"], job)
                else:
                    logger.warning("P1 issue creation failed: %s", create_resp.text[:300])

    # -- P2: Info (structured log only) ------------------------------------

    def p2_log(self, job: str, outcome: dict) -> None:
        """Success or info event. Logged only — weekly digest reads these."""
        entry = {"severity": "P2", "job": job, **outcome}
        self._emit(entry)

    # -- Status (for /status endpoint) -------------------------------------

    def status(self) -> dict:
        """Current status snapshot for the /status HTTP endpoint."""
        return {
            "service": "skill-library-mcp",
            "last_runs": {
                job: {
                    "ts": run.get("ts"),
                    "severity": run.get("severity"),
                    "status": run.get("status", run.get("message", "unknown")),
                }
                for job, run in self._last_runs.items()
            },
            "p0_configured": bool(self._p0_url),
            "p1_configured": bool(self._p1_pat and self._p1_repo),
            "autonomy": os.environ.get("MAINTENANCE_AUTONOMY", "conservative"),
        }

    # -- Helpers -----------------------------------------------------------

    @staticmethod
    def _error_signature(job: str, error: Exception) -> str:
        """Stable hash for deduplicating recurring failures."""
        key = f"{job}:{type(error).__name__}:{str(error)[:100]}"
        return hashlib.sha256(key.encode()).hexdigest()[:16]


# ---------------------------------------------------------------------------
# Singleton
# ---------------------------------------------------------------------------

_instance: Notifier | None = None


def get_notifier() -> Notifier:
    global _instance
    if _instance is None:
        _instance = Notifier()
    return _instance
