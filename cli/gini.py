"""CLI entry point"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np

from audit.provenance import ap_sum
from data.session_loader import load_session
from models.rules_9b import select_paid_roles_for_member
from validators import (
    validate_role_catalog,
    validate_session_data,
)


def gini_coefficient(values: list[int]) -> float:
    """Calculates Gini coefficient for a list of values."""
    sorted_values = np.sort(values)  # Sort the values in ascending order
    n = len(sorted_values)
    cumulative_sum = np.cumsum(sorted_values)
    gini = (n + 1 - 2 * (np.sum(cumulative_sum) / cumulative_sum[-1])) / n
    return gini


def main() -> None:
    """Prints errors, warnings, and full committee data, and calculates Gini coefficient."""
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
    if any(str(i.level) == "ERROR" for i in catalog_issues + session_issues):
        print("Errors detected; aborting computation.")
        return
    session = loaded.session
    print(f"Session {session.id} ({session.start_year}-{session.end_year})")
    stipends = []
    for member in loaded.members.values():
        selection = select_paid_roles_for_member(member, session)
        stipend = ap_sum(rs.amount for rs in selection.paid_roles)
        stipends.append(stipend.value)
    gini = gini_coefficient(stipends)
    print(f"\nGini coefficient for stipends: {gini:.4f}")


if __name__ == "__main__":
    main()
