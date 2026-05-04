# Allegro MCP — common tasks.
#
#   make help                    # list every target
#   make build                   # build the Docker image
#   make run                     # run the server in Docker (stdio)
#   make test                    # run pytest locally (needs uv)
#   make lint                    # ruff (check + format --check) + mypy locally
#   make format                  # apply ruff format + ruff --fix locally
#   make inspector               # MCP Inspector against the Docker image
#   make gen-models              # codegen Pydantic models from swagger.yaml
#   make check-models-freshness  # warn if upstream OpenAPI spec moved
#   make gen-tools               # emit tool inventory from the spec
#   make clean                   # remove the image
#
# Override the image tag or Dockerfile location via env vars:
#   IMAGE=allegro-mcp:dev DOCKERFILE=docker/Dockerfile.dev make build

IMAGE       ?= allegro-mcp:latest
DOCKERFILE  ?= docker/Dockerfile

# Tools
DOCKER ?= docker
UV     ?= uv

# Credentials passthrough for `make run` / `make inspector`. Export in your
# shell before invoking; the recipes refuse to run without ALLEGRO_CLIENT_ID
# + ALLEGRO_CLIENT_SECRET + ALLEGRO_AUTH_FLOW.
ENV_FLAGS = \
    -e ALLEGRO_CLIENT_ID -e ALLEGRO_CLIENT_SECRET -e ALLEGRO_AUTH_FLOW \
    -e ALLEGRO_REFRESH_TOKEN -e ALLEGRO_REDIRECT_URI -e ALLEGRO_PKCE_CALLBACK_PORT \
    -e ALLEGRO_SCOPES -e ALLEGRO_ENVIRONMENT \
    -e ALLEGRO_API_BASE_URL -e ALLEGRO_OAUTH_BASE_URL \
    -e ALLEGRO_DEFAULT_MARKETPLACE -e ALLEGRO_ACCEPT_LANGUAGE \
    -e ALLEGRO_USER_AGENT -e ALLEGRO_TIMEOUT -e ALLEGRO_MAX_RETRIES \
    -e ALLEGRO_ENABLE_WRITES \
    -e ALLEGRO_LOG_DIR -e ALLEGRO_LOG_LEVEL -e ALLEGRO_LOG_RETENTION_DAYS

# Mount the token store so refresh tokens survive container restarts.
TOKEN_STORE_VOLUME ?= $(HOME)/.allegro-mcp:/home/mcp/.allegro-mcp

.DEFAULT_GOAL := help
.PHONY: help build run inspector test lint format sync clean \
        gen-models check-models-freshness gen-tools \
        docs-sync docs-serve docs-build docs-lint docs-link-check \
        docs-coverage docs-all docs-clean

help: ## Show this help
	@awk 'BEGIN {FS = ":.*##"; printf "Targets:\n"} \
	      /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-22s\033[0m %s\n", $$1, $$2 }' \
	      $(MAKEFILE_LIST)

build: ## Build the Docker image
	$(DOCKER) build -f $(DOCKERFILE) -t $(IMAGE) .

run: _check-creds ## Run the MCP server in Docker (stdio)
	$(DOCKER) run --rm -i -v $(TOKEN_STORE_VOLUME) $(ENV_FLAGS) $(IMAGE)

inspector: _check-creds ## Open MCP Inspector against the Docker image
	npx @modelcontextprotocol/inspector \
	    $(DOCKER) run --rm -i -v $(TOKEN_STORE_VOLUME) $(ENV_FLAGS) $(IMAGE)

sync: ## Install dev dependencies locally with uv
	$(UV) sync --extra dev

test: ## Run pytest locally (uv-managed venv)
	$(UV) run pytest tests/

lint: ## Run ruff (check + format --check) + mypy locally
	$(UV) run ruff check src tests
	$(UV) run ruff format --check src tests
	$(UV) run mypy src

format: ## Apply ruff format + ruff --fix locally
	$(UV) run ruff format src tests
	$(UV) run ruff check --fix src tests

clean: ## Remove the Docker image
	-$(DOCKER) image rm $(IMAGE)

# ---- Codegen --------------------------------------------------------------
# Models are generated from Allegro's official OpenAPI spec at
# https://developer.allegro.pl/swagger.yaml. Output is committed under
# src/allegro_client/models/_generated/ and reviewed in PRs.

gen-models: ## Codegen Pydantic models from the official OpenAPI spec
	$(UV) run python scripts/gen_models.py

check-models-freshness: ## Warn if the upstream OpenAPI spec has moved
	$(UV) run python scripts/check_models_freshness.py

gen-tools: ## Emit the MCP tool inventory from the spec (markdown table)
	$(UV) run python scripts/gen_tool_inventory.py

# ---- Documentation --------------------------------------------------------

docs-sync: ## Install docs dependencies (uv sync --extra docs)
	$(UV) sync --extra docs

docs-gen: ## Run every docs generator (tool catalog, error codes, config)
	$(UV) run python scripts/gen_tool_catalog.py
	$(UV) run python scripts/gen_error_codes.py
	$(UV) run python scripts/gen_configuration.py

docs-serve: docs-gen ## Live-reload docs locally at http://127.0.0.1:8000
	DISABLE_MKDOCS_2_WARNING=true $(UV) run mkdocs serve -a 127.0.0.1:8000

docs-build: docs-gen ## Build the static site (strict: fails on warnings)
	DISABLE_MKDOCS_2_WARNING=true $(UV) run mkdocs build --strict

docs-clean: ## Remove the built site
	rm -rf site

docs-coverage: docs-build ## Verify every @mcp.tool has a rendered page
	$(UV) run python scripts/check_tool_coverage.py site

docs-lint: ## markdownlint + codespell on docs and source prose
	$(UV) run markdownlint-cli2 'docs/**/*.md' '*.md' || true
	$(UV) run codespell --config .codespellrc docs/ src/ scripts/

docs-link-check: docs-build ## lychee link-check the built site
	lychee --config lychee.toml site/ || true

docs-all: docs-build docs-coverage docs-lint docs-link-check ## All docs gates

_check-creds:
	@if [ -z "$$ALLEGRO_CLIENT_ID" ] || [ -z "$$ALLEGRO_CLIENT_SECRET" ] || [ -z "$$ALLEGRO_AUTH_FLOW" ]; then \
	    echo "ERROR: export ALLEGRO_CLIENT_ID, ALLEGRO_CLIENT_SECRET, ALLEGRO_AUTH_FLOW first." >&2; \
	    exit 1; \
	fi
