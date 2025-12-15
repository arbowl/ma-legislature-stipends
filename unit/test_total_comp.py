from models.core import (
    Member,
    Chamber,
    Party,
    RoleAssignment,
)
from config.role_catalog import ROLE_DEFINITIONS
from models.total_comp import total_comp_for_member
from unit.utils import mk_session

SPEAKER = ROLE_DEFINITIONS["SPEAKER"]


def test_total_comp_basic():
    session = mk_session()
    member = Member(
        member_id="H001",
        name="Test Speaker",
        chamber=Chamber.HOUSE,
        party=Party.DEMOCRAT,
        distance_miles_from_state_house=10.0,
    )
    member.roles.append(
        RoleAssignment(
            member_id=member.member_id,
            role_code=SPEAKER.code,
            session_id=session.id,
        )
    )
    res = total_comp_for_member(member, session)
    assert res.total == 75_000 + 80_000 + 15_000
    amounts = {c.label: c.amount.value for c in res.components}
    assert amounts["Base salary (Article CXVIII)"] == 75_000
    assert amounts["Section 9B stipends"] == 80_000
    assert amounts["Section 9C for travel/expenses"] == 15_000
