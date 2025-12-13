"""Data structures"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum, Enum, auto
from typing import Optional


class Chamber(Enum):
    """Enumeration for different chambers of the Legislature"""

    HOUSE = "house"
    SENATE = "senate"
    JOINT = "joint"


class Party(Enum):
    """Enumeration for political parties"""

    DEMOCRAT = "D"
    REPUBLICAN = "R"
    OTHER = "Other"
    UNKNOWN = "Unknown"


class RoleDomain(Enum):
    """High-level bucket for role types"""

    LEADERSHIP = auto()
    COMMITTEE = auto()
    PARTY_LEADERSHIP = auto()
    OTHER = auto()


class CommitteeRoleType(Enum):
    """Enumeration for committee roles"""

    CHAIR = auto()
    VICE_CHAIR = auto()
    RANKING_MINORITY = auto()
    ASSISTANT_VICE_CHAIR = auto()
    ASSISTANT_RANKING_MINORITY = auto()
    MEMBER = auto()


@dataclass(frozen=True)
class Session:
    """A legislative session"""

    id: str
    start_year: int
    end_year: int
    label: str = ""


@dataclass(frozen=True)
class Committee:
    """A legislative committee"""

    code: str
    name: str
    chamber: Chamber


@dataclass(frozen=True)
class RoleDefinition:
    """Definition of a role type"""

    code: RoleCode
    title: str
    domain: RoleDomain
    chamber: Optional[Chamber]
    committee_code: Optional[str]
    committee_role_type: Optional[CommitteeRoleType]
    stipend_tier_id: Optional[str]


@dataclass
class Member:
    """A legislative member"""

    member_id: str
    name: str
    chamber: Chamber
    party: Party = Party.UNKNOWN
    distance_miles_from_state_house: Optional[float] = None
    roles: list[RoleAssignment]


@dataclass(frozen=True)
class RoleAssignment:
    """An assignment of a role to a member during a session"""

    member_id: str
    role_code: str
    session_id: str


class RoleCode(StrEnum):
    """Enumeration of role codes"""

    SPEAKER = "SPEAKER"
    SENATE_PRESIDENT = "SENATE_PRESIDENT"
    HOUSE_WM_CHAIR = "HOUSE_WM_CHAIR"
    SENATE_WM_CHAIR = "SENATE_WM_CHAIR"
    HOUSE_MAJORITY_LEADER = "HOUSE_MAJORITY_LEADER"
    HOUSE_MINORITY_LEADER = "HOUSE_MINORITY_LEADER"
    SENATE_MAJORITY_LEADER = "SENATE_MAJORITY_LEADER"
    SENATE_MINORITY_LEADER = "SENATE_MINORITY_LEADER"
    HOUSE_SPEAKER_PRO_TEM = "HOUSE_SPEAKER_PRO_TEM"
    SENATE_SPEAKER_PRO_TEM = "SENATE_SPEAKER_PRO_TEM"
    HOUSE_ASSISTANT_MAJORITY_LEADER = "HOUSE_ASSISTANT_MAJORITY_LEADER"
    HOUSE_ASSISTANT_MINORITY_LEADER = "HOUSE_ASSISTANT_MINORITY_LEADER"
    HOUSE_RULES_CHAIR = "HOUSE_RULES_CHAIR"
    SENATE_RULES_CHAIR = "SENATE_RULES_CHAIR"
    HOUSE_EDUCATION_CHAIR = "HOUSE_EDUCATION_CHAIR"
    SENATE_EDUCATION_CHAIR = "SENATE_EDUCATION_CHAIR"
    HOUSE_JUDICIARY_CHAIR = "HOUSE_JUDICIARY_CHAIR"
    SENATE_JUDICIARY_CHAIR = "SENATE_JUDICIARY_CHAIR"


class StipendTierCode(StrEnum):
    """Enumeration of stipend tier codes"""

    TIER_80K = "T80K"
    TIER_65K = "T65K"
    TIER_60K = "T60K"
    TIER_50K = "T50K"
    TIER_35K = "T35K"
    TIER_30K = "T30K"
    TIER_15K = "T15K"
    TIER_5200 = "T5200"

    @staticmethod
    def get_base_amount(tier_id: StipendTierCode) -> int:
        """Get the base amount for the stipend tier"""
        tier_amounts = {
            StipendTierCode.TIER_80K: 80_000,
            StipendTierCode.TIER_65K: 65_000,
            StipendTierCode.TIER_60K: 60_000,
            StipendTierCode.TIER_50K: 50_000,
            StipendTierCode.TIER_35K: 35_000,
            StipendTierCode.TIER_30K: 30_000,
            StipendTierCode.TIER_15K: 15_000,
            StipendTierCode.TIER_5200: 5_200,
        }
        return tier_amounts[tier_id]
