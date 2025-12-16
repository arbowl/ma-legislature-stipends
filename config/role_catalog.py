"""Role catalog for the Legislature"""

from __future__ import annotations

from enum import Enum

from models.core import (
    Chamber,
    RoleDomain,
    CommitteeRoleType,
    RoleDefinition,
    StipendTierCode,
)


class _RoleKey(str, Enum):
    """Keys for the role dictionary"""

    CODE = "code"
    TITLE = "title"
    DOMAIN = "domain"
    CHAMBER = "chamber"
    COMMITTEE_CODE = "committee_code"
    COMMITTEE_ROLE_TYPE = "committee_role_type"
    TIER_ID = "tier_id"


Spec = dict[_RoleKey, dict]

ROLE_SPECS: list[Spec] = []

# 9B(a): President & Speaker - 80,000

ROLE_SPECS += [
    Spec(
        code="SENATE_PRESIDENT",
        title="President of the Senate",
        domain=RoleDomain.LEADERSHIP,
        chamber=Chamber.SENATE,
        tier_id=StipendTierCode.TIER_80K,
    ),
    Spec(
        code="SPEAKER",
        title="Speaker of the House",
        domain=RoleDomain.LEADERSHIP,
        chamber=Chamber.HOUSE,
        tier_id=StipendTierCode.TIER_80K,
    ),
]

# 9B(b): Ways & Means chairs - 65,000

ROLE_SPECS += [
    Spec(
        code="HOUSE_WAYS_MEANS_CHAIR",
        title="House Chair, Committee on Ways and Means",
        domain=RoleDomain.COMMITTEE,
        chamber=Chamber.HOUSE,
        committee_code="HOUSE_WAYS_AND_MEANS",
        committee_role_type=CommitteeRoleType.CHAIR,
        tier_id=StipendTierCode.TIER_65K,
    ),
    Spec(
        code="SENATE_WAYS_MEANS_CHAIR",
        title="Senate Chair, Committee on Ways and Means",
        domain=RoleDomain.COMMITTEE,
        chamber=Chamber.SENATE,
        committee_code="SENATE_WAYS_AND_MEANS",
        committee_role_type=CommitteeRoleType.CHAIR,
        tier_id=StipendTierCode.TIER_65K,
    ),
]

# 9B(b): Floor leaders of each major party - 60,000

ROLE_SPECS += [
    Spec(
        code="HOUSE_MAJORITY_FLOOR_LEADER",
        title="House Majority Floor Leader",
        domain=RoleDomain.LEADERSHIP,
        chamber=Chamber.HOUSE,
        tier_id=StipendTierCode.TIER_60K,
    ),
    Spec(
        code="HOUSE_MINORITY_FLOOR_LEADER",
        title="House Minority Floor Leader",
        domain=RoleDomain.LEADERSHIP,
        chamber=Chamber.HOUSE,
        tier_id=StipendTierCode.TIER_60K,
    ),
    Spec(
        code="SENATE_MAJORITY_FLOOR_LEADER",
        title="Senate Majority Floor Leader",
        domain=RoleDomain.LEADERSHIP,
        chamber=Chamber.SENATE,
        tier_id=StipendTierCode.TIER_60K,
    ),
    Spec(
        code="SENATE_MINORITY_FLOOR_LEADER",
        title="Senate Minority Floor Leader",
        domain=RoleDomain.LEADERSHIP,
        chamber=Chamber.SENATE,
        tier_id=StipendTierCode.TIER_60K,
    ),
]

# 9B(b): Presidents Pro Tempore & Speakers Pro Tempore - 50,000

ROLE_SPECS += [
    Spec(
        code="SENATE_PRESIDENT_PRO_TEMPORE",
        title="President Pro Tempore of the Senate",
        domain=RoleDomain.LEADERSHIP,
        chamber=Chamber.SENATE,
        tier_id=StipendTierCode.TIER_50K,
    ),
    Spec(
        code="HOUSE_SPEAKER_PRO_TEMPORE",
        title="Speaker Pro Tempore of the House",
        domain=RoleDomain.LEADERSHIP,
        chamber=Chamber.HOUSE,
        tier_id=StipendTierCode.TIER_50K,
    ),
]

# 9B(c): Assistant / Second / Third Assistant floor leaders - 35,000

