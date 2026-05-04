# ruff: noqa
"""Generated MCP tools — DO NOT EDIT.

Run ``make gen-tools`` to regenerate from the cached OpenAPI spec.
Tag: Commission refunds
"""

from __future__ import annotations

from typing import Any, cast

from ..errors import ErrorResponse
from ._decorators import requires_writes_enabled
from ._runtime import allegro_call, get_client, mcp


@mcp.tool
@allegro_call
def get_refund_application(*, claimId: str) -> dict[str, Any] | ErrorResponse:
    """Get a refund application details

    Use this resource to get refund application details. Read more: <a href="../../tutorials/jak-obslugiwac-zamowienia-GRaj0qyvwtR#jak-pobrac-pojedynczy-wniosek-o-rabat-transakcyjny" target="_blank">PL</a> / <a href="../../tutorials/process-orders-PgPMlWDr8Cv#how-to-retrieve-single-sale-commission-refund" target="_blank">EN</a>.


    HTTP: ``GET /order/refund-claims/{claimId}``
    """
    params: dict[str, Any] = {}
    response = get_client().request_json(
        "GET",
        f"/order/refund-claims/{claimId}",
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
@requires_writes_enabled
def cancel_refund_application(*, claimId: str) -> dict[str, Any] | ErrorResponse:
    """Cancel a refund application

    Use this resource to cancel a refund application. This cannot be undone. Read more: <a href="../../tutorials/jak-obslugiwac-zamowienia-GRaj0qyvwtR#jak-anulowac-wniosek-o-rabat-transakcyjny" target="_blank">PL</a> / <a href="../../tutorials/process-orders-PgPMlWDr8Cv#how-to-cancel-sale-commission-refund" target="_blank">EN</a>.


    HTTP: ``DELETE /order/refund-claims/{claimId}``
    """
    params: dict[str, Any] = {}
    response = get_client().request_json(
        "DELETE",
        f"/order/refund-claims/{claimId}",
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
def get_refund_applications(
    *,
    lineItem_offer_id: str | None = None,
    buyer_id: str | None = None,
    status: str | None = None,
    limit: int | None = None,
    offset: int | None = None,
) -> dict[str, Any] | ErrorResponse:
    """Get a list of refund applications

    Use this resource to get a list of refund applications based on the provided query parameters. Read more: <a href="../../tutorials/jak-obslugiwac-zamowienia-GRaj0qyvwtR#jak-pobrac-liste-utworzonych-wnioskow-o-rabat-transakcyjny" target="_blank">PL</a> / <a href="../../tutorials/process-orders-PgPMlWDr8Cv#how-to-retrieve-list-of-sale-commission-refunds" target="_blank">EN</a>.


    HTTP: ``GET /order/refund-claims``
    """
    params = {
        "lineItem.offer.id": lineItem_offer_id,
        "buyer.id": buyer_id,
        "status": status,
        "limit": limit,
        "offset": offset,
    }
    response = get_client().request_json(
        "GET",
        f"/order/refund-claims",
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
@requires_writes_enabled
def create_refund_application(
    *, body: dict[str, Any] | None = None
) -> dict[str, Any] | ErrorResponse:
    """Create a refund application

    Use this resource to create a refund application. Read more: <a href="../../tutorials/jak-obslugiwac-zamowienia-GRaj0qyvwtR#jak-utworzyc-wniosek-o-rabat-transakcyjny" target="_blank">PL</a> / <a href="../../tutorials/process-orders-PgPMlWDr8Cv#how-to-create-a-sale-commission-refund-application" target="_blank">EN</a>.


    HTTP: ``POST /order/refund-claims``
    """
    params: dict[str, Any] = {}
    response = get_client().request_json(
        "POST",
        f"/order/refund-claims",
        json=body,
        params=params,
    )
    return cast(dict[str, Any], response)
