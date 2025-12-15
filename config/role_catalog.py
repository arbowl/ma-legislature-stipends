# ma_leg_comp/config/role_catalog.py

from __future__ import annotations

from typing import Optional

from models.core import (
    Chamber,
    RoleDomain,
    CommitteeRoleType,
    RoleDefinition,
)

# ---------------------------------------------------------------------------
# Tier IDs (strings only). These must match config/stipend_tiers.py
# ---------------------------------------------------------------------------

T80K = "T80K"
T65K = "T65K"
T60K = "T60K"
T50K = "T50K"
T35K = "T35K"
T30K = "T30K"
T15K = "T15K"
T5200 = "T5200"


Spec = dict  # simple alias for readability


ROLE_SPECS: list[Spec] = []

# ---------------------------------------------------------------------------
# 9B(a): Presiding officers – 80,000
# ---------------------------------------------------------------------------

ROLE_SPECS += [
    Spec(
        code="SPEAKER",
        title="Speaker of the House",
        domain=RoleDomain.LEADERSHIP,
        chamber=Chamber.HOUSE,
        committee_code=None,
        committee_role_type=None,
        tier_id=T80K,
    ),
    Spec(
        code="SENATE_PRESIDENT",
        title="President of the Senate",
        domain=RoleDomain.LEADERSHIP,
        chamber=Chamber.SENATE,
        committee_code=None,
        committee_role_type=None,
        tier_id=T80K,
    ),
]

# ---------------------------------------------------------------------------
# 9B(b): Ways & Means chairs – 65,000
# ---------------------------------------------------------------------------

ROLE_SPECS += [
    Spec(
        code="HOUSE_WAYS_MEANS_CHAIR",
        title="House Chair, Committee on Ways and Means",
        domain=RoleDomain.COMMITTEE,
        chamber=Chamber.HOUSE,
        committee_code="WAYS_MEANS_HOUSE",
        committee_role_type=CommitteeRoleType.CHAIR,
        tier_id=T65K,
    ),
    Spec(
        code="SENATE_WAYS_MEANS_CHAIR",
        title="Senate Chair, Committee on Ways and Means",
        domain=RoleDomain.COMMITTEE,
        chamber=Chamber.SENATE,
        committee_code="WAYS_MEANS_SENATE",
        committee_role_type=CommitteeRoleType.CHAIR,
        tier_id=T65K,
    ),
]

# ---------------------------------------------------------------------------
# 9B(b): Floor leaders of each major party – 60,000
# ---------------------------------------------------------------------------

ROLE_SPECS += [
    Spec(
        code="HOUSE_MAJORITY_FLOOR_LEADER",
        title="House Majority Floor Leader",
        domain=RoleDomain.LEADERSHIP,
        chamber=Chamber.HOUSE,
        committee_code=None,
        committee_role_type=None,
        tier_id=T60K,
    ),
    Spec(
        code="HOUSE_MINORITY_FLOOR_LEADER",
        title="House Minority Floor Leader",
        domain=RoleDomain.LEADERSHIP,
        chamber=Chamber.HOUSE,
        committee_code=None,
        committee_role_type=None,
        tier_id=T60K,
    ),
    Spec(
        code="SENATE_MAJORITY_FLOOR_LEADER",
        title="Senate Majority Floor Leader",
        domain=RoleDomain.LEADERSHIP,
        chamber=Chamber.SENATE,
        committee_code=None,
        committee_role_type=None,
        tier_id=T60K,
    ),
    Spec(
        code="SENATE_MINORITY_FLOOR_LEADER",
        title="Senate Minority Floor Leader",
        domain=RoleDomain.LEADERSHIP,
        chamber=Chamber.SENATE,
        committee_code=None,
        committee_role_type=None,
        tier_id=T60K,
    ),
]

# ---------------------------------------------------------------------------
# 9B(b): President / Speaker pro tempore – 50,000
# ---------------------------------------------------------------------------

ROLE_SPECS += [
    Spec(
        code="HOUSE_SPEAKER_PRO_TEM",
        title="Speaker Pro Tempore of the House",
        domain=RoleDomain.LEADERSHIP,
        chamber=Chamber.HOUSE,
        committee_code=None,
        committee_role_type=None,
        tier_id=T50K,
    ),
    Spec(
        code="SENATE_PRESIDENT_PRO_TEM",
        title="President Pro Tempore of the Senate",
        domain=RoleDomain.LEADERSHIP,
        chamber=Chamber.SENATE,
        committee_code=None,
        committee_role_type=None,
        tier_id=T50K,
    ),
]

