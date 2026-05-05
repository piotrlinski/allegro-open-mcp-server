# ruff: noqa
"""Generated MCP tools — DO NOT EDIT.

Run ``make gen-tools`` to regenerate from the cached OpenAPI spec.
Tag: Points of service
"""

from __future__ import annotations

from typing import Any, cast

from ..errors import ErrorResponse
from ._decorators import requires_writes_enabled
from ._runtime import allegro_call, get_client, mcp


@mcp.tool
@allegro_call
@requires_writes_enabled
def create_pos(*, body: dict[str, Any] | None = None) -> dict[str, Any] | ErrorResponse:
    """Create a point of service

    Use this resource to create a point of service. Read more: <a href="../../news/punkty-odbioru-osobistego-8dmlj8qk7ik" target="_blank">PL</a> / <a href="../../news/points-of-service-Rdoz09ZE7sW" target="_blank">EN</a>.


    HTTP: ``POST /points-of-service``
    """
    params: dict[str, Any] = {}
    response = get_client().request_json(
        "POST",
        f"/points-of-service",
        json=body,
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
def get_pos_list(
    *, seller_id: str | None = None, countryCode: str | None = None
) -> dict[str, Any] | ErrorResponse:
    """Get the user's points of service

    Use this resource to get a list of points of service by seller ID. Read more: <a href="../../news/punkty-odbioru-osobistego-8dmlj8qk7ik" target="_blank">PL</a> / <a href="../../news/points-of-service-Rdoz09ZE7sW" target="_blank">EN</a>.


    HTTP: ``GET /points-of-service``
    """
    params = {
        "seller.id": seller_id,
        "countryCode": countryCode,
    }
    response = get_client().request_json(
        "GET",
        f"/points-of-service",
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
def get_pos_data(*, id: str) -> dict[str, Any] | ErrorResponse:
    """Get the details of a point of service

    Use this resource to get a details of a point of service for a given ID. Read more: <a href="../../news/punkty-odbioru-osobistego-8dmlj8qk7ik" target="_blank">PL</a> / <a href="../../news/points-of-service-Rdoz09ZE7sW" target="_blank">EN</a>.


    HTTP: ``GET /points-of-service/{id}``
    """
    params: dict[str, Any] = {}
    response = get_client().request_json(
        "GET",
        f"/points-of-service/{id}",
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
@requires_writes_enabled
def modify_pos(*, id: str, body: dict[str, Any] | None = None) -> dict[str, Any] | ErrorResponse:
    """Modify a point of service

    Use this resource to modify a point of service. Read more: <a href="../../news/punkty-odbioru-osobistego-8dmlj8qk7ik" target="_blank">PL</a> / <a href="../../news/points-of-service-Rdoz09ZE7sW" target="_blank">EN</a>.


    HTTP: ``PUT /points-of-service/{id}``
    """
    params: dict[str, Any] = {}
    response = get_client().request_json(
        "PUT",
        f"/points-of-service/{id}",
        json=body,
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
@requires_writes_enabled
def delete_pos(*, id: str) -> dict[str, Any] | ErrorResponse:
    """Delete a point of service

    Use this resource to delete a point of service. Read more: <a href="../../news/punkty-odbioru-osobistego-8dmlj8qk7ik" target="_blank">PL</a> / <a href="../../news/points-of-service-Rdoz09ZE7sW" target="_blank">EN</a>.


    HTTP: ``DELETE /points-of-service/{id}``
    """
    params: dict[str, Any] = {}
    response = get_client().request_json(
        "DELETE",
        f"/points-of-service/{id}",
        params=params,
    )
    return cast(dict[str, Any], response)
