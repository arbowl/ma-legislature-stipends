"""Validators"""

from __future__ import annotations

from audit.issues import AuditIssue
from config.role_catalog import ROLE_DEFINITIONS, get_role_definition
from config.stipend_tiers import STIPEND_TIERS
from data.session_loader import LoadedSession
from models.core import CommitteeRoleType, Member


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
                    message=(
                        f"Title {title!r} used for multiple role codes {codes}"
                    ),
                    title=title,
                    role_codes=codes,
                )
            )
    return issues