# ---------------------------------------------------------------------------
# 9B(c): Assistant / Second / Third Assistant floor leaders – 35,000
# ---------------------------------------------------------------------------

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
                code=f"{chamber.name}_{side_code}_ASSISTANT_FLOOR_LEADER",
                title=f"{chamber_label} Assistant {side_label} Floor Leader",
                domain=RoleDomain.LEADERSHIP,
                chamber=chamber,
                committee_code=None,
                committee_role_type=None,
                tier_id=T35K,
            ),
            Spec(
                code=(
                    f"{chamber.name}_{side_code}_SECOND_ASSISTANT_"
                    "FLOOR_LEADER"
                ),
                title=(
                    f"{chamber_label} Second Assistant {side_label} "
                    "Floor Leader",
                ),
                domain=RoleDomain.LEADERSHIP,
                chamber=chamber,
                committee_code=None,
                committee_role_type=None,
                tier_id=T35K,
            ),
            Spec(
                code=(
                    f"{chamber.name}_{side_code}_THIRD_ASSISTANT_"
                    "FLOOR_LEADER"
                ),
                title=(
                    f"{chamber_label} Third Assistant {side_label} "
                    "Floor Leader"
                ),
                domain=RoleDomain.LEADERSHIP,
                chamber=chamber,
                committee_code=None,
                committee_role_type=None,
                tier_id=T35K,
            ),
        ]

# ---------------------------------------------------------------------------
# 9B(d): 30,000 group – specific chairs / vice / ranking
# ---------------------------------------------------------------------------

# Chairs of each of the 4 divisions of the House – 30,000 (leadership)
ROLE_SPECS += [
    Spec(
        code="HOUSE_DIVISION_1_CHAIR",
        title="Chair, First Division of the House",
        domain=RoleDomain.LEADERSHIP,
        chamber=Chamber.HOUSE,
        committee_code=None,
        committee_role_type=None,
        tier_id=T30K,
    ),
    Spec(
        code="HOUSE_DIVISION_2_CHAIR",
        title="Chair, Second Division of the House",
        domain=RoleDomain.LEADERSHIP,
        chamber=Chamber.HOUSE,
        committee_code=None,
        committee_role_type=None,
        tier_id=T30K,
    ),
    Spec(
        code="HOUSE_DIVISION_3_CHAIR",
        title="Chair, Third Division of the House",
        domain=RoleDomain.LEADERSHIP,
        chamber=Chamber.HOUSE,
        committee_code=None,
        committee_role_type=None,
        tier_id=T30K,
    ),
    Spec(
        code="HOUSE_DIVISION_4_CHAIR",
        title="Chair, Fourth Division of the House",
        domain=RoleDomain.LEADERSHIP,
        chamber=Chamber.HOUSE,
        committee_code=None,
        committee_role_type=None,
        tier_id=T30K,
    ),
]

# Rules committees – chairs – 30,000
ROLE_SPECS += [
    Spec(
        code="SENATE_RULES_CHAIR",
        title="Chair, Senate Committee on Rules",
        domain=RoleDomain.COMMITTEE,
        chamber=Chamber.SENATE,
        committee_code="RULES_SENATE",
        committee_role_type=CommitteeRoleType.CHAIR,
        tier_id=T30K,
    ),
    Spec(
        code="HOUSE_RULES_CHAIR",
        title="Chair, House Committee on Rules",
        domain=RoleDomain.COMMITTEE,
        chamber=Chamber.HOUSE,
        committee_code="RULES_HOUSE",
        committee_role_type=CommitteeRoleType.CHAIR,
        tier_id=T30K,
    ),
]

# Bonding, Capital Expenditures and State Assets – joint chairs – 30,000
ROLE_SPECS += [
    Spec(
        code="SENATE_BONDING_CAPITAL_CHAIR",
        title=(
            "Senate Chair, Joint Committee on Bonding, Capital Expenditures "
            "and State Assets"
        ),
        domain=RoleDomain.COMMITTEE,
        chamber=Chamber.SENATE,
        committee_code="BONDING_CAPITAL_JOINT",
        committee_role_type=CommitteeRoleType.CHAIR,
        tier_id=T30K,
    ),
    Spec(
        code="HOUSE_BONDING_CAPITAL_CHAIR",
        title=(
            "House Chair, Joint Committee on Bonding, Capital Expenditures "
            "and State Assets"
        ),
        domain=RoleDomain.COMMITTEE,
        chamber=Chamber.HOUSE,
        committee_code="BONDING_CAPITAL_JOINT",
        committee_role_type=CommitteeRoleType.CHAIR,
        tier_id=T30K,
    ),
]

