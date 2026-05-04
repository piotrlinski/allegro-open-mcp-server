#!/usr/bin/env python3
"""Generate one MCP tool module per OpenAPI tag.

Reads the cached swagger.yaml and emits a single Python module per tag at
``src/allegro_mcp/tools/<module>.py``. Each operation in the spec becomes
one ``@mcp.tool``-decorated function with:

* a snake_case name derived from ``operationId``,
* typed keyword-only arguments built from the operation's parameters
  (path + query) plus an optional ``body`` for write operations,
* a docstring built from the operation's summary / description,
* return type ``dict[str, Any] | ErrorResponse`` (we don't bind to one of
  the 1 200+ generated Pydantic classes because the OpenAPI components map
  inconsistently to operation responses; raw dicts let callers introspect
  cleanly while keeping the generator simple),
* decorators: ``@mcp.tool`` + ``@allegro_call``; write methods (POST,
  PUT, PATCH, DELETE) also stack ``@requires_writes_enabled``.

Run via ``make gen-tools``. Output is committed and reviewed in PRs.
"""

from __future__ import annotations

import re
import sys
import textwrap
from collections import defaultdict
from pathlib import Path
from typing import Any

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
SPEC_PATH = REPO_ROOT / ".cache" / "swagger.yaml"
TOOLS_DIR = REPO_ROOT / "src" / "allegro_mcp" / "tools"

# Methods that mutate state — annotated with @requires_writes_enabled so the
# tool stays visible but refuses to fire unless the operator opted in via
# ALLEGRO_ENABLE_WRITES=true.
_WRITE_METHODS = {"post", "put", "patch", "delete"}

# Tools that don't get the writes-enabled gate even though their HTTP method
# is in _WRITE_METHODS — typically because they only fetch a representation
# (e.g. POST for fee calculation) without persisting state.
_READ_OPERATION_OVERRIDES: frozenset[str] = frozenset(
    {
        # POST endpoints that read but don't mutate the seller's account.
        "calculateFeePreview",
        "calculateFeesUsingPOST",
    }
)


def _camel_to_snake(name: str) -> str:
    """Turn ``getOfferEvents`` into ``get_offer_events``."""
    s1 = re.sub(r"(.)([A-Z][a-z]+)", r"\1_\2", name)
    s2 = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", s1)
    return s2.lower().replace("__", "_")


def _slugify_tag(tag: str) -> str:
    """Turn ``"User's offer information"`` into ``user_offer_information``."""
    cleaned = re.sub(r"[^A-Za-z0-9]+", "_", tag).strip("_").lower()
    if cleaned and cleaned[0].isdigit():
        cleaned = f"_{cleaned}"
    # Avoid stomping on Python keywords / fastmcp internals.
    if cleaned in {"auth", "auth_module"}:
        cleaned = f"{cleaned}_module"
    return cleaned


def _python_type_for(schema: dict[str, Any]) -> str:
    """Map an OpenAPI parameter schema to a Python annotation.

    We don't try to be exhaustive — the goal is "good enough so MCP clients
    see a sane input schema". Anything we don't understand falls back to
    ``str | None`` which any JSON-encodable value satisfies.
    """
    if not schema:
        return "str | None"
    t = schema.get("type")
    if t == "integer":
        return "int | None"
    if t == "number":
        return "float | None"
    if t == "boolean":
        return "bool | None"
    if t == "array":
        return "list[str] | None"
    return "str | None"


_PYTHON_KEYWORDS: frozenset[str] = frozenset(
    {
        "False", "None", "True", "and", "as", "assert", "async", "await",
        "break", "class", "continue", "def", "del", "elif", "else", "except",
        "finally", "for", "from", "global", "if", "import", "in", "is",
        "lambda", "nonlocal", "not", "or", "pass", "raise", "return", "try",
        "while", "with", "yield", "match", "case", "type",
    }
)


def _safe_arg_name(name: str) -> str:
    """Convert ``seller.id`` (a dotted query-param name) into ``seller_id``.

    Allegro's spec uses dotted query params (``seller.id``, ``offer.id``)
    and a few keyword-clashing names (``from``, ``type``). Tools accept
    Python identifiers; the generator maps the identifier back to the
    original dotted key when issuing the request, and trailing-underscores
    keyword clashes (``from`` → ``from_``).
    """
    safe = re.sub(r"[^A-Za-z0-9_]", "_", name)
    if safe in _PYTHON_KEYWORDS or not safe or safe[0].isdigit():
        safe = f"{safe}_"
    return safe


