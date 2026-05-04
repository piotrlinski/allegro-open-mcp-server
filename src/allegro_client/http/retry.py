"""Retry transport for the Allegro REST client.

Sits in the ``httpx.Client(transport=…)`` slot so retries happen at the
wire level (after auth has injected its bearer, after ``Accept`` is set,
before the response goes back to the caller). Implementing retries here
rather than in ``AllegroClient`` keeps the client itself unaware of retry
mechanics and makes the behaviour testable in isolation.

Behaviour:

* HTTP 429 → sleep ``Retry-After`` (or 1s if absent), retry up to ``max_retries``.
* HTTP 502/503/504 → exponential backoff (1s, 2s, 4s …), retry up to ``max_retries``.
* :class:`httpx.ConnectError` / :class:`httpx.ReadTimeout` → 1 retry with 1s sleep.
* Other 4xx → no retry; passed through to :class:`AllegroClient` for status mapping.
"""

from __future__ import annotations

import logging
import time
from collections.abc import Callable

import httpx

logger = logging.getLogger(__name__)

_RETRYABLE_STATUSES = frozenset({429, 502, 503, 504})
_TRANSIENT_EXCEPTIONS: tuple[type[Exception], ...] = (
    httpx.ConnectError,
    httpx.ReadTimeout,
    httpx.RemoteProtocolError,
)


def _parse_retry_after(value: str | None) -> float:
    """Parse a ``Retry-After`` header value to seconds.

    Allegro emits an integer seconds value; we tolerate the HTTP-date form
    too. Falls back to 1 second on garbage input — the goal is "back off
    briefly" rather than precise scheduling.
    """
    if not value:
        return 1.0
    try:
        return max(0.0, float(value))
    except ValueError:
        # HTTP-date form is rare from Allegro and we don't need exact timing.
        return 1.0


class RetryTransport(httpx.BaseTransport):
    """Wraps another transport with the retry policy described in the module docstring.

    ``inner`` is the httpx transport that actually performs the HTTP I/O;
    ``sleep`` is injected so unit tests can substitute a recording stub
    without burning real wall-clock time.
    """

    def __init__(
        self,
        *,
        inner: httpx.BaseTransport | None = None,
        max_retries: int = 3,
        sleep: Callable[[float], None] = time.sleep,
    ) -> None:
        self._inner = inner or httpx.HTTPTransport()
        self._max_retries = max_retries
        self._sleep = sleep

    def handle_request(self, request: httpx.Request) -> httpx.Response:
        attempt = 0
        while True:
            try:
                response = self._inner.handle_request(request)
            except _TRANSIENT_EXCEPTIONS as exc:
                if attempt >= self._max_retries:
                    raise
                attempt += 1
                logger.warning(
                    "Transient %s; retry %d/%d",
                    type(exc).__name__,
                    attempt,
                    self._max_retries,
                )
                self._sleep(min(1.0 * (2 ** (attempt - 1)), 8.0))
                continue

            if response.status_code not in _RETRYABLE_STATUSES:
                return response
            if attempt >= self._max_retries:
                return response  # let the caller surface the error.

            attempt += 1
            if response.status_code == 429:
                delay = _parse_retry_after(response.headers.get("Retry-After"))
            else:
                # 5xx exponential backoff: 1s, 2s, 4s, capped at 8s.
                delay = min(1.0 * (2 ** (attempt - 1)), 8.0)

            logger.warning(
                "HTTP %s on %s %s; retry %d/%d after %.1fs",
                response.status_code,
                request.method,
                request.url.path,
                attempt,
                self._max_retries,
                delay,
            )
            response.close()
            self._sleep(delay)

    def close(self) -> None:
        self._inner.close()
