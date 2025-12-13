"""Travel stipends"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


from models.core import Member, Session
from config.travel_config import TRAVEL_RULE_9C


@dataclass(frozen=True)
class TravelAllowance:
    """Stipends for travel"""

    member_id: str
    session_id: str
    amount: int
    distance_miles: Optional[float]
    rule_applied: str


def travel_9c_for_member(member: Member, session: Session) -> TravelAllowance:
    """Calculates the travel stipend for a member"""
    d = member.distance_miles_from_state_house
    if d is None:
        raise ValueError(
            f"Missing distance_miles_from_state_house "
            f"for member {member.member_id}"
        )
    rule = TRAVEL_RULE_9C
    if d <= rule.distance_threshold_miles:
        amount = rule.amount_leq_threshold
        rule_applied = (
            f"distance {d:.1f} <= {rule.distance_threshold_miles} miles "
            f"-> ${rule.amount_leq_threshold}"
        )
    else:
        amount = rule.amount_gt_threshold
        rule_applied = (
            f"distance {d:.1f} > {rule.distance_threshold_miles} miles "
            f"-> ${rule.amount_gt_threshold}"
        )
    return TravelAllowance(
        member_id=member.member_id,
        session_id=session.id,
        amount=amount,
        distance_miles=d,
        rule_applied=rule_applied,
    )
