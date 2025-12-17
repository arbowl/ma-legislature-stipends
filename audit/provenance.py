"""Auditability"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Iterable, Optional


class SourceKind(Enum):
    """Where the source comes from"""

    STATUTE = auto()
    OFFICIAL_WEBSITE = auto()
    ECONOMIC_SERIES = auto()
    DATA_FILE = auto()
    CALCULATION = auto()
    MANUAL_OVERRIDE = auto()


@dataclass(frozen=True)
class SourceRef:
    """Direct link to the source"""

    id: str
    label: str
    kind: SourceKind
    url: Optional[str] = None
    details: frozenset = field(default_factory=frozenset)


@dataclass(frozen=True)
class AmountWithProvenance:
    """Cited amount"""

    value: int
    sources: frozenset[SourceRef] = field(default_factory=frozenset)


def ap_zero() -> AmountWithProvenance:
    """Generates a zero provenance artifact"""
    return AmountWithProvenance(value=0, sources=frozenset())


def ap_from(value: int, *sources: SourceRef) -> AmountWithProvenance:
    """Generates a provenance artifact from data"""
    return AmountWithProvenance(value=value, sources=frozenset(sources))


def ap_add(
    a: AmountWithProvenance, b: AmountWithProvenance
) -> AmountWithProvenance:
    """Adds two provenance artifacts"""
    return AmountWithProvenance(
        value=a.value + b.value, sources=a.sources | b.sources
    )


def ap_sum(amounts: Iterable[AmountWithProvenance]) -> AmountWithProvenance:
    """Combines provenance artifacts"""
    total = ap_zero()
    for a in amounts:
        total = ap_add(total, a)
    return total


def ap_scale(
    a: AmountWithProvenance, factor: float, **extra_sources: SourceRef
) -> AmountWithProvenance:
    """Scales provenance artifacts according to BEA"""
    new_value = round(a.value * factor)
    return AmountWithProvenance(
        value=new_value, sources=a.sources | frozenset(extra_sources.values())
    )