# Ways and Means – vice chairs – 30,000
ROLE_SPECS += [
    Spec(
        code="SENATE_WAYS_MEANS_VICE_CHAIR",
        title="Vice Chair, Senate Committee on Ways and Means",
        domain=RoleDomain.COMMITTEE,
        chamber=Chamber.SENATE,
        committee_code="WAYS_MEANS_SENATE",
        committee_role_type=CommitteeRoleType.VICE_CHAIR,
        tier_id=T30K,
    ),
    Spec(
        code="HOUSE_WAYS_MEANS_VICE_CHAIR",
        title="Vice Chair, House Committee on Ways and Means",
        domain=RoleDomain.COMMITTEE,
        chamber=Chamber.HOUSE,
        committee_code="WAYS_MEANS_HOUSE",
        committee_role_type=CommitteeRoleType.VICE_CHAIR,
        tier_id=T30K,
    ),
]

# Ways and Means – ranking minority members – 30,000
ROLE_SPECS += [
    Spec(
        code="SENATE_WAYS_MEANS_RANKING_MINORITY",
        title="Ranking Minority Member, Senate Committee on Ways and Means",
        domain=RoleDomain.COMMITTEE,
        chamber=Chamber.SENATE,
        committee_code="WAYS_MEANS_SENATE",
        committee_role_type=CommitteeRoleType.RANKING_MINORITY,
        tier_id=T30K,
    ),
    Spec(
        code="HOUSE_WAYS_MEANS_RANKING_MINORITY",
        title="Ranking Minority Member, House Committee on Ways and Means",
        domain=RoleDomain.COMMITTEE,
        chamber=Chamber.HOUSE,
        committee_code="WAYS_MEANS_HOUSE",
        committee_role_type=CommitteeRoleType.RANKING_MINORITY,
        tier_id=T30K,
    ),
]

# Post Audit and Oversight – chairs – 30,000
ROLE_SPECS += [
    Spec(
        code="SENATE_POST_AUDIT_CHAIR",
        title="Chair, Senate Committee on Post Audit and Oversight",
        domain=RoleDomain.COMMITTEE,
        chamber=Chamber.SENATE,
        committee_code="POST_AUDIT_SENATE",
        committee_role_type=CommitteeRoleType.CHAIR,
        tier_id=T30K,
    ),
    Spec(
        code="HOUSE_POST_AUDIT_CHAIR",
        title="Chair, House Committee on Post Audit and Oversight",
        domain=RoleDomain.COMMITTEE,
        chamber=Chamber.HOUSE,
        committee_code="POST_AUDIT_HOUSE",
        committee_role_type=CommitteeRoleType.CHAIR,
        tier_id=T30K,
    ),
]

# Bills in the Third Reading – chairs – 30,000
ROLE_SPECS += [
    Spec(
        code="SENATE_BILLS_THIRD_READING_CHAIR",
        title="Chair, Senate Committee on Bills in the Third Reading",
        domain=RoleDomain.COMMITTEE,
        chamber=Chamber.SENATE,
        committee_code="BILLS_THIRD_READING_SENATE",
        committee_role_type=CommitteeRoleType.CHAIR,
        tier_id=T30K,
    ),
    Spec(
        code="HOUSE_BILLS_THIRD_READING_CHAIR",
        title="Chair, House Committee on Bills in the Third Reading",
        domain=RoleDomain.COMMITTEE,
        chamber=Chamber.HOUSE,
        committee_code="BILLS_THIRD_READING_HOUSE",
        committee_role_type=CommitteeRoleType.CHAIR,
        tier_id=T30K,
    ),
]

# Steering and Policy – chairs – 30,000
ROLE_SPECS += [
    Spec(
        code="SENATE_STEERING_POLICY_CHAIR",
        title="Chair, Senate Committee on Steering and Policy",
        domain=RoleDomain.COMMITTEE,
        chamber=Chamber.SENATE,
        committee_code="STEERING_POLICY_SENATE",
        committee_role_type=CommitteeRoleType.CHAIR,
        tier_id=T30K,
    ),
    Spec(
        code="HOUSE_STEERING_POLICY_SCHEDULING_CHAIR",
        title="Chair, House Committee on Steering, Policy and Scheduling",
        domain=RoleDomain.COMMITTEE,
        chamber=Chamber.HOUSE,
        committee_code="STEERING_POLICY_SCHEDULING_HOUSE",
        committee_role_type=CommitteeRoleType.CHAIR,
        tier_id=T30K,
    ),
]

