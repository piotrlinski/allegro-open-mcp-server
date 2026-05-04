# ruff: noqa
"""Generated MCP tools — DO NOT EDIT.

Run ``make gen-tools`` to regenerate from the cached OpenAPI spec.
Tag: Fulfillment Returns
"""

from __future__ import annotations

from typing import Any, cast

from ..errors import ErrorResponse
from ._decorators import requires_writes_enabled
from ._runtime import allegro_call, get_client, mcp


@mcp.tool
@allegro_call
def get_refund_dispositions_report(
    *,
    createdAt_gte: str | None = None,
    createdAt_lte: str | None = None,
    limit: int | None = None,
    offset: int | None = None,
) -> dict[str, Any] | ErrorResponse:
    """Get refund dispositions report

    Use this resource to get refund dispositions for returns handled in One Fulfillment. The response contains data from the last 90 days only. The response contains both buyer returns and operational returns. When there is no matching disposition, the `report` array is empty. Read more: <a href="../../tutorials/one-fulfillment-by-allegro-0ADwgOLqWSw#jak-pobrac-raport-dyspozycji-zwrotu-srodkow" target="_blank">PL</a> / <a href="../../tutorials/one-fulfillment-by-allegro-4R9dXyMPlc9#how-to-retrieve-the-refund-disposition-report" target="_blank">EN</a>.


    HTTP: ``GET /fulfillment/returns/refund-dispositions``
    """
    params = {
        "createdAt.gte": createdAt_gte,
        "createdAt.lte": createdAt_lte,
        "limit": limit,
        "offset": offset,
    }
    response = get_client().request_json(
        "GET",
        f"/fulfillment/returns/refund-dispositions",
        params=params,
    )
    return cast(dict[str, Any], response)
