# ruff: noqa
"""Generated MCP tools — DO NOT EDIT.

Run ``make gen-tools`` to regenerate from the cached OpenAPI spec.
Tag: Advance Ship Notices
"""

from __future__ import annotations

from typing import Any, cast

from ..errors import ErrorResponse
from ._decorators import requires_writes_enabled
from ._runtime import allegro_call, get_client, mcp


@mcp.tool
@allegro_call
def get_advance_ship_notices(
    *, offset: int | None = None, limit: int | None = None, status: list[str] | None = None
) -> dict[str, Any] | ErrorResponse:
    """Get list of Advance Ship Notices

    Use this resource to get a list of Advance Ship Notices. The list is ordered by **createdAt** property. Default **offset** is 0, default **limit** is 50. A list can be filtered by statuses. Multiple status query parameters are allowed. In such cases, filters are joined with **OR** logical operator. Read more: <a href="../../tutorials/one-fulfillment-by-allegro-0ADwgOLqWSw#jak-przegladac-utworzone-awizo" target="_blank">PL</a> / <a href="../../tutorials/one-fulfillment-by-allegro-4R9dXyMPlc9#how-to-get-created-advance-ship-notices" target="_blank">EN</a>.


    HTTP: ``GET /fulfillment/advance-ship-notices``
    """
    params = {
        "offset": offset,
        "limit": limit,
        "status": status,
    }
    response = get_client().request_json(
        "GET",
        f"/fulfillment/advance-ship-notices",
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
@requires_writes_enabled
def create_advance_ship_notice(
    *, body: dict[str, Any] | None = None
) -> dict[str, Any] | ErrorResponse:
    """Create an Advance Ship Notice

    Use this resource to create an Advance Ship Notice. Read more: <a href="../../tutorials/one-fulfillment-by-allegro-0ADwgOLqWSw#utworz-draft-awizo" target="_blank">PL</a> / <a href="../../tutorials/one-fulfillment-by-allegro-4R9dXyMPlc9#create-a-draft-of-the-advance-ship-notice" target="_blank">EN</a>.


    HTTP: ``POST /fulfillment/advance-ship-notices``
    """
    params: dict[str, Any] = {}
    response = get_client().request_json(
        "POST",
        f"/fulfillment/advance-ship-notices",
        json=body,
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
def get_advance_ship_notice(*, id: str) -> dict[str, Any] | ErrorResponse:
    """Get single Advance Ship Notice

    Use this resource to get an Advance Ship Notice. Read more: <a href="../../tutorials/one-fulfillment-by-allegro-0ADwgOLqWSw#jak-przegladac-utworzone-awizo" target="_blank">PL</a> / <a href="../../tutorials/one-fulfillment-by-allegro-4R9dXyMPlc9#how-to-get-created-advance-ship-notices" target="_blank">EN</a>.


    HTTP: ``GET /fulfillment/advance-ship-notices/{id}``
    """
    params: dict[str, Any] = {}
    response = get_client().request_json(
        "GET",
        f"/fulfillment/advance-ship-notices/{id}",
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
@requires_writes_enabled
def update_advance_ship_notice(
    *, id: str, body: dict[str, Any] | None = None
) -> dict[str, Any] | ErrorResponse:
    """Update Advance Ship Notice

    Use this resource to update an Advance Ship Notice. Any content property update will clear labels property. Use Create labels command to create new labels for provided content. If a client wants to update read-only property, an error is returned (only in cases when sent value will be different than actual on the server). Read more: <a href="../../tutorials/one-fulfillment-by-allegro-0ADwgOLqWSw#uzupelnij-dane-o-awizo" target="_blank">PL</a> / <a href="../../one-fulfillment-by-allegro-4R9dXyMPlc9#complete-the-data-of-advance-ship-notice" target="_blank">EN</a>.


    HTTP: ``PUT /fulfillment/advance-ship-notices/{id}``
    """
    params: dict[str, Any] = {}
    response = get_client().request_json(
        "PUT",
        f"/fulfillment/advance-ship-notices/{id}",
        json=body,
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
@requires_writes_enabled
def delete_advance_ship_notice(*, id: str) -> dict[str, Any] | ErrorResponse:
    """Delete Advance Ship Notice

    Use this resource to delete an Advance Ship Notice. Read more: <a href="../../tutorials/one-fulfillment-by-allegro-0ADwgOLqWSw#jak-usunac-awizo" target="_blank">PL</a> / <a href="../../tutorials/one-fulfillment-by-allegro-4R9dXyMPlc9#how-to-delete-advance-ship-notice" target="_blank">EN</a>.


    HTTP: ``DELETE /fulfillment/advance-ship-notices/{id}``
    """
    params: dict[str, Any] = {}
    response = get_client().request_json(
        "DELETE",
        f"/fulfillment/advance-ship-notices/{id}",
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
@requires_writes_enabled
def cancel_advance_ship_notice(*, id: str) -> dict[str, Any] | ErrorResponse:
    """Cancel Advance Ship Notice

    Use this resource to cancel an Advance Ship Notice in IN_TRANSIT status. Read more: <a href="../../tutorials/one-fulfillment-by-allegro-0ADwgOLqWSw#anuluj-awizo" target="_blank">PL</a> / <a href="../../tutorials/one-fulfillment-by-allegro-4R9dXyMPlc9#cancel-advance-ship-notice" target="_blank">EN</a>.


    HTTP: ``PUT /fulfillment/advance-ship-notices/{id}/cancel``
    """
    params: dict[str, Any] = {}
    response = get_client().request_json(
        "PUT",
        f"/fulfillment/advance-ship-notices/{id}/cancel",
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
def get_advance_ship_notice_labels(*, id: str) -> dict[str, Any] | ErrorResponse:
    """Get labels for Advance Ship Notice

    Use this resource to get labels for Advance Ship Notice after being created with "create labels command". Read more: <a href="../../tutorials/one-fulfillment-by-allegro-0ADwgOLqWSw#wygeneruj-oznaczenia-na-kartony" target="_blank">PL</a> / <a href="../../tutorials/one-fulfillment-by-allegro-4R9dXyMPlc9#create-labels-for-boxes" target="_blank">EN</a>.


    HTTP: ``GET /fulfillment/advance-ship-notices/{id}/labels``
    """
    params: dict[str, Any] = {}
    response = get_client().request_json(
        "GET",
        f"/fulfillment/advance-ship-notices/{id}/labels",
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
@requires_writes_enabled
def submit_command(
    *, command_id: str, body: dict[str, Any] | None = None
) -> dict[str, Any] | ErrorResponse:
    """Submit the Advance Ship Notice

    Use this resource to submit the Advance Ship Notice. After this operation, updates of the Advance Ship Notice are limited to selected properties only. See <a href="../../documentation#operation/updateSubmittedAdvanceShipNotice">PUT /fulfillment/advance-ship-notices/{id}/submitted</a>. Read more: <a href="../../tutorials/one-fulfillment-by-allegro-0ADwgOLqWSw#zakoncz-edycje-i-wyslij-awizo" target="_blank">PL</a> / <a href="../../tutorials/one-fulfillment-by-allegro-4R9dXyMPlc9#finish-editing-and-submit-the-advance-ship-notice" target="_blank">EN</a>.


    HTTP: ``PUT /fulfillment/submit-commands/{command-id}``
    """
    params: dict[str, Any] = {}
    response = get_client().request_json(
        "PUT",
        f"/fulfillment/submit-commands/{command_id}",
        json=body,
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
def get_submit_command(*, command_id: str) -> dict[str, Any] | ErrorResponse:
    """Get submit status

    Use this resource to get submit status of the Advance Ship Notice. Read more: <a href="../../tutorials/one-fulfillment-by-allegro-0ADwgOLqWSw#zakoncz-edycje-i-wyslij-awizo" target="_blank">PL</a> / <a href="../../tutorials/one-fulfillment-by-allegro-4R9dXyMPlc9#finish-editing-and-submit-the-advance-ship-notice" target="_blank">EN</a>.


    HTTP: ``GET /fulfillment/submit-commands/{command-id}``
    """
    params: dict[str, Any] = {}
    response = get_client().request_json(
        "GET",
        f"/fulfillment/submit-commands/{command_id}",
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
@requires_writes_enabled
def update_submitted_advance_ship_notice(
    *, id: str, body: dict[str, Any] | None = None
) -> dict[str, Any] | ErrorResponse:
    """Update submitted Advance Ship Notice

    Use this resource to update already submitted Advance Ship Notice. Update is allowed only when Advance Ship Notice is in "IN_TRANSIT" status. Handling unit's amount property update clears labels property. Use Create labels command to create new labels for provided content. Read more: <a href="../../tutorials/one-fulfillment-by-allegro-0ADwgOLqWSw#edytuj-zakonczone-awizo" target="_blank">PL</a> / <a href="../../tutorials/one-fulfillment-by-allegro-4R9dXyMPlc9#edit-advance-ship-notice" target="_blank">EN</a>.


    HTTP: ``PUT /fulfillment/advance-ship-notices/{id}/submitted``
    """
    params: dict[str, Any] = {}
    response = get_client().request_json(
        "PUT",
        f"/fulfillment/advance-ship-notices/{id}/submitted",
        json=body,
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
def get_advance_ship_notice_receiving_state(*, id: str) -> dict[str, Any] | ErrorResponse:
    """Check current state and details of Advance Ship Notice receiving

    Use this resource to check the state of Advance Ship Notice receiving in Fulfillment Center in real time. The response contains a receiving progress and information about particular items - their quantities and conditions. While the Advance Ship Notice is in UNPACKING state, report is updated dynamically, which might result in different responses even at short time intervals. Read more: <a href="../../tutorials/one-fulfillment-by-allegro-0ADwgOLqWSw#sprawdz-postep-odbioru-awizo-przez-magazyn" target="_blank">PL</a> / <a href="../../tutorials/one-fulfillment-by-allegro-4R9dXyMPlc9#check-current-state-and-details-of-advance-ship-notice-receiving" target="_blank">EN</a>.


    HTTP: ``GET /fulfillment/advance-ship-notices/{id}/receiving-state``
    """
    params: dict[str, Any] = {}
    response = get_client().request_json(
        "GET",
        f"/fulfillment/advance-ship-notices/{id}/receiving-state",
        params=params,
    )
    return cast(dict[str, Any], response)
