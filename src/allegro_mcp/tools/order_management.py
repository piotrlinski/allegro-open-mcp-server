# ruff: noqa
"""Generated MCP tools — DO NOT EDIT.

Run ``make gen-tools`` to regenerate from the cached OpenAPI spec.
Tag: Order management
"""

from __future__ import annotations

from typing import Any, cast

from ..errors import ErrorResponse
from ._decorators import requires_writes_enabled
from ._runtime import allegro_call, get_client, mcp


@mcp.tool
@allegro_call
def get_order_events(
    *, from_: str | None = None, type_: list[str] | None = None, limit: int | None = None
) -> dict[str, Any] | ErrorResponse:
    """Get order events

    Use this resource to return events that allow you to monitor actions which clients perform, i.e. making a purchase, filling in the checkout form (FOD), finishing payment process, making a surcharge. Read more: <a href="../../tutorials/jak-obslugiwac-zamowienia-GRaj0qyvwtR#dziennik-zdarzen" target="_blank">PL</a> / <a href="../../tutorials/process-orders-PgPMlWDr8Cv#event-log" target="_blank">EN</a>.


    HTTP: ``GET /order/events``
    """
    params = {
        "from": from_,
        "type": type_,
        "limit": limit,
    }
    response = get_client().request_json(
        "GET",
        f"/order/events",
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
def get_order_events_statistics() -> dict[str, Any] | ErrorResponse:
    """Get order events statistics

    Use this resource to returns object that contains event id and occurrence date of the latest event. It gives you current starting point for reading events. Read more: <a href="../../tutorials/jak-obslugiwac-zamowienia-GRaj0qyvwtR#jak-znalezc-najnowsze-zdarzenie" target="_blank">PL</a> / <a href="../../tutorials/process-orders-PgPMlWDr8Cv#how-to-find-the-newest-event" target="_blank">EN</a>.


    HTTP: ``GET /order/event-stats``
    """
    params: dict[str, Any] = {}
    response = get_client().request_json(
        "GET",
        f"/order/event-stats",
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
def get_list_of_orders(
    *,
    offset: int | None = None,
    limit: int | None = None,
    status: str | None = None,
    fulfillment_status: str | None = None,
    fulfillment_provider_id: str | None = None,
    fulfillment_shipmentSummary_lineItemsSent: str | None = None,
    lineItems_boughtAt_lte: str | None = None,
    lineItems_boughtAt_gte: str | None = None,
    payment_id: str | None = None,
    surcharges_id: str | None = None,
    delivery_method_id: str | None = None,
    buyer_login: str | None = None,
    marketplace_id: str | None = None,
    updatedAt_lte: str | None = None,
    updatedAt_gte: str | None = None,
    sort: str | None = None,
) -> dict[str, Any] | ErrorResponse:
    """Get the user's orders

    Use this resource to get an order list. Read more: <a href="../../tutorials/jak-obslugiwac-zamowienia-GRaj0qyvwtR#lista-zamowien" target="_blank">PL</a> / <a href="../../tutorials/process-orders-PgPMlWDr8Cv#order-list" target="_blank">EN</a>.


    HTTP: ``GET /order/checkout-forms``
    """
    params = {
        "offset": offset,
        "limit": limit,
        "status": status,
        "fulfillment.status": fulfillment_status,
        "fulfillment.provider.id": fulfillment_provider_id,
        "fulfillment.shipmentSummary.lineItemsSent": fulfillment_shipmentSummary_lineItemsSent,
        "lineItems.boughtAt.lte": lineItems_boughtAt_lte,
        "lineItems.boughtAt.gte": lineItems_boughtAt_gte,
        "payment.id": payment_id,
        "surcharges.id": surcharges_id,
        "delivery.method.id": delivery_method_id,
        "buyer.login": buyer_login,
        "marketplace.id": marketplace_id,
        "updatedAt.lte": updatedAt_lte,
        "updatedAt.gte": updatedAt_gte,
        "sort": sort,
    }
    response = get_client().request_json(
        "GET",
        f"/order/checkout-forms",
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
def get_orders_details(*, id: str) -> dict[str, Any] | ErrorResponse:
    """Get an order's details

    Use this resource to get an order details. Read more: <a href="../../tutorials/jak-obslugiwac-zamowienia-GRaj0qyvwtR#szczegoly-zamowienia" target="_blank">PL</a> / <a href="../../tutorials/process-orders-PgPMlWDr8Cv#order-details" target="_blank">EN</a>.


    HTTP: ``GET /order/checkout-forms/{id}``
    """
    params: dict[str, Any] = {}
    response = get_client().request_json(
        "GET",
        f"/order/checkout-forms/{id}",
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
def get_orders_carriers() -> dict[str, Any] | ErrorResponse:
    """Get a list of available shipping carriers

    Shipping carriers are essential to provide accurate tracking experience for customers. Use this resource to get a list of all available shipping carriers. This resource is rate limited to 50 requests per second. The response of this resource can be stored in accordance with returned caching headers. Read more: <a href="../../news/nowy-zasob-do-pobrania-identyfikatorow-przewoznikow-8dmljjGRGUE" target="_blank">PL</a> / <a href="../../news/new-resource-to-retrieve-available-delivery-company-id-VL6zDDdr4hk" target="_blank">EN</a>.


    HTTP: ``GET /order/carriers``
    """
    params: dict[str, Any] = {}
    response = get_client().request_json(
        "GET",
        f"/order/carriers",
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
def get_order_shipments(*, id: str) -> dict[str, Any] | ErrorResponse:
    """Get a list of parcel tracking numbers

    Get a list of parcel tracking numbers currently assigned to the order. Orders can be retrieved using REST API resource GET /order/checkout-forms. Please note that the shipment list may contain parcel tracking numbers added through other channels such as Moje Allegro or by the carrier that delivers the parcel. Read more: <a href="../../tutorials/jak-obslugiwac-zamowienia-GRaj0qyvwtR#jak-pobrac-numery-przesylek-dodane-do-zamowienia" target="_blank">PL</a> / <a href="../../tutorials/process-orders-PgPMlWDr8Cv#retrieving-tracking-numbers" target="_blank">EN</a>. This resource is rate limited to 50 requests per second.


    HTTP: ``GET /order/checkout-forms/{id}/shipments``
    """
    params: dict[str, Any] = {}
    response = get_client().request_json(
        "GET",
        f"/order/checkout-forms/{id}/shipments",
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
@requires_writes_enabled
def create_order_shipments(
    *, id: str, body: dict[str, Any] | None = None
) -> dict[str, Any] | ErrorResponse:
    """Add a parcel tracking number

    Add a parcel tracking number (shipment) to given order line items. Read more: <a href="../../tutorials/jak-obslugiwac-zamowienia-GRaj0qyvwtR#jak-dodac-numer-przesylki-do-przedmiotu-w-zamowieniu" target="_blank">PL</a> / <a href="../../tutorials/process-orders-PgPMlWDr8Cv#add-tracking-number-to-order" target="_blank">EN</a>. This resource is rate limited to 50 requests per second.


    HTTP: ``POST /order/checkout-forms/{id}/shipments``
    """
    params: dict[str, Any] = {}
    response = get_client().request_json(
        "POST",
        f"/order/checkout-forms/{id}/shipments",
        json=body,
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
@requires_writes_enabled
def set_order_fulfillment(
    *, id: str, checkoutForm_revision: str | None = None, body: dict[str, Any] | None = None
) -> dict[str, Any] | ErrorResponse:
    """Set seller order status

    Use to set seller order status. Read more: <a href="../../tutorials/jak-obslugiwac-zamowienia-GRaj0qyvwtR#zmiana-statusu-realizacji-zamowienia" target="_blank">PL</a> / <a href="../../tutorials/process-orders-PgPMlWDr8Cv#order-fulfillment-status-change" target="_blank">EN</a>.


    HTTP: ``PUT /order/checkout-forms/{id}/fulfillment``
    """
    params = {
        "checkoutForm.revision": checkoutForm_revision,
    }
    response = get_client().request_json(
        "PUT",
        f"/order/checkout-forms/{id}/fulfillment",
        json=body,
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
def get_order_invoices_details(*, id: str) -> dict[str, Any] | ErrorResponse:
    """Get order invoices details

    Use to get invoices details including antivirus scan results and EPT invoice verification status. Read more: <a href="../../tutorials/jak-obslugiwac-zamowienia-GRaj0qyvwtR#jak-pobrac-informacje-o-fakturach-dodanych-do-zamowienia" target="_blank">PL</a> / <a href="../../tutorials/process-orders-PgPMlWDr8Cv#retrieve-information-about-invoices" target="_blank">EN</a>.


    HTTP: ``GET /order/checkout-forms/{id}/invoices``
    """
    params: dict[str, Any] = {}
    response = get_client().request_json(
        "GET",
        f"/order/checkout-forms/{id}/invoices",
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
@requires_writes_enabled
def add_order_invoices_metadata(
    *, id: str, body: dict[str, Any] | None = None
) -> dict[str, Any] | ErrorResponse:
    """Post new invoice

    Use to add new invoice metadata. Before you send an invoice file, you need to initialize the invoice instance with the required parameters. Read more: <a href="../../tutorials/jak-obslugiwac-zamowienia-GRaj0qyvwtR#jak-dodac-fakture-do-zamowienia" target="_blank">PL</a> / <a href="../../tutorials/process-orders-PgPMlWDr8Cv#add-an-invoice-to-the-order" target="_blank">EN</a>.


    HTTP: ``POST /order/checkout-forms/{id}/invoices``
    """
    params: dict[str, Any] = {}
    response = get_client().request_json(
        "POST",
        f"/order/checkout-forms/{id}/invoices",
        json=body,
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
@requires_writes_enabled
def upload_order_invoice_file(
    *, id: str, invoiceId: str, body: dict[str, Any] | None = None
) -> dict[str, Any] | ErrorResponse:
    """Upload invoice file

    Use to upload invoice file to match created invoice metadata. Read more: <a href="../../tutorials/jak-obslugiwac-zamowienia-GRaj0qyvwtR#jak-dodac-fakture-do-zamowienia" target="_blank">PL</a> / <a href="../../tutorials/process-orders-PgPMlWDr8Cv#add-an-invoice-to-the-order" target="_blank">EN</a>.


    HTTP: ``PUT /order/checkout-forms/{id}/invoices/{invoiceId}/file``
    """
    params: dict[str, Any] = {}
    response = get_client().request_json(
        "PUT",
        f"/order/checkout-forms/{id}/invoices/{invoiceId}/file",
        json=body,
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
@requires_writes_enabled
def upload_order_billing_document_link(
    *, orderId: str, body: dict[str, Any] | None = None
) -> dict[str, Any] | ErrorResponse:
    """Upload URL to billing documents

    Used to upload a URL to a billing document. You can add up to 10 links.


    HTTP: ``POST /order/{orderId}/billing-documents/links``
    """
    params: dict[str, Any] = {}
    response = get_client().request_json(
        "POST",
        f"/order/{orderId}/billing-documents/links",
        json=body,
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
def get_allegro_pickup_drop_off_points_get(
    *, carriers: list[str] | None = None
) -> dict[str, Any] | ErrorResponse:
    """Get Allegro pickup drop off points

    Get a list of Allegro pickup drop off points. Read more: <a href="../../tutorials/jak-zarzadzac-przesylkami-przez-wysylam-z-allegro-LRVjK7K21sY#jak-pobrac-liste-punktow-allegro" target="_blank">PL</a> / <a href="../../tutorials/how-to-manage-parcels-via-ship-with-allegro-ZM9YAyGKWTV#how-to-retrieve-list-of-allegro-pickup-drop-off-points" target="_blank">EN</a>.


    HTTP: ``GET /order/carriers/ALLEGRO/points``
    """
    params = {
        "carriers": carriers,
    }
    response = get_client().request_json(
        "GET",
        f"/order/carriers/ALLEGRO/points",
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
def get_parcel_tracking(
    *, carrierId: str, waybill: list[str] | None = None
) -> dict[str, Any] | ErrorResponse:
    """Get carrier parcel tracking history

    Get tracking history for parcels. Read more: <a href="../../tutorials/jak-zarzadzac-przesylkami-przez-wysylam-z-allegro-LRVjK7K21sY#jak-pobrac-historie-statusow-przesylek" target="_blank">PL</a> / <a href="../../tutorials/how-to-manage-parcels-via-ship-with-allegro-ZM9YAyGKWTV#how-to-retrieve-parcels-statuses-history" target="_blank">EN</a>.


    HTTP: ``GET /order/carriers/{carrierId}/tracking``
    """
    params = {
        "waybill": waybill,
    }
    response = get_client().request_json(
        "GET",
        f"/order/carriers/{carrierId}/tracking",
        params=params,
    )
    return cast(dict[str, Any], response)
