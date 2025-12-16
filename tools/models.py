"""Data models for tool outputs"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any, Optional

from audit.provenance import SourceRef


@dataclass
class ProvenanceInfo:
    """Provenance information for JSON export"""

    source_id: str
    label: str
    kind: str
    url: Optional[str] = None
    details: list[str] = None

    @staticmethod
    def from_source_ref(source: SourceRef) -> ProvenanceInfo:
        """Convert SourceRef to JSON-serializable format"""
        details_list = list(source.details) if source.details else []
        return ProvenanceInfo(
            source_id=source.id,
            label=source.label,
            kind=source.kind.name,
            url=source.url,
            details=details_list if details_list else None,
        )

    def to_dict(self) -> dict[str, Any]:
        """Convert to dict, excluding None values"""
        result = asdict(self)
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class RoleStipendInfo:
    """Information about a role stipend"""

    role_code: str
    role_title: str
    tier_id: Optional[str]
    base_amount: int
    adjusted_amount: int
    adjustment_factor: float
    paid: bool
    reason: str
    provenance: list[dict[str, Any]]

    def to_dict(self) -> dict[str, Any]:
        """Converts the dataclass to a dict"""
        return asdict(self)


@dataclass
class CompensationComponent:
    """A component of compensation"""

    label: str
    amount: int
    provenance: list[dict[str, Any]]
    details: Optional[dict[str, Any]] = None

    def to_dict(self) -> dict[str, Any]:
        """Converts the dataclass to a dict"""
        result = asdict(self)
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class MemberProfile:
    """Complete member profile"""

    member_id: str
    name: str
    chamber: str
    party: str
    district: Optional[str]
    distance_from_state_house: Optional[float]
    session_id: str
    compensation: dict[str, Any]
    validation_issues: list[dict[str, Any]]
    raw_data_sources: dict[str, str]

    def to_dict(self) -> dict[str, Any]:
        """Converts the dataclass to a dict"""
        return asdict(self)


@dataclass
class SessionSummaryStats:
    """Summary statistics for a session"""

    session_id: str
    total_members: int
    total_compensation: int
    average_compensation: float
    median_compensation: float
    by_chamber: dict[str, dict[str, Any]]
    by_party: dict[str, dict[str, Any]]
    stipend_distribution: dict[str, int]
    top_earners: list[dict[str, Any]]

    def to_dict(self) -> dict[str, Any]:
        """Converts the dataclass to a dict"""
        return asdict(self)


@dataclass
class SessionReport:
    """Complete session report"""

    session_id: str
    session_label: str
    start_year: int
    end_year: int
    generated_at: str
    members: list[dict[str, Any]]
    summary_statistics: dict[str, Any]
    validation_summary: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        """Converts the dataclass to a dict"""
        return asdict(self)
