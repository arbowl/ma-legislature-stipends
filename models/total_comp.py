"""Generates comp after applying rules"""

from __future__ import annotations

from dataclasses import dataclass

from audit.provenance import AmountWithProvenance, SourceRef, ap_sum
from models.core import Member, Session
from models.rules_9b import select_paid_roles_for_member
from models.rules_9c import travel_9c_for_member
from config.base_salary import base_salary_for_session


@dataclass(frozen=True)
class CompLabels:
    """Type of component"""

    base_salary: str = "Base salary (Article CXVIII)"
    stipends_9b: str = "Stipends (Section 9B)"
    travel_9c: str = "Travel (Section 9C)"


@dataclass(frozen=True)
class Component:
    """Salary component"""

    label: str
    amount: AmountWithProvenance


@dataclass(frozen=True)
class TotalCompResult:
    """Total compensation after stipends"""

    member_id: str
    session_id: str
    components: list[Component]
    total: AmountWithProvenance


def total_comp_for_member(member: Member, session: Session) -> TotalCompResult:
    """Generates total compensation for a member in a session"""
    base = base_salary_for_session(session)
    selection = select_paid_roles_for_member(member, session)
    stipends_9b = ap_sum(rs.amount for rs in selection.paid_roles)
    selection_sources: set[SourceRef] = set()
    for prov in selection.provenance:
        selection_sources.update(prov.sources)
    stipends_9b = AmountWithProvenance(
        value=stipends_9b.value,
        sources=stipends_9b.sources | frozenset(selection_sources),
    )
    travel_9c = travel_9c_for_member(member, session)
    comps = [
        Component(label=CompLabels.base_salary, amount=base),
        Component(label=CompLabels.stipends_9b, amount=stipends_9b),
        Component(label=CompLabels.travel_9c, amount=travel_9c.amount),
    ]
    total_amount = ap_sum(c.amount for c in comps)
    return TotalCompResult(
        member_id=member.member_id,
        session_id=session.id,
        components=comps,
        total=total_amount,
    )
