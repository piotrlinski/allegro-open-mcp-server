"""Tests for :func:`setup_logging`."""

from __future__ import annotations

import logging
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path

import pytest

from allegro_mcp.logging import setup_logging


def test_creates_log_file_under_log_dir(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    isolated_root_logger: None,
) -> None:
    monkeypatch.setenv("ALLEGRO_LOG_DIR", str(tmp_path))
    log_file = setup_logging()
    assert log_file == tmp_path / "allegro-mcp.log"
    assert log_file.parent.is_dir()


def test_no_handler_writes_to_stdout_or_stderr(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    isolated_root_logger: None,
) -> None:
    """Critical: if any handler writes to stdout, it corrupts the MCP stdio
    transport. pytest itself attaches log capture handlers (which redirect
    to ``/dev/null`` or in-memory buffers); those are fine — what we're
    asserting is that :func:`setup_logging` doesn't add a stdout/stderr-bound
    one of its own.
    """
    import sys

    monkeypatch.setenv("ALLEGRO_LOG_DIR", str(tmp_path))
    setup_logging()
    root = logging.getLogger()
    file_handlers = [h for h in root.handlers if isinstance(h, TimedRotatingFileHandler)]
    assert len(file_handlers) == 1, "expected exactly one rotating file handler"

    for handler in root.handlers:
        stream = getattr(handler, "stream", None)
        assert stream is not sys.stdout, f"{handler!r} writes to stdout — would corrupt MCP stdio"
        assert stream is not sys.stderr, f"{handler!r} writes to stderr — discouraged"


def test_idempotent(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    isolated_root_logger: None,
) -> None:
    monkeypatch.setenv("ALLEGRO_LOG_DIR", str(tmp_path))
    setup_logging()
    setup_logging()  # second call must replace, not stack.
    root = logging.getLogger()
    file_handlers = [h for h in root.handlers if isinstance(h, TimedRotatingFileHandler)]
    assert len(file_handlers) == 1


def test_log_level_from_env(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    isolated_root_logger: None,
) -> None:
    monkeypatch.setenv("ALLEGRO_LOG_DIR", str(tmp_path))
    monkeypatch.setenv("ALLEGRO_LOG_LEVEL", "DEBUG")
    setup_logging()
    assert logging.getLogger().level == logging.DEBUG


def test_invalid_retention_falls_back(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    isolated_root_logger: None,
) -> None:
    monkeypatch.setenv("ALLEGRO_LOG_DIR", str(tmp_path))
    monkeypatch.setenv("ALLEGRO_LOG_RETENTION_DAYS", "not-a-number")
    # Should fall back to 7 rather than crash.
    setup_logging()
