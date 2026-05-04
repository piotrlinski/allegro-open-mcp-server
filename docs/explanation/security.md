# Security

## Secret hygiene

* `client_secret`, `refresh_token`, and access tokens are stored as
  `pydantic.SecretStr` — never logged, never appear in `repr()`.
* The on-disk token store at `~/.allegro-mcp/tokens.json` is written
  with mode `0600` (owner read/write only) via an atomic
  `tmpfile + os.replace` pattern.
* Refresh tokens **rotate** on every refresh; the store overwrites
  atomically so a crash during refresh can't leave behind a half-written
  file.

## Stdio vs stdout

MCP speaks JSON-RPC over stdio. **Anything written to stdout corrupts
the protocol stream**. The server's logging module
(`allegro_mcp.logging`) attaches only a `TimedRotatingFileHandler`
— never a `StreamHandler`. Interactive OAuth prompts (device-code URLs,
authcode browser-fallback messages) write to **stderr** instead.

A test (`test_no_handler_writes_to_stdout_or_stderr`) iterates the root
logger's handlers and fails if any of them targets `sys.stdout` or
`sys.stderr`.

## Write gate

High-blast-radius mutating tools (`offer_delete`, `payment_refund`,
`auction_place_bid`, `order_set_status`, …) carry a
`@requires_writes_enabled` decorator. Default behaviour: visible-but-disabled,
returning an `ErrorResponse(error="WRITES_DISABLED", …)` until the
operator sets `ALLEGRO_ENABLE_WRITES=true`.

This makes the default posture safe for read-mostly use (e.g. an
agent inspecting orders) while keeping the write path one env-var flip
away.

## Scope minimisation

* `ALLEGRO_SCOPES` controls which OAuth scopes the device/authcode flows
  request. Only ask for what your tools actually need.
* Tools annotated with `@requires_scope("...")` short-circuit before any
  HTTP round-trip if the cached token doesn't carry the scope —
  surfaces scope misconfiguration as a typed `MISSING_SCOPE` error
  instead of a 403 response.

## Sandbox first

`ALLEGRO_ENVIRONMENT=sandbox` swaps both the API and OAuth bases to the
parallel `*.allegrosandbox.pl` namespace. Use it for everything that
mutates state during development.
