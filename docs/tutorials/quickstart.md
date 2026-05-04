# Quickstart

Five-minute walkthrough: register an Allegro app, set env vars, start the
server, and run your first tool from MCP Inspector.

## 1. Register an Allegro app

1. Sign in to [developer.allegro.pl](https://developer.allegro.pl).
2. **My applications → Register a new application**.
3. Pick the application type that matches the OAuth flow you'll use:
   *Device flow* is the right answer for an MCP server. See
   [Pick an OAuth flow](../how-to/oauth-flows.md).

You walk away with a `Client ID`, a `Client Secret`, and (for some flows)
a `Redirect URI`.

## 2. Configure env vars

```bash
cp .env.example .env
# then in .env:
ALLEGRO_CLIENT_ID=...
ALLEGRO_CLIENT_SECRET=...
ALLEGRO_AUTH_FLOW=device
```

The full env-var matrix lives in [Configuration](../reference/configuration.md).

## 3. Run the server

```bash
uv sync --extra dev
uv run allegro-mcp
```

On first run the server prints a verification URL + user code to **stderr**.
Open the URL, enter the code, approve the requested scopes. The server
persists a refresh token at `~/.allegro-mcp/tokens.json` so subsequent
runs don't re-prompt.

## 4. Try a tool with MCP Inspector

```bash
make inspector
```

Inspector opens a browser tab; click **Tools** and try:

* `marketplaces_list` — read-only, public; tests that auth works at all.
* `me_get` — read-only, returns the authenticated seller's profile.
* `auth_status` — shows the cached token's scope + time-to-expiry.

## 5. Wire it into Claude Desktop / Claude Code

* [Configure Claude Desktop](../how-to/with-claude-desktop.md)
* [Configure Claude Code](../how-to/with-claude-code.md)
