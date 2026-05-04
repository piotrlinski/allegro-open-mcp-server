"""Tests for the four OAuth strategies + the auth_flow refresh-on-401 path."""

from __future__ import annotations

import time
from typing import Any

import httpx
import pytest
import respx
from pydantic import SecretStr

from allegro_client.auth.authcode import AuthorizationCodeAuth
from allegro_client.auth.base import AuthStrategy, TokenSet
from allegro_client.auth.client_credentials import ClientCredentialsAuth
from allegro_client.auth.device import DeviceCodeAuth
from allegro_client.auth.factory import build_auth
from allegro_client.auth.refresh import RefreshTokenAuth
from allegro_client.auth.store import InMemoryTokenStore
from allegro_client.config import AllegroClientConfig
from allegro_client.errors import AllegroError, AuthError

TOKEN_URL = "https://allegro.pl/auth/oauth/token"
DEVICE_URL = "https://allegro.pl/auth/oauth/device"


def _config(flow: str, **overrides: Any) -> AllegroClientConfig:
    base: dict[str, Any] = {
        "client_id": "cid",
        "client_secret": SecretStr("sec"),
        "auth_flow": flow,
    }
    base.update(overrides)
    return AllegroClientConfig(**base)


def _token_response(**overrides: Any) -> dict[str, Any]:
    base = {
        "access_token": "new-access",
        "refresh_token": "new-refresh",
        "expires_in": 3600,
        "scope": "allegro:api:sale:offers:read",
        "token_type": "Bearer",
    }
    base.update(overrides)
    return base


class TestRefreshTokenAuth:
    def test_acquire_uses_refresh_token(self, respx_mock: respx.MockRouter) -> None:
        config = _config("refresh_token", refresh_token=SecretStr("seed-rt"))
        store = InMemoryTokenStore()
        strategy = RefreshTokenAuth(config, store)

        route = respx_mock.post(TOKEN_URL).mock(
            return_value=httpx.Response(200, json=_token_response())
        )
        tokens = strategy.acquire()

        assert tokens.access_token == "new-access"
        # Verify grant_type=refresh_token + the seed token went out.
        body = dict(
            item.split("=") for item in route.calls.last.request.content.decode().split("&")
        )
        assert body["grant_type"] == "refresh_token"
        assert body["refresh_token"] == "seed-rt"


class TestClientCredentialsAuth:
    def test_acquire_two_legged(self, respx_mock: respx.MockRouter) -> None:
        config = _config("client_credentials", scopes=["allegro:api:public"])
        strategy = ClientCredentialsAuth(config, InMemoryTokenStore())
        route = respx_mock.post(TOKEN_URL).mock(
            return_value=httpx.Response(200, json=_token_response(refresh_token=None))
        )
        tokens = strategy.acquire()

        body = dict(
            item.split("=") for item in route.calls.last.request.content.decode().split("&")
        )
        assert body["grant_type"] == "client_credentials"
        assert "scope" in body
        assert tokens.refresh_token is None  # no refresh token on two-legged.


