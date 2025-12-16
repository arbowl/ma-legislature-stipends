"""Base salary stub"""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Optional

from audit.provenance import AmountWithProvenance, ap_from
from audit.sources_registry import (
    ARTICLE_CXVIII_BASE,
    BASE_SALARY_ADJUSTMENT,
)
from models.core import Session


@dataclass(frozen=True)
class BaseSalaryConfig:
    """Base salary before stipends"""

    session_id: str
    base_amount: AmountWithProvenance
    factor: Optional[float]
    note: str = ""


def load_base_salary_adjustment(session: Session) -> BaseSalaryConfig:
    """Load salary plus raises"""
    path = Path("data/sessions") / session.id / "base_salary.json"
    data: dict = json.loads(path.read_text())
    if data["session_id"] != session.id:
        raise ValueError(
            f"base_salary.jspn session_id mismatch: "
            f"{data['session_id']} != {session.id}"
        )
    base_amount = int(data["base_amount"])
    factor = data.get("aggregate_change_factor")
    factor_f = float(factor) if factor is not None else None
    note = data.get("note", "")
    return BaseSalaryConfig(
        session_id=session.id,
        base_amount=base_amount,
        factor=factor_f,
        note=note,
    )


def base_salary_for_session(session: Session) -> AmountWithProvenance:
    """Base salary plus adjustments for a session"""
    cfg = load_base_salary_adjustment(session)
    return ap_from(cfg.base_amount, ARTICLE_CXVIII_BASE, BASE_SALARY_ADJUSTMENT)
