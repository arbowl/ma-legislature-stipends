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
STIPEND_AMOUNT_ADJUSTMENT = SourceRef(
    id="STIPEND_9B",
    label="Manual stipend adjustment from Massachusetts Almanac",
    kind=SourceKind.CALCULATION,
    url="https://massachusettsalmanac.com/perks-n-pay/",
    details=frozenset(
        "Data calculated via delta from base value to Almanac reported current value"
    ),
)
TRAVEL_AMOUNT_ADJUSTMENT = SourceRef(
    id="STIPEND_9B",
    label="Manual stipend adjustment from Massachusetts Almanac",
    kind=SourceKind.CALCULATION,
    url="https://massachusettsalmanac.com/perks-n-pay/",
    details=frozenset(
        "Data calculated via delta from base value to Almanac reported current value"
    ),
)
BASE_SALARY_ADJUSTMENT = SourceRef(
    id="BASE_SALARY_9B",
    label="Manual 9B(g) biennial adjustment factors (2019, 2021, 2023, 2025)",
    kind=SourceKind.MANUAL_OVERRIDE,
    url=None,
    details=frozenset(
        [
            "https://www.cbsnews.com/boston/news/massachusetts-lawmakers-governor-charlie-baker-pay-raises/",
            "https://www.heraldnews.com/story/news/state/2021/01/02/massachusetts-lawmakers-eligible-6-46-percent-pay-raise-2021-baker-state-representatives-senators/4111890001/",
            "https://franklinobserver.town.news/g/franklin-town-ma/n/137414/healey-other-state-officers-line-20-raises",
            "https://www.masslive.com/boston/2025/01/gov-maura-healey-orders-11-pay-raise-for-mass-lawmakers-in-2025.html",
        ]
    ),
)

_ALL_SOURCES: dict[str, SourceRef] = {
    s.id: s
    for s in [
        MGL_3_9B,
        MGL_3_9C,
        ARTICLE_CXVIII_BASE,
        BEA_WAGE_SERIES,
        BASE_SALARY_ADJUSTMENT,
    ]
}


def get_source(id: str) -> SourceRef:
    """Given an ID, return a source from the registry"""
    return _ALL_SOURCES[id]
