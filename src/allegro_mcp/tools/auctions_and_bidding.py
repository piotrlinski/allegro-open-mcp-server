# ruff: noqa
"""Generated MCP tools — DO NOT EDIT.

Run ``make gen-tools`` to regenerate from the cached OpenAPI spec.
Tag: Auctions and Bidding
"""

from __future__ import annotations

from typing import Any, cast

from ..errors import ErrorResponse
from ._decorators import requires_writes_enabled
from ._runtime import allegro_call, get_client, mcp


@mcp.tool
@allegro_call
@requires_writes_enabled
def place_bid(
    *, offerId: str, body: dict[str, Any] | None = None
) -> dict[str, Any] | ErrorResponse:
    """Place a bid in an auction

    Use this resource to place a bid in an auction. Read more: <a href="../../news/nowe-zasoby-zloz-oferte-kupna-w-licytacji-q018m02vDT1" target="_blank">PL</a> / <a href="../../news/new-resources-place-a-bid-in-an-auction-rjWwEj1e7sG" target="_blank">EN</a>.


    HTTP: ``PUT /bidding/offers/{offerId}/bid``
    """
    params: dict[str, Any] = {}
    response = get_client().request_json(
        "PUT",
        f"/bidding/offers/{offerId}/bid",
        json=body,
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
def get_bid(*, offerId: str) -> dict[str, Any] | ErrorResponse:
    """Get current user's bid information

    Use this resource to retrieve current user's bid information. Read more: <a href="../../news/nowe-zasoby-zloz-oferte-kupna-w-licytacji-q018m02vDT1" target="_blank">PL</a> / <a href="../../news/new-resources-place-a-bid-in-an-auction-rjWwEj1e7sG" target="_blank">EN</a>.


    HTTP: ``GET /bidding/offers/{offerId}/bid``
    """
    params: dict[str, Any] = {}
    response = get_client().request_json(
        "GET",
        f"/bidding/offers/{offerId}/bid",
        params=params,
    )
    return cast(dict[str, Any], response)
