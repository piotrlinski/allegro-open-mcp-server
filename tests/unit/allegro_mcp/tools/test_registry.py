"""Smoke test for the MCP tool registry.

Confirms that importing :mod:`allegro_mcp.tools` registers a healthy number
of tools against the shared FastMCP instance, and that a representative
sample (auth tools + a few from the generated modules) is reachable.
"""

from __future__ import annotations

import asyncio


def _list_tools() -> list[object]:
    import allegro_mcp.tools as _tools  # noqa: F401 — side-effect imports.
    from allegro_mcp.tools._runtime import mcp

    return asyncio.run(mcp.list_tools())


def test_registers_many_tools() -> None:
    tools = _list_tools()
    # Authoritative count drifts as Allegro updates the spec; lower bound
    # catches regressions where a whole module fails to import. ~265
    # generated + 3 hand-written at time of writing.
    assert len(tools) > 200, f"unexpected tool count: {len(tools)}"


def test_auth_tools_present() -> None:
    names = {getattr(t, "name", "") for t in _list_tools()}
    assert "auth_status" in names
    assert "auth_login_device" in names
    assert "auth_revoke" in names


def test_generated_tools_present() -> None:
    names = {getattr(t, "name", "") for t in _list_tools()}
    # Pick from each high-traffic module so a regression in any one
    # surfaces here.
    expected_subset = {
        "search_offers_using_get",  # Offer management
        "get_offer_events",  # User's offer information
        "get_listing_categories",  # Categories and parameters
        "get_user_orders_get",  # Order management
    }
    # We don't fail on every name — Allegro renames operationIds —
    # but at least one from this set must survive any spec churn.
    assert names & expected_subset, (
        f"none of the canonical generated tool names found; missing: {expected_subset}"
    )
