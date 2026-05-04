"""Tests for :class:`AllegroMCPConfig`."""

from __future__ import annotations

from pathlib import Path

import pytest
from pydantic import ValidationError

from allegro_mcp.config import AllegroMCPConfig


class TestDefaults:
    def test_writes_disabled_by_default(self, clean_env: None) -> None:
        config = AllegroMCPConfig()
        assert config.enable_writes is False

    def test_default_log_dir_in_home(self, clean_env: None) -> None:
        config = AllegroMCPConfig()
        assert config.log_dir == Path.home() / ".allegro-mcp" / "logs"


class TestEnvLoading:
    def test_enable_writes_from_env(self, clean_env: None, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("ALLEGRO_ENABLE_WRITES", "true")
        config = AllegroMCPConfig()
        assert config.enable_writes is True

    def test_log_retention_validation(
        self, clean_env: None, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setenv("ALLEGRO_LOG_RETENTION_DAYS", "0")
        with pytest.raises(ValidationError):
            AllegroMCPConfig()
