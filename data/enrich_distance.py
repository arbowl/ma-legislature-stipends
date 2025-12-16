"""Use district_centroids.json to inform members.json"""

import argparse
import json
import math
import re
from pathlib import Path
from typing import Any

# Massachusetts State House (24 Beacon St, Boston)
STATE_HOUSE_LAT = 42.3587
STATE_HOUSE_LON = -71.0636

ORDINAL_WORDS: dict[str, int] = {
    "first": 1,
    "second": 2,
    "third": 3,
    "fourth": 4,
    "fifth": 5,
    "sixth": 6,
    "seventh": 7,
    "eighth": 8,
    "ninth": 9,
    "tenth": 10,
    "eleventh": 11,
    "twelfth": 12,
    "thirteenth": 13,
    "fourteenth": 14,
    "fifteenth": 15,
    "sixteenth": 16,
    "seventeenth": 17,
    "eighteenth": 18,
    "nineteenth": 19,
    "twentieth": 20,
    # extend if needed
}

HOUSE_PREFIX_TO_COUNTY: dict[str, str] = {
    "BARN": "barnstable",
    "BDN": "barnstable dukes and nantucket",  # special case in centroid file
    "BERK": "berkshire",
    "BRISTOL": "bristol",
    "ESSEX": "essex",
    "FRANK": "franklin",
    "HAMPDEN": "hampden",
    "HAMPSHIRE": "hampshire",
    "MIDDLE": "middlesex",
    "NORFOLK": "norfolk",
    "PLY": "plymouth",
    "SUFFOLK": "suffolk",
    "WOR": "worcester",
}

COUNTY_TO_PREFIX: dict[str, str] = {v: k for k, v in HOUSE_PREFIX_TO_COUNTY.items()}


