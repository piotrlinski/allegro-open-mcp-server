# ruff: noqa
"""Generated MCP tools — DO NOT EDIT.

Run ``make gen-tools`` to regenerate from the cached OpenAPI spec.
Tag: Conversions
"""

from __future__ import annotations

from typing import Any, cast

from ..errors import ErrorResponse
from ._decorators import requires_writes_enabled
from ._runtime import allegro_call, get_client, mcp


@mcp.tool
@allegro_call
def get_cps_conversions(
    *,
    orderCreatedAt_gte: str | None = None,
    orderCreatedAt_lte: str | None = None,
    lastModifiedAt_gte: str | None = None,
    lastModifiedAt_lte: str | None = None,
    status: str | None = None,
    offset: int | None = None,
    limit: int | None = None,
    includePublisherUrlParameters: str | None = None,
) -> dict[str, Any] | ErrorResponse:
    """[BETA] List CPS conversions

    Use this resource to find your CPS (Cost Per Sale) conversions for specific filters. The response contains a list of CPS conversions that correspond with the specified parameters. Read more: <a href="../../tutorials/afiliacja-0A1bPnwVwUq#jak-pobrac-informacje-o-konwersji-cps" target="_blank">PL</a> / <a href="../../tutorials/affiliation-8do60yLKPIq#how-to-retrieve-cps-conversion-information" target="_blank">EN</a>.


    HTTP: ``GET /affiliate/conversions/cps``
    """
    params = {
        "orderCreatedAt.gte": orderCreatedAt_gte,
        "orderCreatedAt.lte": orderCreatedAt_lte,
        "lastModifiedAt.gte": lastModifiedAt_gte,
        "lastModifiedAt.lte": lastModifiedAt_lte,
        "status": status,
        "offset": offset,
        "limit": limit,
        "includePublisherUrlParameters": includePublisherUrlParameters,
    }
    response = get_client().request_json(
        "GET",
        f"/affiliate/conversions/cps",
        params=params,
    )
    return cast(dict[str, Any], response)
