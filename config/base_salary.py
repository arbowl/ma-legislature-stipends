"""Base salary stub"""

from __future__ import annotations

from dataclasses import dataclass

from models.core import Session


@dataclass(frozen=True)
class BaseSalary:
    """Base salary before stipends"""

    session_id: str
    amount: int
    note: str = ""


def base_salary_for_session(session: Session) -> BaseSalary:
    """TODO: Fix placeholder"""
    return BaseSalary(
        session_id=session.id,
        amount=75_000,
        note="Base salary",
    )