# Joint committees – State Admin and Regulatory Oversight – chairs – 30,000
ROLE_SPECS += [
    Spec(
        code="SENATE_STATE_ADMIN_CHAIR",
        title=(
            "Senate Chair, Joint Committee on State Administration and "
            "Regulatory Oversight"
        ),
        domain=RoleDomain.COMMITTEE,
        chamber=Chamber.SENATE,
        committee_code="STATE_ADMIN_JOINT",
        committee_role_type=CommitteeRoleType.CHAIR,
        tier_id=T30K,
    ),
    Spec(
        code="HOUSE_STATE_ADMIN_CHAIR",
        title=(
            "House Chair, Joint Committee on State Administration and "
            "Regulatory Oversight"
        ),
        domain=RoleDomain.COMMITTEE,
        chamber=Chamber.HOUSE,
        committee_code="STATE_ADMIN_JOINT",
        committee_role_type=CommitteeRoleType.CHAIR,
        tier_id=T30K,
    ),
]

# Joint committees – Health Care Financing – chairs – 30,000
ROLE_SPECS += [
    Spec(
        code="SENATE_HEALTH_CARE_FINANCING_CHAIR",
        title="Senate Chair, Joint Committee on Health Care Financing",
        domain=RoleDomain.COMMITTEE,
        chamber=Chamber.SENATE,
        committee_code="HEALTH_CARE_FINANCING_JOINT",
        committee_role_type=CommitteeRoleType.CHAIR,
        tier_id=T30K,
    ),
    Spec(
        code="HOUSE_HEALTH_CARE_FINANCING_CHAIR",
        title="House Chair, Joint Committee on Health Care Financing",
        domain=RoleDomain.COMMITTEE,
        chamber=Chamber.HOUSE,
        committee_code="HEALTH_CARE_FINANCING_JOINT",
        committee_role_type=CommitteeRoleType.CHAIR,
        tier_id=T30K,
    ),
]

# Joint committees – Financial Services – chairs – 30,000
ROLE_SPECS += [
    Spec(
        code="SENATE_FIN_SERVICES_CHAIR",
        title="Senate Chair, Joint Committee on Financial Services",
        domain=RoleDomain.COMMITTEE,
        chamber=Chamber.SENATE,
        committee_code="FINANCIAL_SERVICES_JOINT",
        committee_role_type=CommitteeRoleType.CHAIR,
        tier_id=T30K,
    ),
    Spec(
        code="HOUSE_FIN_SERVICES_CHAIR",
        title="House Chair, Joint Committee on Financial Services",
        domain=RoleDomain.COMMITTEE,
        chamber=Chamber.HOUSE,
        committee_code="FINANCIAL_SERVICES_JOINT",
        committee_role_type=CommitteeRoleType.CHAIR,
        tier_id=T30K,
    ),
]

# Joint committees – Revenue – chairs – 30,000
ROLE_SPECS += [
    Spec(
        code="SENATE_REVENUE_CHAIR",
        title="Senate Chair, Joint Committee on Revenue",
        domain=RoleDomain.COMMITTEE,
        chamber=Chamber.SENATE,
        committee_code="REVENUE_JOINT",
        committee_role_type=CommitteeRoleType.CHAIR,
        tier_id=T30K,
    ),
    Spec(
        code="HOUSE_REVENUE_CHAIR",
        title="House Chair, Joint Committee on Revenue",
        domain=RoleDomain.COMMITTEE,
        chamber=Chamber.HOUSE,
        committee_code="REVENUE_JOINT",
        committee_role_type=CommitteeRoleType.CHAIR,
        tier_id=T30K,
    ),
]

# Joint committees – Economic Development and Emerging Technologies – chairs – 30,000
ROLE_SPECS += [
    Spec(
        code="SENATE_ECON_DEV_CHAIR",
        title=(
            "Senate Chair, Joint Committee on Economic Development and "
            "Emerging Technologies"
        ),
        domain=RoleDomain.COMMITTEE,
        chamber=Chamber.SENATE,
        committee_code="ECON_DEV_EMERGING_TECH_JOINT",
        committee_role_type=CommitteeRoleType.CHAIR,
        tier_id=T30K,
    ),
    Spec(
        code="HOUSE_ECON_DEV_CHAIR",
        title=(
            "House Chair, Joint Committee on Economic Development and "
            "Emerging Technologies"
        ),
        domain=RoleDomain.COMMITTEE,
        chamber=Chamber.HOUSE,
        committee_code="ECON_DEV_EMERGING_TECH_JOINT",
        committee_role_type=CommitteeRoleType.CHAIR,
        tier_id=T30K,
    ),
]

