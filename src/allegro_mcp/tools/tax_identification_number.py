# ruff: noqa
"""Generated MCP tools — DO NOT EDIT.

Run ``make gen-tools`` to regenerate from the cached OpenAPI spec.
Tag: Tax Identification Number
"""

from __future__ import annotations

from typing import Any, cast

from ..errors import ErrorResponse
from ._decorators import requires_writes_enabled
from ._runtime import allegro_call, get_client, mcp


@mcp.tool
@allegro_call
@requires_writes_enabled
def add_tax_id(*, body: dict[str, Any] | None = None) -> dict[str, Any] | ErrorResponse:
    """Add tax identification number

    Use this resource to add tax identification number. For international sellers only. Read more: <a href="../../news/one-fulfillment-umozliwiamy-zarzadzanie-numerem-identyfikacji-podatkowej-vat-6M2xgdAmGFM" target="_blank">PL</a> / <a href="../../news/one-fulfillment-we-allow-you-to-manage-your-vat-identification-number-Pgj9WXjWwcm" target="_blank">EN</a>.


    HTTP: ``POST /fulfillment/tax-id``
    """
    params: dict[str, Any] = {}
    response = get_client().request_json(
        "POST",
        f"/fulfillment/tax-id",
        json=body,
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
@requires_writes_enabled
def update_tax_id(*, body: dict[str, Any] | None = None) -> dict[str, Any] | ErrorResponse:
    """Update tax identification number

    Use this resource to update tax identification number. For international sellers only. Read more: <a href="../../news/one-fulfillment-umozliwiamy-zarzadzanie-numerem-identyfikacji-podatkowej-vat-6M2xgdAmGFM" target="_blank">PL</a> / <a href="../../news/one-fulfillment-we-allow-you-to-manage-your-vat-identification-number-Pgj9WXjWwcm" target="_blank">EN</a>.


    HTTP: ``PUT /fulfillment/tax-id``
    """
    params: dict[str, Any] = {}
    response = get_client().request_json(
        "PUT",
        f"/fulfillment/tax-id",
        json=body,
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
def get_tax_id() -> dict[str, Any] | ErrorResponse:
    """Get tax identification number

    Use this resource to get tax identification number with verification status. After adding or updating the tax identification number the status will be NOT_VERIFIED and you will have to wait for acceptance status to start selling. Read more: <a href="../../news/one-fulfillment-umozliwiamy-zarzadzanie-numerem-identyfikacji-podatkowej-vat-6M2xgdAmGFM" target="_blank">PL</a> / <a href="../../news/one-fulfillment-we-allow-you-to-manage-your-vat-identification-number-Pgj9WXjWwcm" target="_blank">EN</a>.


    HTTP: ``GET /fulfillment/tax-id``
    """
    params: dict[str, Any] = {}
    response = get_client().request_json(
        "GET",
        f"/fulfillment/tax-id",
        params=params,
    )
    return cast(dict[str, Any], response)
