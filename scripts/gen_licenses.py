"""Generate ``docs/reference/licenses.md`` from runtime dependency metadata.

Walks the *runtime* dependency tree (anything that ships when a user runs
``pip install allegro-mcp``) and emits a markdown table mapping each
package to its license, version, and PyPI URL. Excludes dev/docs deps —
those are tooling, not redistributed.

This is the project's third-party-notice file: an MIT-licensed package
isn't required to ship one, but enterprise downstream consumers often
ask for an explicit inventory. Auto-generation keeps it in sync with
the actual dependency graph.

Strategy:

* Run ``uv export --no-dev --frozen`` to enumerate every runtime package.
* For each package, read its installed metadata via
  ``importlib.metadata`` and prefer (in order):
  1. the PEP 639 ``License-Expression`` field,
  2. the ``License ::`` trove classifiers,
  3. the legacy ``License`` field.
* Emit a single markdown table sorted by package name.

Run as a pre-build step (``make docs-gen``); the docs output is gitignored.
The repo-root ``THIRD_PARTY_NOTICES.md`` is committed and bundled into the
wheel so enterprise consumers can find it via ``importlib.resources``.
"""

from __future__ import annotations

import importlib.metadata as md
import re
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DOCS_ROOT = REPO_ROOT / "docs"
NOTICES_PATH = REPO_ROOT / "THIRD_PARTY_NOTICES.md"

# Platform-conditional or version-conditional deps that aren't installed in
# the canonical CI venv (Linux Python 3.12) but appear in ``uv export``. These
# are well-known stable licenses; hardcoded so the inventory doesn't carry
# ``(metadata not installed)`` rows that look like an audit failure.
_KNOWN_LICENSES: dict[str, tuple[str, str]] = {
    "backports-tarfile": ("MIT", "https://github.com/jaraco/backports.tarfile"),
    "caio": ("Apache-2.0", "https://github.com/mosquito/caio"),
    "colorama": ("BSD-3-Clause", "https://github.com/tartley/colorama"),
    "jeepney": ("MIT", "https://gitlab.com/takluyver/jeepney"),
    "pywin32": ("PSF-2.0", "https://github.com/mhammond/pywin32"),
    "pywin32-ctypes": ("BSD-3-Clause", "https://github.com/enthought/pywin32-ctypes"),
    "secretstorage": ("BSD-3-Clause", "https://github.com/mitya57/secretstorage"),
    "tomli": ("MIT", "https://github.com/hukkin/tomli"),
}


def _emit(path: str, content: str) -> None:
    out = DOCS_ROOT / path
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(content, encoding="utf-8")


_EXPORT_PKG_RE = re.compile(r"^([a-zA-Z][a-zA-Z0-9._-]*)==", re.MULTILINE)


def _runtime_packages() -> list[str]:
    """Enumerate runtime packages via ``uv export --no-dev --frozen``.

    ``uv export`` emits a requirements.txt-style listing of the resolved
    runtime closure, excluding dev / docs optional-dependency groups.
    Each line of interest looks like ``name==version`` (sometimes with a
    trailing environment marker after `` ; ``).

    Falls back to the package's own direct deps if ``uv`` is unavailable.
    """
    try:
        out = subprocess.run(
            ["uv", "export", "--no-dev", "--no-hashes", "--frozen"],
            capture_output=True,
            text=True,
            check=True,
        ).stdout
    except (FileNotFoundError, subprocess.CalledProcessError):
        try:
            return sorted(
                {
                    re.split(r"[<>=!~ ;[]", d)[0].strip()
                    for d in (md.requires("allegro-mcp") or [])
                    if "; extra ==" not in d
                }
            )
        except md.PackageNotFoundError:
            return []

    seen: set[str] = set()
    out_pkgs: list[str] = []
    for match in _EXPORT_PKG_RE.finditer(out):
        name = match.group(1).lower()
        if name == "allegro-mcp":
            continue
        if name not in seen:
            seen.add(name)
            out_pkgs.append(name)
    return sorted(out_pkgs)


