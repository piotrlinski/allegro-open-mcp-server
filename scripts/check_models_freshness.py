#!/usr/bin/env python3
"""Detect drift between the upstream Allegro OpenAPI spec and the codegen banner.

Run via ``make check-models-freshness``. Compares the SHA-256 of the live
spec at https://developer.allegro.pl/swagger.yaml against the checksum line
written into ``src/allegro_client/models/_generated/__init__.py`` by
``scripts.gen_models``. Exits 0 on match, 0 with a warning on mismatch
(non-fatal so CI doesn't fail when Allegro pushes a routine spec update),
and 1 only when the banner is missing or malformed.
"""

from __future__ import annotations

import hashlib
import re
import sys
import urllib.request
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
GENERATED_INIT = REPO_ROOT / "src" / "allegro_client" / "models" / "_generated" / "__init__.py"
SPEC_URL = "https://developer.allegro.pl/swagger.yaml"
BANNER_RE = re.compile(r"Spec checksum: sha256:([0-9a-f]{64})")


def main() -> int:
    init_text = GENERATED_INIT.read_text()
    match = BANNER_RE.search(init_text)
    if match is None:
        print(
            f"ERROR: no spec-checksum banner in {GENERATED_INIT.relative_to(REPO_ROOT)};"
            " run `make gen-models`.",
            file=sys.stderr,
        )
        return 1
    cached_digest = match.group(1)

    print(f"→ fetching {SPEC_URL}")
    with urllib.request.urlopen(SPEC_URL) as resp:
        upstream = resp.read()
    upstream_digest = hashlib.sha256(upstream).hexdigest()

    if cached_digest == upstream_digest:
        print(f"✓ in sync ({cached_digest[:12]}…)")
        return 0

    print(
        f"⚠ spec drift detected:\n"
        f"  cached:   {cached_digest}\n"
        f"  upstream: {upstream_digest}\n"
        f"  → run `make gen-models` to refresh, then review the diff."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
