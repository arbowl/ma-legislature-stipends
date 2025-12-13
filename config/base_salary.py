"""Base salary stub"""

from __future__ import annotations

from dataclasses import dataclass

from audit.provenance import AmountWithProvenance, ap_from
from audit.sources_registry import ARTICLE_CXVIII_BASE
from models.core import Session


@dataclass(frozen=True)
class BaseSalary:
    """Base salary before stipends"""

    session_id: str
    amount: AmountWithProvenance
    note: str = ""


def base_salary_for_session(session: Session) -> BaseSalary:
    """TODO: Fix placeholder"""
    amount = ap_from(75_000, ARTICLE_CXVIII_BASE)
    return BaseSalary(
        session_id=session.id,
        amount=amount,
        note="Base salary",
    )
