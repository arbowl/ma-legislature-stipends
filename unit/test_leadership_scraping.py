"""Tests for leadership scraping and normalization"""

import json
from pathlib import Path
from unittest.mock import Mock
from unittest.mock import patch

import pytest
from bs4 import BeautifulSoup

from ingest.members import _infer_chamber_from_section
from ingest.members import _parse_leadership_entry
from ingest.members import _parse_top_level_leader
from ingest.members import scrape_leadership
from ingest.types import RawLeadershipRole
from scripts.normalize_leadership import normalize_leadership_title


@pytest.fixture
def mock_senate_president_html():
    """HTML for top-level Senate President"""
    return """
    <div class="col-sm-12 col-md-6">
        <h2>Senate</h2>
        <div class="leadershipImageWrapper headshotWrapper-lg">
            <a href="/Legislators/Profile/KES0">
                <img src="/images/KES0.jpg" alt="Karen E. Spilka">
            </a>
        </div>
        <h3 class="leadershipName">
            <a href="/Legislators/Profile/KES0">Karen E. Spilka</a>
        </h3>
        <span class="leadershipRole">President of the Senate</span>
        <span class="leadershipDistrict">Middlesex and Norfolk (D)</span>
    </div>
    """


@pytest.fixture
def mock_speaker_html():
    """HTML for top-level Speaker of the House"""
    return """
    <div class="col-sm-12 col-md-6">
        <h2>House of Representatives</h2>
        <div class="leadershipImageWrapper headshotWrapper-lg">
            <a href="/Legislators/Profile/R_M1">
                <img src="/images/R_M1.jpg" alt="Ronald Mariano">
            </a>
        </div>
        <h3 class="leadershipName">
            <a href="/Legislators/Profile/R_M1">Ronald Mariano</a>
        </h3>
        <span class="leadershipRole">Speaker of the House</span>
        <span class="leadershipDistrict">Quincy (D)</span>
    </div>
    """


@pytest.fixture
def mock_leadership_list_entry_html():
    """HTML for a list-based leadership entry"""
    return """
    <li>
        <a href="#"><span class="fa fa-star"></span></a>
        <a href="/Legislators/Profile/CSC0">
            <img src="/images/CSC0.jpg" alt="Cynthia Stone Creem">
        </a>
        <div>
            <h3 class="leadershipName">
                <a href="/Legislators/Profile/CSC0">Cynthia Stone Creem</a>
            </h3>
            <span class="leadershipRole">Majority Leader</span>
            <span class="leadershipDistrict">Norfolk and Middlesex (D)</span>
        </div>
    </li>
    """


@pytest.fixture
def raw_leadership_2025_2026():
    """Load the actual raw leadership data for 2025-2026"""
    raw_file = Path("data/raw/2025-2026/leadership_raw.json")
    if not raw_file.exists():
        pytest.skip(f"Raw leadership data not found: {raw_file}")
    with raw_file.open('r', encoding='utf-8') as f:
        return json.load(f)


@pytest.fixture
def session_roles_2025_2026():
    """Load the normalized roles for 2025-2026"""
    roles_file = Path("data/sessions/2025-2026/roles.json")
    if not roles_file.exists():
        pytest.skip(f"Session roles not found: {roles_file}")
    with roles_file.open('r', encoding='utf-8') as f:
        return json.load(f)


@pytest.fixture
def session_members_2025_2026():
    """Load the members for 2025-2026"""
    members_file = Path("data/sessions/2025-2026/members.json")
    if not members_file.exists():
        pytest.skip(f"Session members not found: {members_file}")
    with members_file.open('r', encoding='utf-8') as f:
        return json.load(f)


def test_parse_top_level_leader_senate_president(mock_senate_president_html):
    """Test parsing of Senate President (top-level leader)"""
    soup = BeautifulSoup(mock_senate_president_html, "html.parser")
    section = soup.select_one("div.col-sm-12.col-md-6")
    result = _parse_top_level_leader(section, "senate")
    assert result is not None
    assert result.member_id == "KES0"
    assert result.chamber == "senate"
    assert result.raw_title == "President of the Senate"
    assert result.raw_district_party == "Middlesex and Norfolk (D)"


