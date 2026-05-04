"""Tests for the :mod:`allegro_mcp.tools._decorators` guards."""

from __future__ import annotations

from typing import Any

import pytest
from pydantic import SecretStr

from allegro_client import AllegroClient, AllegroClientConfig
from allegro_mcp.config import AllegroMCPConfig
from allegro_mcp.errors import ErrorResponse
from allegro_mcp.tools._decorators import (
    require_nonempty,
    requires_scope,
    requires_writes_enabled,
)
from allegro_mcp.tools._runtime import close_client, init_client


@pytest.fixture
def cleanup_client() -> Any:
    yield
    close_client()


def _init(*, enable_writes: bool = False) -> None:
    init_client(
        AllegroClientConfig(client_id="cid", client_secret=SecretStr("sec"), auth_flow="device"),
        AllegroMCPConfig(enable_writes=enable_writes),
        client=AllegroClient(
            AllegroClientConfig(
                client_id="cid", client_secret=SecretStr("sec"), auth_flow="device"
            ),
            auth=None,
        ),
    )


class TestRequireNonempty:
    def test_short_circuits_on_empty_list(self) -> None:
        @require_nonempty("ids", message="Need at least one id.")
        def tool(*, ids: list[str]) -> int:
            return len(ids)

        result = tool(ids=[])
        assert isinstance(result, ErrorResponse)
        assert result.error == "EMPTY_INPUT"

    def test_passes_through_when_nonempty(self) -> None:
        @require_nonempty("ids", message="Need at least one id.")
        def tool(*, ids: list[str]) -> int:
            return len(ids)

        assert tool(ids=["a", "b"]) == 2

    def test_passes_through_when_field_missing(self) -> None:
        # Don't conflate "absent" (kwarg not supplied) with "empty"; the
        # tool body should decide what to do with the default.
        @require_nonempty("ids", message="Need at least one id.")
        def tool(*, ids: list[str] | None = None) -> int:
            return len(ids or [])

        assert tool() == 0


class TestRequiresWritesEnabled:
    def test_blocks_when_disabled(self, cleanup_client: None) -> None:
        _init(enable_writes=False)

        @requires_writes_enabled
        def offer_delete(*, offer_id: str) -> str:
            return f"deleted {offer_id}"

        result = offer_delete(offer_id="x")
        assert isinstance(result, ErrorResponse)
        assert result.error == "WRITES_DISABLED"

    def test_allows_when_enabled(self, cleanup_client: None) -> None:
        _init(enable_writes=True)

        @requires_writes_enabled
        def offer_delete(*, offer_id: str) -> str:
            return f"deleted {offer_id}"

        assert offer_delete(offer_id="x") == "deleted x"


class TestRequiresScope:
    def test_no_known_scopes_fails_open(self, cleanup_client: None) -> None:
        # When the strategy has not yet acquired a token the cache is
        # empty; the guard should NOT short-circuit (we don't know yet).
        _init()

        @requires_scope("allegro:api:sale:offers:write")
        def tool() -> int:
            return 42

        assert tool() == 42

    def test_blocks_when_scope_missing(self, cleanup_client: None) -> None:
        from allegro_client.auth.base import TokenSet

        _init()
        from allegro_mcp.tools._runtime import _SHARED_CLIENT

        # Attach a fake TokenSet with a different scope so the guard sees
        # what's granted and rejects.
        assert _SHARED_CLIENT is not None

        # Fabricate an auth strategy attached to the client — we use the
        # client's own httpx auth slot so reaches via getattr work.
        class _FakeStrategy:
            _tokens = TokenSet(
                access_token="x",
                refresh_token=None,
                expires_at=0.0,
                scope="allegro:api:sale:offers:read",
            )

        _SHARED_CLIENT._auth = _FakeStrategy()  # type: ignore[attr-defined]

        @requires_scope("allegro:api:sale:offers:write")
        def tool() -> int:
            return 42

        result = tool()
        assert isinstance(result, ErrorResponse)
        assert result.error == "MISSING_SCOPE"
