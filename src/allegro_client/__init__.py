"""Allegro REST API SDK — MCP-agnostic, designed to be extractable as a
standalone package.

Public surface (grows as implementation tasks land):

    from allegro_client import (
        AllegroClientConfig,  # config
        AllegroError,         # errors (exception hierarchy root)
        __version__,
    )

Importing from ``allegro_client.*`` should never reach into ``allegro_mcp.*``
or any MCP framework module. The boundary is enforced by
``tests/unit/test_architecture.py``.
"""

from __future__ import annotations

from .config import AllegroClientConfig
from .errors import (
    AllegroError,
    AuthError,
    ConflictError,
    ErrorDetail,
    ForbiddenError,
    NotFoundError,
    RateLimitError,
    ServerError,
    TokenExpiredError,
    ValidationError,
)
from .http import AllegroClient, paginate, paginate_cursor
from .version import __version__

__all__ = [
    "AllegroClient",
    "AllegroClientConfig",
    "AllegroError",
    "AuthError",
    "ConflictError",
    "ErrorDetail",
    "ForbiddenError",
    "NotFoundError",
    "RateLimitError",
    "ServerError",
    "TokenExpiredError",
    "ValidationError",
    "__version__",
    "paginate",
    "paginate_cursor",
]
