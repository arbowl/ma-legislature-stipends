"""Scrape committee roles"""

from __future__ import annotations

import json
from time import sleep
from dataclasses import dataclass, asdict
from pathlib import Path
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
    if (
        len(parts) >= 3
        and parts[0].lower() == "committees"
        and parts[1].lower() == "detail"
    ):
        return parts[2]
    return ""


def _extract_role_label(li: BeautifulSoup) -> Optional[str]:
    """If the li starts with a <span> like 'Chairperson, ' or 'Vice Chair, ',
    return that word; otherwise None.
    """
    span = li.find("span")
    if not span:
        return None
    text = span.get_text(strip=True).rstrip(",")
    return text or None


def _extract_committee_name_and_id(li: BeautifulSoup) -> tuple[str, str]:
    """Find the first <a> with /Committees/Detail/ in the href."""
    a = li.find("a", href=True)
    if not a:
        return "", ""
    href = a["href"]
    if "/Committees/Detail/" not in href:
        return "", ""
    name = a.get_text(strip=True)
    cid = _extract_committee_id_from_href(href)
    return name, cid


def scrape_committees_for_member(
    member_id: str, session_id: str
) -> list[RawCommitteeRole]:
    """Scrape `/Legislators/Profile/<ID>/Committees` for a single member,
    assuming the default view is the current session (e.g. 194th).
    """
    path = f"/Legislators/Profile/{member_id}/Committees"
    soup = get_soup(path)
    roles: list[RawCommitteeRole] = []
    for li in soup.find_all("li"):
        committee_name, committee_id = _extract_committee_name_and_id(li)
        if not committee_id:
            continue
        raw_role_label = _extract_role_label(li)
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
    """Scrape committees for ALL members and write JSON file."""
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


def dump_committees_raw(
    session_id: str,
    member_ids: list[str],
    out_root: Path = Path("data/raw"),
) -> Path:
    """Scrape committees for ALL members and write JSON file."""
    out_dir = out_root / session_id
    out_dir.mkdir(parents=True, exist_ok=True)
    all_roles: list[dict] = []
    for idx, mid in enumerate(member_ids):
        print(f"{round((idx + 1) / len(member_ids) * 100, 2)}% done")
        roles = scrape_committees_for_member(mid, session_id)
        all_roles.extend(asdict(r) for r in roles)
        sleep(0.25)
    out_path = out_dir / "committee_roles_raw.json"
    out_path.write_text(json.dumps(all_roles, indent=2), encoding="utf-8")
    return out_path


def main() -> None:
    """Generates the raw committee JSON"""
    members_raw = json.loads(Path("data/raw/2025-2026/members_raw.json").read_text())
    member_ids = [m["member_id"] for m in members_raw]
    dump_committees_raw("2025-2026", member_ids)


if __name__ == "__main__":
    main()
