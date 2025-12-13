from models.core import Session


def mk_session() -> Session:
    return Session(
        id=Session.from_id_number(194),
        start_year=2025,
        end_year=2026,
        label=Session.from_id_number(194)
    )
