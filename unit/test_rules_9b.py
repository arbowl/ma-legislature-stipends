""""""

from models.core import (
    Member,
    Chamber,
    Party,
    RoleAssignment,
    Session,
    RoleCode
)
from models.rules_9b import (
    raw_role_stipends_for_member,
    stipend_9b_for_member,
    select_paid_roles_for_member
)
from config.role_catalog import (
    SPEAKER,
    HOUSE_EDUCATION_CHAIR,
    HOUSE_JUDICIARY_CHAIR,
    HOUSE_ASSISTANT_MAJORITY_LEADER,
)


def _mk_session() -> Session:
    return Session(
        id=Session.from_id_number(194),
        start_year=2025,
        end_year=2026,
        label=Session.from_id_number(194)
    )


def test_speaker_stipend_basic():
    session = _mk_session()
    member = Member(
        member_id="H001",
        name="Test Speaker",
        chamber=Chamber.HOUSE,
        party=Party.DEMOCRAT,
    )
    member.roles.append(
        RoleAssignment(
            member_id=member.member_id,
            role_code=RoleCode.SPEAKER,
            session_id=Session.from_id_number(194),
        )
    )
    stipends = raw_role_stipends_for_member(member, session)
    assert len(stipends) == 1
    s = stipends[0]
    assert s.role_code == RoleCode.SPEAKER
    assert s.amount == 80_000


def test_speaker_plus_chair_gets_both():
    session = _mk_session()
    member = Member(
        member_id="H001",
        name="Test Speaker",
        chamber=Chamber.HOUSE,
        party=Party.DEMOCRAT,
    )
    speaker = RoleAssignment(
        member_id=member.member_id,
        role_code=SPEAKER.code,
        session_id=session.id,
    )
    chair = RoleAssignment(
        member_id=member.member_id,
        role_code=HOUSE_EDUCATION_CHAIR.code,
        session_id=session.id,
    )
    member.roles.extend([speaker, chair])
    total = stipend_9b_for_member(member, session)
    assert total == 80_000 + 30_000


def test_two_chairs_and_one_leadership():
    session = _mk_session()
    member = Member(
        member_id="H001",
        name="Multi-Role Member",
        chamber=Chamber.HOUSE,
        party=Party.DEMOCRAT,
    )
    chair1 = RoleAssignment(
        member_id=member.member_id,
        role_code=HOUSE_EDUCATION_CHAIR.code,
        session_id=session.id,
    )
    chair2 = RoleAssignment(
        member_id=member.member_id,
        role_code=HOUSE_JUDICIARY_CHAIR.code,
        session_id=session.id,
    )
    leadership = RoleAssignment(
        member_id=member.member_id,
        role_code=HOUSE_ASSISTANT_MAJORITY_LEADER.code,
        session_id=session.id,
    )
    member.roles.extend([chair1, chair2, leadership])
    selection = select_paid_roles_for_member(member, session)
    paid_codes = {r.role_code for r in selection.paid_roles}
    assert len(paid_codes) == 2
    assert HOUSE_ASSISTANT_MAJORITY_LEADER.code in paid_codes
    assert {
        HOUSE_ASSISTANT_MAJORITY_LEADER.code,
        HOUSE_JUDICIARY_CHAIR.code
    } & paid_codes
