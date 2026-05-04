# ruff: noqa
"""Generated MCP tools — DO NOT EDIT.

Run ``make gen-tools`` to regenerate from the cached OpenAPI spec.
Tag: Products
"""

from __future__ import annotations

from typing import Any, cast

from ..errors import ErrorResponse
from ._decorators import requires_writes_enabled
from ._runtime import allegro_call, get_client, mcp


@mcp.tool
@allegro_call
def get_flat_product_parameters_using_get(*, categoryId: str) -> dict[str, Any] | ErrorResponse:
    """Get product parameters available in given category

    Use this resource to get the list of product parameters available in given category. You can use these parameters to create a new product. Read more: <a href="../../tutorials/jak-jednym-requestem-wystawic-oferte-powiazana-z-produktem-D7Kj9gw4xFA#jak-utworzyc-nowy-produkt" target="_blank">PL</a> / <a href="../../tutorials/list-offer-assigned-product-one-request-D7Kj9M71Bu6#how-to-create-a-product" target="_blank">EN</a>.


    HTTP: ``GET /sale/categories/{categoryId}/product-parameters``
    """
    params: dict[str, Any] = {}
    response = get_client().request_json(
        "GET",
        f"/sale/categories/{categoryId}/product-parameters",
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
def get_sale_products(
    *,
    phrase: str | None = None,
    mode: str | None = None,
    language: str | None = None,
    category_id: str | None = None,
    Dynamic_filters: str | None = None,
    page_id: str | None = None,
    searchFeatures: str | None = None,
) -> dict[str, Any] | ErrorResponse:
    """Get search products results

    Use this resource to get a list of products according to provided parameters. At least ean or phrase parameter is required. Read more: <a href="../../tutorials/jak-jednym-requestem-wystawic-oferte-powiazana-z-produktem-D7Kj9gw4xFA#jak-znalezc-produkt" target="_blank">PL</a> / <a href="../../tutorials/list-offer-assigned-product-one-request-D7Kj9M71Bu6#how-to-find-a-product" target="_blank">EN</a>. This resource is limited with Leaky Bucket mechanism, read more <a href="../../tutorials/informacje-podstawowe-b21569boAI1#ograniczenie-liczby-zapytan-limity" target="_blank">PL</a> / <a href="../../tutorials/basic-information-VL6YelvVKTn#limiting-the-number-of-queries-limits" target="_blank">EN</a>.


    HTTP: ``GET /sale/products``
    """
    params = {
        "phrase": phrase,
        "mode": mode,
        "language": language,
        "category.id": category_id,
        "Dynamic filters": Dynamic_filters,
        "page.id": page_id,
        "searchFeatures": searchFeatures,
    }
    response = get_client().request_json(
        "GET",
        f"/sale/products",
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
def get_sale_product(
    *, productId: str, category_id: str | None = None, language: str | None = None
) -> dict[str, Any] | ErrorResponse:
    """Get all data of the particular product

    Use this resource to retrieve all data of the particular product. Read more: <a href="../../tutorials/jak-jednym-requestem-wystawic-oferte-powiazana-z-produktem-D7Kj9gw4xFA#jak-pobrac-pelne-dane-o-produkcie" target="_blank">PL</a> / <a href="../../tutorials/list-offer-assigned-product-one-request-D7Kj9M71Bu6#how-to-retrieve-product-data" target="_blank">EN</a>. This resource is limited with <a href="../../tutorials/basic-information-VL6YelvVKTn#limiting-the-number-of-queries-limits" target="_blank">Leaky Bucket</a> mechanism.


    HTTP: ``GET /sale/products/{productId}``
    """
    params = {
        "category.id": category_id,
        "language": language,
    }
    response = get_client().request_json(
        "GET",
        f"/sale/products/{productId}",
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
@requires_writes_enabled
def propose_sale_product(*, body: dict[str, Any] | None = None) -> dict[str, Any] | ErrorResponse:
    """Propose a product

    Use this resource to propose a product. You can add up to 20,000 new products to the Catalog each month. Read more: <a href="../../tutorials/jak-jednym-requestem-wystawic-oferte-powiazana-z-produktem-D7Kj9gw4xFA#jak-utworzyc-nowy-produkt" target="_blank">PL</a> / <a href="../../tutorials/list-offer-assigned-product-one-request-D7Kj9M71Bu6#how-to-create-a-product" target="_blank">EN</a>.


    HTTP: ``POST /sale/product-proposals``
    """
    params: dict[str, Any] = {}
    response = get_client().request_json(
        "POST",
        f"/sale/product-proposals",
        json=body,
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
@requires_writes_enabled
def product_change_proposal(
    *, productId: str, body: dict[str, Any] | None = None
) -> dict[str, Any] | ErrorResponse:
    """Propose changes in product

    Use this resource to propose changes in product. Read more: <a href="../../tutorials/jak-jednym-requestem-wystawic-oferte-powiazana-z-produktem-D7Kj9gw4xFA#jak-zglosic-blad-w-produkcie" target="_blank">PL</a> / <a href="../../tutorials/list-offer-assigned-product-one-request-D7Kj9M71Bu6#how-to-report-incorrect-data-in-a-product" target="_blank">EN</a>. This resource is limited to 100 suggestions per day for a single user.


    HTTP: ``POST /sale/products/{productId}/change-proposals``
    """
    params: dict[str, Any] = {}
    response = get_client().request_json(
        "POST",
        f"/sale/products/{productId}/change-proposals",
        json=body,
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
def get_product_change_proposal(*, changeProposalId: str) -> dict[str, Any] | ErrorResponse:
    """Get all data of the particular product changes proposal

    Use this resource to retrieve all data of the particular product changes proposal. Read more: <a href="../../tutorials/jak-jednym-requestem-wystawic-oferte-powiazana-z-produktem-D7Kj9gw4xFA#jak-zglosic-blad-w-produkcie" target="_blank">PL</a> / <a href="../../tutorials/list-offer-assigned-product-one-request-D7Kj9M71Bu6#how-to-report-incorrect-data-in-a-product" target="_blank">EN</a>.


    HTTP: ``GET /sale/products/change-proposals/{changeProposalId}``
    """
    params: dict[str, Any] = {}
    response = get_client().request_json(
        "GET",
        f"/sale/products/change-proposals/{changeProposalId}",
        params=params,
    )
    return cast(dict[str, Any], response)
