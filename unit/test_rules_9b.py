from models.core import (
    Member,
    Chamber,
    Party,
    RoleAssignment,
)
from models.rules_9b import (
    raw_role_stipends_for_member,
    stipend_9b_for_member,
    select_paid_roles_for_member,
)
from config.role_catalog import ROLE_DEFINITIONS
from unit.utils import mk_session
from audit.sources_registry import HOUSE_RULES_18, SENATE_RULES_11E

SPEAKER = ROLE_DEFINITIONS["SPEAKER"]
HOUSE_EDUCATION_CHAIR = ROLE_DEFINITIONS["HOUSE_EDUCATION_CHAIR"]
HOUSE_JUDICIARY_CHAIR = ROLE_DEFINITIONS["HOUSE_JUDICIARY_CHAIR"]
HOUSE_ASSISTANT_MAJORITY_LEADER = ROLE_DEFINITIONS[
    "HOUSE_MAJORITY_ASSISTANT_FLOOR_LEADER"
]


def test_speaker_stipend_basic():
    session = mk_session()
    member = Member(
        member_id="H001",
        name="Test Speaker",
        chamber=Chamber.HOUSE,
        party=Party.DEMOCRAT,
    )
    member.roles.append(
        RoleAssignment(
            member_id=member.member_id,
            role_code=SPEAKER.code,
            session_id=session.id,
        )
    )
    stipends = raw_role_stipends_for_member(member, session)
    assert len(stipends) == 1
    s = stipends[0]
    assert s.role_code == "SPEAKER"
    assert s.amount.value == 80_000


def test_speaker_plus_chair_gets_one():
    session = mk_session()
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
    assert total == 80_000


def test_two_chairs_and_one_leadership():
    session = mk_session()
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
    assert len(paid_codes) == 1
    assert HOUSE_ASSISTANT_MAJORITY_LEADER.code in paid_codes
    assert {HOUSE_ASSISTANT_MAJORITY_LEADER.code} & paid_codes


def test_house_provenance_includes_house_rules():
    """Test that House member provenance includes HOUSE_RULES_18"""
    session = mk_session()
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
    member.roles.extend([chair1, chair2])
    selection = select_paid_roles_for_member(member, session)
    # Check that provenance exists
    assert len(selection.provenance) == 2
    # Check that at least one provenance entry has HOUSE_RULES_18
    all_sources = set()
    for prov in selection.provenance:
        all_sources.update(prov.sources)
    assert HOUSE_RULES_18 in all_sources
