"""Generate member profile outputs"""

from __future__ import annotations

import json
from pathlib import Path
import re

from audit.provenance import SourceRef
from config.comp_adjustment import (
    load_stipend_adjustment,
    load_travel_adjustment,
)
from config.role_catalog import get_role_definition
from models.core import Member, Session
from models.rules_9b import (
    select_paid_roles_for_member,
    raw_role_stipends_for_member,
)
from models.rules_9c import travel_9c_for_member
from models.total_comp import CompLabels, total_comp_for_member
from tools.models import (
    CompensationComponent,
    MemberProfile,
    ProvenanceInfo,
    RoleStipendInfo,
)
from validators import _validate_member_raw_roles


def _extract_provenance(sources: frozenset) -> list[dict]:
    """Extract provenance from a frozenset of sources"""
    all_sources = []

    def extract_recursive(item: SourceRef | frozenset) -> None:
        """Extracts all sources from a list"""
        if isinstance(item, frozenset):
            for sub_item in item:
                extract_recursive(sub_item)
        elif isinstance(item, SourceRef):
            all_sources.append(item)

    extract_recursive(sources)
    seen = set()
    unique_sources = []
    for source in all_sources:
        if hasattr(source, "id") and source.id not in seen:
            seen.add(source.id)
            unique_sources.append(ProvenanceInfo.from_source_ref(source).to_dict())
    return unique_sources


def generate_member_profile(
    member: Member, session: Session, session_id: str
) -> MemberProfile:
    """Generate a complete member profile with full provenance"""
    comp_result = total_comp_for_member(member, session)
    selection = select_paid_roles_for_member(member, session)
    raw_stipends = raw_role_stipends_for_member(member, session)
    stipends_breakdown = []
    paid_roles_list = list(selection.paid_roles)
    adjustment_factor = load_stipend_adjustment(session.id).factor
    for rs in raw_stipends:
        role_def = get_role_definition(rs.role_code)
        base_amt = rs.amount.value
        if adjustment_factor != 1.0:
            base_amt = round(rs.amount.value / adjustment_factor)
        is_paid = False
        for i, paid_rs in enumerate(paid_roles_list):
            if (
                paid_rs.role_code == rs.role_code
                and paid_rs.amount.value == rs.amount.value
            ):
                is_paid = True
                paid_roles_list.pop(i)
                break
        stipends_breakdown.append(
            RoleStipendInfo(
                role_code=rs.role_code,
                role_title=role_def.title,
                tier_id=role_def.stipend_tier_id,
                base_amount=base_amt,
                adjusted_amount=rs.amount.value,
                adjustment_factor=adjustment_factor,
                paid=is_paid,
                reason=rs.reason,
                provenance=_extract_provenance(rs.amount.sources),
            ).to_dict()
        )
    stipends_breakdown.sort(key=lambda x: (not x["paid"], -x["adjusted_amount"]))
    components = []
    for comp in comp_result.components:
        prov = _extract_provenance(comp.amount.sources)
        comp_dict = CompensationComponent(
            label=comp.label, amount=comp.amount.value, provenance=prov
        ).to_dict()
        if comp.label == CompLabels.base_salary:
            base_salary_data = json.loads(
                (Path("data/sessions") / session.id / "base_salary.json").read_text()
            )
            original_base = 62548
            comp_dict["details"] = {
                "base_amount": original_base,
                "adjustment_factor": base_salary_data.get(
                    "aggregate_change_factor", 1.0
                ),
            }
        if comp.label == CompLabels.stipends_9b:
            discarded = len(raw_stipends) - len(selection.paid_roles)
            comp_dict["details"] = {
                "breakdown": stipends_breakdown,
                "total_roles": len(raw_stipends),
                "paid_roles": len(selection.paid_roles),
                "discarded_roles": discarded,
            }
        if comp.label == CompLabels.travel_9c:
            travel_result = travel_9c_for_member(member, session)
            travel_adj = load_travel_adjustment(session.id)
            match = re.search(r"\$([0-9,]+)", travel_result.rule_applied)
            base_amount = (
                int(match.group(1).replace(",", "")) if match else comp.amount.value
            )
            comp_dict["details"] = {
                "distance_miles": member.distance_miles_from_state_house,
                "calculation": travel_result.rule_applied,
                "base_amount": base_amount,
                "adjustment_factor": travel_adj.factor,
            }
        components.append(comp_dict)
    issues = _validate_member_raw_roles(member, session_id)
    validation_issues = [
        {
            "level": str(issue.level),
            "code": issue.code,
            "message": issue.message,
            "context": issue.context,
        }
        for issue in issues
    ]
    profile = MemberProfile(
        member_id=member.member_id,
        name=member.name,
        chamber=member.chamber.value,
        party=member.party.value,
        district=member.district,
        distance_from_state_house=member.distance_miles_from_state_house,
        session_id=session_id,
        compensation={"total": comp_result.total.value, "components": components},
        validation_issues=validation_issues,
        raw_data_sources={
            "member_data": f"data/sessions/{session_id}/members.json",
            "role_assignments": f"data/sessions/{session_id}/roles.json",
            "distances": f"data/sessions/{session_id}/distances.json",
        },
    )
    return profile
