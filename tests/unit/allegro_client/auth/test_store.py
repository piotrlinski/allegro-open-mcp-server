"""Tests for :class:`FileTokenStore` and :class:`InMemoryTokenStore`."""

from __future__ import annotations

import json
import os
import stat
from pathlib import Path

from allegro_client.auth.base import TokenSet
from allegro_client.auth.store import (
    SCHEMA_VERSION,
    FileTokenStore,
    InMemoryTokenStore,
)


def _tokens(**overrides: object) -> TokenSet:
    base: dict[str, object] = {
        "access_token": "at",
        "refresh_token": "rt",
        "expires_at": 1_700_000_000.0,
        "scope": "allegro:api:sale:offers:read",
    }
    base.update(overrides)
    return TokenSet(**base)  # type: ignore[arg-type]


class TestFileTokenStore:
    def test_round_trip(self, tmp_path: Path) -> None:
        store = FileTokenStore(tmp_path / "tokens.json")
        original = _tokens()
        store.save(original)
        loaded = store.load()
        assert loaded is not None
        assert loaded.access_token == "at"
        assert loaded.refresh_token == "rt"
        assert loaded.expires_at == 1_700_000_000.0

    def test_load_returns_none_when_missing(self, tmp_path: Path) -> None:
        store = FileTokenStore(tmp_path / "missing.json")
        assert store.load() is None

    def test_corrupt_file_treated_as_missing(self, tmp_path: Path) -> None:
        path = tmp_path / "tokens.json"
        path.write_text("{not json")
        assert FileTokenStore(path).load() is None

    def test_save_writes_0600_permissions(self, tmp_path: Path) -> None:
        path = tmp_path / "tokens.json"
        FileTokenStore(path).save(_tokens())
        mode = stat.S_IMODE(os.stat(path).st_mode)
        assert mode == 0o600, f"expected 0o600, got {oct(mode)}"

    def test_save_is_atomic_via_rename(self, tmp_path: Path) -> None:
        path = tmp_path / "tokens.json"
        store = FileTokenStore(path)
        store.save(_tokens())
        # Sibling temp file should not linger after the rename completes.
        assert not (tmp_path / "tokens.json.tmp").exists()

    def test_overwrites_previous(self, tmp_path: Path) -> None:
        path = tmp_path / "tokens.json"
        store = FileTokenStore(path)
        store.save(_tokens(access_token="first"))
        store.save(_tokens(access_token="second"))
        loaded = store.load()
        assert loaded is not None
        assert loaded.access_token == "second"

    def test_clear_removes_file(self, tmp_path: Path) -> None:
        path = tmp_path / "tokens.json"
        store = FileTokenStore(path)
        store.save(_tokens())
        store.clear()
        assert not path.exists()
        # Idempotent: clear() on missing file does not raise.
        store.clear()

    def test_creates_parent_directories(self, tmp_path: Path) -> None:
        path = tmp_path / "subdir" / "deeper" / "tokens.json"
        FileTokenStore(path).save(_tokens())
        assert path.exists()

    def test_schema_version_recorded(self, tmp_path: Path) -> None:
        path = tmp_path / "tokens.json"
        FileTokenStore(path).save(_tokens())
        raw = json.loads(path.read_text())
        assert raw["_schema_version"] == SCHEMA_VERSION

    def test_future_schema_returns_none(self, tmp_path: Path) -> None:
        # Forward-compat: a newer-version token store should be treated as
        # missing rather than crashing the server.
        path = tmp_path / "tokens.json"
        path.write_text(json.dumps({"_schema_version": SCHEMA_VERSION + 1, "access_token": "x"}))
        assert FileTokenStore(path).load() is None


class TestInMemoryTokenStore:
    def test_round_trip(self) -> None:
        store = InMemoryTokenStore()
        assert store.load() is None
        store.save(_tokens())
        assert store.load() is not None
        store.clear()
        assert store.load() is None
