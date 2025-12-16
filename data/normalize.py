"""Normalize raw to structured"""

from __future__ import annotations

from typing import Optional

from config.committee_catalog import get_committee_by_external_id
from config.role_catalog import ROLE_DEFINITIONS
from models.core import CommitteeRoleType


def normalize_role_label(raw: Optional[str]) -> Optional[CommitteeRoleType]:
    if not raw:
        return None
    t = raw.lower()
    if "chair" in t and "vice" not in t:
        return CommitteeRoleType.CHAIR
    if "vice" in t:
        return CommitteeRoleType.VICE_CHAIR
    if "ranking" in t:
        return CommitteeRoleType.RANKING_MINORITY
    return None


def committee_role_to_internal(
    chamber: str,
    committee_external_id: str,
    raw_role_label: Optional[str],
) -> Optional[str]:
    role_type = normalize_role_label(raw_role_label)
    if role_type is None:
        return None
    committee = get_committee_by_external_id(committee_external_id)
    if committee is None:
        if role_type is CommitteeRoleType.CHAIR:
            return "GENERIC_OTHER_COMMITTEE_CHAIR"
        if role_type is CommitteeRoleType.VICE_CHAIR:
            return "GENERIC_OTHER_COMMITTEE_VICE_CHAIR"
        return None
    committee_code = committee.code
    for rd in ROLE_DEFINITIONS.values():
        if rd.committee_code != committee_code:
            continue
        if rd.committee_role_type != role_type:
            continue
        if rd.chamber is not None and rd.chamber.name.lower() != chamber:
            continue
        return rd.code
    if role_type is CommitteeRoleType.CHAIR:
        return "GENERIC_OTHER_COMMITTEE_CHAIR"
    if role_type is CommitteeRoleType.VICE_CHAIR:
        return "GENERIC_OTHER_COMMITTEE_VICE_CHAIR"
    return None


def main() -> None:
    """Run normalization to convert raw data"""
    normalize("2025-2026", Path("data/raw"), Path("data/sessions"))


if __name__ == "__main__":
    main()
