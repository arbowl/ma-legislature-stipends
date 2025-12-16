"""Loads session data"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional

from models.core import (
    Session,
    Member,
    RoleAssignment,
    Chamber,
    Party,
)


@dataclass(frozen=True)
class LoadedSession:
    """Session from JSON"""

    session: Session
    members: dict[str, Member]
    role_assignments: list[RoleAssignment]


def _parse_chamber(value: str) -> Chamber:
    """Gets chamber from string"""
    match value.lower():
        case "house":
            return Chamber.HOUSE
        case "senate":
            return Chamber.SENATE
        case "joint":
            return Chamber.JOINT
        case _:
            raise ValueError(f"Unknown chamber value: {value}")


def _parse_party(value: Optional[str]) -> Party:
    """Gets party from string"""
    if value is None:
        value = "other"
    match value.lower():
        case "d":
            return Party.DEMOCRAT
        case "r":
            return Party.REPUBLICAN
        case "other" | "o":
            return Party.OTHER
        case _:
            raise ValueError(f"Unknown party value: {value}")


def _parse_session_years(session_id: str) -> tuple[int, int]:
    parts = session_id.split("-")
    if len(parts) != 2:
        raise ValueError(f"Cannot parse session years from {session_id!r}")
    return int(parts[0]), int(parts[1])


def load_session(root: Path, session_id: str) -> LoadedSession:
    """Loads session data from JSON"""
    session_dir = root / session_id
    with (session_dir / "members.json").open() as f:
        mdata: dict[str, Any] = json.load(f)
    if mdata["session_id"] != session_id:
        raise ValueError(
            f"members.json session_id mismatch (expected {session_id}, got "
            f"{mdata['session_id']})"
        )
    members: dict[str, Member] = {}
    row: dict[str, str]
    for row in mdata["members"]:
        member = Member(
            member_id=row["member_id"],
            name=row["name"],
            chamber=_parse_chamber(row["chamber"]),
            party=_parse_party(row.get("party", "UNKNOWN")),
            distance_miles_from_state_house=row.get("distance_miles_from_state_house"),
        )
        members[member.member_id] = member
    with (session_dir / "roles.json").open() as f:
        rdata: dict[str, Any] = json.load(f)
    if rdata["session_id"] != session_id:
        raise ValueError(
            f"roles.json session_id mismatch (expected {session_id}, got "
            f"{rdata['session_id']})"
        )
    role_assignments: list[RoleAssignment] = []
    for row in rdata["roles"]:
        ra = RoleAssignment(
            member_id=row["member_id"],
            role_code=row["role_code"],
            session_id=session_id,
        )
        role_assignments.append(ra)
    for ra in role_assignments:
        member = members.get(ra.member_id)
        if member is None:
            raise ValueError(f"RoleAssignment for unknown member_id {ra.member_id}")
        member.roles.append(ra)
    start_year, end_year = _parse_session_years(session_id)
    session = Session(
        id=session_id,
        start_year=start_year,
        end_year=end_year,
        label=f"{start_year}-{end_year}",
    )
    return LoadedSession(
        session=session,
        members=members,
        role_assignments=role_assignments,
    )
