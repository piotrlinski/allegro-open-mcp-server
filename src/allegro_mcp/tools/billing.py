# ruff: noqa
"""Generated MCP tools — DO NOT EDIT.

Run ``make gen-tools`` to regenerate from the cached OpenAPI spec.
Tag: Billing
"""

from __future__ import annotations

from typing import Any, cast

from ..errors import ErrorResponse
from ._decorators import requires_writes_enabled
from ._runtime import allegro_call, get_client, mcp


@mcp.tool
@allegro_call
def get_billing_entries(
    *,
    marketplaceId: str | None = None,
    occurredAt_gte: str | None = None,
    occurredAt_lte: str | None = None,
    type_id: list[str] | None = None,
    offer_id: str | None = None,
    order_id: str | None = None,
    limit: int | None = None,
    offset: int | None = None,
) -> dict[str, Any] | ErrorResponse:
    """Get a list of billing entries

    Use this resource to get a list of billing entries. The billing entries are sorted in descending order (newest first) by the date on which they occurred. Read more: <a href="../../tutorials/jak-sprawdzic-oplaty-nn9DOL5PASX#historia-operacji-billingowych" target="_blank">PL</a> / <a href="../../tutorials/how-to-check-the-fees-3An6Wame3Um#billing-operations" target="_blank">EN</a>.


    HTTP: ``GET /billing/billing-entries``
    """
    params = {
        "marketplaceId": marketplaceId,
        "occurredAt.gte": occurredAt_gte,
        "occurredAt.lte": occurredAt_lte,
        "type.id": type_id,
        "offer.id": offer_id,
        "order.id": order_id,
        "limit": limit,
        "offset": offset,
    }
    response = get_client().request_json(
        "GET",
        f"/billing/billing-entries",
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
def get_billing_types() -> dict[str, Any] | ErrorResponse:
    """Get a list of billing types

    Use this resource to get a list of all billing types. Type names are localized according to the "Accept-Language" header. Read more: <a href="../../tutorials/jak-sprawdzic-oplaty-nn9DOL5PASX#historia-operacji-billingowych" target="_blank">PL</a> / <a href="../../tutorials/how-to-check-the-fees-3An6Wame3Um#billing-operations" target="_blank">EN</a>.


    HTTP: ``GET /billing/billing-types``
    """
    params: dict[str, Any] = {}
    response = get_client().request_json(
        "GET",
        f"/billing/billing-types",
        params=params,
    )
    return cast(dict[str, Any], response)
