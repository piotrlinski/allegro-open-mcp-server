# ruff: noqa
"""Generated MCP tools — DO NOT EDIT.

Run ``make gen-tools`` to regenerate from the cached OpenAPI spec.
Tag: Message Center
"""

from __future__ import annotations

from typing import Any, cast

from ..errors import ErrorResponse
from ._decorators import requires_writes_enabled
from ._runtime import allegro_call, get_client, mcp


@mcp.tool
@allegro_call
def list_threads_get(
    *, limit: int | None = None, offset: int | None = None
) -> dict[str, Any] | ErrorResponse:
    """List user threads

    Use this resource to get the list of user threads sorted by last message date, starting from newest. Read more: <a href="../../tutorials/jak-zarzadzac-centrum-wiadomosci-XxWm2K890Fk#lista-watkow-na-koncie" target="_blank">PL</a> / <a href="../../tutorials/how-to-manage-the-message-center-g05avyGlZUW#list-of-threads" target="_blank">EN</a>.


    HTTP: ``GET /messaging/threads``
    """
    params = {
        "limit": limit,
        "offset": offset,
    }
    response = get_client().request_json(
        "GET",
        f"/messaging/threads",
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
def get_thread_get(*, threadId: str) -> dict[str, Any] | ErrorResponse:
    """Get user thread

    Use this resource to get thread with provided identifier. Read more: <a href="../../tutorials/jak-zarzadzac-centrum-wiadomosci-XxWm2K890Fk#szczegolowe-informacje-o-danym-watku" target="_blank">PL</a> / <a href="../../tutorials/how-to-manage-the-message-center-g05avyGlZUW#information-about-a-particular-thread" target="_blank">EN</a>.


    HTTP: ``GET /messaging/threads/{threadId}``
    """
    params: dict[str, Any] = {}
    response = get_client().request_json(
        "GET",
        f"/messaging/threads/{threadId}",
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
@requires_writes_enabled
def change_read_flag_on_thread_put(
    *, threadId: str, body: dict[str, Any] | None = None
) -> dict[str, Any] | ErrorResponse:
    """Mark a particular thread as read

    Use this resource to mark thread with provided identifier as read. Read more: <a href="../../tutorials/jak-zarzadzac-centrum-wiadomosci-XxWm2K890Fk#szczegolowe-informacje-o-wiadomosci" target="_blank">PL</a> / <a href="../../tutorials/how-to-manage-the-message-center-g05avyGlZUW#information-about-a-particular-message" target="_blank">EN</a>.


    HTTP: ``PUT /messaging/threads/{threadId}/read``
    """
    params: dict[str, Any] = {}
    response = get_client().request_json(
        "PUT",
        f"/messaging/threads/{threadId}/read",
        json=body,
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
@requires_writes_enabled
def new_message_post(*, body: dict[str, Any] | None = None) -> dict[str, Any] | ErrorResponse:
    """Write a new message

    Use this resource to write new message to recipient. This resource is rate limited to 1 request per second for a user. Read more: <a href="../../tutorials/jak-zarzadzac-centrum-wiadomosci-XxWm2K890Fk#nowa-wiadomosc" target="_blank">PL</a> / <a href="../../tutorials/how-to-manage-the-message-center-g05avyGlZUW#add-a-new-message" target="_blank">EN</a>.


    HTTP: ``POST /messaging/messages``
    """
    params: dict[str, Any] = {}
    response = get_client().request_json(
        "POST",
        f"/messaging/messages",
        json=body,
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
def list_messages_get(
    *,
    threadId: str,
    limit: int | None = None,
    offset: int | None = None,
    before: str | None = None,
    after: str | None = None,
) -> dict[str, Any] | ErrorResponse:
    """List messages in thread

    Use this resource to list messages in thread with provided identifier. Read more: <a href="../../tutorials/jak-zarzadzac-centrum-wiadomosci-XxWm2K890Fk#lista-wiadomosci-dla-wybranego-watku" target="_blank">PL</a> / <a href="../../tutorials/how-to-manage-the-message-center-g05avyGlZUW#list-of-the-messages-for-the-particular-thread" target="_blank">EN</a>.


    HTTP: ``GET /messaging/threads/{threadId}/messages``
    """
    params = {
        "limit": limit,
        "offset": offset,
        "before": before,
        "after": after,
    }
    response = get_client().request_json(
        "GET",
        f"/messaging/threads/{threadId}/messages",
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
@requires_writes_enabled
def new_message_in_thread_post(
    *, threadId: str, body: dict[str, Any] | None = None
) -> dict[str, Any] | ErrorResponse:
    """Write a new message in thread

    Use this resource to write new message in existing thread. This resource is rate limited to 1 request per second for a user. Read more: <a href="../../tutorials/jak-zarzadzac-centrum-wiadomosci-XxWm2K890Fk#nowa-wiadomosc" target="_blank">PL</a> / <a href="../../tutorials/how-to-manage-the-message-center-g05avyGlZUW#add-a-new-message" target="_blank">EN</a>.


    HTTP: ``POST /messaging/threads/{threadId}/messages``
    """
    params: dict[str, Any] = {}
    response = get_client().request_json(
        "POST",
        f"/messaging/threads/{threadId}/messages",
        json=body,
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
def get_message_get(*, messageId: str) -> dict[str, Any] | ErrorResponse:
    """Get single message

    Use this resource to get message with provided identifier. Read more: <a href="../../tutorials/jak-zarzadzac-centrum-wiadomosci-XxWm2K890Fk#szczegolowe-informacje-o-wiadomosci" target="_blank">PL</a> / <a href="../../tutorials/how-to-manage-the-message-center-g05avyGlZUW#information-about-a-particular-message" target="_blank">EN</a>.


    HTTP: ``GET /messaging/messages/{messageId}``
    """
    params: dict[str, Any] = {}
    response = get_client().request_json(
        "GET",
        f"/messaging/messages/{messageId}",
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
@requires_writes_enabled
def delete_message_delete(*, messageId: str) -> dict[str, Any] | ErrorResponse:
    """Delete single message

    Use this resource to delete message with provided identifier. Read more: <a href="../../tutorials/jak-zarzadzac-centrum-wiadomosci-XxWm2K890Fk#usuniecie-wiadomosci" target="_blank">PL</a> / <a href="../../tutorials/how-to-manage-the-message-center-g05avyGlZUW#delete-a-message" target="_blank">EN</a>.


    HTTP: ``DELETE /messaging/messages/{messageId}``
    """
    params: dict[str, Any] = {}
    response = get_client().request_json(
        "DELETE",
        f"/messaging/messages/{messageId}",
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
@requires_writes_enabled
def new_attachment_declaration_post(
    *, body: dict[str, Any] | None = None
) -> dict[str, Any] | ErrorResponse:
    """Add attachment declaration

    Use this resource to add attachment declaration before uploading. Read more: <a href="../../tutorials/jak-zarzadzac-centrum-wiadomosci-XxWm2K890Fk#deklaracja-zalacznika" target="_blank">PL</a> / <a href="../../tutorials/how-to-manage-the-message-center-g05avyGlZUW#attachment-declaration" target="_blank">EN</a>.


    HTTP: ``POST /messaging/message-attachments``
    """
    params: dict[str, Any] = {}
    response = get_client().request_json(
        "POST",
        f"/messaging/message-attachments",
        json=body,
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
@requires_writes_enabled
def upload_attachment_put(
    *, attachmentId: str, body: dict[str, Any] | None = None
) -> dict[str, Any] | ErrorResponse:
    """Upload attachment binary data

    Use this resource to upload attachment using identifier that was declared. Read more: <a href="../../tutorials/jak-zarzadzac-centrum-wiadomosci-XxWm2K890Fk#dodanie-zalacznika" target="_blank">PL</a> / <a href="../../tutorials/how-to-manage-the-message-center-g05avyGlZUW#add-an-attachment" target="_blank">EN</a>.


    HTTP: ``PUT /messaging/message-attachments/{attachmentId}``
    """
    params: dict[str, Any] = {}
    response = get_client().request_json(
        "PUT",
        f"/messaging/message-attachments/{attachmentId}",
        json=body,
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
def download_attachment_get(*, attachmentId: str) -> dict[str, Any] | ErrorResponse:
    """Download attachment

    Use this resource to download attachment with provided identifier. You can retrieve attachments uploaded within the last 6 months. Read more: <a href="../../tutorials/jak-zarzadzac-centrum-wiadomosci-XxWm2K890Fk#pobranie-zalacznika" target="_blank">PL</a> / <a href="../../tutorials/how-to-manage-the-message-center-g05avyGlZUW#attachment-related-to-the-message" target="_blank">EN</a>.


    HTTP: ``GET /messaging/message-attachments/{attachmentId}``
    """
    params: dict[str, Any] = {}
    response = get_client().request_json(
        "GET",
        f"/messaging/message-attachments/{attachmentId}",
        params=params,
    )
    return cast(dict[str, Any], response)