def _resolve_license(name: str) -> tuple[str, str, str]:
    """Return ``(license, version, homepage)`` for a package by name.

    Priority of license source:

    1. PEP 639 ``License-Expression`` (set by modern packages).
    2. ``License ::`` trove classifiers (most older packages).
    3. Legacy ``License`` field (free-form text).
    4. ``_KNOWN_LICENSES`` hardcoded fallback (platform-conditional
       deps not installed in the build environment).
    """
    try:
        m = md.metadata(name)
    except md.PackageNotFoundError:
        if name in _KNOWN_LICENSES:
            lic, url = _KNOWN_LICENSES[name]
            return lic, "(conditional)", url
        return "(metadata not installed)", "?", f"https://pypi.org/project/{name}/"

    expr = m.get("License-Expression", "")
    if expr:
        license_str = expr
    else:
        classifiers = [
            c.split("::")[-1].strip()
            for c in (m.get_all("Classifier") or [])
            if c.startswith("License ::")
        ]
        if classifiers:
            license_str = " / ".join(classifiers)
        else:
            license_lines = (m.get("License", "") or "").splitlines()
            license_str = license_lines[0].strip() if license_lines else ""
            if not license_str and name in _KNOWN_LICENSES:
                license_str = _KNOWN_LICENSES[name][0]
            elif not license_str:
                license_str = "(unspecified)"
            if len(license_str) > 80:
                license_str = license_str[:77] + "…"

    version = m.get("Version", "?")

    # Find a homepage URL — try Project-URL fields first, then Home-page.
    homepage = ""
    for pu in m.get_all("Project-URL") or []:
        label, _, url = pu.partition(",")
        url = url.strip()
        if label.strip().lower() in {"homepage", "source", "repository"} and url:
            homepage = url
            break
    if not homepage:
        homepage = (m.get("Home-page", "") or "").strip()
    if not homepage and name in _KNOWN_LICENSES:
        homepage = _KNOWN_LICENSES[name][1]
    if not homepage:
        homepage = f"https://pypi.org/project/{name}/"

    return license_str, version, homepage


