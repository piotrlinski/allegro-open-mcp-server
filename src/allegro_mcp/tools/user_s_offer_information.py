# ruff: noqa
"""Generated MCP tools — DO NOT EDIT.

Run ``make gen-tools`` to regenerate from the cached OpenAPI spec.
Tag: User's offer information
"""

from __future__ import annotations

from typing import Any, cast

from ..errors import ErrorResponse
from ._decorators import requires_writes_enabled
from ._runtime import allegro_call, get_client, mcp


@mcp.tool
@allegro_call
def get_product_offer(*, offerId: str) -> dict[str, Any] | ErrorResponse:
    """Get all data of the particular product-offer

    Use this resource to retrieve all data of the particular product-offer. Read more: <a href="../../tutorials/jak-jednym-requestem-wystawic-oferte-powiazana-z-produktem-D7Kj9gw4xFA#asynchroniczne-procesowanie" target="_blank">PL</a> / <a href="../../tutorials/list-offer-assigned-product-one-request-D7Kj9M71Bu6#asynchronous-processing" target="_blank">EN</a>.


    HTTP: ``GET /sale/product-offers/{offerId}``
    """
    params: dict[str, Any] = {}
    response = get_client().request_json(
        "GET",
        f"/sale/product-offers/{offerId}",
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
def get_partial_product_offer(
    *, offerId: str, include: list[str] | None = None
) -> dict[str, Any] | ErrorResponse:
    """Get selected data of the particular product-offer

    Use this resource to retrieve selected data of the particular product-offer. The model and functionality is a subset of the full product offer get endpoint (`GET /sale/product-offers/{offerId}`), but it is faster and more reliable. Read more: <a href="../../news/get-sale-product-offers-offerid-parts-pobierz-wybrane-elementy-oferty-aMoB3nZk3Iv" target="_blank">PL</a> / <a href="../../news/get-sale-product-offers-offerid-parts-retrieve-selected-parts-of-the-offer-Pg51yzeAPf3" target="_blank">EN</a>.


    HTTP: ``GET /sale/product-offers/{offerId}/parts``
    """
    params = {
        "include": include,
    }
    response = get_client().request_json(
        "GET",
        f"/sale/product-offers/{offerId}/parts",
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
def search_offers_using_get(
    *,
    offer_id: list[str] | None = None,
    name: str | None = None,
    sellingMode_price_amount_gte: float | None = None,
    sellingMode_price_amount_lte: float | None = None,
    sellingMode_priceAutomation_rule_id: str | None = None,
    sellingMode_priceAutomation_rule_id_empty: bool | None = None,
    publication_status: list[str] | None = None,
    publication_marketplace: str | None = None,
    sellingMode_format: list[str] | None = None,
    external_id: list[str] | None = None,
    delivery_shippingRates_id: str | None = None,
    delivery_shippingRates_id_empty: bool | None = None,
    sort: str | None = None,
    limit: int | None = None,
    offset: int | None = None,
    category_id: str | None = None,
    product_id_empty: bool | None = None,
    productizationRequired: bool | None = None,
    b2b_buyableOnlyByBusiness: bool | None = None,
    fundraisingCampaign_id: str | None = None,
    fundraisingCampaign_id_empty: bool | None = None,
    afterSalesServices_returnPolicy_id: str | None = None,
    isFulfillment: bool | None = None,
) -> dict[str, Any] | ErrorResponse:
    """Get seller's offers

    Use this resource to get the list of the seller's offers. You can use different query parameters to filter the list. Read more: <a href="../../tutorials/jak-zarzadzac-ofertami-7GzB2L37ase#jak-pobrac-moje-oferty-w-rest-api" target="_blank">PL</a> / <a href="../../tutorials/how-to-process-list-of-offers-m09BKA5v8H3#list-of-offers" target="_blank">EN</a>.


    HTTP: ``GET /sale/offers``
    """
    params = {
        "offer.id": offer_id,
        "name": name,
        "sellingMode.price.amount.gte": sellingMode_price_amount_gte,
        "sellingMode.price.amount.lte": sellingMode_price_amount_lte,
        "sellingMode.priceAutomation.rule.id": sellingMode_priceAutomation_rule_id,
        "sellingMode.priceAutomation.rule.id.empty": sellingMode_priceAutomation_rule_id_empty,
        "publication.status": publication_status,
        "publication.marketplace": publication_marketplace,
        "sellingMode.format": sellingMode_format,
        "external.id": external_id,
        "delivery.shippingRates.id": delivery_shippingRates_id,
        "delivery.shippingRates.id.empty": delivery_shippingRates_id_empty,
        "sort": sort,
        "limit": limit,
        "offset": offset,
        "category.id": category_id,
        "product.id.empty": product_id_empty,
        "productizationRequired": productizationRequired,
        "b2b.buyableOnlyByBusiness": b2b_buyableOnlyByBusiness,
        "fundraisingCampaign.id": fundraisingCampaign_id,
        "fundraisingCampaign.id.empty": fundraisingCampaign_id_empty,
        "afterSalesServices.returnPolicy.id": afterSalesServices_returnPolicy_id,
        "isFulfillment": isFulfillment,
    }
    response = get_client().request_json(
        "GET",
        f"/sale/offers",
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
def get_offer_smart_classification_get(
    *, offerId: str, marketplaceId: str | None = None
) -> dict[str, Any] | ErrorResponse:
    """Get Smart! classification report of the particular offer

    Use this resource to get a full Smart! offer classification report of one of your offers. Please keep in mind you have to meet Smart! seller conditions first - for more details, use *GET /sale/smart*. To learn more about Smart! offer requirements, see our knowledge base article: [PL](https://help.allegro.com/pl/sell/a/allegro-smart-na-allegro-pl-informacje-dla-sprzedajacych-9g0rWRXKxHG#jakie-warunki-musisz-spelnic-aby-zyskac-oznaczenie-smart) / [EN](https://help.allegro.com/en/sell/a/allegro-smart-on-allegro-pl-information-for-sellers-LR8j8Y26GTR#what-requirements-you-need-to-meet-to-get-the-smart-badge). Read more: <a href="../../tutorials/jak-zarzadzac-kontem-danymi-uzytkownika-ZM9YAKgPgi2#kwalifikacja-oferty" target="_blank">PL</a> / <a href="../../tutorials/account-and-user-data-management-jn9vBjqjnsw#offer-qualification" target="_blank">EN</a>.


    HTTP: ``GET /sale/offers/{offerId}/smart``
    """
    params = {
        "marketplaceId": marketplaceId,
    }
    response = get_client().request_json(
        "GET",
        f"/sale/offers/{offerId}/smart",
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
def get_offer_events(
    *, from_: str | None = None, limit: int | None = None, type_: list[str] | None = None
) -> dict[str, Any] | ErrorResponse:
    """Get events about the seller's offers

    Use this endpoint to get events from the last 24 hours concerning changes in the authorized seller's offers. At present we support the following events: - OFFER_ACTIVATED - offer is visible on site and available for purchase, occurs when offer status changes from ACTIVATING to ACTIVE. - OFFER_CHANGED - occurs when offer's fields has been changed e.g. description or photos. - OFFER_ENDED - offer is no longer available for purchase, occurs when offer status changes from ACTIVE to ENDED. - OFFER_STOCK_CHANGED - stock in an offer was changed either via purchase or by seller. - OFFER_PRICE_CHANGED - occurs when price in an offer was changed. - OFFER_ARCHIVED - offer is no longer available on listing and has been archived. - OFFER_BID_PLACED - bid was placed on the offer. - OFFER_BID_CANCELED - bid for offer was canceled. - OFFER_TRANSLATION_UPDATED - translation of offer was updated. - OFFER_VISIBILITY_CHANGED - visibility of offer was changed on marketplaces. - OFFER_DELIVERY_COUNTRIES_BLOCKED - the offer has been blocked in selected countries. Returned events may occur by actions made via browser or API. The resource allows you to get events concerning active offers and offers scheduled for activation (status ACTIVE and ACTIVATING). Returned events do not concern offers in INACTIVE and ENDED status (the exception is OFFER_ARCHIVED event). External id is returned for all event types except OFFER_BID_PLACED and OFFER_BID_CANCELED. Please note that one change may result in more…


    HTTP: ``GET /sale/offer-events``
    """
    params = {
        "from": from_,
        "limit": limit,
        "type": type_,
    }
    response = get_client().request_json(
        "GET",
        f"/sale/offer-events",
        params=params,
    )
    return cast(dict[str, Any], response)
