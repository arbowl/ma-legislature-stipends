"""Travel stipends"""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Optional

from audit.provenance import AmountWithProvenance, ap_scale
from models.core import Member, Session
from config.travel_config import TRAVEL_RULE_9C
from config.comp_adjustment import load_travel_adjustment


@dataclass(frozen=True)
class TravelAllowance:
    """Stipends for travel"""

    member_id: str
    session_id: str
    amount: AmountWithProvenance
    distance_miles: Optional[float]
    rule_applied: str


@dataclass(frozen=True)
class DistanceException:
    """Encodes manual distance overrides"""

    override_reason: str
    distance_miles_from_state_house: Optional[float] = None

    @staticmethod
    def from_dict(json_data: dict[str, str | float], code: str) -> DistanceException:
        """Generates a DistanceException from a JSON"""
        data: dict = json_data[code]
        return DistanceException(
            override_reason=data["override_reason"],
            distance_miles_from_state_house=data.get("distance_miles_from_state_house"),
        )


def load_district_exceptions() -> dict[str, DistanceException]:
    """Loads the district exception files"""
    json_path = Path("data/sessions/2025-2026/distance_exceptions.json")
    with open(json_path, "r") as f:
        data = json.load(f)
        return {code: DistanceException.from_dict(data, code) for code in data}


DISTRICT_EXCEPTIONS = load_district_exceptions()
"""Dictionary of `member_codes: DistanceException`"""


def travel_9c_for_member(member: Member, session: Session) -> TravelAllowance:
    """Calculates the travel stipend for a member"""
    exceptions: bool = False
    if member.member_id not in DISTRICT_EXCEPTIONS:
        d = member.distance_miles_from_state_house
    else:
        if DISTRICT_EXCEPTIONS[member.member_id].distance_miles_from_state_house:
            d = DISTRICT_EXCEPTIONS[member.member_id].distance_miles_from_state_house
        else:
            d = member.distance_miles_from_state_house
            exceptions = True
    if d is None:
        raise ValueError(
            f"Missing distance_miles_from_state_house " f"for member {member.member_id}"
        )
    rule = TRAVEL_RULE_9C
    if d <= rule.distance_threshold_miles:
        amount = rule.amount_leq_threshold
        rule_applied = (
            f"distance {d:.1f} <= {rule.distance_threshold_miles} miles "
            f"-> ${rule.amount_leq_threshold.value}"
        )
    else:
        amount = rule.amount_gt_threshold
        rule_applied = (
            f"distance {d:.1f} > {rule.distance_threshold_miles} miles "
            f"-> ${rule.amount_gt_threshold.value}"
        )
    if exceptions:
        if amount == rule.amount_gt_threshold:
            amount = rule.amount_leq_threshold
        else:
            amount = rule.amount_gt_threshold
        rule_applied = (
            DISTRICT_EXCEPTIONS[member.member_id].override_reason
        ) + f" -> ${amount.value}"
    adjustment = load_travel_adjustment(session.id)
    if adjustment.factor > 1.0:
        amount = ap_scale(amount, adjustment.factor)
    return TravelAllowance(
        member_id=member.member_id,
        session_id=session.id,
        amount=amount,
        distance_miles=d,
        rule_applied=rule_applied,
    )
