"""Travel rules"""

from __future__ import annotations

from dataclasses import dataclass

from audit.provenance import AmountWithProvenance, ap_from
from audit.sources_registry import MGL_3_9C


@dataclass(frozen=True)
class TravelRule:
    """Encodes the 9C logic constants"""

    distance_threshold_miles: float
    amount_leq_threshold: AmountWithProvenance
    amount_gt_threshold: AmountWithProvenance


TRAVEL_RULE_9C = TravelRule(
    distance_threshold_miles=50.0,
    amount_leq_threshold=ap_from(15_000, MGL_3_9C),
    amount_gt_threshold=ap_from(20_000, MGL_3_9C),
)
