"""Defines the roles"""

from __future__ import annotations

from models.core import (
    Chamber,
    RoleDomain,
    CommitteeRoleType,
    RoleDefinition,
    RoleCode,
    StipendTierCode,
)

# Role definitions per 9B
SPEAKER = RoleDefinition(
    code=RoleCode.SPEAKER,
    title="Speaker of the House",
    domain=RoleDomain.LEADERSHIP,
    chamber=Chamber.HOUSE,
    committee_code=None,
    committee_role_type=None,
    stipend_tier_id=StipendTierCode.TIER_80K,
)
SENATE_PRESIDENT = RoleDefinition(
    code=RoleCode.SENATE_PRESIDENT,
    title="President of the Senate",
    domain=RoleDomain.LEADERSHIP,
    chamber=Chamber.SENATE,
    committee_code=None,
    committee_role_type=None,
    stipend_tier_id=StipendTierCode.TIER_80K,
)

HOUSE_WM_CHAIR = RoleDefinition(
    code=RoleCode.HOUSE_WM_CHAIR,
    title="House Chair, Committee on Ways and Means",
    domain=RoleDomain.COMMITTEE,
    chamber=Chamber.HOUSE,
    committee_code="WAYS_MEANS_HOUSE",
    committee_role_type=CommitteeRoleType.CHAIR,
    stipend_tier_id=StipendTierCode.TIER_65K,
)
SENATE_WM_CHAIR = RoleDefinition(
    code=RoleCode.SENATE_WM_CHAIR,
    title="Senate Chair, Committee on Ways and Means",
    domain=RoleDomain.COMMITTEE,
    chamber=Chamber.SENATE,
    committee_code="WAYS_MEANS_SENATE",
    committee_role_type=CommitteeRoleType.CHAIR,
    stipend_tier_id=StipendTierCode.TIER_65K,
)

HOUSE_MAJORITY_LEADER = RoleDefinition(
    code=RoleCode.HOUSE_MAJORITY_LEADER,
    title="House Majority Floor Leader",
    domain=RoleDomain.LEADERSHIP,
    chamber=Chamber.HOUSE,
    committee_code=None,
    committee_role_type=None,
    stipend_tier_id=StipendTierCode.TIER_60K,
)
HOUSE_MINORITY_LEADER = RoleDefinition(
    code=RoleCode.HOUSE_MINORITY_LEADER,
    title="House Minority Floor Leader",
    domain=RoleDomain.LEADERSHIP,
    chamber=Chamber.HOUSE,
    committee_code=None,
    committee_role_type=None,
    stipend_tier_id=StipendTierCode.TIER_60K,
)
SENATE_MAJORITY_LEADER = RoleDefinition(
    code=RoleCode.SENATE_MAJORITY_LEADER,
    title="Senate Majority Floor Leader",
    domain=RoleDomain.LEADERSHIP,
    chamber=Chamber.SENATE,
    committee_code=None,
    committee_role_type=None,
    stipend_tier_id=StipendTierCode.TIER_60K,
)
SENATE_MINORITY_LEADER = RoleDefinition(
    code=RoleCode.SENATE_MINORITY_LEADER,
    title="Senate Minority Floor Leader",
    domain=RoleDomain.LEADERSHIP,
    chamber=Chamber.SENATE,
    committee_code=None,
    committee_role_type=None,
    stipend_tier_id=StipendTierCode.TIER_60K,
)

HOUSE_SPEAKER_PRO_TEM = RoleDefinition(
    code=RoleCode.HOUSE_SPEAKER_PRO_TEM,
    title="Speaker Pro Tempore of the House",
    domain=RoleDomain.LEADERSHIP,
    chamber=Chamber.HOUSE,
    committee_code=None,
    committee_role_type=None,
    stipend_tier_id=StipendTierCode.TIER_50K,
)
SENATE_SPEAKER_PRO_TEM = RoleDefinition(
    code=RoleCode.SENATE_SPEAKER_PRO_TEM,
    title="President Pro Tempore of the Senate",
    domain=RoleDomain.LEADERSHIP,
    chamber=Chamber.SENATE,
    committee_code=None,
    committee_role_type=None,
    stipend_tier_id=StipendTierCode.TIER_50K,
)