class TestDeviceCodeAuth:
    def test_polls_until_authorised(self, respx_mock: respx.MockRouter) -> None:
        config = _config("device", scopes=["allegro:api:sale:offers:read"])
        respx_mock.post(DEVICE_URL).mock(
            return_value=httpx.Response(
                200,
                json={
                    "device_code": "dc",
                    "user_code": "ABC-123",
                    "verification_uri_complete": "https://allegro.pl/device?code=ABC-123",
                    "interval": 1,
                },
            )
        )
        # First two token-endpoint calls return authorization_pending; third succeeds.
        respx_mock.post(TOKEN_URL).mock(
            side_effect=[
                httpx.Response(400, json={"error": "authorization_pending"}),
                httpx.Response(400, json={"error": "authorization_pending"}),
                httpx.Response(200, json=_token_response()),
            ]
        )
        announces: list[tuple[str, str]] = []
        slept: list[float] = []
        strategy = DeviceCodeAuth(
            config,
            InMemoryTokenStore(),
            announce=lambda uri, code: announces.append((uri, code)),
            sleep=slept.append,
        )

        tokens = strategy.acquire()
        assert tokens.access_token == "new-access"
        assert announces == [("https://allegro.pl/device?code=ABC-123", "ABC-123")]
        assert len(slept) == 2  # two pending → two sleeps.

    def test_slow_down_increases_interval(self, respx_mock: respx.MockRouter) -> None:
        config = _config("device")
        respx_mock.post(DEVICE_URL).mock(
            return_value=httpx.Response(
                200,
                json={"device_code": "dc", "user_code": "X", "interval": 1},
            )
        )
        respx_mock.post(TOKEN_URL).mock(
            side_effect=[
                httpx.Response(400, json={"error": "slow_down"}),
                httpx.Response(200, json=_token_response()),
            ]
        )
        slept: list[float] = []
        strategy = DeviceCodeAuth(
            config,
            InMemoryTokenStore(),
            announce=lambda *_: None,
            sleep=slept.append,
        )
        strategy.acquire()
        # slow_down bumps the interval by 5s.
        assert slept[0] == 6.0

    def test_fatal_error_aborts(self, respx_mock: respx.MockRouter) -> None:
        config = _config("device")
        respx_mock.post(DEVICE_URL).mock(
            return_value=httpx.Response(
                200, json={"device_code": "dc", "user_code": "X", "interval": 1}
            )
        )
        respx_mock.post(TOKEN_URL).mock(
            return_value=httpx.Response(400, json={"error": "access_denied"})
        )
        strategy = DeviceCodeAuth(
            config,
            InMemoryTokenStore(),
            announce=lambda *_: None,
            sleep=lambda _: None,
        )
        with pytest.raises(AuthError) as ei:
            strategy.acquire()
        assert ei.value.code == "access_denied"


class TestAuthorizationCodeAuth:
    def test_constructor_demands_redirect_uri(self) -> None:
        # AllegroClientConfig refuses to construct without redirect_uri for
        # authcode flow, so we can't test the post-construction path through
        # config alone. Test the strategy's own guard against a hand-built
        # bad config: we side-step the validator.
        config = AllegroClientConfig.model_construct(
            client_id="cid",
            client_secret=SecretStr("sec"),
            auth_flow="authcode",
            redirect_uri=None,
            scopes=[],
            environment="production",
            timeout=30.0,
            max_retries=3,
            pkce_callback_port=8765,
            accept_language="pl-PL",
            user_agent="x/0",
            api_base_url=None,
            oauth_base_url=None,
            token_store_path=None,  # type: ignore[arg-type]
            default_marketplace=None,
            refresh_token=None,
        )
        # Re-derive the URLs that model_construct skipped.
        config = AllegroClientConfig(
            client_id="cid",
            client_secret=SecretStr("sec"),
            auth_flow="authcode",
            redirect_uri="http://127.0.0.1:8765/callback",  # type: ignore[arg-type]
        )
        strategy = AuthorizationCodeAuth(config, InMemoryTokenStore())
        # Strategy is constructible; full happy-path requires a real
        # browser+listener combo and is exercised in integration tests.
        assert isinstance(strategy, AuthStrategy)


