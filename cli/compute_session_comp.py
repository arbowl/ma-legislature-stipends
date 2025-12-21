"""CLI entry point"""

from __future__ import annotations

import argparse
from pathlib import Path

from audit.issues import AuditIssue
from data.session_loader import load_session
from models.total_comp import total_comp_for_member
from validators import (
    validate_role_catalog,
    validate_session_data,
)


def _print_issues(header: str, issues: list[AuditIssue]) -> None:
    """Prints all collected validator issues"""
    if not issues:
        return
    print(header)
    for i in issues:
        ctx_str = ",".join(f"{k}={v}" for k, v in i.context.items())
        print(f"  [{i.level}] {i.code}: {i.message} ({ctx_str})")
    print()


def main() -> None:
    """Prints errors, warnings, and full committee data."""
    parser = argparse.ArgumentParser(
        description="Compute legislative compensation for a session."
    )
    parser.add_argument("session_id", help="Session ID, e.g. 2025-2026")
    parser.add_argument(
        "--data-root",
        default="data/sessions",
        help="Root directory containing session data (default: data/sessions)",
    )
    args = parser.parse_args()
    loaded = load_session(Path(args.data_root), args.session_id)
    catalog_issues = validate_role_catalog()
    session_issues = validate_session_data(loaded)
    _print_issues("Catalog issues:", catalog_issues)
    _print_issues("Session issues:", session_issues)
    if any(str(i.level) == "ERROR" for i in catalog_issues + session_issues):
        print("Errors detected; aborting computation.")
        return
    session = loaded.session
    print(f"Session {session.id} ({session.start_year}-{session.end_year})")
    print()
    print(f"{'Member ID':<10}  {'Name':<25}  {'Total':>10}")
    for member in loaded.members.values():
        res = total_comp_for_member(member, session)
        print(f"{member.member_id:<10}  {member.name:<25}  {res.total.value:>10}")


if __name__ == "__main__":
    main()
