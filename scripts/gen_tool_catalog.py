#!/usr/bin/env python3
"""Emit a markdown table of every registered MCP tool.

Output: ``docs/reference/tool-catalog.md``. Re-run from ``make docs-gen``.
The catalog is gitignored — it's regenerated on every docs build.
"""

from __future__ import annotations

import asyncio
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
OUT = REPO_ROOT / "docs" / "reference" / "tool-catalog.md"


async def collect() -> list[tuple[str, str]]:
    import allegro_mcp.tools as _tools  # noqa: F401 — side-effect imports.
    from allegro_mcp.tools._runtime import mcp

    tools = await mcp.list_tools()
    rows: list[tuple[str, str]] = []
    for tool in tools:
        name = getattr(tool, "name", "?")
        description = (getattr(tool, "description", "") or "").strip()
        # Keep table cells short — first sentence only.
        first_line = description.splitlines()[0] if description else ""
        rows.append((name, first_line))
    rows.sort()
    return rows


def main() -> int:
    rows = asyncio.run(collect())
    OUT.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Tool catalog",
        "",
        "Auto-generated from the registered ``@mcp.tool`` set. Re-run via",
        "``make docs-gen``.",
        "",
        f"**{len(rows)} tools registered.**",
        "",
        "| Tool | Summary |",
        "| --- | --- |",
    ]
    for name, summary in rows:
        # Escape pipes inside the summary so the table doesn't break.
        clean = summary.replace("|", "\\|")
        lines.append(f"| `{name}` | {clean} |")
    OUT.write_text("\n".join(lines) + "\n")
    print(f"✓ wrote {OUT.relative_to(REPO_ROOT)} ({len(rows)} tools)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
