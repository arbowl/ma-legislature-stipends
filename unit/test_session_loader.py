from pathlib import Path
import json

from data.session_loader import load_session
from models.core import Chamber


def test_load_session_basic(tmp_path: Path):
    session_id = "2025-2026"
    session_dir = tmp_path / session_id
    session_dir.mkdir()
    members_payload = {
        "session_id": session_id,
        "members": [
            {
                "member_id": "H001",
                "name": "Test Speaker",
                "chamber": "House",
                "party": "D",
                "distance_miles_from_state_house": 10.0,
            }
        ],
    }
    roles_payload = {
        "session_id": session_id,
        "roles": [
            {"member_id": "H001", "role_code": "SPEAKER"},
        ],
    }
    (session_dir / "members.json").write_text(json.dumps(members_payload))
    (session_dir / "roles.json").write_text(json.dumps(roles_payload))
    loaded = load_session(tmp_path, session_id)
    assert loaded.session.id == session_id
    assert loaded.members["H001"].chamber == Chamber.HOUSE
    assert loaded.members["H001"].roles[0].role_code == "SPEAKER"
