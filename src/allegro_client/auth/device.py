"""Device Code OAuth strategy.

Best fit for an MCP server: no browser-redirect requirement, no localhost
listener. First run prints a verification URL + user code to **stderr**
(stdout is reserved for the MCP protocol), the user approves it from any
device with a browser, and the strategy polls
``POST /auth/oauth/token`` until the user finishes authorising.

Spec: https://developer.allegro.pl/auth#device-flow
"""

from __future__ import annotations

import sys
import time
from collections.abc import Callable
from typing import Any

import httpx

from ..errors import ERROR_OAUTH_FLOW, AllegroError, AuthError
from .base import AuthStrategy, TokenSet

DEVICE_PATH = "/auth/oauth/device"

DEFAULT_INTERVAL_SECONDS = 5.0
DEFAULT_TIMEOUT_SECONDS = 600.0  # 10 minutes; matches Allegro's user-code expiry.


class DeviceCodeAuth(AuthStrategy):
    """Polling-style OAuth flow for headless processes.

    Constructor accepts overridable hooks so tests can swap clock and
    user-prompt behaviour without subclassing.

    * ``announce`` is invoked once with ``(verification_uri, user_code)``
      and defaults to writing to stderr (so stdout stays clean for MCP).
    * ``sleep`` controls the polling interval; tests pass a recording stub.
    """

    def __init__(
        self,
        *args: object,
        announce: Callable[[str, str], None] | None = None,
        sleep: Callable[[float], None] = time.sleep,
        timeout_seconds: float = DEFAULT_TIMEOUT_SECONDS,
        **kwargs: object,
    ) -> None:
        super().__init__(*args, **kwargs)  # type: ignore[arg-type]
        self._announce = announce or _default_announce
        self._sleep = sleep
        self._timeout_seconds = timeout_seconds

    def acquire(self) -> TokenSet:
        device = self._request_device_code()
        verification_uri = (
            device.get("verification_uri_complete") or device.get("verification_uri") or ""
        )
        user_code = device.get("user_code", "")
        device_code = device.get("device_code", "")
        interval = float(
            device.get("interval", DEFAULT_INTERVAL_SECONDS) or DEFAULT_INTERVAL_SECONDS
        )

        self._announce(str(verification_uri), str(user_code))
        return self._poll_until_authorised(
            device_code=str(device_code),
            interval=interval,
        )

    # ---- Internals --------------------------------------------------------

    def _request_device_code(self) -> dict[str, Any]:
        url = f"{self._config.oauth_base_url_str}{DEVICE_PATH}"
        scope = " ".join(self._config.scopes) if self._config.scopes else ""
        try:
            response = self._oauth_client().post(
                url,
                auth=(
                    self._config.client_id,
                    self._config.client_secret.get_secret_value(),
                ),
                data={"client_id": self._config.client_id, "scope": scope},
                headers={"Accept": "application/json"},
            )
        except httpx.HTTPError as exc:
            raise AllegroError(
                code=ERROR_OAUTH_FLOW,
                message=f"Device endpoint unreachable: {exc}",
            ) from exc

        try:
            payload = response.json()
        except ValueError as exc:
            raise AllegroError(
                code=ERROR_OAUTH_FLOW,
                message=f"Non-JSON device response (HTTP {response.status_code})",
                http_status=response.status_code,
            ) from exc

        if response.status_code >= 400:
            raise AuthError.from_response(http_status=response.status_code, body=payload)
        if not isinstance(payload, dict):
            raise AllegroError(
                code=ERROR_OAUTH_FLOW,
                message=f"Unexpected device response shape: {type(payload).__name__}",
            )
        return payload

    def _poll_until_authorised(self, *, device_code: str, interval: float) -> TokenSet:
        deadline = time.time() + self._timeout_seconds
        while time.time() < deadline:
            try:
                return self._post_token(
                    data={
                        "grant_type": "urn:ietf:params:oauth:grant-type:device_code",
                        "device_code": device_code,
                    }
                )
            except AuthError as exc:
                # ``authorization_pending`` and ``slow_down`` are the only
                # non-fatal codes per the spec; everything else aborts.
                if exc.code == "authorization_pending":
                    self._sleep(interval)
                    continue
                if exc.code == "slow_down":
                    interval += 5.0
                    self._sleep(interval)
                    continue
                raise

        raise AllegroError(
            code=ERROR_OAUTH_FLOW,
            message=(
                "Device-code authorisation timed out after "
                f"{self._timeout_seconds:.0f}s. Re-run the server and approve "
                "in your browser."
            ),
        )


def _default_announce(verification_uri: str, user_code: str) -> None:
    """Write the device-code prompt to stderr.

    stderr matters: an MCP client speaks JSON-RPC over stdout, so anything
    written there corrupts the protocol. stderr is for human-readable
    output that the operator (or the MCP client's logger) sees.
    """
    print(
        f"\nAllegro authorisation required:\n"
        f"  1. Open: {verification_uri}\n"
        f"  2. Enter code: {user_code}\n"
        f"  3. Approve the requested scopes.\n"
        f"Waiting for confirmation…",
        file=sys.stderr,
        flush=True,
    )
