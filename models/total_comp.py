"""Generates comp after applying rules"""

from __future__ import annotations

from dataclasses import dataclass

from models.core import Member, Session
from models.rules_9b import stipend_9b_for_member
from models.rules_9c import travel_9c_for_member, TravelAllowance
from config.base_salary import base_salary_for_session


@dataclass(frozen=True)
class Component:
    """Salary component"""

    label: str
    amount: int


@dataclass(frozen=True)
class TotalCompResult:
    """Total compensation after stipends"""

    member_id: str
    session_id: str
    components: list[Component]
    total: int


def total_comp_for_member(member: Member, session: Session) -> TotalCompResult:
    """Generates total compensation for a member in a session"""
    base = base_salary_for_session(session)
    stipends_9b = stipend_9b_for_member(member, session)
    travel_9c = travel_9c_for_member(member, session)
    comps = [
        Component(label="Base salary (Article CXVIII)", amount=base.amount),
        Component(label="Section 9B stipends", amount=stipends_9b),
        Component(
            label="Section 9C for travel/expenses", amount=travel_9c.amount
        )
    ]
    total_amount = sum(c.amount for c in comps)
    return TotalCompResult(
        member_id=member.member_id,
        session_id=session.id,
        components=comps,
        total=total_amount,
    )
