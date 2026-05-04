# Pick an OAuth flow

Allegro supports four OAuth 2.0 flows; this server supports all four. Pick
based on where the server runs and how often a human can step in.

| Flow | When to use | First-run UX |
| --- | --- | --- |
| `device` (recommended) | Headless MCP server, long-lived refresh token | Prints URL + code to stderr; approve once in any browser |
| `authcode` | Operator on the same machine, browser available | Server opens browser, listens on `http://127.0.0.1:8765/callback` |
| `client_credentials` | App-only access, public data only (categories, marketplaces) | None — no user identity |
| `refresh_token` | You've already obtained a refresh token elsewhere | None — supply via `ALLEGRO_REFRESH_TOKEN` |

## Device flow (recommended)

```env
ALLEGRO_AUTH_FLOW=device
```

The server prints something like:

```
Allegro authorisation required:
  1. Open: https://allegro.pl/device?code=ABC-123
  2. Enter code: ABC-123
  3. Approve the requested scopes.
Waiting for confirmation…
```

Approve in the browser, the server polls until the user finishes, and
then persists the access + refresh tokens at
`~/.allegro-mcp/tokens.json` (mode `0600`).

Refresh tokens are valid for 3 months and **rotate on every refresh** —
the server overwrites the cache atomically, so you only ever see this
prompt once per token lifetime.

## Authorization Code with PKCE

```env
ALLEGRO_AUTH_FLOW=authcode
ALLEGRO_REDIRECT_URI=http://127.0.0.1:8765/callback
ALLEGRO_PKCE_CALLBACK_PORT=8765
```

The server spins up a localhost listener and opens your browser at the
authorisation URL. After you approve, the browser redirects to the local
listener; the server exchanges the code for tokens.

> **Caveat:** the operator must be on the same machine as the server (the
> redirect targets `127.0.0.1`). Containers need to publish the callback
> port and you'll need a host-side browser to drive the flow. Most users
> are happier with `device`.

## Client Credentials (app-only)

```env
ALLEGRO_AUTH_FLOW=client_credentials
ALLEGRO_SCOPES=allegro:api:public
```

Two-legged: the server gets a token bound to the application, not a user.
Limited to public resources — categories, marketplaces, offer search,
pricing-fee preview. **Cannot** access orders, offers (write), messaging,
or anything billed.

## Pre-shared refresh token

```env
ALLEGRO_AUTH_FLOW=refresh_token
ALLEGRO_REFRESH_TOKEN=<refresh-token-obtained-elsewhere>
```

If you already have a refresh token (e.g. obtained via Postman or a
one-off device-flow run), supply it and the server skips interactive auth
entirely. The refresh token rotates on every refresh — the server
persists the new value to the token store as usual.
