"""Entrypoint for the Allegro MCP server.

Kept tiny so the console-script declared in ``pyproject.toml``
(``allegro-mcp = allegro_mcp.server:main``) keeps pointing at the same
place across releases. All meaningful logic — tool definitions, request
signing, response parsing, models — lives in submodules.

``main()`` does five things, in order:

1. parse CLI args (with env-var fallbacks),
2. configure file-based logging (stdout is reserved for the MCP transport),
3. build the typed configs and fail fast on missing credentials,
4. import :mod:`allegro_mcp.tools` (which registers every ``@mcp.tool``),
5. run the FastMCP loop on stdio.

Credentials can come from CLI flags or env vars; flags take precedence.
"""

from __future__ import annotations

import argparse
import logging
import os
import sys
from typing import Any

from pydantic import SecretStr, ValidationError

from allegro_client import AllegroClientConfig

from . import tools as _tools  # noqa: F401 — side-effect import (registers @mcp.tool).
from .config import AllegroMCPConfig
from .logging import setup_logging
from .tools._runtime import close_client, init_client, mcp

logger = logging.getLogger(__name__)


def _env_default(name: str, default: str | None = None) -> str | None:
    """Read ``$ALLEGRO_<NAME>`` for argparse fallback defaults."""
    return os.environ.get(f"ALLEGRO_{name}", default)


def _build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="allegro-mcp",
        description=(
            "MCP server for the Allegro REST API (allegro.pl). Speaks MCP over "
            "stdio; works with any MCP-aware client (Claude Desktop, Claude Code, "
            "MCP Inspector, …). All flags fall back to ALLEGRO_* env vars."
        ),
    )
    parser.add_argument("--client-id", default=_env_default("CLIENT_ID"))
    parser.add_argument("--client-secret", default=_env_default("CLIENT_SECRET"))
    parser.add_argument(
        "--auth-flow",
        default=_env_default("AUTH_FLOW"),
        choices=["device", "authcode", "client_credentials", "refresh_token", None],
        help="OAuth flow to use. See README.md for guidance.",
    )
    parser.add_argument("--refresh-token", default=_env_default("REFRESH_TOKEN"))
    parser.add_argument("--redirect-uri", default=_env_default("REDIRECT_URI"))
    parser.add_argument(
        "--environment",
        default=_env_default("ENVIRONMENT", "production"),
        choices=["production", "sandbox"],
    )
    parser.add_argument(
        "--enable-writes",
        default=None,
        action=argparse.BooleanOptionalAction,
        help="Gate high-blast-radius write tools. Default: false (env: ALLEGRO_ENABLE_WRITES).",
    )
    return parser


def main(argv: list[str] | None = None) -> None:
    """Console-script entrypoint."""
    args = _build_arg_parser().parse_args(argv)

    log_file = setup_logging()
    logger.info("Allegro MCP server starting; logs at %s", log_file)

    try:
        # Build kwargs dynamically: any flag the operator left unset falls
        # through to env-var loading inside BaseSettings. ``Any`` typed because
        # BaseSettings doesn't expose a static __init__ signature mypy can use.
        client_kwargs: dict[str, Any] = {}
        if args.client_id:
            client_kwargs["client_id"] = args.client_id
        if args.client_secret:
            client_kwargs["client_secret"] = SecretStr(args.client_secret)
        if args.auth_flow:
            client_kwargs["auth_flow"] = args.auth_flow
        if args.refresh_token:
            client_kwargs["refresh_token"] = SecretStr(args.refresh_token)
        if args.redirect_uri:
            client_kwargs["redirect_uri"] = args.redirect_uri
        if args.environment:
            client_kwargs["environment"] = args.environment
        client_config = AllegroClientConfig(**client_kwargs)

        mcp_kwargs: dict[str, Any] = {}
        if args.enable_writes is not None:
            mcp_kwargs["enable_writes"] = bool(args.enable_writes)
        mcp_config = AllegroMCPConfig(**mcp_kwargs)
    except ValidationError as exc:
        missing = ", ".join(
            f"--{str(err['loc'][0]).replace('_', '-')}" if err.get("loc") else "--?"
            for err in exc.errors()
        )
        logger.error("Startup aborted: missing/invalid configuration (%s)", missing)
        # Print to stderr — stdout is reserved for the MCP protocol stream.
        print(
            f"\nallegro-mcp: missing/invalid configuration ({missing}).\n"
            "Pass them as CLI flags or set the corresponding ALLEGRO_* env vars.\n"
            "See .env.example for the full list.\n",
            file=sys.stderr,
            flush=True,
        )
        raise SystemExit(2) from exc

    init_client(client_config, mcp_config)

    try:
        mcp.run()  # stdio transport — what MCP clients expect.
    finally:
        close_client()


if __name__ == "__main__":
    main()
