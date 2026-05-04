"""Tests for :class:`RetryTransport`."""

from __future__ import annotations

import httpx
import pytest

from allegro_client.http.retry import RetryTransport


class _Recorder:
    """Counting transport that emits a scripted sequence of responses/exceptions."""

    def __init__(self, sequence: list[httpx.Response | Exception]) -> None:
        self._sequence = sequence
        self.calls = 0

    def handle_request(self, request: httpx.Request) -> httpx.Response:
        self.calls += 1
        item = self._sequence[min(self.calls - 1, len(self._sequence) - 1)]
        if isinstance(item, Exception):
            raise item
        return item

    def close(self) -> None:
        pass


def _request(method: str = "GET", path: str = "/x") -> httpx.Request:
    return httpx.Request(method, f"https://api.allegro.pl{path}")


def _resp(status: int, **kwargs: object) -> httpx.Response:
    return httpx.Response(status, **kwargs)  # type: ignore[arg-type]


class TestRateLimitRetry:
    def test_429_honors_retry_after(self) -> None:
        slept: list[float] = []
        inner = _Recorder([_resp(429, headers={"Retry-After": "3"}), _resp(200, json={})])
        transport = RetryTransport(inner=inner, max_retries=3, sleep=slept.append)  # type: ignore[arg-type]

        response = transport.handle_request(_request())
        assert response.status_code == 200
        assert inner.calls == 2
        assert slept == [3.0]

    def test_429_default_when_header_missing(self) -> None:
        slept: list[float] = []
        inner = _Recorder([_resp(429), _resp(200, json={})])
        transport = RetryTransport(inner=inner, max_retries=3, sleep=slept.append)  # type: ignore[arg-type]

        response = transport.handle_request(_request())
        assert response.status_code == 200
        assert slept == [1.0]

    def test_max_retries_exhausted_returns_last_response(self) -> None:
        slept: list[float] = []
        inner = _Recorder([_resp(429), _resp(429), _resp(429), _resp(429)])
        transport = RetryTransport(inner=inner, max_retries=2, sleep=slept.append)  # type: ignore[arg-type]

        response = transport.handle_request(_request())
        assert response.status_code == 429  # surface to caller for status mapping.
        assert inner.calls == 3  # initial + 2 retries
        assert len(slept) == 2


class TestServerErrorRetry:
    def test_503_exponential_backoff(self) -> None:
        slept: list[float] = []
        inner = _Recorder([_resp(503), _resp(503), _resp(200, json={})])
        transport = RetryTransport(inner=inner, max_retries=3, sleep=slept.append)  # type: ignore[arg-type]

        response = transport.handle_request(_request())
        assert response.status_code == 200
        # 1s, then 2s.
        assert slept == [1.0, 2.0]


class TestNetworkErrorRetry:
    def test_connect_error_recovered(self) -> None:
        slept: list[float] = []
        inner = _Recorder([httpx.ConnectError("nope"), _resp(200, json={})])
        transport = RetryTransport(inner=inner, max_retries=3, sleep=slept.append)  # type: ignore[arg-type]

        response = transport.handle_request(_request())
        assert response.status_code == 200
        assert slept == [1.0]

    def test_connect_error_eventually_propagates(self) -> None:
        slept: list[float] = []
        inner = _Recorder([httpx.ConnectError("nope")] * 5)
        transport = RetryTransport(inner=inner, max_retries=2, sleep=slept.append)  # type: ignore[arg-type]

        with pytest.raises(httpx.ConnectError):
            transport.handle_request(_request())


class TestNonRetryableStatuses:
    @pytest.mark.parametrize("status", [400, 401, 403, 404, 409])
    def test_4xx_passes_through(self, status: int) -> None:
        slept: list[float] = []
        inner = _Recorder([_resp(status, json={})])
        transport = RetryTransport(inner=inner, max_retries=3, sleep=slept.append)  # type: ignore[arg-type]

        response = transport.handle_request(_request())
        assert response.status_code == status
        assert inner.calls == 1  # no retry
        assert slept == []