# Joint committees – Judiciary – chairs – 30,000
ROLE_SPECS += [
    Spec(
        code="SENATE_JUDICIARY_CHAIR",
        title="Senate Chair, Joint Committee on the Judiciary",
        domain=RoleDomain.COMMITTEE,
        chamber=Chamber.SENATE,
        committee_code="JUDICIARY_JOINT",
        committee_role_type=CommitteeRoleType.CHAIR,
        tier_id=T30K,
    ),
    Spec(
        code="HOUSE_JUDICIARY_CHAIR",
        title="House Chair, Joint Committee on the Judiciary",
        domain=RoleDomain.COMMITTEE,
        chamber=Chamber.HOUSE,
        committee_code="JUDICIARY_JOINT",
        committee_role_type=CommitteeRoleType.CHAIR,
        tier_id=T30K,
    ),
]

# Joint committees – Education – chairs – 30,000
ROLE_SPECS += [
    Spec(
        code="SENATE_EDUCATION_CHAIR",
        title="Senate Chair, Joint Committee on Education",
        domain=RoleDomain.COMMITTEE,
        chamber=Chamber.SENATE,
        committee_code="EDUCATION_JOINT",
        committee_role_type=CommitteeRoleType.CHAIR,
        tier_id=T30K,
    ),
    Spec(
        code="HOUSE_EDUCATION_CHAIR",
        title="House Chair, Joint Committee on Education",
        domain=RoleDomain.COMMITTEE,
        chamber=Chamber.HOUSE,
        committee_code="EDUCATION_JOINT",
        committee_role_type=CommitteeRoleType.CHAIR,
        tier_id=T30K,
    ),
]

# Joint committees – Telecommunications, Utilities and Energy – chairs – 30,000
ROLE_SPECS += [
    Spec(
        code="SENATE_TELECOM_UTILITIES_ENERGY_CHAIR",
        title=(
            "Senate Chair, Joint Committee on Telecommunications, "
            "Utilities and Energy"
        ),
        domain=RoleDomain.COMMITTEE,
        chamber=Chamber.SENATE,
        committee_code="TELECOM_UTILITIES_ENERGY_JOINT",
        committee_role_type=CommitteeRoleType.CHAIR,
        tier_id=T30K,
    ),
    Spec(
        code="HOUSE_TELECOM_UTILITIES_ENERGY_CHAIR",
        title=(
            "House Chair, Joint Committee on Telecommunications, "
            "Utilities and Energy"
        ),
        domain=RoleDomain.COMMITTEE,
        chamber=Chamber.HOUSE,
        committee_code="TELECOM_UTILITIES_ENERGY_JOINT",
        committee_role_type=CommitteeRoleType.CHAIR,
        tier_id=T30K,
    ),
]

# Joint committees – Transportation – chairs – 30,000
ROLE_SPECS += [
    Spec(
        code="SENATE_TRANSPORTATION_CHAIR",
        title="Senate Chair, Joint Committee on Transportation",
        domain=RoleDomain.COMMITTEE,
        chamber=Chamber.SENATE,
        committee_code="TRANSPORTATION_JOINT",
        committee_role_type=CommitteeRoleType.CHAIR,
        tier_id=T30K,
    ),
    Spec(
        code="HOUSE_TRANSPORTATION_CHAIR",
        title="House Chair, Joint Committee on Transportation",
        domain=RoleDomain.COMMITTEE,
        chamber=Chamber.HOUSE,
        committee_code="TRANSPORTATION_JOINT",
        committee_role_type=CommitteeRoleType.CHAIR,
        tier_id=T30K,
    ),
]

# ---------------------------------------------------------------------------
# 9B(e): 15,000 group – other committee chairs + named vice/ranking roles
# ---------------------------------------------------------------------------

# Generic: chairs of all other committees – 15,000
ROLE_SPECS += [
    Spec(
        code="GENERIC_OTHER_COMMITTEE_CHAIR",
        title="Chair, other committee (not listed in 9B(d))",
        domain=RoleDomain.COMMITTEE,
        chamber=None,
        committee_code=None,
        committee_role_type=CommitteeRoleType.CHAIR,
        tier_id=T15K,
    ),
]

