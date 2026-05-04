"""HTTP transport for the Allegro REST API.

Public surface:

* :class:`AllegroClient` — typed sync wrapper around ``httpx.Client``.
* :func:`paginate` / :func:`paginate_cursor` — iterators over paginated endpoints.
* :class:`RetryTransport` — exposed for advanced callers who want to layer
  their own transport on top.
"""

from __future__ import annotations

from .client import AllegroClient
from .pagination import paginate, paginate_cursor
from .retry import RetryTransport

__all__ = ["AllegroClient", "RetryTransport", "paginate", "paginate_cursor"]
