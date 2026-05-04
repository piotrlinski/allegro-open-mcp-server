"""MCP-server-specific configuration knobs.

Composes :class:`AllegroClientConfig` (from the MCP-agnostic SDK) with the
extras only the MCP server cares about: the write gate, the log directory,
and rotation policy. Loads from the same ``ALLEGRO_*`` env-var prefix so
operators don't juggle two namespaces.
"""

from __future__ import annotations

from pathlib import Path
from typing import Annotated

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from allegro_client.config import AllegroClientConfig


def _default_log_dir() -> Path:
    return Path.home() / ".allegro-mcp" / "logs"


class AllegroMCPConfig(BaseSettings):
    """MCP-only knobs that sit on top of :class:`AllegroClientConfig`.

    Loaded as a separate :class:`BaseSettings` (rather than subclassing
    AllegroClientConfig) so the SDK's settings stay self-contained — the
    extractability boundary explicitly forbids importing MCP knobs from
    inside :mod:`allegro_client`.
    """

    enable_writes: bool = Field(
        default=False,
        description=(
            "Gate high-blast-radius write tools (offer_delete, payment_refund, "
            "auction_place_bid, …). Default: false."
        ),
    )
    log_dir: Path = Field(default_factory=_default_log_dir)
    log_level: str = Field(default="INFO")
    log_retention_days: Annotated[int, Field(ge=1, le=365)] = 7
    log_utc: bool = Field(default=False)

    model_config = SettingsConfigDict(env_prefix="ALLEGRO_", extra="ignore")


def load_configs() -> tuple[AllegroClientConfig, AllegroMCPConfig]:
    """Load both configs from environment in one call.

    The two settings classes use the same prefix; loading them separately
    keeps the SDK's settings free of MCP-only knobs. mypy doesn't see env
    vars, so the ``call-arg`` ignore covers the BaseSettings call style.
    """
    client = AllegroClientConfig()  # type: ignore[call-arg]
    mcp = AllegroMCPConfig()
    return client, mcp
