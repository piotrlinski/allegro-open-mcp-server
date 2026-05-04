# ruff: noqa
"""Generated MCP tools — DO NOT EDIT.

Run ``make gen-tools`` to regenerate from the cached OpenAPI spec.
Tag: Customer returns
"""

from __future__ import annotations

from typing import Any, cast

from ..errors import ErrorResponse
from ._decorators import requires_writes_enabled
from ._runtime import allegro_call, get_client, mcp


@mcp.tool
@allegro_call
def get_customer_returns(
    *,
    customerReturnId: str | None = None,
    orderId: str | None = None,
    buyer_email: str | None = None,
    buyer_login: str | None = None,
    items_offerId: str | None = None,
    items_name: str | None = None,
    parcels_waybill: str | None = None,
    parcels_transportingWaybill: str | None = None,
    parcels_carrierId: str | None = None,
    parcels_transportingCarrierId: str | None = None,
    parcels_sender_phoneNumber: str | None = None,
    referenceNumber: str | None = None,
    from_: str | None = None,
    createdAt_gte: str | None = None,
    createdAt_lte: str | None = None,
    marketplaceId: str | None = None,
    status: str | None = None,
    limit: int | None = None,
    offset: int | None = None,
) -> dict[str, Any] | ErrorResponse:
    """[BETA] Get customer returns by provided query parameters

    Use this resource to get all customer returns filtered by query parameters. Read more: <a href="../../tutorials/jak-obslugiwac-zamowienia-GRaj0qyvwtR#jak-pobrac-liste-zwrotow" target="_blank">PL</a> / <a href="../../tutorials/process-orders-PgPMlWDr8Cv#how-to-retrieve-customer-returns-list" target="_blank">EN</a>. This resource is limited to 25 requests per second for a single user and 50 requests per second for clientId.


    HTTP: ``GET /order/customer-returns``
    """
    params = {
        "customerReturnId": customerReturnId,
        "orderId": orderId,
        "buyer.email": buyer_email,
        "buyer.login": buyer_login,
        "items.offerId": items_offerId,
        "items.name": items_name,
        "parcels.waybill": parcels_waybill,
        "parcels.transportingWaybill": parcels_transportingWaybill,
        "parcels.carrierId": parcels_carrierId,
        "parcels.transportingCarrierId": parcels_transportingCarrierId,
        "parcels.sender.phoneNumber": parcels_sender_phoneNumber,
        "referenceNumber": referenceNumber,
        "from": from_,
        "createdAt.gte": createdAt_gte,
        "createdAt.lte": createdAt_lte,
        "marketplaceId": marketplaceId,
        "status": status,
        "limit": limit,
        "offset": offset,
    }
    response = get_client().request_json(
        "GET",
        f"/order/customer-returns",
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
def get_customer_return_by_id(*, customerReturnId: str) -> dict[str, Any] | ErrorResponse:
    """[BETA] Get customer return by id

    Use this resource to get customer returns by its identifier. Read more: <a href="../../tutorials/jak-obslugiwac-zamowienia-GRaj0qyvwtR#jak-pobrac-szczegolowe-informacje-o-zwrocie" target="_blank">PL</a> / <a href="../../tutorials/process-orders-PgPMlWDr8Cv#how-to-retrieve-detailed-information-about-customer-return" target="_blank">EN</a>.


    HTTP: ``GET /order/customer-returns/{customerReturnId}``
    """
    params: dict[str, Any] = {}
    response = get_client().request_json(
        "GET",
        f"/order/customer-returns/{customerReturnId}",
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
@requires_writes_enabled
def reject_customer_return_refund(
    *, customerReturnId: str, body: dict[str, Any] | None = None
) -> dict[str, Any] | ErrorResponse:
    """[BETA] Reject customer return refund

    Use this resource to reject customer return refund with provided reason. Read more: <a href="../../tutorials/jak-obslugiwac-zamowienia-GRaj0qyvwtR#jak-odmowic-zwrotu-wplaty" target="_blank">PL</a> / <a href="../../tutorials/process-orders-PgPMlWDr8Cv#how-to-reject-customer-return-refund" target="_blank">EN</a>.


    HTTP: ``POST /order/customer-returns/{customerReturnId}/rejection``
    """
    params: dict[str, Any] = {}
    response = get_client().request_json(
        "POST",
        f"/order/customer-returns/{customerReturnId}/rejection",
        json=body,
        params=params,
    )
    return cast(dict[str, Any], response)
