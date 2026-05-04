"""Dispatch on :attr:`AllegroClientConfig.auth_flow` to a concrete strategy.

Single function; isolated in its own module so consumers can write
``from allegro_client.auth import build_auth`` without dragging in every
strategy class. Each strategy module remains independently importable.
"""

from __future__ import annotations

from ..config import AllegroClientConfig
from .authcode import AuthorizationCodeAuth
from .base import AuthStrategy
from .client_credentials import ClientCredentialsAuth
from .device import DeviceCodeAuth
from .refresh import RefreshTokenAuth
from .store import FileTokenStore, TokenStore


def build_auth(
    config: AllegroClientConfig,
    store: TokenStore | None = None,
) -> AuthStrategy:
    """Return the strategy matching ``config.auth_flow``.

    ``store`` defaults to a :class:`FileTokenStore` at
    ``config.token_store_path``. Tests pass an
    :class:`InMemoryTokenStore` to skip filesystem I/O.
    """
    effective_store = store or FileTokenStore(config.token_store_path)
    if config.auth_flow == "device":
        return DeviceCodeAuth(config, effective_store)
    if config.auth_flow == "authcode":
        return AuthorizationCodeAuth(config, effective_store)
    if config.auth_flow == "client_credentials":
        return ClientCredentialsAuth(config, effective_store)
    if config.auth_flow == "refresh_token":
        return RefreshTokenAuth(config, effective_store)
    # AllegroClientConfig validates auth_flow as a Literal so this is
    # unreachable in normal use; the explicit raise keeps mypy happy.
    raise ValueError(f"Unknown auth_flow: {config.auth_flow}")
