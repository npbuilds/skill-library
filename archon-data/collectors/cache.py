"""TTL-based file cache for API responses."""

import json
import math
import time
from pathlib import Path

CACHE_DIR = Path(__file__).parent.parent / "cache"


class _NaNSafeEncoder(json.JSONEncoder):
    """JSON encoder that converts NaN/Infinity to None.

    Also handles numpy numeric types (float64, int64) which yfinance and
    fredapi return — these aren't caught by isinstance(o, float).
    """

    def default(self, o):
        try:
            f = float(o)
            if math.isnan(f) or math.isinf(f):
                return None
            return f
        except (TypeError, ValueError):
            pass
        return str(o)

    def encode(self, o):
        return super().encode(self._clean(o))

    def _clean(self, o):
        if isinstance(o, float):
            if math.isnan(o) or math.isinf(o):
                return None
            return o
        if hasattr(o, '__float__') and not isinstance(o, (int, bool, str)):
            try:
                f = float(o)
                if math.isnan(f) or math.isinf(f):
                    return None
                return f
            except (TypeError, ValueError):
                pass
        if isinstance(o, dict):
            return {k: self._clean(v) for k, v in o.items()}
        if isinstance(o, (list, tuple)):
            return [self._clean(v) for v in o]
        return o


def get_cached(key: str, ttl_seconds: int) -> dict | None:
    """Return cached data if fresh, None if stale or missing."""
    path = CACHE_DIR / f"{key}.json"
    if not path.exists():
        return None
    try:
        data = json.loads(path.read_text())
        if time.time() - data.get("_cached_at", 0) < ttl_seconds:
            return data
    except (json.JSONDecodeError, OSError):
        pass
    return None


def set_cached(key: str, data: dict) -> None:
    """Write a COPY of data to cache with timestamp. Does not mutate the input."""
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    cache_copy = {**data, "_cached_at": time.time()}
    try:
        (CACHE_DIR / f"{key}.json").write_text(
            json.dumps(cache_copy, cls=_NaNSafeEncoder)
        )
    except OSError:
        pass


def get_stale(key: str) -> dict | None:
    """Return the last cached payload regardless of age, or None if missing.

    Fallback for when a live fetch fails: serving last-known-good data (tagged
    stale by the caller) beats serving nothing. Callers should skip payloads
    that themselves carry an "error" key.
    """
    path = CACHE_DIR / f"{key}.json"
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text())
    except (json.JSONDecodeError, OSError):
        return None
