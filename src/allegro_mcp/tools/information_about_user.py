# ruff: noqa
"""Generated MCP tools — DO NOT EDIT.

Run ``make gen-tools`` to regenerate from the cached OpenAPI spec.
Tag: Information about user
"""

from __future__ import annotations

from typing import Any, cast

from ..errors import ErrorResponse
from ._decorators import requires_writes_enabled
from ._runtime import allegro_call, get_client, mcp


@mcp.tool
@allegro_call
def get_user_ratings(
    *,
    recommended: str | None = None,
    lastChangedAt_gte: str | None = None,
    lastChangedAt_lte: str | None = None,
    offset: int | None = None,
    limit: int | None = None,
) -> dict[str, Any] | ErrorResponse:
    """Get the user's ratings

    Use this resource to receive your sales ratings sorted by last change date, starting from the latest. Read more: <a href="../../tutorials/jak-zarzadzac-kontem-danymi-uzytkownika-ZM9YAKgPgi2#jak-pobrac-informacje-o-ocenie-sprzedazy" target="_blank">PL</a> / <a href="../../tutorials/account-and-user-data-management-jn9vBjqjnsw#how-to-retrieve-user-s-ratings-data" target="_blank">EN</a>.


    HTTP: ``GET /sale/user-ratings``
    """
    params = {
        "recommended": recommended,
        "lastChangedAt.gte": lastChangedAt_gte,
        "lastChangedAt.lte": lastChangedAt_lte,
        "offset": offset,
        "limit": limit,
    }
    response = get_client().request_json(
        "GET",
        f"/sale/user-ratings",
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
def get_user_rating(*, ratingId: str) -> dict[str, Any] | ErrorResponse:
    """Get the user's rating by given rating id

    Use this resource to receive your sales rating by given rating id. Read more: <a href="../../tutorials/jak-zarzadzac-kontem-danymi-uzytkownika-ZM9YAKgPgi2#jak-pobrac-informacje-o-ocenie-sprzedazy" target="_blank">PL</a> / <a href="../../tutorials/account-and-user-data-management-jn9vBjqjnsw#how-to-retrieve-user-s-ratings-data" target="_blank">EN</a>.


    HTTP: ``GET /sale/user-ratings/{ratingId}``
    """
    params: dict[str, Any] = {}
    response = get_client().request_json(
        "GET",
        f"/sale/user-ratings/{ratingId}",
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
@requires_writes_enabled
def answer_user_rating(
    *, ratingId: str, body: dict[str, Any] | None = None
) -> dict[str, Any] | ErrorResponse:
    """Answer for user's rating

    Use this resource to answer for received rating. Read more: <a href="../../tutorials/jak-zarzadzac-kontem-danymi-uzytkownika-ZM9YAKgPgi2#jak-dodac-odpowiedz-na-ocene" target="_blank">PL</a> / <a href="../../tutorials/account-and-user-data-management-jn9vBjqjnsw#how-to-answer-for-user-rating" target="_blank">EN</a>.


    HTTP: ``PUT /sale/user-ratings/{ratingId}/answer``
    """
    params: dict[str, Any] = {}
    response = get_client().request_json(
        "PUT",
        f"/sale/user-ratings/{ratingId}/answer",
        json=body,
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
@requires_writes_enabled
def user_rating_removal(
    *, ratingId: str, body: dict[str, Any] | None = None
) -> dict[str, Any] | ErrorResponse:
    """Request removal of user's rating

    Use this resource to request removal of received rating. Read more: <a href="../../tutorials/jak-zarzadzac-kontem-danymi-uzytkownika-ZM9YAKgPgi2#jak-wyslac-prosbe-o-usuniecie-oceny" target="_blank">PL</a> / <a href="../../tutorials/account-and-user-data-management-jn9vBjqjnsw#how-to-send-a-request-to-remove-user-rating" target="_blank">EN</a>.


    HTTP: ``PUT /sale/user-ratings/{ratingId}/removal``
    """
    params: dict[str, Any] = {}
    response = get_client().request_json(
        "PUT",
        f"/sale/user-ratings/{ratingId}/removal",
        json=body,
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
def get_sale_quality() -> dict[str, Any] | ErrorResponse:
    """Get sales quality

    Use this resource to get current sales quality with at most 30 days history. Read more: <a href="../../tutorials/jak-zarzadzac-kontem-danymi-uzytkownika-ZM9YAKgPgi2#jakosc-sprzedazy" target="_blank">PL</a> / <a href="../../tutorials/account-and-user-data-management-jn9vBjqjnsw#sales-quality" target="_blank">EN</a>.


    HTTP: ``GET /sale/quality``
    """
    params: dict[str, Any] = {}
    response = get_client().request_json(
        "GET",
        f"/sale/quality",
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
def me_get() -> dict[str, Any] | ErrorResponse:
    """Get basic information about user

    Use this resource when you need basic information about authenticated user. Read more: <a href="../../tutorials/jak-zarzadzac-kontem-danymi-uzytkownika-ZM9YAKgPgi2#informacje-o-uzytkowniku" target="_blank">PL</a> / <a href="../../tutorials/account-and-user-data-management-jn9vBjqjnsw#information-about-user" target="_blank">EN</a>.


    HTTP: ``GET /me``
    """
    params: dict[str, Any] = {}
    response = get_client().request_json(
        "GET",
        f"/me",
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
def get_list_of_additional_emails() -> dict[str, Any] | ErrorResponse:
    """Get user's additional emails

    Use this resource to get a list of all additional email addresses assigned to account. Read more: <a href="../../tutorials/jak-zarzadzac-kontem-danymi-uzytkownika-ZM9YAKgPgi2#jak-pobrac-adresy-e-mail" target="_blank">PL</a> / <a href="../../tutorials/account-and-user-data-management-jn9vBjqjnsw#how-to-retrieve-email-addresses" target="_blank">EN</a>.


    HTTP: ``GET /account/additional-emails``
    """
    params: dict[str, Any] = {}
    response = get_client().request_json(
        "GET",
        f"/account/additional-emails",
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
@requires_writes_enabled
def add_additional_email(*, body: dict[str, Any] | None = None) -> dict[str, Any] | ErrorResponse:
    """Add a new additional email address to user's account

    Use this resource to add a new additional email address to account. Read more: <a href="../../tutorials/jak-zarzadzac-kontem-danymi-uzytkownika-ZM9YAKgPgi2#jak-dodac-adres-e-mail" target="_blank">PL</a> / <a href="../../tutorials/account-and-user-data-management-jn9vBjqjnsw#how-to-add-an-additional-email" target="_blank">EN</a>.


    HTTP: ``POST /account/additional-emails``
    """
    params: dict[str, Any] = {}
    response = get_client().request_json(
        "POST",
        f"/account/additional-emails",
        json=body,
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
def get_additional_email(*, emailId: str) -> dict[str, Any] | ErrorResponse:
    """Get information about a particular additional email

    Use this resource to retrieve a single additional email. Read more: <a href="../../tutorials/jak-zarzadzac-kontem-danymi-uzytkownika-ZM9YAKgPgi2#jak-pobrac-szczegolowe-informacje-o-adresie-e-mail" target="_blank">PL</a> / <a href="../../tutorials/account-and-user-data-management-jn9vBjqjnsw#how-to-retrieve-e-mail-details" target="_blank">EN</a>.


    HTTP: ``GET /account/additional-emails/{emailId}``
    """
    params: dict[str, Any] = {}
    response = get_client().request_json(
        "GET",
        f"/account/additional-emails/{emailId}",
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
@requires_writes_enabled
def delete_additional_email(*, emailId: str) -> dict[str, Any] | ErrorResponse:
    """Delete an additional email address

    Use this resource to delete one of additional emails. Read more: <a href="../../tutorials/jak-zarzadzac-kontem-danymi-uzytkownika-ZM9YAKgPgi2#jak-usunac-adres-e-mail" target="_blank">PL</a> / <a href="../../tutorials/account-and-user-data-management-jn9vBjqjnsw#how-to-remove-e-mail" target="_blank">EN</a>.


    HTTP: ``DELETE /account/additional-emails/{emailId}``
    """
    params: dict[str, Any] = {}
    response = get_client().request_json(
        "DELETE",
        f"/account/additional-emails/{emailId}",
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
def get_seller_smart_classification_get(
    *, marketplaceId: str | None = None
) -> dict[str, Any] | ErrorResponse:
    """Get Smart! seller classification report

    Use this resource to get a full Smart! seller classification report. Read more: <a href="../../tutorials/jak-zarzadzac-kontem-danymi-uzytkownika-ZM9YAKgPgi2#kwalifikacja-sprzedawcy" target="_blank">PL</a> / <a href="../../tutorials/account-and-user-data-management-jn9vBjqjnsw#seller-qualification" target="_blank">EN</a>.


    HTTP: ``GET /sale/smart``
    """
    params = {
        "marketplaceId": marketplaceId,
    }
    response = get_client().request_json(
        "GET",
        f"/sale/smart",
        params=params,
    )
    return cast(dict[str, Any], response)
