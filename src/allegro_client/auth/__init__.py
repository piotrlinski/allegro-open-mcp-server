"""OAuth strategies for the Allegro REST API.

Four flows are supported, each as a concrete :class:`AuthStrategy` subclass:

* :class:`DeviceCodeAuth` — TV-style; first run prints URL+code, server polls.
* :class:`AuthorizationCodeAuth` — three-legged with PKCE + localhost callback.
* :class:`ClientCredentialsAuth` — two-legged, public resources only.
* :class:`RefreshTokenAuth` — pre-shared refresh token; no interactive step.

Use :func:`build_auth` to dispatch on ``config.auth_flow``.
"""

from __future__ import annotations

from .authcode import AuthorizationCodeAuth
from .base import AuthStrategy, TokenSet
from .client_credentials import ClientCredentialsAuth
from .device import DeviceCodeAuth
from .factory import build_auth
from .refresh import RefreshTokenAuth
from .store import FileTokenStore, InMemoryTokenStore, TokenStore

__all__ = [
    "AuthStrategy",
    "AuthorizationCodeAuth",
    "ClientCredentialsAuth",
    "DeviceCodeAuth",
    "FileTokenStore",
    "InMemoryTokenStore",
    "RefreshTokenAuth",
    "TokenSet",
    "TokenStore",
    "build_auth",
]
