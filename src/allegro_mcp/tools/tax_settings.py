# ruff: noqa
"""Generated MCP tools — DO NOT EDIT.

Run ``make gen-tools`` to regenerate from the cached OpenAPI spec.
Tag: Tax settings
"""

from __future__ import annotations

from typing import Any, cast

from ..errors import ErrorResponse
from ._decorators import requires_writes_enabled
from ._runtime import allegro_call, get_client, mcp


@mcp.tool
@allegro_call
def get_tax_settings_for_category(
    *, category_id: str | None = None, countryCode: list[str] | None = None
) -> dict[str, Any] | ErrorResponse:
    """Get all tax settings for category

    Use this resource to receive tax settings for given category. Based on received settings you may set VAT tax settings for your offers. Read more: <a href="../../tutorials/jak-jednym-requestem-wystawic-oferte-powiazana-z-produktem-D7Kj9gw4xFA#opcje-faktury-i-stawki-vat" target="_blank">PL</a> / <a href="../../tutorials/list-offer-assigned-product-one-request-D7Kj9M71Bu6#invoice-and-vat-settings" target="_blank">EN</a>.


    HTTP: ``GET /sale/tax-settings``
    """
    params = {
        "category.id": category_id,
        "countryCode": countryCode,
    }
    response = get_client().request_json(
        "GET",
        f"/sale/tax-settings",
        params=params,
    )
    return cast(dict[str, Any], response)