for chamber, chamber_label in [
    (Chamber.HOUSE, "House"),
    (Chamber.SENATE, "Senate"),
]:
    for side_code, side_label in [
        ("MAJORITY", "Majority"),
        ("MINORITY", "Minority"),
    ]:
        ROLE_SPECS += [
            Spec(
                code=f"{chamber_label.upper()}_{side_code}_ASSISTANT_FLOOR_LEADER",
                title=f"{chamber_label} Assistant {side_label} Floor Leader",
                domain=RoleDomain.LEADERSHIP,
                chamber=chamber,
                tier_id=StipendTierCode.TIER_35K,
            ),
            Spec(
                code=f"{chamber_label.upper()}_{side_code}_SECOND_ASSISTANT_FLOOR_LEADER",
                title=f"{chamber_label} Second Assistant {side_label} Floor Leader",
                domain=RoleDomain.LEADERSHIP,
                chamber=chamber,
                tier_id=StipendTierCode.TIER_35K,
            ),
            Spec(
                code=f"{chamber_label.upper()}_{side_code}_THIRD_ASSISTANT_FLOOR_LEADER",
                title=f"{chamber_label} Third Assistant {side_label} Floor Leader",
                domain=RoleDomain.LEADERSHIP,
                chamber=chamber,
                tier_id=StipendTierCode.TIER_35K,
            ),
        ]

# 9B(d): House division chairs - 30,000

ROLE_SPECS += [
    Spec(
        code="HOUSE_DIVISION_CHAIR_1",
        title="Chair, First Division of the House of Representatives",
        domain=RoleDomain.LEADERSHIP,
        chamber=Chamber.HOUSE,
        tier_id=StipendTierCode.TIER_30K,
    ),
    Spec(
        code="HOUSE_DIVISION_CHAIR_2",
        title="Chair, Second Division of the House of Representatives",
        domain=RoleDomain.LEADERSHIP,
        chamber=Chamber.HOUSE,
        tier_id=StipendTierCode.TIER_30K,
    ),
    Spec(
        code="HOUSE_DIVISION_CHAIR_3",
        title="Chair, Third Division of the House of Representatives",
        domain=RoleDomain.LEADERSHIP,
        chamber=Chamber.HOUSE,
        tier_id=StipendTierCode.TIER_30K,
    ),
    Spec(
        code="HOUSE_DIVISION_CHAIR_4",
        title="Chair, Fourth Division of the House of Representatives",
        domain=RoleDomain.LEADERSHIP,
        chamber=Chamber.HOUSE,
        tier_id=StipendTierCode.TIER_30K,
    ),
]

# 9B(d): Rules chairs - 30,000

ROLE_SPECS += [
    Spec(
        code="SENATE_RULES_CHAIR",
        title="Chair, Senate Committee on Rules",
        domain=RoleDomain.COMMITTEE,
        chamber=Chamber.SENATE,
        committee_code="SENATE_RULES",
        committee_role_type=CommitteeRoleType.CHAIR,
        tier_id=StipendTierCode.TIER_30K,
    ),
    Spec(
        code="HOUSE_RULES_CHAIR",
        title="Chair, House Committee on Rules",
        domain=RoleDomain.COMMITTEE,
        chamber=Chamber.HOUSE,
        committee_code="HOUSE_RULES",
        committee_role_type=CommitteeRoleType.CHAIR,
        tier_id=StipendTierCode.TIER_30K,
    ),
]

# 9B(d): Bonding, Capital Expenditures & State Assets - 30,000

ROLE_SPECS += [
    Spec(
        code="SENATE_BONDING_CAPITAL_CHAIR",
        title="Chair, Senate Committee on Bonding, Capital Expenditures and State Assets",
        domain=RoleDomain.COMMITTEE,
        chamber=Chamber.SENATE,
        committee_code="JOINT_BONDING_CAPITAL_EXPENDITURES_AND_STATE_ASSETS",
        committee_role_type=CommitteeRoleType.CHAIR,
        tier_id=StipendTierCode.TIER_30K,
    ),
    Spec(
        code="HOUSE_BONDING_CAPITAL_CHAIR",
        title="House Chair, Joint Committee on Bonding, Capital Expenditures and State Assets",
        domain=RoleDomain.COMMITTEE,
        chamber=Chamber.HOUSE,
        committee_code="JOINT_BONDING_CAPITAL_EXPENDITURES_AND_STATE_ASSETS",
        committee_role_type=CommitteeRoleType.CHAIR,
        tier_id=StipendTierCode.TIER_30K,
    ),
]

