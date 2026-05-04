# ruff: noqa
"""Generated MCP tools — DO NOT EDIT.

Run ``make gen-tools`` to regenerate from the cached OpenAPI spec.
Tag: Fulfillment Parcels
"""

from __future__ import annotations

from typing import Any, cast

from ..errors import ErrorResponse
from ._decorators import requires_writes_enabled
from ._runtime import allegro_call, get_client, mcp


@mcp.tool
@allegro_call
def get_fulfillment_order_parcels(*, orderId: str) -> dict[str, Any] | ErrorResponse:
    """Get list of shipped parcels

    Use this resource to get list of parcels and included items for a given order. Items include detailed information such as expiration dates and serial numbers. Read more: <a href="../../tutorials/one-fulfillment-by-allegro-0ADwgOLqWSw#jak-obslugiwac-zamowienia" target="_blank">PL</a> / <a href="../../tutorials/one-fulfillment-by-allegro-4R9dXyMPlc9#how-to-handle-orders" target="_blank">EN</a>.


    HTTP: ``GET /fulfillment/orders/{orderId}/parcels``
    """
    params: dict[str, Any] = {}
    response = get_client().request_json(
        "GET",
        f"/fulfillment/orders/{orderId}/parcels",
        params=params,
    )
    return cast(dict[str, Any], response)
