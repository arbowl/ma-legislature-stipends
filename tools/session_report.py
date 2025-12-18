"""Generate session report outputs"""

from __future__ import annotations

from datetime import datetime
from statistics import median
from typing import Any

from data.session_loader import LoadedSession
from models.total_comp import total_comp_for_member
from tools.models import SessionReport, SessionSummaryStats
from validators import (
    validate_role_catalog,
    validate_session_data,
    validate_distance_margins,
)


def generate_session_report(loaded: LoadedSession) -> SessionReport:
    """Generate a comprehensive session report"""
    session = loaded.session
    all_results = []
    for member in loaded.members.values():
        comp_result = total_comp_for_member(member, session)
        all_results.append(
            {
                "member_id": member.member_id,
                "name": member.name,
                "chamber": member.chamber.value,
                "party": member.party.value,
                "base_salary": comp_result.components[0].amount.value,
                "stipends_9b": comp_result.components[1].amount.value,
                "travel_9c": comp_result.components[2].amount.value,
                "total": comp_result.total.value,
                "distance_miles": member.distance_miles_from_state_house,
            }
        )
    summary = _generate_summary_stats(session.id, all_results)
    catalog_issues = validate_role_catalog()
    session_issues = validate_session_data(loaded)
    distance_issues = validate_distance_margins(loaded)
    validation_summary = {
        "catalog_errors": len([i for i in catalog_issues if str(i.level) == "ERROR"]),
        "catalog_warnings": len(
            [i for i in catalog_issues if str(i.level) == "WARNING"]
        ),
        "session_errors": len([i for i in session_issues if str(i.level) == "ERROR"]),
        "session_warnings": len(
            [i for i in session_issues if str(i.level) == "WARNING"]
        ),
        "distance_errors": len([i for i in distance_issues if str(i.level) == "ERROR"]),
        "distance_warnings": len(
            [i for i in distance_issues if str(i.level) == "WARNING"]
        ),
        "all_issues": [
            {
                "level": str(issue.level),
                "code": issue.code,
                "message": issue.message,
                "context": issue.context,
            }
            for issue in catalog_issues + session_issues + distance_issues
        ],
    }
    report = SessionReport(
        session_id=session.id,
        session_label=session.label,
        start_year=session.start_year,
        end_year=session.end_year,
        generated_at=datetime.utcnow().isoformat() + "Z",
        members=all_results,
        summary_statistics=summary.to_dict(),
        validation_summary=validation_summary,
    )
    return report


def _generate_summary_stats(
    session_id: str, results: list[dict[str, Any]]
) -> SessionSummaryStats:
    """Generate summary statistics from results"""
    total_comp = sum(r["total"] for r in results)
    totals = [r["total"] for r in results]
    by_chamber = {}
    for chamber in ["house", "senate"]:
        chamber_results = [r for r in results if r["chamber"] == chamber]
        if chamber_results:
            chamber_total = sum(r["total"] for r in chamber_results)
            by_chamber[chamber] = {
                "count": len(chamber_results),
                "total_compensation": chamber_total,
                "average_compensation": chamber_total / len(chamber_results),
                "median_compensation": median([r["total"] for r in chamber_results]),
            }
    by_party = {}
    for party in set(r["party"] for r in results):
        party_results = [r for r in results if r["party"] == party]
        if party_results:
            party_total = sum(r["total"] for r in party_results)
            by_party[party] = {
                "count": len(party_results),
                "total_compensation": party_total,
                "average_compensation": party_total / len(party_results),
            }
    stipend_distribution = {
        "0_stipends": len([r for r in results if r["stipends_9b"] == 0]),
        "1_or_more_stipends": len([r for r in results if r["stipends_9b"] > 0]),
    }
    top_10 = sorted(results, key=lambda x: x["total"], reverse=True)[:10]
    top_earners = [
        {
            "rank": i + 1,
            "member_id": r["member_id"],
            "name": r["name"],
            "chamber": r["chamber"],
            "total": r["total"],
        }
        for i, r in enumerate(top_10)
    ]
    return SessionSummaryStats(
        session_id=session_id,
        total_members=len(results),
        total_compensation=total_comp,
        average_compensation=total_comp / len(results) if results else 0,
        median_compensation=median(totals) if totals else 0,
        by_chamber=by_chamber,
        by_party=by_party,
        stipend_distribution=stipend_distribution,
        top_earners=top_earners,
    )
