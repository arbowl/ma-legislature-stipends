"""Normalize all roles (committee + leadership) from raw to structured format"""

import json
from pathlib import Path
from typing import Optional
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))
from config.committee_catalog import get_committee_by_external_id
from config.role_catalog import ROLE_DEFINITIONS
from models.core import CommitteeRoleType


def normalize_role_label(raw: Optional[str]) -> Optional[CommitteeRoleType]:
    """Translate committee role labels"""
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
    """Map committee role to internal code"""
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


def main() -> None:
    """Normalize both committee and leadership roles into roles.json"""
    session_id = "2025-2026"
    raw_dir = Path("data/raw") / session_id
    output_dir = Path("data/sessions") / session_id
    all_role_entries = []
    print("=" * 60)
    print("NORMALIZING ALL ROLES")
    print("=" * 60)
    print("\n1. Processing committee roles...")
    committee_file = raw_dir / "committee_roles_raw.json"
    with committee_file.open("r", encoding="utf-8") as f:
        committee_data = json.load(f)
    for entry in committee_data:
        member_id = entry["member_id"]
        committee_external_id = entry["committee_external_id"]
        raw_role_label = entry.get("raw_role_label")
        if raw_role_label is None:
            continue
        with (Path("data/sessions") / session_id / "members.json").open() as mf:
            members_data = json.load(mf)
            member = next(
                (m for m in members_data["members"] if m["member_id"] == member_id),
                None,
            )
            if member is None:
                continue
            chamber = member["chamber"]
        role_code = committee_role_to_internal(
            chamber, committee_external_id, raw_role_label
        )
        if role_code:
            all_role_entries.append(
                {
                    "member_id": member_id,
                    "role_code": role_code,
                    "session_id": session_id,
                }
            )
    print(f"   Processed {len(all_role_entries)} committee roles")
    print("\n2. Processing leadership roles...")
    leadership_file = raw_dir / "leadership_raw.json"
    with leadership_file.open("r", encoding="utf-8") as f:
        leadership_data = json.load(f)
    unmapped_roles = []
    leadership_count = 0
    for entry in leadership_data:
        member_id = entry["member_id"]
        raw_title = entry["raw_title"]
        chamber = entry["chamber"]
        role_code = normalize_leadership_title(raw_title, chamber)
        if role_code is None:
            unmapped_roles.append((member_id, raw_title, chamber))
        else:
            all_role_entries.append(
                {
                    "member_id": member_id,
                    "role_code": role_code,
                    "session_id": session_id,
                }
            )
            leadership_count += 1
    print(f"   Processed {leadership_count} leadership roles")
    if unmapped_roles:
        print(
            f"\n   [WARNING] {len(unmapped_roles)} leadership roles not modeled in 9B:"
        )
        for mid, title, chamber in unmapped_roles:
            print(f"     - {mid}: {title} ({chamber})")
        print("   (These roles exist but have no statutory stipend basis)")
    output_file = output_dir / "roles.json"
    output_data = {"session_id": session_id, "roles": all_role_entries}
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with output_file.open("w", encoding="utf-8") as f:
        json.dump(output_data, f, indent=2)
    print(f"\n" + "=" * 60)
    print(f"[SUCCESS] Wrote {len(all_role_entries)} total roles to {output_file}")
    print(f"  - Committee roles: {len(all_role_entries) - leadership_count}")
    print(f"  - Leadership roles: {leadership_count}")
    print("=" * 60)


if __name__ == "__main__":
    main()
