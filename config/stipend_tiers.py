"""Compute stipend tiers for Massachusetts legislators based on their roles and
responsibilities.'
"""

from __future__ import annotations

from dataclasses import dataclass
from models.core import StipendTierCode
from audit.provenance import AmountWithProvenance, ap_from
from audit.sources_registry import MGL_3_9B


@dataclass(frozen=True)
class StipendTier:
    """A stipend tier definition"""

    id: str
    base_amount: AmountWithProvenance


STIPEND_TIERS: dict[StipendTierCode, StipendTier] = {
    StipendTierCode.TIER_80K: StipendTier(
        id=StipendTierCode.TIER_80K,
        base_amount=ap_from(
            StipendTierCode.get_base_amount(StipendTierCode.TIER_80K),
            MGL_3_9B,
        ),
    ),
    StipendTierCode.TIER_65K: StipendTier(
        id=StipendTierCode.TIER_65K,
        base_amount=ap_from(
            StipendTierCode.get_base_amount(StipendTierCode.TIER_65K),
            MGL_3_9B,
        ),
    ),
    StipendTierCode.TIER_60K: StipendTier(
        id=StipendTierCode.TIER_60K,
        base_amount=ap_from(
            StipendTierCode.get_base_amount(StipendTierCode.TIER_60K),
            MGL_3_9B,
        ),
    ),
    StipendTierCode.TIER_50K: StipendTier(
        id=StipendTierCode.TIER_50K,
        base_amount=ap_from(
            StipendTierCode.get_base_amount(StipendTierCode.TIER_50K),
            MGL_3_9B,
        ),
    ),
    StipendTierCode.TIER_35K: StipendTier(
        id=StipendTierCode.TIER_35K,
        base_amount=ap_from(
            StipendTierCode.get_base_amount(StipendTierCode.TIER_35K),
            MGL_3_9B,
        ),
    ),
    StipendTierCode.TIER_30K: StipendTier(
        id=StipendTierCode.TIER_30K,
        base_amount=ap_from(
            StipendTierCode.get_base_amount(StipendTierCode.TIER_30K),
            MGL_3_9B,
        ),
    ),
    StipendTierCode.TIER_15K: StipendTier(
        id=StipendTierCode.TIER_15K,
        base_amount=ap_from(
            StipendTierCode.get_base_amount(StipendTierCode.TIER_15K),
            MGL_3_9B,
        ),
    ),
    StipendTierCode.TIER_5200: StipendTier(
        id=StipendTierCode.TIER_5200,
        base_amount=ap_from(
            StipendTierCode.get_base_amount(StipendTierCode.TIER_5200),
            MGL_3_9B,
        ),
    ),
}


def get_stipend_tier(tier_id: StipendTierCode) -> StipendTier:
    """Returns a stipend tier given a stipend ID"""
    return STIPEND_TIERS[tier_id]
