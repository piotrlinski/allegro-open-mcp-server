"""Pre-shared refresh token strategy.

Simplest of the four flows: the operator obtained a refresh token
out-of-band (e.g. via Postman or a one-off script using the device flow)
and supplies it via ``ALLEGRO_REFRESH_TOKEN``. We never run an interactive
step; first request triggers a refresh against the supplied token.
"""

from __future__ import annotations

from ..errors import ERROR_OAUTH_FLOW, AllegroError
from .base import AuthStrategy, TokenSet


class RefreshTokenAuth(AuthStrategy):
    """Bootstrap auth from a pre-shared refresh token only.

    The :meth:`acquire` method exchanges ``config.refresh_token`` for a
    fresh ``TokenSet``. After the first successful refresh, normal
    refresh-on-expiry handling in :class:`AuthStrategy` takes over.
    """

    def acquire(self) -> TokenSet:
        if self._config.refresh_token is None:
            # Belt-and-braces: AllegroClientConfig validates this at
            # construction time. Re-check here so a misconfigured caller
            # who built the strategy by hand sees a clear error.
            raise AllegroError(
                code=ERROR_OAUTH_FLOW,
                message="RefreshTokenAuth requires ALLEGRO_REFRESH_TOKEN to be set.",
            )
        return self._refresh(self._config.refresh_token.get_secret_value())
