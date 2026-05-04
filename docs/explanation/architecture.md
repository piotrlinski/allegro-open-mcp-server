# Architecture

## Two-package layout

```text
src/
├── allegro_client/              # MCP-agnostic; future PyPI package
│   ├── config.py                # AllegroClientConfig
│   ├── errors.py                # AllegroError hierarchy + ErrorDetail
│   ├── auth/                    # 4 OAuth strategies + TokenStore
│   ├── http/                    # AllegroClient + retry + pagination
│   └── models/_generated/       # codegen Pydantic from OpenAPI
└── allegro_mcp/                 # FastMCP wrapper; depends on allegro_client
    ├── config.py                # AllegroMCPConfig (composes the SDK config)
    ├── errors.py                # ErrorResponse envelope + map_error()
    ├── logging.py               # file-rotating logger (stdout reserved for MCP)
    ├── server.py                # argparse → bootstrap → mcp.run()
    └── tools/                   # 268 @mcp.tool functions
        ├── _runtime.py          # FastMCP instance + lifecycle + allegro_call
        ├── _decorators.py       # require_nonempty, requires_scope, requires_writes_enabled
        ├── auth.py              # hand-written: auth_status, auth_login_device, auth_revoke
        └── *.py                 # ~50 modules, generated from OpenAPI tags
```

## Layered dependencies

```text
allegro_client.config → allegro_client.errors → allegro_client.auth →
  allegro_client.http → allegro_client.models
```

```text
allegro_mcp.config → allegro_mcp.errors → allegro_mcp.logging →
  allegro_mcp.tools._runtime → allegro_mcp.tools.* → allegro_mcp.server
```

Cross-package: `allegro_mcp.*` may import `allegro_client.*`. The reverse
is forbidden — a load-bearing test in
[`tests/unit/test_architecture.py`](https://github.com/piotrlinski/allegro-open-mcp-server/blob/master/tests/unit/test_architecture.py)
walks every `.py` file under `src/`, parses imports, and fails CI on any
upward edge.

## Why the boundary

The `allegro_client` package is designed to be lifted into its own PyPI
distribution later. Anyone running into a need for a plain Python
Allegro REST client (no MCP) should be able to depend on `allegro-client`
in their own project. Keeping FastMCP/MCP imports out from day one makes
that split a 30-minute mechanical move rather than a refactor.

See [Extract the standalone client](../how-to/extract-allegro-client.md).

## OpenAPI-driven model layer

Allegro publishes the canonical REST spec at
`https://developer.allegro.pl/swagger.yaml` (OpenAPI 3.0, ~39 kLOC). We
codegen Pydantic v2 models from it via
[datamodel-code-generator](https://github.com/koxudaxi/datamodel-code-generator)
into `src/allegro_client/models/_generated/`. Output is committed and
reviewed in PRs.

Drift detection: each codegen run stamps a SHA-256 banner in the output's
`__init__.py`; `make check-models-freshness` warns if the upstream spec
has moved.

## Tool generation

`scripts/gen_tools.py` reads the same spec and emits one tool function
per `(method, path)` operation, grouped by tag. ~265 generated tools +
3 hand-written auth tools = **268 MCP tools** out of the box. Tools call
the typed `AllegroClient.request_json(...)` and return
`dict[str, Any] | ErrorResponse`.

Re-run with `make gen-tools` whenever the OpenAPI spec changes.
