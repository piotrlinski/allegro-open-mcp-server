# ruff: noqa
"""Generated MCP tools — DO NOT EDIT.

Run ``make gen-tools`` to regenerate from the cached OpenAPI spec.
Tag: Offer rating
"""

from __future__ import annotations

from typing import Any, cast

from ..errors import ErrorResponse
from ._decorators import requires_writes_enabled
from ._runtime import allegro_call, get_client, mcp


@mcp.tool
@allegro_call
def offer_rating_get(*, offerId: str) -> dict[str, Any] | ErrorResponse:
    """Get offer rating

    Use this resource to get offer rating. Read more: <a href="../../news/nowy-zasob-do-pobrania-oceny-produktu-q018mmPe0H7" target="_blank">PL</a> / <a href="../../news/new-resource-to-retrieve-product-rating-q018mmPrWUX" target="_blank">EN</a>.


    HTTP: ``GET /sale/offers/{offerId}/rating``
    """
    params: dict[str, Any] = {}
    response = get_client().request_json(
        "GET",
        f"/sale/offers/{offerId}/rating",
        params=params,
    )
    return cast(dict[str, Any], response)
