# Error codes

Tools return either a Pydantic response model or an
[`ErrorResponse`](../) envelope on failure. The `error` field is one of:

## Synthetic codes (raised by the client / MCP layer)

| Code | Meaning |
| --- | --- |
| `NETWORK_ERROR` | Transport failure that escaped the retry transport (extremely rare) |
| `PARSE_ERROR` | Server returned a body that didn't match any expected shape |
| `OAUTH_FLOW_ERROR` | Interactive OAuth step failed — user denied, polling timed out, … |
| `TOKEN_STORE_ERROR` | Couldn't read or write the persisted token file |
| `INVALID_INPUT` | Pydantic validation rejected the inbound arguments |
| `EMPTY_INPUT` | A required collection argument was empty (short-circuit guard) |
| `MISSING_SCOPE` | Tool requires an OAuth scope the loaded token doesn't carry |
| `WRITES_DISABLED` | High-blast-radius write tool fired but `ALLEGRO_ENABLE_WRITES` is false |
| `HTTP_<status>` | Fallback when Allegro returned an opaque body for the given status |

## Allegro server codes

The `errors[].code` field from Allegro flows through verbatim. Examples:

| Code | Meaning |
| --- | --- |
| `OFFER_NOT_FOUND` | Offer ID doesn't exist or isn't visible to the caller |
| `OFFER_INVALID` | Offer payload failed Allegro's validation rules |
| `RATE_LIMIT` | 9 000 req/min per Client ID exceeded; the retry transport already attempted one Retry-After-honoring retry |
| `invalid_grant` | OAuth refresh token rejected — re-run `auth_login_device` |
| `authorization_pending` | OAuth device flow still polling for user approval |
| `slow_down` | OAuth device flow asked to back off; the strategy increases its polling interval |

The full list is published by Allegro at
[developer.allegro.pl/errors-list](https://developer.allegro.pl/errors-list/).
