"""Shared pytest fixtures.

Two patterns get reused enough to live globally:

* :func:`clean_env` strips every ``ALLEGRO_*`` env var so config tests start
  from a known baseline; tests opt in by accepting the fixture.
* :func:`isolated_root_logger` snapshots the root logger and restores it
  after the test, so handlers added by :func:`setup_logging` don't leak
  between tests.
"""

from __future__ import annotations

import contextlib
import logging
import os
from collections.abc import Iterator

import pytest


@pytest.fixture
def clean_env(monkeypatch: pytest.MonkeyPatch) -> None:
    """Remove every ``ALLEGRO_*`` env var for the duration of one test."""
    for key in list(os.environ):
        if key.startswith("ALLEGRO_"):
            monkeypatch.delenv(key, raising=False)


@pytest.fixture
def isolated_root_logger() -> Iterator[None]:
    """Snapshot+restore the root logger so file handlers don't leak."""
    root = logging.getLogger()
    original_handlers = root.handlers[:]
    original_level = root.level
    yield
    for handler in root.handlers[:]:
        root.removeHandler(handler)
        with contextlib.suppress(Exception):
            handler.close()
    for handler in original_handlers:
        root.addHandler(handler)
    root.setLevel(original_level)
