# ruff: noqa
"""Generated MCP tools — DO NOT EDIT.

Run ``make gen-tools`` to regenerate from the cached OpenAPI spec.
Tag: Categories and parameters
"""

from __future__ import annotations

from typing import Any, cast

from ..errors import ErrorResponse
from ._decorators import requires_writes_enabled
from ._runtime import allegro_call, get_client, mcp


@mcp.tool
@allegro_call
def get_categories_using_get(*, parent_id: str | None = None) -> dict[str, Any] | ErrorResponse:
    """Get IDs of Allegro categories

    Use this resource to traverse the Allegro categories tree. It returns the list of the given category's children or a list of the main Allegro categories. Read more: <a href="../../tutorials/jak-jednym-requestem-wystawic-oferte-powiazana-z-produktem-D7Kj9gw4xFA#uzupelnij-kategorie-i-parametry" target="_blank">PL</a> / <a href="../../tutorials/list-offer-assigned-product-one-request-D7Kj9M71Bu6#provide-category-and-parameters" target="_blank">EN</a>.


    HTTP: ``GET /sale/categories``
    """
    params = {
        "parent.id": parent_id,
    }
    response = get_client().request_json(
        "GET",
        f"/sale/categories",
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
def get_category_using_get_1(*, categoryId: str) -> dict[str, Any] | ErrorResponse:
    """Get a category by ID

    Use this resource to get the details of a specific category. Read more: <a href="../../tutorials/jak-jednym-requestem-wystawic-oferte-powiazana-z-produktem-D7Kj9gw4xFA#jak-utworzyc-nowy-produkt" target="_blank">PL</a> / <a href="../../tutorials/list-offer-assigned-product-one-request-D7Kj9M71Bu6#how-to-create-a-product" target="_blank">EN</a>.


    HTTP: ``GET /sale/categories/{categoryId}``
    """
    params: dict[str, Any] = {}
    response = get_client().request_json(
        "GET",
        f"/sale/categories/{categoryId}",
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
def get_flat_parameters_using_get_2(*, categoryId: str) -> dict[str, Any] | ErrorResponse:
    """Get parameters supported by a category

    Use this resource to get the list of parameters that are supported by the given category. Read more: <a href="../../tutorials/jak-jednym-requestem-wystawic-oferte-powiazana-z-produktem-D7Kj9gw4xFA#parametry-ofertowe" target="_blank">PL</a> / <a href="../../tutorials/list-offer-assigned-product-one-request-D7Kj9M71Bu6#offer-parameters" target="_blank">EN</a>.


    HTTP: ``GET /sale/categories/{categoryId}/parameters``
    """
    params: dict[str, Any] = {}
    response = get_client().request_json(
        "GET",
        f"/sale/categories/{categoryId}/parameters",
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
def get_category_parameters_scheduled_changes_using_get_1(
    *,
    scheduledFor_gte: str | None = None,
    scheduledFor_lte: str | None = None,
    scheduledAt_gte: str | None = None,
    scheduledAt_lte: str | None = None,
    type_: list[str] | None = None,
    offset: int | None = None,
    limit: int | None = None,
) -> dict[str, Any] | ErrorResponse:
    """Get planned changes in category parameters

    Use this resource to get information about planned changes in category parameters. Please note that in some cases, the returned events may finally not happen in the future. At present we support the following changes: - REQUIREMENT_CHANGE - the parameter will be required in the category. Read more: <a href="../../tutorials/jak-zarzadzac-ofertami-7GzB2L37ase#jak-sprawdzic-przyszle-zmiany-w-parametrach" target="_blank">PL</a> / <a href="../../tutorials/how-to-process-list-of-offers-m09BKA5v8H3#how-to-check-future-changes-in-parameters" target="_blank">EN</a>.


    HTTP: ``GET /sale/category-parameters-scheduled-changes``
    """
    params = {
        "scheduledFor.gte": scheduledFor_gte,
        "scheduledFor.lte": scheduledFor_lte,
        "scheduledAt.gte": scheduledAt_gte,
        "scheduledAt.lte": scheduledAt_lte,
        "type": type_,
        "offset": offset,
        "limit": limit,
    }
    response = get_client().request_json(
        "GET",
        f"/sale/category-parameters-scheduled-changes",
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
def get_category_events_using_get_1(
    *, from_: str | None = None, limit: int | None = None, type_: list[str] | None = None
) -> dict[str, Any] | ErrorResponse:
    """Get changes in categories

    Use this resource to get information about changes in categories. It returns changes that occurred in the last 3 months. At present we support the following changes: - CATEGORY_CREATED - new category was created. - CATEGORY_RENAMED - category name has been changed. - CATEGORY_MOVED - category has been moved to a different place in category tree, category parent id field is changed. - CATEGORY_DELETED - category is no longer available, category from redirectCategory field should be used instead. Read more: <a href="../../tutorials/jak-zarzadzac-ofertami-7GzB2L37ase#dziennik-zmian-w-kategoriach" target="_blank">PL</a> / <a href="../../tutorials/how-to-process-list-of-offers-m09BKA5v8H3#event-journal-in-categories" target="_blank">EN</a>.


    HTTP: ``GET /sale/category-events``
    """
    params = {
        "from": from_,
        "limit": limit,
        "type": type_,
    }
    response = get_client().request_json(
        "GET",
        f"/sale/category-events",
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
def category_suggestion_using_get(*, name: str | None = None) -> dict[str, Any] | ErrorResponse:
    """Get categories suggestions

    Use this resource to receive suggested categories for given phrase. This resource is rate limited to 5 requests per second. Read more: <a href="../../news/udostepnilismy-nowy-zasob-dzieki-ktoremu-sprawdzisz-sugerowane-kategorie-dla-podanej-frazy-4RAl9jwX1FW" target="_blank">PL</a> / <a href="../../news/we-have-introduced-a-new-resource-that-allows-you-to-retrieve-the-suggested-categories-for-the-given-phrase-v8Wdy1EOyF0" target="_blank">EN</a>.


    HTTP: ``GET /sale/matching-categories``
    """
    params = {
        "name": name,
    }
    response = get_client().request_json(
        "GET",
        f"/sale/matching-categories",
        params=params,
    )
    return cast(dict[str, Any], response)
