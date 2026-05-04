"""Allow ``python -m allegro_mcp`` as an alias for the console script."""

from __future__ import annotations

from .server import main

if __name__ == "__main__":
    main()
