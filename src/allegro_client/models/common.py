"""Hand-written Pydantic models that complement the codegen output.

Anything codegen leaves gaps for, anything that needs custom validators,
and anything we want a stable hand-curated shape for (e.g. pagination
envelopes) lives here. The codegen-generated models import this module via
``allegro_client.models``; nothing here imports the generated tree, to
keep the dependency direction acyclic.
"""

from __future__ import annotations

from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class _AllegroModel(BaseModel):
    """Common base configuration for hand-written Allegro models.

    Mirrors the conventions used by datamodel-code-generator output so the
    public API feels uniform regardless of whether a model came from
    codegen or this file.
    """

    model_config = ConfigDict(populate_by_name=True, extra="ignore")


class Money(_AllegroModel):
    """Allegro's standard monetary amount: ``{"amount": "12.34", "currency": "PLN"}``.

    The wire format is a string for ``amount``; we store it as ``Decimal``
    to preserve precision. JSON output round-trips back to a string.
    """

    amount: Decimal
    currency: str = Field(min_length=3, max_length=3, description="ISO 4217 currency code.")


class Marketplace(_AllegroModel):
    """One entry from ``GET /marketplaces``.

    Kept hand-written even though codegen would produce a similar shape:
    this model is referenced from tutorial docs and tool examples, so we
    want a stable name regardless of upstream renames.
    """

    id: str
    name: str
    country: str | None = None


class PaginationInfo(_AllegroModel):
    """Page metadata returned alongside list-style endpoints.

    Allegro mixes two styles: offset/limit (``totalCount``) and cursor
    (``nextPage``). Both fields are optional; the non-applicable one is
    simply absent on the wire.
    """

    total_count: int | None = Field(default=None, alias="totalCount")
    next_page: str | None = Field(default=None, alias="nextPage")
