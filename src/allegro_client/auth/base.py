"""Abstract base class for OAuth strategies.

Concrete strategies inherit from :class:`AuthStrategy`, which itself is an
:class:`httpx.Auth` so it slots straight into ``httpx.Client(auth=…)``.
The base class owns:

* lazy initial token acquisition (delegated to :meth:`acquire`),
* refresh-on-401 logic,
* persistence to a :class:`TokenStore`,
* a mutex that prevents two threads from refreshing concurrently.

Subclasses implement only :meth:`acquire`. Refresh shares one HTTP
``POST /auth/oauth/token`` shape across every flow, so it lives here.
"""

from __future__ import annotations

import base64
import logging
import threading
import time
from abc import ABC, abstractmethod
from collections.abc import Generator
from dataclasses import asdict, dataclass, field
from typing import Any

import httpx

from ..config import AllegroClientConfig
from ..errors import ERROR_OAUTH_FLOW, AllegroError, AuthError
from .store import TokenStore

logger = logging.getLogger(__name__)

TOKEN_PATH = "/auth/oauth/token"


@dataclass(slots=True)
class TokenSet:
    """A persisted set of OAuth tokens.

    ``access_token`` is what we send on every API call; ``refresh_token``
    is held back for renewal. ``expires_at`` is a UNIX-seconds timestamp;
    ``scope`` carries the space-separated scopes Allegro granted (which
    may be a subset of what we asked for).
    """

    access_token: str
    refresh_token: str | None = None
    expires_at: float = 0.0
    scope: str = ""
    token_type: str = "Bearer"
    extra: dict[str, str] = field(default_factory=dict)

    @property
    def is_expired(self) -> bool:
        """True when the access token is within 30 seconds of expiry."""
        return self.expires_at <= time.time() + 30

    def to_dict(self) -> dict[str, object]:
        return asdict(self)

    @classmethod
    def from_dict(cls, raw: dict[str, Any]) -> TokenSet:
        extra_raw = raw.get("extra") or {}
        extra = (
            {k: str(v) for k, v in extra_raw.items() if isinstance(v, str)}
            if isinstance(extra_raw, dict)
            else {}
        )
        return cls(
            access_token=str(raw.get("access_token", "")),
            refresh_token=(str(raw["refresh_token"]) if raw.get("refresh_token") else None),
            expires_at=float(raw.get("expires_at", 0.0) or 0.0),
            scope=str(raw.get("scope", "")),
            token_type=str(raw.get("token_type", "Bearer")),
            extra=extra,
        )

    @classmethod
    def from_oauth_response(cls, payload: dict[str, Any]) -> TokenSet:
        """Build a :class:`TokenSet` from a fresh ``/auth/oauth/token`` response.

        Allegro returns ``expires_in`` (seconds from now) rather than an
        absolute expiry; we convert immediately so renewals don't drift.
        """
        expires_in = float(payload.get("expires_in", 0) or 0)
        return cls(
            access_token=str(payload["access_token"]),
            refresh_token=(str(payload["refresh_token"]) if payload.get("refresh_token") else None),
            expires_at=time.time() + expires_in,
            scope=str(payload.get("scope", "")),
            token_type=str(payload.get("token_type", "Bearer")),
        )


