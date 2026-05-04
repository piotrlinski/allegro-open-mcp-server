"""Tests for the :mod:`allegro_client.errors` module."""

from __future__ import annotations

from allegro_client.errors import (
    AllegroError,
    AuthError,
    ConflictError,
    ForbiddenError,
    NotFoundError,
    RateLimitError,
    ServerError,
    ValidationError,
)


class TestStandardEnvelope:
    def test_parses_first_error_as_primary(self) -> None:
        err = AllegroError.from_response(
            http_status=400,
            body={
                "errors": [
                    {
                        "code": "OFFER_INVALID",
                        "message": "Title too short",
                        "userMessage": "Tytuł oferty jest za krótki.",
                        "path": "name",
                    },
                    {
                        "code": "OFFER_INVALID",
                        "message": "Image required",
                        "path": "images",
                    },
                ]
            },
        )
        assert isinstance(err, ValidationError)
        assert err.code == "OFFER_INVALID"
        assert err.message == "Title too short"
        assert err.user_message == "Tytuł oferty jest za krótki."
        assert len(err.details) == 2
        assert err.details[0].path == "name"
        assert err.details[1].path == "images"

    def test_request_id_threaded_through(self) -> None:
        err = AllegroError.from_response(
            http_status=500,
            body={"errors": [{"code": "INTERNAL", "message": "boom"}]},
            request_id="req-123",
        )
        assert err.request_id == "req-123"


class TestOAuthEnvelope:
    def test_parses_oauth_error_shape(self) -> None:
        err = AllegroError.from_response(
            http_status=401,
            body={"error": "invalid_grant", "error_description": "Token expired"},
        )
        assert isinstance(err, AuthError)
        assert err.code == "invalid_grant"
        assert err.message == "Token expired"


class TestStatusMapping:
    def test_401_maps_to_auth_error(self) -> None:
        err = AllegroError.from_response(http_status=401, body={})
        assert isinstance(err, AuthError)

    def test_403_maps_to_forbidden(self) -> None:
        err = AllegroError.from_response(http_status=403, body={})
        assert isinstance(err, ForbiddenError)

    def test_404_maps_to_not_found(self) -> None:
        err = AllegroError.from_response(http_status=404, body={})
        assert isinstance(err, NotFoundError)

    def test_409_maps_to_conflict(self) -> None:
        err = AllegroError.from_response(http_status=409, body={})
        assert isinstance(err, ConflictError)

    def test_429_maps_to_rate_limit(self) -> None:
        err = AllegroError.from_response(http_status=429, body={})
        assert isinstance(err, RateLimitError)

    def test_500_maps_to_server_error(self) -> None:
        err = AllegroError.from_response(http_status=503, body={})
        assert isinstance(err, ServerError)

    def test_unknown_status_falls_back_to_base(self) -> None:
        err = AllegroError.from_response(http_status=418, body={})
        assert type(err) is AllegroError


class TestRateLimitMetadata:
    def test_carries_retry_after(self) -> None:
        err = RateLimitError(
            "RATE_LIMIT", "Too many requests", retry_after_seconds=42, http_status=429
        )
        assert err.retry_after_seconds == 42


class TestFallbackBody:
    def test_opaque_body_yields_synthetic_code(self) -> None:
        err = AllegroError.from_response(http_status=502, body=b"<html>...</html>")
        assert isinstance(err, ServerError)
        assert err.code == "HTTP_502"

    def test_unknown_dict_shape_yields_synthetic_code(self) -> None:
        err = AllegroError.from_response(http_status=400, body={"unexpected": "shape"})
        assert isinstance(err, ValidationError)
        assert err.code == "HTTP_400"