def test_parse_top_level_leader_speaker(mock_speaker_html):
    """Test parsing of Speaker of the House (top-level leader)"""
    soup = BeautifulSoup(mock_speaker_html, "html.parser")
    section = soup.select_one("div.col-sm-12.col-md-6")
    result = _parse_top_level_leader(section, "house")
    assert result is not None
    assert result.member_id == "R_M1"
    assert result.chamber == "house"
    assert result.raw_title == "Speaker of the House"
    assert result.raw_district_party == "Quincy (D)"


def test_parse_leadership_entry_list_item(mock_leadership_list_entry_html):
    """Test parsing of a list-based leadership entry"""
    soup = BeautifulSoup(mock_leadership_list_entry_html, "html.parser")
    li = soup.select_one("li")
    result = _parse_leadership_entry(li, "senate")
    assert result is not None
    assert result.member_id == "CSC0"
    assert result.chamber == "senate"
    assert result.raw_title == "Majority Leader"
    assert result.raw_district_party == "Norfolk and Middlesex (D)"


def test_infer_chamber_from_section():
    """Test chamber inference from section headers"""
    assert _infer_chamber_from_section("Senate") == "senate"
    assert _infer_chamber_from_section("SENATE") == "senate"
    assert _infer_chamber_from_section("House of Representatives") == "house"
    assert _infer_chamber_from_section("House") == "house"
    assert _infer_chamber_from_section("HOUSE") == "house"
    assert _infer_chamber_from_section("Unknown Section") is None


def test_scrape_leadership_count_2025_2026(raw_leadership_2025_2026):
    """Verify correct count of leadership positions scraped"""
    assert len(raw_leadership_2025_2026) == 28
    senate_count = sum(1 for entry in raw_leadership_2025_2026 if entry["chamber"] == "senate")
    house_count = sum(1 for entry in raw_leadership_2025_2026 if entry["chamber"] == "house")
    assert senate_count == 13
    assert house_count == 15


def test_scrape_leadership_all_have_member_ids(raw_leadership_2025_2026):
    """Ensure no leadership entry has missing member_id"""
    for entry in raw_leadership_2025_2026:
        assert "member_id" in entry
        assert entry["member_id"], f"Empty member_id for entry: {entry}"
        assert len(entry["member_id"]) > 0


def test_scrape_leadership_chamber_assignment(raw_leadership_2025_2026):
    """Verify all entries have valid chamber assignments"""
    for entry in raw_leadership_2025_2026:
        assert entry["chamber"] in ["senate", "house"]


def test_scrape_leadership_senate_positions(raw_leadership_2025_2026):
    """Test specific Senate leadership positions"""
    senate_leaders = [e for e in raw_leadership_2025_2026 if e["chamber"] == "senate"]
    president = next((e for e in senate_leaders if "President of the Senate" in e["raw_title"]), None)
    majority_leader = next((e for e in senate_leaders if e["raw_title"] == "Majority Leader"), None)
    minority_leader = next((e for e in senate_leaders if e["raw_title"] == "Minority Leader"), None)
    assert president is not None
    assert president["member_id"] == "KES0"
    assert majority_leader is not None
    assert majority_leader["member_id"] == "CSC0"
    assert minority_leader is not None
    assert minority_leader["member_id"] == "BET0"


def test_scrape_leadership_house_positions(raw_leadership_2025_2026):
    """Test specific House leadership positions"""
    house_leaders = [e for e in raw_leadership_2025_2026 if e["chamber"] == "house"]
    speaker = next((e for e in house_leaders if "Speaker of the House" in e["raw_title"]), None)
    majority_leader = next((e for e in house_leaders if e["raw_title"] == "Majority Leader"), None)
    minority_leader = next((e for e in house_leaders if e["raw_title"] == "Minority Leader"), None)
    assert speaker is not None
    assert speaker["member_id"] == "R_M1"
    assert majority_leader is not None
    assert majority_leader["member_id"] == "MJM1"
    assert minority_leader is not None
    assert minority_leader["member_id"] == "BHJ1"


