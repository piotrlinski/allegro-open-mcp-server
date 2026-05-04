"""Shared runtime for the ``@mcp.tool`` registry.

Owns the single :class:`fastmcp.FastMCP` instance every tool registers
against, plus the lazy process-wide :class:`AllegroClient` cache and the
``allegro_call`` decorator that converts SDK exceptions into the MCP
:class:`ErrorResponse` envelope.

Tool modules import ``mcp`` and the helpers from here; this module
imports nothing from ``tools.*`` (its submodules) to keep the dependency
direction clean. The architecture test enforces it.
"""

from __future__ import annotations

import functools
import logging
import threading
from collections.abc import Callable
from typing import ParamSpec, TypeVar

import httpx
from fastmcp import FastMCP
from pydantic import ValidationError as PydanticValidationError

from allegro_client import AllegroClient, AllegroClientConfig, AllegroError
from allegro_client.auth import build_auth

from ..config import AllegroMCPConfig
from ..errors import (
    ERROR_INVALID_INPUT,
    ErrorResponse,
    map_error,
)

# Synthetic code returned when the retry transport's last attempt still
# raised. Kept inline so we don't import a one-string constant from a
# sibling module.
_ERROR_NETWORK = "NETWORK_ERROR"

logger = logging.getLogger(__name__)

mcp: FastMCP = FastMCP("Allegro")
"""The single FastMCP instance every tool registers against.

Tool modules do ``from ._runtime import mcp`` and stack ``@mcp.tool`` on
their functions. ``allegro_mcp.tools.__init__`` side-effect-imports each
module to trigger registration before :func:`server.main` calls
``mcp.run()``.
"""

_T = TypeVar("_T")
_P = ParamSpec("_P")

# ---- Client lifecycle ------------------------------------------------------

_SHARED_CLIENT: AllegroClient | None = None
_MCP_CONFIG: AllegroMCPConfig | None = None
_CLIENT_LOCK = threading.Lock()


def init_client(
    client_config: AllegroClientConfig,
    mcp_config: AllegroMCPConfig,
    *,
    client: AllegroClient | None = None,
) -> AllegroClient:
    """Create the shared :class:`AllegroClient`.

    Called once by :func:`server.main` after CLI args + env vars are
    resolved into the two configs. Idempotent: a second call returns the
    existing cached client without rebuilding it.

    The optional ``client`` parameter lets tests inject a pre-built client
    (with a mocked transport, in-memory token store, etc.) bypassing the
    standard ``build_auth`` factory.
    """
    global _SHARED_CLIENT, _MCP_CONFIG
    with _CLIENT_LOCK:
        _MCP_CONFIG = mcp_config
        if _SHARED_CLIENT is None:
            if client is not None:
                _SHARED_CLIENT = client
            else:
                auth = build_auth(client_config)
                _SHARED_CLIENT = AllegroClient(client_config, auth=auth)
        return _SHARED_CLIENT


def get_client() -> AllegroClient:
    """Return the process-wide :class:`AllegroClient`.

    Initialised eagerly by :func:`server.main` via :func:`init_client`. As
    a convenience for ad-hoc scripts and tests, falls back to constructing
    one from ``ALLEGRO_*`` env vars when no client has been initialised.
    """
    global _SHARED_CLIENT, _MCP_CONFIG
    with _CLIENT_LOCK:
        if _SHARED_CLIENT is None:
            try:
                client_config = AllegroClientConfig()  # type: ignore[call-arg]
                mcp_config = AllegroMCPConfig()
            except PydanticValidationError as exc:
                missing = ", ".join(
                    f"ALLEGRO_{str(err['loc'][0]).upper()}" if err.get("loc") else "ALLEGRO_?"
                    for err in exc.errors()
                )
                raise RuntimeError(
                    f"Missing Allegro configuration ({missing}). Pass them as "
                    "CLI flags or set the corresponding ALLEGRO_* env vars."
                ) from exc
            _MCP_CONFIG = mcp_config
            _SHARED_CLIENT = AllegroClient(client_config, auth=build_auth(client_config))
        return _SHARED_CLIENT


def get_mcp_config() -> AllegroMCPConfig:
    """Return the cached :class:`AllegroMCPConfig` set by :func:`init_client`.

    Defaults to a fresh load from env vars if :func:`init_client` hasn't
    run yet (only useful for ad-hoc tool invocations outside the server).
    """
    global _MCP_CONFIG
    with _CLIENT_LOCK:
        if _MCP_CONFIG is None:
            _MCP_CONFIG = AllegroMCPConfig()
        return _MCP_CONFIG


def close_client() -> None:
    """Close the shared client and drop the cache.

    Called from :func:`server.main`'s ``finally`` block on shutdown, and
    from tests that need to swap configurations between runs.
    """
    global _SHARED_CLIENT, _MCP_CONFIG
    with _CLIENT_LOCK:
        if _SHARED_CLIENT is not None:
            _SHARED_CLIENT.close()
            _SHARED_CLIENT = None
        _MCP_CONFIG = None


# ---- Decorators ------------------------------------------------------------


def allegro_call(fn: Callable[_P, _T]) -> Callable[_P, _T | ErrorResponse]:
    """Translate SDK exceptions into the MCP :class:`ErrorResponse` envelope.

    Wraps every ``@mcp.tool`` so tool bodies can stay focused on the happy
    path. Handles three error families:

    1. :class:`AllegroError` — from the SDK; map directly via :func:`map_error`.
    2. :class:`httpx.RequestError` — transport-level failure that escaped
       the retry transport (extremely rare; mapped to ``NETWORK_ERROR``).
    3. :class:`pydantic.ValidationError` — argument validation failure;
       mapped to ``INVALID_INPUT``.

    Uses :class:`ParamSpec` so the wrapper preserves the wrapped tool's
    signature for both mypy and IDE autocomplete (FastMCP introspects the
    decorated callable to derive its input schema).
    """

    @functools.wraps(fn)
    def wrapper(*args: _P.args, **kwargs: _P.kwargs) -> _T | ErrorResponse:
        try:
            return fn(*args, **kwargs)
        except AllegroError as exc:
            return map_error(exc)
        except httpx.RequestError as exc:
            return ErrorResponse(
                error=_ERROR_NETWORK,
                message=f"{type(exc).__name__}: {exc}",
            )
        except PydanticValidationError as exc:
            return ErrorResponse(
                error=ERROR_INVALID_INPUT,
                message=str(exc.errors(include_url=False)[:3]),
            )

    return wrapper
