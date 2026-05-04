"""Single source of truth for the package version.

Imported by ``pyproject.toml`` build hooks (when configured) and by the
default User-Agent header in :class:`AllegroClientConfig`. Bump alongside
``[project].version`` when cutting a release.
"""

from __future__ import annotations

__version__ = "0.1.0"
