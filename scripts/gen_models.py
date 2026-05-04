#!/usr/bin/env python3
"""Codegen Pydantic models from Allegro's official OpenAPI 3.0 spec.

Source of truth: https://developer.allegro.pl/swagger.yaml

Run via ``make gen-models``. Output lands at
``src/allegro_client/models/_generated/`` and is committed; this script is
re-run when the upstream spec moves.

Why a wrapper around ``datamodel-codegen``: we want a single switch for
target-python-version, output mode, and the post-processing step that
appends a checksum banner so :mod:`scripts.check_models_freshness` can
detect drift on CI.
"""

from __future__ import annotations

import hashlib
import shutil
import subprocess
import sys
import urllib.request
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CACHE_DIR = REPO_ROOT / ".cache"
SPEC_URL = "https://developer.allegro.pl/swagger.yaml"
SPEC_PATH = CACHE_DIR / "swagger.yaml"
OUTPUT_DIR = REPO_ROOT / "src" / "allegro_client" / "models" / "_generated"
# datamodel-codegen emits one giant module by default. Splitting one-class-per-file
# turns a 30 kLOC module into 1 000+ files which makes git diffs and IDE jumps
# painful. We keep everything in ``models.py`` and curate the public surface in
# ``models/__init__.py``.
OUTPUT_FILE = OUTPUT_DIR / "models.py"


def fetch_spec(force: bool = False) -> Path:
    """Download the Allegro OpenAPI spec to ``.cache/swagger.yaml``."""
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    if force or not SPEC_PATH.exists():
        print(f"→ downloading {SPEC_URL}")
        with urllib.request.urlopen(SPEC_URL) as resp:  # noqa: S310 — known URL
            SPEC_PATH.write_bytes(resp.read())
    print(f"  spec at {SPEC_PATH} ({SPEC_PATH.stat().st_size:,} bytes)")
    return SPEC_PATH


def reset_output() -> None:
    """Wipe the previous generated tree, keeping the package marker."""
    if OUTPUT_DIR.exists():
        shutil.rmtree(OUTPUT_DIR)
    OUTPUT_DIR.mkdir(parents=True)
    # The package marker is rewritten by :func:`write_banner`; keep an empty
    # placeholder here so codegen running in parallel doesn't trip on a
    # missing ``__init__.py``.
    (OUTPUT_DIR / "__init__.py").write_text("")


def run_codegen(spec: Path) -> None:
    """Invoke ``datamodel-codegen`` against the cached spec."""
    cmd = [
        "datamodel-codegen",
        "--input",
        str(spec),
        "--input-file-type",
        "openapi",
        "--output",
        str(OUTPUT_FILE),
        "--output-model-type",
        "pydantic_v2.BaseModel",
        "--target-python-version",
        "3.10",
        "--use-annotated",
        "--use-union-operator",
        "--use-standard-collections",
        "--use-double-quotes",
        "--use-schema-description",
        "--field-constraints",
        # ``all`` instead of ``one``: discriminated unions in Pydantic v2
        # require the discriminator field to be ``Literal[...]``; if even one
        # member's discriminator is a plain ``Enum`` Pydantic refuses to
        # build the schema. Forcing every enum to a Literal keeps the
        # discriminator inference happy at the cost of verbosity.
        "--enum-field-as-literal",
        "all",
        "--disable-timestamp",
    ]
    print(f"→ {' '.join(cmd)}")
    subprocess.run(cmd, check=True)


def strip_discriminators() -> None:
    """Strip ``discriminator="..."`` keyword from generated ``Field`` calls.

    OpenAPI's ``discriminator`` directive maps to Pydantic v2 discriminated
    unions, but they require every member's discriminator field to be
    ``Literal[...]``. datamodel-code-generator emits the discriminator
    keyword even when it has produced a parent class whose discriminator
    field is plain ``str`` — Pydantic refuses to build the schema in that
    case. We drop the argument; runtime validation against the parent class
    still works (just without auto-dispatch into the subclass).
    """
    import re

    src = OUTPUT_FILE.read_text()
    # Match `, discriminator="changeType"` or `discriminator="changeType",`
    # within Field(...) calls, removing leading or trailing comma and any
    # surrounding whitespace cleanly.
    patterns = [
        re.compile(r',\s*discriminator="[^"]+"'),
        re.compile(r'discriminator="[^"]+",\s*'),
        re.compile(r'discriminator="[^"]+"'),
    ]
    for pat in patterns:
        src = pat.sub("", src)
    OUTPUT_FILE.write_text(src)


def write_banner(spec: Path) -> None:
    """Stash a checksum banner so :mod:`check_models_freshness` can spot drift."""
    digest = hashlib.sha256(spec.read_bytes()).hexdigest()
    init = OUTPUT_DIR / "__init__.py"
    banner = (
        '"""Pydantic models generated from the official Allegro OpenAPI spec.\n\n'
        "DO NOT edit files in this package by hand. Run ``make gen-models`` to\n"
        "regenerate from ``https://developer.allegro.pl/swagger.yaml``. Linting\n"
        "and strict typing are relaxed for this subtree (see ``pyproject.toml``);\n"
        "the contract is enforced at runtime by Pydantic validation, not by mypy.\n\n"
        f"Spec checksum: sha256:{digest}\n"
        '"""\n\n'
    )
    existing = init.read_text() if init.exists() else ""
    init.write_text(banner + _strip_existing_banner(existing))


def _strip_existing_banner(text: str) -> str:
    """Drop a previously written banner so we don't stack them on each run."""
    if text.startswith('"""Pydantic models generated from the official Allegro'):
        # Find the second triple-quote that closes the banner, then skip past
        # the trailing blank line.
        end = text.find('"""', 3)
        if end != -1:
            return text[end + 3 :].lstrip("\n")
    return text


def format_output() -> None:
    """Run ruff format on the generated tree so blame diffs are stable."""
    subprocess.run(
        ["ruff", "format", str(OUTPUT_DIR)],
        check=False,  # generated code is exempt from lint, formatting is best-effort.
    )


def main(argv: list[str] | None = None) -> int:
    args = argv or sys.argv[1:]
    force = "--force" in args
    spec = fetch_spec(force=force)
    reset_output()
    run_codegen(spec)
    strip_discriminators()
    write_banner(spec)
    format_output()
    print(f"✓ generated models at {OUTPUT_DIR}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
