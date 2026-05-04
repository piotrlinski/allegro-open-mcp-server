# Extract the standalone client

The repo's two-package layout (`allegro_client` MCP-agnostic + `allegro_mcp`
FastMCP wrapper) is designed to make the future split into a standalone
`allegro-client` PyPI distribution a mechanical operation.

The boundary is enforced from day one by
[`tests/unit/test_architecture.py`](https://github.com/piotrlinski/allegro-open-mcp-server/blob/master/tests/unit/test_architecture.py)
which fails CI if `allegro_client` ever imports `fastmcp`, `mcp`, or
`allegro_mcp.*`.

## Steps

1. **Move** `src/allegro_client/` into a new repo:

   ```bash
   git mv src/allegro_client/ /path/to/allegro-client/src/allegro_client/
   ```

2. **Create** a minimal `pyproject.toml` for the new package:

   ```toml
   [project]
   name = "allegro-client"
   version = "0.1.0"
   requires-python = ">=3.10"
   dependencies = ["httpx>=0.27", "pydantic>=2.7", "pydantic-settings>=2.0"]

   [build-system]
   requires = ["hatchling"]
   build-backend = "hatchling.build"

   [tool.hatch.build.targets.wheel]
   packages = ["src/allegro_client"]
   ```

3. **Update** `allegro-mcp`'s `pyproject.toml`: remove
   `src/allegro_client` from the wheel packages, add
   `allegro-client>=0.1` to `dependencies`.

4. **Re-run** `uv sync` and the test suite. Imports inside `allegro_mcp/`
   already say `from allegro_client.…` — nothing changes.

The architecture test will fail to find the `allegro_client/` directory
under `src/` after the move; either move the test along with the SDK or
update its `SRC` constant in the MCP repo.
