"""Data structures"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum, Enum, auto
from typing import Optional

from audit.provenance import AmountWithProvenance
from audit.sources_registry import MGL_3_9B


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

    @staticmethod
    def from_id_number(session: int) -> Session:
        """Generates session ID from General Court #"""
        sessions: dict[int, str] = {
            0: "0-1",  # demo
            194: "2025-2026",
        }
        if session not in sessions:
            raise IndexError(f"Session #{session} not recognized.")
        return Session(
            id=sessions[session],
            start_year=sessions[session].split("-")[0],
            end_year=sessions[session].split("-")[1],
        )


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
    roles: list[RoleAssignment] = field(default_factory=list)
    party: Party = Party.UNKNOWN
    district: Optional[str] = None
    distance_miles_from_state_house: Optional[float] = None


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
    HOUSE_SPEAKER_PRO_TEMPORE = "HOUSE_SPEAKER_PRO_TEMPORE"
    SENATE_PRESIDENT_PRO_TEMPORE = "SENATE_PRESIDENT_PRO_TEMPORE"
    HOUSE_ASSISTANT_MAJORITY_LEADER = "HOUSE_ASSISTANT_MAJORITY_LEADER"
    HOUSE_SECOND_ASSISTANT_MAJORITY_LEADER = "HOUSE_SECOND_ASSISTANT_MAJORITY_LEADER"
    HOUSE_THIRD_ASSISTANT_MAJORITY_LEADER = "HOUSE_THIRD_ASSISTANT_MAJORITY_LEADER"
    HOUSE_ASSISTANT_MINORITY_LEADER = "HOUSE_ASSISTANT_MINORITY_LEADER"
    HOUSE_SECOND_ASSISTANT_MINORITY_LEADER = "HOUSE_SECOND_ASSISTANT_MINORITY_LEADER"
    HOUSE_THIRD_ASSISTANT_MINORITY_LEADER = "HOUSE_THIRD_ASSISTANT_MINORITY_LEADER"
    SENATE_ASSISTANT_MAJORITY_LEADER = "SENATE_ASSISTANT_MAJORITY_LEADER"
    SENATE_SECOND_ASSISTANT_MAJORITY_LEADER = "SENATE_SECOND_ASSISTANT_MAJORITY_LEADER"
    SENATE_THIRD_ASSISTANT_MAJORITY_LEADER = "SENATE_THIRD_ASSISTANT_MAJORITY_LEADER"
    SENATE_ASSISTANT_MINORITY_LEADER = "SENATE_ASSISTANT_MINORITY_LEADER"
    SENATE_SECOND_ASSISTANT_MINORITY_LEADER = "SENATE_SECOND_ASSISTANT_MINORITY_LEADER"
    SENATE_THIRD_ASSISTANT_MINORITY_LEADER = "SENATE_THIRD_ASSISTANT_MINORITY_LEADER"
    HOUSE_RULES_CHAIR = "HOUSE_RULES_CHAIR"
    SENATE_RULES_CHAIR = "SENATE_RULES_CHAIR"
    HOUSE_EDUCATION_CHAIR = "HOUSE_EDUCATION_CHAIR"
    SENATE_EDUCATION_CHAIR = "SENATE_EDUCATION_CHAIR"
    HOUSE_JUDICIARY_CHAIR = "HOUSE_JUDICIARY_CHAIR"
    SENATE_JUDICIARY_CHAIR = "SENATE_JUDICIARY_CHAIR"
    GENERIC_OTHER_COMMITTEE_CHAIR = "GENERIC_OTHER_COMMITTEE_CHAIR"
    GENERIC_OTHER_COMMITTEE_VICE_CHAIR = "GENERIC_OTHER_COMMITTEE_VICE_CHAIR"


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
    def get_base_amount(tier_id: StipendTierCode) -> AmountWithProvenance:
        """Get the base amount for the stipend tier"""
        tier_amounts: dict[StipendTierCode, AmountWithProvenance] = {
            StipendTierCode.TIER_80K: AmountWithProvenance(80_000, MGL_3_9B),
            StipendTierCode.TIER_65K: AmountWithProvenance(65_000, MGL_3_9B),
            StipendTierCode.TIER_60K: AmountWithProvenance(60_000, MGL_3_9B),
            StipendTierCode.TIER_50K: AmountWithProvenance(50_000, MGL_3_9B),
            StipendTierCode.TIER_35K: AmountWithProvenance(35_000, MGL_3_9B),
            StipendTierCode.TIER_30K: AmountWithProvenance(30_000, MGL_3_9B),
            StipendTierCode.TIER_15K: AmountWithProvenance(15_000, MGL_3_9B),
            StipendTierCode.TIER_5200: AmountWithProvenance(5_200, MGL_3_9B),
        }
        return tier_amounts[tier_id]
