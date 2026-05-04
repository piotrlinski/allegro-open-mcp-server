"""Allegro versioned media-type helpers.

Allegro versions its REST API via the ``Accept`` and ``Content-Type``
headers — every endpoint expects ``application/vnd.allegro.public.v1+json``
or ``application/vnd.allegro.beta.v1+json`` rather than a path-prefix like
``/v1/...``.

This module centralises the constant strings and a tiny resolver so callers
can ask "what Accept header does this endpoint want?" without sprinkling
mime-type literals through the codebase.
"""

from __future__ import annotations

GA_JSON = "application/vnd.allegro.public.v1+json"
"""GA media type — the default for every endpoint Allegro promotes to stable."""

BETA_JSON = "application/vnd.allegro.beta.v1+json"
"""Beta media type — used for endpoints flagged as beta in the OpenAPI spec."""

# Endpoints/path prefixes that require the beta media type at time of writing.
# Keys are matched as **prefixes** (so ``/returns`` covers ``/returns/{id}`` etc.).
# Update via the OpenAPI spec; see ``scripts/check_models_freshness.py``.
_BETA_PREFIXES: tuple[str, ...] = (
    "/sale/offers/batch/price-and-stock",
    "/returns",
)


def resolve(path: str) -> str:
    """Return the Accept/Content-Type media type for the given API path.

    Falls back to the GA media type if the path doesn't match a known beta
    prefix. Path is matched on the leading characters; case-sensitive
    because Allegro's paths are.
    """
    for prefix in _BETA_PREFIXES:
        if path.startswith(prefix):
            return BETA_JSON
    return GA_JSON


__all__ = ["BETA_JSON", "GA_JSON", "resolve"]