def haversine_miles(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Great-circle distance in miles between two lat/lon points."""
    radius_of_earth = 3958.8
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = (
        math.sin(dphi / 2) ** 2
        + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return radius_of_earth * c


def norm_senate_name(name: str) -> str:
    """Normalize senate district names like 'First Suffolk' or
    'Norfolk, Plymouth and Bristol' into a canonical key.
    """
    s = name.lower().strip()
    s = re.sub(r"[,\s]+", " ", s)
    return s


def build_senate_centroid_index(
    centroids: dict[str, Any],
) -> dict[str, tuple[str, tuple[float, float]]]:
    """Returns mapping: normalized_name -> (canonical_name, (lat, lon))"""
    index: dict[str, tuple[str, tuple[float, float]]] = {}
    for name, coords in centroids["Senate"].items():
        norm = norm_senate_name(name)
        index[norm] = (name, (coords[0], coords[1]))
    return index


def parse_house_centroid_key(key: str) -> tuple[str, int]:
    """Convert centroid key like 'SUFFOLK11' or 'MIDDLE02' into
    (county_label, district_number).

    Special case: 'BDN' is treated as '1st Barnstable, Dukes and Nantucket'.
    """
    if key == "BDN":
        return "barnstable dukes and nantucket", 1
    m = re.match(r"^([A-Z]+)(\d+)$", key)
    if not m:
        raise ValueError(f"Unexpected House centroid key: {key}")
    prefix, num_str = m.groups()
    if prefix not in HOUSE_PREFIX_TO_COUNTY:
        raise ValueError(f"Unknown House centroid prefix: {prefix} in key {key}")
    county_label = HOUSE_PREFIX_TO_COUNTY[prefix]
    return county_label, int(num_str)


def parse_house_district_name(name: str) -> tuple[str, int]:
    """Normalize House district names like:
      '11th Suffolk'
      '1st Middlesex'
      'Eleventh Hampden'
      'First Berkshire'
      'Barnstable, Dukes and Nantucket'

    into: (county_label, number), where county_label matches
    HOUSE_PREFIX_TO_COUNTY values.
    """
    raw = name.strip()
    lower = raw.lower()
    if (
        lower == "barnstable, dukes and nantucket"
        or "barnstable, dukes and nantucket" in lower
    ):
        return "barnstable dukes and nantucket", 1
    s = re.sub(r"\bdistrict\b", "", raw, flags=re.IGNORECASE).strip()
    parts = s.split()
    if len(parts) < 2:
        raise ValueError(f"Unexpected house district name format: {name!r}")
    first_token = parts[0]
    m = re.match(r"(\d+)(st|nd|rd|th)?$", first_token.lower())
    if m:
        num = int(m.group(1))
    else:
        num = ORDINAL_WORDS.get(first_token.lower())
        if num is None:
            raise ValueError(f"Unknown ordinal in House district name: {name!r}")
    county_label = parts[-1].lower()
    return county_label, num


def build_house_centroid_index(
    centroids: dict[str, Any],
) -> dict[tuple[str, int], tuple[str, tuple[float, float]]]:
    """
    Returns mapping: (county_label, num) -> (centroid_key, (lat, lon)).
    """
    index: dict[tuple[str, int], tuple[str, tuple[float, float]]] = {}
    for key, coords in centroids["House"].items():
        county_label, num = parse_house_centroid_key(key)
        index[(county_label, num)] = (key, (coords[0], coords[1]))
    return index


def enrich_members_with_distance(
    members_path: Path,
    centroids_path: Path,
    state_house_lat: float = STATE_HOUSE_LAT,
    state_house_lon: float = STATE_HOUSE_LON,
) -> None:
    """Read members.json, attach distance_miles_from_state_house, and
    write the file back in place.

    Expects members.json structure like:
        {
          "session_id": "...",
          "members": [
            {
              "member_id": "...",
              "chamber": "HOUSE" | "SENATE",
              "district": "...",
              ...
            },
            ...
          ]
        }
    """
    # pylint: disable = too-many-locals
    # This is a rarely used, one-purpose function
    with centroids_path.open("r", encoding="utf-8") as f:
        centroids = json.load(f)
    house_index = build_house_centroid_index(centroids)
    senate_index = build_senate_centroid_index(centroids)
    with members_path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    members = data.get("members", [])
    missing_house = []
    missing_senate = []
    for m in members:
        chamber = (m.get("chamber") or "").upper()
        district_name = m.get("district") or ""
        if not district_name:
            m["distance_miles_from_state_house"] = None
            continue
        if chamber == "HOUSE":
            try:
                county_label, num = parse_house_district_name(district_name)
                key = (county_label, num)
                _, (lat, lon) = house_index[key]
                dist = haversine_miles(state_house_lat, state_house_lon, lat, lon)
                m["distance_miles_from_state_house"] = round(dist, 3)
            # pylint: disable = broad-exception-caught
            # Useful for debugging, rarely invoked
            except Exception as e:
                print(f"Exception caught: {e}")
                m["distance_miles_from_state_house"] = None
                missing_house.append((m.get("member_id"), district_name, str(e)))
        elif chamber == "SENATE":
            norm = norm_senate_name(district_name)
            entry = senate_index.get(norm)
            if entry is None:
                m["distance_miles_from_state_house"] = None
                missing_senate.append((m.get("member_id"), district_name))
            else:
                _, (lat, lon) = entry
                dist = haversine_miles(state_house_lat, state_house_lon, lat, lon)
                m["distance_miles_from_state_house"] = round(dist, 3)
        else:
            m["distance_miles_from_state_house"] = None
    data["members"] = members
    with members_path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, sort_keys=True)
    if missing_house:
        print("WARNING: Failed to map House districts to centroids:")
        for member_id, district_name, err in missing_house:
            print(f"  {member_id}: {district_name!r} -> {err}")
    if missing_senate:
        print("WARNING: Failed to map Senate districts to centroids:")
        for member_id, district_name in missing_senate:
            print(f"  {member_id}: {district_name!r}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Enrich members.json with distance to State House."
    )
    parser.add_argument(
        "members_json", type=Path, help="Path to members.json for a session"
    )
    parser.add_argument(
        "--centroids",
        type=Path,
        default=Path("data/sessions/2025-2026/district_centroids.json"),
        help="Path to district_centroids.json",
    )
    args = parser.parse_args()
    enrich_members_with_distance(args.members_json, args.centroids)
