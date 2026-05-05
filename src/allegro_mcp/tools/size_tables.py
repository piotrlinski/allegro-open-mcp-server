# ruff: noqa
"""Generated MCP tools — DO NOT EDIT.

Run ``make gen-tools`` to regenerate from the cached OpenAPI spec.
Tag: Size tables
"""

from __future__ import annotations

from typing import Any, cast

from ..errors import ErrorResponse
from ._decorators import requires_writes_enabled
from ._runtime import allegro_call, get_client, mcp


@mcp.tool
@allegro_call
def get_table(*, tableId: str) -> dict[str, Any] | ErrorResponse:
    """Get a size table

    Use this resource to get selected size table. Read more: <a href="../../news/tabele-rozmiarow-w-rest-api-LRV05q2dGtV" target="_blank">PL</a> / <a href="../../news/size-tables-in-rest-api-D7KP4DE1BH3" target="_blank">EN</a>.


    HTTP: ``GET /sale/size-tables/{tableId}``
    """
    params: dict[str, Any] = {}
    response = get_client().request_json(
        "GET",
        f"/sale/size-tables/{tableId}",
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
@requires_writes_enabled
def modify_table(
    *, tableId: str, body: dict[str, Any] | None = None
) -> dict[str, Any] | ErrorResponse:
    """Update a size table

    Use this resource to update selected size table. Read more: <a href="../../news/tabele-rozmiarow-zmieniamy-istniejacy-zasob-i-dodajemy-nowe-zasoby-do-ich-obslugi-k1nyd21A4fP" target="_blank">PL</a> / <a href="../../news/size-tables-we-change-the-existing-resource-and-add-new-resources-to-handle-them-jn91bynlbC9" target="_blank">EN</a>.


    HTTP: ``PUT /sale/size-tables/{tableId}``
    """
    params: dict[str, Any] = {}
    response = get_client().request_json(
        "PUT",
        f"/sale/size-tables/{tableId}",
        json=body,
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
def get_tables() -> dict[str, Any] | ErrorResponse:
    """Get the user's size tables

    Use this resource to get all size tables assigned to a seller account. Read more: <a href="../../news/tabele-rozmiarow-w-rest-api-LRV05q2dGtV" target="_blank">PL</a> / <a href="../../news/size-tables-in-rest-api-D7KP4DE1BH3" target="_blank">EN</a>.


    HTTP: ``GET /sale/size-tables``
    """
    params: dict[str, Any] = {}
    response = get_client().request_json(
        "GET",
        f"/sale/size-tables",
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
@requires_writes_enabled
def create_table(*, body: dict[str, Any] | None = None) -> dict[str, Any] | ErrorResponse:
    """Create a size table

    Use this resource to create size table. Read more: <a href="../../news/tabele-rozmiarow-zmieniamy-istniejacy-zasob-i-dodajemy-nowe-zasoby-do-ich-obslugi-k1nyd21A4fP" target="_blank">PL</a> / <a href="../../news/size-tables-we-change-the-existing-resource-and-add-new-resources-to-handle-them-jn91bynlbC9" target="_blank">EN</a>.


    HTTP: ``POST /sale/size-tables``
    """
    params: dict[str, Any] = {}
    response = get_client().request_json(
        "POST",
        f"/sale/size-tables",
        json=body,
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
def get_tables_templates() -> dict[str, Any] | ErrorResponse:
    """Get the size tables templates

    Use this resource to get all size tables templates. Read more: <a href="../../news/tabele-rozmiarow-zmieniamy-istniejacy-zasob-i-dodajemy-nowe-zasoby-do-ich-obslugi-k1nyd21A4fP" target="_blank">PL</a> / <a href="../../news/size-tables-we-change-the-existing-resource-and-add-new-resources-to-handle-them-jn91bynlbC9" target="_blank">EN</a>.


    HTTP: ``GET /sale/size-tables-templates``
    """
    params: dict[str, Any] = {}
    response = get_client().request_json(
        "GET",
        f"/sale/size-tables-templates",
        params=params,
    )
    return cast(dict[str, Any], response)
