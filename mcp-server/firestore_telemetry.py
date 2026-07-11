"""
firestore_telemetry.py — Best-effort Firestore mirroring for telemetry events.

On Cloud Run the container filesystem is ephemeral: usage/gap/feedback jsonl
appended by _log_event is silently lost on cold start or redeploy, so cloud
usage never reaches the dashboard or score recalibration. This module mirrors
those events to Firestore, where the telemetry pull loop (Phase 3) exports
them back into git.

Design constraints (all load-bearing):
- SYNCHRONOUS writes, no background threads: Cloud Run's request-based CPU
  throttling can starve post-response threads and silently drop the write —
  exactly the loss mode being fixed. ~30-80ms per tool call is acceptable.
- Deterministic doc IDs "{session_id}_{timestamp}_{seq}" (seq = per-process
  monotonic counter): idempotent on retry, collision-free within a session
  even for same-instant events, and the (session_id, timestamp, seq) tuple is
  the pull loop's dedupe key.
- NEVER raises: a Firestore outage must not fail a tool call. Errors go to
  stderr (captured by Cloud Logging in remote mode).
- Import-guarded: without google-cloud-firestore installed this is a permanent
  no-op, so local/stdio installs are unaffected.
- The caller gates on TELEMETRY_FIRESTORE=1 in addition to remote mode —
  a developer running `--remote` locally with the library installed must not
  write telemetry into prod via ADC.
"""

import itertools
import os
import sys
import threading

try:
    from google.cloud import firestore as _firestore
except ImportError:
    _firestore = None

_client = None
_client_failed = False
_lock = threading.Lock()
_seq = itertools.count()


def _get_client():
    """Lazy singleton. Returns None if the library is missing or the client
    can't be constructed (auth/config); failure is remembered so a broken
    environment doesn't pay a retry cost on every event."""
    global _client, _client_failed
    if _firestore is None or _client_failed:
        return None
    if _client is None:
        with _lock:
            if _client is None and not _client_failed:
                try:
                    project = os.environ.get("FIRESTORE_PROJECT") or None
                    _client = _firestore.Client(project=project)
                except Exception as e:
                    _client_failed = True
                    print(f"skill-library: firestore telemetry disabled: {e}",
                          file=sys.stderr)
    return _client


def mirror_event(collection: str, record: dict) -> None:
    """Best-effort synchronous write of one telemetry record. Never raises."""
    try:
        client = _get_client()
        if client is None:
            return
        doc_id = f"{record.get('session_id', 'nosession')}_{record.get('timestamp', 'notime')}_{next(_seq)}"
        client.collection(collection).document(doc_id).set(record)
    except Exception as e:
        print(f"skill-library: firestore mirror to '{collection}' failed: {e}",
              file=sys.stderr)
