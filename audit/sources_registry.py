"""Sources for data"""

from __future__ import annotations

from audit.provenance import SourceKind, SourceRef


MGL_3_9B = SourceRef(
    id="MGL_3_9B",
    label="Mass. Gen. Laws c.3 S9B",
    kind=SourceKind.STATUTE,
    url="https://malegislature.gov/Laws/GeneralLaws/PartI/TitleI/Chapter3/Section9B",
    details=frozenset(),
)
MGL_3_9C = SourceRef(
    id="MGL_3_9C",
    label="Mass. Gen. Laws c.3 S9C",
    kind=SourceKind.STATUTE,
    url="https://malegislature.gov/Laws/GeneralLaws/PartI/TitleI/Chapter3/Section9C",
    details=frozenset(),
)
ARTICLE_CXVIII_BASE = SourceRef(
    id="MGL_ART_CXVIII",
    label="Mass. Const. amend. Art. CXVIII (legislator base salary)",
    kind=SourceKind.STATUTE,
    details=frozenset(),
)
BEA_WAGE_SERIES = SourceRef(
    id="BEA_WAGE_SERIES",
    label="BEA Massachusetts wages and salaries series (8-quarter adjustment)",
    kind=SourceKind.ECONOMIC_SERIES,
    url="https://bea.gov/",
    details=frozenset(),
)

_ALL_SOURCES: dict[str, SourceRef] = {
    s.id: s for s in [
        MGL_3_9B,
        MGL_3_9C,
        ARTICLE_CXVIII_BASE,
        BEA_WAGE_SERIES,
    ]
}


def get_source(id: str) -> SourceRef:
    """Given an ID, return a source from the registry"""
    return _ALL_SOURCES[id]
