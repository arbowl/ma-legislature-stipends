"""Compute stipend tiers for Massachusetts legislators based on their roles and
responsibilities.'
"""

from __future__ import annotations

from dataclasses import dataclass
from models.core import StipendTierCode


@dataclass(frozen=True)
class StipendTier:
    """A stipend tier definition"""

    id: str
    base_amount: int
