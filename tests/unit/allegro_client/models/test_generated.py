"""Smoke tests for the codegen Pydantic models.

These confirm the generated module imports and that a representative slice
of public-facing types is present. The bulk of correctness is delegated to
Pydantic's own runtime validation; these tests are a sanity check that
``make gen-models`` produced sane output, not a contract suite for the
shape of every model (the OpenAPI spec is authoritative for that).
"""

from __future__ import annotations

from pathlib import Path

import pytest

# tests/unit/allegro_client/models/test_generated.py → repo root is 4 levels up.
REPO_ROOT = Path(__file__).resolve().parents[4]
GENERATED = REPO_ROOT / "src" / "allegro_client" / "models" / "_generated"


def test_module_imports() -> None:
    """Every generated class instantiates lazily as the module loads."""
    import allegro_client.models._generated.models as gen

    classes = [name for name in dir(gen) if isinstance(getattr(gen, name), type)]
    # The OpenAPI spec at the time of writing produced 1 100+ classes.
    # Lower the threshold if the spec ever shrinks materially.
    assert len(classes) > 500, f"unexpectedly small generated surface: {len(classes)}"


def test_banner_present() -> None:
    """``make gen-models`` writes a checksum banner; a freshness check on CI
    relies on it. Verify it survived the codegen + format pipeline.
    """
    init = (GENERATED / "__init__.py").read_text()
    assert "Pydantic models generated" in init
    assert "Spec checksum: sha256:" in init


@pytest.mark.parametrize(
    "name",
    [
        "Offer",
        "Order",
        "Category",
        "Product",
        "Marketplace",
        "BillingEntry",
        "Promotion",
        "Auction",
        "Thread",
        "Message",
        "UserRating",
        "BadgeCampaign",
        "Payment",
    ],
)
def test_canonical_models_exist(name: str) -> None:
    """Each top-level resource has at least one class with the expected name.

    OpenAPI codegen emits suffix-collision variants (``Offer``, ``Offer1``, …)
    when the spec defines multiple inline schemas with the same name; this
    test only asserts that the canonical (unsuffixed) name is present.
    """
    import allegro_client.models._generated.models as gen

    assert hasattr(gen, name), f"missing generated model: {name}"


def test_marketplace_minimal_payload() -> None:
    """Marketplace is one of the few models with a stable enough shape that
    we can pin a minimal-payload smoke test against it.

    Allegro's ``GET /marketplaces`` returns objects with at least an ``id``;
    every other field is optional in the spec. If this ever fails the spec
    has tightened — re-check and update the test rather than reverting.
    """
    from allegro_client.models._generated.models import Marketplace

    fields = Marketplace.model_fields
    # Pick the smallest payload that satisfies every required field. This
    # is a robust shape test even if the spec adds more required fields
    # later — it just means we update the dict here.
    required = {name: _placeholder_for(info) for name, info in fields.items() if info.is_required()}
    Marketplace.model_validate(required)


def _placeholder_for(info: object) -> object:
    """Generate a minimal value satisfying the field's type for shape tests."""
    annotation = getattr(info, "annotation", None)
    # Optimistic: most required string fields are happy with a non-empty str.
    # Numeric fields with constraints will surface as test failures we then
    # tighten by hand. Keeping the placeholder logic simple is deliberate.
    if annotation is str or _is_optional_of(annotation, str):
        return "x"
    if annotation is int:
        return 1
    if annotation is float:
        return 1.0
    if annotation is bool:
        return False
    return "x"


def _is_optional_of(annotation: object, target: type) -> bool:
    import typing

    if typing.get_origin(annotation) in {typing.Union, type(None) | int}:
        return target in typing.get_args(annotation)
    return False