@pytest.mark.parametrize("raw_title,chamber,expected", [
    ("President of the Senate", "senate", "SENATE_PRESIDENT"),
    ("Speaker of the House", "house", "SPEAKER"),
    ("President Pro Tempore", "senate", "SENATE_PRESIDENT_PRO_TEMPORE"),
    ("Speaker Pro Tempore", "house", "HOUSE_SPEAKER_PRO_TEMPORE"),
])
def test_normalize_presiding_officers(raw_title, chamber, expected):
    """Test normalization of presiding officer titles"""
    result = normalize_leadership_title(raw_title, chamber)
    assert result == expected


@pytest.mark.parametrize("raw_title,chamber,expected", [
    ("Majority Leader", "senate", "SENATE_MAJORITY_FLOOR_LEADER"),
    ("Majority Leader", "house", "HOUSE_MAJORITY_FLOOR_LEADER"),
    ("Minority Leader", "senate", "SENATE_MINORITY_FLOOR_LEADER"),
    ("Minority Leader", "house", "HOUSE_MINORITY_FLOOR_LEADER"),
])
def test_normalize_floor_leaders(raw_title, chamber, expected):
    """Test normalization of floor leader titles"""
    result = normalize_leadership_title(raw_title, chamber)
    assert result == expected


@pytest.mark.parametrize("raw_title,chamber,expected", [
    ("Assistant Majority Leader", "senate", "SENATE_MAJORITY_ASSISTANT_FLOOR_LEADER"),
    ("Assistant Majority Leader", "house", "HOUSE_MAJORITY_ASSISTANT_FLOOR_LEADER"),
    ("Second Assistant Majority Leader", "house", "HOUSE_MAJORITY_SECOND_ASSISTANT_FLOOR_LEADER"),
    ("Assistant Minority Leader", "senate", "SENATE_MINORITY_ASSISTANT_FLOOR_LEADER"),
    ("First Assistant Minority Leader", "house", "HOUSE_MINORITY_ASSISTANT_FLOOR_LEADER"),
    ("Second Assistant Minority Leader", "house", "HOUSE_MINORITY_SECOND_ASSISTANT_FLOOR_LEADER"),
    ("Third Assistant Minority Leader", "house", "HOUSE_MINORITY_THIRD_ASSISTANT_FLOOR_LEADER"),
])
def test_normalize_assistant_leaders(raw_title, chamber, expected):
    """Test normalization of assistant leader titles"""
    result = normalize_leadership_title(raw_title, chamber)
    assert result == expected


@pytest.mark.parametrize("raw_title,chamber,expected", [
    ("First Division Chair", "house", "HOUSE_DIVISION_CHAIR_1"),
    ("Second Division Chair", "house", "HOUSE_DIVISION_CHAIR_2"),
    ("Third Division Chair", "house", "HOUSE_DIVISION_CHAIR_3"),
    ("Fourth Division Chair", "house", "HOUSE_DIVISION_CHAIR_4"),
])
def test_normalize_division_chairs(raw_title, chamber, expected):
    """Test normalization of House Division Chair titles"""
    result = normalize_leadership_title(raw_title, chamber)
    assert result == expected


def test_normalize_unmapped_whip_positions():
    """Test that Whip positions are currently unmapped (no statutory stipend basis)"""
    assert normalize_leadership_title("Senate Majority Whip", "senate") is None
    assert normalize_leadership_title("Assistant Majority Whip", "senate") is None


def test_normalize_case_insensitive():
    """Test that normalization is case-insensitive"""
    assert normalize_leadership_title("PRESIDENT OF THE SENATE", "senate") == "SENATE_PRESIDENT"
    assert normalize_leadership_title("president of the senate", "senate") == "SENATE_PRESIDENT"
    assert normalize_leadership_title("PreSiDenT oF ThE SeNaTe", "senate") == "SENATE_PRESIDENT"


