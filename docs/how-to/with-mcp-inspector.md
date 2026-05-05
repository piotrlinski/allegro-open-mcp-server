# Run with MCP Inspector

[MCP Inspector](https://github.com/modelcontextprotocol/inspector) is the
canonical browser-based debugger for MCP servers.

```bash
make inspector
```

This wraps:

```bash
npx @modelcontextprotocol/inspector \
    docker run --rm -i \
      -v ~/.allegro-mcp:/home/mcp/.allegro-mcp \
      -e ALLEGRO_CLIENT_ID -e ALLEGRO_CLIENT_SECRET -e ALLEGRO_AUTH_FLOW \
      allegro-mcp:latest
```

Browse to `http://127.0.0.1:6274/`, click **Tools**, and try one of:

* `marketplaces_list` — public, fastest sanity check
* `me_get` — confirms auth works
* `auth_status` — shows the cached token's scope + time-to-expiry

## Without Docker, via uvx

```bash
ALLEGRO_CLIENT_ID=... ALLEGRO_CLIENT_SECRET=... ALLEGRO_AUTH_FLOW=device \
npx @modelcontextprotocol/inspector \
    uvx --from git+https://github.com/piotrlinski/allegro-open-mcp-server allegro-mcp
```

## Without Docker, from a local clone

```bash
npx @modelcontextprotocol/inspector uv run allegro-mcp
```

(Set `ALLEGRO_*` env vars in your shell first.)
