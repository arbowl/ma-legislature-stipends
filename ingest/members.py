"""Scrapers"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Literal, Final, Optional
from urllib.parse import urljoin

from bs4 import BeautifulSoup

from ingest.common import get_soup
from ingest.types import RawMember, RawLeadershipRole, to_dict_list


BASE_URL: Final = "https://malegislature.gov"
ChamberStr = Literal["house", "senate"]
MEMBERS_PATHS: dict[ChamberStr, str] = {
    "senate": "/Legislators/Members/Senate",
    "house": "/Legislators/Members/House",
}
LEADERSHIP_PATH = "/Legislators/Leadership"


def _party_to_code(text: str) -> Optional[str]:
    t = text.strip().lower()
    if t.startswith("democrat"):
        return "D"
    if t.startswith("republican"):
        return "R"
    return None


def _parse_member_row(tr: BeautifulSoup, chamber: ChamberStr) -> Optional[RawMember]:
    tds = tr.find_all("td")
    if len(tds) < 6:
        return None
    picture_link = tr.select_one("td.pictureCol a[href*='/Legislators/Profile/']")
    if not picture_link:
        return None
    profile_path = picture_link.get("href", "").strip()
    if not profile_path:
        return None
    parts = profile_path.split("/")
    member_id = parts[-1].split("?", 1)[0]
    first_name = tds[2].get_text(strip=True)
    last_name = tds[3].get_text(strip=True)
    name = f"{first_name} {last_name}".strip()
    district_text = tds[4].get_text(strip=True)
    party_text = tds[5].get_text(strip=True)
    party = _party_to_code(party_text)
    profile_url = urljoin(BASE_URL, profile_path)
    return RawMember(
        member_id=member_id,
        name=name,
        chamber=chamber,
        raw_district=district_text,
        party=party,
        profile_url=profile_url,
    )


def scrape_members_for_chamber(chamber: ChamberStr) -> list[RawMember]:
    """Scrapes members for a given chamber"""
    path = MEMBERS_PATHS[chamber]
    soup = get_soup(path)
    table = soup.find("table")
    if not table:
        return []
    tbody = table.find("tbody")
    rows = tbody.find_all("tr") if tbody else table.find_all("tr")
    members: list[RawMember] = []
    for tr in rows:
        rm = _parse_member_row(tr, chamber)
        if rm is not None:
            members.append(rm)
    return members


def scrape_all_members() -> list[RawMember]:
    """Gets all members from both chambers"""
    out: list[RawMember] = []
    for chamber in ("senate", "house"):
        out.extend(scrape_members_for_chamber(chamber))
    return out


def _infer_chamber_from_section(header_text: str) -> Optional[ChamberStr]:
    """Gets chamber from element"""
    t = header_text.lower()
    if "senate" in t:
        return "senate"
    if "house" in t:
        return "house"
    return None


def _parse_top_level_leader(
    section: BeautifulSoup, chamber: ChamberStr
) -> Optional[RawLeadershipRole]:
    """
    Parse the top-level leader (Senate President or Speaker of House).

    Example block:
    <div class="leadershipImageWrapper headshotWrapper-lg">
        <a href="/Legislators/Profile/KES0">
            <img src="..." alt="Karen E. Spilka">
        </a>
        ...
    </div>
    <h3 class="leadershipName">
        <a href="/Legislators/Profile/KES0">Karen E. Spilka</a>
    </h3>
    <span class="leadershipRole">President of the Senate</span>
    <span class="leadershipDistrict">Middlesex and Norfolk (D)</span>
    """
    img_wrapper = section.select_one("div.leadershipImageWrapper.headshotWrapper-lg")
    if not img_wrapper:
        return None
    profile_link = img_wrapper.select_one("a[href*='/Legislators/Profile/']")
    if not profile_link:
        return None
    profile_path = profile_link.get("href", "").strip()
    if not profile_path:
        return None
    parts = profile_path.split("/")
    member_id = parts[-1].split("?", 1)[0]
    role_el = section.select_one("span.leadershipRole")
    raw_title = role_el.get_text(strip=True) if role_el else ""
    district_el = section.select_one("span.leadershipDistrict")
    raw_district_party = district_el.get_text(strip=True) if district_el else ""
    return RawLeadershipRole(
        member_id=member_id,
        chamber=chamber,
        raw_title=raw_title,
        raw_district_party=raw_district_party,
    )


def _parse_leadership_entry(
    li: BeautifulSoup, chamber: ChamberStr
) -> Optional[RawLeadershipRole]:
    """
    Example block:

    <li>
      <a ...><span class="fa fa-star"></span></a>
      <a href="/Legislators/Profile/CSC0">
        <img ...>
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
    name_link = li.select_one("h3.leadershipName a[href*='/Legislators/Profile/']")
    if not name_link:
        return None
    profile_path = name_link.get("href", "").strip()
    if not profile_path:
        return None
    parts = profile_path.split("/")
    member_id = parts[-1].split("?", 1)[0]
    role_el = li.select_one("span.leadershipRole")
    raw_title = role_el.get_text(strip=True) if role_el else ""
    district_el = li.select_one("span.leadershipDistrict")
    raw_district_party = district_el.get_text(strip=True) if district_el else ""
    return RawLeadershipRole(
        member_id=member_id,
        chamber=chamber,
        raw_title=raw_title,
        raw_district_party=raw_district_party,
    )


def scrape_leadership() -> list[RawLeadershipRole]:
    """Gets leadership card from page"""
    soup = get_soup(LEADERSHIP_PATH)
    roles: list[RawLeadershipRole] = []
    for col in soup.select("div.col-sm-12.col-md-6"):
        h2 = col.select_one("h2")
        if not h2:
            continue
        chamber = _infer_chamber_from_section(h2.get_text(strip=True))
        if chamber is None:
            continue
        top_leader = _parse_top_level_leader(col, chamber)
        if top_leader:
            roles.append(top_leader)
        ul = col.select_one("ul.leadershipList")
        if ul:
            for li in ul.find_all("li", recursive=False):
                rl = _parse_leadership_entry(li, chamber)
                if rl is not None:
                    roles.append(rl)
    return roles


def dump_members_raw(session_id: str, out_root: Path = Path("data/raw")) -> Path:
    """Dumps raw members to JSON"""
    members = scrape_all_members()
    out_dir = out_root / session_id
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "members_raw.json"
    out_path.write_text(json.dumps(to_dict_list(members), indent=2), encoding="utf-8")
    return out_path


def dump_leadership_raw(session_id: str, out_root: Path = Path("data/raw")) -> Path:
    """Dumps raw leadership to JSON"""
    roles = scrape_leadership()
    out_dir = out_root / session_id
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "leadership_raw.json"
    out_path.write_text(json.dumps(to_dict_list(roles), indent=2), encoding="utf-8")
    return out_path


def main() -> None:
    """Generates raw member and leadership JSONs"""
    parser = argparse.ArgumentParser(
        description="Scrape MA Legislature raw member & leadership data."
    )
    parser.add_argument(
        "--session-id",
        default="2025-2026",
        help="Session identifier to use for output directory (default: 2025-2026)",
    )
    parser.add_argument(
        "--out-root",
        default="data/raw",
        help="Root directory for raw JSON outputs (default: data/raw)",
    )
    args = parser.parse_args()
    out_root = Path(args.out_root)
    m_path = dump_members_raw(args.session_id, out_root=out_root)
    print(f"wrote members_raw.json to {m_path}")
    l_path = dump_leadership_raw(args.session_id, out_root=out_root)
    print(f"wrote leadership_raw.json to {l_path}")


if __name__ == "__main__":
    main()
