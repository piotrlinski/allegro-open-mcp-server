"""File-based logging setup for the MCP server.

MCP uses stdio as its transport, so writing log records to stdout would
corrupt the protocol stream. We attach only a daily-rotated file handler;
no stream handler is added.

This module is imported once from :func:`server.main` and is otherwise
side-effect free: importing it does NOT install handlers — only calling
:func:`setup_logging` does.
"""

from __future__ import annotations

import logging as _stdlogging
import os
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path

logger = _stdlogging.getLogger(__name__)


def setup_logging() -> Path:
    """Route every log record to a file with daily rotation.

    Configurable via env vars (overridable per :class:`AllegroMCPConfig`):

    * ``ALLEGRO_LOG_DIR`` — override the directory (default ``~/.allegro-mcp/logs``).
    * ``ALLEGRO_LOG_LEVEL`` — root log level (default ``INFO``).
    * ``ALLEGRO_LOG_RETENTION_DAYS`` — how many daily-rotated files to keep
      (default 7).
    * ``ALLEGRO_LOG_UTC`` — rotate at UTC midnight when truthy (default
      false → local midnight).

    Idempotent: calling it twice with the same settings does not stack
    handlers. Returns the path to the live log file.
    """
    log_dir = Path(os.environ.get("ALLEGRO_LOG_DIR") or Path.home() / ".allegro-mcp" / "logs")
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / "allegro-mcp.log"

    try:
        retention_days = int(os.environ.get("ALLEGRO_LOG_RETENTION_DAYS", "7"))
    except ValueError:
        retention_days = 7
    retention_days = max(retention_days, 1)

    use_utc = os.environ.get("ALLEGRO_LOG_UTC", "").strip().lower() in {"1", "true", "yes", "y"}

    handler = TimedRotatingFileHandler(
        log_file,
        when="midnight",
        backupCount=retention_days,
        encoding="utf-8",
        utc=use_utc,
    )
    handler.setFormatter(_stdlogging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s"))

    root = _stdlogging.getLogger()
    root.setLevel(os.environ.get("ALLEGRO_LOG_LEVEL", "INFO"))

    # Idempotent: drop any prior rotating-file handler this module installed
    # (matched by class, not path, so changing ALLEGRO_LOG_DIR between calls
    # doesn't leak handlers from a previous configuration).
    for existing in list(root.handlers):
        if isinstance(existing, TimedRotatingFileHandler):
            root.removeHandler(existing)
            existing.close()
    root.addHandler(handler)
    return log_file
