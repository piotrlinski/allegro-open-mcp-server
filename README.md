# allegro-mcp

[![CI](https://github.com/piotrlinski/allegro-open-mcp-server/actions/workflows/ci.yml/badge.svg)](https://github.com/piotrlinski/allegro-open-mcp-server/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

A Python [MCP](https://modelcontextprotocol.io/) server for the
[Allegro REST API](https://developer.allegro.pl/), backed by a
**separable `allegro_client` SDK** under the hood.

```text
src/
├── allegro_client/    # MCP-agnostic — extractable as its own PyPI package
└── allegro_mcp/       # FastMCP wrapper exposing 268 tools
```

## What you get

* **268 MCP tools** spanning all ~30 Allegro resource groups (offers,
  orders, shipments, messaging, billing, returns, disputes, payments,
  promotions, fulfillment, …).
* **Four OAuth flows**: Device Code (recommended for MCP), Authorization
  Code with PKCE, Client Credentials, and pre-shared refresh token.
* **Persistent token store** at `~/.allegro-mcp/tokens.json` (mode `0600`,
  atomic writes, refresh-token rotation handled automatically).
* **Sandbox + production** environments with a single env-var flip.
* **Write gate** — high-blast-radius mutating tools refuse to fire unless
  `ALLEGRO_ENABLE_WRITES=true`. Default is read-mostly safe.
* **Generated Pydantic models** codegen'd from Allegro's official
  OpenAPI 3.0 spec via [datamodel-code-generator](https://github.com/koxudaxi/datamodel-code-generator).
* **Production-grade tooling**: mypy `--strict`, ruff, pre-commit hooks,
  multi-stage Docker build, GitHub Actions CI on Python 3.10/3.11/3.12.
* **250+ unit tests**, including a layer-enforcement test that protects
  the future package-extraction boundary.

## Quickstart

```bash
git clone https://github.com/piotrlinski/allegro-open-mcp-server
cd allegro-open-mcp-server

uv sync --extra dev
cp .env.example .env             # fill in ALLEGRO_CLIENT_ID, ALLEGRO_CLIENT_SECRET, ALLEGRO_AUTH_FLOW
uv run allegro-mcp               # speaks MCP over stdio
```

On first run with `ALLEGRO_AUTH_FLOW=device`, the server prints a
verification URL + user code to stderr; approve in your browser and the
refresh token persists for next time.

Full walkthrough → [docs/tutorials/quickstart.md](docs/tutorials/quickstart.md).

## Authentication

| Flow | When to use |
| --- | --- |
| `device` (recommended) | Headless MCP server; first run prints URL+code to stderr |
| `authcode` | Operator on the same host; spawns localhost callback listener |
| `client_credentials` | App-only access to public resources only |
| `refresh_token` | Pre-shared refresh token, no interactive auth |

Pick one with [docs/how-to/oauth-flows.md](docs/how-to/oauth-flows.md).

## MCP client setup

* **Claude Desktop** — [docs/how-to/with-claude-desktop.md](docs/how-to/with-claude-desktop.md)
* **Claude Code** — [docs/how-to/with-claude-code.md](docs/how-to/with-claude-code.md)
* **MCP Inspector** — `make inspector`

## Development

```bash
make sync                  # install dev dependencies
make test                  # run pytest (250+ tests)
make lint                  # ruff + mypy --strict
make format                # apply ruff formatting + auto-fixes
make gen-models            # regenerate Pydantic models from the OpenAPI spec
make gen-tools             # regenerate MCP tool modules from the spec
make check-models-freshness   # warn if upstream spec moved
make build                 # build the Docker image
make run                   # run the server in Docker (stdio)
make inspector             # run MCP Inspector against the Docker image
make docs-serve            # live-reload docs at http://127.0.0.1:8000
```

## Architecture

Two packages, one wheel today, two future PyPI distributions:

```text
allegro_client.config → allegro_client.errors → allegro_client.auth →
  allegro_client.http → allegro_client.models           # MCP-agnostic SDK

allegro_mcp.config → allegro_mcp.errors → allegro_mcp.logging →
  allegro_mcp.tools → allegro_mcp.server                # FastMCP wrapper
```

The boundary is enforced by `tests/unit/test_architecture.py` — CI fails
if `allegro_client` ever imports `fastmcp`, `mcp`, or `allegro_mcp.*`.

Read more: [docs/explanation/architecture.md](docs/explanation/architecture.md)

## Contributing

PRs welcome. See [CONTRIBUTING.md](CONTRIBUTING.md).

## Security

Found a vulnerability? Please follow [SECURITY.md](SECURITY.md).

## License

[MIT](LICENSE) — community project; not affiliated with Grupa Allegro.
