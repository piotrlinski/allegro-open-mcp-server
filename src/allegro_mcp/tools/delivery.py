# ruff: noqa
"""Generated MCP tools — DO NOT EDIT.

Run ``make gen-tools`` to regenerate from the cached OpenAPI spec.
Tag: Delivery
"""

from __future__ import annotations

from typing import Any, cast

from ..errors import ErrorResponse
from ._decorators import requires_writes_enabled
from ._runtime import allegro_call, get_client, mcp


@mcp.tool
@allegro_call
def get_list_of_shipping_ratest(
    *, marketplace: str | None = None
) -> dict[str, Any] | ErrorResponse:
    """Get the user's shipping rates

    Use this resource to get a list of seller's shipping rates. Read more: <a href="../../tutorials/jak-zarzadzac-kontem-danymi-uzytkownika-ZM9YAKgPgi2#jak-pobrac-cennik-dostaw" target="_blank">PL</a> / <a href="../../tutorials/account-and-user-data-management-jn9vBjqjnsw#how-to-retrieve-shipping-rates" target="_blank">EN</a>.


    HTTP: ``GET /sale/shipping-rates``
    """
    params = {
        "marketplace": marketplace,
    }
    response = get_client().request_json(
        "GET",
        f"/sale/shipping-rates",
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
@requires_writes_enabled
def create_shipping_rates_set(
    *, body: dict[str, Any] | None = None
) -> dict[str, Any] | ErrorResponse:
    """Create a new shipping rates set

    Use this resource to create a new seller's shipping rates set. Read more: <a href="../../tutorials/jak-zarzadzac-kontem-danymi-uzytkownika-ZM9YAKgPgi2#jak-dodac-cennik-dostaw" target="_blank">PL</a> / <a href="../../tutorials/account-and-user-data-management-jn9vBjqjnsw#how-to-add-shipping-rates" target="_blank">EN</a>.


    HTTP: ``POST /sale/shipping-rates``
    """
    params: dict[str, Any] = {}
    response = get_client().request_json(
        "POST",
        f"/sale/shipping-rates",
        json=body,
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
def get_shipping_rates_set(*, id: str) -> dict[str, Any] | ErrorResponse:
    """Get the details of a shipping rates set

    Use this resource to get details of the given shipping rates set. Read more: <a href="../../tutorials/jak-zarzadzac-kontem-danymi-uzytkownika-ZM9YAKgPgi2#jak-pobrac-cennik-dostaw" target="_blank">PL</a> / <a href="../../tutorials/account-and-user-data-management-jn9vBjqjnsw#how-to-retrieve-shipping-rates" target="_blank">EN</a>.


    HTTP: ``GET /sale/shipping-rates/{id}``
    """
    params: dict[str, Any] = {}
    response = get_client().request_json(
        "GET",
        f"/sale/shipping-rates/{id}",
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
@requires_writes_enabled
def modify_shipping_rates_set(
    *, id: str, body: dict[str, Any] | None = None
) -> dict[str, Any] | ErrorResponse:
    """Edit a user's shipping rates set

    Use this resource to edit a new seller's shipping rates set. Read more: <a href="../../tutorials/jak-zarzadzac-kontem-danymi-uzytkownika-ZM9YAKgPgi2#jak-edytowac-cennik-dostaw" target="_blank">PL</a> / <a href="../../tutorials/account-and-user-data-management-jn9vBjqjnsw#how-to-modify-shipping-rates" target="_blank">EN</a>.


    HTTP: ``PUT /sale/shipping-rates/{id}``
    """
    params: dict[str, Any] = {}
    response = get_client().request_json(
        "PUT",
        f"/sale/shipping-rates/{id}",
        json=body,
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
def get_sale_delivery_settings(
    *, marketplace_id: str | None = None
) -> dict[str, Any] | ErrorResponse:
    """Get the user's delivery settings

    Use this resource to get the delivery settings declared by the seller. Read more: <a href="../../tutorials/jak-zarzadzac-kontem-danymi-uzytkownika-ZM9YAKgPgi2#jak-pobrac-ustawienia-dostawy" target="_blank">PL</a> / <a href="../../tutorials/account-and-user-data-management-jn9vBjqjnsw#how-to-get-delivery-settings" target="_blank">EN</a>.


    HTTP: ``GET /sale/delivery-settings``
    """
    params = {
        "marketplace.id": marketplace_id,
    }
    response = get_client().request_json(
        "GET",
        f"/sale/delivery-settings",
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
@requires_writes_enabled
def put_sale_delivery_settings(
    *, body: dict[str, Any] | None = None
) -> dict[str, Any] | ErrorResponse:
    """Modify the user's delivery settings

    Use this resource to modify the delivery settings declared by the seller. Read more: <a href="../../tutorials/jak-zarzadzac-kontem-danymi-uzytkownika-ZM9YAKgPgi2#jak-edytowac-ustawienia-dostawy" target="_blank">PL</a> / <a href="../../tutorials/account-and-user-data-management-jn9vBjqjnsw#how-to-edit-delivery-settings" target="_blank">EN</a>.


    HTTP: ``PUT /sale/delivery-settings``
    """
    params: dict[str, Any] = {}
    response = get_client().request_json(
        "PUT",
        f"/sale/delivery-settings",
        json=body,
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
def get_list_of_delivery_methods(
    *, marketplace: str | None = None
) -> dict[str, Any] | ErrorResponse:
    """Get the list of delivery methods

    Use this resource to get a list of all delivery methods currently available on the platform, as well as those that have already been discontinued. Read more: <a href="../../tutorials/jak-zarzadzac-kontem-danymi-uzytkownika-ZM9YAKgPgi2#jak-dodac-cennik-dostaw" target="_blank">PL</a> / <a href="../../tutorials/account-and-user-data-management-jn9vBjqjnsw#how-to-add-shipping-rates" target="_blank">EN</a>.


    HTTP: ``GET /sale/delivery-methods``
    """
    params = {
        "marketplace": marketplace,
    }
    response = get_client().request_json(
        "GET",
        f"/sale/delivery-methods",
        params=params,
    )
    return cast(dict[str, Any], response)