def test_normalize_with_extra_whitespace():
    """Test that normalization handles extra whitespace"""
    assert normalize_leadership_title("  Majority Leader  ", "senate") == "SENATE_MAJORITY_FLOOR_LEADER"
    assert normalize_leadership_title("\tSpeaker of the House\n", "house") == "SPEAKER"


def test_normalize_chamber_specific_logic():
    """Test that same title maps differently per chamber"""
    senate_result = normalize_leadership_title("Majority Leader", "senate")
    house_result = normalize_leadership_title("Majority Leader", "house")
    assert senate_result == "SENATE_MAJORITY_FLOOR_LEADER"
    assert house_result == "HOUSE_MAJORITY_FLOOR_LEADER"
    assert senate_result != house_result


def test_normalize_invalid_inputs():
    """Test normalization with invalid inputs"""
    assert normalize_leadership_title("Nonexistent Title", "senate") is None
    assert normalize_leadership_title("Speaker of the House", "senate") is None
    assert normalize_leadership_title("President of the Senate", "house") is None


def test_e2e_all_leadership_members_exist(raw_leadership_2025_2026, session_members_2025_2026):
    """Verify every leadership member exists in the members file"""
    member_ids_in_session = {m["member_id"] for m in session_members_2025_2026["members"]}
    for entry in raw_leadership_2025_2026:
        member_id = entry["member_id"]
        assert member_id in member_ids_in_session, \
            f"Leadership member {member_id} ({entry['raw_title']}) not found in members.json"


def test_e2e_mapped_leadership_roles_in_session(raw_leadership_2025_2026, session_roles_2025_2026):
    """Verify that mappable leadership positions appear in roles.json"""
    member_roles = {}
    for role in session_roles_2025_2026["roles"]:
        member_id = role["member_id"]
        role_code = role["role_code"]
        if member_id not in member_roles:
            member_roles[member_id] = []
        member_roles[member_id].append(role_code)
    unmapped_count = 0
    for entry in raw_leadership_2025_2026:
        member_id = entry["member_id"]
        raw_title = entry["raw_title"]
        chamber = entry["chamber"]
        expected_role_code = normalize_leadership_title(raw_title, chamber)
        if expected_role_code is None:
            unmapped_count += 1
        else:
            assert member_id in member_roles, \
                f"Member {member_id} with leadership role {raw_title} not found in roles.json"
            assert expected_role_code in member_roles[member_id], \
                f"Role {expected_role_code} for {member_id} ({raw_title}) not found in roles.json"
    assert unmapped_count == 2, f"Expected 2 unmapped positions (Whips), got {unmapped_count}"


def test_e2e_specific_members_2025_2026(session_roles_2025_2026):
    """Test specific key leadership members have correct roles"""
    member_roles = {}
    for role in session_roles_2025_2026["roles"]:
        member_id = role["member_id"]
        role_code = role["role_code"]
        if member_id not in member_roles:
            member_roles[member_id] = []
        member_roles[member_id].append(role_code)
    test_cases = [
        ("KES0", "SENATE_PRESIDENT", "Karen E. Spilka"),
        ("R_M1", "SPEAKER", "Ronald Mariano"),
        ("CSC0", "SENATE_MAJORITY_FLOOR_LEADER", "Cynthia Stone Creem"),
        ("MJM1", "HOUSE_MAJORITY_FLOOR_LEADER", "Michael J. Moran"),
        ("WNB0", "SENATE_PRESIDENT_PRO_TEMPORE", "William N. Brownsberger"),
        ("K_H1", "HOUSE_SPEAKER_PRO_TEMPORE", "Kate Hogan"),
        ("BET0", "SENATE_MINORITY_FLOOR_LEADER", "Bruce E. Tarr"),
        ("BHJ1", "HOUSE_MINORITY_FLOOR_LEADER", "Bradley H. Jones, Jr."),
    ]
    for member_id, expected_role, name in test_cases:
        assert member_id in member_roles, f"{name} ({member_id}) not found in roles"
        assert expected_role in member_roles[member_id], \
            f"{name} ({member_id}) missing role {expected_role}"