# 9B(d): Ways & Means vice chairs and ranking minority members - 30,000

ROLE_SPECS += [
    Spec(
        code="SENATE_WAYS_MEANS_VICE_CHAIR",
        title="Vice Chair, Senate Committee on Ways and Means",
        domain=RoleDomain.COMMITTEE,
        chamber=Chamber.SENATE,
        committee_code="SENATE_WAYS_AND_MEANS",
        committee_role_type=CommitteeRoleType.VICE_CHAIR,
        tier_id=StipendTierCode.TIER_30K,
    ),
    Spec(
        code="HOUSE_WAYS_MEANS_VICE_CHAIR",
        title="Vice Chair, House Committee on Ways and Means",
        domain=RoleDomain.COMMITTEE,
        chamber=Chamber.HOUSE,
        committee_code="HOUSE_WAYS_AND_MEANS",
        committee_role_type=CommitteeRoleType.VICE_CHAIR,
        tier_id=StipendTierCode.TIER_30K,
    ),
    Spec(
        code="SENATE_WAYS_MEANS_RM",
        title="Ranking Minority Member, Senate Committee on Ways and Means",
        domain=RoleDomain.COMMITTEE,
        chamber=Chamber.SENATE,
        committee_code="SENATE_WAYS_AND_MEANS",
        committee_role_type=CommitteeRoleType.RANKING_MINORITY,
        tier_id=StipendTierCode.TIER_30K,
    ),
    Spec(
        code="HOUSE_WAYS_MEANS_RM",
        title="Ranking Minority Member, House Committee on Ways and Means",
        domain=RoleDomain.COMMITTEE,
        chamber=Chamber.HOUSE,
        committee_code="HOUSE_WAYS_AND_MEANS",
        committee_role_type=CommitteeRoleType.RANKING_MINORITY,
        tier_id=StipendTierCode.TIER_30K,
    ),
]

# 9B(d): Post Audit and Oversight chairs - 30,000

ROLE_SPECS += [
    Spec(
        code="SENATE_POST_AUDIT_CHAIR",
        title="Chair, Senate Committee on Post Audit and Oversight",
        domain=RoleDomain.COMMITTEE,
        chamber=Chamber.SENATE,
        committee_code="SENATE_POST_AUDIT_AND_OVERSIGHT",
        committee_role_type=CommitteeRoleType.CHAIR,
        tier_id=StipendTierCode.TIER_30K,
    ),
    Spec(
        code="HOUSE_POST_AUDIT_CHAIR",
        title="Chair, House Committee on Post Audit and Oversight",
        domain=RoleDomain.COMMITTEE,
        chamber=Chamber.HOUSE,
        committee_code="HOUSE_POST_AUDIT_AND_OVERSIGHT",
        committee_role_type=CommitteeRoleType.CHAIR,
        tier_id=StipendTierCode.TIER_30K,
    ),
]

# 9B(d): Bills in the Third Reading chairs - 30,000

ROLE_SPECS += [
    Spec(
        code="SENATE_BILLS_THIRD_READING_CHAIR",
        title="Chair, Senate Committee on Bills in the Third Reading",
        domain=RoleDomain.COMMITTEE,
        chamber=Chamber.SENATE,
        committee_code="SENATE_BILLS_IN_THE_THIRD_READING",
        committee_role_type=CommitteeRoleType.CHAIR,
        tier_id=StipendTierCode.TIER_30K,
    ),
    Spec(
        code="HOUSE_BILLS_THIRD_READING_CHAIR",
        title="Chair, House Committee on Bills in the Third Reading",
        domain=RoleDomain.COMMITTEE,
        chamber=Chamber.HOUSE,
        committee_code="HOUSE_BILLS_IN_THE_THIRD_READING",
        committee_role_type=CommitteeRoleType.CHAIR,
        tier_id=StipendTierCode.TIER_30K,
    ),
]

# 9B(d): Steering and Policy chairs - 30,000

