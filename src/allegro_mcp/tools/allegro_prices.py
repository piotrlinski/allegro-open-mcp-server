# ruff: noqa
"""Generated MCP tools — DO NOT EDIT.

Run ``make gen-tools`` to regenerate from the cached OpenAPI spec.
Tag: Allegro Prices
"""

from __future__ import annotations

from typing import Any, cast

from ..errors import ErrorResponse
from ._decorators import requires_writes_enabled
from ._runtime import allegro_call, get_client, mcp


@mcp.tool
@allegro_call
def get_allegro_prices_consent_for_offer(*, offerId: str) -> dict[str, Any] | ErrorResponse:
    """Get the current consents' state for an offer

    Use this resource to get the current Allegro Prices consent value for the offer on each of the available marketplaces. Read more: <a href="../../tutorials/jak-przypisac-oferte-kampanii-GRaj0q6Gwuy#allegro-ceny-jak-zarzadzac-zgodami-na-uczestnictwo-w-programie" target="_blank">PL</a> / <a href="../../tutorials/how-to-submit-offers-to-campaigns-AgGjd6EmyH4#allegro-prices-how-to-manage-program-participation-consents" target="_blank">EN</a>.


    HTTP: ``GET /sale/allegro-prices-offer-consents/{offerId}``
    """
    params: dict[str, Any] = {}
    response = get_client().request_json(
        "GET",
        f"/sale/allegro-prices-offer-consents/{offerId}",
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
@requires_writes_enabled
def update_allegro_prices_consent_for_offer(
    *, offerId: str, body: dict[str, Any] | None = None
) -> dict[str, Any] | ErrorResponse:
    """Update consents for an offer

    Use this resource to update the Allegro Prices consent value for the offer on chosen marketplaces. Read more: <a href="../../tutorials/jak-przypisac-oferte-kampanii-GRaj0q6Gwuy#allegro-ceny-jak-zarzadzac-zgodami-na-uczestnictwo-w-programie" target="_blank">PL</a> / <a href="../../tutorials/how-to-submit-offers-to-campaigns-AgGjd6EmyH4#allegro-prices-how-to-manage-program-participation-consents" target="_blank">EN</a>.


    HTTP: ``PUT /sale/allegro-prices-offer-consents/{offerId}``
    """
    params: dict[str, Any] = {}
    response = get_client().request_json(
        "PUT",
        f"/sale/allegro-prices-offer-consents/{offerId}",
        json=body,
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
def get_allegro_prices_eligibility_for_account() -> dict[str, Any] | ErrorResponse:
    """Get the current eligibility information for the account

    Use this resource to get the current Allegro Prices eligibility information for the account on each of the available marketplaces. Read more: <a href="../../tutorials/jak-przypisac-oferte-kampanii-GRaj0q6Gwuy#allegro-ceny-jak-zarzadzac-zgodami-na-uczestnictwo-w-programie" target="_blank">PL</a> / <a href="../../tutorials/how-to-submit-offers-to-campaigns-AgGjd6EmyH4#allegro-prices-how-to-manage-program-participation-consents" target="_blank">EN</a>.


    HTTP: ``GET /sale/allegro-prices-account-eligibility``
    """
    params: dict[str, Any] = {}
    response = get_client().request_json(
        "GET",
        f"/sale/allegro-prices-account-eligibility",
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
@requires_writes_enabled
def update_allegro_prices_consent_for_account(
    *, body: dict[str, Any] | None = None
) -> dict[str, Any] | ErrorResponse:
    """Update consents for the account

    Use this resource to update the Allegro Prices consent value for the account on chosen marketplaces. Read more: <a href="../../tutorials/jak-przypisac-oferte-kampanii-GRaj0q6Gwuy#allegro-ceny-jak-zarzadzac-zgodami-na-uczestnictwo-w-programie" target="_blank">PL</a> / <a href="../../tutorials/how-to-submit-offers-to-campaigns-AgGjd6EmyH4#allegro-prices-how-to-manage-program-participation-consents" target="_blank">EN</a>.


    HTTP: ``PUT /sale/allegro-prices-account-consent``
    """
    params: dict[str, Any] = {}
    response = get_client().request_json(
        "PUT",
        f"/sale/allegro-prices-account-consent",
        json=body,
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
def get_account_participation() -> dict[str, Any] | ErrorResponse:
    """Get account participation status

    Use this resource to retrieve the account participation status for all supported marketplaces in the Allegro Prices program.


    HTTP: ``GET /sale/allegro-prices/accounts/participations``
    """
    params: dict[str, Any] = {}
    response = get_client().request_json(
        "GET",
        f"/sale/allegro-prices/accounts/participations",
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
@requires_writes_enabled
def update_account_participation(
    *, body: dict[str, Any] | None = None
) -> dict[str, Any] | ErrorResponse:
    """Update account participation

    Use this resource to update the account participation status for one or more marketplaces in the Allegro Prices program.


    HTTP: ``PATCH /sale/allegro-prices/accounts/participations``
    """
    params: dict[str, Any] = {}
    response = get_client().request_json(
        "PATCH",
        f"/sale/allegro-prices/accounts/participations",
        json=body,
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
@requires_writes_enabled
def submit_offer_commands(*, body: dict[str, Any] | None = None) -> dict[str, Any] | ErrorResponse:
    """Submit offers command

    Use this resource to submit a command to add offers to the Allegro Prices program. Returns a command ID that can be used to track the processing status.


    HTTP: ``POST /sale/allegro-prices/offers/submit-offer-commands``
    """
    params: dict[str, Any] = {}
    response = get_client().request_json(
        "POST",
        f"/sale/allegro-prices/offers/submit-offer-commands",
        json=body,
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
def get_submit_offer_command_status(*, commandId: str) -> dict[str, Any] | ErrorResponse:
    """Get submit offer command status

    Use this resource to retrieve the status and details of a previously submitted offer command.


    HTTP: ``GET /sale/allegro-prices/offers/submit-offer-commands/{commandId}``
    """
    params: dict[str, Any] = {}
    response = get_client().request_json(
        "GET",
        f"/sale/allegro-prices/offers/submit-offer-commands/{commandId}",
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
@requires_writes_enabled
def exclude_offer_commands(*, body: dict[str, Any] | None = None) -> dict[str, Any] | ErrorResponse:
    """Exclude offers command

    Use this resource to submit a command to exclude offers from the Allegro Prices program. Returns a command ID that can be used to track the processing status.


    HTTP: ``POST /sale/allegro-prices/offers/exclusion-commands``
    """
    params: dict[str, Any] = {}
    response = get_client().request_json(
        "POST",
        f"/sale/allegro-prices/offers/exclusion-commands",
        json=body,
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
def get_exclude_offer_command_status(*, commandId: str) -> dict[str, Any] | ErrorResponse:
    """Get exclude offer command status

    Use this resource to retrieve the status and details of a previously submitted exclusion command.


    HTTP: ``GET /sale/allegro-prices/offers/exclusion-commands/{commandId}``
    """
    params: dict[str, Any] = {}
    response = get_client().request_json(
        "GET",
        f"/sale/allegro-prices/offers/exclusion-commands/{commandId}",
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
@requires_writes_enabled
def get_allegro_prices_offers(
    *, body: dict[str, Any] | None = None
) -> dict[str, Any] | ErrorResponse:
    """Query Allegro Prices offers status

    Use this resource to retrieve a list of offers and their status in the Allegro Prices program with optional filtering and pagination. Allows filtering by offer IDs, marketplace, and scope (WITH_DECLARATION, DISCOUNTED, or EXCLUDED). Only offers in ACTIVATING, ACTIVE, or ENDED statuses are considered.


    HTTP: ``POST /sale/allegro-prices/offers-queries``
    """
    params: dict[str, Any] = {}
    response = get_client().request_json(
        "POST",
        f"/sale/allegro-prices/offers-queries",
        json=body,
        params=params,
    )
    return cast(dict[str, Any], response)
