# ruff: noqa
"""Generated MCP tools — DO NOT EDIT.

Run ``make gen-tools`` to regenerate from the cached OpenAPI spec.
Tag: Fulfillment Products
"""

from __future__ import annotations

from typing import Any, cast

from ..errors import ErrorResponse
from ._decorators import requires_writes_enabled
from ._runtime import allegro_call, get_client, mcp


@mcp.tool
@allegro_call
def get_available_products(
    *, offset: int | None = None, limit: int | None = None
) -> dict[str, Any] | ErrorResponse:
    """Get list of available products

    Use this resource to get a list of products that can be added to Advance Ship Notice. The list contains products for which the seller has created offers and is ordered by product's name. Read more: <a href="../../tutorials/one-fulfillment-by-allegro-0ADwgOLqWSw#sprawdz-dostepne-produkty-do-awizacji" target="_blank">PL</a> / <a href="../../tutorials/one-fulfillment-by-allegro-4R9dXyMPlc9#check-available-products-for-asn" target="_blank">EN</a>.


    HTTP: ``GET /fulfillment/available-products``
    """
    params = {
        "offset": offset,
        "limit": limit,
    }
    response = get_client().request_json(
        "GET",
        f"/fulfillment/available-products",
        params=params,
    )
    return cast(dict[str, Any], response)