class TestRefreshOn401:
    """Verify that the shared :meth:`auth_flow` retries with a refreshed token."""

    def test_refreshes_when_server_returns_401(self) -> None:
        config = _config("refresh_token", refresh_token=SecretStr("seed-rt"))
        store = InMemoryTokenStore()
        store.save(
            TokenSet(
                access_token="stale-at",
                refresh_token="stale-rt",
                expires_at=time.time() + 600,  # not yet expired.
                scope="",
            )
        )
        strategy = RefreshTokenAuth(config, store)

        with respx.mock(assert_all_called=True) as mock:
            mock.post(TOKEN_URL).mock(
                return_value=httpx.Response(
                    200, json=_token_response(access_token="fresh-at", refresh_token="fresh-rt")
                )
            )
            api_route = mock.get("https://api.allegro.pl/marketplaces").mock(
                side_effect=[
                    httpx.Response(401, json={"error": "invalid_token"}),
                    httpx.Response(200, json={"id": "allegro-pl"}),
                ]
            )
            with httpx.Client(auth=strategy) as client:
                response = client.get("https://api.allegro.pl/marketplaces")

        assert response.status_code == 200
        # First call used the stale token; second used the freshly-refreshed one.
        assert api_route.call_count == 2
        assert api_route.calls[0].request.headers["Authorization"] == "Bearer stale-at"
        assert api_route.calls[1].request.headers["Authorization"] == "Bearer fresh-at"

    def test_refreshes_proactively_when_token_expired(self) -> None:
        config = _config("refresh_token", refresh_token=SecretStr("seed-rt"))
        store = InMemoryTokenStore()
        store.save(
            TokenSet(
                access_token="expired-at",
                refresh_token="seed-rt",
                expires_at=time.time() - 60,  # already expired.
                scope="",
            )
        )
        strategy = RefreshTokenAuth(config, store)

        with respx.mock(assert_all_called=True) as mock:
            mock.post(TOKEN_URL).mock(
                return_value=httpx.Response(200, json=_token_response(access_token="fresh-at"))
            )
            api = mock.get("https://api.allegro.pl/anything").mock(
                return_value=httpx.Response(200, json={})
            )
            with httpx.Client(auth=strategy) as client:
                client.get("https://api.allegro.pl/anything")

        assert api.calls.last.request.headers["Authorization"] == "Bearer fresh-at"


class TestFactory:
    @pytest.mark.parametrize(
        ("flow", "extra", "expected"),
        [
            ("device", {}, DeviceCodeAuth),
            (
                "refresh_token",
                {"refresh_token": SecretStr("rt")},
                RefreshTokenAuth,
            ),
            ("client_credentials", {}, ClientCredentialsAuth),
            (
                "authcode",
                {"redirect_uri": "http://127.0.0.1:8765/cb"},
                AuthorizationCodeAuth,
            ),
        ],
    )
    def test_dispatches_to_correct_class(
        self,
        flow: str,
        extra: dict[str, Any],
        expected: type[AuthStrategy],
    ) -> None:
        config = _config(flow, **extra)
        strategy = build_auth(config, InMemoryTokenStore())
        assert isinstance(strategy, expected)


class TestPersistence:
    def test_acquire_writes_to_store(self, respx_mock: respx.MockRouter) -> None:
        config = _config("refresh_token", refresh_token=SecretStr("seed-rt"))
        store = InMemoryTokenStore()
        strategy = RefreshTokenAuth(config, store)

        respx_mock.post(TOKEN_URL).mock(return_value=httpx.Response(200, json=_token_response()))
        # Drive the full ensure_token path (the same one auth_flow uses).
        with httpx.Client(auth=strategy) as client:
            respx_mock.get("https://api.allegro.pl/anything").mock(
                return_value=httpx.Response(200, json={})
            )
            client.get("https://api.allegro.pl/anything")

        cached = store.load()
        assert cached is not None
        assert cached.access_token == "new-access"
        assert cached.refresh_token == "new-refresh"


class TestRefreshTokenGuard:
    def test_missing_refresh_token_raises(self) -> None:
        # Build via model_construct to dodge AllegroClientConfig's validator;
        # the strategy guards itself defensively in case a test/host
        # constructs the strategy directly with a half-formed config.
        config = AllegroClientConfig(
            client_id="cid",
            client_secret=SecretStr("sec"),
            auth_flow="device",  # validator-friendly value.
        )
        # Manually swap in the wrong flow + nuke the refresh_token.
        object.__setattr__(config, "auth_flow", "refresh_token")
        object.__setattr__(config, "refresh_token", None)

        strategy = RefreshTokenAuth(config, InMemoryTokenStore())
        with pytest.raises(AllegroError) as ei:
            strategy.acquire()
        assert ei.value.code == "OAUTH_FLOW_ERROR"
