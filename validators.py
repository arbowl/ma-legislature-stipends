"""Validators"""

from __future__ import annotations

from pathlib import Path

from audit.issues import AuditIssue
from config.role_catalog import ROLE_DEFINITIONS, RoleDefinition, get_role_definition
from config.stipend_tiers import STIPEND_TIERS
from data.session_loader import LoadedSession
from models.core import CommitteeRoleType, Member


def _validate_member_raw_roles(member: Member, session_id: str) -> list[AuditIssue]:
    """Check per-member invariants on the raw role data"""
    issues: list[AuditIssue] = []
    role_defs: list[RoleDefinition] = []
    for ra in member.roles:
        if ra.session_id != session_id:
            continue
        try:
            role_defs.append(get_role_definition(ra.role_code))
        except KeyError:
            continue
    chair_roles = [
        rd for rd in role_defs if rd.committee_role_type == CommitteeRoleType.CHAIR
    ]
    stipend_roles = [rd for rd in role_defs if rd.stipend_tier_id is not None]
    if len(chair_roles) > 1:
        issues.append(
            AuditIssue.warning(
                code="MULTIPLE_CHAIR_ROLES_RAW",
                message=(
                    f"Member {member.member_id} has {len(chair_roles)} "
                    f"chair roles in raw data; 9B(f) only allows one paid "
                    "chair, so one or more may be discarded."
                ),
                member_id=member.member_id,
                session_id=session_id,
                chair_role_codes=[rd.code for rd in chair_roles],
            )
        )
    if len(stipend_roles) > 2:
        issues.append(
            AuditIssue.warning(
                code="MORE_THAN_TWO_STIPEND_ROLES_RAW",
                message=(
                    f"Member {member.member_id} has {len(stipend_roles)} "
                    "stipend-bearing roles; 9B(f) only allows two paid "
                    "positions by default."
                ),
                member_id=member.member_id,
                session_id=session_id,
                stipend_role_codes=[rd.code for rd in stipend_roles],
            )
        )
    return issues


def validate_role_catalog() -> list[AuditIssue]:
    """Validates the role catalog"""
    issues: list[AuditIssue] = []
    for code, rd in ROLE_DEFINITIONS.items():
        if rd.stipend_tier_id is not None and rd.stipend_tier_id not in STIPEND_TIERS:
            issues.append(
                AuditIssue.error(
                    code="UNKNOWN_STIPEND_TIER",
                    message=(
                        f"Role {code} references unknown stipend_tier_id "
                        f"{rd.stipend_tier_id}",
                    ),
                    role_code=code,
                    stipend_tier_id=rd.stipend_tier_id,
                )
            )
    title_to_codes: dict[str, list[str]] = {}
    for code, rd in ROLE_DEFINITIONS.items():
        title_to_codes.setdefault(rd.title, []).append(code)
    for title, codes in title_to_codes.items():
        if len(codes) > 1:
            issues.append(
                AuditIssue.warning(
                    code="DUPLICATE_ROLE_TITLE",
                    message=(f"Title {title!r} used for multiple role codes {codes}"),
                    title=title,
                    role_codes=codes,
                )
            )
    return issues


def validate_session_data(loaded: LoadedSession) -> list[AuditIssue]:
    """Validates a session at the data level"""
    issues: list[AuditIssue] = []
    for ra in loaded.role_assignments:
        if ra.role_code not in ROLE_DEFINITIONS:
            issues.append(
                AuditIssue.error(
                    code="UNKNOWN_ROLE_CODE",
                    message=(f"RoleAssignment has unknown role_code {ra.role_code}"),
                    role_code=ra.role_code,
                    session_id=ra.session_id,
                )
            )
    if any(str(i.level) == "ERROR" and i.code == "UNKNOWN_ROLE_CODE" for i in issues):
        return issues
    for member in loaded.members.values():
        issues.extend(_validate_member_raw_roles(member, loaded.session.id))
    return issues


def main() -> None:
    """Runs the validators for debugging purposes"""
    # pylint: disable = import-outside-toplevel
    # This is for quick validation, but we don't want to create a dependency.
    from data.session_loader import load_session

    loaded = load_session(Path("data/sessions"), "2025-2026")
    print([i for i in validate_role_catalog() if str(i.level) == "ERROR"])
    print([i for i in validate_session_data(loaded) if str(i.level) == "ERROR"])


if __name__ == "__main__":
    main()
