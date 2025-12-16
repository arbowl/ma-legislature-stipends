"""Normalize raw to structured"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

from config.committee_catalog import get_committee_by_external_id
from config.role_catalog import ROLE_DEFINITIONS
from models.core import CommitteeRoleType


def normalize_role_label(raw: Optional[str]) -> Optional[CommitteeRoleType]:
    """Tooling to translate roles and committees"""
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


def normalize_leadership_title(raw_title: str, chamber: str) -> Optional[str]:
    """Map scraped leadership title to internal role code"""
    title_lower = raw_title.lower().strip()
    chamber_lower = chamber.lower().strip()
    if title_lower == "president of the senate" and chamber_lower == "senate":
        return "SENATE_PRESIDENT"
    if title_lower == "president pro tempore" and chamber_lower == "senate":
        return "SENATE_PRESIDENT_PRO_TEMPORE"
    if title_lower == "speaker of the house" and chamber_lower == "house":
        return "SPEAKER"
    if title_lower == "speaker pro tempore" and chamber_lower == "house":
        return "HOUSE_SPEAKER_PRO_TEMPORE"
    if title_lower == "majority leader":
        if chamber_lower == "senate":
            return "SENATE_MAJORITY_FLOOR_LEADER"
        if chamber_lower == "house":
            return "HOUSE_MAJORITY_FLOOR_LEADER"
    if title_lower == "minority leader":
        if chamber_lower == "senate":
            return "SENATE_MINORITY_FLOOR_LEADER"
        if chamber_lower == "house":
            return "HOUSE_MINORITY_FLOOR_LEADER"
    if title_lower == "assistant majority leader":
        if chamber_lower == "senate":
            return "SENATE_MAJORITY_ASSISTANT_FLOOR_LEADER"
        if chamber_lower == "house":
            return "HOUSE_MAJORITY_ASSISTANT_FLOOR_LEADER"
    if title_lower == "second assistant majority leader":
        if chamber_lower == "house":
            return "HOUSE_MAJORITY_SECOND_ASSISTANT_FLOOR_LEADER"
    if title_lower == "assistant minority leader" and chamber_lower == "senate":
        return "SENATE_MINORITY_ASSISTANT_FLOOR_LEADER"
    if title_lower == "first assistant minority leader" and chamber_lower == "house":
        return "HOUSE_MINORITY_ASSISTANT_FLOOR_LEADER"
    if title_lower == "second assistant minority leader" and chamber_lower == "house":
        return "HOUSE_MINORITY_SECOND_ASSISTANT_FLOOR_LEADER"
    if title_lower == "third assistant minority leader" and chamber_lower == "house":
        return "HOUSE_MINORITY_THIRD_ASSISTANT_FLOOR_LEADER"
    if title_lower == "first division chair" and chamber_lower == "house":
        return "HOUSE_DIVISION_CHAIR_1"
    if title_lower == "second division chair" and chamber_lower == "house":
        return "HOUSE_DIVISION_CHAIR_2"
    if title_lower == "third division chair" and chamber_lower == "house":
        return "HOUSE_DIVISION_CHAIR_3"
    if title_lower == "fourth division chair" and chamber_lower == "house":
        return "HOUSE_DIVISION_CHAIR_4"
    return None


def normalize_leadership_roles(
    session_id: str,
    raw_root: Path,
    sessions_root: Path
) -> None:
    """Convert leadership_raw.json to roles entries"""
    raw_file = raw_root / session_id / "leadership_raw.json"
    with raw_file.open('r', encoding='utf-8') as f:
        leadership_data = json.load(f)
    role_entries = []
    unmapped_roles = []
    for entry in leadership_data:
        member_id = entry["member_id"]
        raw_title = entry["raw_title"]
        chamber = entry["chamber"]
        role_code = normalize_leadership_title(raw_title, chamber)
        if role_code is None:
            unmapped_roles.append((member_id, raw_title, chamber))
            print(f"[UNMAPPED] {member_id}: '{raw_title}' in {chamber}")
        else:
            role_entries.append({
                "member_id": member_id,
                "role_code": role_code,
                "session_id": session_id
            })
    if unmapped_roles:
        print(f"\nWarning: {len(unmapped_roles)} leadership roles not modeled in 9B")
        print("These roles exist but have no statutory stipend basis:")
        for mid, title, chamber in unmapped_roles:
            print(f"  - {mid}: {title} ({chamber})")
    output_file = sessions_root / session_id / "roles.json"
    output_data = {
        "session_id": session_id,
        "roles": role_entries
    }
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with output_file.open('w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2)
    print(f"\nWrote {len(role_entries)} leadership roles to {output_file}")


def main() -> None:
    """Run normalization to convert raw data"""
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("session_id", help="Session ID, e.g. 2025-2026")
    args = parser.parse_args()
    normalize_leadership_roles(
        args.session_id,
        Path("data/raw"),
        Path("data/sessions")
    )


if __name__ == "__main__":
    main()