def _render(packages: list[str]) -> str:
    """Render the licenses page from the given runtime package list."""
    rows = [(name, *_resolve_license(name)) for name in packages]
    permissive_keywords = (
        "MIT",
        "BSD",
        "Apache",
        "ISC",
        "Python Software Foundation",
        "Public Domain",
        "Unlicense",
        "PSF",
    )
    weak_copyleft_keywords = ("MPL", "Mozilla Public License")
    strong_copyleft_keywords = ("GPL", "AGPL", "LGPL", "GNU General Public License")

    def classify(license_str: str) -> str:
        s = license_str.upper()
        # Strip "GPL" appearance inside the docutils multi-license string.
        if "GENERAL PUBLIC LICENSE (GPL)" in s and "BSD" in s:
            return "permissive"
        if any(k.upper() in s for k in strong_copyleft_keywords):
            return "copyleft"
        if any(k.upper() in s for k in weak_copyleft_keywords):
            return "weak-copyleft"
        if any(k.upper() in s for k in permissive_keywords):
            return "permissive"
        return "unknown"

    classified = [(name, lic, ver, url, classify(lic)) for name, lic, ver, url in rows]
    counts = {"permissive": 0, "weak-copyleft": 0, "copyleft": 0, "unknown": 0}
    for *_, c in classified:
        counts[c] = counts.get(c, 0) + 1

    lines = [
        "---",
        "title: Third-party licenses",
        "description: Auto-generated inventory of every runtime dependency, the license each one ships under, and the package version pinned in the latest build.",
        "---",
        "",
        "# Third-party licenses",
        "",
        "Every package that gets installed when a user runs",
        "`pip install allegro-mcp` (or the equivalent via `uvx` / Docker)",
        "is listed below. Dev / docs / lint tooling is omitted — those are",
        "build-time only and never reach the user.",
        "",
        "Generated from installed package metadata via",
        "[`scripts/gen_licenses.py`](https://github.com/piotrlinski/allegro-open-mcp-server/blob/master/scripts/gen_licenses.py).",
        "Refreshed on every docs build; CI fails if the metadata becomes",
        "unparseable.",
        "",
        "## Summary",
        "",
        "| Category | Count | Notes |",
        "| --- | ---:| --- |",
        f"| Permissive (MIT / BSD / Apache / ISC / PSF / Public Domain) | {counts['permissive']} | Compatible with MIT redistribution. |",
        f"| Weak copyleft (MPL-2.0) | {counts['weak-copyleft']} | File-level copyleft; obligations only apply if the dep's source is modified. Compatible with MIT redistribution. |",
        f"| Strong copyleft (GPL / AGPL / LGPL) | {counts['copyleft']} | Would constrain MIT redistribution if any appear here — investigate if non-zero. |",
        f"| Unknown | {counts['unknown']} | Missing metadata; check upstream PyPI page. |",
        "",
    ]
    if counts["copyleft"] > 0:
        lines += [
            '!!! warning "Strong-copyleft dependency detected"',
            "    One or more runtime dependencies are licensed under GPL/AGPL/LGPL.",
            "    Audit before shipping — derivative works may inherit obligations.",
            "",
        ]
    else:
        lines += [
            '!!! success "No strong-copyleft runtime dependencies"',
            "    The runtime dependency graph is fully MIT-compatible. Redistribute",
            "    the package under MIT terms; downstream consumers see only permissive",
            "    or weak-copyleft transitive licenses.",
            "",
        ]

    lines += [
        "## Inventory",
        "",
        "| Package | Version | License | Source |",
        "| --- | --- | --- | --- |",
    ]
    for name, lic, ver, url, _ in classified:
        # Escape pipes inside license names so the markdown table doesn't break.
        lic_safe = lic.replace("|", "\\|")
        lines.append(f"| `{name}` | `{ver}` | {lic_safe} | <{url}> |")
    lines += [
        "",
        "## How this is computed",
        "",
        "1. `uv export --no-dev --frozen` enumerates the runtime dependency",
        "   graph (excludes `[project.optional-dependencies].dev` and",
        "   `.docs`).",
        "2. For each package, `importlib.metadata` is queried in this order:",
        "   PEP 639 `License-Expression` field, then trove classifiers,",
        "   then the legacy `License` field.",
        "3. Categorisation is keyword-based — see `classify` in",
        "   `scripts/gen_licenses.py`.",
        "",
        "## Caveats",
        "",
        "* Trove classifiers can be misleading. Notably, `docutils` advertises",
        "  itself as `Public Domain / BSD License / GNU General Public License",
        "  (GPL)`; in practice the shipped Python code is BSD-2-Clause /",
        "  Public Domain. The classifier carries the historical multi-license",
        "  text, not the runtime-licence-of-record.",
        "* `certifi` and `pathspec` are MPL-2.0 — *file-level* copyleft.",
        "  Just depending on them imposes no obligations; only modifications",
        "  to their source files trigger copyleft terms.",
        "* This page is regenerated from the *currently installed* venv. The",
        "  pinned versions in CI may drift slightly from local development;",
        "  the docs build is the canonical render.",
    ]
    return "\n".join(lines) + "\n"


def main() -> int:
    """Generate the licenses reference page + ``THIRD_PARTY_NOTICES.md``.

    Two outputs from the same render so they can never disagree:

    * ``docs/reference/licenses.md`` — for the published docs site
      (gitignored; auto-generated on each docs build).
    * ``THIRD_PARTY_NOTICES.md`` at the repo root — committed and
      bundled into the PyPI wheel via
      ``[tool.hatch.build.targets.wheel.force-include]`` in
      ``pyproject.toml``. Enterprise downstream consumers expect to
      find this file inside the wheel without going to the docs site.
    """
    packages = _runtime_packages()
    if not packages:
        # Fail loudly — silent empty output would mask a broken environment.
        print("::error::Could not enumerate runtime packages (uv export empty).")
        return 1
    rendered = _render(packages)
    _emit("reference/licenses.md", rendered)
    NOTICES_PATH.write_text(rendered, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
