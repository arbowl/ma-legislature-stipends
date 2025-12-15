from pathlib import Path
import json

from config.role_catalog import ROLE_DEFINITIONS
from data.session_loader import LoadedSession, load_session
from models.core import (
    Member,
    Session,
    RoleAssignment,
    Chamber,
    Party,
)
from validators import validate_session_data

HOUSE_EDUCATION_CHAIR = ROLE_DEFINITIONS["HOUSE_EDUCATION_CHAIR"]
HOUSE_JUDICIARY_CHAIR = ROLE_DEFINITIONS["HOUSE_JUDICIARY_CHAIR"]


def test_validate_session_unknown_role(tmp_path: Path):
    session_id = "2025-2026"
    d = tmp_path / session_id
    d.mkdir()
    members_payload = {
        "session_id": session_id,
        "members": [
            {
                "member_id": "H001",
                "name": "Test Person",
                "chamber": "house",
                "party": "D",
            }
        ],
    }
    roles_payload = {
        "session_id": session_id,
        "roles": [
            {
                "member_id": "H001",
                "role_code": "NON_EXISTENT_ROLE"
            },
        ],
    }
    (d / "members.json").write_text(json.dumps(members_payload))
    (d / "roles.json").write_text(json.dumps(roles_payload))
    loaded = load_session(tmp_path, session_id)
    issues = validate_session_data(loaded)
    assert any(i.code == "UNKNOWN_ROLE_CODE" for i in issues)


def test_multiple_chair_warning():
    session = Session(id="2025_2026", start_year=2025, end_year=2026, label="")
    m = Member(
        member_id="H001",
        name="Chair Hoarder",
        chamber=Chamber.HOUSE,
        party=Party.DEMOCRAT,
    )
    m.roles.extend(
        [
            RoleAssignment(
                member_id=m.member_id,
                role_code=HOUSE_EDUCATION_CHAIR.code,
                session_id=session.id
            ),
            RoleAssignment(
                member_id=m.member_id,
                role_code=HOUSE_JUDICIARY_CHAIR.code,
                session_id=session.id
            ),
        ]
    )
    loaded = LoadedSession(
        session=session,
        members={m.member_id: m},
        role_assignments=m.roles[:],
    )
    issues = validate_session_data(loaded)
    assert any(i.code == "MULTIPLE_CHAIR_ROLES_RAW" for i in issues)
