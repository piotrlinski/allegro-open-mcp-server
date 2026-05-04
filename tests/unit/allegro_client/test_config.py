"""Tests for :class:`AllegroClientConfig`."""

from __future__ import annotations

import pytest
from pydantic import SecretStr, ValidationError

from allegro_client.config import (
    PROD_API_BASE_URL,
    PROD_OAUTH_BASE_URL,
    SANDBOX_API_BASE_URL,
    SANDBOX_OAUTH_BASE_URL,
    AllegroClientConfig,
)


class TestRequired:
    def test_missing_credentials_raises(self, clean_env: None) -> None:
        with pytest.raises(ValidationError) as ei:
            AllegroClientConfig()  # type: ignore[call-arg]
        msg = str(ei.value)
        assert "client_id" in msg
        assert "client_secret" in msg
        assert "auth_flow" in msg

    def test_minimum_fields_for_device_flow(self, clean_env: None) -> None:
        config = AllegroClientConfig(
            client_id="cid", client_secret=SecretStr("sec"), auth_flow="device"
        )
        assert config.client_id == "cid"
        assert config.auth_flow == "device"


class TestConditionalRequirements:
    def test_refresh_token_flow_demands_refresh_token(self, clean_env: None) -> None:
        with pytest.raises(ValidationError) as ei:
            AllegroClientConfig(
                client_id="cid",
                client_secret=SecretStr("sec"),
                auth_flow="refresh_token",
            )
        assert "ALLEGRO_REFRESH_TOKEN" in str(ei.value)

    def test_refresh_token_flow_with_token_ok(self, clean_env: None) -> None:
        config = AllegroClientConfig(
            client_id="cid",
            client_secret=SecretStr("sec"),
            auth_flow="refresh_token",
            refresh_token=SecretStr("rt"),
        )
        assert config.auth_flow == "refresh_token"

    def test_authcode_flow_demands_redirect_uri(self, clean_env: None) -> None:
        with pytest.raises(ValidationError) as ei:
            AllegroClientConfig(
                client_id="cid",
                client_secret=SecretStr("sec"),
                auth_flow="authcode",
            )
        assert "ALLEGRO_REDIRECT_URI" in str(ei.value)


class TestBaseUrlDerivation:
    def test_production_defaults(self, clean_env: None) -> None:
        config = AllegroClientConfig(
            client_id="cid", client_secret=SecretStr("sec"), auth_flow="device"
        )
        assert config.environment == "production"
        assert config.api_base_url_str == PROD_API_BASE_URL
        assert config.oauth_base_url_str == PROD_OAUTH_BASE_URL

    def test_sandbox(self, clean_env: None) -> None:
        config = AllegroClientConfig(
            client_id="cid",
            client_secret=SecretStr("sec"),
            auth_flow="device",
            environment="sandbox",
        )
        assert config.api_base_url_str == SANDBOX_API_BASE_URL
        assert config.oauth_base_url_str == SANDBOX_OAUTH_BASE_URL

    def test_override_wins(self, clean_env: None) -> None:
        config = AllegroClientConfig(
            client_id="cid",
            client_secret=SecretStr("sec"),
            auth_flow="device",
            api_base_url="https://api.example.com",  # type: ignore[arg-type]
        )
        assert config.api_base_url_str == "https://api.example.com"


class TestEnvironmentLoading:
    def test_env_prefix(self, clean_env: None, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("ALLEGRO_CLIENT_ID", "from-env")
        monkeypatch.setenv("ALLEGRO_CLIENT_SECRET", "from-env-secret")
        monkeypatch.setenv("ALLEGRO_AUTH_FLOW", "device")
        config = AllegroClientConfig()  # type: ignore[call-arg]
        assert config.client_id == "from-env"
        assert config.client_secret.get_secret_value() == "from-env-secret"

    def test_scopes_comma_separated(self, clean_env: None, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("ALLEGRO_CLIENT_ID", "cid")
        monkeypatch.setenv("ALLEGRO_CLIENT_SECRET", "sec")
        monkeypatch.setenv("ALLEGRO_AUTH_FLOW", "device")
        monkeypatch.setenv(
            "ALLEGRO_SCOPES",
            "allegro:api:sale:offers:read, allegro:api:orders:read",
        )
        config = AllegroClientConfig()  # type: ignore[call-arg]
        assert config.scopes == [
            "allegro:api:sale:offers:read",
            "allegro:api:orders:read",
        ]

    def test_unrelated_env_vars_ignored(
        self, clean_env: None, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setenv("ALLEGRO_CLIENT_ID", "cid")
        monkeypatch.setenv("ALLEGRO_CLIENT_SECRET", "sec")
        monkeypatch.setenv("ALLEGRO_AUTH_FLOW", "device")
        monkeypatch.setenv("ALLEGRO_SOMETHING_ELSE", "ignored")
        # extra="ignore" → no error raised.
        AllegroClientConfig()  # type: ignore[call-arg]


class TestSecretMasking:
    def test_secret_not_in_repr(self, clean_env: None) -> None:
        config = AllegroClientConfig(
            client_id="cid",
            client_secret=SecretStr("super-secret-value"),
            auth_flow="device",
        )
        rendered = repr(config)
        assert "super-secret-value" not in rendered
        assert "**********" in rendered or "SecretStr" in rendered
