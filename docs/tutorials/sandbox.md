# Sandbox setup

Allegro provides a parallel sandbox at `*.allegrosandbox.pl` for testing
without affecting real listings or wallets.

## Endpoints

* API base: `https://api.allegro.pl.allegrosandbox.pl`
* OAuth base: `https://allegro.pl.allegrosandbox.pl`

## Set up

1. Sign up at [https://allegro.pl.allegrosandbox.pl/rejestracja](https://allegro.pl.allegrosandbox.pl/rejestracja)
   (separate from your production account).
2. Register a new application at the sandbox developer portal.
3. Run the server with `ALLEGRO_ENVIRONMENT=sandbox`:

```bash
ALLEGRO_ENVIRONMENT=sandbox uv run allegro-mcp
```

The base URLs are derived automatically — no need to override
`ALLEGRO_API_BASE_URL` or `ALLEGRO_OAUTH_BASE_URL`.

## Limitations

The sandbox doesn't simulate every endpoint behaviour and may have stale
fixture data. Real-money flows (payments, refunds) work but never charge
real cards. For end-to-end smoke tests, prefer reads over writes.
