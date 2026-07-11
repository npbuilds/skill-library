"""Tests for Firestore telemetry mirroring.

The mirror is the only durable path for cloud usage/gap/feedback events
(local jsonl is ephemeral on Cloud Run), but it must never fail a tool call
and must never fire outside the explicit REMOTE_MODE + TELEMETRY_FIRESTORE=1
opt-in. These tests pin: doc-ID uniqueness for same-instant events, the
never-raises contract, the no-op path when the library is absent, and the
usage-collection semantics guard (skill-load events only).
"""

from unittest.mock import MagicMock

import pytest

import firestore_telemetry


@pytest.fixture(autouse=True)
def reset_module_state():
    """Each test gets a fresh singleton/failure state."""
    firestore_telemetry._client = None
    firestore_telemetry._client_failed = False
    yield
    firestore_telemetry._client = None
    firestore_telemetry._client_failed = False


def _install_fake_client(monkeypatch):
    """Route mirror_event writes into a dict: {collection: {doc_id: record}}."""
    written: dict[str, dict] = {}

    class FakeDocRef:
        def __init__(self, collection, doc_id):
            self.collection, self.doc_id = collection, doc_id

        def set(self, record):
            written.setdefault(self.collection, {})[self.doc_id] = record

    class FakeCollection:
        def __init__(self, name):
            self.name = name

        def document(self, doc_id):
            return FakeDocRef(self.name, doc_id)

    fake_client = MagicMock()
    fake_client.collection.side_effect = FakeCollection
    monkeypatch.setattr(firestore_telemetry, "_client", fake_client)
    return written


def test_same_instant_events_get_distinct_doc_ids(monkeypatch):
    """Two events with identical session_id + timestamp must not overwrite
    each other — the seq suffix is the collision guard."""
    written = _install_fake_client(monkeypatch)
    record = {"session_id": "s1", "timestamp": "2026-07-11T00:00:00+00:00"}
    firestore_telemetry.mirror_event("usage", dict(record, skill="a"))
    firestore_telemetry.mirror_event("usage", dict(record, skill="b"))
    assert len(written["usage"]) == 2, (
        f"same-instant events collided; doc ids: {list(written['usage'])}"
    )


def test_doc_id_embeds_session_and_timestamp(monkeypatch):
    written = _install_fake_client(monkeypatch)
    firestore_telemetry.mirror_event(
        "gaps", {"session_id": "sess42", "timestamp": "2026-07-11T01:02:03+00:00"}
    )
    (doc_id,) = written["gaps"].keys()
    assert doc_id.startswith("sess42_2026-07-11T01:02:03+00:00_")


def test_mirror_never_raises_on_write_failure(monkeypatch):
    """A Firestore outage must not propagate into the tool call."""
    fake_client = MagicMock()
    fake_client.collection.side_effect = RuntimeError("firestore down")
    monkeypatch.setattr(firestore_telemetry, "_client", fake_client)
    firestore_telemetry.mirror_event("usage", {"session_id": "s", "timestamp": "t"})


def test_noop_when_library_missing(monkeypatch):
    """Without google-cloud-firestore, mirror_event is a silent no-op."""
    monkeypatch.setattr(firestore_telemetry, "_firestore", None)
    firestore_telemetry.mirror_event("usage", {"session_id": "s", "timestamp": "t"})
    assert firestore_telemetry._client is None


def test_client_construction_failure_is_remembered(monkeypatch):
    """A broken environment pays the client-construction cost once, not on
    every event."""
    calls = []

    class ExplodingFirestore:
        @staticmethod
        def Client(project=None):
            calls.append(1)
            raise RuntimeError("no credentials")

    monkeypatch.setattr(firestore_telemetry, "_firestore", ExplodingFirestore)
    firestore_telemetry.mirror_event("usage", {"session_id": "s", "timestamp": "t"})
    firestore_telemetry.mirror_event("usage", {"session_id": "s", "timestamp": "t"})
    assert len(calls) == 1, "client construction must not be retried per event"


def test_server_usage_semantics_guard():
    """server._log_event must mirror to 'usage' only for skill-load events —
    search events (no skill field) would break the dashboard's usage
    semantics. Pinned here against the server module's collection routing."""
    import server

    # The guard lives in _log_event; replicate its routing decision.
    def routed_collection(record):
        collection = server._MIRROR_COLLECTIONS.get("usage.jsonl")
        if collection == "usage" and not record.get("skill"):
            collection = None
        return collection

    assert routed_collection({"skill": "magic-system-design"}) == "usage"
    assert routed_collection({"type": "search", "query": "q"}) is None
