# ruff: noqa
"""Generated MCP tools — DO NOT EDIT.

Run ``make gen-tools`` to regenerate from the cached OpenAPI spec.
Tag: Offer management
"""

from __future__ import annotations

from typing import Any, cast

from ..errors import ErrorResponse
from ._decorators import requires_writes_enabled
from ._runtime import allegro_call, get_client, mcp


@mcp.tool
@allegro_call
@requires_writes_enabled
def create_product_offers(*, body: dict[str, Any] | None = None) -> dict[str, Any] | ErrorResponse:
    """Create offer based on product

    Use this resource to create offer based on product. Read more: <a href="../../tutorials/jak-jednym-requestem-wystawic-oferte-powiazana-z-produktem-D7Kj9gw4xFA#jak-utworzyc-oferte-powiazana-z-produktem" target="_blank">PL</a> / <a href="../../tutorials/list-offer-assigned-product-one-request-D7Kj9M71Bu6#how-to-list-product-offer" target="_blank">EN</a>. Note that requests may be limited.


    HTTP: ``POST /sale/product-offers``
    """
    params: dict[str, Any] = {}
    response = get_client().request_json(
        "POST",
        f"/sale/product-offers",
        json=body,
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
@requires_writes_enabled
def edit_product_offers(
    *, offerId: str, body: dict[str, Any] | None = None
) -> dict[str, Any] | ErrorResponse:
    """Edit an offer

    Use this resource to edit offer. This resource allows you to edit each field independently, so use it if you want to change only, for example, the price or the quantity in an offer. Read more: <a href="../../tutorials/jak-zarzadzac-ofertami-7GzB2L37ase#edycja-pojedynczej-oferty" target="_blank">PL</a> / <a href="../../tutorials/how-to-process-list-of-offers-m09BKA5v8H3#editing-single-offer" target="_blank">EN</a>. Note that requests may be limited.


    HTTP: ``PATCH /sale/product-offers/{offerId}``
    """
    params: dict[str, Any] = {}
    response = get_client().request_json(
        "PATCH",
        f"/sale/product-offers/{offerId}",
        json=body,
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
def get_product_offer_processing_status(
    *, offerId: str, operationId: str
) -> dict[str, Any] | ErrorResponse:
    """Check the processing status of a POST or PATCH request

    The URI for the resource given by Location header of POST /sale/product-offers and PATCH /sale/product-offers/{offerId}. Use this resource to check processing status of a POST or PATCH request. Read more: <a href="../../tutorials/jak-jednym-requestem-wystawic-oferte-powiazana-z-produktem-D7Kj9gw4xFA#publikacja-oferty-w-asynchronicznym-api" target="_blank">PL</a> / <a href="../../tutorials/list-offer-assigned-product-one-request-D7Kj9M71Bu6#offer-publication-in-asynchronous-api" target="_blank">EN</a>.


    HTTP: ``GET /sale/product-offers/{offerId}/operations/{operationId}``
    """
    params: dict[str, Any] = {}
    response = get_client().request_json(
        "GET",
        f"/sale/product-offers/{offerId}/operations/{operationId}",
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
@requires_writes_enabled
def delete_offer_using_delete(*, offerId: str) -> dict[str, Any] | ErrorResponse:
    """Delete a draft offer

    Use this resource to delete a draft offer. Read more: <a href="../../tutorials/jak-jednym-requestem-wystawic-oferte-powiazana-z-produktem-D7Kj9gw4xFA#szkic-oferty" target="_blank">PL</a> / <a href="../../tutorials/list-offer-assigned-product-one-request-D7Kj9M71Bu6#inactive-status" target="_blank">EN</a>.


    HTTP: ``DELETE /sale/offers/{offerId}``
    """
    params: dict[str, Any] = {}
    response = get_client().request_json(
        "DELETE",
        f"/sale/offers/{offerId}",
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
@requires_writes_enabled
def create_change_price_command_using_put(
    *, offerId: str, commandId: str, body: dict[str, Any] | None = None
) -> dict[str, Any] | ErrorResponse:
    """Modify the Buy Now price in an offer

    Use this resource to change the Buy Now price in a single offer. Read more: <a href="../../news/mozliwosc-zmiany-ceny-kup-teraz-2YzrKRrr3Sl" target="_blank">PL</a> / <a href="../../news/possibility-to-change-the-buy-it-now-price-q018mq8D2hW" target="_blank">EN</a>.


    HTTP: ``PUT /offers/{offerId}/change-price-commands/{commandId}``
    """
    params: dict[str, Any] = {}
    response = get_client().request_json(
        "PUT",
        f"/offers/{offerId}/change-price-commands/{commandId}",
        json=body,
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
@requires_writes_enabled
def change_publication_status_using_put(
    *, commandId: str, body: dict[str, Any] | None = None
) -> dict[str, Any] | ErrorResponse:
    """Batch offer publish / unpublish

    Use this resource to modify multiple offers publication at once. Read more: <a href="../../tutorials/jak-zarzadzac-ofertami-7GzB2L37ase#jak-zakonczyc-oferte" target="_blank">PL</a> / <a href="../../tutorials/how-to-process-list-of-offers-m09BKA5v8H3#ending-offers" target="_blank">EN</a>. This resource is rate limited to 250 000 offer changes per hour or 9000 offer changes per minute.


    HTTP: ``PUT /sale/offer-publication-commands/{commandId}``
    """
    params: dict[str, Any] = {}
    response = get_client().request_json(
        "PUT",
        f"/sale/offer-publication-commands/{commandId}",
        json=body,
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
def get_publication_report_using_get(*, commandId: str) -> dict[str, Any] | ErrorResponse:
    """Publish command summary

    Use this resource to retrieve information about the offer listing statuses. You will receive a summary with a number of correctly listed offers and errors. Read more: <a href="../../tutorials/jak-jednym-requestem-wystawic-oferte-powiazana-z-produktem-D7Kj9gw4xFA#zestawienie-zadan" target="_blank">PL</a> / <a href="../../tutorials/list-offer-assigned-product-one-request-D7Kj9M71Bu6#task-list" target="_blank">EN</a>. This resource is rate limited to retrieving information about 270 000 offer changes per minute.


    HTTP: ``GET /sale/offer-publication-commands/{commandId}``
    """
    params: dict[str, Any] = {}
    response = get_client().request_json(
        "GET",
        f"/sale/offer-publication-commands/{commandId}",
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
def get_publication_tasks_using_get(
    *, commandId: str, limit: int | None = None, offset: int | None = None
) -> dict[str, Any] | ErrorResponse:
    """Publish command detailed report

    Use this resource to retrieve information about the offer statuses on the site (Defaults: limit = 100, offset = 0). Read more: <a href="../../tutorials/jak-jednym-requestem-wystawic-oferte-powiazana-z-produktem-D7Kj9gw4xFA#asynchroniczne-procesowanie" target="_blank">PL</a> / <a href="../../tutorials/list-offer-assigned-product-one-request-D7Kj9M71Bu6#asynchronous-processing" target="_blank">EN</a>. This resource is rate limited to retrieving information about 270 000 offer changes per minute.


    HTTP: ``GET /sale/offer-publication-commands/{commandId}/tasks``
    """
    params = {
        "limit": limit,
        "offset": offset,
    }
    response = get_client().request_json(
        "GET",
        f"/sale/offer-publication-commands/{commandId}/tasks",
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
def get_available_offer_promotion_packages() -> dict[str, Any] | ErrorResponse:
    """Get all available offer promotion packages

    Use this resource to retrieve all available offer promotion packages. Read more: <a href="../../tutorials/jak-zarzadzac-ofertami-7GzB2L37ase#jak-pobrac-dostepne-opcje-promowania" target="_blank">PL</a> / <a href="../../tutorials/how-to-process-list-of-offers-m09BKA5v8H3#how-to-retrieve-available-promo-options" target="_blank">EN</a>.


    HTTP: ``GET /sale/offer-promotion-packages``
    """
    params: dict[str, Any] = {}
    response = get_client().request_json(
        "GET",
        f"/sale/offer-promotion-packages",
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
@requires_writes_enabled
def modify_offer_promo_options_using_post(
    *, offerId: str, body: dict[str, Any] | None = None
) -> dict[str, Any] | ErrorResponse:
    """Modify offer promotion packages

    Use this resource to modify offer promotion packages. Read more: <a href="../../tutorials/jak-zarzadzac-ofertami-7GzB2L37ase#jak-dodac-lub-zmienic-opcje-promowania-w-pojedynczej-ofercie" target="_blank">PL</a> / <a href="../../tutorials/how-to-process-list-of-offers-m09BKA5v8H3#how-to-add-or-change-promo-options-in-a-single-offer" target="_blank">EN</a>.


    HTTP: ``POST /sale/offers/{offerId}/promo-options-modification``
    """
    params: dict[str, Any] = {}
    response = get_client().request_json(
        "POST",
        f"/sale/offers/{offerId}/promo-options-modification",
        json=body,
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
def get_offer_promo_options_using_get(*, offerId: str) -> dict[str, Any] | ErrorResponse:
    """Get offer promotion packages

    Use this resource to get promotion packages assigned to an offer. Read more: <a href="../../tutorials/jak-zarzadzac-ofertami-7GzB2L37ase#jak-pobrac-opcje-promowania-przypisane-do-oferty" target="_blank">PL</a> / <a href="../../tutorials/how-to-process-list-of-offers-m09BKA5v8H3#how-to-retrieve-promo-options-assigned-to-an-offer" target="_blank">EN</a>.


    HTTP: ``GET /sale/offers/{offerId}/promo-options``
    """
    params: dict[str, Any] = {}
    response = get_client().request_json(
        "GET",
        f"/sale/offers/{offerId}/promo-options",
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
def get_promo_options_for_seller_offers_using_get(
    *, limit: int | None = None, offset: int | None = None
) -> dict[str, Any] | ErrorResponse:
    """Get promo options for seller's offers

    Use this resource to retrieve promo options for seller offers. Read more: <a href="../../tutorials/jak-zarzadzac-ofertami-7GzB2L37ase#jak-pobrac-opcje-promowania-dla-wielu-ofert" target="_blank">PL</a> / <a href="../../tutorials/how-to-process-list-of-offers-m09BKA5v8H3#how-to-retrieve-available-promo-options-for-multiple-offers" target="_blank">EN</a>.


    HTTP: ``GET /sale/offers/promo-options``
    """
    params = {
        "limit": limit,
        "offset": offset,
    }
    response = get_client().request_json(
        "GET",
        f"/sale/offers/promo-options",
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
@requires_writes_enabled
def promo_modification_command_using_put(
    *, commandId: str, body: dict[str, Any] | None = None
) -> dict[str, Any] | ErrorResponse:
    """Batch offer promotion package modification

    Use this resource to modify promotion packages on multiple offers at once. Read more: <a href="../../tutorials/jak-zarzadzac-ofertami-7GzB2L37ase#jak-dodac-lub-edytowac-opcje-promowania-na-wielu-ofertach" target="_blank">PL</a> / <a href="../../tutorials/how-to-process-list-of-offers-m09BKA5v8H3#how-to-add-or-change-promo-options-in-multiple-offers" target="_blank">EN</a>.


    HTTP: ``PUT /sale/offers/promo-options-commands/{commandId}``
    """
    params: dict[str, Any] = {}
    response = get_client().request_json(
        "PUT",
        f"/sale/offers/promo-options-commands/{commandId}",
        json=body,
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
def get_promo_modification_command_result_using_get(
    *, commandId: str
) -> dict[str, Any] | ErrorResponse:
    """Modification command summary

    Use this resource to find out how many offers were edited within one {commandId}. You will receive a summary with a number of successfully edited offers and errors. Read more: <a href="../../tutorials/jak-zarzadzac-ofertami-7GzB2L37ase#jak-sprawdzic-szczegolowy-raport-zadania" target="_blank">PL</a> / <a href="../../tutorials/how-to-process-list-of-offers-m09BKA5v8H3#how-to-check-a-detailed-report-of-your-task" target="_blank">EN</a>.


    HTTP: ``GET /sale/offers/promo-options-commands/{commandId}``
    """
    params: dict[str, Any] = {}
    response = get_client().request_json(
        "GET",
        f"/sale/offers/promo-options-commands/{commandId}",
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
def get_promo_modification_command_detailed_result_using_get(
    *, commandId: str, limit: int | None = None, offset: int | None = None
) -> dict[str, Any] | ErrorResponse:
    """Modification command detailed result

    Use this resource to retrieve the result of an offer modification command. Read more: <a href="../../tutorials/jak-zarzadzac-ofertami-7GzB2L37ase#jak-sprawdzic-szczegolowy-raport-zadania" target="_blank">PL</a> / <a href="../../tutorials/how-to-process-list-of-offers-m09BKA5v8H3#how-to-check-a-detailed-report-of-your-task" target="_blank">EN</a>.


    HTTP: ``GET /sale/offers/promo-options-commands/{commandId}/tasks``
    """
    params = {
        "limit": limit,
        "offset": offset,
    }
    response = get_client().request_json(
        "GET",
        f"/sale/offers/promo-options-commands/{commandId}/tasks",
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
def get_offers_unfilled_parameters_using_get_1(
    *,
    offer_id: list[str] | None = None,
    parameterType: str | None = None,
    offset: int | None = None,
    limit: int | None = None,
) -> dict[str, Any] | ErrorResponse:
    """Get offers with missing parameters

    Use this resource to get information about required parameters or parameters scheduled to become required that are not filled in offers. Read more: <a href="../../tutorials/jak-zarzadzac-ofertami-7GzB2L37ase#jak-sprawdzic-nieuzupelnione-parametry-w-ofertach" target="_blank">PL</a> / <a href="../../tutorials/how-to-process-list-of-offers-m09BKA5v8H3#how-to-check-unfilled-parameters-in-offers" target="_blank">EN</a>.


    HTTP: ``GET /sale/offers/unfilled-parameters``
    """
    params = {
        "offer.id": offer_id,
        "parameterType": parameterType,
        "offset": offset,
        "limit": limit,
    }
    response = get_client().request_json(
        "GET",
        f"/sale/offers/unfilled-parameters",
        params=params,
    )
    return cast(dict[str, Any], response)
