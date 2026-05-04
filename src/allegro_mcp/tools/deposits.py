# ruff: noqa
"""Generated MCP tools — DO NOT EDIT.

Run ``make gen-tools`` to regenerate from the cached OpenAPI spec.
Tag: Deposits
"""

from __future__ import annotations

from typing import Any, cast

from ..errors import ErrorResponse
from ._decorators import requires_writes_enabled
from ._runtime import allegro_call, get_client, mcp


@mcp.tool
@allegro_call
def get_deposit_types() -> dict[str, Any] | ErrorResponse:
    """Get deposit types

    Use this resource to get deposit types available when creating an offer. Read more: <a href="../../news/1-pazdziernika-2025-dostosujemy-allegro-api-do-rozporzadzenia-o-systemie-kaucyjnym-m0mLB4XM9Ib" target="_blank">PL</a> / <a href="../../news/on-october-1-2025-we-will-adapt-Allegro-API-to-the-deposit-system-regulation-m0mLB4XM9Ib" target="_blank">EN</a>.


    HTTP: ``GET /deposit/types``
    """
    params: dict[str, Any] = {}
    response = get_client().request_json(
        "GET",
        f"/deposit/types",
        params=params,
    )
    return cast(dict[str, Any], response)