def _docstring(op: dict[str, Any], method: str, path: str) -> str:
    summary = (op.get("summary") or "").strip()
    description = (op.get("description") or "").strip()
    pieces: list[str] = []
    if summary:
        pieces.append(summary)
    if description and description != summary:
        # Keep the first 1500 chars of description to avoid huge docstrings.
        pieces.append(textwrap.shorten(description, width=1500, placeholder="…"))
    pieces.append(f"\nHTTP: ``{method.upper()} {path}``")
    return "\n\n".join(pieces).rstrip()


def _format_docstring(text: str) -> str:
    """Format a docstring body for embedding in a Python source file.

    Allegro descriptions contain ad-hoc backslash sequences (``\\-``,
    ``\\n``) in their HTML markup; embedding the raw text in a regular
    string literal would emit ``SyntaxWarning: invalid escape sequence``
    for each one. The generator collapses backslashes to forward slashes
    so the resulting docstring is just text — no escape interpretation
    needed.
    """
    if not text:
        return '"""Tool generated from the Allegro OpenAPI spec."""'
    # Drop backslashes outright; they're never load-bearing in the
    # human-readable description text.
    cleaned = text.replace("\\", "")
    body = textwrap.indent(cleaned, "    ").lstrip()
    return f'"""{body}\n    """'


def _path_params(op: dict[str, Any], path_item: dict[str, Any]) -> list[dict[str, Any]]:
    seen: set[str] = set()
    out: list[dict[str, Any]] = []
    for source in (path_item.get("parameters", []), op.get("parameters", [])):
        for p in source:
            if not isinstance(p, dict):
                continue
            name = p.get("name")
            if not isinstance(name, str) or name in seen:
                continue
            if p.get("in") == "path":
                seen.add(name)
                out.append(p)
    return out


def _query_params(op: dict[str, Any], path_item: dict[str, Any]) -> list[dict[str, Any]]:
    seen: set[str] = set()
    out: list[dict[str, Any]] = []
    for source in (path_item.get("parameters", []), op.get("parameters", [])):
        for p in source:
            if not isinstance(p, dict):
                continue
            name = p.get("name")
            if not isinstance(name, str) or name in seen:
                continue
            if p.get("in") == "query":
                seen.add(name)
                out.append(p)
    return out


def _has_request_body(op: dict[str, Any]) -> bool:
    return bool(op.get("requestBody"))


def _build_function(
    *,
    operation_id: str,
    method: str,
    path: str,
    op: dict[str, Any],
    path_item: dict[str, Any],
) -> str:
    name = _camel_to_snake(operation_id)
    docstring = _format_docstring(_docstring(op, method, path))
    path_params = _path_params(op, path_item)
    query_params = _query_params(op, path_item)
    has_body = _has_request_body(op)

    # Build the function signature.
    args: list[str] = []
    arg_renames: dict[str, str] = {}  # python identifier → original key.
    for p in path_params:
        original = str(p.get("name") or "")
        identifier = _safe_arg_name(original)
        annotation = _python_type_for(p.get("schema") or {}).replace(" | None", "")
        args.append(f"{identifier}: {annotation}")  # required (no default).
        if identifier != original:
            arg_renames[identifier] = original
    for p in query_params:
        original = str(p.get("name") or "")
        identifier = _safe_arg_name(original)
        annotation = _python_type_for(p.get("schema") or {})
        args.append(f"{identifier}: {annotation} = None")
        if identifier != original:
            arg_renames[identifier] = original
    if has_body:
        args.append("body: dict[str, Any] | None = None")

    # Build the request invocation.
    path_template = path
    for p in path_params:
        original = str(p.get("name") or "")
        identifier = _safe_arg_name(original)
        path_template = path_template.replace(f"{{{original}}}", f"{{{identifier}}}")

    query_lines: list[str] = []
    if query_params:
        for p in query_params:
            original = str(p.get("name") or "")
            identifier = _safe_arg_name(original)
            key = original if "." in original or identifier != original else identifier
            query_lines.append(f'        "{key}": {identifier},')

    body_args = []
    if has_body:
        body_args.append("            json=body,")

    method_upper = method.upper()
    indent = "    "

    # Decorator stack.
    decorators = ["@mcp.tool", "@allegro_call"]
    if method in _WRITE_METHODS and operation_id not in _READ_OPERATION_OVERRIDES:
        decorators.append("@requires_writes_enabled")

    decorator_block = "\n".join(decorators)

    body_lines: list[str] = []
    body_lines.append(f"{indent}{docstring}")
    if query_params:
        body_lines.append(f"{indent}params = {{")
        body_lines.extend(query_lines)
        body_lines.append(f"{indent}}}")
    else:
        body_lines.append(f"{indent}params: dict[str, Any] = {{}}")
    # Cast to dict[str, Any] keeps mypy --strict happy without forcing the
    # client to introspect schemas; if the response is not a JSON object
    # (rare — a few endpoints return arrays) the @allegro_call wrapper
    # will catch the resulting downstream surprise.
    body_lines.append(f"{indent}response = get_client().request_json(")
    body_lines.append(f'{indent}    "{method_upper}",')
    body_lines.append(f'{indent}    f"{path_template}",')
    if has_body:
        body_lines.append(f"{indent}    json=body,")
    body_lines.append(f"{indent}    params=params,")
    body_lines.append(f"{indent})")
    body_lines.append(f"{indent}return cast(dict[str, Any], response)")

    args_str = ", ".join(args) if args else ""
    sig = f"def {name}(*, {args_str}) -> dict[str, Any] | ErrorResponse:" if args_str \
        else f"def {name}() -> dict[str, Any] | ErrorResponse:"

    return decorator_block + "\n" + sig + "\n" + "\n".join(body_lines) + "\n"


