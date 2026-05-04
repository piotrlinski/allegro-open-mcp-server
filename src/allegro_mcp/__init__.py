"""MCP server for the Allegro REST API.

Wraps :mod:`allegro_client` (the MCP-agnostic SDK) with FastMCP tools.
Importing this package registers tools as a side effect of
:mod:`allegro_mcp.tools` being imported by :mod:`allegro_mcp.server`.
"""

from __future__ import annotations

from allegro_client import __version__

__all__ = ["__version__"]
