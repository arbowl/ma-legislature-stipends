from pathlib import Path
import json

from models.core import Member, Session, Party, Chamber
from models.total_comp import total_comp_for_member  # whatever you call it

session = Session.from_id_number(194)
members_path = Path("data/sessions/2025-2026/members.json")

with members_path.open() as f:
    data: dict[str, list[dict]] = json.load(f)

members = []
for m in data["members"]:
    members.append(Member(
        member_id=m["member_id"],
        name=m["name"],
        chamber=Chamber(m["chamber"]),
        party=Party(m["party"]),
        district=m["district"],
        distance_miles_from_state_house=m.get("distance_miles_from_state_house"),
        # plus whatever other fields you use
    ))

for member in members:
    total = total_comp_for_member(member, session)
    print(member.member_id, member.name, float(total))