ROLE_SPECS += [
    Spec(
        code="SENATE_STEERING_POLICY_CHAIR",
        title="Chair, Senate Committee on Steering and Policy",
        domain=RoleDomain.COMMITTEE,
        chamber=Chamber.SENATE,
        committee_code="SENATE_STEERING_AND_POLICY",
        committee_role_type=CommitteeRoleType.CHAIR,
        tier_id=StipendTierCode.TIER_30K,
    ),
    Spec(
        code="HOUSE_STEERING_POLICY_SCHEDULING_CHAIR",
        title="Chair, House Committee on Steering, Policy and Scheduling",
        domain=RoleDomain.COMMITTEE,
        chamber=Chamber.HOUSE,
        committee_code="HOUSE_STEERING_POLICY_AND_SCHEDULING",
        committee_role_type=CommitteeRoleType.CHAIR,
        tier_id=StipendTierCode.TIER_30K,
    ),
]

# 9B(d): Joint statutory chairs - 30,000

ROLE_SPECS += [
    Spec(
        code="SENATE_STATE_ADMIN_CHAIR",
        title="Senate Chair, Joint Committee on State Administration and Regulatory Oversight",
        domain=RoleDomain.COMMITTEE,
        chamber=Chamber.SENATE,
        committee_code="JOINT_STATE_ADMINISTRATION_AND_REGULATORY_OVERSIGHT",
        committee_role_type=CommitteeRoleType.CHAIR,
        tier_id=StipendTierCode.TIER_30K,
    ),
    Spec(
        code="HOUSE_STATE_ADMIN_CHAIR",
        title="House Chair, Joint Committee on State Administration and Regulatory Oversight",
        domain=RoleDomain.COMMITTEE,
        chamber=Chamber.HOUSE,
        committee_code="JOINT_STATE_ADMINISTRATION_AND_REGULATORY_OVERSIGHT",
        committee_role_type=CommitteeRoleType.CHAIR,
        tier_id=StipendTierCode.TIER_30K,
    ),
    Spec(
        code="SENATE_HEALTH_CARE_FINANCING_CHAIR",
        title="Senate Chair, Joint Committee on Health Care Financing",
        domain=RoleDomain.COMMITTEE,
        chamber=Chamber.SENATE,
        committee_code="JOINT_HEALTH_CARE_FINANCING",
        committee_role_type=CommitteeRoleType.CHAIR,
        tier_id=StipendTierCode.TIER_30K,
    ),
    Spec(
        code="HOUSE_HEALTH_CARE_FINANCING_CHAIR",
        title="House Chair, Joint Committee on Health Care Financing",
        domain=RoleDomain.COMMITTEE,
        chamber=Chamber.HOUSE,
        committee_code="JOINT_HEALTH_CARE_FINANCING",
        committee_role_type=CommitteeRoleType.CHAIR,
        tier_id=StipendTierCode.TIER_30K,
    ),
    Spec(
        code="SENATE_FINANCIAL_SERVICES_CHAIR",
        title="Senate Chair, Joint Committee on Financial Services",
        domain=RoleDomain.COMMITTEE,
        chamber=Chamber.SENATE,
        committee_code="JOINT_FINANCIAL_SERVICES",
        committee_role_type=CommitteeRoleType.CHAIR,
        tier_id=StipendTierCode.TIER_30K,
    ),
    Spec(
        code="HOUSE_FINANCIAL_SERVICES_CHAIR",
        title="House Chair, Joint Committee on Financial Services",
        domain=RoleDomain.COMMITTEE,
        chamber=Chamber.HOUSE,
        committee_code="JOINT_FINANCIAL_SERVICES",
        committee_role_type=CommitteeRoleType.CHAIR,
        tier_id=StipendTierCode.TIER_30K,
    ),
    Spec(
        code="SENATE_REVENUE_CHAIR",
        title="Senate Chair, Joint Committee on Revenue",
        domain=RoleDomain.COMMITTEE,
        chamber=Chamber.SENATE,
        committee_code="JOINT_REVENUE",
        committee_role_type=CommitteeRoleType.CHAIR,
        tier_id=StipendTierCode.TIER_30K,
    ),
    Spec(
        code="HOUSE_REVENUE_CHAIR",
        title="House Chair, Joint Committee on Revenue",
        domain=RoleDomain.COMMITTEE,
        chamber=Chamber.HOUSE,
        committee_code="JOINT_REVENUE",
        committee_role_type=CommitteeRoleType.CHAIR,
        tier_id=StipendTierCode.TIER_30K,
    ),
    Spec(
        code="SENATE_ECON_DEV_EMERG_TECH_CHAIR",
        title="Senate Chair, Joint Committee on Economic Development and Emerging Technologies",
        domain=RoleDomain.COMMITTEE,
        chamber=Chamber.SENATE,
        committee_code="JOINT_ECONOMIC_DEVELOPMENT_AND_EMERGING_TECHNOLOGIES",
        committee_role_type=CommitteeRoleType.CHAIR,
        tier_id=StipendTierCode.TIER_30K,
    ),
    Spec(
        code="HOUSE_ECON_DEV_EMERG_TECH_CHAIR",
        title="House Chair, Joint Committee on Economic Development and Emerging Technologies",
        domain=RoleDomain.COMMITTEE,
        chamber=Chamber.HOUSE,
        committee_code="JOINT_ECONOMIC_DEVELOPMENT_AND_EMERGING_TECHNOLOGIES",
        committee_role_type=CommitteeRoleType.CHAIR,
        tier_id=StipendTierCode.TIER_30K,
    ),
    Spec(
        code="SENATE_JUDICIARY_CHAIR",
        title="Senate Chair, Joint Committee on the Judiciary",
        domain=RoleDomain.COMMITTEE,
        chamber=Chamber.SENATE,
        committee_code="JOINT_THE_JUDICIARY",
        committee_role_type=CommitteeRoleType.CHAIR,
        tier_id=StipendTierCode.TIER_30K,
    ),
    Spec(
        code="HOUSE_JUDICIARY_CHAIR",
        title="House Chair, Joint Committee on the Judiciary",
        domain=RoleDomain.COMMITTEE,
        chamber=Chamber.HOUSE,
        committee_code="JOINT_THE_JUDICIARY",
        committee_role_type=CommitteeRoleType.CHAIR,
        tier_id=StipendTierCode.TIER_30K,
    ),
    Spec(
        code="SENATE_EDUCATION_CHAIR",
        title="Senate Chair, Joint Committee on Education",
        domain=RoleDomain.COMMITTEE,
        chamber=Chamber.SENATE,
        committee_code="JOINT_EDUCATION",
        committee_role_type=CommitteeRoleType.CHAIR,
        tier_id=StipendTierCode.TIER_30K,
    ),
    Spec(
        code="HOUSE_EDUCATION_CHAIR",
        title="House Chair, Joint Committee on Education",
        domain=RoleDomain.COMMITTEE,
        chamber=Chamber.HOUSE,
        committee_code="JOINT_EDUCATION",
        committee_role_type=CommitteeRoleType.CHAIR,
        tier_id=StipendTierCode.TIER_30K,
    ),
    Spec(
        code="SENATE_TELECOM_UTILITIES_ENERGY_CHAIR",
        title="Senate Chair, Joint Committee on Telecommunications, Utilities and Energy",
        domain=RoleDomain.COMMITTEE,
        chamber=Chamber.SENATE,
        committee_code="JOINT_TELECOMMUNICATIONS_UTILITIES_AND_ENERGY",
        committee_role_type=CommitteeRoleType.CHAIR,
        tier_id=StipendTierCode.TIER_30K,
    ),
    Spec(
        code="HOUSE_TELECOM_UTILITIES_ENERGY_CHAIR",
        title="House Chair, Joint Committee on Telecommunications, Utilities and Energy",
        domain=RoleDomain.COMMITTEE,
        chamber=Chamber.HOUSE,
        committee_code="JOINT_TELECOMMUNICATIONS_UTILITIES_AND_ENERGY",
        committee_role_type=CommitteeRoleType.CHAIR,
        tier_id=StipendTierCode.TIER_30K,
    ),
    Spec(
        code="SENATE_TRANSPORTATION_CHAIR",
        title="Senate Chair, Joint Committee on Transportation",
        domain=RoleDomain.COMMITTEE,
        chamber=Chamber.SENATE,
        committee_code="JOINT_TRANSPORTATION",
        committee_role_type=CommitteeRoleType.CHAIR,
        tier_id=StipendTierCode.TIER_30K,
    ),
    Spec(
        code="HOUSE_TRANSPORTATION_CHAIR",
        title="House Chair, Joint Committee on Transportation",
        domain=RoleDomain.COMMITTEE,
        chamber=Chamber.HOUSE,
        committee_code="JOINT_TRANSPORTATION",
        committee_role_type=CommitteeRoleType.CHAIR,
        tier_id=StipendTierCode.TIER_30K,
    ),
]

