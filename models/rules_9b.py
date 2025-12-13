"""Massachusetts General Law Chapter 9B rules for computing legislator
stipends.
"""

from __future__ import annotations

from itertools import combinations
from dataclasses import dataclass
from typing import Optional

from models.core import (
    RoleAssignment,
    Session,
    Member,
    StipendTierCode,
    RoleCode,
    CommitteeRoleType,
)
from config.role_catalog import (
    ROLE_DEFINITIONS,
    get_role_definition,
)


@dataclass(frozen=True)
class RoleStipend:
    """Stipend given for a role"""

    role_code: str
    session_id: str
    amount: int
    reason: str


@dataclass(frozen=True)
class PaidRoleSelection:
    """Result of applying caps"""

    session_id: str
    member_id: str
    paid_roles: list[RoleStipend]
    total_amount: int


def _session_adjustment_factor(session: Session) -> float:
    """Add adjustments to stipend tiers"""
    return 1.0  # Placeholder


def _is_committee_chair(role_code: RoleCode) -> bool:
    rd = get_role_definition(role_code)
    return rd.committee_role_type == CommitteeRoleType.CHAIR


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


def subset_key(
    subset: tuple[RoleStipend, ...]
) -> tuple[int, tuple[str, ...]]:
    """Generate sorted tuple of stipends and codes"""
    total = sum(r.amount for r in subset)
    codes = tuple(sorted(r.role_code for r in subset))
    return (total, codes)


def select_paid_roles_for_member(
    member: Member,
    session: Session,
) -> PaidRoleSelection:
    """Apply 9B constraints"""
    raw = raw_role_stipends_for_member(member, session)
    if not raw:
        return PaidRoleSelection(
            session_id=session.id,
            member_id=member.member_id,
            paid_roles=[],
            total_amount=0,
        )
    candidates: list[tuple[RoleStipend, bool]] = [
        (rs, _is_committee_chair(rs.role_code)) for rs in raw
    ]
    if len(candidates) == 1:
        rs, _is_chair = candidates[0]
        return PaidRoleSelection(
            session_id=session.id,
            member_id=member.member_id,
            paid_roles=[rs],
            total_amount=rs.amount,
        )
    best_subset: tuple[RoleStipend, ...] = tuple()
    best_amount = 0
    all_rs_only = [rs for (rs, _is_chair) in candidates]
    for k in (1, 2):
        for combo in combinations(all_rs_only, k):
            chair_count = sum(
                1 for rs in combo if _is_committee_chair(rs.role_code)
            )
            if chair_count > 1:
                continue
            total = sum(rs.amount for rs in combo)
            if total > best_amount:
                best_amount = total
                best_subset = combo
            elif total == best_amount and best_subset:
                if subset_key(combo) < subset_key(best_subset):
                    best_subset = combo
    if not best_subset and raw:
        best_subset = (max(raw, key=lambda r: r.amount),)
        best_amount = sum(r.amount for r in best_subset)
    paid_roles_sorted = sorted(
        best_subset, key=lambda r: (-r.amount, r.role_code)
    )
    return PaidRoleSelection(
        session_id=session.id,
        member_id=member.member_id,
        paid_roles=paid_roles_sorted,
        total_amount=best_amount,
    )


def stipend_9b_for_member(member: Member, session: Session) -> int:
    """Public helper to return total 9B stipend for a member"""
    selection = select_paid_roles_for_member(member, session)
    return selection.total_amount
