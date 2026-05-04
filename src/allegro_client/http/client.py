"""Synchronous Allegro REST client.

Thin OOP wrapper around :class:`httpx.Client` that owns:

* the base URL (derived from :class:`AllegroClientConfig` ``environment``),
* the standard headers (``User-Agent``, ``Accept-Language``,
  versioned ``Accept`` / ``Content-Type``),
* the auth strategy (any :class:`httpx.Auth` subclass — typically one of
  the four flows in :mod:`allegro_client.auth`),
* the retry transport (429 / 5xx / network errors).

Callers reach for typed methods (:meth:`get`, :meth:`post`, …) when they
have a Pydantic model for the response, and the lower-level
:meth:`get_json` / :meth:`request_json` for raw dict responses (used by
the pagination iterators).

The client is **MCP-agnostic** — it has no awareness of FastMCP, tools, or
any envelope wrapping; that's the MCP layer's job.
"""

from __future__ import annotations

import logging
from typing import Any, TypeVar

import httpx
from pydantic import BaseModel

from ..config import AllegroClientConfig
from ..errors import ERROR_NETWORK, ERROR_PARSE, AllegroError, AuthError
from . import media_types
from .retry import RetryTransport

logger = logging.getLogger(__name__)

T = TypeVar("T", bound=BaseModel)


