# Configure Claude Code

Claude Code reads MCP servers from `~/.claude/settings.json` (global) or
`.claude/settings.json` (per project). Add an entry under `mcpServers`.

## uvx (recommended — no clone needed)

```json
{
  "mcpServers": {
    "allegro": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/piotrlinski/allegro-open-mcp-server",
        "allegro-mcp"
      ],
      "env": {
        "ALLEGRO_CLIENT_ID": "your-client-id",
        "ALLEGRO_CLIENT_SECRET": "your-client-secret",
        "ALLEGRO_AUTH_FLOW": "device"
      }
    }
  }
}
```

Pin a release with `git+…/allegro-open-mcp-server@v0.1.0` for stability.

## From a local clone

```json
{
  "mcpServers": {
    "allegro": {
      "command": "uv",
      "args": ["--directory", "/absolute/path/to/allegro-open-mcp-server", "run", "allegro-mcp"],
      "env": {
        "ALLEGRO_CLIENT_ID": "your-client-id",
        "ALLEGRO_CLIENT_SECRET": "your-client-secret",
        "ALLEGRO_AUTH_FLOW": "device"
      }
    }
  }
}
```

Then in the Claude Code session:

```text
> /mcp
```

You should see `allegro` in the list along with all 268 tools. Try
`marketplaces_list` first — public, no auth state needed beyond a valid
client_id.
