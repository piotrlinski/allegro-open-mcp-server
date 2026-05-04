"""Iterators over Allegro's paginated list endpoints.

Allegro mixes two pagination styles:

* **Offset/limit** — most list endpoints. Caller asks for ``limit`` rows
  starting at ``offset``; the response carries ``totalCount``.
* **Cursor** — newer or high-cardinality endpoints. Caller follows
  ``nextPage`` / ``page.id`` until the server stops returning a continuation
  token.

Both are exposed as plain Python generators rather than custom collection
types — callers can ``for item in paginate(...)`` or ``list(paginate(...))``
without an extra abstraction layer.
"""

from __future__ import annotations

from collections.abc import Iterator
from typing import TYPE_CHECKING, Any, TypeVar

if TYPE_CHECKING:
    from .client import AllegroClient

T = TypeVar("T")


def paginate(
    client: AllegroClient,
    path: str,
    *,
    model: type[T],
    params: dict[str, Any] | None = None,
    page_key: str = "items",
    page_size: int = 100,
    max_items: int | None = None,
) -> Iterator[T]:
    """Iterate offset/limit-paginated rows.

    ``model`` is a Pydantic class describing **a single row**, not the
    envelope. ``page_key`` is the JSON property in the response that holds
    the row array (Allegro varies between ``items``, ``offers``, ``orders``,
    …). ``page_size`` controls the per-page request count; ``max_items``
    caps the iteration to keep MCP responses from blowing up the context.
    """
    base_params = dict(params or {})
    yielded = 0
    offset = int(base_params.pop("offset", 0))

    while True:
        page_params = {**base_params, "limit": page_size, "offset": offset}
        body: dict[str, Any] = client.get_json(path, params=page_params)
        rows = body.get(page_key, []) or []

        if not isinstance(rows, list):
            return  # Defensive: the schema lied; stop rather than loop forever.

        for row in rows:
            yield model.model_validate(row)  # type: ignore[attr-defined]
            yielded += 1
            if max_items is not None and yielded >= max_items:
                return

        if len(rows) < page_size:
            return  # short page → drained.
        offset += page_size


def paginate_cursor(
    client: AllegroClient,
    path: str,
    *,
    model: type[T],
    params: dict[str, Any] | None = None,
    page_key: str = "items",
    cursor_key: str = "page.id",
    next_cursor_key: str = "nextPage",
    page_size: int = 100,
    max_items: int | None = None,
) -> Iterator[T]:
    """Iterate cursor-paginated rows.

    The default key names follow Allegro's documented contract: requests
    take ``page.id`` (sometimes ``cursor``) and responses return the
    next-page cursor under ``nextPage``. Callers can override both for
    endpoints that diverge.
    """
    base_params = dict(params or {})
    yielded = 0
    cursor: str | None = None

    while True:
        page_params = {**base_params, "limit": page_size}
        if cursor is not None:
            page_params[cursor_key] = cursor
        body: dict[str, Any] = client.get_json(path, params=page_params)
        rows = body.get(page_key, []) or []

        if not isinstance(rows, list):
            return

        for row in rows:
            yield model.model_validate(row)  # type: ignore[attr-defined]
            yielded += 1
            if max_items is not None and yielded >= max_items:
                return

        cursor = body.get(next_cursor_key)
        if not cursor:
            return