# 9B(e): other committee chairs / vice chairs / ranking minority members - 15,000
# All remaining statutory special roles (not captured above) default to 15k.
# We still separate them as roles in case the statute changes tiers later.

ROLE_SPECS += [
    Spec(
        code="HOUSE_RULES_VICE_CHAIR",
        title="Vice Chair, House Committee on Rules",
        domain=RoleDomain.COMMITTEE,
        chamber=Chamber.HOUSE,
        committee_code="HOUSE_RULES",
        committee_role_type=CommitteeRoleType.VICE_CHAIR,
        tier_id=StipendTierCode.TIER_15K,
    ),
    Spec(
        code="HOUSE_RULES_RM",
        title="Ranking Minority Member, House Committee on Rules",
        domain=RoleDomain.COMMITTEE,
        chamber=Chamber.HOUSE,
        committee_code="HOUSE_RULES",
        committee_role_type=CommitteeRoleType.RANKING_MINORITY,
        tier_id=StipendTierCode.TIER_15K,
    ),
    Spec(
        code="HOUSE_POST_AUDIT_VICE_CHAIR",
        title="Vice Chair, House Committee on Post Audit and Oversight",
        domain=RoleDomain.COMMITTEE,
        chamber=Chamber.HOUSE,
        committee_code="HOUSE_POST_AUDIT_AND_OVERSIGHT",
        committee_role_type=CommitteeRoleType.VICE_CHAIR,
        tier_id=StipendTierCode.TIER_15K,
    ),
    Spec(
        code="SENATE_WAYS_MEANS_ASSISTANT_VICE_CHAIR",
        title="Assistant Vice Chair, Senate Committee on Ways and Means",
        domain=RoleDomain.COMMITTEE,
        chamber=Chamber.SENATE,
        committee_code="SENATE_WAYS_AND_MEANS",
        committee_role_type=CommitteeRoleType.ASSISTANT_VICE_CHAIR,
        tier_id=StipendTierCode.TIER_15K,
    ),
    Spec(
        code="HOUSE_WAYS_MEANS_ASSISTANT_VICE_CHAIR",
        title="Assistant Vice Chair, House Committee on Ways and Means",
        domain=RoleDomain.COMMITTEE,
        chamber=Chamber.HOUSE,
        committee_code="HOUSE_WAYS_AND_MEANS",
        committee_role_type=CommitteeRoleType.ASSISTANT_VICE_CHAIR,
        tier_id=StipendTierCode.TIER_15K,
    ),
    Spec(
        code="HOUSE_WAYS_MEANS_ASSISTANT_RM",
        title="Assistant Ranking Minority Member, House Committee on Ways and Means",
        domain=RoleDomain.COMMITTEE,
        chamber=Chamber.HOUSE,
        committee_code="HOUSE_WAYS_AND_MEANS",
        committee_role_type=CommitteeRoleType.ASSISTANT_RANKING_MINORITY,
        tier_id=StipendTierCode.TIER_15K,
    ),
    Spec(
        code="HOUSE_FINANCIAL_SERVICES_VICE_CHAIR",
        title="Vice Chair, House Committee on Financial Services",
        domain=RoleDomain.COMMITTEE,
        chamber=Chamber.HOUSE,
        committee_code="JOINT_FINANCIAL_SERVICES",
        committee_role_type=CommitteeRoleType.VICE_CHAIR,
        tier_id=StipendTierCode.TIER_15K,
    ),
    Spec(
        code="HOUSE_FINANCIAL_SERVICES_RM",
        title="Ranking Minority Member, House Committee on Financial Services",
        domain=RoleDomain.COMMITTEE,
        chamber=Chamber.HOUSE,
        committee_code="JOINT_FINANCIAL_SERVICES",
        committee_role_type=CommitteeRoleType.RANKING_MINORITY,
        tier_id=StipendTierCode.TIER_15K,
    ),
    Spec(
        code="HOUSE_HEALTH_CARE_FINANCING_VICE_CHAIR",
        title="Vice Chair, House Committee on Health Care Financing",
        domain=RoleDomain.COMMITTEE,
        chamber=Chamber.HOUSE,
        committee_code="JOINT_HEALTH_CARE_FINANCING",
        committee_role_type=CommitteeRoleType.VICE_CHAIR,
        tier_id=StipendTierCode.TIER_15K,
    ),
    Spec(
        code="HOUSE_BONDING_CAPITAL_VICE_CHAIR",
        title="Vice Chair, House Committee on Bonding, Capital Expenditures and State Assets",
        domain=RoleDomain.COMMITTEE,
        chamber=Chamber.HOUSE,
        committee_code="JOINT_BONDING_CAPITAL_EXPENDITURES_AND_STATE_ASSETS",
        committee_role_type=CommitteeRoleType.VICE_CHAIR,
        tier_id=StipendTierCode.TIER_15K,
    ),
    Spec(
        code="HOUSE_BONDING_CAPITAL_RM",
        title=(
            "Ranking Minority Member, House Committee on Bonding, "
            "Capital Expenditures and State Assets"
        ),
        domain=RoleDomain.COMMITTEE,
        chamber=Chamber.HOUSE,
        committee_code="JOINT_BONDING_CAPITAL_EXPENDITURES_AND_STATE_ASSETS",
        committee_role_type=CommitteeRoleType.RANKING_MINORITY,
        tier_id=StipendTierCode.TIER_15K,
    ),
    Spec(
        code="HOUSE_STATE_ADMIN_VICE_CHAIR",
        title="Vice Chair, House Committee on State Administration and Regulatory Oversight",
        domain=RoleDomain.COMMITTEE,
        chamber=Chamber.HOUSE,
        committee_code="JOINT_STATE_ADMINISTRATION_AND_REGULATORY_OVERSIGHT",
        committee_role_type=CommitteeRoleType.VICE_CHAIR,
        tier_id=StipendTierCode.TIER_15K,
    ),
    Spec(
        code="HOUSE_ECON_DEV_EMERG_TECH_VICE_CHAIR",
        title="Vice Chair, House Committee on Economic Development and Emerging Technologies",
        domain=RoleDomain.COMMITTEE,
        chamber=Chamber.HOUSE,
        committee_code="JOINT_ECONOMIC_DEVELOPMENT_AND_EMERGING_TECHNOLOGIES",
        committee_role_type=CommitteeRoleType.VICE_CHAIR,
        tier_id=StipendTierCode.TIER_15K,
    ),
    Spec(
        code="HOUSE_ECON_DEV_EMERG_TECH_RM",
        title=(
            "Ranking Minority Member, House Committee on Economic Development "
            "and Emerging Technologies"
        ),
        domain=RoleDomain.COMMITTEE,
        chamber=Chamber.HOUSE,
        committee_code="JOINT_ECONOMIC_DEVELOPMENT_AND_EMERGING_TECHNOLOGIES",
        committee_role_type=CommitteeRoleType.RANKING_MINORITY,
        tier_id=StipendTierCode.TIER_15K,
    ),
    Spec(
        code="HOUSE_REVENUE_VICE_CHAIR",
        title="Vice Chair, House Committee on Revenue",
        domain=RoleDomain.COMMITTEE,
        chamber=Chamber.HOUSE,
        committee_code="JOINT_REVENUE",
        committee_role_type=CommitteeRoleType.VICE_CHAIR,
        tier_id=StipendTierCode.TIER_15K,
    ),
    Spec(
        code="SENATE_HEALTH_CARE_FINANCING_RM",
        title="Ranking Minority Member, Senate Committee on Health Care Financing",
        domain=RoleDomain.COMMITTEE,
        chamber=Chamber.SENATE,
        committee_code="JOINT_HEALTH_CARE_FINANCING",
        committee_role_type=CommitteeRoleType.RANKING_MINORITY,
        tier_id=StipendTierCode.TIER_15K,
    ),
    Spec(
        code="HOUSE_HEALTH_CARE_FINANCING_RM",
        title="Ranking Minority Member, House Committee on Health Care Financing",
        domain=RoleDomain.COMMITTEE,
        chamber=Chamber.HOUSE,
        committee_code="JOINT_HEALTH_CARE_FINANCING",
        committee_role_type=CommitteeRoleType.RANKING_MINORITY,
        tier_id=StipendTierCode.TIER_15K,
    ),
    Spec(
        code="HOUSE_JUDICIARY_VICE_CHAIR",
        title="Vice Chair, House Committee on the Judiciary",
        domain=RoleDomain.COMMITTEE,
        chamber=Chamber.HOUSE,
        committee_code="JOINT_THE_JUDICIARY",
        committee_role_type=CommitteeRoleType.VICE_CHAIR,
        tier_id=StipendTierCode.TIER_15K,
    ),
    Spec(
        code="HOUSE_JUDICIARY_RM",
        title="Ranking Minority Member, House Committee on the Judiciary",
        domain=RoleDomain.COMMITTEE,
        chamber=Chamber.HOUSE,
        committee_code="JOINT_THE_JUDICIARY",
        committee_role_type=CommitteeRoleType.RANKING_MINORITY,
        tier_id=StipendTierCode.TIER_15K,
    ),
    Spec(
        code="HOUSE_TRANSPORTATION_VICE_CHAIR",
        title="Vice Chair, House Committee on Transportation",
        domain=RoleDomain.COMMITTEE,
        chamber=Chamber.HOUSE,
        committee_code="JOINT_TRANSPORTATION",
        committee_role_type=CommitteeRoleType.VICE_CHAIR,
        tier_id=StipendTierCode.TIER_15K,
    ),
    Spec(
        code="HOUSE_BILLS_THIRD_READING_VICE_CHAIR",
        title="Vice Chair, House Committee on Bills in the Third Reading",
        domain=RoleDomain.COMMITTEE,
        chamber=Chamber.HOUSE,
        committee_code="HOUSE_BILLS_IN_THE_THIRD_READING",
        committee_role_type=CommitteeRoleType.VICE_CHAIR,
        tier_id=StipendTierCode.TIER_15K,
    ),
    Spec(
        code="HOUSE_STEERING_POLICY_SCHEDULING_VICE_CHAIR",
        title="Vice Chair, House Committee on Steering, Policy and Scheduling",
        domain=RoleDomain.COMMITTEE,
        chamber=Chamber.HOUSE,
        committee_code="HOUSE_STEERING_POLICY_AND_SCHEDULING",
        committee_role_type=CommitteeRoleType.VICE_CHAIR,
        tier_id=StipendTierCode.TIER_15K,
    ),
    Spec(
        code="HOUSE_EDUCATION_VICE_CHAIR",
        title="Vice Chair, House Committee on Education",
        domain=RoleDomain.COMMITTEE,
        chamber=Chamber.HOUSE,
        committee_code="JOINT_EDUCATION",
        committee_role_type=CommitteeRoleType.VICE_CHAIR,
        tier_id=StipendTierCode.TIER_15K,
    ),
    Spec(
        code="HOUSE_TELECOM_UTILITIES_ENERGY_VICE_CHAIR",
        title="Vice Chair, House Committee on Telecommunications, Utilities and Energy",
        domain=RoleDomain.COMMITTEE,
        chamber=Chamber.HOUSE,
        committee_code="JOINT_TELECOMMUNICATIONS_UTILITIES_AND_ENERGY",
        committee_role_type=CommitteeRoleType.VICE_CHAIR,
        tier_id=StipendTierCode.TIER_15K,
    ),
]

