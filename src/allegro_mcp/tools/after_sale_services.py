# ruff: noqa
"""Generated MCP tools — DO NOT EDIT.

Run ``make gen-tools`` to regenerate from the cached OpenAPI spec.
Tag: After sale services
"""

from __future__ import annotations

from typing import Any, cast

from ..errors import ErrorResponse
from ._decorators import requires_writes_enabled
from ._runtime import allegro_call, get_client, mcp


@mcp.tool
@allegro_call
def get_public_seller_listing_using_get_1(
    *, limit: int | None = None, offset: int | None = None
) -> dict[str, Any] | ErrorResponse:
    """Get the user's return policies

    Use this resource to get the seller's return policies. Read more: <a href="../../tutorials/jak-zarzadzac-ofertami-7GzB2L37ase#jak-pobrac-warunki-zwrotow-przypisane-do-konta" target="_blank">PL</a> / <a href="../../tutorials/how-to-process-list-of-offers-m09BKA5v8H3#how-to-retrieve-return-policies-assigned-to-the-account" target="_blank">EN</a>.


    HTTP: ``GET /after-sales-service-conditions/return-policies``
    """
    params = {
        "limit": limit,
        "offset": offset,
    }
    response = get_client().request_json(
        "GET",
        f"/after-sales-service-conditions/return-policies",
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
@requires_writes_enabled
def create_after_sales_service_return_policy(
    *, body: dict[str, Any] | None = None
) -> dict[str, Any] | ErrorResponse:
    """Create new user's return policy

    Use this resource to create a return policy definition. Read more: <a href="../../tutorials/jak-zarzadzac-ofertami-7GzB2L37ase#jak-dodac-informacje-o-warunkach-zwrotow" target="_blank">PL</a> / <a href="../../tutorials/how-to-process-list-of-offers-m09BKA5v8H3#how-to-add-return-policy-information" target="_blank">EN</a>.


    HTTP: ``POST /after-sales-service-conditions/return-policies``
    """
    params: dict[str, Any] = {}
    response = get_client().request_json(
        "POST",
        f"/after-sales-service-conditions/return-policies",
        json=body,
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
def get_after_sales_service_return_policy(*, returnPolicyId: str) -> dict[str, Any] | ErrorResponse:
    """Get the user's return policy

    Use this resource to get a return policy details. Read more: <a href="../../tutorials/jak-zarzadzac-ofertami-7GzB2L37ase#jak-pobrac-warunki-zwrotow-przypisane-do-konta" target="_blank">PL</a> / <a href="../../tutorials/how-to-process-list-of-offers-m09BKA5v8H3#how-to-retrieve-return-policies-assigned-to-the-account" target="_blank">EN</a>.


    HTTP: ``GET /after-sales-service-conditions/return-policies/{returnPolicyId}``
    """
    params: dict[str, Any] = {}
    response = get_client().request_json(
        "GET",
        f"/after-sales-service-conditions/return-policies/{returnPolicyId}",
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
@requires_writes_enabled
def update_after_sales_service_return_policy(
    *, returnPolicyId: str, body: dict[str, Any] | None = None
) -> dict[str, Any] | ErrorResponse:
    """Change the user's return policy

    Use this resource to modify the return policy details. Read more: <a href="../../tutorials/jak-zarzadzac-ofertami-7GzB2L37ase#jak-edytowac-informacje-o-warunkach-zwrotu" target="_blank">PL</a> / <a href="../../tutorials/how-to-process-list-of-offers-m09BKA5v8H3#how-to-update-return-policy-information" target="_blank">EN</a>.


    HTTP: ``PUT /after-sales-service-conditions/return-policies/{returnPolicyId}``
    """
    params: dict[str, Any] = {}
    response = get_client().request_json(
        "PUT",
        f"/after-sales-service-conditions/return-policies/{returnPolicyId}",
        json=body,
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
@requires_writes_enabled
def delete_after_sales_service_return_policy(
    *, returnPolicyId: str
) -> dict[str, Any] | ErrorResponse:
    """Delete the user's return policy

    Use this resource to delete a return policy definition.


    HTTP: ``DELETE /after-sales-service-conditions/return-policies/{returnPolicyId}``
    """
    params: dict[str, Any] = {}
    response = get_client().request_json(
        "DELETE",
        f"/after-sales-service-conditions/return-policies/{returnPolicyId}",
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
def get_public_seller_listing(
    *, limit: int | None = None, offset: int | None = None
) -> dict[str, Any] | ErrorResponse:
    """Get the user's implied warranties

    Use this resource to get the seller's implied warranties. Read more: <a href="../../tutorials/jak-zarzadzac-ofertami-7GzB2L37ase#jak-pobrac-warunki-reklamacji-przypisane-do-konta" target="_blank">PL</a> / <a href="../../tutorials/how-to-process-list-of-offers-m09BKA5v8H3#how-to-retrieve-implied-warranties-assigned-to-the-account" target="_blank">EN</a>.


    HTTP: ``GET /after-sales-service-conditions/implied-warranties``
    """
    params = {
        "limit": limit,
        "offset": offset,
    }
    response = get_client().request_json(
        "GET",
        f"/after-sales-service-conditions/implied-warranties",
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
@requires_writes_enabled
def create_after_sales_service_implied_warranty(
    *, body: dict[str, Any] | None = None
) -> dict[str, Any] | ErrorResponse:
    """Create new user's implied warranty

    Use this resource to create an implied warranty definition. Read more: <a href="../../tutorials/jak-zarzadzac-ofertami-7GzB2L37ase#jak-dodac-informacje-o-warunkach-reklamacji" target="_blank">PL</a> / <a href="../../tutorials/how-to-process-list-of-offers-m09BKA5v8H3#how-to-add-implied-warranty-information" target="_blank">EN</a>.


    HTTP: ``POST /after-sales-service-conditions/implied-warranties``
    """
    params: dict[str, Any] = {}
    response = get_client().request_json(
        "POST",
        f"/after-sales-service-conditions/implied-warranties",
        json=body,
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
def get_after_sales_service_implied_warranty(
    *, impliedWarrantyId: str
) -> dict[str, Any] | ErrorResponse:
    """Get the user's implied warranty

    Use this resource to get an implied warranty details. Read more: <a href="../../tutorials/jak-zarzadzac-ofertami-7GzB2L37ase#jak-pobrac-warunki-reklamacji-przypisane-do-konta" target="_blank">PL</a> / <a href="../../tutorials/how-to-process-list-of-offers-m09BKA5v8H3#how-to-retrieve-implied-warranties-assigned-to-the-account" target="_blank">EN</a>.


    HTTP: ``GET /after-sales-service-conditions/implied-warranties/{impliedWarrantyId}``
    """
    params: dict[str, Any] = {}
    response = get_client().request_json(
        "GET",
        f"/after-sales-service-conditions/implied-warranties/{impliedWarrantyId}",
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
@requires_writes_enabled
def update_after_sales_service_implied_warranty(
    *, impliedWarrantyId: str, body: dict[str, Any] | None = None
) -> dict[str, Any] | ErrorResponse:
    """Change the user's implied warranty

    Use this resource to modify the implied warranty details. Read more: <a href="../../tutorials/jak-zarzadzac-ofertami-7GzB2L37ase#jak-edytowac-informacje-o-warunkach-reklamacji" target="_blank">PL</a> / <a href="../../tutorials/how-to-process-list-of-offers-m09BKA5v8H3#how-to-update-implied-warranty-information" target="_blank">EN</a>.


    HTTP: ``PUT /after-sales-service-conditions/implied-warranties/{impliedWarrantyId}``
    """
    params: dict[str, Any] = {}
    response = get_client().request_json(
        "PUT",
        f"/after-sales-service-conditions/implied-warranties/{impliedWarrantyId}",
        json=body,
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
def get_public_seller_listing_using_get_2(
    *, limit: int | None = None, offset: int | None = None
) -> dict[str, Any] | ErrorResponse:
    """Get the user's warranties

    Use this resource to get the seller's warranties. Read more: <a href="../../tutorials/jak-zarzadzac-ofertami-7GzB2L37ase#jak-pobrac-informacje-o-gwarancjach-przypisanych-do-konta" target="_blank">PL</a> / <a href="../../tutorials/how-to-process-list-of-offers-m09BKA5v8H3#how-to-retrieve-warranties-assigned-to-the-account" target="_blank">EN</a>.


    HTTP: ``GET /after-sales-service-conditions/warranties``
    """
    params = {
        "limit": limit,
        "offset": offset,
    }
    response = get_client().request_json(
        "GET",
        f"/after-sales-service-conditions/warranties",
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
@requires_writes_enabled
def create_after_sales_service_warranty(
    *, body: dict[str, Any] | None = None
) -> dict[str, Any] | ErrorResponse:
    """Create new user's warranty

    Use this resource to create a warranty definition. Read more: <a href="../../tutorials/jak-zarzadzac-ofertami-7GzB2L37ase#jak-dodac-informacje-o-gwarancjach" target="_blank">PL</a> / <a href="../../tutorials/how-to-process-list-of-offers-m09BKA5v8H3#how-to-add-warranty-information" target="_blank">EN</a>.


    HTTP: ``POST /after-sales-service-conditions/warranties``
    """
    params: dict[str, Any] = {}
    response = get_client().request_json(
        "POST",
        f"/after-sales-service-conditions/warranties",
        json=body,
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
def get_after_sales_service_warranty(*, warrantyId: str) -> dict[str, Any] | ErrorResponse:
    """Get the user's warranty

    Use this resource to get a warranty details. Read more: <a href="../../tutorials/jak-zarzadzac-ofertami-7GzB2L37ase#jak-pobrac-informacje-o-gwarancjach-przypisanych-do-konta" target="_blank">PL</a> / <a href="../../tutorials/how-to-process-list-of-offers-m09BKA5v8H3#how-to-retrieve-warranties-assigned-to-the-account" target="_blank">EN</a>.


    HTTP: ``GET /after-sales-service-conditions/warranties/{warrantyId}``
    """
    params: dict[str, Any] = {}
    response = get_client().request_json(
        "GET",
        f"/after-sales-service-conditions/warranties/{warrantyId}",
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
@requires_writes_enabled
def update_after_sales_service_warranty(
    *, warrantyId: str, body: dict[str, Any] | None = None
) -> dict[str, Any] | ErrorResponse:
    """Change the user's warranty

    Use this resource to modify the warranty details. Read more: <a href="../../tutorials/jak-zarzadzac-ofertami-7GzB2L37ase#jak-edytowac-informacje-o-gwarancjach" target="_blank">PL</a> / <a href="../../tutorials/how-to-process-list-of-offers-m09BKA5v8H3#how-to-update-warranty-information" target="_blank">EN</a>.


    HTTP: ``PUT /after-sales-service-conditions/warranties/{warrantyId}``
    """
    params: dict[str, Any] = {}
    response = get_client().request_json(
        "PUT",
        f"/after-sales-service-conditions/warranties/{warrantyId}",
        json=body,
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
@requires_writes_enabled
def create_after_sales_service_conditions_attachment(
    *, body: dict[str, Any] | None = None
) -> dict[str, Any] | ErrorResponse:
    """Create a warranty attachment metadata

    You can attach PDF files to warranties. Uploading attachments flow: 1. Create an attachment object to receive an upload URL (*POST /after-sales-service-conditions/attachments*), 2. Use the upload URL to submit the PDF file (*PUT /after-sales-service-conditions/attachments/{attachmentId}*), 3. Create (or update) warranty with attachment (*POST /after-sales-service-conditions/warranties*). Read more: <a href="../../tutorials/jak-zarzadzac-ofertami-7GzB2L37ase#jak-dodac-zalacznik-do-informacji-o-gwarancjach" target="_blank">PL</a> / <a href="../../tutorials/how-to-process-list-of-offers-m09BKA5v8H3#how-to-add-attachment-to-warranty-information" target="_blank">EN</a>.


    HTTP: ``POST /after-sales-service-conditions/attachments``
    """
    params: dict[str, Any] = {}
    response = get_client().request_json(
        "POST",
        f"/after-sales-service-conditions/attachments",
        json=body,
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
@requires_writes_enabled
def upload_after_sales_service_conditions_attachment(
    *, attachmentId: str, body: dict[str, Any] | None = None
) -> dict[str, Any] | ErrorResponse:
    """Upload an warranty attachment

    Upload an after sale services attachment. This operation should be used after creating an offer attachment with *POST /sale/offer-attachments* **Important!** You can find the URL address to upload the file to our server in the *Location* response header of *POST /after-sales-service-conditions/attachments*. The URL is unique and one-time. As its format may change in time, you should always use the address from the header. Do not compose the address on your own. Read more: <a href="../../tutorials/jak-zarzadzac-ofertami-7GzB2L37ase#jak-dodac-zalacznik-do-informacji-o-gwarancjach" target="_blank">PL</a> / <a href="../../tutorials/how-to-process-list-of-offers-m09BKA5v8H3#how-to-add-attachment-to-warranty-information" target="_blank">EN</a>.


    HTTP: ``PUT /after-sales-service-conditions/attachments/{attachmentId}``
    """
    params: dict[str, Any] = {}
    response = get_client().request_json(
        "PUT",
        f"/after-sales-service-conditions/attachments/{attachmentId}",
        json=body,
        params=params,
    )
    return cast(dict[str, Any], response)
