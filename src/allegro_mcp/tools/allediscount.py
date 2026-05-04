# ruff: noqa
"""Generated MCP tools — DO NOT EDIT.

Run ``make gen-tools`` to regenerate from the cached OpenAPI spec.
Tag: AlleDiscount
"""

from __future__ import annotations

from typing import Any, cast

from ..errors import ErrorResponse
from ._decorators import requires_writes_enabled
from ._runtime import allegro_call, get_client, mcp


@mcp.tool
@allegro_call
@requires_writes_enabled
def submit_offer_to_alle_discount_commands(
    *, body: dict[str, Any] | None = None
) -> dict[str, Any] | ErrorResponse:
    """Create submit offer command

    Use this resource to create a command for submitting an offer. Offer will be submitted to the AlleDiscount campaign only if command is processed successfully. Read more: <a href="../../tutorials/jak-przypisac-oferte-kampanii-GRaj0q6Gwuy#jak-zglosic-oferte-do-kampanii" target="_blank">PL</a> / <a href="../../tutorials/how-to-submit-offers-to-campaigns-AgGjd6EmyH4#how-to-submit-an-offer-to-a-campaign" target="_blank">EN</a>.


    HTTP: ``POST /sale/alle-discount/submit-offer-commands``
    """
    params: dict[str, Any] = {}
    response = get_client().request_json(
        "POST",
        f"/sale/alle-discount/submit-offer-commands",
        json=body,
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
def get_submit_offer_to_alle_discount_commands_status(
    *, commandId: str
) -> dict[str, Any] | ErrorResponse:
    """Get the offer submission command status

    Use this resource to get information about the submit offer command execution status. Read more: <a href="../../tutorials/jak-przypisac-oferte-kampanii-GRaj0q6Gwuy#jak-sprawdzic-status-zgloszenia-oferty-do-kampanii" target="_blank">PL</a> / <a href="../../tutorials/how-to-submit-offers-to-campaigns-AgGjd6EmyH4#how-to-check-the-status-of-an-offer-submission-to-a-campaign" target="_blank">EN</a>.


    HTTP: ``GET /sale/alle-discount/submit-offer-commands/{commandId}``
    """
    params: dict[str, Any] = {}
    response = get_client().request_json(
        "GET",
        f"/sale/alle-discount/submit-offer-commands/{commandId}",
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
@requires_writes_enabled
def withdraw_offer_from_alle_discount_commands(
    *, body: dict[str, Any] | None = None
) -> dict[str, Any] | ErrorResponse:
    """Create withdraw offer command

    Use this resource to create a command for withdrawing an offer from specific campaign. Offer will be withdrawn from the AlleDiscount campaign only if command is processed successfully. Read more: <a href="../../tutorials/jak-przypisac-oferte-kampanii-GRaj0q6Gwuy#jak-wycofac-oferte-z-kampanii" target="_blank">PL</a> / <a href="../../tutorials/how-to-submit-offers-to-campaigns-AgGjd6EmyH4#how-to-withdraw-an-offer-from-a-campaign" target="_blank">EN</a>.


    HTTP: ``POST /sale/alle-discount/withdraw-offer-commands``
    """
    params: dict[str, Any] = {}
    response = get_client().request_json(
        "POST",
        f"/sale/alle-discount/withdraw-offer-commands",
        json=body,
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
def get_withdraw_offer_from_alle_discount_commands_status(
    *, commandId: str
) -> dict[str, Any] | ErrorResponse:
    """Get the offer withdrawal command status

    Use this resource to get information about the withdrawal command execution status. Read more: <a href="../../tutorials/jak-przypisac-oferte-kampanii-GRaj0q6Gwuy#jak-sprawdzic-status-wycofania-oferty-z-kampanii" target="_blank">PL</a> / <a href="../../tutorials/how-to-submit-offers-to-campaigns-AgGjd6EmyH4#how-to-check-the-withdrawal-status-of-an-offer-from-a-campaign" target="_blank">EN</a>.


    HTTP: ``GET /sale/alle-discount/withdraw-offer-commands/{commandId}``
    """
    params: dict[str, Any] = {}
    response = get_client().request_json(
        "GET",
        f"/sale/alle-discount/withdraw-offer-commands/{commandId}",
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
def get_offers_eligible_for_alle_discount(
    *,
    campaignId: str,
    limit: int | None = None,
    offset: int | None = None,
    meetsConditions: bool | None = None,
    offerId: str | None = None,
) -> dict[str, Any] | ErrorResponse:
    """List eligible offers

    Endpoint returning info about offers that can be submitted to a given AlleDiscount campaign. Only offer linked to the product in published list of goods (products) can be submitted to a given AlleDiscount campaign. Read more: <a href="../../tutorials/jak-przypisac-oferte-kampanii-GRaj0q6Gwuy#lista-ofert-kwalifikujacych-sie-do-kampanii" target="_blank">PL</a> / <a href="../../tutorials/how-to-submit-offers-to-campaigns-AgGjd6EmyH4#list-of-offers-eligible-for-the-selected-campaign" target="_blank">EN</a>.


    HTTP: ``GET /sale/alle-discount/{campaignId}/eligible-offers``
    """
    params = {
        "limit": limit,
        "offset": offset,
        "meetsConditions": meetsConditions,
        "offerId": offerId,
    }
    response = get_client().request_json(
        "GET",
        f"/sale/alle-discount/{campaignId}/eligible-offers",
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
def get_offers_submitted_to_alle_discount(
    *,
    campaignId: str,
    limit: int | None = None,
    offset: int | None = None,
    offerId: str | None = None,
    participationId: str | None = None,
) -> dict[str, Any] | ErrorResponse:
    """List offer participations

    Endpoint returning info about offer participations for a given AlleDiscount campaign. With this endpoint you are able to validate if the offer participates in AlleDiscount and if it has lowered price on the platform. Read more: <a href="../../tutorials/jak-przypisac-oferte-kampanii-GRaj0q6Gwuy#lista-ofert-zgloszonych-do-wybranej-kampanii" target="_blank">PL</a> / <a href="../../tutorials/how-to-submit-offers-to-campaigns-AgGjd6EmyH4#list-of-offers-submitted-for-the-selected-campaign" target="_blank">EN</a>.


    HTTP: ``GET /sale/alle-discount/{campaignId}/submitted-offers``
    """
    params = {
        "limit": limit,
        "offset": offset,
        "offerId": offerId,
        "participationId": participationId,
    }
    response = get_client().request_json(
        "GET",
        f"/sale/alle-discount/{campaignId}/submitted-offers",
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
def get_alle_discount_campaigns(*, campaignId: str | None = None) -> dict[str, Any] | ErrorResponse:
    """List AlleDiscount campaigns

    List current AlleDiscount campaigns. Each campaign has its own list of goods (products) that indicate which offers can be submitted to it. Read more: <a href="../../tutorials/jak-przypisac-oferte-kampanii-GRaj0q6Gwuy#lista-dostepnych-kampanii-alleobnizka" target="_blank">PL</a> / <a href="../../tutorials/how-to-submit-offers-to-campaigns-AgGjd6EmyH4#list-of-available-allediscount-campaigns" target="_blank">EN</a>.


    HTTP: ``GET /sale/alle-discount/campaigns``
    """
    params = {
        "campaignId": campaignId,
    }
    response = get_client().request_json(
        "GET",
        f"/sale/alle-discount/campaigns",
        params=params,
    )
    return cast(dict[str, Any], response)
