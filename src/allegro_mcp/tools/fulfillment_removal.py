# ruff: noqa
"""Generated MCP tools — DO NOT EDIT.

Run ``make gen-tools`` to regenerate from the cached OpenAPI spec.
Tag: Fulfillment Removal
"""

from __future__ import annotations

from typing import Any, cast

from ..errors import ErrorResponse
from ._decorators import requires_writes_enabled
from ._runtime import allegro_call, get_client, mcp


@mcp.tool
@allegro_call
def get_fulfillment_removal_preferences() -> dict[str, Any] | ErrorResponse:
    """Get current active removal preference

    Use this resource to read your current removal preference. Removal preference is associated with system removal order at the moment of removal order is created. It means there can be not yet fulfilled removal orders associated with previously set removal preference. Read more: <a href="../../tutorials/one-fulfillment-by-allegro-0ADwgOLqWSw#pobierz-aktualne-ustawienia-sposobu-usuniecia-towaru-z-magazynu" target="_blank">PL</a> / <a href="../../tutorials/one-fulfillment-by-allegro-4R9dXyMPlc9#retrieve-current-settings-for-how-to-remove-goods-from-the-warehouse" target="_blank">EN</a>.


    HTTP: ``GET /fulfillment/removal/preferences``
    """
    params: dict[str, Any] = {}
    response = get_client().request_json(
        "GET",
        f"/fulfillment/removal/preferences",
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
@requires_writes_enabled
def create_fulfillment_removal_preferences(
    *, body: dict[str, Any] | None = None
) -> dict[str, Any] | ErrorResponse:
    """Create new active Fulfillment Removal Preference

    Use this resource to create new active removal preference. From the moment the preference is set, it becomes the active one, and all new system removal orders will be associated with this preference. Removal preference is associated with system removal order at the moment of removal order is created. It means there can be not yet fulfilled removal orders associated with previously set removal preference. Read more: <a href="../../tutorials/one-fulfillment-by-allegro-0ADwgOLqWSw#utworz-lub-edytuj-ustawienia-sposobu-usuniecia-towaru-z-magazynu" target="_blank">PL</a> / <a href="../../tutorials/one-fulfillment-by-allegro-4R9dXyMPlc9#create-or-edit-settings-for-how-to-remove-goods-from-the-warehouse" target="_blank">EN</a>.


    HTTP: ``PUT /fulfillment/removal/preferences``
    """
    params: dict[str, Any] = {}
    response = get_client().request_json(
        "PUT",
        f"/fulfillment/removal/preferences",
        json=body,
        params=params,
    )
    return cast(dict[str, Any], response)