# 9B(f) generics for "all other" committees

ROLE_SPECS += [
    Spec(
        code="GENERIC_OTHER_COMMITTEE_CHAIR",
        title="Chair, other committee",
        domain=RoleDomain.COMMITTEE,
        chamber=None,
        committee_code=None,
        committee_role_type=CommitteeRoleType.CHAIR,
        tier_id=StipendTierCode.TIER_15K,
    ),
    Spec(
        code="GENERIC_OTHER_COMMITTEE_VICE_CHAIR",
        title="Vice Chair, other committee",
        domain=RoleDomain.COMMITTEE,
        chamber=None,
        committee_code=None,
        committee_role_type=CommitteeRoleType.VICE_CHAIR,
        tier_id=StipendTierCode.TIER_5200,
    ),
]

ROLE_DEFINITIONS: dict[str, RoleDefinition] = {
    spec[_RoleKey.CODE]: RoleDefinition(
        code=spec[_RoleKey.CODE],
        title=spec[_RoleKey.TITLE],
        domain=spec[_RoleKey.DOMAIN],
        chamber=spec[_RoleKey.CHAMBER],
        committee_code=spec.get(_RoleKey.COMMITTEE_CODE),
        committee_role_type=spec.get(_RoleKey.COMMITTEE_ROLE_TYPE),
        stipend_tier_id=spec.get(_RoleKey.TIER_ID),
    )
    for spec in ROLE_SPECS
}


def get_role_definition(code: str) -> RoleDefinition:
    """Helper function to get defs from codes"""
    return ROLE_DEFINITIONS[code]
