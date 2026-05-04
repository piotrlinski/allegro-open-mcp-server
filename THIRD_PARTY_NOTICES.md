---
title: Third-party licenses
description: Auto-generated inventory of every runtime dependency, the license each one ships under, and the package version pinned in the latest build.
---

# Third-party licenses

Every package that gets installed when a user runs
`pip install allegro-mcp` (or the equivalent via `uvx` / Docker)
is listed below. Dev / docs / lint tooling is omitted — those are
build-time only and never reach the user.

Generated from installed package metadata via
[`scripts/gen_licenses.py`](https://github.com/piotrlinski/allegro-open-mcp-server/blob/master/scripts/gen_licenses.py).
Refreshed on every docs build; CI fails if the metadata becomes
unparseable.

## Summary

| Category | Count | Notes |
| --- | ---:| --- |
| Permissive (MIT / BSD / Apache / ISC / PSF / Public Domain) | 74 | Compatible with MIT redistribution. |
| Weak copyleft (MPL-2.0) | 1 | File-level copyleft; obligations only apply if the dep's source is modified. Compatible with MIT redistribution. |
| Strong copyleft (GPL / AGPL / LGPL) | 0 | Would constrain MIT redistribution if any appear here — investigate if non-zero. |
| Unknown | 0 | Missing metadata; check upstream PyPI page. |

!!! success "No strong-copyleft runtime dependencies"
    The runtime dependency graph is fully MIT-compatible. Redistribute
    the package under MIT terms; downstream consumers see only permissive
    or weak-copyleft transitive licenses.

## Inventory

| Package | Version | License | Source |
| --- | --- | --- | --- |
| `aiofile` | `3.9.0` | Apache Software License | <http://github.com/mosquito/aiofile> |
| `annotated-types` | `0.7.0` | MIT License | <https://github.com/annotated-types/annotated-types> |
| `anyio` | `4.13.0` | MIT | <https://pypi.org/project/anyio/> |
| `attrs` | `26.1.0` | MIT | <https://pypi.org/project/attrs/> |
| `authlib` | `1.7.1` | BSD License | <https://github.com/authlib/authlib> |
| `backports-tarfile` | `(conditional)` | MIT | <https://github.com/jaraco/backports.tarfile> |
| `beartype` | `0.22.9` | MIT License | <https://pypi.org/project/beartype/> |
| `cachetools` | `7.1.1` | MIT | <https://github.com/tkem/cachetools/> |
| `caio` | `0.9.25` | Apache-2.0 | <https://github.com/mosquito/caio> |
| `certifi` | `2026.4.22` | Mozilla Public License 2.0 (MPL 2.0) | <https://github.com/certifi/python-certifi> |
| `cffi` | `2.0.0` | MIT | <https://pypi.org/project/cffi/> |
| `click` | `8.3.3` | BSD-3-Clause | <https://github.com/pallets/click/> |
| `colorama` | `0.4.6` | BSD License | <https://github.com/tartley/colorama> |
| `cryptography` | `47.0.0` | Apache-2.0 OR BSD-3-Clause | <https://github.com/pyca/cryptography> |
| `cyclopts` | `4.11.2` | Apache-2.0 | <https://github.com/BrianPugh/cyclopts> |
| `dnspython` | `2.8.0` | ISC License (ISCL) | <https://www.dnspython.org> |
| `docstring-parser` | `0.18.0` | MIT License | <https://github.com/rr-/docstring_parser> |
| `docutils` | `0.22.4` | Public Domain / BSD License / GNU General Public License (GPL) | <https://docutils.sourceforge.io> |
| `email-validator` | `2.3.0` | The Unlicense (Unlicense) | <https://github.com/JoshData/python-email-validator> |
| `exceptiongroup` | `1.3.1` | MIT License | <https://pypi.org/project/exceptiongroup/> |
| `fastmcp` | `3.2.4` | Apache-2.0 | <https://gofastmcp.com> |
| `griffelib` | `2.0.2` | ISC | <https://pypi.org/project/griffelib/> |
| `h11` | `0.16.0` | MIT License | <https://github.com/python-hyper/h11> |
| `httpcore` | `1.0.9` | BSD-3-Clause | <https://www.encode.io/httpcore/> |
| `httpx` | `0.28.1` | BSD License | <https://github.com/encode/httpx> |
| `httpx-sse` | `0.4.3` | MIT | <https://github.com/florimondmanca/httpx-sse> |
| `idna` | `3.13` | BSD-3-Clause | <https://github.com/kjd/idna> |
| `importlib-metadata` | `8.7.1` | Apache-2.0 | <https://github.com/python/importlib_metadata> |
| `jaraco-classes` | `3.4.0` | MIT License | <https://github.com/jaraco/jaraco.classes> |
| `jaraco-context` | `6.1.2` | MIT | <https://github.com/jaraco/jaraco.context> |
| `jaraco-functools` | `4.4.0` | MIT | <https://github.com/jaraco/jaraco.functools> |
| `jeepney` | `(conditional)` | MIT | <https://gitlab.com/takluyver/jeepney> |
| `joserfc` | `1.6.4` | BSD License | <https://github.com/authlib/joserfc> |
| `jsonref` | `1.1.0` | MIT | <https://github.com/gazpachoking/jsonref> |
| `jsonschema` | `4.26.0` | MIT | <https://github.com/python-jsonschema/jsonschema> |
| `jsonschema-path` | `0.4.6` | Apache Software License | <https://github.com/p1c2u/jsonschema-path> |
| `jsonschema-specifications` | `2025.9.1` | MIT | <https://github.com/python-jsonschema/jsonschema-specifications> |
| `keyring` | `25.7.0` | MIT | <https://github.com/jaraco/keyring> |
| `markdown-it-py` | `4.0.0` | MIT License | <https://github.com/executablebooks/markdown-it-py> |
| `mcp` | `1.27.0` | MIT License | <https://modelcontextprotocol.io> |
| `mdurl` | `0.1.2` | MIT License | <https://github.com/executablebooks/mdurl> |
| `more-itertools` | `11.0.2` | MIT | <https://github.com/more-itertools/more-itertools> |
| `openapi-pydantic` | `0.5.1` | MIT License | <https://github.com/mike-oakley/openapi-pydantic> |
| `opentelemetry-api` | `1.41.1` | Apache-2.0 | <https://github.com/open-telemetry/opentelemetry-python/tree/main/opentelemetry-api> |
| `packaging` | `26.2` | Apache-2.0 OR BSD-2-Clause | <https://github.com/pypa/packaging> |
| `pathable` | `0.5.0` | Apache Software License | <https://github.com/p1c2u/pathable> |
| `platformdirs` | `4.9.6` | MIT | <https://github.com/tox-dev/platformdirs> |
| `py-key-value-aio` | `0.4.4` | Apache Software License | <https://pypi.org/project/py-key-value-aio/> |
| `pycparser` | `3.0` | BSD-3-Clause | <https://github.com/eliben/pycparser> |
| `pydantic` | `2.13.3` | MIT | <https://github.com/pydantic/pydantic> |
| `pydantic-core` | `2.46.3` | MIT | <https://github.com/pydantic> |
| `pydantic-settings` | `2.14.0` | MIT | <https://github.com/pydantic/pydantic-settings> |
| `pygments` | `2.20.0` | BSD-2-Clause | <https://pygments.org> |
| `pyjwt` | `2.12.1` | MIT | <https://github.com/jpadilla/pyjwt> |
| `pyperclip` | `1.11.0` | BSD License | <https://github.com/asweigart/pyperclip> |
| `python-dotenv` | `1.2.2` | BSD-3-Clause | <https://github.com/theskumar/python-dotenv> |
| `python-multipart` | `0.0.27` | Apache-2.0 | <https://github.com/Kludex/python-multipart> |
| `pywin32` | `(conditional)` | PSF-2.0 | <https://github.com/mhammond/pywin32> |
| `pywin32-ctypes` | `(conditional)` | BSD-3-Clause | <https://github.com/enthought/pywin32-ctypes> |
| `pyyaml` | `6.0.3` | MIT License | <https://pyyaml.org/> |
| `referencing` | `0.37.0` | MIT | <https://github.com/python-jsonschema/referencing> |
| `rich` | `15.0.0` | MIT License | <https://github.com/Textualize/rich> |
| `rich-rst` | `1.3.2` | MIT | <https://github.com/wasi-master/rich-rst> |
| `rpds-py` | `0.30.0` | MIT | <https://github.com/crate-py/rpds> |
| `secretstorage` | `(conditional)` | BSD-3-Clause | <https://github.com/mitya57/secretstorage> |
| `sse-starlette` | `3.4.1` | BSD-3-Clause | <https://github.com/sysid/sse-starlette> |
| `starlette` | `1.0.0` | BSD-3-Clause | <https://github.com/Kludex/starlette> |
| `tomli` | `(conditional)` | MIT | <https://github.com/hukkin/tomli> |
| `typing-extensions` | `4.15.0` | PSF-2.0 | <https://github.com/python/typing_extensions> |
| `typing-inspection` | `0.4.2` | MIT | <https://github.com/pydantic/typing-inspection> |
| `uncalled-for` | `0.3.1` | MIT License | <https://github.com/chrisguidry/uncalled-for> |
| `uvicorn` | `0.46.0` | BSD-3-Clause | <https://uvicorn.dev/> |
| `watchfiles` | `1.1.1` | MIT License | <https://github.com/samuelcolvin/watchfiles> |
| `websockets` | `16.0` | BSD-3-Clause | <https://github.com/python-websockets/websockets> |
| `zipp` | `3.23.1` | MIT | <https://github.com/jaraco/zipp> |

## How this is computed

1. `uv export --no-dev --frozen` enumerates the runtime dependency
   graph (excludes `[project.optional-dependencies].dev` and
   `.docs`).
2. For each package, `importlib.metadata` is queried in this order:
   PEP 639 `License-Expression` field, then trove classifiers,
   then the legacy `License` field.
3. Categorisation is keyword-based — see `classify` in
   `scripts/gen_licenses.py`.

## Caveats

* Trove classifiers can be misleading. Notably, `docutils` advertises
  itself as `Public Domain / BSD License / GNU General Public License
  (GPL)`; in practice the shipped Python code is BSD-2-Clause /
  Public Domain. The classifier carries the historical multi-license
  text, not the runtime-licence-of-record.
* `certifi` and `pathspec` are MPL-2.0 — *file-level* copyleft.
  Just depending on them imposes no obligations; only modifications
  to their source files trigger copyleft terms.
* This page is regenerated from the *currently installed* venv. The
  pinned versions in CI may drift slightly from local development;
  the docs build is the canonical render.
