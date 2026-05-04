# ruff: noqa
"""Generated MCP tools — DO NOT EDIT.

Run ``make gen-tools`` to regenerate from the cached OpenAPI spec.
Tag: Information about marketplaces
"""

from __future__ import annotations

from typing import Any, cast

from ..errors import ErrorResponse
from ._decorators import requires_writes_enabled
from ._runtime import allegro_call, get_client, mcp


@mcp.tool
@allegro_call
def marketplaces_get() -> dict[str, Any] | ErrorResponse:
    """Get details for all marketplaces in allegro

    Use this resource to get information about all the marketplaces on the platform. Read more: <a href="../../tutorials/wystawianie-i-zarzadzanie-oferta-w-serwisach-zagranicznych-wwzjP4M8gTZ#serwis-bazowy-uzytkownika-oraz-lista-dostepnych-serwisow" target="_blank">PL</a> / <a href="../../tutorials/listing-and-managing-offers-on-foreign-marketplaces-7GndGjeAATn#user-s-base-marketplace-and-list-of-available-marketplaces" target="_blank">EN</a>.


    HTTP: ``GET /marketplaces``
    """
    params: dict[str, Any] = {}
    response = get_client().request_json(
        "GET",
        f"/marketplaces",
        params=params,
    )
    return cast(dict[str, Any], response)
