"""Deterministic canonicalisation and content-addressing primitives."""
from __future__ import annotations

import hashlib
import json
from typing import Any

__all__ = ["canonical_json", "digest", "idempotency_key", "short_id", "canonical_bytes"]


def _default(obj: Any) -> Any:
    if isinstance(obj, (set, frozenset)):
        return sorted((_sort_key(item) for item in obj), key=lambda pair: pair[0])