# House Rules – vice chair & ranking minority – 15,000
ROLE_SPECS += [
    Spec(
        code="HOUSE_RULES_VICE_CHAIR",
        title="Vice Chair, House Committee on Rules",
        domain=RoleDomain.COMMITTEE,
        chamber=Chamber.HOUSE,
        committee_code="RULES_HOUSE",
        committee_role_type=CommitteeRoleType.VICE_CHAIR,
        tier_id=T15K,
    ),
    Spec(
        code="HOUSE_RULES_RANKING_MINORITY",
        title="Ranking Minority Member, House Committee on Rules",
        domain=RoleDomain.COMMITTEE,
        chamber=Chamber.HOUSE,
        committee_code="RULES_HOUSE",
        committee_role_type=CommitteeRoleType.RANKING_MINORITY,
        tier_id=T15K,
    ),
]

# House Post Audit and Oversight – vice chair – 15,000
ROLE_SPECS += [
    Spec(
        code="HOUSE_POST_AUDIT_VICE_CHAIR",
        title="Vice Chair, House Committee on Post Audit and Oversight",
        domain=RoleDomain.COMMITTEE,
        chamber=Chamber.HOUSE,
        committee_code="POST_AUDIT_HOUSE",
        committee_role_type=CommitteeRoleType.VICE_CHAIR,
        tier_id=T15K,
    ),
]

# Ways and Means – assistant vice chairs & assistant ranking minority – 15,000
ROLE_SPECS += [
    Spec(
        code="SENATE_WAYS_MEANS_ASSISTANT_VICE_CHAIR",
        title="Assistant Vice Chair, Senate Committee on Ways and Means",
        domain=RoleDomain.COMMITTEE,
        chamber=Chamber.SENATE,
        committee_code="WAYS_MEANS_SENATE",
        committee_role_type=CommitteeRoleType.ASSISTANT_VICE_CHAIR,
        tier_id=T15K,
    ),
    Spec(
        code="HOUSE_WAYS_MEANS_ASSISTANT_VICE_CHAIR",
        title="Assistant Vice Chair, House Committee on Ways and Means",
        domain=RoleDomain.COMMITTEE,
        chamber=Chamber.HOUSE,
        committee_code="WAYS_MEANS_HOUSE",
        committee_role_type=CommitteeRoleType.ASSISTANT_VICE_CHAIR,
        tier_id=T15K,
    ),
    Spec(
        code="HOUSE_WAYS_MEANS_ASSISTANT_RANKING_MINORITY",
        title=(
            "Assistant Ranking Minority Member, House Committee on "
            "Ways and Means"
        ),
        domain=RoleDomain.COMMITTEE,
        chamber=Chamber.HOUSE,
        committee_code="WAYS_MEANS_HOUSE",
        committee_role_type=CommitteeRoleType.ASSISTANT_RANKING_MINORITY,
        tier_id=T15K,
    ),
]

# Financial Services – House vice chair & ranking minority – 15,000
ROLE_SPECS += [
    Spec(
        code="HOUSE_FIN_SERVICES_VICE_CHAIR",
        title="House Vice Chair, Joint Committee on Financial Services",
        domain=RoleDomain.COMMITTEE,
        chamber=Chamber.HOUSE,
        committee_code="FINANCIAL_SERVICES_JOINT",
        committee_role_type=CommitteeRoleType.VICE_CHAIR,
        tier_id=T15K,
    ),
    Spec(
        code="HOUSE_FIN_SERVICES_RANKING_MINORITY",
        title="Ranking Minority Member, House Committee on Financial Services",
        domain=RoleDomain.COMMITTEE,
        chamber=Chamber.HOUSE,
        committee_code="FINANCIAL_SERVICES_JOINT",
        committee_role_type=CommitteeRoleType.RANKING_MINORITY,
        tier_id=T15K,
    ),
]

