from typing import Optional

from models.core import Session


def mk_session(general_court: Optional[int] = None) -> Session:
    """A sample session that uses base values"""
    general_court = 0 if general_court is None else general_court
    return Session.from_id_number(general_court)
