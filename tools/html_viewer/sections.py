"""Add sections to template.html dynamically."""

sections: dict[str, str] = {
    "Purpose": """
The Beacon Hill Stipends project is a comprehensive model of annual compensation 
for members of the Massachusetts General Court. It is built to be transparent,
reproducible, and auditable, using publicly available information and statutory
interpretation. It primarily draws upon the Massachusetts General Laws, c.3
§§9B and 9C, and the Massachusetts Constitution, Article CXVIII.

This tool is built from public records and statue, not an authoritative source.

Use the [CTHRU](https://cthrupayroll.mass.gov/#!/year/2025/) portal to verify
actual compensation for a member for a given session.
""",
    "Methodology": """
### Sources

This project models the following statutes as a starting point:

- [M.G.L. c.3 §9B](https://malegislature.gov/Laws/GeneralLaws/PartI/TitleI/Chapter3/Section9b)

- [M.G.L. c.3 §9C](https://malegislature.gov/Laws/GeneralLaws/PartI/TitleI/Chapter3/Section9c)

- [Article CXVIII](https://malegislature.gov/Laws/Constitution#amendmentArticleCXVIII) of the Massachusetts Constitution

- [House Rules](https://malegislature.gov/Laws/Rules/House)

- [Senate Rules](https://malegislature.gov/Laws/Rules/Senate)

Other data sources include:

- Official Legislature website (members, roles, committees)

- Massachusetts Secretary of State website (district centroids)

- Official news reports detailing pay raises

_All scraping and transformations are reproducible and the code is open source._

### Model

At a high level, the model:

- Scrapes the official Legislature website for member information

- Normalizes the data into a clean internal model

- Applies the base salary plus biennial adjustments

- Computes stipends per member based on their roles

- Enforces caps on roles and stipends as defined by statutes

- Computes travel expenses based on distance to the State House

- Produces a per-member compensation breakdown with detailed provenance

### Discrepancies

Some liberties are taken with the model to make it consistent:

- Member distances are approximated using district centroids from the Secretary of State

- The model calculates the predicted annual compensation based on statute, not payroll data
""",
    "FAQs": """
### Q: Does this show exactly what my legislator takes home?

**A:** No. This model is a prediction of what legislators would be paid if the statutes were followed exactly.
It is not a guarantee of what they will actually receive.

### Q: Why does the model say my legislator is paid X, but the CTHRU portal says Y?

**A:** The model is based on statute, not payroll data. The CTHRU portal shows actual pay data.

### Q: How can I see the full breakdown of my legislator's compensation?

**A:** Click the sections under a legislator's card to expand them and see the full breakdown.
Click the "📜" icon to see the detailed provenance for each component.
""",
    "About/Contact": """

My name is Drew Bowler. I'm an independent engineer and civic technologist focused on 
improving public access to legislative data and government accountability.

I developed the Beacon Hill Stipends page as an independent project. The site is not 
affiliated with any political party or organization. The only goal is to provide a 
transparent and reproducible model of legislative compensation.

The code is open source and available on [GitHub](https://github.com/arbowl/ma-legislature-stipends).

You can contact me at [info@beaconhilltracker.org](mailto:info@beaconhilltracker.org)

_Special thanks to Scotia Hille for providing input on data and functionality._
""",
}

