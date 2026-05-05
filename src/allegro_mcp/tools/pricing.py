# ruff: noqa
"""Generated MCP tools — DO NOT EDIT.

Run ``make gen-tools`` to regenerate from the cached OpenAPI spec.
Tag: Pricing
"""

from __future__ import annotations

from typing import Any, cast

from ..errors import ErrorResponse
from ._decorators import requires_writes_enabled
from ._runtime import allegro_call, get_client, mcp


@mcp.tool
@allegro_call
@requires_writes_enabled
def calculate_fee_preview(*, body: dict[str, Any] | None = None) -> dict[str, Any] | ErrorResponse:
    """Calculate fee and commission for an offer

    Provides information about fee and commission for an offer. This resource is limited to 25 requests per second for a single user. Read more: <a href="../../tutorials/jak-sprawdzic-oplaty-nn9DOL5PASX#kalkulator-oplat" target="_blank">PL</a> / <a href="../../tutorials/how-to-check-the-fees-3An6Wame3Um#fee-calculator" target="_blank">EN</a>.


    HTTP: ``POST /pricing/offer-fee-preview``
    """
    params: dict[str, Any] = {}
    response = get_client().request_json(
        "POST",
        f"/pricing/offer-fee-preview",
        json=body,
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
def offer_quotes_public(*, offer_id: list[str] | None = None) -> dict[str, Any] | ErrorResponse:
    """Get the user's current offer quotes

    This endpoint returns current offer quotes (listing and promo fees) cycles for authenticated user and list of offers. Read more: <a href="../../tutorials/jak-sprawdzic-oplaty-nn9DOL5PASX#data-naliczenia-kolejnej-oplaty" target="_blank">PL</a> / <a href="../../tutorials/how-to-check-the-fees-3An6Wame3Um#check-when-a-fee-is-charged" target="_blank">EN</a>.


    HTTP: ``GET /pricing/offer-quotes``
    """
    params = {
        "offer.id": offer_id,
    }
    response = get_client().request_json(
        "GET",
        f"/pricing/offer-quotes",
        params=params,
    )
    return cast(dict[str, Any], response)
