# Contributing

Thanks for considering a contribution. Here's what you need to know.

## Setup

```bash
git clone https://github.com/piotrlinski/allegro-open-mcp-server
cd allegro-open-mcp-server
uv sync --extra dev
pre-commit install
```

## Workflow

```bash
# Make your changes, then:
make format              # apply ruff fixes + formatting
make lint                # ruff check + ruff format --check + mypy --strict
make test                # run the full pytest suite

# Re-run codegen if you touched the OpenAPI spec or the generators:
make gen-models
make gen-tools
make check-models-freshness  # only warns; never fails CI
```

CI re-runs the same checks on Python 3.10, 3.11, 3.12. PRs that fail any
of them are unlikely to merge.

## Code style

* Ruff (with `select = ["E","F","I","B","UP","SIM","T20","A","RUF","PERF","PT"]`).
* mypy `--strict` for everything except the codegen output and a few
  documented per-module exemptions.
* Module docstrings explain *why* the module exists; class/function
  docstrings explain *non-obvious behaviour*. We keep comments terse and
  reserve them for hidden constraints, not narration.
* No emojis in source unless explicitly requested.

## The architecture boundary

`allegro_client` is designed to be liftable into its own PyPI package
later. It must NOT import `fastmcp`, `mcp`, or anything from
`allegro_mcp.*`. `tests/unit/test_architecture.py` enforces this.

If you find yourself wanting to break the boundary, lift the dependency
*upward* into `allegro_mcp.*` instead.

## Adding a new tool

Tools come from two sources:

1. **Generated tools** (most of them) — emitted by `scripts/gen_tools.py`
   from `paths.*` in the cached OpenAPI spec. Don't hand-edit the
   resulting modules; re-run `make gen-tools` instead.
2. **Hand-written tools** (auth status, login, revoke) — live in
   `src/allegro_mcp/tools/auth.py`. New hand-written tools go in their
   own module. Decorator stack: `@mcp.tool` → `@allegro_call` →
   optional guards (`@require_nonempty`, `@requires_scope`,
   `@requires_writes_enabled`).

Add the new module's side-effect import to `src/allegro_mcp/tools/__init__.py`
so it registers at server startup.

## Bumping the OpenAPI spec

```bash
make gen-models                 # downloads + codegen + commits diff
make check-models-freshness     # confirms cache matches upstream
make gen-tools                  # regenerates tool modules
make test
```

Review the diffs in `src/allegro_client/models/_generated/models.py` and
in the generated tool modules. Codegen is deterministic (we pass
`--disable-timestamp`); meaningful diffs reflect real spec changes.

## Commit style

Conventional Commits-ish (`feat:`, `fix:`, `docs:`, `refactor:`, `chore:`,
`test:`). Don't tag the AI assistant.

## License

By contributing you agree your work ships under the [MIT license](LICENSE).
