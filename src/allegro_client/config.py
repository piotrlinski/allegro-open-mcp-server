"""Allegro REST API connection settings.

Loaded from environment variables prefixed with ``ALLEGRO_``. Owns nothing
beyond credentials, OAuth flow selection, base URLs, and a couple of HTTP
knobs — kept in its own module so every other layer can import it without
dragging in httpx, FastMCP, or domain models.

The class is **MCP-agnostic**. MCP-only knobs (``enable_writes``, log
directory naming) live in :class:`allegro_mcp.config.AllegroMCPConfig`,
which composes this one.
"""

from __future__ import annotations

from pathlib import Path
from typing import Annotated, Literal

from pydantic import (
    AnyHttpUrl,
    Field,
    SecretStr,
    field_validator,
    model_validator,
)
from pydantic_settings import BaseSettings, NoDecode, SettingsConfigDict

# Pydantic v2 ships typing_extensions transitively; using it keeps mypy happy
# on Python 3.10 where ``typing.Self`` is unavailable.
from typing_extensions import Self

from .version import __version__

# ---- URL constants ---------------------------------------------------------
# Hard-coded because they're stable contract surface, not config: the OAuth
# endpoints live under the bare allegro.pl host (NOT api.allegro.pl), and the
# sandbox uses a parallel allegrosandbox.pl namespace.
PROD_API_BASE_URL = "https://api.allegro.pl"
PROD_OAUTH_BASE_URL = "https://allegro.pl"
SANDBOX_API_BASE_URL = "https://api.allegro.pl.allegrosandbox.pl"
SANDBOX_OAUTH_BASE_URL = "https://allegro.pl.allegrosandbox.pl"

DEFAULT_TIMEOUT = 30.0
DEFAULT_MAX_RETRIES = 3
DEFAULT_PKCE_CALLBACK_PORT = 8765
DEFAULT_REPO_URL = "https://github.com/piotrlinski/allegro-open-mcp-server"

AuthFlow = Literal["device", "authcode", "client_credentials", "refresh_token"]
Environment = Literal["production", "sandbox"]


def _default_token_store_path() -> Path:
    """``~/.allegro-mcp/tokens.json`` — created lazily by :class:`FileTokenStore`."""
    return Path.home() / ".allegro-mcp" / "tokens.json"


def _default_user_agent() -> str:
    """Allegro requires a descriptive User-Agent. Default points back to the repo."""
    return f"allegro-mcp/{__version__} (+{DEFAULT_REPO_URL})"


class AllegroClientConfig(BaseSettings):
    """Allegro REST API connection settings.

    Loads from environment variables prefixed with ``ALLEGRO_``. Required
    fields cause a :class:`pydantic.ValidationError` at construction time so
    the server fails fast on misconfiguration rather than mid-request.

    Conditional requirements (validated in :meth:`_check_flow_requirements`):

    * ``auth_flow="refresh_token"``  ⇒ ``refresh_token`` must be set.
    * ``auth_flow="authcode"``       ⇒ ``redirect_uri`` must be set.

    Base URLs are derived from :attr:`environment` unless overridden.
    """

    # ---- Required ---------------------------------------------------------
    client_id: str = Field(min_length=1, description="Allegro application client_id.")
    client_secret: SecretStr = Field(min_length=1, description="Allegro application client_secret.")
    auth_flow: AuthFlow = Field(description="Which OAuth flow to use.")

    # ---- Conditionally required ------------------------------------------
    refresh_token: SecretStr | None = Field(default=None, description="Pre-shared refresh token.")
    redirect_uri: AnyHttpUrl | None = Field(default=None, description="OAuth redirect URI.")
    pkce_callback_port: int = Field(
        default=DEFAULT_PKCE_CALLBACK_PORT,
        ge=1024,
        le=65535,
        description="Localhost port the authcode flow listens on for the callback.",
    )

    # ---- Optional --------------------------------------------------------
    # NoDecode tells pydantic-settings not to JSON-decode the env value, so
    # the field_validator below sees the raw comma-separated string.
    scopes: Annotated[list[str], NoDecode] = Field(
        default_factory=list, description="Requested OAuth scopes."
    )
    environment: Environment = Field(default="production")
    api_base_url: AnyHttpUrl | None = Field(default=None, description="Override the API base URL.")
    oauth_base_url: AnyHttpUrl | None = Field(
        default=None, description="Override the OAuth base URL."
    )
    token_store_path: Path = Field(default_factory=_default_token_store_path)
    default_marketplace: str | None = Field(default=None, description="e.g. 'allegro-pl'.")
    accept_language: str = Field(default="pl-PL")
    user_agent: str = Field(default_factory=_default_user_agent)
    timeout: Annotated[float, Field(gt=0)] = DEFAULT_TIMEOUT
    max_retries: Annotated[int, Field(ge=0, le=10)] = DEFAULT_MAX_RETRIES

    model_config = SettingsConfigDict(
        env_prefix="ALLEGRO_",
        extra="ignore",
        # Comma-separated env values (e.g. ALLEGRO_SCOPES=foo,bar) are split
        # for ``list[str]`` fields. JSON-encoded values still parse.
        env_parse_none_str="",
    )

    # ---- Field-level coercion --------------------------------------------

    @field_validator("scopes", mode="before")
    @classmethod
    def _split_scopes(cls, value: object) -> object:
        """Accept comma-separated env strings as well as native lists."""
        if isinstance(value, str):
            return [s.strip() for s in value.split(",") if s.strip()]
        return value

    # ---- Cross-field validation ------------------------------------------

    @model_validator(mode="after")
    def _check_flow_requirements(self) -> Self:
        if self.auth_flow == "refresh_token" and self.refresh_token is None:
            raise ValueError(
                "ALLEGRO_REFRESH_TOKEN is required when ALLEGRO_AUTH_FLOW=refresh_token."
            )
        if self.auth_flow == "authcode" and self.redirect_uri is None:
            raise ValueError("ALLEGRO_REDIRECT_URI is required when ALLEGRO_AUTH_FLOW=authcode.")
        return self

    @model_validator(mode="after")
    def _derive_base_urls(self) -> Self:
        """Fill in :attr:`api_base_url` and :attr:`oauth_base_url` from the
        environment selector when the caller didn't override them.
        """
        if self.api_base_url is None:
            url = PROD_API_BASE_URL if self.environment == "production" else SANDBOX_API_BASE_URL
            object.__setattr__(self, "api_base_url", AnyHttpUrl(url))
        if self.oauth_base_url is None:
            url = (
                PROD_OAUTH_BASE_URL if self.environment == "production" else SANDBOX_OAUTH_BASE_URL
            )
            object.__setattr__(self, "oauth_base_url", AnyHttpUrl(url))
        return self

    # ---- Convenience accessors -------------------------------------------

    @property
    def api_base_url_str(self) -> str:
        """The API base URL as a plain string (httpx prefers strings)."""
        # _derive_base_urls fills these in; assert for type narrowing.
        assert self.api_base_url is not None
        return str(self.api_base_url).rstrip("/")

    @property
    def oauth_base_url_str(self) -> str:
        """The OAuth base URL as a plain string."""
        assert self.oauth_base_url is not None
        return str(self.oauth_base_url).rstrip("/")
