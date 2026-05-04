"""Tests for the MCP error envelope + ``map_error``."""

from __future__ import annotations

from allegro_client.errors import (
    AllegroError,
    NotFoundError,
)
from allegro_client.errors import (
    ErrorDetail as ClientErrorDetail,
)
from allegro_mcp.errors import (
    ERROR_EMPTY_INPUT,
    ERROR_WRITES_DISABLED,
    ErrorDetail,
    ErrorResponse,
    map_error,
)


def test_map_error_carries_fields() -> None:
    exc = NotFoundError(
        code="OFFER_NOT_FOUND",
        message="Offer 123 not visible to caller",
        user_message="Nie znaleziono oferty.",
        http_status=404,
        details=[ClientErrorDetail(code="X", message="Y", path="offerId")],
        request_id="req-9",
    )
    envelope = map_error(exc)
    assert envelope.error == "OFFER_NOT_FOUND"
    assert envelope.http_status == 404
    assert envelope.user_message == "Nie znaleziono oferty."
    assert envelope.request_id == "req-9"
    assert len(envelope.details) == 1
    assert envelope.details[0].path == "offerId"


def test_envelope_is_json_serialisable() -> None:
    envelope = ErrorResponse(error="X", message="Y", details=[ErrorDetail(code="C")])
    blob = envelope.model_dump_json()
    assert '"error":"X"' in blob


def test_synthetic_codes_exposed() -> None:
    # Smoke test that the constants exist and have the documented values.
    assert ERROR_EMPTY_INPUT == "EMPTY_INPUT"
    assert ERROR_WRITES_DISABLED == "WRITES_DISABLED"


def test_base_allegro_error_maps_too() -> None:
    # Even the base class maps cleanly (e.g. for synthetic NETWORK_ERROR).
    exc = AllegroError(code="NETWORK_ERROR", message="connection reset")
    envelope = map_error(exc)
    assert envelope.error == "NETWORK_ERROR"
    assert envelope.http_status is None
