# syntax=docker/dockerfile:1.7
# See README.md for build/run instructions and MCP-client config.
#
# Multi-stage build: a uv-based builder produces a self-contained virtualenv,
# the runtime stage runs as a non-root user under slim python. The token
# store is mounted at ``/home/mcp/.allegro-mcp`` so refresh tokens survive
# container restarts.

FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS builder

WORKDIR /app

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=never

COPY pyproject.toml uv.lock README.md ./
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project --no-dev

COPY src/ ./src/
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev


FROM python:3.12-slim-bookworm AS runtime

# Run as a non-root user. The home directory is where the token store
# lives by default (~/.allegro-mcp/tokens.json) — mount it as a volume
# so refresh tokens survive container restarts.
RUN groupadd --system mcp && useradd --system --gid mcp --create-home mcp

WORKDIR /app
COPY --from=builder --chown=mcp:mcp /app /app

ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    ALLEGRO_LOG_DIR=/var/log/allegro-mcp

RUN mkdir -p /var/log/allegro-mcp /home/mcp/.allegro-mcp \
    && chown -R mcp:mcp /var/log/allegro-mcp /home/mcp/.allegro-mcp

VOLUME ["/var/log/allegro-mcp", "/home/mcp/.allegro-mcp"]

USER mcp

ENTRYPOINT ["allegro-mcp"]
