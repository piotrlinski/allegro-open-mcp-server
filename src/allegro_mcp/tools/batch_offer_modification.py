# ruff: noqa
"""Generated MCP tools — DO NOT EDIT.

Run ``make gen-tools`` to regenerate from the cached OpenAPI spec.
Tag: Batch offer modification
"""

from __future__ import annotations

from typing import Any, cast

from ..errors import ErrorResponse
from ._decorators import requires_writes_enabled
from ._runtime import allegro_call, get_client, mcp


@mcp.tool
@allegro_call
@requires_writes_enabled
def modification_command(
    *, commandId: str, body: dict[str, Any] | None = None
) -> dict[str, Any] | ErrorResponse:
    """Batch offer modification

    Use this resource to modify multiple offers at once. Read more: <a href="../../tutorials/jak-zarzadzac-ofertami-7GzB2L37ase#edycja-wielu-ofert-jednoczesnie" target="_blank">PL</a> / <a href="../../tutorials/how-to-process-list-of-offers-m09BKA5v8H3#editing-many-offers" target="_blank">EN</a>. This resource is rate limited to 250 000 offer changes per hour or 9000 offer changes per minute - limit applies to a single user of the application.


    HTTP: ``PUT /sale/offer-modification-commands/{commandId}``
    """
    params: dict[str, Any] = {}
    response = get_client().request_json(
        "PUT",
        f"/sale/offer-modification-commands/{commandId}",
        json=body,
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
def get_general_report(*, commandId: str) -> dict[str, Any] | ErrorResponse:
    """Modification command summary

    Use this resource to find out how many offers were edited within one {commandId}. You will receive a summary with a number of successfully edited offers. Read more: <a href="../../tutorials/jak-zarzadzac-ofertami-7GzB2L37ase#edycja-wielu-ofert-jednoczesnie" target="_blank">PL</a> / <a href="../../tutorials/how-to-process-list-of-offers-m09BKA5v8H3#editing-many-offers" target="_blank">EN</a>. This resource is rate limited to retrieving information about 270 000 offer changes per minute.


    HTTP: ``GET /sale/offer-modification-commands/{commandId}``
    """
    params: dict[str, Any] = {}
    response = get_client().request_json(
        "GET",
        f"/sale/offer-modification-commands/{commandId}",
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
def get_tasks(
    *, commandId: str, limit: int | None = None, offset: int | None = None
) -> dict[str, Any] | ErrorResponse:
    """Modification command detailed report

    Use this resource to retrieve a detailed summary of changes introduced within one {commandId} (defaults: limit = 100, offset = 0). Read more: <a href="../../tutorials/jak-zarzadzac-ofertami-7GzB2L37ase#edycja-wielu-ofert-jednoczesnie" target="_blank">PL</a> / <a href="../../tutorials/how-to-process-list-of-offers-m09BKA5v8H3#editing-many-offers" target="_blank">EN</a>. This resource is rate limited to retrieving information about 270 000 offer changes per minute.


    HTTP: ``GET /sale/offer-modification-commands/{commandId}/tasks``
    """
    params = {
        "limit": limit,
        "offset": offset,
    }
    response = get_client().request_json(
        "GET",
        f"/sale/offer-modification-commands/{commandId}/tasks",
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
@requires_writes_enabled
def price_modification_command(
    *, commandId: str, body: dict[str, Any] | None = None
) -> dict[str, Any] | ErrorResponse:
    """Batch offer price modification

    Change price of offers. Read more: <a href="../../tutorials/jak-zarzadzac-ofertami-7GzB2L37ase#cena" target="_blank">PL</a> / <a href="../../tutorials/how-to-process-list-of-offers-m09BKA5v8H3#price" target="_blank">EN</a>. This resource is rate limited to 150 000 offer changes per hour or 9000 offer changes per minute - limit applies to a single user of the application.


    HTTP: ``PUT /sale/offer-price-change-commands/{commandId}``
    """
    params: dict[str, Any] = {}
    response = get_client().request_json(
        "PUT",
        f"/sale/offer-price-change-commands/{commandId}",
        json=body,
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
def get_price_modification_command_status(*, commandId: str) -> dict[str, Any] | ErrorResponse:
    """Change price command summary

    Returns status and summary of particular command execution. Read more: <a href="../../tutorials/jak-zarzadzac-ofertami-7GzB2L37ase#cena" target="_blank">PL</a> / <a href="../../tutorials/how-to-process-list-of-offers-m09BKA5v8H3#price" target="_blank">EN</a>. This resource is rate limited to retrieving information about 270 000 offer changes per minute.


    HTTP: ``GET /sale/offer-price-change-commands/{commandId}``
    """
    params: dict[str, Any] = {}
    response = get_client().request_json(
        "GET",
        f"/sale/offer-price-change-commands/{commandId}",
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
def get_price_modification_command_tasks_statuses(
    *, commandId: str, limit: int | None = None, offset: int | None = None
) -> dict[str, Any] | ErrorResponse:
    """Change price command detailed report

    Defaults: limit = 100, offset = 0. Read more: <a href="../../tutorials/jak-zarzadzac-ofertami-7GzB2L37ase#cena" target="_blank">PL</a> / <a href="../../tutorials/how-to-process-list-of-offers-m09BKA5v8H3#price" target="_blank">EN</a>. This resource is rate limited to retrieving information about 270 000 offer changes per minute.


    HTTP: ``GET /sale/offer-price-change-commands/{commandId}/tasks``
    """
    params = {
        "limit": limit,
        "offset": offset,
    }
    response = get_client().request_json(
        "GET",
        f"/sale/offer-price-change-commands/{commandId}/tasks",
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
@requires_writes_enabled
def batch_offer_modification(
    *, body: dict[str, Any] | None = None
) -> dict[str, Any] | ErrorResponse:
    """Batch offer price and stock modification (beta)

    Bulk price and stock modification. Contrary to standard batch price or stock modification, it lets you modify both price and stock modification across multiple offers, or within the same offer but in a separate modification unit. <br> Change price and stock of offers. Read more: <a href="../../tutorials/jak-zarzadzac-ofertami-7GzB2L37ase#cena-i-liczba-przedmiotow" target="_blank">PL</a> / <a href="../../tutorials/how-to-process-list-of-offers-m09BKA5v8H3#price-and-stock" target="_blank">EN</a>. <br> This resource is rate limited to 150 000 offer changes per hour or 9000 offer changes per minute - limit applies to a single user of the application.


    HTTP: ``POST /sale/offer-bulk-modification-commands``
    """
    params: dict[str, Any] = {}
    response = get_client().request_json(
        "POST",
        f"/sale/offer-bulk-modification-commands",
        json=body,
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
def batch_offer_modification_command_status(*, commandId: str) -> dict[str, Any] | ErrorResponse:
    """Batch price and stock command summary (beta)

    Returns status and summary of particular command execution. Read more: <a href="../../tutorials/jak-zarzadzac-ofertami-7GzB2L37ase#cena-i-liczba-przedmiotow" target="_blank">PL</a> / <a href="../../tutorials/how-to-process-list-of-offers-m09BKA5v8H3#price-and-stock" target="_blank">EN</a>. This resource is rate limited to retrieving information about 270 000 offer changes per minute.


    HTTP: ``GET /sale/offer-bulk-modification-commands/{commandId}``
    """
    params: dict[str, Any] = {}
    response = get_client().request_json(
        "GET",
        f"/sale/offer-bulk-modification-commands/{commandId}",
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
def batch_offer_modification_command_task_statuses(
    *, commandId: str, limit: int | None = None, offset: int | None = None
) -> dict[str, Any] | ErrorResponse:
    """Batch price and stock command detailed report (beta)

    Defaults: limit = 100, offset = 0. Read more: <a href="../../tutorials/jak-zarzadzac-ofertami-7GzB2L37ase#cena-i-liczba-przedmiotow" target="_blank">PL</a> / <a href="../../tutorials/how-to-process-list-of-offers-m09BKA5v8H3#price-and-stock" target="_blank">EN</a>. This resource is rate limited to retrieving information about 270 000 offer changes per minute.


    HTTP: ``GET /sale/offer-bulk-modification-commands/{commandId}/tasks``
    """
    params = {
        "limit": limit,
        "offset": offset,
    }
    response = get_client().request_json(
        "GET",
        f"/sale/offer-bulk-modification-commands/{commandId}/tasks",
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
@requires_writes_enabled
def quantity_modification_command(
    *, commandId: str, body: dict[str, Any] | None = None
) -> dict[str, Any] | ErrorResponse:
    """Batch offer quantity modification

    Change quantity of multiple offers. Read more: <a href="../../tutorials/jak-zarzadzac-ofertami-7GzB2L37ase#liczba-przedmiotow" target="_blank">PL</a> / <a href="../../tutorials/how-to-process-list-of-offers-m09BKA5v8H3#quantity" target="_blank">EN</a>. This resource is rate limited to 250 000 offer changes per hour or 9000 offer changes per minute - limit applies to a single user of the application.


    HTTP: ``PUT /sale/offer-quantity-change-commands/{commandId}``
    """
    params: dict[str, Any] = {}
    response = get_client().request_json(
        "PUT",
        f"/sale/offer-quantity-change-commands/{commandId}",
        json=body,
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
def get_quantity_modification_command_status(*, commandId: str) -> dict[str, Any] | ErrorResponse:
    """Change quantity command summary

    Returns status and summary of the command. Read more: <a href="../../tutorials/jak-zarzadzac-ofertami-7GzB2L37ase#liczba-przedmiotow" target="_blank">PL</a> / <a href="../../tutorials/how-to-process-list-of-offers-m09BKA5v8H3#quantity" target="_blank">EN</a>. This resource is rate limited to retrieving information about 270 000 offer changes per minute.


    HTTP: ``GET /sale/offer-quantity-change-commands/{commandId}``
    """
    params: dict[str, Any] = {}
    response = get_client().request_json(
        "GET",
        f"/sale/offer-quantity-change-commands/{commandId}",
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
def get_quantity_modification_command_tasks_statuses(
    *, commandId: str, limit: int | None = None, offset: int | None = None
) -> dict[str, Any] | ErrorResponse:
    """Change quantity command detailed report

    Defaults: limit = 100, offset = 0. Read more: <a href="../../tutorials/jak-zarzadzac-ofertami-7GzB2L37ase#liczba-przedmiotow" target="_blank">PL</a> / <a href="../../tutorials/how-to-process-list-of-offers-m09BKA5v8H3#quantity" target="_blank">EN</a>. This resource is rate limited to retrieving information about 270 000 offer changes per minute.


    HTTP: ``GET /sale/offer-quantity-change-commands/{commandId}/tasks``
    """
    params = {
        "limit": limit,
        "offset": offset,
    }
    response = get_client().request_json(
        "GET",
        f"/sale/offer-quantity-change-commands/{commandId}/tasks",
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
@requires_writes_enabled
def offer_automatic_pricing_modification_command(
    *, body: dict[str, Any] | None = None
) -> dict[str, Any] | ErrorResponse:
    """Batch offer automatic pricing rules modification

    Use this resource to modify the automatic pricing rules of multiple offers at the same time. Read more: <a href="../../tutorials/jak-zarzadzac-ofertami-7GzB2L37ase#reguly-cenowe" target="_blank">PL</a> / <a href="../../tutorials/how-to-process-list-of-offers-m09BKA5v8H3#pricing-rules" target="_blank">EN</a>. This resource is rate limited to 150 000 offer changes per hour or 9000 offer changes per minute - limit applies to a single user of the application.


    HTTP: ``POST /sale/offer-price-automation-commands``
    """
    params: dict[str, Any] = {}
    response = get_client().request_json(
        "POST",
        f"/sale/offer-price-automation-commands",
        json=body,
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
def getoffer_automatic_pricing_modification_command_status(
    *, commandId: str
) -> dict[str, Any] | ErrorResponse:
    """Automatic pricing command summary

    Returns status and summary of the offer-price-automation-command. Read more: <a href="../../tutorials/jak-zarzadzac-ofertami-7GzB2L37ase#reguly-cenowe" target="_blank">PL</a> / <a href="../../tutorials/how-to-process-list-of-offers-m09BKA5v8H3#pricing-rules" target="_blank">EN</a>. This resource is rate limited to retrieving information about 270 000 offer changes per minute.


    HTTP: ``GET /sale/offer-price-automation-commands/{commandId}``
    """
    params: dict[str, Any] = {}
    response = get_client().request_json(
        "GET",
        f"/sale/offer-price-automation-commands/{commandId}",
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
def getoffer_automatic_pricing_modification_command_tasks_statuses(
    *, commandId: str, limit: int | None = None, offset: int | None = None
) -> dict[str, Any] | ErrorResponse:
    """Automatic pricing command detailed report

    Defaults: limit = 100, offset = 0. Returns status and report of the offer-price-automation-command. Read more: <a href="../../tutorials/jak-zarzadzac-ofertami-7GzB2L37ase#reguly-cenowe" target="_blank">PL</a> / <a href="../../tutorials/how-to-process-list-of-offers-m09BKA5v8H3#pricing-rules" target="_blank">EN</a>. This resource is rate limited to retrieving information about 270 000 offer changes per minute.


    HTTP: ``GET /sale/offer-price-automation-commands/{commandId}/tasks``
    """
    params = {
        "limit": limit,
        "offset": offset,
    }
    response = get_client().request_json(
        "GET",
        f"/sale/offer-price-automation-commands/{commandId}/tasks",
        params=params,
    )
    return cast(dict[str, Any], response)
