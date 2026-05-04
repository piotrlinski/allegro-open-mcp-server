# ruff: noqa
"""Generated MCP tools — DO NOT EDIT.

Run ``make gen-tools`` to regenerate from the cached OpenAPI spec.
Tag: Badge campaigns
"""

from __future__ import annotations

from typing import Any, cast

from ..errors import ErrorResponse
from ._decorators import requires_writes_enabled
from ._runtime import allegro_call, get_client, mcp


@mcp.tool
@allegro_call
def badge_campaigns_get_all(*, marketplace_id: str | None = None) -> dict[str, Any] | ErrorResponse:
    """Get a list of available badge campaigns

    Badge campaigns are another way to promote your offers. You can apply for a badge, which - depending on a type - will be displayed on your offer page of on the list of offers. First - use this resource to get a list of all available badge campaigns at the moment, then use *POST /sale/badges* to apply for badge. Read more: <a href="../../tutorials/jak-przypisac-oferte-kampanii-GRaj0q6Gwuy#lista-dostepnych-kampanii" target="_blank">PL</a> / <a href="../../tutorials/how-to-submit-offers-to-campaigns-AgGjd6EmyH4#list-of-available-campaigns" target="_blank">EN</a>.


    HTTP: ``GET /sale/badge-campaigns``
    """
    params = {
        "marketplace.id": marketplace_id,
    }
    response = get_client().request_json(
        "GET",
        f"/sale/badge-campaigns",
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
@requires_writes_enabled
def post_badges(*, body: dict[str, Any] | None = None) -> dict[str, Any] | ErrorResponse:
    """Apply for badge in selected offer

    This resource allows you to apply for a badge. Most badges involve additional fee charged. Your badge application will be verified and you will be notified about the verification status via e-mail. You can use *Location* provided in header of the response to track your application status. Application will be removed after 30 days when status of the application was changed form PROCESSED or DECLINED. Fees will be charged in accordance with Annex No. 1 to the <a href="https://allegro.pl/regulaminy/regulamin-strefy-okazji-9dGVAPB69In" target="_blank">Daily deals zone terms and conditions</a>. By using this resource you agree to the <a href="https://allegro.pl/regulaminy/regulamin-strefy-okazji-9dGVAPB69In" target="_blank">Daily deals zone terms and conditions</a> or <a href="https://allegro.pl/regulaminy/regulamin-programu-bonusowego-prowizja-nawet-0-5-0KPkAE7wkcv" target="_blank">Commission discount terms and conditions</a>. Read more: <a href="../../tutorials/jak-przypisac-oferte-kampanii-GRaj0q6Gwuy#zglos-oferte-do-kampanii" target="_blank">PL</a> / <a href="../../tutorials/how-to-submit-offers-to-campaigns-AgGjd6EmyH4#submit-offer-to-a-campaign" target="_blank">EN</a>.


    HTTP: ``POST /sale/badges``
    """
    params: dict[str, Any] = {}
    response = get_client().request_json(
        "POST",
        f"/sale/badges",
        json=body,
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
def get_badges(
    *,
    offer_id: str | None = None,
    marketplace_id: str | None = None,
    offset: int | None = None,
    limit: int | None = None,
) -> dict[str, Any] | ErrorResponse:
    """Get a list of badges

    Use this resource to get a list of badges in authorized seller's offers. Read more: <a href="../../tutorials/jak-przypisac-oferte-kampanii-GRaj0q6Gwuy#kampanie-przypisane-do-ofert" target="_blank">PL</a> / <a href="../../tutorials/how-to-submit-offers-to-campaigns-AgGjd6EmyH4#check-badges-assigned-to-offers" target="_blank">EN</a>.


    HTTP: ``GET /sale/badges``
    """
    params = {
        "offer.id": offer_id,
        "marketplace.id": marketplace_id,
        "offset": offset,
        "limit": limit,
    }
    response = get_client().request_json(
        "GET",
        f"/sale/badges",
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
def badge_applications_get_one(*, applicationId: str) -> dict[str, Any] | ErrorResponse:
    """Get a badge application details

    Use this resource to get a badge application details. Read more: <a href="../../tutorials/jak-przypisac-oferte-kampanii-GRaj0q6Gwuy#pobierz-dane-zgloszenie" target="_blank">PL</a> / <a href="../../tutorials/how-to-submit-offers-to-campaigns-AgGjd6EmyH4#retrieve-campaign-application" target="_blank">EN</a>.


    HTTP: ``GET /sale/badge-applications/{applicationId}``
    """
    params: dict[str, Any] = {}
    response = get_client().request_json(
        "GET",
        f"/sale/badge-applications/{applicationId}",
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
def badge_applications_get_all(
    *,
    campaign_id: str | None = None,
    offer_id: str | None = None,
    offset: int | None = None,
    limit: int | None = None,
) -> dict[str, Any] | ErrorResponse:
    """Get a list of badge applications

    Use this resource to get a list of badge applications. Read more: <a href="../../tutorials/jak-przypisac-oferte-kampanii-GRaj0q6Gwuy#pobierz-swoje-zgloszenia" target="_blank">PL</a> / <a href="../../tutorials/how-to-submit-offers-to-campaigns-AgGjd6EmyH4#retrieve-all-campaign-applications" target="_blank">EN</a>.


    HTTP: ``GET /sale/badge-applications``
    """
    params = {
        "campaign.id": campaign_id,
        "offer.id": offer_id,
        "offset": offset,
        "limit": limit,
    }
    response = get_client().request_json(
        "GET",
        f"/sale/badge-applications",
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
def badge_operations_get_one(*, operationId: str) -> dict[str, Any] | ErrorResponse:
    """Get badge operation details

    Use this resource to get badge operation details. Read more: <a href="../../tutorials/jak-przypisac-oferte-kampanii-GRaj0q6Gwuy#zmiana-ceny-i-zakonczenie-oznaczenia" target="_blank">PL</a> / <a href="../../tutorials/how-to-submit-offers-to-campaigns-AgGjd6EmyH4#change-price-and-finish-badge" target="_blank">EN</a>.


    HTTP: ``GET /sale/badge-operations/{operationId}``
    """
    params: dict[str, Any] = {}
    response = get_client().request_json(
        "GET",
        f"/sale/badge-operations/{operationId}",
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
@requires_writes_enabled
def patch_badge(
    *, offerId: str, campaignId: str, body: dict[str, Any] | None = None
) -> dict[str, Any] | ErrorResponse:
    """Update campaign badge for the given offer

    This resource allows you to update a campaign badge for the given offer. You can use *Location* provided in header of the response to track your update status. Update offer price in a campaign or finish marking an offer in a campaign. Read more: <a href="../../tutorials/jak-przypisac-oferte-kampanii-GRaj0q6Gwuy#zmiana-ceny-i-zakonczenie-oznaczenia" target="_blank">PL</a> / <a href="../../tutorials/how-to-submit-offers-to-campaigns-AgGjd6EmyH4#change-price-and-finish-badge" target="_blank">EN</a>.


    HTTP: ``PATCH /sale/badges/offers/{offerId}/campaigns/{campaignId}``
    """
    params: dict[str, Any] = {}
    response = get_client().request_json(
        "PATCH",
        f"/sale/badges/offers/{offerId}/campaigns/{campaignId}",
        json=body,
        params=params,
    )
    return cast(dict[str, Any], response)
