# ruff: noqa
"""Generated MCP tools — DO NOT EDIT.

Run ``make gen-tools`` to regenerate from the cached OpenAPI spec.
Tag: Compatibility List
"""

from __future__ import annotations

from typing import Any, cast

from ..errors import ErrorResponse
from ._decorators import requires_writes_enabled
from ._runtime import allegro_call, get_client, mcp


@mcp.tool
@allegro_call
def get_categories_that_support_compatibility_list() -> dict[str, Any] | ErrorResponse:
    """Get list of categories where compatibility list is supported

    Compatibility list is available in particular categories, this resource allows to get the list of these categories with additional details. Read more: <a href="../../tutorials/jak-zarzadzac-sekcja-pasuje-do-E7Zj6gAEGil#jak-sprawdzic-czy-w-danej-kategorii-moge-dodac-sekcje-pasuje-do-do-oferty" target="_blank">PL</a> / <a href="../../tutorials/how-to-manage-the-compatibility-section-v8WbL1wV0Hz#which-categories-support-compatibility-section" target="_blank">EN</a>.


    HTTP: ``GET /sale/compatibility-list/supported-categories``
    """
    params: dict[str, Any] = {}
    response = get_client().request_json(
        "GET",
        f"/sale/compatibility-list/supported-categories",
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
def get_compatibility_list_suggestion(
    *, offer_id: str | None = None, product_id: str | None = None, language: str | None = None
) -> dict[str, Any] | ErrorResponse:
    """Get suggested compatibility list.

    Resource allows to fetch compatibility list suggestion for given offer or product. Read more: <a href="../../tutorials/jak-zarzadzac-sekcja-pasuje-do-E7Zj6gAEGil#jak-wyszukac-sugerowana-sekcje-compatibilitylist" target="_blank">PL</a> / <a href="../../tutorials/how-to-manage-the-compatibility-section-v8WbL1wV0Hz#how-to-search-for-the-suggested-compatibility-section" target="_blank">EN</a>.


    HTTP: ``GET /sale/compatibility-list-suggestions``
    """
    params = {
        "offer.id": offer_id,
        "product.id": product_id,
        "language": language,
    }
    response = get_client().request_json(
        "GET",
        f"/sale/compatibility-list-suggestions",
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
def get_compatible_products_groups(
    *, type_: str | None = None, limit: int | None = None, offset: int | None = None
) -> dict[str, Any] | ErrorResponse:
    """Get list of compatible product groups

    Compatible products are organized in groups, this resource allows to browse these groups. Read more: <a href="../../tutorials/jak-zarzadzac-sekcja-pasuje-do-E7Zj6gAEGil#jak-zarzadzac-sekcja-pasuje-do-zintegrowana-z-baza-pojazdow" target="_blank">PL</a> / <a href="../../tutorials/how-to-manage-the-compatibility-section-v8WbL1wV0Hz#managing-the-compatibility-section-compatibilitylist-integrated-vehicle-database" target="_blank">EN</a>.


    HTTP: ``GET /sale/compatible-products/groups``
    """
    params = {
        "type": type_,
        "limit": limit,
        "offset": offset,
    }
    response = get_client().request_json(
        "GET",
        f"/sale/compatible-products/groups",
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
def get_compatible_products(
    *,
    type_: str | None = None,
    group_id: str | None = None,
    tecdoc_kTypNr: str | None = None,
    tecdoc_nTypNr: str | None = None,
    phrase: str | None = None,
    limit: int | None = None,
    offset: int | None = None,
) -> dict[str, Any] | ErrorResponse:
    """Get list of compatible products

    Resource allows to fetch compatible products of given type. Read more: <a href="../../tutorials/jak-zarzadzac-sekcja-pasuje-do-E7Zj6gAEGil#jak-zarzadzac-sekcja-pasuje-do-zintegrowana-z-baza-pojazdow" target="_blank">PL</a> / <a href="../../tutorials/how-to-manage-the-compatibility-section-v8WbL1wV0Hz#managing-the-compatibility-section-compatibilitylist-integrated-vehicle-database" target="_blank">EN</a>.


    HTTP: ``GET /sale/compatible-products``
    """
    params = {
        "type": type_,
        "group.id": group_id,
        "tecdoc.kTypNr": tecdoc_kTypNr,
        "tecdoc.nTypNr": tecdoc_nTypNr,
        "phrase": phrase,
        "limit": limit,
        "offset": offset,
    }
    response = get_client().request_json(
        "GET",
        f"/sale/compatible-products",
        params=params,
    )
    return cast(dict[str, Any], response)
