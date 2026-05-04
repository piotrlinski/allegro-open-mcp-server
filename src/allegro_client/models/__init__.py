"""Pydantic models for Allegro REST API payloads.

The bulk of these are generated from the official OpenAPI spec at
``https://developer.allegro.pl/swagger.yaml`` into the ``_generated``
subpackage. This module curates a flat public re-export surface so callers
write ``from allegro_client.models import Offer`` instead of navigating
the generated tree.

Run ``make gen-models`` to refresh ``_generated/`` from the upstream spec.

Hand-written types (validators, forward-compat shims, anything codegen
leaves gaps for) live in :mod:`allegro_client.models.common`.
"""

from __future__ import annotations

# The curated re-export list lands here once `make gen-models` produces
# `_generated/`. Until codegen runs, only hand-written common types are
# importable.
from .common import Marketplace, Money, PaginationInfo

__all__ = [
    "Marketplace",
    "Money",
    "PaginationInfo",
]
