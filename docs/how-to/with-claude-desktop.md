# Configure Claude Desktop

Add the server to Claude Desktop's `claude_desktop_config.json`. Path:

* macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
* Windows: `%APPDATA%\Claude\claude_desktop_config.json`

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

Restart Claude Desktop. The first tool call triggers the device-flow
prompt; the URL + code are written to Claude Desktop's MCP log (look in
the *Developer* menu for the log path).

## Docker variant

```json
{
  "mcpServers": {
    "allegro": {
      "command": "docker",
      "args": [
        "run", "--rm", "-i",
        "-v", "/Users/you/.allegro-mcp:/home/mcp/.allegro-mcp",
        "-e", "ALLEGRO_CLIENT_ID",
        "-e", "ALLEGRO_CLIENT_SECRET",
        "-e", "ALLEGRO_AUTH_FLOW",
        "allegro-mcp:latest"
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

The volume mount keeps the refresh token across container restarts.