def test_e2e_division_chairs_2025_2026(session_roles_2025_2026):
    """Test that all four House Division Chairs are properly mapped"""
    member_roles = {}
    for role in session_roles_2025_2026["roles"]:
        member_id = role["member_id"]
        role_code = role["role_code"]
        if member_id not in member_roles:
            member_roles[member_id] = []
        member_roles[member_id].append(role_code)
    division_chairs = [
        ("DWG1", "HOUSE_DIVISION_CHAIR_1", "Danielle W. Gregoire"),
        ("JNR1", "HOUSE_DIVISION_CHAIR_2", "Jeffrey N. Roy"),
        ("C_G1", "HOUSE_DIVISION_CHAIR_3", "Carlos Gonzalez"),
        ("JJO1", "HOUSE_DIVISION_CHAIR_4", "James J. O'Day"),
    ]
    for member_id, expected_role, name in division_chairs:
        assert member_id in member_roles, f"Division Chair {name} ({member_id}) not found"
        assert expected_role in member_roles[member_id], \
            f"Division Chair {name} ({member_id}) missing role {expected_role}"


def test_e2e_unmapped_roles_documented(raw_leadership_2025_2026):
    """Document the unmapped leadership positions for 2025-2026"""
    unmapped = []
    for entry in raw_leadership_2025_2026:
        raw_title = entry["raw_title"]
        chamber = entry["chamber"]
        member_id = entry["member_id"]
        if normalize_leadership_title(raw_title, chamber) is None:
            unmapped.append((member_id, raw_title, chamber))
    expected_unmapped = [
        ("MFR0", "Senate Majority Whip", "senate"),
        ("JAC0", "Assistant Majority Whip", "senate"),
    ]
    assert len(unmapped) == len(expected_unmapped), \
        f"Expected {len(expected_unmapped)} unmapped roles, got {len(unmapped)}: {unmapped}"
    for expected in expected_unmapped:
        assert expected in unmapped, f"Expected unmapped role not found: {expected}"


def test_no_duplicate_exact_titles_per_member(raw_leadership_2025_2026):
    """Ensure no member has duplicate exact role titles"""
    member_titles = {}
    for entry in raw_leadership_2025_2026:
        member_id = entry["member_id"]
        raw_title = entry["raw_title"]
        if member_id not in member_titles:
            member_titles[member_id] = []
        assert raw_title not in member_titles[member_id], \
            f"Duplicate title '{raw_title}' for member {member_id}"
        member_titles[member_id].append(raw_title)


def test_leadership_party_consistency_2025_2026(raw_leadership_2025_2026):
    """Verify majority leaders are Democrats and minority leaders are Republicans"""
    for entry in raw_leadership_2025_2026:
        raw_title = entry["raw_title"]
        district_party = entry["raw_district_party"]
        if "(" in district_party and ")" in district_party:
            party = district_party.split("(")[-1].split(")")[0].strip()
            if "Majority" in raw_title:
                assert party == "D", \
                    f"Majority leader should be Democrat, got {party} for {entry['member_id']}"
            elif "Minority" in raw_title:
                assert party == "R", \
                    f"Minority leader should be Republican, got {party} for {entry['member_id']}"


def test_senate_has_exactly_one_president(raw_leadership_2025_2026):
    """Verify exactly one Senate President"""
    presidents = [e for e in raw_leadership_2025_2026
                  if e["chamber"] == "senate" and "President of the Senate" in e["raw_title"]]
    assert len(presidents) == 1, f"Expected 1 Senate President, got {len(presidents)}"


def test_house_has_exactly_one_speaker(raw_leadership_2025_2026):
    """Verify exactly one Speaker of the House"""
    speakers = [e for e in raw_leadership_2025_2026
                if e["chamber"] == "house" and "Speaker of the House" in e["raw_title"]]
    assert len(speakers) == 1, f"Expected 1 Speaker, got {len(speakers)}"


def test_all_leadership_have_district_info(raw_leadership_2025_2026):
    """Verify all leadership entries have district information"""
    for entry in raw_leadership_2025_2026:
        assert "raw_district_party" in entry
        assert entry["raw_district_party"], \
            f"Missing district info for {entry['member_id']} ({entry['raw_title']})"
