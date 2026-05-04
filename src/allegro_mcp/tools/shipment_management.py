# ruff: noqa
"""Generated MCP tools — DO NOT EDIT.

Run ``make gen-tools`` to regenerate from the cached OpenAPI spec.
Tag: Shipment management
"""

from __future__ import annotations

from typing import Any, cast

from ..errors import ErrorResponse
from ._decorators import requires_writes_enabled
from ._runtime import allegro_call, get_client, mcp


@mcp.tool
@allegro_call
def get_delivery_services() -> dict[str, Any] | ErrorResponse:
    """Get available delivery services

    Use this resource to get delivery services available for user. It returns services provided by Allegro and contracts with carriers owned by user and configured by GUI. Read more: <a href="../../tutorials/jak-zarzadzac-przesylkami-przez-wysylam-z-allegro-LRVjK7K21sY#jak-pobrac-liste-uslug-dostawy" target="_blank">PL</a> / <a href="../../tutorials/how-to-manage-parcels-via-ship-with-allegro-ZM9YAyGKWTV#how-to-retrieve-a-list-of-delivery-services" target="_blank">EN</a>.


    HTTP: ``GET /shipment-management/delivery-services``
    """
    params: dict[str, Any] = {}
    response = get_client().request_json(
        "GET",
        f"/shipment-management/delivery-services",
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
@requires_writes_enabled
def create_new_shipment(*, body: dict[str, Any] | None = None) -> dict[str, Any] | ErrorResponse:
    """Create new shipment

    Use this resource to create shipment for delivery. Read more: <a href="../../tutorials/jak-zarzadzac-przesylkami-przez-wysylam-z-allegro-LRVjK7K21sY#jak-utworzyc-nowa-paczke" target="_blank">PL</a> / <a href="../../tutorials/how-to-manage-parcels-via-ship-with-allegro-ZM9YAyGKWTV#how-to-create-a-new-shipment" target="_blank">EN</a>.


    HTTP: ``POST /shipment-management/shipments/create-commands``
    """
    params: dict[str, Any] = {}
    response = get_client().request_json(
        "POST",
        f"/shipment-management/shipments/create-commands",
        json=body,
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
def get_shipment_creation_status(*, commandId: str) -> dict[str, Any] | ErrorResponse:
    """Get shipment creation command status

    Use this resource to get shipment creation status. Read more: <a href="../../tutorials/jak-zarzadzac-przesylkami-przez-wysylam-z-allegro-LRVjK7K21sY#jak-sprawdzic-status-utworzenia-paczki" target="_blank">PL</a> / <a href="../../tutorials/how-to-manage-parcels-via-ship-with-allegro-ZM9YAyGKWTV#how-to-check-the-creation-status-of-a-shipment" target="_blank">EN</a>.


    HTTP: ``GET /shipment-management/shipments/create-commands/{commandId}``
    """
    params: dict[str, Any] = {}
    response = get_client().request_json(
        "GET",
        f"/shipment-management/shipments/create-commands/{commandId}",
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
@requires_writes_enabled
def cancel_shipment(*, body: dict[str, Any] | None = None) -> dict[str, Any] | ErrorResponse:
    """Cancel shipment

    Use this resource to cancel parcel. Read more: <a href="../../tutorials/jak-zarzadzac-przesylkami-przez-wysylam-z-allegro-LRVjK7K21sY#jak-anulowac-paczke" target="_blank">PL</a> / <a href="../../tutorials/how-to-manage-parcels-via-ship-with-allegro-ZM9YAyGKWTV#how-to-cancel-a-shipment" target="_blank">EN</a>.


    HTTP: ``POST /shipment-management/shipments/cancel-commands``
    """
    params: dict[str, Any] = {}
    response = get_client().request_json(
        "POST",
        f"/shipment-management/shipments/cancel-commands",
        json=body,
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
def get_shipment_cancellation_status(*, commandId: str) -> dict[str, Any] | ErrorResponse:
    """Get shipment cancellation status

    Use this resource to get parcel cancellation status. Read more: <a href="../../tutorials/jak-zarzadzac-przesylkami-przez-wysylam-z-allegro-LRVjK7K21sY#jak-sprawdzic-status-anulowania-paczki" target="_blank">PL</a> / <a href="../../tutorials/how-to-manage-parcels-via-ship-with-allegro-ZM9YAyGKWTV#how-to-check-shipment-cancellation-status" target="_blank">EN</a>.


    HTTP: ``GET /shipment-management/shipments/cancel-commands/{commandId}``
    """
    params: dict[str, Any] = {}
    response = get_client().request_json(
        "GET",
        f"/shipment-management/shipments/cancel-commands/{commandId}",
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
def get_shipment_details(*, shipmentId: str) -> dict[str, Any] | ErrorResponse:
    """Get shipment details

    Use this resource to get parcel details. Read more: <a href="../../tutorials/jak-zarzadzac-przesylkami-przez-wysylam-z-allegro-LRVjK7K21sY#jak-pobrac-szczegolowe-informacje-o-paczce" target="_blank">PL</a> / <a href="../../tutorials/how-to-manage-parcels-via-ship-with-allegro-ZM9YAyGKWTV#how-to-retrieve-shipment-details" target="_blank">EN</a>.


    HTTP: ``GET /shipment-management/shipments/{shipmentId}``
    """
    params: dict[str, Any] = {}
    response = get_client().request_json(
        "GET",
        f"/shipment-management/shipments/{shipmentId}",
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
@requires_writes_enabled
def get_shipment_labels(*, body: dict[str, Any] | None = None) -> dict[str, Any] | ErrorResponse:
    """Get shipments labels

    Use this resource to get label for created shipment. <br/>Returned content type depends on created shipment. Read more: <a href="../../tutorials/jak-zarzadzac-przesylkami-przez-wysylam-z-allegro-LRVjK7K21sY#jak-utworzyc-etykiete-na-paczke" target="_blank">PL</a> / <a href="../../tutorials/how-to-manage-parcels-via-ship-with-allegro-ZM9YAyGKWTV#how-to-create-a-label-for-shipment" target="_blank">EN</a>.


    HTTP: ``POST /shipment-management/label``
    """
    params: dict[str, Any] = {}
    response = get_client().request_json(
        "POST",
        f"/shipment-management/label",
        json=body,
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
@requires_writes_enabled
def get_shipment_protocol(*, body: dict[str, Any] | None = None) -> dict[str, Any] | ErrorResponse:
    """Get shipments protocol

    Protocol availability depends on Carrier. Read more: <a href="../../tutorials/jak-zarzadzac-przesylkami-przez-wysylam-z-allegro-LRVjK7K21sY#jak-pobrac-protokol-nadania-przesylek" target="_blank">PL</a> / <a href="../../tutorials/how-to-manage-parcels-via-ship-with-allegro-ZM9YAyGKWTV#how-to-retrieve-shipment-protocol" target="_blank">EN</a>.


    HTTP: ``POST /shipment-management/protocol``
    """
    params: dict[str, Any] = {}
    response = get_client().request_json(
        "POST",
        f"/shipment-management/protocol",
        json=body,
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
@requires_writes_enabled
def get_pickup_proposals(*, body: dict[str, Any] | None = None) -> dict[str, Any] | ErrorResponse:
    """Get shipments pickup proposals

    Use this resource to get parcels pickup date proposals. Pickup takes place, when courier arrives to take parcels for shipment. Read more: <a href="../../tutorials/jak-zarzadzac-przesylkami-przez-wysylam-z-allegro-LRVjK7K21sY#jak-sprawdzic-proponowana-date-odbioru-paczek-przez-kuriera" target="_blank">PL</a> / <a href="../../tutorials/how-to-manage-parcels-via-ship-with-allegro-ZM9YAyGKWTV#how-to-check-pickup-date-proposals" target="_blank">EN</a>.


    HTTP: ``POST /shipment-management/pickup-proposals``
    """
    params: dict[str, Any] = {}
    response = get_client().request_json(
        "POST",
        f"/shipment-management/pickup-proposals",
        json=body,
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
@requires_writes_enabled
def create_pickup(*, body: dict[str, Any] | None = None) -> dict[str, Any] | ErrorResponse:
    """Request shipments pickup

    Use this resource to request a pickup of shipments. Read more: <a href="../../tutorials/jak-zarzadzac-przesylkami-przez-wysylam-z-allegro-LRVjK7K21sY#jak-zamowic-odbior-paczek-przez-kuriera" target="_blank">PL</a> / <a href="../../tutorials/how-to-manage-parcels-via-ship-with-allegro-ZM9YAyGKWTV#how-to-request-shipment-pickup-by-a-courier" target="_blank">EN</a>.


    HTTP: ``POST /shipment-management/pickups/create-commands``
    """
    params: dict[str, Any] = {}
    response = get_client().request_json(
        "POST",
        f"/shipment-management/pickups/create-commands",
        json=body,
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
def create_pickup_status(*, commandId: str) -> dict[str, Any] | ErrorResponse:
    """Create pickup command status

    Use this resource to get pickup request status. Read more: <a href="../../tutorials/jak-zarzadzac-przesylkami-przez-wysylam-z-allegro-LRVjK7K21sY#jak-sprawdzic-status-zamowienia-odbioru-paczek" target="_blank">PL</a> / <a href="../../tutorials/how-to-manage-parcels-via-ship-with-allegro-ZM9YAyGKWTV#how-to-check-shipment-pickup-request-status" target="_blank">EN</a>.


    HTTP: ``GET /shipment-management/pickups/create-commands/{commandId}``
    """
    params: dict[str, Any] = {}
    response = get_client().request_json(
        "GET",
        f"/shipment-management/pickups/create-commands/{commandId}",
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
def get_pickup_details(*, pickupId: str) -> dict[str, Any] | ErrorResponse:
    """Get pickup details

    Use this resource to get pickup details. Read more: <a href="../../tutorials/jak-zarzadzac-przesylkami-przez-wysylam-z-allegro-LRVjK7K21sY#jak-sprawdzic-status-zamowienia-odbioru-paczek" target="_blank">PL</a> / <a href="../../tutorials/how-to-manage-parcels-via-ship-with-allegro-ZM9YAyGKWTV#how-to-check-shipment-pickup-request-status" target="_blank">EN</a>.


    HTTP: ``GET /shipment-management/pickups/{pickupId}``
    """
    params: dict[str, Any] = {}
    response = get_client().request_json(
        "GET",
        f"/shipment-management/pickups/{pickupId}",
        params=params,
    )
    return cast(dict[str, Any], response)
