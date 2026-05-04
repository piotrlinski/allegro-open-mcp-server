"""Tool-level guards layered on top of :func:`allegro_call`.

These decorators short-circuit a tool call before any network round-trip
when:

* a required collection argument is empty (:func:`require_nonempty`),
* the configured token doesn't carry a needed OAuth scope
  (:func:`requires_scope`), or
* the high-blast-radius write gate is closed
  (:func:`requires_writes_enabled`).

Stack order: ``@mcp.tool`` outermost, then ``@allegro_call``, then any of
these guards innermost. The guards return an :class:`ErrorResponse`
directly so the ``allegro_call`` exception handler doesn't fire.
"""

from __future__ import annotations

import functools
from collections.abc import Callable
from typing import ParamSpec, TypeVar

from ..errors import (
    ERROR_EMPTY_INPUT,
    ERROR_MISSING_SCOPE,
    ERROR_WRITES_DISABLED,
    ErrorResponse,
)
from ._runtime import get_mcp_config

_T = TypeVar("_T")
_P = ParamSpec("_P")


def require_nonempty(
    field: str,
    *,
    message: str,
) -> Callable[[Callable[_P, _T]], Callable[_P, _T | ErrorResponse]]:
    """Short-circuit a tool when a named (possibly nested) field is empty.

    ``field`` is the keyword argument's name on the wrapped tool. When the
    resolved value is empty/falsy the decorator returns
    ``ErrorResponse(error="EMPTY_INPUT", message=...)`` without invoking
    the tool body — saves the network round-trip and gives callers a
    deterministic error code.
    """
    parts = field.split(".")

    def decorator(fn: Callable[_P, _T]) -> Callable[_P, _T | ErrorResponse]:
        @functools.wraps(fn)
        def wrapper(*args: _P.args, **kwargs: _P.kwargs) -> _T | ErrorResponse:
            value: object = kwargs.get(parts[0])
            for attr in parts[1:]:
                if value is None:
                    break
                value = getattr(value, attr)
            if value is not None and not value:
                return ErrorResponse(error=ERROR_EMPTY_INPUT, message=message)
            return fn(*args, **kwargs)

        return wrapper

    return decorator


def requires_writes_enabled(
    fn: Callable[_P, _T],
) -> Callable[_P, _T | ErrorResponse]:
    """Refuse to invoke ``fn`` unless ``ALLEGRO_ENABLE_WRITES`` is true.

    Apply to high-blast-radius writes (offer_delete, payment_refund,
    auction_place_bid, …). The tool stays registered so the MCP client
    can introspect it, but firing without the gate flipped surfaces a
    clear ``WRITES_DISABLED`` error rather than mutating production state.
    """

    @functools.wraps(fn)
    def wrapper(*args: _P.args, **kwargs: _P.kwargs) -> _T | ErrorResponse:
        if not get_mcp_config().enable_writes:
            return ErrorResponse(
                error=ERROR_WRITES_DISABLED,
                message=(
                    f"{fn.__name__} is a write tool; set ALLEGRO_ENABLE_WRITES=true "
                    "to enable mutating operations."
                ),
            )
        return fn(*args, **kwargs)

    return wrapper


def requires_scope(scope: str) -> Callable[[Callable[_P, _T]], Callable[_P, _T | ErrorResponse]]:
    """Annotate a tool with the OAuth scope it needs.

    Currently checks the cached scope set on the active token if one is
    available; tools that fire before any HTTP round trip will simply not
    short-circuit (we only know which scopes were granted after the first
    refresh response). Treat this as a fail-soft hint to surface scope
    issues earlier — the server still rejects the tool's HTTP call if the
    scope is genuinely missing.
    """

    def decorator(fn: Callable[_P, _T]) -> Callable[_P, _T | ErrorResponse]:
        @functools.wraps(fn)
        def wrapper(*args: _P.args, **kwargs: _P.kwargs) -> _T | ErrorResponse:
            from ._runtime import _SHARED_CLIENT  # circular at import time.

            granted = _granted_scopes(_SHARED_CLIENT)
            if granted and scope not in granted:
                return ErrorResponse(
                    error=ERROR_MISSING_SCOPE,
                    message=(
                        f"Tool {fn.__name__} requires OAuth scope '{scope}', which the "
                        "current token does not carry."
                    ),
                )
            return fn(*args, **kwargs)

        return wrapper

    return decorator


def _granted_scopes(client: object) -> set[str]:
    """Best-effort extraction of granted scopes from an :class:`AllegroClient`.

    The strategy caches the latest :class:`TokenSet` privately; we reach
    in here rather than expose a public accessor because the scope cache
    is an implementation detail. Returns an empty set if anything is
    missing — :func:`requires_scope` treats empty as "don't know" rather
    than "definitely missing".
    """
    if client is None:
        return set()
    auth = getattr(client, "_auth", None)
    tokens = getattr(auth, "_tokens", None) if auth is not None else None
    scope_str = getattr(tokens, "scope", "") or ""
    return {s for s in scope_str.split() if s}