_MODULE_HEADER = '''# ruff: noqa
"""Generated MCP tools — DO NOT EDIT.

Run ``make gen-tools`` to regenerate from the cached OpenAPI spec.
Tag: {tag}
"""

from __future__ import annotations

from typing import Any, cast

from ..errors import ErrorResponse
from ._decorators import requires_writes_enabled
from ._runtime import allegro_call, get_client, mcp


'''


def _emit_module(tag: str, operations: list[dict[str, Any]]) -> str:
    parts = [_MODULE_HEADER.format(tag=tag)]
    for entry in operations:
        parts.append(
            _build_function(
                operation_id=entry["operationId"],
                method=entry["method"],
                path=entry["path"],
                op=entry["op"],
                path_item=entry["path_item"],
            )
        )
        parts.append("\n")
    return "".join(parts)


def main() -> int:
    spec = yaml.safe_load(SPEC_PATH.read_text())
    operations: dict[str, list[dict[str, Any]]] = defaultdict(list)
    seen_ids: set[str] = set()

    for path, path_item in spec.get("paths", {}).items():
        if not isinstance(path_item, dict):
            continue
        for method, op in path_item.items():
            if method not in {"get", "post", "put", "patch", "delete"}:
                continue
            if not isinstance(op, dict):
                continue
            operation_id = op.get("operationId") or f"{method}_{re.sub(r'[^a-zA-Z0-9]+', '_', path)}"
            tag = (op.get("tags") or ["misc"])[0]
            module_name = _slugify_tag(tag)
            if operation_id in seen_ids:
                # OpenAPI sometimes has duplicates; suffix to keep names unique.
                operation_id = f"{operation_id}_{method}"
            seen_ids.add(operation_id)
            operations[module_name].append(
                {
                    "operationId": operation_id,
                    "method": method,
                    "path": path,
                    "op": op,
                    "path_item": path_item,
                    "tag": tag,
                }
            )

    # Wipe any previously-generated tool modules but keep the hand-written
    # ones (auth.py, _runtime.py, _decorators.py, __init__.py).
    keep = {"auth.py", "_runtime.py", "_decorators.py", "__init__.py"}
    for existing in TOOLS_DIR.glob("*.py"):
        if existing.name not in keep:
            existing.unlink()

    written: list[str] = []
    for module, ops in sorted(operations.items()):
        if not module:
            continue
        out = TOOLS_DIR / f"{module}.py"
        out.write_text(_emit_module(ops[0]["tag"], ops))
        written.append(module)

    # Update tools/__init__.py with side-effect imports.
    init = TOOLS_DIR / "__init__.py"
    init_lines = [
        '"""MCP tool registry.',
        "",
        "Importing this package side-effect-registers every ``@mcp.tool`` against",
        "the shared ``mcp`` instance in :mod:`allegro_mcp.tools._runtime`.",
        '"""',
        "",
        "from __future__ import annotations",
        "",
        "# Hand-written.",
        "from . import auth as _auth  # noqa: F401",
        "",
        "# Generated by ``make gen-tools`` from the OpenAPI spec.",
    ]
    for module in sorted(written):
        init_lines.append(f"from . import {module} as _{module}  # noqa: F401")
    init.write_text("\n".join(init_lines) + "\n")

    print(f"✓ wrote {len(written)} tool modules covering {sum(len(v) for v in operations.values())} operations")
    return 0


if __name__ == "__main__":
    sys.exit(main())
