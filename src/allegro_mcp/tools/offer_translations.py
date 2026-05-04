# ruff: noqa
"""Generated MCP tools — DO NOT EDIT.

Run ``make gen-tools`` to regenerate from the cached OpenAPI spec.
Tag: Offer translations
"""

from __future__ import annotations

from typing import Any, cast

from ..errors import ErrorResponse
from ._decorators import requires_writes_enabled
from ._runtime import allegro_call, get_client, mcp


@mcp.tool
@allegro_call
def get_offer_translation_using_get(
    *, offerId: str, language: str | None = None
) -> dict[str, Any] | ErrorResponse:
    """Get offer translations

    Get offer translation for given language or all present. Read more: <a href="../../tutorials/jak-zarzadzac-ofertami-7GzB2L37ase#tlumaczenia-ofert" target="_blank">PL</a> / <a href="../../tutorials/how-to-process-list-of-offers-m09BKA5v8H3#offer-translations" target="_blank">EN</a>.


    HTTP: ``GET /sale/offers/{offerId}/translations``
    """
    params = {
        "language": language,
    }
    response = get_client().request_json(
        "GET",
        f"/sale/offers/{offerId}/translations",
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
@requires_writes_enabled
def update_offer_translation_using_patch(
    *, language: str, offerId: str, body: dict[str, Any] | None = None
) -> dict[str, Any] | ErrorResponse:
    """Update offer translation

    Update manual translation for offer. Read more: <a href="../../tutorials/jak-zarzadzac-ofertami-7GzB2L37ase#tlumaczenia-ofert" target="_blank">PL</a> / <a href="../../tutorials/how-to-process-list-of-offers-m09BKA5v8H3#offer-translations" target="_blank">EN</a>.


    HTTP: ``PATCH /sale/offers/{offerId}/translations/{language}``
    """
    params: dict[str, Any] = {}
    response = get_client().request_json(
        "PATCH",
        f"/sale/offers/{offerId}/translations/{language}",
        json=body,
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
@requires_writes_enabled
def delete_manual_translation_using_delete(
    *, language: str, offerId: str, element: str | None = None, products_id: str | None = None
) -> dict[str, Any] | ErrorResponse:
    """Delete offer translation

    Delete single element or entire manual translation. Read more: <a href="../../tutorials/jak-zarzadzac-ofertami-7GzB2L37ase#tlumaczenia-ofert" target="_blank">PL</a> / <a href="../../tutorials/how-to-process-list-of-offers-m09BKA5v8H3#offer-translations" target="_blank">EN</a>.


    HTTP: ``DELETE /sale/offers/{offerId}/translations/{language}``
    """
    params = {
        "element": element,
        "products.id": products_id,
    }
    response = get_client().request_json(
        "DELETE",
        f"/sale/offers/{offerId}/translations/{language}",
        params=params,
    )
    return cast(dict[str, Any], response)
