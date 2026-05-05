# ruff: noqa
"""Generated MCP tools — DO NOT EDIT.

Run ``make gen-tools`` to regenerate from the cached OpenAPI spec.
Tag: Contacts
"""

from __future__ import annotations

from typing import Any, cast

from ..errors import ErrorResponse
from ._decorators import requires_writes_enabled
from ._runtime import allegro_call, get_client, mcp


@mcp.tool
@allegro_call
@requires_writes_enabled
def create_contact(*, body: dict[str, Any] | None = None) -> dict[str, Any] | ErrorResponse:
    """Create a new contact

    Use this resource to create a new contact. Read more: <a href="../../tutorials/jak-zarzadzac-kontem-danymi-uzytkownika-ZM9YAKgPgi2#jak-utworzyc-nowy-kontakt" target="_blank">PL</a> / <a href="../../tutorials/account-and-user-data-management-jn9vBjqjnsw#how-to-create-new-contact" target="_blank">EN</a>.


    HTTP: ``POST /sale/offer-contacts``
    """
    params: dict[str, Any] = {}
    response = get_client().request_json(
        "POST",
        f"/sale/offer-contacts",
        json=body,
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
def get_list_of_contacts() -> dict[str, Any] | ErrorResponse:
    """Get the user's contacts

    Use this resource to get details of many contacts. Read more: <a href="../../tutorials/jak-zarzadzac-kontem-danymi-uzytkownika-ZM9YAKgPgi2#jak-pobrac-liste-kontaktow" target="_blank">PL</a> / <a href="../../tutorials/account-and-user-data-management-jn9vBjqjnsw#how-to-retrieve-a-list-of-contacts" target="_blank">EN</a>.


    HTTP: ``GET /sale/offer-contacts``
    """
    params: dict[str, Any] = {}
    response = get_client().request_json(
        "GET",
        f"/sale/offer-contacts",
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
def get_contact(*, id: str) -> dict[str, Any] | ErrorResponse:
    """Get contact details

    Use this resource to get contact details. Read more: <a href="../../tutorials/jak-zarzadzac-kontem-danymi-uzytkownika-ZM9YAKgPgi2#jak-pobrac-szczegoly-danego-kontaktu" target="_blank">PL</a> / <a href="../../tutorials/account-and-user-data-management-jn9vBjqjnsw#how-to-retrieve-contact-details" target="_blank">EN</a>.


    HTTP: ``GET /sale/offer-contacts/{id}``
    """
    params: dict[str, Any] = {}
    response = get_client().request_json(
        "GET",
        f"/sale/offer-contacts/{id}",
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
@requires_writes_enabled
def modify_contact(
    *, id: str, body: dict[str, Any] | None = None
) -> dict[str, Any] | ErrorResponse:
    """Modify contact details

    Use this resource to modify contact details. Read more: <a href="../../tutorials/jak-zarzadzac-kontem-danymi-uzytkownika-ZM9YAKgPgi2#jak-zmienic-dane-kontaktu" target="_blank">PL</a> / <a href="../../tutorials/account-and-user-data-management-jn9vBjqjnsw#how-to-change-contact-data" target="_blank">EN</a>.


    HTTP: ``PUT /sale/offer-contacts/{id}``
    """
    params: dict[str, Any] = {}
    response = get_client().request_json(
        "PUT",
        f"/sale/offer-contacts/{id}",
        json=body,
        params=params,
    )
    return cast(dict[str, Any], response)
