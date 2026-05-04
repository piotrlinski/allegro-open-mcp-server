# Configure Claude Code

Claude Code reads MCP servers from `~/.claude/settings.json` (global) or
`.claude/settings.json` (per project). Add an entry under `mcpServers`:

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
