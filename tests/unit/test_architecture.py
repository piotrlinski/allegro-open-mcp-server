"""Architecture-level invariants enforced as tests.

Two boundaries we never want to leak across:

1. **Layered dependency direction** — within each top-level package
   (``allegro_client`` and ``allegro_mcp``), modules can only import from
   layers below them. Upward imports create cycles and tangle responsibilities.

2. **Extractability** — :mod:`allegro_client` is designed to be liftable
   into its own PyPI package later. It must NOT import:
     * the MCP wrapper package (``allegro_mcp``),
     * any MCP framework module (``fastmcp``, ``mcp``).

The tests parse imports out of the source — no clever AST analysis, just
``ast.walk`` — and assert the dependency graph stays within the rules.
"""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
SRC = REPO_ROOT / "src"


# Within ``allegro_client``: modules at index N may only import from modules
# at indexes 0..N. ``models._generated`` is treated as part of the ``models``
# layer for boundary purposes.
CLIENT_LAYERS = [
    "version",
    "errors",
    "config",
    "auth.store",
    "auth.base",
    "auth",
    "http.media_types",
    "http.retry",
    "http.client",
    "http.pagination",
    "http",
    "models.common",
    "models",
]

# Within ``allegro_mcp``: similar rules. ``tools._runtime`` may import from
# the MCP foundation; tools modules import from ``_runtime``.
MCP_LAYERS = [
    "config",
    "errors",
    "logging",
    "tools._runtime",
    "tools._decorators",
    "tools",
    "server",
]


def _iter_python_files(root: Path) -> list[Path]:
    return [p for p in root.rglob("*.py") if "_generated" not in p.parts]


def _module_imports(path: Path) -> list[str]:
    tree = ast.parse(path.read_text())
    out: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            out.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            # Resolve relative imports against the file's own package path.
            level = node.level
            if level:
                parts = path.relative_to(SRC).with_suffix("").parts
                base = parts[: len(parts) - level]
                out.append(".".join((*base, node.module)))
            else:
                out.append(node.module)
    return out


# ---- Cross-package extractability ------------------------------------------


class TestExtractability:
    """``allegro_client`` must stay MCP-agnostic.

    These are the load-bearing boundary tests for the future-package split.
    Breaking either of them means ``allegro_client`` is no longer liftable
    into its own distribution without code changes.
    """

    @pytest.mark.parametrize(
        "path", _iter_python_files(SRC / "allegro_client"), ids=lambda p: p.name
    )
    def test_does_not_import_mcp_wrapper(self, path: Path) -> None:
        bad = [
            imp
            for imp in _module_imports(path)
            if imp == "allegro_mcp" or imp.startswith("allegro_mcp.")
        ]
        assert bad == [], (
            f"{path.relative_to(REPO_ROOT)} imports the MCP wrapper "
            f"({bad}); allegro_client must stay MCP-agnostic so it can be "
            f"extracted into its own package later."
        )

    @pytest.mark.parametrize(
        "path", _iter_python_files(SRC / "allegro_client"), ids=lambda p: p.name
    )
    def test_does_not_import_fastmcp(self, path: Path) -> None:
        bad = [
            imp
            for imp in _module_imports(path)
            if imp in {"fastmcp", "mcp"} or imp.startswith(("fastmcp.", "mcp."))
        ]
        assert bad == [], (
            f"{path.relative_to(REPO_ROOT)} imports an MCP framework module "
            f"({bad}); allegro_client must stay MCP-agnostic."
        )


# ---- Layered dependency direction -----------------------------------------


def _layer_index(layers: list[str], qualname: str) -> int | None:
    """Return the highest layer index that ``qualname`` is part of, or None."""
    best: int | None = None
    for idx, layer in enumerate(layers):
        if qualname == layer or qualname.startswith(f"{layer}."):
            best = idx
    return best


class TestClientLayering:
    """``allegro_client`` modules can only import from layers at or below them."""

    @pytest.mark.parametrize(
        "path", _iter_python_files(SRC / "allegro_client"), ids=lambda p: p.name
    )
    def test_imports_only_lower_layers(self, path: Path) -> None:
        rel = path.relative_to(SRC / "allegro_client").with_suffix("")
        if rel.name == "__init__":
            self_qual = ".".join(rel.parent.parts) or "__init__"
        else:
            self_qual = ".".join(rel.parts)
        if self_qual.startswith("models._generated"):
            return  # generated layer — no assertions.
        self_idx = _layer_index(CLIENT_LAYERS, self_qual)
        if self_idx is None:
            return  # not part of the layer table (e.g. __init__ at root).

        violations: list[str] = []
        for imp in _module_imports(path):
            if not imp.startswith("allegro_client."):
                continue
            tail = imp[len("allegro_client.") :]
            if tail.startswith("models._generated"):
                continue
            target_idx = _layer_index(CLIENT_LAYERS, tail)
            if target_idx is not None and target_idx > self_idx:
                violations.append(f"{tail} (layer {target_idx}) > self (layer {self_idx})")
        assert violations == [], (
            f"{path.relative_to(REPO_ROOT)} imports from a higher layer: "
            f"{violations}. Refactor so dependencies point downward only."
        )


class TestMCPLayering:
    """``allegro_mcp`` modules can only import from layers at or below them."""

    @pytest.mark.parametrize("path", _iter_python_files(SRC / "allegro_mcp"), ids=lambda p: p.name)
    def test_imports_only_lower_layers(self, path: Path) -> None:
        rel = path.relative_to(SRC / "allegro_mcp").with_suffix("")
        if rel.name == "__init__":
            self_qual = ".".join(rel.parent.parts) or "__init__"
        else:
            self_qual = ".".join(rel.parts)
        # Generated tool modules are siblings of `_runtime` etc. We treat
        # them at the ``tools`` layer.
        if self_qual.startswith("tools.") and self_qual not in (
            "tools._runtime",
            "tools._decorators",
            "tools",
        ):
            self_qual = "tools"
        self_idx = _layer_index(MCP_LAYERS, self_qual)
        if self_idx is None:
            return

        violations: list[str] = []
        for imp in _module_imports(path):
            if not imp.startswith("allegro_mcp."):
                continue
            tail = imp[len("allegro_mcp.") :]
            target_idx = _layer_index(MCP_LAYERS, tail)
            if target_idx is not None and target_idx > self_idx:
                violations.append(f"{tail} (layer {target_idx}) > self (layer {self_idx})")
        assert violations == [], (
            f"{path.relative_to(REPO_ROOT)} imports from a higher layer: {violations}."
        )
