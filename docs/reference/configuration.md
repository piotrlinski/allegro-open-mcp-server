# Configuration

Loaded by [`AllegroClientConfig`](../) and [`AllegroMCPConfig`](../) from
environment variables prefixed with `ALLEGRO_`. CLI flags on
`allegro-mcp` take precedence over env vars; env vars take precedence
over defaults.

## Required

| Variable | Description |
| --- | --- |
| `ALLEGRO_CLIENT_ID` | Application `client_id` from developer.allegro.pl |
| `ALLEGRO_CLIENT_SECRET` | Application `client_secret`. Held as `SecretStr` — never logged |
| `ALLEGRO_AUTH_FLOW` | `device` \| `authcode` \| `client_credentials` \| `refresh_token` |

## Conditionally required

| Variable | Required when |
| --- | --- |
| `ALLEGRO_REFRESH_TOKEN` | `ALLEGRO_AUTH_FLOW=refresh_token` |
| `ALLEGRO_REDIRECT_URI` | `ALLEGRO_AUTH_FLOW=authcode` |
| `ALLEGRO_PKCE_CALLBACK_PORT` | `ALLEGRO_AUTH_FLOW=authcode` (default `8765`) |

## Optional

| Variable | Default | Description |
| --- | --- | --- |
| `ALLEGRO_SCOPES` | empty | Comma-separated OAuth scopes |
| `ALLEGRO_ENVIRONMENT` | `production` | `production` or `sandbox` |
| `ALLEGRO_API_BASE_URL` | derived | Override the API base URL |
| `ALLEGRO_OAUTH_BASE_URL` | derived | Override the OAuth base URL |
| `ALLEGRO_TOKEN_STORE_PATH` | `~/.allegro-mcp/tokens.json` | Where the refresh token persists |
| `ALLEGRO_DEFAULT_MARKETPLACE` | none | e.g. `allegro-pl` |
| `ALLEGRO_ACCEPT_LANGUAGE` | `pl-PL` | Response localisation |
| `ALLEGRO_USER_AGENT` | `allegro-mcp/<version> (+repo URL)` | HTTP User-Agent |
| `ALLEGRO_TIMEOUT` | `30` | httpx request timeout (seconds) |
| `ALLEGRO_MAX_RETRIES` | `3` | Max retries on 429/5xx/network errors |
| `ALLEGRO_ENABLE_WRITES` | `false` | Gate high-blast-radius write tools |
| `ALLEGRO_LOG_DIR` | `~/.allegro-mcp/logs` | Where rotating log files land |
| `ALLEGRO_LOG_LEVEL` | `INFO` | Root log level |
| `ALLEGRO_LOG_RETENTION_DAYS` | `7` | Daily-rotated log retention |
| `ALLEGRO_LOG_UTC` | `false` | Rotate at UTC midnight when truthy |

## URL constants

| Environment | API base | OAuth base |
| --- | --- | --- |
| `production` | `https://api.allegro.pl` | `https://allegro.pl` |
| `sandbox` | `https://api.allegro.pl.allegrosandbox.pl` | `https://allegro.pl.allegrosandbox.pl` |
