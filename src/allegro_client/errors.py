"""Allegro REST API error types.

Two distinct response shapes need handling:

* Standard Allegro errors arrive as ``{"errors": [{"code", "message",
  "userMessage", "path", "details", "metadata"}]}`` per the API guideline.
* OAuth errors (RFC 6749) arrive as ``{"error", "error_description"}``,
  typically only on 401s from the token endpoint.

:meth:`AllegroError.from_response` parses both. The exception hierarchy is
keyed on HTTP status so callers can ``except RateLimitError`` etc. without
inspecting :attr:`code`.

This module is intentionally MCP-agnostic — it exposes plain exceptions, not
the MCP ``ErrorResponse`` envelope. The MCP layer maps these via
:func:`allegro_mcp.errors.map_error`.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Final

# ---- Synthetic error codes (client-side, no server origin) -----------------
ERROR_NETWORK: Final[str] = "NETWORK_ERROR"
"""Connection failure / timeout / unrecoverable transport error."""

ERROR_PARSE: Final[str] = "PARSE_ERROR"
"""Server returned a body that didn't match any expected shape."""

ERROR_OAUTH_FLOW: Final[str] = "OAUTH_FLOW_ERROR"
"""Interactive OAuth step failed (user denied, polling timed out, …)."""

ERROR_TOKEN_STORE: Final[str] = "TOKEN_STORE_ERROR"
"""Could not read or write the persisted token file."""


@dataclass(frozen=True, slots=True)
class ErrorDetail:
    """One entry from Allegro's standard ``errors[]`` array.

    Every field is optional because Allegro is inconsistent about which it
    populates. We keep the original keys close to the wire (``user_message``
    rather than ``userMessage``, but otherwise verbatim) so debugging stays
    obvious.
    """

    code: str | None = None
    message: str | None = None
    user_message: str | None = None
    path: str | None = None
    details: str | None = None
    metadata: dict[str, Any] | None = field(default=None)


class AllegroError(Exception):
    """Base exception for any failure observed against the Allegro REST API.

    :attr:`code` is either an Allegro-server code (verbatim from the response
    ``errors[0].code``), an OAuth ``error`` slug, or one of the synthetic
    constants in this module (``NETWORK_ERROR`` / ``PARSE_ERROR`` / …).
    """

    def __init__(
        self,
        code: str,
        message: str,
        *,
        user_message: str | None = None,
        http_status: int | None = None,
        details: list[ErrorDetail] | None = None,
        request_id: str | None = None,
    ) -> None:
        self.code = code
        self.message = message
        self.user_message = user_message
        self.http_status = http_status
        self.details: list[ErrorDetail] = details or []
        self.request_id = request_id
        super().__init__(f"[{code}] {message}")

    # ---- Factories ----------------------------------------------------

    @classmethod
    def from_response(
        cls,
        *,
        http_status: int,
        body: object,
        request_id: str | None = None,
    ) -> AllegroError:
        """Parse a JSON-decoded body into the most specific subclass available.

        ``body`` is the value returned by ``response.json()``; we accept
        ``object`` rather than ``dict`` because malformed responses might
        come back as anything.
        """
        klass = _status_to_class(http_status)

        # OAuth-style: {"error": "...", "error_description": "..."}
        if isinstance(body, dict) and "error" in body and "errors" not in body:
            code = str(body.get("error") or "OAUTH_ERROR")
            message = str(body.get("error_description") or code)
            return klass(
                code=code,
                message=message,
                http_status=http_status,
                request_id=request_id,
            )

        # Standard: {"errors": [{"code", "message", "userMessage", ...}]}
        if isinstance(body, dict) and isinstance(body.get("errors"), list) and body["errors"]:
            raw_errors = body["errors"]
            details = [_parse_detail(e) for e in raw_errors if isinstance(e, dict)]
            primary = raw_errors[0] if isinstance(raw_errors[0], dict) else {}
            code = str(primary.get("code") or f"HTTP_{http_status}")
            message = str(primary.get("message") or f"HTTP {http_status}")
            user_message = primary.get("userMessage")
            return klass(
                code=code,
                message=message,
                user_message=str(user_message) if user_message is not None else None,
                http_status=http_status,
                details=details,
                request_id=request_id,
            )

        # Fallback: opaque body, surface what we know.
        return klass(
            code=f"HTTP_{http_status}",
            message=f"HTTP {http_status}",
            http_status=http_status,
            request_id=request_id,
        )


# ---- Concrete subclasses ---------------------------------------------------


class AuthError(AllegroError):
    """401 — credentials missing/invalid, or refresh token rejected."""


class TokenExpiredError(AuthError):
    """Subset of :class:`AuthError`: server says the access token expired.

    The auth strategy catches this in its ``auth_flow`` and refreshes
    transparently; callers rarely see it.
    """


class ForbiddenError(AllegroError):
    """403 — token authentic but lacks the required scope."""


class NotFoundError(AllegroError):
    """404 — resource missing or not visible to the caller."""


class ValidationError(AllegroError):
    """400 / 422 — the request payload violated the Allegro schema."""


class ConflictError(AllegroError):
    """409 — concurrent edit or business-rule conflict."""


class RateLimitError(AllegroError):
    """429 — request rate or quota exceeded.

    :attr:`retry_after_seconds` carries the parsed ``Retry-After`` header
    when present; the retry transport sleeps that long before its single
    retry attempt.
    """

    def __init__(
        self,
        code: str,
        message: str,
        *,
        retry_after_seconds: int | None = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(code, message, **kwargs)
        self.retry_after_seconds = retry_after_seconds


class ServerError(AllegroError):
    """5xx — Allegro itself failed. Retried by the retry transport."""


# ---- Helpers ----------------------------------------------------------------


def _parse_detail(raw: dict[str, Any]) -> ErrorDetail:
    """Translate one Allegro error entry into our typed :class:`ErrorDetail`.

    Allegro publishes camelCase keys; we use snake_case attributes for
    consistency with the rest of the codebase.
    """
    return ErrorDetail(
        code=_str_or_none(raw.get("code")),
        message=_str_or_none(raw.get("message")),
        user_message=_str_or_none(raw.get("userMessage")),
        path=_str_or_none(raw.get("path")),
        details=_str_or_none(raw.get("details")),
        metadata=raw.get("metadata") if isinstance(raw.get("metadata"), dict) else None,
    )


def _str_or_none(value: object) -> str | None:
    return str(value) if value is not None else None


def _status_to_class(status: int) -> type[AllegroError]:
    """Pick the most specific exception class for the given HTTP status.

    400/422 → ValidationError; 401 → AuthError; 403 → ForbiddenError;
    404 → NotFoundError; 409 → ConflictError; 429 → RateLimitError;
    5xx → ServerError; anything else → :class:`AllegroError`.
    """
    if status == 401:
        return AuthError
    if status == 403:
        return ForbiddenError
    if status == 404:
        return NotFoundError
    if status == 409:
        return ConflictError
    if status == 429:
        return RateLimitError
    if status in (400, 422):
        return ValidationError
    if 500 <= status < 600:
        return ServerError
    return AllegroError
