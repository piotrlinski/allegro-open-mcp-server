# ruff: noqa
"""Generated MCP tools — DO NOT EDIT.

Run ``make gen-tools`` to regenerate from the cached OpenAPI spec.
Tag: Additional services
"""

from __future__ import annotations

from typing import Any, cast

from ..errors import ErrorResponse
from ._decorators import requires_writes_enabled
from ._runtime import allegro_call, get_client, mcp


@mcp.tool
@allegro_call
@requires_writes_enabled
def create_additional_services_group_using_post(
    *, body: dict[str, Any] | None = None
) -> dict[str, Any] | ErrorResponse:
    """Create additional services group

    Use this resource to create a group of additional services. Read more: <a href="../../tutorials/jak-zarzadzac-ofertami-7GzB2L37ase#jak-dodac-nowa-grupe-uslug-dodatkowych" target="_blank">PL</a> / <a href="../../tutorials/how-to-process-list-of-offers-m09BKA5v8H3#how-to-add-a-new-additional-service-group" target="_blank">EN</a>.


    HTTP: ``POST /sale/offer-additional-services/groups``
    """
    params: dict[str, Any] = {}
    response = get_client().request_json(
        "POST",
        f"/sale/offer-additional-services/groups",
        json=body,
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
def get_list_of_additional_services_groups_using_get(
    *, offset: int | None = None, limit: int | None = None
) -> dict[str, Any] | ErrorResponse:
    """Get the user's additional services groups

    Use this resource to retrieve a list of groups with additional services available to a given user which you may assign to offers. Read more: <a href="../../tutorials/jak-zarzadzac-ofertami-7GzB2L37ase#jak-pobrac-liste-grup-uslug-dodatkowych-na-koncie" target="_blank">PL</a> / <a href="../../tutorials/how-to-process-list-of-offers-m09BKA5v8H3#how-to-retrieve-a-list-of-additional-services-groups-for-the-account" target="_blank">EN</a>.


    HTTP: ``GET /sale/offer-additional-services/groups``
    """
    params = {
        "offset": offset,
        "limit": limit,
    }
    response = get_client().request_json(
        "GET",
        f"/sale/offer-additional-services/groups",
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
def get_list_of_additional_services_definitions_categories_using_get() -> (
    dict[str, Any] | ErrorResponse
):
    """Get the additional services definitions by categories

    Use this resource to get additional services definitions, grouped by additional services categories, available on given marketplace. Read more: <a href="../../tutorials/jak-zarzadzac-ofertami-7GzB2L37ase#jak-pobrac-liste-dostepnych-uslug-dodatkowych" target="_blank">PL</a> / <a href="../../tutorials/how-to-process-list-of-offers-m09BKA5v8H3#how-to-retrieve-a-list-of-available-additional-services" target="_blank">EN</a>.


    HTTP: ``GET /sale/offer-additional-services/categories``
    """
    params: dict[str, Any] = {}
    response = get_client().request_json(
        "GET",
        f"/sale/offer-additional-services/categories",
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
def get_additional_services_group_using_get(*, groupId: str) -> dict[str, Any] | ErrorResponse:
    """Get the details of an additional services group

    Use this resource to get additional services group for a given ID. Read more: <a href="../../tutorials/jak-zarzadzac-ofertami-7GzB2L37ase#jak-pobrac-wybrana-grupe-uslug-dodatkowych" target="_blank">PL</a> / <a href="../../tutorials/how-to-process-list-of-offers-m09BKA5v8H3#how-to-retrieve-a-group-of-additional-services-for-a-given-id" target="_blank">EN</a>.


    HTTP: ``GET /sale/offer-additional-services/groups/{groupId}``
    """
    params: dict[str, Any] = {}
    response = get_client().request_json(
        "GET",
        f"/sale/offer-additional-services/groups/{groupId}",
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
@requires_writes_enabled
def modify_additional_services_group_using_put(
    *, groupId: str, body: dict[str, Any] | None = None
) -> dict[str, Any] | ErrorResponse:
    """Modify an additional services group

    Use this resource to modify existing additional service group. Read more: <a href="../../tutorials/jak-zarzadzac-ofertami-7GzB2L37ase#jak-zaktualizowac-grupe-uslug-dodatkowych" target="_blank">PL</a> / <a href="../../tutorials/how-to-process-list-of-offers-m09BKA5v8H3#how-to-update-additional-service-group" target="_blank">EN</a>.


    HTTP: ``PUT /sale/offer-additional-services/groups/{groupId}``
    """
    params: dict[str, Any] = {}
    response = get_client().request_json(
        "PUT",
        f"/sale/offer-additional-services/groups/{groupId}",
        json=body,
        params=params,
    )
    return cast(dict[str, Any], response)
