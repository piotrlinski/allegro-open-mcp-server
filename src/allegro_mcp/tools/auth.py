"""MCP tools for managing the OAuth state.

Three operator-facing tools, distinct from the resource tools (offers,
orders, …) because they don't hit Allegro's REST surface — they expose
the locally-cached token state and let an operator nudge the auth
strategy from an MCP client.

* :func:`auth_status` — current token's scope + expiry, no secrets.
* :func:`auth_login_device` — kick off the device-code flow when the user
  needs a fresh interactive grant (different scopes, new account, …).
* :func:`auth_revoke` — clear the cached token store. Next tool call
  forces a fresh ``acquire()``.
"""

from __future__ import annotations

import time

from pydantic import BaseModel, Field

from ..errors import ErrorResponse
from ._runtime import allegro_call, get_client, mcp


class AuthStatus(BaseModel):
    """Snapshot of the current OAuth state visible to MCP clients."""

    flow: str = Field(
        description="Active auth flow: device | authcode | client_credentials | refresh_token."
    )
    has_access_token: bool
    has_refresh_token: bool
    expires_in_seconds: int | None = Field(default=None)
    scope: str = Field(default="", description="Space-separated scopes granted by the token.")
    token_store_path: str | None = None


class AuthRevokeResult(BaseModel):
    """Outcome of :func:`auth_revoke`."""

    cleared: bool


@mcp.tool
@allegro_call
def auth_status() -> AuthStatus | ErrorResponse:
    """Inspect the cached OAuth tokens.

    Returns flow type, whether tokens are present, time-to-expiry, and the
    granted scope list. Never reveals the token bytes themselves.
    """
    client = get_client()
    auth = getattr(client, "_auth", None)
    tokens = getattr(auth, "_tokens", None) if auth is not None else None
    config = getattr(client, "_config", None)
    flow = str(getattr(config, "auth_flow", ""))
    store_path = str(getattr(config, "token_store_path", "")) or None

    if tokens is None:
        return AuthStatus(
            flow=flow,
            has_access_token=False,
            has_refresh_token=False,
            token_store_path=store_path,
        )
    return AuthStatus(
        flow=flow,
        has_access_token=bool(tokens.access_token),
        has_refresh_token=bool(tokens.refresh_token),
        expires_in_seconds=max(0, int(tokens.expires_at - time.time())),
        scope=tokens.scope,
        token_store_path=store_path,
    )


@mcp.tool
@allegro_call
def auth_login_device() -> AuthStatus | ErrorResponse:
    """Force a fresh device-code login.

    Triggers ``acquire()`` on the active strategy, which prints a URL and
    user-code to stderr and polls until the user approves or the
    ten-minute window lapses. Useful when scopes change or the cached
    refresh token has been revoked at Allegro.
    """
    client = get_client()
    auth = getattr(client, "_auth", None)
    if auth is None:
        return ErrorResponse(error="NO_AUTH", message="No auth strategy attached.")
    fresh = auth.acquire()
    auth._persist(fresh)
    return auth_status()


@mcp.tool
@allegro_call
def auth_revoke() -> AuthRevokeResult | ErrorResponse:
    """Clear the persisted token store.

    Removes the cached refresh token from disk; the next tool call will
    re-run the active flow's ``acquire()``. Doesn't tell Allegro to
    invalidate the token server-side — that would require an extra
    revocation API not currently exposed.
    """
    client = get_client()
    auth = getattr(client, "_auth", None)
    store = getattr(auth, "_store", None) if auth is not None else None
    if store is None:
        return ErrorResponse(error="NO_AUTH", message="No auth strategy attached.")
    store.clear()
    # Drop the in-memory copy too so the next call really does re-acquire.
    if auth is not None and hasattr(auth, "_tokens"):
        auth._tokens = None
    return AuthRevokeResult(cleared=True)