# HCF – House vice chair; Senate & House ranking minority – 15,000
ROLE_SPECS += [
    Spec(
        code="HOUSE_HEALTH_CARE_FINANCING_VICE_CHAIR",
        title="House Vice Chair, Joint Committee on Health Care Financing",
        domain=RoleDomain.COMMITTEE,
        chamber=Chamber.HOUSE,
        committee_code="HEALTH_CARE_FINANCING_JOINT",
        committee_role_type=CommitteeRoleType.VICE_CHAIR,
        tier_id=T15K,
    ),
    Spec(
        code="SENATE_HEALTH_CARE_FINANCING_RANKING_MINORITY",
        title=(
            "Ranking Minority Member, Senate, Joint Committee on "
            "Health Care Financing"
        ),
        domain=RoleDomain.COMMITTEE,
        chamber=Chamber.SENATE,
        committee_code="HEALTH_CARE_FINANCING_JOINT",
        committee_role_type=CommitteeRoleType.RANKING_MINORITY,
        tier_id=T15K,
    ),
    Spec(
        code="HOUSE_HEALTH_CARE_FINANCING_RANKING_MINORITY",
        title=(
            "Ranking Minority Member, House, Joint Committee on "
            "Health Care Financing"
        ),
        domain=RoleDomain.COMMITTEE,
        chamber=Chamber.HOUSE,
        committee_code="HEALTH_CARE_FINANCING_JOINT",
        committee_role_type=CommitteeRoleType.RANKING_MINORITY,
        tier_id=T15K,
    ),
]

# BCESA – House vice chair & ranking minority – 15,000
ROLE_SPECS += [
    Spec(
        code="HOUSE_BONDING_CAPITAL_VICE_CHAIR",
        title=(
            "House Vice Chair, Joint Committee on Bonding, "
            "Capital Expenditures and State Assets"
        ),
        domain=RoleDomain.COMMITTEE,
        chamber=Chamber.HOUSE,
        committee_code="BONDING_CAPITAL_JOINT",
        committee_role_type=CommitteeRoleType.VICE_CHAIR,
        tier_id=T15K,
    ),
    Spec(
        code="HOUSE_BONDING_CAPITAL_RANKING_MINORITY",
        title=(
            "House Ranking Minority Member, Joint Committee on Bonding, "
            "Capital Expenditures and State Assets"
        ),
        domain=RoleDomain.COMMITTEE,
        chamber=Chamber.HOUSE,
        committee_code="BONDING_CAPITAL_JOINT",
        committee_role_type=CommitteeRoleType.RANKING_MINORITY,
        tier_id=T15K,
    ),
]

# State Administration and Regulatory Oversight – House vice chair – 15,000
ROLE_SPECS += [
    Spec(
        code="HOUSE_STATE_ADMIN_VICE_CHAIR",
        title=(
            "House Vice Chair, Joint Committee on State Administration "
            "and Regulatory Oversight"
        ),
        domain=RoleDomain.COMMITTEE,
        chamber=Chamber.HOUSE,
        committee_code="STATE_ADMIN_JOINT",
        committee_role_type=CommitteeRoleType.VICE_CHAIR,
        tier_id=T15K,
    ),
]

# EDET – House vice chair & ranking minority – 15,000
ROLE_SPECS += [
    Spec(
        code="HOUSE_ECON_DEV_VICE_CHAIR",
        title=(
            "House Vice Chair, Joint Committee on Economic Development "
            "and Emerging Technologies"
        ),
        domain=RoleDomain.COMMITTEE,
        chamber=Chamber.HOUSE,
        committee_code="ECON_DEV_EMERGING_TECH_JOINT",
        committee_role_type=CommitteeRoleType.VICE_CHAIR,
        tier_id=T15K,
    ),
    Spec(
        code="HOUSE_ECON_DEV_RANKING_MINORITY",
        title=(
            "Ranking Minority Member, House, Joint Committee on "
            "Economic Development and Emerging Technologies"
        ),
        domain=RoleDomain.COMMITTEE,
        chamber=Chamber.HOUSE,
        committee_code="ECON_DEV_EMERGING_TECH_JOINT",
        committee_role_type=CommitteeRoleType.RANKING_MINORITY,
        tier_id=T15K,
    ),
]

# Revenue – House vice chair – 15,000
ROLE_SPECS += [
    Spec(
        code="HOUSE_REVENUE_VICE_CHAIR",
        title="Vice Chair, House Committee on Revenue",
        domain=RoleDomain.COMMITTEE,
        chamber=Chamber.HOUSE,
        committee_code="REVENUE_JOINT",
        committee_role_type=CommitteeRoleType.VICE_CHAIR,
        tier_id=T15K,
    ),
]