class AuthStrategy(httpx.Auth, ABC):
    """Common skeleton for the four OAuth flows.

    The :meth:`auth_flow` implementation is shared:

    1. Lazily load tokens (call :meth:`acquire` on first use).
    2. If access token is expired, refresh before sending.
    3. Inject ``Authorization: Bearer <access_token>``.
    4. Yield the request; on a 401 response, try one refresh + retry.

    Subclasses override only :meth:`acquire` for their flow's initial
    token grant. ``requires_request_body = False`` because we don't need
    the request body to compute the auth header.
    """

    requires_request_body = False

    def __init__(self, config: AllegroClientConfig, store: TokenStore) -> None:
        self._config = config
        self._store = store
        self._tokens: TokenSet | None = None
        self._lock = threading.Lock()
        # The HTTP client used for token-endpoint round trips. Constructed
        # lazily so unit tests can swap a transport in via :meth:`_oauth_client`.
        self._oauth_http: httpx.Client | None = None

    # ---- httpx.Auth contract ---------------------------------------------

    def auth_flow(self, request: httpx.Request) -> Generator[httpx.Request, httpx.Response, None]:
        tokens = self._ensure_token()
        request.headers["Authorization"] = f"Bearer {tokens.access_token}"
        response = yield request

        if response.status_code != 401:
            return

        # 401: try a single refresh, then resend.
        with self._lock:
            current = self._tokens
            if current and current.access_token != tokens.access_token:
                # Another thread already refreshed; reuse its tokens.
                refreshed = current
            elif current and current.refresh_token:
                refreshed = self._refresh(current.refresh_token)
                self._persist(refreshed)
            else:
                # No refresh token to use — re-acquire from scratch.
                refreshed = self.acquire()
                self._persist(refreshed)

        request.headers["Authorization"] = f"Bearer {refreshed.access_token}"
        yield request

    # ---- Subclass extension points ----------------------------------------

    @abstractmethod
    def acquire(self) -> TokenSet:
        """Perform the flow-specific initial token grant.

        Called on cold start (no cached tokens) and as a last resort when
        refresh fails. The base class persists the returned :class:`TokenSet`.
        """

    # ---- Shared mechanics -------------------------------------------------

    def _ensure_token(self) -> TokenSet:
        with self._lock:
            if self._tokens is None:
                stored = self._store.load()
                if stored is not None:
                    self._tokens = stored
            if self._tokens is None:
                fresh = self.acquire()
                self._persist(fresh)
                return fresh
            if self._tokens.is_expired and self._tokens.refresh_token:
                refreshed = self._refresh(self._tokens.refresh_token)
                self._persist(refreshed)
                return refreshed
            return self._tokens

    def _persist(self, tokens: TokenSet) -> None:
        """Cache in memory and write through to the on-disk store."""
        self._tokens = tokens
        try:
            self._store.save(tokens)
        except OSError as exc:
            # Persistence failure is non-fatal: we still have the in-memory
            # tokens, but warn so the operator sees the issue.
            logger.warning("Could not persist tokens: %s", exc)

    def _refresh(self, refresh_token: str) -> TokenSet:
        """``POST /auth/oauth/token`` with ``grant_type=refresh_token``.

        Allegro rotates refresh tokens on every refresh — the response carries
        a new ``refresh_token`` we must persist or future renewals will fail.
        """
        return self._post_token(
            data={
                "grant_type": "refresh_token",
                "refresh_token": refresh_token,
            }
        )

    def _post_token(self, *, data: dict[str, str]) -> TokenSet:
        """Issue a token-endpoint request with HTTP-Basic client auth.

        Centralises the Authorization header, error mapping, and parsing
        used by every concrete strategy's :meth:`acquire`.
        """
        client_id = self._config.client_id
        client_secret = self._config.client_secret.get_secret_value()
        creds = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()
        headers = {
            "Authorization": f"Basic {creds}",
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
        }
        url = f"{self._config.oauth_base_url_str}{TOKEN_PATH}"

        try:
            response = self._oauth_client().post(url, data=data, headers=headers)
        except httpx.HTTPError as exc:
            raise AllegroError(
                code=ERROR_OAUTH_FLOW,
                message=f"OAuth token endpoint unreachable: {exc}",
            ) from exc

        try:
            payload = response.json()
        except ValueError as exc:
            raise AllegroError(
                code=ERROR_OAUTH_FLOW,
                message=f"Non-JSON OAuth response (HTTP {response.status_code})",
                http_status=response.status_code,
            ) from exc

        if response.status_code >= 400:
            # OAuth error envelope: {"error": "...", "error_description": "..."}.
            # Always raise AuthError here regardless of HTTP status — the OAuth
            # token endpoint uses OAuth error semantics (``authorization_pending``,
            # ``slow_down``, ``invalid_grant`` …) which the device-flow poller
            # branches on.
            base = AuthError.from_response(http_status=response.status_code, body=payload)
            raise AuthError(
                code=base.code,
                message=base.message,
                user_message=base.user_message,
                http_status=base.http_status,
                details=base.details,
                request_id=base.request_id,
            )

        return TokenSet.from_oauth_response(payload)

    def _oauth_client(self) -> httpx.Client:
        """Lazy per-strategy ``httpx.Client`` for token-endpoint round trips.

        Reuses one instance so the OAuth host enjoys connection pooling.
        Tests can replace the transport by subclassing and overriding.
        """
        if self._oauth_http is None:
            self._oauth_http = httpx.Client(timeout=self._config.timeout)
        return self._oauth_http

    # ---- Lifecycle --------------------------------------------------------

    def close(self) -> None:
        if self._oauth_http is not None:
            self._oauth_http.close()
            self._oauth_http = None
