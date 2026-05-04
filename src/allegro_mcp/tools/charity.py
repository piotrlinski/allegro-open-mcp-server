# ruff: noqa
"""Generated MCP tools — DO NOT EDIT.

Run ``make gen-tools`` to regenerate from the cached OpenAPI spec.
Tag: Charity
"""

from __future__ import annotations

from typing import Any, cast

from ..errors import ErrorResponse
from ._decorators import requires_writes_enabled
from ._runtime import allegro_call, get_client, mcp


@mcp.tool
@allegro_call
def search_fundraising_campaigns(
    *, limit: int | None = None, phrase: str | None = None
) -> dict[str, Any] | ErrorResponse:
    """Search fundraising campaigns

    Use this resource to search fundraising campaigns. Read more: <a href="../../news/wystaw-oferte-charytatywna-na-allegro-MR87PBxZySY" target="_blank">PL</a> / <a href="../../news/list-a-charity-offer-on-allegro-LRV0572GOhr" target="_blank">EN</a>.


    HTTP: ``GET /charity/fundraising-campaigns``
    """
    params = {
        "limit": limit,
        "phrase": phrase,
    }
    response = get_client().request_json(
        "GET",
        f"/charity/fundraising-campaigns",
        params=params,
    )
    return cast(dict[str, Any], response)
