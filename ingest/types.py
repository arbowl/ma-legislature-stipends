"""Ingestion models"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Literal, Optional


ChamberStr = Literal["house", "senate"]


@dataclass
class RawMember:
    """Unprocessed data for a single member"""

    member_id: str
    name: str
    chamber: ChamberStr
    raw_district: str
    party: Optional[str]
    profile_url: str


@dataclass
class RawLeadershipRole:
    """Unprocessed leadership information"""

    member_id: str
    chamber: ChamberStr
    raw_title: str
    raw_district_party: str


def to_dict_list(items: list[object]) -> list[dict]:
    """Turns a dataclass into a dict"""
    return [asdict(i) for i in items]
