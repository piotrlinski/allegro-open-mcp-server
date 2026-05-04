# Allegro MCP

A Python [MCP](https://modelcontextprotocol.io/) server for the
[Allegro REST API](https://developer.allegro.pl/), backed by a
**separable `allegro_client` SDK** under the hood.

```text
src/
├── allegro_client/    # MCP-agnostic — extractable as its own PyPI package
└── allegro_mcp/       # FastMCP wrapper that exposes ~265 tools
```

## What you get

* All ~30 Allegro resource groups exposed as MCP tools (offers, orders,
  shipments, messaging, billing, returns, disputes, payments, …).
* Four OAuth flows: Device Code (recommended), Authorization Code with
  PKCE, Client Credentials, and pre-shared refresh token.
* Persistent token store at `~/.allegro-mcp/tokens.json` so refresh
  tokens survive restarts.
* Sandbox + production environments out of the box.
* A write-gate (`ALLEGRO_ENABLE_WRITES=true`) that keeps mutating tools
  visible-but-disabled until the operator opts in.
* Generated Pydantic models codegen'd from Allegro's official OpenAPI 3.0
  spec — re-runnable via `make gen-models`.
* Code that's mypy `--strict` clean, ruff clean, and 250+ unit tests.

## Quickstart

```bash
uv sync --extra dev
cp .env.example .env  # fill in ALLEGRO_CLIENT_ID, ALLEGRO_CLIENT_SECRET, ALLEGRO_AUTH_FLOW
uv run allegro-mcp    # speaks MCP over stdio
```

Detailed walkthrough → [Quickstart](tutorials/quickstart.md).

## License

[MIT](https://github.com/piotrlinski/allegro-open-mcp-server/blob/master/LICENSE).
Community project — not affiliated with Grupa Allegro.
