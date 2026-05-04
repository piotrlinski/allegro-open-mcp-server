"""Persistent storage for :class:`TokenSet` instances.

The default :class:`FileTokenStore` writes JSON to a path under the user's
home directory (``~/.allegro-mcp/tokens.json`` by default) and protects
the file with mode ``0600`` so other users on the host can't read the
refresh token. The :class:`TokenStore` Protocol is the abstraction
boundary — production code uses :class:`FileTokenStore`, but tests can
substitute an in-memory store.
"""

from __future__ import annotations

import contextlib
import json
import os
from pathlib import Path
from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from .base import TokenSet


SCHEMA_VERSION = 1
"""Bumps on incompatible on-disk format changes; surfaced via ``_schema_version``
key in the JSON blob so future versions can migrate."""


class TokenStore(Protocol):
    """Pluggable persistence interface for :class:`TokenSet`."""

    def load(self) -> TokenSet | None:
        """Return the cached :class:`TokenSet`, or ``None`` if no cache exists."""
        ...

    def save(self, tokens: TokenSet) -> None:
        """Persist ``tokens``, replacing any prior value atomically."""
        ...

    def clear(self) -> None:
        """Remove the persisted tokens (used by ``auth_revoke`` tooling)."""
        ...


class FileTokenStore:
    """JSON-on-disk token store with atomic writes and ``0600`` permissions.

    Atomic in the rename-into-place sense: we write to a sibling temp file
    in the same directory, then ``os.replace`` it over the target. This
    avoids ever leaving a half-written tokens file even if the process
    crashes mid-write.
    """

    def __init__(self, path: Path) -> None:
        self._path = path

    @property
    def path(self) -> Path:
        return self._path

    def load(self) -> TokenSet | None:
        from .base import (
            TokenSet,  # local import: avoids the auth.store→auth.base→auth.store cycle.
        )

        if not self._path.exists():
            return None
        try:
            raw = json.loads(self._path.read_text())
        except (OSError, json.JSONDecodeError):
            # Corrupt or unreadable cache: pretend it's missing. The next
            # auth call will trigger a fresh acquire().
            return None
        if not isinstance(raw, dict):
            return None
        # Forward-compat: ignore newer schemas; the next ``save()`` overwrites.
        if int(raw.get("_schema_version", 0)) > SCHEMA_VERSION:
            return None
        return TokenSet.from_dict(raw)

    def save(self, tokens: TokenSet) -> None:
        self._path.parent.mkdir(parents=True, exist_ok=True)
        payload = {"_schema_version": SCHEMA_VERSION, **tokens.to_dict()}
        tmp = self._path.with_suffix(self._path.suffix + ".tmp")
        tmp.write_text(json.dumps(payload, sort_keys=True, indent=2))
        # Tighten permissions BEFORE the atomic rename: even on POSIX a brief
        # window with mode 0644 is observable to other users on the host.
        # Filesystems that don't honour chmod (Windows shares, some FUSE) are
        # tolerated — the rename below is still correct.
        with contextlib.suppress(OSError):
            os.chmod(tmp, 0o600)
        os.replace(tmp, self._path)

    def clear(self) -> None:
        with contextlib.suppress(FileNotFoundError):
            self._path.unlink()


class InMemoryTokenStore:
    """Test-only token store. Ships in production code so callers who don't
    want disk persistence (ad-hoc scripts, ephemeral containers) can pass
    one in without subclassing.
    """

    def __init__(self) -> None:
        self._tokens: TokenSet | None = None

    def load(self) -> TokenSet | None:
        return self._tokens

    def save(self, tokens: TokenSet) -> None:
        self._tokens = tokens

    def clear(self) -> None:
        self._tokens = None
