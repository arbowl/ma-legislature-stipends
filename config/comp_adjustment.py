"""Manually derived and computed 9B comp adjustment"""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path

from audit.sources_registry import (
    TRAVEL_AMOUNT_ADJUSTMENT, STIPEND_AMOUNT_ADJUSTMENT
)
from audit.provenance import SourceRef
from models.core import Session


@dataclass(frozen=True)
class AdjustedStipend:
    """Biennial 9B adjustments"""

    session_id: str
    factor: float
    source: SourceRef
    note: str


@dataclass(frozen=True)
class AdjustedBaseSalary:
    """Base salary plus adjustment"""

    session_id: str
    factor: float
    source: SourceRef
    note: str


@dataclass(frozen=True)
class AdjustedTravel:
    """Base travel plus adjustment"""

    session_id: str
    factor: float
    source: SourceRef
    note: str


def load_stipend_adjustment(session_id: str) -> AdjustedStipend:
    path = Path("data/sessions") / session_id / "adjustment.json"
    data: dict = json.loads(path.read_text())
    return AdjustedStipend(
        session_id=session_id,
        factor=float(data["aggregate_change_factor"]),
        source=STIPEND_AMOUNT_ADJUSTMENT,
        note=data.get("note", ""),
    )


def load_travel_adjustment(session_id: str) -> AdjustedTravel:
    path = Path("data/sessions") / session_id / "adjustment.json"
    data: dict = json.loads(path.read_text())
    return AdjustedTravel(
        session_id=session_id,
        factor=float(data["aggregate_change_factor"]),
        source=TRAVEL_AMOUNT_ADJUSTMENT,
        note=data.get("note", ""),
    )
