"""Scrape committee roles"""

from __future__ import annotations

from dataclasses import dataclass, asdict
import json
from pathlib import Path
from time import sleep
from typing import Optional

from bs4 import BeautifulSoup

from ingest.common import get_soup


@dataclass
class RawCommitteeRole:
    member_id: str
    session_id: str
    committee_external_id: str
    committee_name: str
    raw_role_label: Optional[str]


def _extract_committee_id_from_href(href: str) -> str:
    """Example href: "/Committees/Detail/S51/Committees"
    We want: "S51"
    """
    parts = href.strip("/").split("/")
    if len(parts) >= 3:
        return parts[2]
    return ""


def _extract_role_label(li: BeautifulSoup) -> Optional[str]:
    """Committee role label appears as:
      <span>Chairperson, </span>
      <span>Vice Chair, </span>
      <span>Member, </span>  (rare)
    or no prefix = plain member
    """
    span = li.find("span")
    if not span:
        return None
    text = span.get_text(strip=True).rstrip(",")
    if text:
        return text
    return None


def _extract_committee_name_and_id(li: BeautifulSoup) -> tuple[str, str]:
    """Finds the <a> inside the <li> and extracts:
      - committee_name (link text)
      - committee_external_id (derived from href)
    """
    a = li.find("a", href=True)
    if not a:
        return ("", "")
    name = a.get_text(strip=True)
    committee_id = _extract_committee_id_from_href(a["href"])
    return name, committee_id


def scrape_committees_for_member(
    member_id: str, session_id: str
) -> list[RawCommitteeRole]:
    """Scrape `/Legislators/Profile/<ID>/Committees` for ONE member.
    The page has a session-select dropdown; we must select the correct session.

    Strategy:
    - Load the page
    - Find the session dropdown <select>
    - Select the <option> whose text contains session_id (e.g. "194th")
    - Extract all <li> entries under that selection
    """
    path = f"/Legislators/Profile/{member_id}/Committees"
    soup = get_soup(path)
    select = soup.find("select")
    selected_value = None
    if select:
        for option in select.find_all("option"):
            text = option.get_text(strip=True)
            if session_id in text:
                selected_value = option.get("value")
                break
    if selected_value:
        page_url = f"{path}?sessionId={selected_value}"
        soup = get_soup(page_url)
    roles: list[RawCommitteeRole] = []
    ul = soup.find("ul")
    if not ul:
        return roles
    for li in ul.find_all("li", recursive=False):
        committee_name, committee_id = _extract_committee_name_and_id(li)
        raw_role_label = _extract_role_label(li)
        if committee_id:
            roles.append(
                RawCommitteeRole(
                    member_id=member_id,
                    session_id=session_id,
                    committee_external_id=committee_id,
                    committee_name=committee_name,
                    raw_role_label=raw_role_label,
                )
            )
    return roles


def dump_committees_raw(
    session_id: str,
    member_ids: list[str],
    out_root: Path = Path("data/raw"),
) -> Path:
    """Scrape committees for ALL members and write JSON file.
    """
    out_dir = out_root / session_id
    out_dir.mkdir(parents=True, exist_ok=True)
    all_roles: list[dict] = []
    for mid in member_ids:
        roles = scrape_committees_for_member(mid, session_id)
        all_roles.extend(asdict(r) for r in roles)
        sleep(0.25)
    out_path = out_dir / "committee_roles_raw.json"
    out_path.write_text(json.dumps(all_roles, indent=2), encoding="utf-8")
    return out_path


def main() -> None:
    """Generates the raw committee JSON"""
    members_raw = json.loads(
        Path("data/raw/194th/members_raw.json"
    ).read_text())
    member_ids = [m["member_id"] for m in members_raw]
    dump_committees_raw("194th", member_ids)


if __name__ == "__main__":
    main()
