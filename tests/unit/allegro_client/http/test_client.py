"""Tests for :class:`AllegroClient`."""

from __future__ import annotations

from typing import Any

import httpx
import pytest
import respx
from pydantic import BaseModel, SecretStr

from allegro_client.config import AllegroClientConfig
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
from allegro_client.http import AllegroClient


def _config(**overrides: Any) -> AllegroClientConfig:
    """Build a minimal config for tests with optional overrides."""
    base: dict[str, Any] = {
        "client_id": "cid",
        "client_secret": SecretStr("sec"),
        "auth_flow": "device",
    }
    base.update(overrides)
    return AllegroClientConfig(**base)


class _Marketplace(BaseModel):
    """Minimal model for tests — keeps assertions readable."""

    id: str
    name: str | None = None


@pytest.fixture
def client() -> AllegroClient:
    """A client whose retry transport disables sleeping for fast tests."""
    return AllegroClient(_config(), auth=None)


class TestHeaders:
    def test_default_headers_set(self, client: AllegroClient, respx_mock: respx.MockRouter) -> None:
        route = respx_mock.get("https://api.allegro.pl/marketplaces").mock(
            return_value=httpx.Response(200, json={"id": "allegro-pl"})
        )
        client.get("/marketplaces", model=_Marketplace)
        request = route.calls.last.request
        assert request.headers["User-Agent"].startswith("allegro-mcp/")
        assert request.headers["Accept-Language"] == "pl-PL"
        assert request.headers["Accept"] == "application/vnd.allegro.public.v1+json"

    def test_beta_endpoint_uses_beta_media_type(
        self, client: AllegroClient, respx_mock: respx.MockRouter
    ) -> None:
        route = respx_mock.get("https://api.allegro.pl/returns").mock(
            return_value=httpx.Response(200, json={"items": []})
        )
        client.get_json("/returns")
        request = route.calls.last.request
        assert request.headers["Accept"] == "application/vnd.allegro.beta.v1+json"


class TestStatusMapping:
    @pytest.mark.parametrize(
        ("status", "exc_type"),
        [
            (400, ValidationError),
            (401, AuthError),
            (403, ForbiddenError),
            (404, NotFoundError),
            (409, ConflictError),
            (429, RateLimitError),
            (503, ServerError),
        ],
    )
    def test_status_to_exception(
        self,
        client: AllegroClient,
        respx_mock: respx.MockRouter,
        status: int,
        exc_type: type[AllegroError],
    ) -> None:
        respx_mock.get("https://api.allegro.pl/anything").mock(
            return_value=httpx.Response(status, json={"errors": [{"code": "X", "message": "fail"}]})
        )
        # 429 returns from the retry transport eventually after maxing out.
        # We disable retries via a config override for cleaner assertions.
        c = AllegroClient(_config(max_retries=0), auth=None)
        with pytest.raises(exc_type):
            c.get_json("/anything")


class TestParamScrubbing:
    def test_none_params_dropped(self, client: AllegroClient, respx_mock: respx.MockRouter) -> None:
        route = respx_mock.get("https://api.allegro.pl/sale/offers").mock(
            return_value=httpx.Response(200, json={"items": []})
        )
        client.get_json(
            "/sale/offers",
            params={"limit": 10, "offset": 0, "seller.id": None, "status": None},
        )
        url = str(route.calls.last.request.url)
        assert "limit=10" in url
        assert "seller.id" not in url
        assert "status" not in url


class TestParsing:
    def test_204_returns_none(self, respx_mock: respx.MockRouter) -> None:
        c = AllegroClient(_config(), auth=None)
        respx_mock.delete("https://api.allegro.pl/sale/product-offers/123").mock(
            return_value=httpx.Response(204)
        )
        c.delete("/sale/product-offers/123")  # No exception, no return.

    def test_non_json_body_raises_parse_error(self, respx_mock: respx.MockRouter) -> None:
        c = AllegroClient(_config(), auth=None)
        respx_mock.get("https://api.allegro.pl/marketplaces").mock(
            return_value=httpx.Response(
                200, content=b"not-json", headers={"content-type": "text/plain"}
            )
        )
        with pytest.raises(AllegroError) as ei:
            c.get_json("/marketplaces")
        assert ei.value.code == "PARSE_ERROR"

    def test_request_id_threaded(self, respx_mock: respx.MockRouter) -> None:
        c = AllegroClient(_config(max_retries=0), auth=None)
        respx_mock.get("https://api.allegro.pl/anything").mock(
            return_value=httpx.Response(
                404,
                json={"errors": [{"code": "NOT_FOUND", "message": "gone"}]},
                headers={"X-Request-Id": "req-abc"},
            )
        )
        with pytest.raises(NotFoundError) as ei:
            c.get_json("/anything")
        assert ei.value.request_id == "req-abc"


class TestModelValidation:
    def test_invalid_model_raises_parse_error(
        self, client: AllegroClient, respx_mock: respx.MockRouter
    ) -> None:
        # Marketplace requires `id`. Send something without it.
        respx_mock.get("https://api.allegro.pl/marketplaces").mock(
            return_value=httpx.Response(200, json={"name": "missing-id"})
        )
        with pytest.raises(AllegroError) as ei:
            client.get("/marketplaces", model=_Marketplace)
        assert ei.value.code == "PARSE_ERROR"


class TestContentType:
    def test_post_sets_content_type(
        self, client: AllegroClient, respx_mock: respx.MockRouter
    ) -> None:
        route = respx_mock.post("https://api.allegro.pl/sale/products").mock(
            return_value=httpx.Response(201, json={"id": "p1", "name": "X"})
        )
        client.post("/sale/products", model=_Marketplace, json={"name": "X"})
        assert (
            route.calls.last.request.headers["Content-Type"]
            == "application/vnd.allegro.public.v1+json"
        )
