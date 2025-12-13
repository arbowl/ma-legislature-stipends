"""Massachusetts General Law Chapter 9B rules for computing legislator
stipends.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from models.core import (
    RoleAssignment,
    Session,
    Member,
    StipendTierCode,
)
from config.role_catalog import (
    ROLE_DEFINITIONS,
    get_role_definition,
)


@dataclass(frozen=True)
class RoleStipend:
    role_code: str
    session_id: str
    amount: int
    reason: str


def _session_adjustment_factor(session: Session) -> float:
    """Add adjustments to stipend tiers"""
    return 1.0  # Placeholder


def stipend_for_role_assignment(
    assignment: RoleAssignment,
    session: Session
) -> Optional[RoleStipend]:
    """Compute the stipend based on role, session, and adjustment factor"""
    role_def = get_role_definition(assignment.role_code)
    tier_id = role_def.stipend_tier_id
    if tier_id is None:
        return None
    tier = StipendTierCode.get_base_amount(tier_id)
    factor = _session_adjustment_factor(session)
    adjusted = round(tier * factor)
    return RoleStipend(
        role_code=assignment.role_code,
        session_id=assignment.session_id,
        amount=adjusted,
        reason=f"Tier {tier_id} base {tier} adjusted by factor {factor}",
    )


def raw_role_stipends_for_member(
    member: Member,
    session: Session
) -> list[RoleStipend]:
    """Get stipends for role"""
    stipends: list[RoleStipend] = []
    for ra in member.roles:
        if ra.session_id != session.id:
            continue
        rs = stipend_for_role_assignment(ra, session)
        if rs is None:
            continue
        stipends.append(rs)
    return stipends
