"""MCP-shaped error envelope and exception → envelope mapping.

The :mod:`allegro_client` SDK exposes plain :class:`AllegroError` exceptions.
Tools must return a stable, JSON-serialisable shape so MCP clients can
reason about failures programmatically — that's :class:`ErrorResponse`.
The bridge is :func:`map_error`, called by the ``@allegro_call`` decorator
in :mod:`allegro_mcp.tools._runtime`.
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field

from allegro_client.errors import (
    AllegroError,
)
from allegro_client.errors import (
    ErrorDetail as ClientErrorDetail,
)

# ---- MCP-side error codes (synthetic, not from the Allegro server) ---------
ERROR_WRITES_DISABLED = "WRITES_DISABLED"
"""Returned when a write tool fires but ``ALLEGRO_ENABLE_WRITES`` is false."""

ERROR_EMPTY_INPUT = "EMPTY_INPUT"
"""Tool short-circuited because a required collection argument was empty."""

ERROR_MISSING_SCOPE = "MISSING_SCOPE"
"""Tool requires an OAuth scope the loaded token does not carry."""

ERROR_INVALID_INPUT = "INVALID_INPUT"
"""Pydantic validation rejected the inbound arguments."""


class ErrorDetail(BaseModel):
    """JSON-serialisable mirror of :class:`allegro_client.errors.ErrorDetail`.

    Pydantic model rather than the underlying dataclass so MCP clients see
    a clean JSON Schema in tool responses.
    """

    code: str | None = None
    message: str | None = None
    user_message: str | None = None
    path: str | None = None
    details: str | None = None
    metadata: dict[str, Any] | None = None


class ErrorResponse(BaseModel):
    """Uniform error envelope returned by every MCP tool on failure.

    Tools have signatures like ``-> Foo | ErrorResponse``; the FastMCP
    response schema therefore documents both the success and the failure
    shape, and the LLM on the other side gets a stable contract.
    """

    error: str = Field(
        description="Stable error code; either an Allegro server code or a synthetic constant."
    )
    message: str = Field(description="Human-readable English summary of the failure.")
    user_message: str | None = Field(default=None)
    http_status: int | None = Field(default=None)
    details: list[ErrorDetail] = Field(default_factory=list)
    request_id: str | None = Field(default=None)


def map_error(exc: AllegroError) -> ErrorResponse:
    """Translate an SDK exception into the MCP envelope."""
    return ErrorResponse(
        error=exc.code,
        message=exc.message,
        user_message=exc.user_message,
        http_status=exc.http_status,
        details=[_detail_to_pydantic(d) for d in exc.details],
        request_id=exc.request_id,
    )


def _detail_to_pydantic(detail: ClientErrorDetail) -> ErrorDetail:
    return ErrorDetail(
        code=detail.code,
        message=detail.message,
        user_message=detail.user_message,
        path=detail.path,
        details=detail.details,
        metadata=detail.metadata,
    )
