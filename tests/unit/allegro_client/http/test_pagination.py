"""Tests for :func:`paginate` and :func:`paginate_cursor`."""

from __future__ import annotations

import httpx
import pytest
import respx
from pydantic import BaseModel, SecretStr

from allegro_client.config import AllegroClientConfig
from allegro_client.http import AllegroClient, paginate, paginate_cursor


class _Row(BaseModel):
    id: str


def _client() -> AllegroClient:
    return AllegroClient(
        AllegroClientConfig(client_id="cid", client_secret=SecretStr("sec"), auth_flow="device"),
        auth=None,
    )


@pytest.fixture
def client() -> AllegroClient:
    return _client()


class TestOffsetLimit:
    def test_drains_all_pages(self, client: AllegroClient, respx_mock: respx.MockRouter) -> None:
        # Two pages: 100 rows then a short tail.
        page1 = {"items": [{"id": str(i)} for i in range(100)]}
        page2 = {"items": [{"id": str(i)} for i in range(100, 137)]}
        respx_mock.get("https://api.allegro.pl/sale/offers").mock(
            side_effect=[
                httpx.Response(200, json=page1),
                httpx.Response(200, json=page2),
            ]
        )
        rows = list(paginate(client, "/sale/offers", model=_Row))
        assert len(rows) == 137
        assert rows[0].id == "0"
        assert rows[-1].id == "136"

    def test_max_items_caps_iteration(
        self, client: AllegroClient, respx_mock: respx.MockRouter
    ) -> None:
        respx_mock.get("https://api.allegro.pl/sale/offers").mock(
            return_value=httpx.Response(200, json={"items": [{"id": str(i)} for i in range(50)]})
        )
        rows = list(paginate(client, "/sale/offers", model=_Row, max_items=10))
        assert len(rows) == 10

    def test_custom_page_key(self, client: AllegroClient, respx_mock: respx.MockRouter) -> None:
        # Allegro's offer list uses `offers` rather than `items`.
        respx_mock.get("https://api.allegro.pl/sale/offers").mock(
            return_value=httpx.Response(200, json={"offers": [{"id": "1"}]})
        )
        rows = list(paginate(client, "/sale/offers", model=_Row, page_key="offers"))
        assert [r.id for r in rows] == ["1"]


class TestCursor:
    def test_follows_cursor_until_empty(
        self, client: AllegroClient, respx_mock: respx.MockRouter
    ) -> None:
        respx_mock.get("https://api.allegro.pl/sale/offers").mock(
            side_effect=[
                httpx.Response(200, json={"items": [{"id": "1"}], "nextPage": "cursor-2"}),
                httpx.Response(200, json={"items": [{"id": "2"}], "nextPage": "cursor-3"}),
                httpx.Response(200, json={"items": [{"id": "3"}]}),  # no nextPage → stop
            ]
        )
        rows = list(paginate_cursor(client, "/sale/offers", model=_Row))
        assert [r.id for r in rows] == ["1", "2", "3"]

    def test_passes_cursor_in_query(
        self, client: AllegroClient, respx_mock: respx.MockRouter
    ) -> None:
        # Verify the second request carries page.id=cursor-from-first-page.
        responses = [
            httpx.Response(200, json={"items": [{"id": "a"}], "nextPage": "abc"}),
            httpx.Response(200, json={"items": []}),  # empty stops iteration.
        ]
        route = respx_mock.get("https://api.allegro.pl/orders").mock(side_effect=responses)
        list(paginate_cursor(client, "/orders", model=_Row))
        assert route.call_count == 2
        second_url = str(route.calls[1].request.url)
        assert "page.id=abc" in second_url