class AllegroClient:
    """Synchronous typed Allegro REST client.

    Construct with an :class:`AllegroClientConfig` and an :class:`httpx.Auth`
    strategy. Use as a context manager for clean shutdown::

        with AllegroClient(config, auth=auth) as client:
            offers = client.paginate("/sale/offers", model=Offer)

    Calls raise an :class:`allegro_client.errors.AllegroError` subclass on
    HTTP failure; the retry transport handles 429/5xx/network transients
    transparently before the call returns.
    """

    def __init__(
        self,
        config: AllegroClientConfig,
        *,
        auth: httpx.Auth | None = None,
        transport: httpx.BaseTransport | None = None,
    ) -> None:
        self._config = config
        retry_transport = RetryTransport(inner=transport, max_retries=config.max_retries)
        self._http = httpx.Client(
            base_url=config.api_base_url_str,
            auth=auth,
            timeout=config.timeout,
            transport=retry_transport,
            headers={
                "User-Agent": config.user_agent,
                "Accept-Language": config.accept_language,
            },
        )

    # ---- Context-manager glue ---------------------------------------------

    def __enter__(self) -> AllegroClient:
        return self

    def __exit__(self, *_: object) -> None:
        self.close()

    def close(self) -> None:
        """Close the underlying httpx connection pool."""
        self._http.close()

    # ---- Typed convenience methods ---------------------------------------

    def get(self, path: str, *, model: type[T], params: dict[str, Any] | None = None) -> T:
        """``GET path`` and parse the JSON body as ``model``."""
        body = self.request_json("GET", path, params=params)
        return _validate(model, body)

    def post(
        self,
        path: str,
        *,
        model: type[T] | None,
        json: BaseModel | dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
    ) -> T | None:
        """``POST path`` with ``json`` body; parse the response as ``model``.

        Pass ``model=None`` for endpoints that return 204 / empty body.
        """
        body = self.request_json("POST", path, json=json, params=params)
        return None if model is None else _validate(model, body)

    def put(
        self,
        path: str,
        *,
        model: type[T] | None,
        json: BaseModel | dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
    ) -> T | None:
        body = self.request_json("PUT", path, json=json, params=params)
        return None if model is None else _validate(model, body)

    def patch(
        self,
        path: str,
        *,
        model: type[T] | None,
        json: BaseModel | dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
    ) -> T | None:
        body = self.request_json("PATCH", path, json=json, params=params)
        return None if model is None else _validate(model, body)

    def delete(self, path: str, *, params: dict[str, Any] | None = None) -> None:
        """``DELETE path``. No response body expected."""
        self.request_json("DELETE", path, params=params)

    # ---- Lower-level dict-returning methods -------------------------------

    def get_json(self, path: str, *, params: dict[str, Any] | None = None) -> dict[str, Any]:
        """``GET path`` and return the raw JSON body as a dict.

        Used by :func:`allegro_client.http.pagination.paginate` and by tools
        that need to crawl the response shape themselves rather than
        materialising a full Pydantic model.
        """
        body = self.request_json("GET", path, params=params)
        if not isinstance(body, dict):
            raise AllegroError(
                code=ERROR_PARSE,
                message=f"Expected JSON object at {path}, got {type(body).__name__}",
            )
        return body

    def request_json(
        self,
        method: str,
        path: str,
        *,
        json: BaseModel | dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
    ) -> Any:
        """Issue an HTTP request and return the parsed JSON body.

        Centralises:

        * media-type negotiation (GA vs beta per :func:`media_types.resolve`),
        * query-param scrubbing (drop ``None`` values so we don't send
          ``?foo=None`` to Allegro),
        * status-code → :class:`AllegroError` mapping,
        * empty-body short-circuit on 204.

        The retry transport handles 429/5xx/network transients before this
        function gets to see the response.
        """
        media_type = media_types.resolve(path)
        headers = {"Accept": media_type}
        if json is not None:
            headers["Content-Type"] = media_type

        body: Any = None
        if isinstance(json, BaseModel):
            body = json.model_dump(mode="json", exclude_none=True, by_alias=True)
        elif json is not None:
            body = json

        cleaned_params = _drop_none(params)

        try:
            response = self._http.request(
                method,
                path,
                params=cleaned_params,
                json=body,
                headers=headers,
            )
        except httpx.HTTPError as exc:
            raise AllegroError(
                code=ERROR_NETWORK,
                message=f"{type(exc).__name__}: {exc}",
            ) from exc

        request_id = response.headers.get("X-Request-Id")

        if response.status_code == 204 or not response.content:
            if 200 <= response.status_code < 300:
                return None
            # Empty body on a non-2xx: surface via the canonical error path.
            raise AllegroError.from_response(
                http_status=response.status_code,
                body={},
                request_id=request_id,
            )

        try:
            payload = response.json()
        except ValueError as exc:
            raise AllegroError(
                code=ERROR_PARSE,
                message=f"Non-JSON response (HTTP {response.status_code})",
                http_status=response.status_code,
                request_id=request_id,
            ) from exc

        if 200 <= response.status_code < 300:
            return payload

        # 401 specifically: surface AuthError so refresh-on-401 logic in the
        # auth strategy can react. (httpx's auth_flow already handles refresh
        # before the response reaches us, but downstream callers might want
        # to differentiate auth from generic 4xx.)
        if response.status_code == 401:
            raise AuthError.from_response(http_status=401, body=payload, request_id=request_id)

        raise AllegroError.from_response(
            http_status=response.status_code,
            body=payload,
            request_id=request_id,
        )


# ---- Helpers ---------------------------------------------------------------


def _validate(model: type[T], body: Any) -> T:
    """Run ``model.model_validate(body)`` and translate failures.

    Pydantic raises ``ValidationError``; we wrap it as an Allegro PARSE_ERROR
    so callers don't need to handle two error families.
    """
    from pydantic import ValidationError as PydanticValidationError

    try:
        return model.model_validate(body)
    except PydanticValidationError as exc:
        first_errors = exc.errors(include_url=False)[:3]
        raise AllegroError(
            code=ERROR_PARSE,
            message=f"Response did not validate against {model.__name__}: {first_errors}",
        ) from exc


def _drop_none(params: dict[str, Any] | None) -> dict[str, Any] | None:
    """Strip keys whose value is ``None`` so we don't send ``?foo=None``."""
    if params is None:
        return None
    return {k: v for k, v in params.items() if v is not None}
