from pathlib import Path

from data.session_loader import load_session
from models.total_comp import total_comp_for_member, CompLabels
from validators import validate_role_catalog, validate_session_data


def test_demo_session_totals():
    data_root = Path("data/sessions")
    session_id = "0-1"
    loaded = load_session(data_root, session_id)
    catalog_issues = validate_role_catalog()
    session_issues = validate_session_data(loaded)
    assert not any(i.level == "ERROR" for i in catalog_issues + session_issues)
    session = loaded.session
    results = {
        m_id: total_comp_for_member(member, session)
        for m_id, member in loaded.members.items()
    }
    assert results["H001"].total.value == 170_000
    assert results["H002"].total.value == 130_000
    assert results["H003"].total.value == 90_000
    assert results["H004"].total.value == 160_000
    alice_components = {c.label: c.amount.value for c in results["H001"].components}
    assert alice_components[CompLabels.base_salary] == 75_000
    assert alice_components[CompLabels.stipends_9b] == 80_000
    assert alice_components[CompLabels.travel_9c] == 15_000