# Judiciary – House vice chair & ranking minority – 15,000
ROLE_SPECS += [
    Spec(
        code="HOUSE_JUDICIARY_VICE_CHAIR",
        title="House Vice Chair, Joint Committee on the Judiciary",
        domain=RoleDomain.COMMITTEE,
        chamber=Chamber.HOUSE,
        committee_code="JUDICIARY_JOINT",
        committee_role_type=CommitteeRoleType.VICE_CHAIR,
        tier_id=T15K,
    ),
    Spec(
        code="HOUSE_JUDICIARY_RANKING_MINORITY",
        title=(
            "Ranking Minority Member, House, Joint Committee on the Judiciary"
        ),
        domain=RoleDomain.COMMITTEE,
        chamber=Chamber.HOUSE,
        committee_code="JUDICIARY_JOINT",
        committee_role_type=CommitteeRoleType.RANKING_MINORITY,
        tier_id=T15K,
    ),
]

# Transportation – House vice chair – 15,000
ROLE_SPECS += [
    Spec(
        code="HOUSE_TRANSPORTATION_VICE_CHAIR",
        title="Vice Chair, Joint Committee on Transportation (House)",
        domain=RoleDomain.COMMITTEE,
        chamber=Chamber.HOUSE,
        committee_code="TRANSPORTATION_JOINT",
        committee_role_type=CommitteeRoleType.VICE_CHAIR,
        tier_id=T15K,
    ),
]

# Bills in the Third Reading – House vice chair – 15,000
ROLE_SPECS += [
    Spec(
        code="HOUSE_BILLS_THIRD_READING_VICE_CHAIR",
        title="Vice Chair, House Committee on Bills in the Third Reading",
        domain=RoleDomain.COMMITTEE,
        chamber=Chamber.HOUSE,
        committee_code="BILLS_THIRD_READING_HOUSE",
        committee_role_type=CommitteeRoleType.VICE_CHAIR,
        tier_id=T15K,
    ),
]

# Steering, Policy and Scheduling – House vice chair – 15,000
ROLE_SPECS += [
    Spec(
        code="HOUSE_STEERING_POLICY_SCHEDULING_VICE_CHAIR",
        title="Vice Chair, House Committee on Steering, Policy and Scheduling",
        domain=RoleDomain.COMMITTEE,
        chamber=Chamber.HOUSE,
        committee_code="STEERING_POLICY_SCHEDULING_HOUSE",
        committee_role_type=CommitteeRoleType.VICE_CHAIR,
        tier_id=T15K,
    ),
]

# Education – House vice chair – 15,000
ROLE_SPECS += [
    Spec(
        code="HOUSE_EDUCATION_VICE_CHAIR",
        title="House Vice Chair, Joint Committee on Education",
        domain=RoleDomain.COMMITTEE,
        chamber=Chamber.HOUSE,
        committee_code="EDUCATION_JOINT",
        committee_role_type=CommitteeRoleType.VICE_CHAIR,
        tier_id=T15K,
    ),
]

# Telecommunications, Utilities and Energy – House vice chair – 15,000
ROLE_SPECS += [
    Spec(
        code="HOUSE_TELECOM_UTILITIES_ENERGY_VICE_CHAIR",
        title=(
            "House Vice Chair, Joint Committee on "
            "Telecommunications, Utilities and Energy"
        ),
        domain=RoleDomain.COMMITTEE,
        chamber=Chamber.HOUSE,
        committee_code="TELECOM_UTILITIES_ENERGY_JOINT",
        committee_role_type=CommitteeRoleType.VICE_CHAIR,
        tier_id=T15K,
    ),
]

# ---------------------------------------------------------------------------
# 9B(f): Vice chairs of all other committees – 5,200
# ---------------------------------------------------------------------------

ROLE_SPECS += [
    Spec(
        code="GENERIC_OTHER_COMMITTEE_VICE_CHAIR",
        title="Vice Chair, other committee (not otherwise specified)",
        domain=RoleDomain.COMMITTEE,
        chamber=None,
        committee_code=None,
        committee_role_type=CommitteeRoleType.VICE_CHAIR,
        tier_id=T5200,
    ),
]

# ---------------------------------------------------------------------------
# Build RoleDefinition registry
# ---------------------------------------------------------------------------

ROLE_DEFINITIONS: dict[str, RoleDefinition] = {
    spec["code"]: RoleDefinition(
        code=spec["code"],
        title=spec["title"],
        domain=spec["domain"],
        chamber=spec["chamber"],
        committee_code=spec.get("committee_code"),
        committee_role_type=spec.get("committee_role_type"),
        stipend_tier_id=spec.get("tier_id"),
    )
    for spec in ROLE_SPECS
}


def get_role_definition(code: str) -> RoleDefinition:
    return ROLE_DEFINITIONS[code]
