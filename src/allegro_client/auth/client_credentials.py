"""Client Credentials (two-legged) OAuth strategy.

Application-only access; Allegro permits this against public resources
(categories, marketplaces, pricing fees) but not against per-user data
like orders or offers. Useful for read-only catalog browsing tools.
"""

from __future__ import annotations

from .base import AuthStrategy, TokenSet


class ClientCredentialsAuth(AuthStrategy):
    """Two-legged OAuth: ``grant_type=client_credentials``.

    No refresh token is issued; on expiry we re-acquire by hitting the
    token endpoint again. The base class's refresh-on-401 path falls
    through to :meth:`acquire` because :attr:`TokenSet.refresh_token` is
    ``None``.
    """

    def acquire(self) -> TokenSet:
        data: dict[str, str] = {"grant_type": "client_credentials"}
        if self._config.scopes:
            data["scope"] = " ".join(self._config.scopes)
        return self._post_token(data=data)