HOUSE_ASSISTANT_MAJORITY_LEADER = RoleDefinition(
    code=RoleCode.HOUSE_ASSISTANT_MAJORITY_LEADER,
    title="House Assistant Majority Floor Leader",
    domain=RoleDomain.LEADERSHIP,
    chamber=Chamber.HOUSE,
    committee_code=None,
    committee_role_type=None,
    stipend_tier_id=StipendTierCode.TIER_35K,
)
HOUSE_ASSISTANT_MINORITY_LEADER = RoleDefinition(
    code=RoleCode.HOUSE_ASSISTANT_MINORITY_LEADER,
    title="House Assistant Minority Floor Leader",
    domain=RoleDomain.LEADERSHIP,
    chamber=Chamber.HOUSE,
    committee_code=None,
    committee_role_type=None,
    stipend_tier_id=StipendTierCode.TIER_35K,
)

# Missing second assitant, senate, etc. -- circle back here

HOUSE_RULES_CHAIR = RoleDefinition(
    code=RoleCode.HOUSE_RULES_CHAIR,
    title="House Chair, House Committee on Rules",
    domain=RoleDomain.COMMITTEE,
    chamber=Chamber.HOUSE,
    committee_code="RULES_HOUSE",
    committee_role_type=CommitteeRoleType.CHAIR,
    stipend_tier_id=StipendTierCode.TIER_30K,
)
SENATE_RULES_CHAIR = RoleDefinition(
    code=RoleCode.SENATE_RULES_CHAIR,
    title="Senate Chair, Senate Committee on Rules",
    domain=RoleDomain.COMMITTEE,
    chamber=Chamber.SENATE,
    committee_code="RULES_SENATE",
    committee_role_type=CommitteeRoleType.CHAIR,
    stipend_tier_id=StipendTierCode.TIER_30K,
)

HOUSE_EDUCATION_CHAIR = RoleDefinition(
    code=RoleCode.HOUSE_EDUCATION_CHAIR,
    title="House Chair, Joint Committee on Education",
    domain=RoleDomain.COMMITTEE,
    chamber=Chamber.HOUSE,
    committee_code="EDUCATION_JOINT",
    committee_role_type=CommitteeRoleType.CHAIR,
    stipend_tier_id=StipendTierCode.TIER_30K,
)
SENATE_EDUCATION_CHAIR = RoleDefinition(
    code=RoleCode.SENATE_EDUCATION_CHAIR,
    title="Senate Chair, Joint Committee on Education",
    domain=RoleDomain.COMMITTEE,
    chamber=Chamber.SENATE,
    committee_code="EDUCATION_JOINT",
    committee_role_type=CommitteeRoleType.CHAIR,
    stipend_tier_id=StipendTierCode.TIER_30K,
)

HOUSE_JUDICIARY_CHAIR = RoleDefinition(
    code=RoleCode.HOUSE_JUDICIARY_CHAIR,
    title="House Chair, Joint Committee on Judiciary",
    domain=RoleDomain.COMMITTEE,
    chamber=Chamber.HOUSE,
    committee_code="JUDICIARY_JOINT",
    committee_role_type=CommitteeRoleType.CHAIR,
    stipend_tier_id=StipendTierCode.TIER_30K,
)
SENATE_JUDICIARY_CHAIR = RoleDefinition(
    code=RoleCode.SENATE_JUDICIARY_CHAIR,
    title="Senate Chair, Joint Committee on Judiciary",
    domain=RoleDomain.COMMITTEE,
    chamber=Chamber.SENATE,
    committee_code="JUDICIARY_JOINT",
    committee_role_type=CommitteeRoleType.CHAIR,
    stipend_tier_id=StipendTierCode.TIER_30K,
)


# Keep extending


_ROLE_DEFS: list[RoleDefinition] = [
    SPEAKER,
    SENATE_PRESIDENT,
    HOUSE_WM_CHAIR,
    SENATE_WM_CHAIR,
    HOUSE_MAJORITY_LEADER,
    HOUSE_MINORITY_LEADER,
    SENATE_MAJORITY_LEADER,
    SENATE_MINORITY_LEADER,
    HOUSE_SPEAKER_PRO_TEM,
    SENATE_SPEAKER_PRO_TEM,
    HOUSE_ASSISTANT_MAJORITY_LEADER,
    HOUSE_ASSISTANT_MINORITY_LEADER,
    HOUSE_RULES_CHAIR,
    SENATE_RULES_CHAIR,
    HOUSE_EDUCATION_CHAIR,
    SENATE_EDUCATION_CHAIR,
    HOUSE_JUDICIARY_CHAIR,
    SENATE_JUDICIARY_CHAIR,
]
"""Registry of all role definitions"""
ROLE_DEFINITIONS: dict[RoleCode, RoleDefinition] = {
    role.code: role for role in _ROLE_DEFS
}
"""Mapping of role codes to RoleDefinition objects"""

def get_role_definition(code: RoleCode) -> RoleDefinition:
    """Input a role code and returns the corresponding RoleDefinition"""
    return ROLE_DEFINITIONS[code]
