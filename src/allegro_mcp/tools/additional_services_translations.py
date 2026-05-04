# ruff: noqa
"""Generated MCP tools — DO NOT EDIT.

Run ``make gen-tools`` to regenerate from the cached OpenAPI spec.
Tag: Additional services translations
"""

from __future__ import annotations

from typing import Any, cast

from ..errors import ErrorResponse
from ._decorators import requires_writes_enabled
from ._runtime import allegro_call, get_client, mcp


@mcp.tool
@allegro_call
def get_additional_service_group_translations(
    *, groupId: str, language: str | None = None
) -> dict[str, Any] | ErrorResponse:
    """Get translations for specified group

    Use this resource to get translations for additional service group. Read more: <a href="../../tutorials/jak-zarzadzac-ofertami-7GzB2L37ase#tlumaczenia-uslug-dodatkowych" target="_blank">PL</a> / <a href="../../tutorials/how-to-process-list-of-offers-m09BKA5v8H3#additional-services-translations" target="_blank">EN</a>.


    HTTP: ``GET /sale/offer-additional-services/groups/{groupId}/translations``
    """
    params = {
        "language": language,
    }
    response = get_client().request_json(
        "GET",
        f"/sale/offer-additional-services/groups/{groupId}/translations",
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
@requires_writes_enabled
def update_additional_service_group_translation(
    *, groupId: str, language: str, body: dict[str, Any] | None = None
) -> dict[str, Any] | ErrorResponse:
    """Create/Update translations for specified group and language

    Use this resource to create/update translation for additional service group and specified language. It is allowed to provide an incomplete list of services that belong to the group. Read more: <a href="../../tutorials/jak-zarzadzac-ofertami-7GzB2L37ase#tlumaczenia-uslug-dodatkowych" target="_blank">PL</a> / <a href="../../tutorials/how-to-process-list-of-offers-m09BKA5v8H3#additional-services-translations" target="_blank">EN</a>.


    HTTP: ``PATCH /sale/offer-additional-services/groups/{groupId}/translations/{language}``
    """
    params: dict[str, Any] = {}
    response = get_client().request_json(
        "PATCH",
        f"/sale/offer-additional-services/groups/{groupId}/translations/{language}",
        json=body,
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
@requires_writes_enabled
def delete_additional_service_group_translation(
    *, groupId: str, language: str
) -> dict[str, Any] | ErrorResponse:
    """Delete a translation for a specified group and language

    Use this resource to delete the translation for specified additional service group and language. Read more: <a href="../../tutorials/jak-zarzadzac-ofertami-7GzB2L37ase#tlumaczenia-uslug-dodatkowych" target="_blank">PL</a> / <a href="../../tutorials/how-to-process-list-of-offers-m09BKA5v8H3#additional-services-translations" target="_blank">EN</a>.


    HTTP: ``DELETE /sale/offer-additional-services/groups/{groupId}/translations/{language}``
    """
    params: dict[str, Any] = {}
    response = get_client().request_json(
        "DELETE",
        f"/sale/offer-additional-services/groups/{groupId}/translations/{language}",
        params=params,
    )
    return cast(dict[str, Any], response)
