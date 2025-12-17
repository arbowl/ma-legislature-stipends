"""Massachusetts General Law Chapter 9B rules for computing legislator
stipends.
"""

from __future__ import annotations

from itertools import combinations
from dataclasses import dataclass, field
from typing import Optional, Any

from audit.provenance import AmountWithProvenance, ap_scale, SourceRef
from audit.sources_registry import (
    STIPEND_AMOUNT_ADJUSTMENT,
    SENATE_RULES_11E,
    HOUSE_RULES_18,
)
from models.core import (
    RoleAssignment,
    Session,
    Member,
    StipendTierCode,
    RoleCode,
    CommitteeRoleType,
    Chamber,
)
from config.role_catalog import (
    get_role_definition,
)
from config.comp_adjustment import load_stipend_adjustment


@dataclass(frozen=True)
class RoleStipend:
    """Stipend given for a role"""

    role_code: str
    session_id: str
    amount: AmountWithProvenance
    reason: str


@dataclass(frozen=True)
class PaidRoleSelection:
    """Result of applying caps"""

    session_id: str
    member_id: str
    paid_roles: list[RoleStipend]
    total_amount: int
    provenance: list[RoleSelectionProvenance] = field(default_factory=list)


@dataclass(frozen=True)
class RoleSelectionProvenance:
    """Information about a role stipend"""

    role_code: str
    selected: bool
    reason: str
    notes: dict[str, Any] = field(default_factory=dict)
    sources: frozenset[SourceRef] = field(default_factory=frozenset)


@dataclass(frozen=True)
class ChamberRules:
    """Chamber-specific rules for role selection under 9B"""

    chamber: Chamber
    max_chairs: int
    max_positions: int
    source_ref: SourceRef

    @property
    def description(self) -> str:
        """Human-readable rule description"""
        if self.chamber == Chamber.HOUSE:
            return "House: max 1 chair, max 1 position"
        return "Senate: max 2 chairs, max 2 positions"


def get_chamber_rules(chamber: Chamber) -> ChamberRules:
    """Get the authoritative rules that apply to a specific chamber"""
    if chamber == Chamber.HOUSE:
        return ChamberRules(
            chamber=Chamber.HOUSE,
            max_chairs=1,
            max_positions=1,
            source_ref=HOUSE_RULES_18,
        )
    return ChamberRules(
        chamber=Chamber.SENATE,
        max_chairs=2,
        max_positions=2,
        source_ref=SENATE_RULES_11E,
    )


def _session_adjustment_factor(session: Session) -> float:
    """Add adjustments to stipend tiers"""
    adj = load_stipend_adjustment(session.id)
    return adj.factor


def _is_committee_chair(role_code: RoleCode) -> bool:
    rd = get_role_definition(role_code)
    return rd.committee_role_type == CommitteeRoleType.CHAIR


def stipend_for_role_assignment(
    assignment: RoleAssignment, session: Session
) -> Optional[RoleStipend]:
    """Compute the stipend based on role, session, and adjustment factor"""
    role_def = get_role_definition(assignment.role_code)
    tier_id = role_def.stipend_tier_id
    if tier_id is None:
        return None
    tier = StipendTierCode.get_base_amount(tier_id)
    factor = _session_adjustment_factor(session)
    adjusted = tier
    if factor != 1.0:
        adjusted = ap_scale(tier, factor, source=STIPEND_AMOUNT_ADJUSTMENT)
    return RoleStipend(
        role_code=assignment.role_code,
        session_id=assignment.session_id,
        amount=adjusted,
        reason=f"Tier {tier_id} base ${tier.value:,} adjusted by factor {factor}",
    )


def raw_role_stipends_for_member(member: Member, session: Session) -> list[RoleStipend]:
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


def _subset_total_value(subset: tuple[RoleStipend, ...]) -> int:
    """Provenance-enabled summation helper"""
    return sum(r.amount.value for r in subset)


def _subset_key(subset: tuple[RoleStipend, ...]) -> tuple[int, tuple[str, ...]]:
    """Generate sorted tuple of stipends and codes"""
    total = _subset_total_value(subset)
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
            total_amount=rs.amount.value,
        )
    best_subset: tuple[RoleStipend, ...] = tuple()
    best_amount = 0
    all_rs_only = [rs for (rs, _is_chair) in candidates]
    chamber_rules = get_chamber_rules(member.chamber)
    max_chairs = chamber_rules.max_chairs
    max_positions = chamber_rules.max_positions
    for k in range(1, max_positions + 1):
        for combo in combinations(all_rs_only, k):
            chair_count = sum(1 for rs in combo if _is_committee_chair(rs.role_code))
            if chair_count > max_chairs:
                continue
            total = _subset_total_value(combo)
            if total > best_amount:
                best_amount = total
                best_subset = combo
            elif total == best_amount and best_subset:
                if _subset_key(combo) < _subset_key(best_subset):
                    best_subset = combo
    if not best_subset and raw:
        best_subset = (max(raw, key=lambda r: r.amount.value),)
        best_amount = _subset_total_value(best_subset)
    paid_roles_sorted = sorted(
        best_subset, key=lambda r: (-r.amount.value, r.role_code)
    )
    sources_for_decision = (
        [chamber_rules.source_ref] if len(candidates) > 1 else []
    )
    paid_set = {r.role_code for r in paid_roles_sorted}
    provenance: list[RoleSelectionProvenance] = []
    chair_cap_applied = len(
        [rs for (rs, is_chair) in candidates if is_chair]
    ) > 1
    for rs, is_chair in candidates:
        if rs.role_code in paid_set:
            reason = "SELECTED_MAX_VALUE"
            notes = {
                "amount": rs.amount.value,
                "is_chair": is_chair,
                "max_positions": max_positions,
            }
        else:
            if is_chair and chair_cap_applied:
                reason = "DISCARDED_CHAIR_CAP"
            elif len(paid_roles_sorted) >= max_positions:
                reason = "DISCARDED_POSITION_CAP"
            else:
                reason = "DISCARDED_LOWER_VALUE"
            notes = {
                "amount": rs.amount.value,
                "is_chair": is_chair,
                "max_positions": max_positions,
            }
        provenance.append(RoleSelectionProvenance(
            role_code=rs.role_code,
            selected=rs.role_code in paid_set,
            reason=reason,
            notes=notes,
            sources=frozenset(sources_for_decision),
        ))
    return PaidRoleSelection(
        session_id=session.id,
        member_id=member.member_id,
        paid_roles=paid_roles_sorted,
        total_amount=sum(r.amount.value for r in paid_roles_sorted),
        provenance=provenance,
    )


def stipend_9b_for_member(member: Member, session: Session) -> int:
    """Public helper to return total 9B stipend for a member"""
    selection = select_paid_roles_for_member(member, session)
    return selection.total_amount
