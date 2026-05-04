# Security

## Reporting a vulnerability

Please **do not** open a public issue for security-sensitive matters.

Instead:

1. Email the maintainer directly: piotrklinski@gmail.com.
2. Include enough detail to reproduce: affected versions, attack vector,
   and ideally a proof-of-concept payload.
3. Expect an acknowledgement within 72 hours.

If a fix needs coordinated disclosure, we'll agree on a timeline (90 days
default) and credit you in the changelog.

## Security model

This server holds OAuth credentials (`client_id`, `client_secret`,
refresh tokens). It is intended to run **on the operator's machine or in
a controlled container**, not as a multi-tenant service. Threat scope:

* **In scope**: secret leakage via logs, stdout, repr, or tracebacks;
  token-store file permissions; refresh-token rotation; sandbox/prod
  config bleed; write-gate bypasses; OAuth-flow CSRF (state mismatches).
* **Out of scope**: a malicious operator (this is a tool *for* the
  operator); compromised host; supply-chain attacks on the Python
  ecosystem (we lock dependencies via `uv.lock`).

## Practices in place

* Secrets are `pydantic.SecretStr` — masked in `repr()`, never logged.
* Token store: atomic write (`tmpfile + os.replace`), mode `0600`.
* Refresh tokens rotate on every refresh; the store overwrites
  atomically.
* `auth_revoke` clears the on-disk store and the in-memory cache.
* MCP transport is stdio; the logger writes only to a rotating file —
  never to stdout/stderr — to avoid corrupting the protocol stream and
  to avoid leaking secrets through accidental logging.
* The Authorization Code flow uses **PKCE S256** with a fresh
  `state` per attempt; the localhost callback handler verifies the
  `state` matches before accepting the authorisation code.
* High-blast-radius mutating tools (`offer_delete`, `payment_refund`,
  `auction_place_bid`, `order_set_status`, `commission_refund_*`) are
  visible-but-disabled by default; they require an explicit
  `ALLEGRO_ENABLE_WRITES=true` flip.
* `tests/unit/test_architecture.py` blocks `allegro_client` from
  importing the MCP wrapper or any MCP framework module — protects the
  future package-extraction boundary, also keeps the SDK's surface
  free of unexpected runtime dependencies.

## Things to know if you're auditing

* OAuth scopes are negotiated at first acquire; the cached scope set is
  read by `@requires_scope` for fail-fast guards.
* Refresh-on-401 is mutex-guarded so concurrent in-flight 401s don't
  trigger double refreshes.
* `httpx.Client` uses connection pooling per process; tokens travel only
  to the API host (`api.allegro.pl` or sandbox equivalent) and the
  OAuth host (`allegro.pl`). No third-party telemetry endpoints exist
  in this codebase.
