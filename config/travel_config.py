"""Travel rules"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class TravelRule:
    """Encodes the 9C logic constants"""

    distance_threshold_miles: float
    amount_leq_threshold: int
    amount_gt_threshold: int


TRAVEL_RULE_9C = TravelRule(
    distance_threshold_miles=50.0,
    amount_leq_threshold=15_000,
    amount_gt_threshold=20_000,
)
