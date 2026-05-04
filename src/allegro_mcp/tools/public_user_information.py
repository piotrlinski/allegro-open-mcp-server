# ruff: noqa
"""Generated MCP tools — DO NOT EDIT.

Run ``make gen-tools`` to regenerate from the cached OpenAPI spec.
Tag: Public user information
"""

from __future__ import annotations

from typing import Any, cast

from ..errors import ErrorResponse
from ._decorators import requires_writes_enabled
from ._runtime import allegro_call, get_client, mcp


@mcp.tool
@allegro_call
def get_user_summary_using_get(*, userId: str) -> dict[str, Any] | ErrorResponse:
    """Get any user's ratings summary

    Use this resource to receive feedback statistics. Read more: <a href="../../news/nowe-zasoby-ktorymi-pobierzesz-informacje-o-ocenach-ZM9L1WPBbUb" target="_blank">PL</a> / <a href="../../news/new-resources-to-download-sales-feedback-d2VYERBMRiz" target="_blank">EN</a>.


    HTTP: ``GET /users/{userId}/ratings-summary``
    """
    params: dict[str, Any] = {}
    response = get_client().request_json(
        "GET",
        f"/users/{userId}/ratings-summary",
        params=params,
    )
    return cast(dict[str, Any], response)
