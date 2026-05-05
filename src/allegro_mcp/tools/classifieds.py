# ruff: noqa
"""Generated MCP tools — DO NOT EDIT.

Run ``make gen-tools`` to regenerate from the cached OpenAPI spec.
Tag: Classifieds
"""

from __future__ import annotations

from typing import Any, cast

from ..errors import ErrorResponse
from ._decorators import requires_writes_enabled
from ._runtime import allegro_call, get_client, mcp


@mcp.tool
@allegro_call
def classified_seller_offer_stats_get(
    *, date_gte: str | None = None, date_lte: str | None = None
) -> dict[str, Any] | ErrorResponse:
    """Get the seller's advertisements daily statistics

    This endpoint returns daily statistics collected for a list of advertisements in a given date range for logged user. Read more: <a href="../../tutorials/jak-wystawic-i-zarzadzac-ogloszeniem-K6r3Z47dKcy#statystyki-wszystkich-ogloszen-sprzedawcy" target="_blank">PL</a> / <a href="../../tutorials/listing-and-managing-classified-ads-5Ln0r6wkWs7#statistics-of-seller-s-classified-ads" target="_blank">EN</a>.


    HTTP: ``GET /sale/classified-seller-stats``
    """
    params = {
        "date.gte": date_gte,
        "date.lte": date_lte,
    }
    response = get_client().request_json(
        "GET",
        f"/sale/classified-seller-stats",
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
def classified_offers_stats_get(
    *, offer_id: list[str] | None = None, date_gte: str | None = None, date_lte: str | None = None
) -> dict[str, Any] | ErrorResponse:
    """Get the advertisements daily statistics

    This endpoint returns daily statistics collected for a list of advertisements in a given date range. Read more: <a href="../../tutorials/jak-wystawic-i-zarzadzac-ogloszeniem-K6r3Z47dKcy#statystyki-wybranych-ogloszen" target="_blank">PL</a> / <a href="../../tutorials/listing-and-managing-classified-ads-5Ln0r6wkWs7#statistics-of-selected-classified-ads" target="_blank">EN</a>.


    HTTP: ``GET /sale/classified-offers-stats``
    """
    params = {
        "offer.id": offer_id,
        "date.gte": date_gte,
        "date.lte": date_lte,
    }
    response = get_client().request_json(
        "GET",
        f"/sale/classified-offers-stats",
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
def get_classified_packages(*, offerId: str) -> dict[str, Any] | ErrorResponse:
    """Get classified packages assigned to an offer

    Use this resource to retrieve classified packages currently assigned to an offer. Read more: <a href="../../tutorials/jak-wystawic-i-zarzadzac-ogloszeniem-K6r3Z47dKcy#dodatkowe-opcje-promowania" target="_blank">PL</a> / <a href="../../tutorials/listing-and-managing-classified-ads-5Ln0r6wkWs7#additional-promo-options" target="_blank">EN</a>.


    HTTP: ``GET /sale/offer-classifieds-packages/{offerId}``
    """
    params: dict[str, Any] = {}
    response = get_client().request_json(
        "GET",
        f"/sale/offer-classifieds-packages/{offerId}",
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
@requires_writes_enabled
def assign_classified_packages(
    *, offerId: str, body: dict[str, Any] | None = None
) -> dict[str, Any] | ErrorResponse:
    """Assign packages to a classified

    Use this resource to assign classified packages to an offer. Read more: <a href="../../tutorials/jak-wystawic-i-zarzadzac-ogloszeniem-K6r3Z47dKcy#dodatkowe-opcje-promowania" target="_blank">PL</a> / <a href="../../tutorials/listing-and-managing-classified-ads-5Ln0r6wkWs7#additional-promo-options" target="_blank">EN</a>.


    HTTP: ``PUT /sale/offer-classifieds-packages/{offerId}``
    """
    params: dict[str, Any] = {}
    response = get_client().request_json(
        "PUT",
        f"/sale/offer-classifieds-packages/{offerId}",
        json=body,
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
def get_classified_package_configurations_for_category(
    *, category_id: str | None = None
) -> dict[str, Any] | ErrorResponse:
    """Get configurations of packages

    Use this resource to retrieve configurations of classifieds packages for a category. Read more: <a href="../../tutorials/jak-wystawic-i-zarzadzac-ogloszeniem-K6r3Z47dKcy#lista-pakietow-i-opcji-dodatkowych" target="_blank">PL</a> / <a href="../../tutorials/listing-and-managing-classified-ads-5Ln0r6wkWs7#list-of-promo-options" target="_blank">EN</a>.


    HTTP: ``GET /sale/classifieds-packages``
    """
    params = {
        "category.id": category_id,
    }
    response = get_client().request_json(
        "GET",
        f"/sale/classifieds-packages",
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
def get_classified_package_configuration(*, packageId: str) -> dict[str, Any] | ErrorResponse:
    """Get the configuration of a package

    Use this resource to retrieve the configuration of a classifieds package. Read more: <a href="../../tutorials/jak-wystawic-i-zarzadzac-ogloszeniem-K6r3Z47dKcy#lista-pakietow-i-opcji-dodatkowych" target="_blank">PL</a> / <a href="../../tutorials/listing-and-managing-classified-ads-5Ln0r6wkWs7#list-of-promo-options" target="_blank">EN</a>.


    HTTP: ``GET /sale/classifieds-packages/{packageId}``
    """
    params: dict[str, Any] = {}
    response = get_client().request_json(
        "GET",
        f"/sale/classifieds-packages/{packageId}",
        params=params,
    )
    return cast(dict[str, Any], response)
