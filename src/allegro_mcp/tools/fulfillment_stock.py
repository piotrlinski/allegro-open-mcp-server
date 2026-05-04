# ruff: noqa
"""Generated MCP tools — DO NOT EDIT.

Run ``make gen-tools`` to regenerate from the cached OpenAPI spec.
Tag: Fulfillment Stock
"""

from __future__ import annotations

from typing import Any, cast

from ..errors import ErrorResponse
from ._decorators import requires_writes_enabled
from ._runtime import allegro_call, get_client, mcp


@mcp.tool
@allegro_call
def get_fulfillment_stock(
    *,
    offset: int | None = None,
    limit: int | None = None,
    phrase: str | None = None,
    sort: str | None = None,
    productId: str | None = None,
    productAvailability: list[str] | None = None,
    productStatus: str | None = None,
    asnStatus: str | None = None,
    outOfStockInFrom: int | None = None,
    outOfStockInTo: int | None = None,
) -> dict[str, Any] | ErrorResponse:
    """Get available stock

    Use this resource to get a list of the products belonging to the seller, which are in Allegro Warehouse. Read more: <a href="../../tutorials/one-fulfillment-by-allegro-0ADwgOLqWSw#jak-pobrac-aktualne-stany-magazynowe" target="_blank">PL</a> / <a href="../../tutorials/one-fulfillment-by-allegro-4R9dXyMPlc9#get-available-stock" target="_blank">EN</a>.


    HTTP: ``GET /fulfillment/stock``
    """
    params = {
        "offset": offset,
        "limit": limit,
        "phrase": phrase,
        "sort": sort,
        "productId": productId,
        "productAvailability": productAvailability,
        "productStatus": productStatus,
        "asnStatus": asnStatus,
        "outOfStockInFrom": outOfStockInFrom,
        "outOfStockInTo": outOfStockInTo,
    }
    response = get_client().request_json(
        "GET",
        f"/fulfillment/stock",
        params=params,
    )
    return cast(dict[str, Any], response)
