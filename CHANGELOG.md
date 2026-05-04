# Changelog

All notable changes to this project are documented here. The format
follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and
this project adheres to [Semantic Versioning](https://semver.org/).

## [Unreleased]

## [0.1.0] — 2026-05-04

Initial alpha release. Two-package layout (`allegro_client` SDK +
`allegro_mcp` FastMCP wrapper) with full coverage of the Allegro REST
API surface.

### Added

* **`allegro_client` SDK** — MCP-agnostic Allegro REST client.
  * `AllegroClientConfig` with env-var loading (`ALLEGRO_*` prefix),
    secret masking, environment-derived base URLs.
  * `AllegroError` exception hierarchy with subclasses for the common
    HTTP failure modes (`AuthError`, `RateLimitError`, `NotFoundError`,
    `ValidationError`, `ConflictError`, `ServerError`, …).
  * Four OAuth strategies: Device Code, Authorization Code with PKCE,
    Client Credentials, pre-shared refresh token. Shared refresh-on-401
    + atomic-rotation persistence via `FileTokenStore`.
  * Synchronous `AllegroClient` wrapping `httpx.Client` with versioned
    media-type negotiation (`application/vnd.allegro.public.v1+json`,
    beta variants), 429 + 5xx + network retry transport, request_id
    threading, and offset/limit + cursor pagination iterators.
  * 1 152+ Pydantic models codegen'd from Allegro's official OpenAPI 3.0
    spec at `https://developer.allegro.pl/swagger.yaml`.
* **`allegro_mcp` server** — FastMCP wrapper over `allegro_client`.
  * 268 MCP tools (3 hand-written auth tools + 265 generated) covering
    every operation in the spec.
  * `ErrorResponse` envelope + `map_error()` translator from SDK
    exceptions.
  * Decorators: `@allegro_call`, `@require_nonempty`, `@requires_scope`,
    `@requires_writes_enabled`.
  * File-rotating logger that never writes to stdout/stderr (MCP stdio
    safety).
  * `allegro-mcp` console script with argparse + env-var fallbacks and
    fail-fast credential validation.
* **Tooling** — multi-stage Docker build, GitHub Actions CI matrix on
  Python 3.10/3.11/3.12, pre-commit hooks, MkDocs Material docs site,
  `Makefile` targets for codegen / docs / Docker / lint / test.
* **Tests** — 250+ unit tests including round-trip of the codegen
  models, respx-mocked OAuth flows, layer-dependency enforcement, and
  the load-bearing extractability test (`allegro_client` doesn't import
  `fastmcp`/`mcp`/`allegro_mcp.*`).
