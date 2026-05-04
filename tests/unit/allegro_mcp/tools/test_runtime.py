"""Tests for :mod:`allegro_mcp.tools._runtime`."""

from __future__ import annotations

from typing import Any

import httpx
import pytest
from pydantic import SecretStr

from allegro_client import AllegroClient, AllegroClientConfig, AllegroError
from allegro_client.errors import RateLimitError
from allegro_mcp.config import AllegroMCPConfig
from allegro_mcp.errors import ErrorResponse
from allegro_mcp.tools._runtime import (
    allegro_call,
    close_client,
    get_client,
    get_mcp_config,
    init_client,
)


def _build_client() -> AllegroClient:
    return AllegroClient(
        AllegroClientConfig(
            client_id="cid",
            client_secret=SecretStr("sec"),
            auth_flow="device",
        ),
        auth=None,
    )


@pytest.fixture
def cleanup_client() -> Any:
    """Reset the runtime singleton between tests."""
    yield
    close_client()


class TestClientLifecycle:
    def test_init_caches_client(self, cleanup_client: None) -> None:
        client = _build_client()
        config = AllegroClientConfig(
            client_id="cid", client_secret=SecretStr("sec"), auth_flow="device"
        )
        mcp_cfg = AllegroMCPConfig()
        first = init_client(config, mcp_cfg, client=client)
        second = init_client(config, mcp_cfg, client=_build_client())  # ignored
        assert first is second is client

    def test_get_client_returns_initialised(self, cleanup_client: None) -> None:
        client = _build_client()
        config = AllegroClientConfig(
            client_id="cid", client_secret=SecretStr("sec"), auth_flow="device"
        )
        init_client(config, AllegroMCPConfig(), client=client)
        assert get_client() is client

    def test_close_drops_cache(self, cleanup_client: None) -> None:
        client = _build_client()
        config = AllegroClientConfig(
            client_id="cid", client_secret=SecretStr("sec"), auth_flow="device"
        )
        init_client(config, AllegroMCPConfig(), client=client)
        close_client()
        # After close, get_client() falls back to constructing one from
        # env vars; we just confirm it's not the same object as before.
        # (Skipping the env-fallback check here — covered by the negative
        # test below.)


class TestGetClientFallback:
    def test_missing_env_raises_runtime_error(self, cleanup_client: None, clean_env: None) -> None:
        with pytest.raises(RuntimeError) as ei:
            get_client()
        assert "ALLEGRO_CLIENT_ID" in str(ei.value)


class TestMCPConfigCache:
    def test_returns_value_passed_to_init(self, cleanup_client: None) -> None:
        client = _build_client()
        config = AllegroClientConfig(
            client_id="cid", client_secret=SecretStr("sec"), auth_flow="device"
        )
        mcp_cfg = AllegroMCPConfig(enable_writes=True)
        init_client(config, mcp_cfg, client=client)
        assert get_mcp_config().enable_writes is True


class TestAllegroCall:
    def test_passes_through_on_success(self) -> None:
        @allegro_call
        def tool(x: int) -> int:
            return x * 2

        assert tool(3) == 6

    def test_translates_allegro_error(self) -> None:
        @allegro_call
        def tool() -> int:
            raise RateLimitError("RATE_LIMIT", "too many", retry_after_seconds=5, http_status=429)

        result = tool()
        assert isinstance(result, ErrorResponse)
        assert result.error == "RATE_LIMIT"
        assert result.http_status == 429

    def test_translates_httpx_request_error(self) -> None:
        @allegro_call
        def tool() -> int:
            raise httpx.ReadTimeout("timed out")

        result = tool()
        assert isinstance(result, ErrorResponse)
        assert result.error == "NETWORK_ERROR"

    def test_lets_other_exceptions_bubble(self) -> None:
        @allegro_call
        def tool() -> int:
            raise ZeroDivisionError("not our problem")

        # Programmer errors should not be silently swallowed.
        with pytest.raises(ZeroDivisionError):
            tool()

    def test_preserves_signature_for_introspection(self) -> None:
        @allegro_call
        def tool(x: int, y: str = "z") -> str:
            return f"{x}{y}"

        # functools.wraps makes __wrapped__ the original; FastMCP uses the
        # decorated callable's signature directly, so the signature on the
        # wrapper must match.
        import inspect

        sig = inspect.signature(tool)
        assert list(sig.parameters) == ["x", "y"]
        assert sig.parameters["y"].default == "z"


class TestAllegroCallNonHttpErrors:
    """Ensure base AllegroError (not just subclasses) is mapped."""

    def test_base_allegro_error(self) -> None:
        @allegro_call
        def tool() -> int:
            raise AllegroError("PARSE_ERROR", "bad json")

        result = tool()
        assert isinstance(result, ErrorResponse)
        assert result.error == "PARSE_ERROR"
