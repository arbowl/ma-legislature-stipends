"""Committees and codes"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final, Optional

from models.core import Chamber


@dataclass(frozen=True)
class Committee:
    """Committee metadata"""

    code: str
    name: str
    is_joint: bool
    primary_chamber: Optional[Chamber]
    external_ids: tuple[str, ...] = ()


_COMMITTEES = [
    Committee(
        code="JOINT_ADVANCED_INFORMATION_TECHNOLOGY_THE_INTERNET_AND_CYBERSECURITY",
        name="Joint Committee on Advanced Information Technology, the Internet and Cybersecurity",
        chamber=None,
        is_joint=True,
        external_ids=("J33",),
    ),
    Committee(
        code="JOINT_AGING_AND_INDEPENDENCE",
        name="Joint Committee on Aging and Independence",
        chamber=None,
        is_joint=True,
        external_ids=("J46",),
    ),
    Committee(
        code="JOINT_AGRICULTURE_AND_FISHERIES",
        name="Joint Committee on Agriculture and Fisheries",
        chamber=None,
        is_joint=True,
        external_ids=("J45",),
    ),
    Committee(
        code="JOINT_BONDING_CAPITAL_EXPENDITURES_AND_STATE_ASSETS",
        name="Joint Committee on Bonding, Capital Expenditures and State Assets",
        chamber=None,
        is_joint=True,
        external_ids=("J32",),
    ),
    Committee(
        code="JOINT_CANNABIS_POLICY",
        name="Joint Committee on Cannabis Policy",
        chamber=None,
        is_joint=True,
        external_ids=("J50",),
    ),
    Committee(
        code="JOINT_CHILDREN_FAMILIES_AND_PERSONS_WITH_DISABILITIES",
        name="Joint Committee on Children, Families and Persons with Disabilities",
        chamber=None,
        is_joint=True,
        external_ids=("J13",),
    ),
    Committee(
        code="JOINT_COMMUNITY_DEVELOPMENT_AND_SMALL_BUSINESSES",
        name="Joint Committee on Community Development and Small Businesses",
        chamber=None,
        is_joint=True,
        external_ids=("J47",),
    ),
    Committee(
        code="JOINT_CONSUMER_PROTECTION_AND_PROFESSIONAL_LICENSURE",
        name="Joint Committee on Consumer Protection and Professional Licensure",
        chamber=None,
        is_joint=True,
        external_ids=("J17",),
    ),
    Committee(
        code="JOINT_ECONOMIC_DEVELOPMENT_AND_EMERGING_TECHNOLOGIES",
        name="Joint Committee on Economic Development and Emerging Technologies",
        chamber=None,
        is_joint=True,
        external_ids=("J12",),
    ),
    Committee(
        code="JOINT_EDUCATION",
        name="Joint Committee on Education",
        chamber=None,
        is_joint=True,
        external_ids=("J14",),
    ),
    Committee(
        code="JOINT_ELECTION_LAWS",
        name="Joint Committee on Election Laws",
        chamber=None,
        is_joint=True,
        external_ids=("J15",),
    ),
    Committee(
        code="JOINT_EMERGENCY_PREPAREDNESS_AND_MANAGEMENT",
        name="Joint Committee on Emergency Preparedness and Management",
        chamber=None,
        is_joint=True,
        external_ids=("J52",),
    ),
    Committee(
        code="JOINT_ENVIRONMENT_AND_NATURAL_RESOURCES",
        name="Joint Committee on Environment and Natural Resources",
        chamber=None,
        is_joint=True,
        external_ids=("J21",),
    ),
    Committee(
        code="JOINT_FINANCIAL_SERVICES",
        name="Joint Committee on Financial Services",
        chamber=None,
        is_joint=True,
        external_ids=("J11",),
    ),
    Committee(
        code="JOINT_HEALTH_CARE_FINANCING",
        name="Joint Committee on Health Care Financing",
        chamber=None,
        is_joint=True,
        external_ids=("J24",),
    ),
    Committee(
        code="JOINT_HIGHER_EDUCATION",
        name="Joint Committee on Higher Education",
        chamber=None,
        is_joint=True,
        external_ids=("J29",),
    ),
    Committee(
        code="JOINT_HOUSING",
        name="Joint Committee on Housing",
        chamber=None,
        is_joint=True,
        external_ids=("J28",),
    ),
    Committee(
        code="JOINT_THE_JUDICIARY",
        name="Joint Committee on the Judiciary",
        chamber=None,
        is_joint=True,
        external_ids=("J19",),
    ),
    Committee(
        code="JOINT_LABOR_AND_WORKFORCE_DEVELOPMENT",
        name="Joint Committee on Labor and Workforce Development",
        chamber=None,
        is_joint=True,
        external_ids=("J43",),
    ),
    Committee(
        code="JOINT_MENTAL_HEALTH_SUBSTANCE_USE_AND_RECOVERY",
        name="Joint Committee on Mental Health, Substance Use and Recovery",
        chamber=None,
        is_joint=True,
        external_ids=("J18",),
    ),
    Committee(
        code="JOINT_MUNICIPALITIES_AND_REGIONAL_GOVERNMENT",
        name="Joint Committee on Municipalities and Regional Government",
        chamber=None,
        is_joint=True,
        external_ids=("J10",),
    ),
    Committee(
        code="JOINT_PUBLIC_HEALTH",
        name="Joint Committee on Public Health",
        chamber=None,
        is_joint=True,
        external_ids=("J16",),
    ),
    Committee(
        code="JOINT_PUBLIC_SAFETY_AND_HOMELAND_SECURITY",
        name="Joint Committee on Public Safety and Homeland Security",
        chamber=None,
        is_joint=True,
        external_ids=("J22",),
    ),
    Committee(
        code="JOINT_PUBLIC_SERVICE",
        name="Joint Committee on Public Service",
        chamber=None,
        is_joint=True,
        external_ids=("J23",),
    ),
    Committee(
        code="JOINT_RACIAL_EQUITY_CIVIL_RIGHTS_AND_INCLUSION",
        name="Joint Committee on Racial Equity, Civil Rights, and Inclusion",
        chamber=None,
        is_joint=True,
        external_ids=("J34",),
    ),
    Committee(
        code="JOINT_REVENUE",
        name="Joint Committee on Revenue",
        chamber=None,
        is_joint=True,
        external_ids=("J26",),
    ),
    Committee(
        code="JOINT_RULES",
        name="Joint Committee on Rules",
        chamber=None,
        is_joint=True,
        external_ids=("J40",),
    ),
    Committee(
        code="JOINT_STATE_ADMINISTRATION_AND_REGULATORY_OVERSIGHT",
        name="Joint Committee on State Administration and Regulatory Oversight",
        chamber=None,
        is_joint=True,
        external_ids=("J25",),
    ),
    Committee(
        code="JOINT_TELECOMMUNICATIONS_UTILITIES_AND_ENERGY",
        name="Joint Committee on Telecommunications, Utilities and Energy",
        chamber=None,
        is_joint=True,
        external_ids=("J37",),
    ),
    Committee(
        code="JOINT_TOURISM_ARTS_AND_CULTURAL_DEVELOPMENT",
        name="Joint Committee on Tourism, Arts and Cultural Development",
        chamber=None,
        is_joint=True,
        external_ids=("J30",),
    ),
    Committee(
        code="JOINT_TRANSPORTATION",
        name="Joint Committee on Transportation",
        chamber=None,
        is_joint=True,
        external_ids=("J27",),
    ),
    Committee(
        code="JOINT_VETERANS_AND_FEDERAL_AFFAIRS",
        name="Joint Committee on Veterans and Federal Affairs",
        chamber=None,
        is_joint=True,
        external_ids=("J31",),
    ),
    Committee(
        code="JOINT_WAYS_AND_MEANS",
        name="Joint Committee on Ways and Means",
        chamber=None,
        is_joint=True,
        external_ids=("J39",),
    ),
    Committee(
        code="SENATE_BILLS_IN_THE_THIRD_READING",
        name="Senate Committee on Bills in the Third Reading",
        chamber=Chamber.SENATE,
        is_joint=False,
        external_ids=("S31",),
    ),
    Committee(
        code="SENATE_THE_CENSUS",
        name="Senate Committee on the Census",
        chamber=Chamber.SENATE,
        is_joint=False,
        external_ids=("S65",),
    ),
    Committee(
        code="SENATE_CLIMATE_CHANGE_AND_GLOBAL_WARMING",
        name="Senate Committee on Climate Change and Global Warming",
        chamber=Chamber.SENATE,
        is_joint=False,
        external_ids=("S51",),
    ),
    Committee(
        code="SENATE_ETHICS",
        name="Senate Committee on Ethics",
        chamber=Chamber.SENATE,
        is_joint=False,
        external_ids=("S56",),
    ),
    Committee(
        code="SENATE_INTERGOVERNMENTAL_AFFAIRS",
        name="Senate Committee on Intergovernmental Affairs",
        chamber=Chamber.SENATE,
        is_joint=False,
        external_ids=("S55",),
    ),
    Committee(
        code="SENATE_JUVENILE_AND_EMERGING_ADULT_JUSTICE",
        name="Senate Committee on Juvenile and Emerging Adult Justice",
        chamber=Chamber.SENATE,
        is_joint=False,
        external_ids=("S66",),
    ),
    Committee(
        code="SENATE_PERSONNEL_AND_ADMINISTRATION",
        name="Senate Committee on Personnel and Administration",
        chamber=Chamber.SENATE,
        is_joint=False,
        external_ids=("S53",),
    ),
    Committee(
        code="SENATE_POST_AUDIT_AND_OVERSIGHT",
        name="Senate Committee on Post Audit and Oversight",
        chamber=Chamber.SENATE,
        is_joint=False,
        external_ids=("S48",),
    ),
    Committee(
        code="SENATE_RULES",
        name="Senate Committee on Rules",
        chamber=Chamber.SENATE,
        is_joint=False,
        external_ids=("S29",),
    ),
    Committee(
        code="COMMITTEE_SUBCOMMITTEE_ON_CHAPTER_250_OF_THE_ACTS_OF_2024",
        name="Subcommittee on chapter 250 of the acts of 2024",
        chamber=None,
        is_joint=False,
        external_ids=("TS10",),
    ),
    Committee(
        code="SENATE_STEERING_AND_POLICY",
        name="Senate Committee on Steering and Policy",
        chamber=Chamber.SENATE,
        is_joint=False,
        external_ids=("S50",),
    ),
    Committee(
        code="SENATE_WAYS_AND_MEANS",
        name="Senate Committee on Ways and Means",
        chamber=Chamber.SENATE,
        is_joint=False,
        external_ids=("S30",),
    ),
    Committee(
        code="HOUSE_BILLS_IN_THE_THIRD_READING",
        name="House Committee on Bills in the Third Reading",
        chamber=Chamber.HOUSE,
        is_joint=False,
        external_ids=("H36",),
    ),
    Committee(
        code="HOUSE_CLIMATE_ACTION_AND_SUSTAINABILITY",
        name="House Committee on Climate Action and Sustainability",
        chamber=Chamber.HOUSE,
        is_joint=False,
        external_ids=("H51",),
    ),
    Committee(
        code="HOUSE_ETHICS",
        name="House Committee on Ethics",
        chamber=Chamber.HOUSE,
        is_joint=False,
        external_ids=("H38",),
    ),
    Committee(
        code="HOUSE_FEDERAL_FUNDING_POLICY_AND_ACCOUNTABILITY",
        name="House Committee on Federal Funding, Policy and Accountability",
        chamber=Chamber.HOUSE,
        is_joint=False,
        external_ids=("H54",),
    ),
    Committee(
        code="HOUSE_HUMAN_RESOURCES_AND_EMPLOYEE_ENGAGEMENT",
        name="House Committee on Human Resources and Employee Engagement",
        chamber=Chamber.HOUSE,
        is_joint=False,
        external_ids=("H45",),
    ),
    Committee(
        code="HOUSE_INTERGOVERNMENTAL_AFFAIRS",
        name="House Committee on Intergovernmental Affairs",
        chamber=Chamber.HOUSE,
        is_joint=False,
        external_ids=("Hxx",),
    ),
    Committee(
        code="HOUSE_OPERATIONS_FACILITIES_AND_SECURITY",
        name="House Committee on Operations, Facilities and Security",
        chamber=Chamber.HOUSE,
        is_joint=False,
        external_ids=("H53",),
    ),
    Committee(
        code="HOUSE_POST_AUDIT_AND_OVERSIGHT",
        name="House Committee on Post Audit and Oversight",
        chamber=Chamber.HOUSE,
        is_joint=False,
        external_ids=("H46",),
    ),
    Committee(
        code="HOUSE_RULES",
        name="House Committee on Rules",
        chamber=Chamber.HOUSE,
        is_joint=False,
        external_ids=("H33",),
    ),
    Committee(
        code="HOUSE_STEERING_POLICY_AND_SCHEDULING",
        name="House Committee on Steering, Policy and Scheduling",
        chamber=Chamber.HOUSE,
        is_joint=False,
        external_ids=("H52",),
    ),
    Committee(
        code="HOUSE_WAYS_AND_MEANS",
        name="House Committee on Ways and Means",
        chamber=Chamber.HOUSE,
        is_joint=False,
        external_ids=("H34",),
    ),
]


COMMITTEES_BY_CODE = Final[dict[str, Committee]] = {c.code for c in _COMMITTEES}

COMMITTEES_BY_EXTERNAL_ID = Final[dict[str, Committee]] = {
    ext: c for c in _COMMITTEES for ext in c.external_ids
}


def get_committee_by_external_id(ext_id: str) -> Committee:
    """Helper to get committee name via ID"""
    return COMMITTEES_BY_EXTERNAL_ID.get(ext_id)
