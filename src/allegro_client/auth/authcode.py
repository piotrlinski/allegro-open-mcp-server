"""Authorization Code with PKCE OAuth strategy.

Three-legged: spins up a localhost callback listener on
``ALLEGRO_PKCE_CALLBACK_PORT``, opens the user's browser at the
authorisation URL, waits for the redirect that carries the auth code,
and exchanges that code for tokens.

Generally the **Device Code** flow is a better fit for headless MCP
servers — Auth Code requires the user to be on the same host as the
server. Implemented here for completeness; documented as the less
preferred option in the README.
"""

from __future__ import annotations

import base64
import hashlib
import logging
import secrets
import sys
import threading
import urllib.parse
import webbrowser
from collections.abc import Callable
from http.server import BaseHTTPRequestHandler, HTTPServer

from ..errors import ERROR_OAUTH_FLOW, AllegroError
from .base import AuthStrategy, TokenSet

logger = logging.getLogger(__name__)

AUTHORIZE_PATH = "/auth/oauth/authorize"


class AuthorizationCodeAuth(AuthStrategy):
    """Three-legged OAuth with PKCE.

    Constructor takes optional hooks (``open_browser``, ``announce``) so
    tests can replace the user-facing pieces.
    """

    def __init__(
        self,
        *args: object,
        open_browser: Callable[[str], None] | None = None,
        announce: Callable[[str], None] | None = None,
        listen_timeout: float = 600.0,
        **kwargs: object,
    ) -> None:
        super().__init__(*args, **kwargs)  # type: ignore[arg-type]
        self._open_browser = open_browser or webbrowser.open
        self._announce = announce or _default_announce
        self._listen_timeout = listen_timeout

    def acquire(self) -> TokenSet:
        if self._config.redirect_uri is None:
            raise AllegroError(
                code=ERROR_OAUTH_FLOW,
                message="AuthorizationCodeAuth requires ALLEGRO_REDIRECT_URI.",
            )
        verifier, challenge = _generate_pkce_pair()
        state = secrets.token_urlsafe(24)
        auth_url = self._build_authorize_url(state=state, challenge=challenge)

        captured: dict[str, str] = {}
        server = self._build_listener(captured=captured, expected_state=state)
        thread = threading.Thread(target=server.handle_request, daemon=True)
        thread.start()

        self._announce(auth_url)
        try:
            self._open_browser(auth_url)
        except Exception as exc:
            logger.warning("Could not open browser automatically: %s", exc)

        thread.join(timeout=self._listen_timeout)
        if thread.is_alive():
            server.server_close()
            raise AllegroError(
                code=ERROR_OAUTH_FLOW,
                message=(
                    f"Authorization Code flow timed out after {self._listen_timeout:.0f}s "
                    "waiting for the browser callback."
                ),
            )

        if "code" not in captured:
            raise AllegroError(
                code=ERROR_OAUTH_FLOW,
                message=captured.get("error", "Authorization Code flow failed."),
            )

        return self._post_token(
            data={
                "grant_type": "authorization_code",
                "code": captured["code"],
                "redirect_uri": str(self._config.redirect_uri),
                "code_verifier": verifier,
            }
        )

    # ---- Helpers ----------------------------------------------------------

    def _build_authorize_url(self, *, state: str, challenge: str) -> str:
        params = {
            "response_type": "code",
            "client_id": self._config.client_id,
            "redirect_uri": str(self._config.redirect_uri),
            "state": state,
            "code_challenge": challenge,
            "code_challenge_method": "S256",
        }
        if self._config.scopes:
            params["scope"] = " ".join(self._config.scopes)
        return f"{self._config.oauth_base_url_str}{AUTHORIZE_PATH}?{urllib.parse.urlencode(params)}"

    def _build_listener(self, *, captured: dict[str, str], expected_state: str) -> HTTPServer:
        port = self._config.pkce_callback_port

        class Handler(BaseHTTPRequestHandler):
            # Suppress default access-log spew to stderr so the MCP client's
            # log isn't polluted with one-off auth callbacks. The ``format``
            # parameter name is dictated by the stdlib superclass; we shadow
            # the builtin only inside this short method.
            def log_message(self, format: str, *args: object) -> None:  # noqa: A002
                return

            def do_GET(self) -> None:
                params = urllib.parse.parse_qs(urllib.parse.urlsplit(self.path).query)
                state = (params.get("state") or [""])[0]
                if state != expected_state:
                    captured["error"] = "state mismatch in OAuth callback"
                    self._respond("State mismatch — authorisation aborted.")
                    return
                if code := (params.get("code") or [""])[0]:
                    captured["code"] = code
                    self._respond("Authorisation complete — you may close this tab.")
                    return
                captured["error"] = (params.get("error") or ["unknown_error"])[0]
                self._respond(f"Authorisation failed: {captured['error']}")

            def _respond(self, body: str) -> None:
                self.send_response(200)
                self.send_header("Content-Type", "text/plain; charset=utf-8")
                self.end_headers()
                self.wfile.write(body.encode("utf-8"))

        return HTTPServer(("127.0.0.1", port), Handler)


def _generate_pkce_pair() -> tuple[str, str]:
    """Return a ``(verifier, challenge)`` pair for PKCE S256.

    The verifier is 64 chars of url-safe random; the challenge is its
    SHA-256 base64url-encoded with no padding, per RFC 7636.
    """
    verifier = secrets.token_urlsafe(48)[:64]
    digest = hashlib.sha256(verifier.encode("ascii")).digest()
    challenge = base64.urlsafe_b64encode(digest).rstrip(b"=").decode("ascii")
    return verifier, challenge


def _default_announce(auth_url: str) -> None:
    """Print the URL the user must visit in case the browser open fails.

    Writes to stderr because stdout belongs to the MCP protocol stream.
    """
    print(
        f"\nOpening Allegro authorisation in your browser:\n  {auth_url}\n",
        file=sys.stderr,
        flush=True,
    )
