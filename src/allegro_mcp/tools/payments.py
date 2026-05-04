# ruff: noqa
"""Generated MCP tools — DO NOT EDIT.

Run ``make gen-tools`` to regenerate from the cached OpenAPI spec.
Tag: Payments
"""

from __future__ import annotations

from typing import Any, cast

from ..errors import ErrorResponse
from ._decorators import requires_writes_enabled
from ._runtime import allegro_call, get_client, mcp


@mcp.tool
@allegro_call
def get_payments_operation_history(
    *,
    wallet_type: str | None = None,
    wallet_paymentOperator: str | None = None,
    payment_id: str | None = None,
    participant_login: str | None = None,
    occurredAt_gte: str | None = None,
    occurredAt_lte: str | None = None,
    group: list[str] | None = None,
    marketplaceId: str | None = None,
    currency: str | None = None,
    limit: int | None = None,
    offset: int | None = None,
) -> dict[str, Any] | ErrorResponse:
    """Payment operations history

    Use this endpoint to get the list of the seller payment operations. Read more: <a href="../../tutorials/jak-sprawdzic-oplaty-nn9DOL5PASX#historia-operacji-platniczych" target="_blank">PL</a> / <a href="../../tutorials/how-to-check-the-fees-3An6Wame3Um#payment-operations" target="_blank">EN</a>.


    HTTP: ``GET /payments/payment-operations``
    """
    params = {
        "wallet.type": wallet_type,
        "wallet.paymentOperator": wallet_paymentOperator,
        "payment.id": payment_id,
        "participant.login": participant_login,
        "occurredAt.gte": occurredAt_gte,
        "occurredAt.lte": occurredAt_lte,
        "group": group,
        "marketplaceId": marketplaceId,
        "currency": currency,
        "limit": limit,
        "offset": offset,
    }
    response = get_client().request_json(
        "GET",
        f"/payments/payment-operations",
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
@requires_writes_enabled
def initiate_refund(*, body: dict[str, Any] | None = None) -> dict[str, Any] | ErrorResponse:
    """Initiate a refund of a payment

    Use this endpoint to initiate a refund of a payment. Read more: <a href="../../tutorials/jak-obslugiwac-zamowienia-GRaj0qyvwtR#jak-wykonac-zwrot-platnosci" target="_blank">PL</a> / <a href="../../tutorials/process-orders-PgPMlWDr8Cv#how-to-refund-a-payment" target="_blank">EN</a>.


    HTTP: ``POST /payments/refunds``
    """
    params: dict[str, Any] = {}
    response = get_client().request_json(
        "POST",
        f"/payments/refunds",
        json=body,
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
def get_refunded_payments(
    *,
    limit: int | None = None,
    offset: int | None = None,
    id: str | None = None,
    payment_id: str | None = None,
    order_id: str | None = None,
    occurredAt_gte: str | None = None,
    occurredAt_lte: str | None = None,
    status: list[str] | None = None,
) -> dict[str, Any] | ErrorResponse:
    """Get a list of refunded payments

    Get a list of refunded payments. Read more: <a href="../../tutorials/jak-obslugiwac-zamowienia-GRaj0qyvwtR#jak-pobrac-liste-zwrotow-platnosci" target="_blank">PL</a> / <a href="../../tutorials/process-orders-PgPMlWDr8Cv#how-to-retrieve-a-list-of-refunded-payment" target="_blank">EN</a>.


    HTTP: ``GET /payments/refunds``
    """
    params = {
        "limit": limit,
        "offset": offset,
        "id": id,
        "payment.id": payment_id,
        "order.id": order_id,
        "occurredAt.gte": occurredAt_gte,
        "occurredAt.lte": occurredAt_lte,
        "status": status,
    }
    response = get_client().request_json(
        "GET",
        f"/payments/refunds",
        params=params,
    )
    return cast(dict[str, Any], response)
