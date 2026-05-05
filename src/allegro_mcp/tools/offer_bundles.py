# ruff: noqa
"""Generated MCP tools — DO NOT EDIT.

Run ``make gen-tools`` to regenerate from the cached OpenAPI spec.
Tag: Offer bundles
"""

from __future__ import annotations

from typing import Any, cast

from ..errors import ErrorResponse
from ._decorators import requires_writes_enabled
from ._runtime import allegro_call, get_client, mcp


@mcp.tool
@allegro_call
@requires_writes_enabled
def create_offer_bundle(*, body: dict[str, Any] | None = None) -> dict[str, Any] | ErrorResponse:
    """Create a new offer bundle

    You can create <a href="https://help.allegro.com/sell/en/a/how-to-create-offer-bundles-rj9eAL2XnhK?marketplaceId=allegro-pl" target="_blank">offer bundle</a> using this endpoint. Bundle has to contain at least two offers and at least one of them has to be set as an entry point. Bundle will be shown on offers' pages which are marked as entry points. You can also specify how many units of each offer will be in bundle using `requiredQuantity` property. <br> Additionally, discount can be specified for each marketplace separately. If you do not want to set discount, set `discounts` property to `null` or empty array. Also, you do not have to specify discount on all marketplaces. Fill marketplaces in 'discounts' array accordingly to your needs. <br> Read more: <a href="../../tutorials/jak-zarzadzac-rabatami-promocjami-yPya2mj6zUP#utworz-zestaw-ofert" target="_blank">PL</a> / <a href="../../tutorials/how-to-manage-rebates-and-promotions-g05avdL0vT4#create-an-offer-bundle" target="_blank">EN</a>.


    HTTP: ``POST /sale/bundles``
    """
    params: dict[str, Any] = {}
    response = get_client().request_json(
        "POST",
        f"/sale/bundles",
        json=body,
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
def list_sellers_offer_bundles(
    *, limit: int | None = None, offer_id: str | None = None, page_id: str | None = None
) -> dict[str, Any] | ErrorResponse:
    """List seller's bundles

    You can fetch page of seller's offer bundles using this endpoint. <br> Paging: <br> To move to next page, specify `page.id` parameter with value obtained in response from previous request. Number of offer bundles on single page can be specified using `limit` parameter. <br> Filtering: <br> Offer bundles can be filtered to bundles which contain offer specified in `offer.id` parameter. Read more: <a href="../../tutorials/jak-zarzadzac-rabatami-promocjami-yPya2mj6zUP#pobierz-liste-zestawow-ofert" target="_blank">PL</a> / <a href="../../tutorials/how-to-manage-rebates-and-promotions-g05avdL0vT4#retrieve-offer-bundles-list" target="_blank">EN</a>.


    HTTP: ``GET /sale/bundles``
    """
    params = {
        "limit": limit,
        "offer.id": offer_id,
        "page.id": page_id,
    }
    response = get_client().request_json(
        "GET",
        f"/sale/bundles",
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
def get_offer_bundle(*, bundleId: str) -> dict[str, Any] | ErrorResponse:
    """Get bundle by ID

    Use this resource to retrieve offer bundle by its unique identifier. Read more: <a href="../../tutorials/jak-zarzadzac-rabatami-promocjami-yPya2mj6zUP#pobierz-szczegoly-wybranego-zestawu" target="_blank">PL</a> / <a href="../../tutorials/how-to-manage-rebates-and-promotions-g05avdL0vT4#retrieve-details-of-the-selected-offer-bundle" target="_blank">EN</a>.


    HTTP: ``GET /sale/bundles/{bundleId}``
    """
    params: dict[str, Any] = {}
    response = get_client().request_json(
        "GET",
        f"/sale/bundles/{bundleId}",
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
@requires_writes_enabled
def delete_offer_bundle(*, bundleId: str) -> dict[str, Any] | ErrorResponse:
    """Delete bundle by ID

    Use this resource to delete offer bundle by its unique identifier. Read more: <a href="../../tutorials/jak-zarzadzac-rabatami-promocjami-yPya2mj6zUP#usun-wybrany-zestaw" target="_blank">PL</a> / <a href="../../tutorials/how-to-manage-rebates-and-promotions-g05avdL0vT4#remove-the-selected-offer-bundle" target="_blank">EN</a>.


    HTTP: ``DELETE /sale/bundles/{bundleId}``
    """
    params: dict[str, Any] = {}
    response = get_client().request_json(
        "DELETE",
        f"/sale/bundles/{bundleId}",
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
@requires_writes_enabled
def update_offer_bundle_discount(
    *, bundleId: str, body: dict[str, Any] | None = None
) -> dict[str, Any] | ErrorResponse:
    """Update discount associated with bundle

    Use this resource to update discount per marketplaces associated with bundle specified by its unique identifier. This will override currently set discounts for all marketplaces, so the unchanged discounts also must be specified in request. In case discount for marketplace is not specified in request it will be deleted. Read more: <a href="../../tutorials/jak-zarzadzac-rabatami-promocjami-yPya2mj6zUP#zmien-rabat-przypisany-do-wybranego-zestawu" target="_blank">PL</a> / <a href="../../tutorials/how-to-manage-rebates-and-promotions-g05avdL0vT4#change-the-discount-for-the-selected-offer-bundle" target="_blank">EN</a>.


    HTTP: ``PUT /sale/bundles/{bundleId}/discount``
    """
    params: dict[str, Any] = {}
    response = get_client().request_json(
        "PUT",
        f"/sale/bundles/{bundleId}/discount",
        json=body,
        params=params,
    )
    return cast(dict[str, Any], response)
