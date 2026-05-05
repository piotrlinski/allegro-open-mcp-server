# ruff: noqa
"""Generated MCP tools — DO NOT EDIT.

Run ``make gen-tools`` to regenerate from the cached OpenAPI spec.
Tag: Post Purchase Issues
"""

from __future__ import annotations

from typing import Any, cast

from ..errors import ErrorResponse
from ._decorators import requires_writes_enabled
from ._runtime import allegro_call, get_client, mcp


@mcp.tool
@allegro_call
def get_list_of_issues(
    *,
    checkoutForm_id: str | None = None,
    limit: int | None = None,
    offset: int | None = None,
    status: list[str] | None = None,
) -> dict[str, Any] | ErrorResponse:
    """Get the user's post purchase issues

    Use this resource to get the list of your disputes and claims ordered by descending opened date. Read more: <a href="../../tutorials/jak-zarzadzac-dyskusjami-E7Zj6gK7ysE#lista-dyskusji-i-reklamacji-na-koncie" target="_blank">PL</a> / <a href="../../tutorials/how-to-manage-discussions-VL6Yr40e5t5#all-disputes-and-claims" target="_blank">EN</a>.


    HTTP: ``GET /sale/issues``
    """
    params = {
        "checkoutForm.id": checkoutForm_id,
        "limit": limit,
        "offset": offset,
        "status": status,
    }
    response = get_client().request_json(
        "GET",
        f"/sale/issues",
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
def get_issue(*, issueId: str) -> dict[str, Any] | ErrorResponse:
    """Get a single dispute or claim

    Use this resource to get a single dispute or claim. Read more: <a href="../../tutorials/jak-zarzadzac-dyskusjami-E7Zj6gK7ysE#szczegolowe-informacje-o-dyskusji-reklamacji" target="_blank">PL</a> / <a href="../../tutorials/how-to-manage-discussions-VL6Yr40e5t5#detailed-information-about-the-dispute-claim" target="_blank">EN</a>.


    HTTP: ``GET /sale/issues/{issueId}``
    """
    params: dict[str, Any] = {}
    response = get_client().request_json(
        "GET",
        f"/sale/issues/{issueId}",
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
def get_chat_from_issue(
    *, issueId: str, limit: int | None = None, offset: int | None = None
) -> dict[str, Any] | ErrorResponse:
    """Get the messages and state claim changes within a post purchase issue

    Use this resource to get the list of messages and state changes within a dispute or claim. Read more: <a href="../../tutorials/jak-zarzadzac-dyskusjami-E7Zj6gK7ysE#wiadomosci-z-dyskusji-i-reklamacji" target="_blank">PL</a> / <a href="../../tutorials/how-to-manage-discussions-VL6Yr40e5t5#disputes-and-claims-messages" target="_blank">EN</a>.


    HTTP: ``GET /sale/issues/{issueId}/chat``
    """
    params = {
        "limit": limit,
        "offset": offset,
    }
    response = get_client().request_json(
        "GET",
        f"/sale/issues/{issueId}/chat",
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
@requires_writes_enabled
def add_message_to_issue(
    *, issueId: str, body: dict[str, Any] | None = None
) -> dict[str, Any] | ErrorResponse:
    """Add a message to an issue

    Use this resource to post a message in certain issue. At least one of fields: 'text', 'attachment' has to be present. Read more: <a href="../../tutorials/jak-zarzadzac-dyskusjami-E7Zj6gK7ysE#nowa-wiadomosc-w-dyskusji-lub-reklamacji" target="_blank">PL</a> / <a href="../../tutorials/how-to-manage-discussions-VL6Yr40e5t5#new-message-in-dispute-or-claim" target="_blank">EN</a>.


    HTTP: ``POST /sale/issues/{issueId}/message``
    """
    params: dict[str, Any] = {}
    response = get_client().request_json(
        "POST",
        f"/sale/issues/{issueId}/message",
        json=body,
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
@requires_writes_enabled
def change_status_of_issue(
    *, issueId: str, body: dict[str, Any] | None = None
) -> dict[str, Any] | ErrorResponse:
    """Change status of a claim

    Change the formal status of a claim, for example accept or reject it. Not a valid operation for disputes. Read more: <a href="../../tutorials/jak-zarzadzac-dyskusjami-E7Zj6gK7ysE#zmien-status-reklamacji" target="_blank">PL</a> / <a href="../../tutorials/how-to-manage-discussions-VL6Yr40e5t5#change-claim-status" target="_blank">EN</a>.


    HTTP: ``POST /sale/issues/{issueId}/status``
    """
    params: dict[str, Any] = {}
    response = get_client().request_json(
        "POST",
        f"/sale/issues/{issueId}/status",
        json=body,
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
@requires_writes_enabled
def create_an_issue_attachment(
    *, body: dict[str, Any] | None = None
) -> dict[str, Any] | ErrorResponse:
    """Create an attachment declaration

    Use this resource to post an attachment declaration. Read more: <a href="../../tutorials/jak-zarzadzac-dyskusjami-E7Zj6gK7ysE#deklaracja-zalacznika" target="_blank">PL</a> / <a href="../../tutorials/how-to-manage-discussions-VL6Yr40e5t5#attachment-declaration" target="_blank">EN</a>.


    HTTP: ``POST /sale/issues/attachments``
    """
    params: dict[str, Any] = {}
    response = get_client().request_json(
        "POST",
        f"/sale/issues/attachments",
        json=body,
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
@requires_writes_enabled
def upload_issue_attachment(
    *, attachmentId: str, body: dict[str, Any] | None = None
) -> dict[str, Any] | ErrorResponse:
    """Upload an attachment

    Upload a post purchase issue message attachment. This operation should be used after creating an attachment declaration with *POST /sale/issues/attachments* **Important!** You can find the URL address to upload the file to our server in the *Location* response header of *POST /sale/issues/attachments*. The URL is unique and one-time. As its format may change in time, you should always use the address from the header. Do not compose the address on your own. Read more: <a href="../../tutorials/jak-zarzadzac-dyskusjami-E7Zj6gK7ysE#dodanie-zalacznika" target="_blank">PL</a> / <a href="../../tutorials/how-to-manage-discussions-VL6Yr40e5t5#adding-an-attachment" target="_blank">EN</a>.


    HTTP: ``PUT /sale/issues/attachments/{attachmentId}``
    """
    params: dict[str, Any] = {}
    response = get_client().request_json(
        "PUT",
        f"/sale/issues/attachments/{attachmentId}",
        json=body,
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
def get_issue_attachment(*, attachmentId: str) -> dict[str, Any] | ErrorResponse:
    """Get an attachment

    Use this resource to get an attachment. Read more: <a href="../../tutorials/jak-zarzadzac-dyskusjami-E7Zj6gK7ysE#pobranie-zalacznika" target="_blank">PL</a> / <a href="../../tutorials/how-to-manage-discussions-VL6Yr40e5t5#attachment-related-to-dispute-claim" target="_blank">EN</a>.


    HTTP: ``GET /sale/issues/attachments/{attachmentId}``
    """
    params: dict[str, Any] = {}
    response = get_client().request_json(
        "GET",
        f"/sale/issues/attachments/{attachmentId}",
        params=params,
    )
    return cast(dict[str, Any], response)
