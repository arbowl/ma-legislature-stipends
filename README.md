![Tests](https://github.com/arbowl/ma-legislature-stipends/workflows/Tests/badge.svg)
![Quick Check](https://github.com/arbowl/ma-legislature-stipends/workflows/Quick%20Check/badge.svg)

https://BeaconHillStipends.org/

# Massachusetts Legislature Compensation Model

A rules engine for calculating Massachusetts legislator compensation based on M.G.L. c.3 §9B (stipends) and §9C (travel expenses). This project scrapes, normalizes, and models legislative data to produce auditable, per-member compensation breakdowns with full provenance tracking.

## Quick Start

```bash
py -m cli.compute_session_comp 2025-2026
```

This runs the compensation calculator for the 2025-2026 session and outputs total compensation for each member.

## Architecture Overview

The pipeline follows a strict separation between the "real" data processing pipeline and visualization tools:

- **Core pipeline** (`ingest/`, `data/`, `models/`, `config/`, `audit/`): Scraping, normalization, rules engine, provenance tracking
- **Visualization playground** (`tools/`): Reports, HTML generation, and data reconfiguration for presentation

### Pipeline Flow

```
1. Scrape (ingest/)
   - Raw HTML from malegislature.gov -> JSON
2. Normalize (data/normalize.py)
   - Raw JSON -> Clean session files
3. Enrich (data/enrich_distance.py)
   - Add geographic data, adjustments
4. Compute (models/)
   - Apply statutory rules
5. Output (cli/ or tools/)
   - Per-member compensation with provenance
```

## Provenance System

Every dollar amount in this system is wrapped in an `AmountWithProvenance` structure that tracks:

- **The value** (in whole dollars)
- **Source references** (statutes, official sites, economic data, calculations)

Source types include:
- `STATUTE`: M.G.L. citations, constitutional amendments
- `OFFICIAL_WEBSITE`: Legislature website, chamber rules
- `ECONOMIC_SERIES`: BEA wage series for biennial adjustments
- `DATA_FILE`: Session-specific configuration files
- `CALCULATION`: Derived values with documented methodology
- `MANUAL_OVERRIDE`: Explicit adjustments with journalistic sourcing

All sources are registered in `audit/sources_registry.py` with URLs and explanatory details. This makes every calculation auditable back to its legal or data source.

### Example: Provenance in Action

When computing a committee chair stipend:
1. Base tier amount -> sourced from M.G.L. c.3 §9B
2. Session adjustment factor -> sourced from BEA wage data or manual override
3. Final stipend -> carries both sources forward

If the member holds multiple roles, the selection logic documents which roles were paid and which were excluded due to statutory caps (House: max 1 position, Senate: max 2 positions), with references to the relevant chamber rules.

## Directory Structure

### `ingest/`
Scrapers for malegislature.gov. Extracts:
- Member roster (names, districts, parties, profile URLs)
- Leadership positions (President, Speaker, floor leaders, etc.)
- Committee assignments and roles

Output: Raw JSON files stored in `data/raw/{session_id}/`

### `data/`
Data pipeline and session management:

- **`normalize.py`**: Converts scraped data into canonical session files
  - Maps inconsistent role titles to internal role codes
  - Links committee assignments to the catalog in `config/committee_catalog.py`
  - Produces `members.json` and `roles.json` for each session

- **`enrich_distance.py`**: Adds geographic data for travel expense calculations (§9C)
  - Uses district centroids to compute State House distance
  - Determines travel tier: $15k (≤50 miles) or $20k (>50 miles)

- **`session_loader.py`**: Loads and validates session data for the rules engine

Session files live in `data/sessions/{session_id}/`:
```
members.json              # Normalized member records
roles.json                # Role assignments mapped to catalog
base_salary.json          # Base salary config
adjustment.json           # Session-specific adjustment factors
district_centroids.json   # Geographic data for travel calc
```

### `config/`
Canonical definitions and catalogs:

- **`role_catalog.py`**: Every role recognized by the statute, with its tier and stipend eligibility
- **`committee_catalog.py`**: Session-independent committee definitions
- **`stipend_tiers.py`**: Statutory stipend tiers (Tier 1: $80k, Tier 2: $65k, etc.)
- **`base_salary.py`**: Article CXVIII base salary
- **`comp_adjustment.py`**: Biennial adjustment factors
- **`travel_config.py`**: §9C travel expense rules

The catalogs map external identifiers (from the Legislature website) to internal codes used by the rules engine.

### `models/`
Core rules engines:

- **`core.py`**: Type definitions (`Member`, `Session`, `RoleAssignment`, etc.)
- **`rules_9b.py`**: Stipend calculation engine
  - Computes stipend for each role
  - Applies chamber-specific caps (House: 1 position max, Senate: 2 positions max)
  - Enforces "at most one paid committee chair" rule
  - Selects the highest-paying lawful combination when caps apply
- **`rules_9c.py`**: Travel expense calculation (distance-based)
- **`total_comp.py`**: Aggregates base salary, stipends, and travel into total compensation

### `audit/`
Provenance and validation infrastructure:

- **`provenance.py`**: `AmountWithProvenance` type and operations (add, scale, sum)
- **`sources_registry.py`**: Registry of all source references with URLs and citations
- **`issues.py`**: Validator issue types (errors, warnings)

### `validators.py`
Validation checks run before computation:
- Role catalog consistency (no duplicate codes, valid tier assignments)
- Session data integrity (all member references valid, roles map to catalog)
- Committee catalog completeness

### `cli/`
Command-line entry points:

- **`compute_session_comp.py`**: Main computation CLI
  - Runs validators
  - Computes total compensation for all members
  - Outputs table with member ID, name, and total

### `tools/` (Visualization Playground)
This directory is for experimenting with output formats and building reports. It's not part of the core data pipeline.

## Data Sources

The pipeline relies on:

1. **malegislature.gov** for member rosters, leadership, and committee data
2. **M.G.L. c.3 §9B** for stipend tier definitions and eligibility rules
3. **M.G.L. c.3 §9C** for travel expense rules
4. **Senate and House Rules** for chamber-specific caps
5. **Massachusetts Constitution Article CXVIII** for base salary ($73,655 as of statute; adjusted biennially)
6. **BEA wage series** (or manual overrides from journalistic sources) for session-specific adjustment factors

## Running a Full Session

To prepare and compute a new session from scratch:

### 1. Scrape the data
```bash
py -m ingest.members --session-id 2025-2026
py -m ingest.committees --session-id 2025-2026
```

Output: `data/raw/2025-2026/*.json`

### 2. Normalize into session files
```bash
py -m data.normalize 2025-2026
```

Output: `data/sessions/2025-2026/members.json`, `roles.json`

### 3. Enrich with geographic data
```bash
py -m data.enrich_distance 2025-2026
```

Output: `data/sessions/2025-2026/district_centroids.json`

### 4. Configure session parameters
Manually create or update:
- `data/sessions/2025-2026/base_salary.json`
- `data/sessions/2025-2026/adjustment.json`

(See existing session files for format)

### 5. Compute compensation
```bash
py -m cli.compute_session_comp 2025-2026
```

### 6. (Optional) Generate reports
```bash
py -m tools.generate_outputs --session-id 2025-2026
```

Output: `tools/output/2025-2026/` (JSON reports, HTML viewer)

## Statutory Rules Implemented

### M.G.L. c.3 §9B: Stipends

The model encodes the full stipend structure:

- **Presiding officers**: Senate President, Speaker of the House
- **Floor leaders**: Majority/Minority leaders, assistant leaders
- **Committee leadership**: Chairs, vice chairs, ranking minority members
- **Tier system**: Tier 1 ($80k), Tier 2 ($65k), Tier 3 ($60k), Tier 4 ($50k), etc.

Statutory caps:
- **House**: No member may receive more than one stipend (House Rules §18)
- **Senate**: Members may be compensated for no more than 2 positions (Senate Rules §11E)
- **All chambers**: At most one paid committee chair per member

When a member holds multiple eligible roles, the engine selects the highest-paying lawful combination and documents which roles were excluded.

### M.G.L. c.3 §9C: Travel Expenses

- Members living ≤50 miles from the State House: $15,000
- Members living >50 miles from the State House: $20,000

Distance calculated from district geographic centroid.

### Article CXVIII: Base Salary

Statutory base: $73,655 (subject to biennial adjustment per §9B(g))

## Key Design Principles

### Session-Independent Catalogs

Role and committee catalogs use internal codes that don't change across sessions. This allows:
- Longitudinal analysis across multiple sessions
- Stable references for tracking role evolution
- Easier diffing and comparison

External identifiers (from the Legislature website) are mapped to internal codes during normalization.

### Separation of Scraping and Logic

Raw scraped data is stored as-is in `data/raw/`. Normalization happens in a separate step, which means:
- Re-running normalization doesn't require re-scraping
- Changes to role mappings can be applied retroactively
- Data lineage is clear: raw -> normalized -> computed

### Explicit Handling of Edge Cases

The normalization layer identifies:
- Unmapped roles (roles that exist but have no statutory stipend)
- Unrecognized committees (mapped to generic "OTHER COMMITTEE" roles)
- Missing or inconsistent data

These are logged during normalization and flagged by validators before computation.

## Testing

Run the test suite:

```bash
pytest unit/
```

Tests cover:
- Role catalog validation
- Session data integrity
- Statutory selection logic (9B caps)
- Provenance propagation
- Demo session computation

## For Journalists and Watchdogs

This system is designed for transparency. Every compensation figure includes:

1. **Which roles** contributed to the total
2. **Which roles** were held but excluded due to caps
3. **Exact statutory or data sources** for every amount
4. **Session-specific adjustments** and their methodology

To audit a specific member:

```bash
py -m tools.member_profile --session-id 2025-2026 --member-id KES0
```

This generates a detailed breakdown showing:
- Base salary (with source)
- Each stipend (role, tier, amount, source)
- Why certain roles didn't count (statutory cap explanation)
- Travel expense (distance, tier, amount, source)
- Total compensation with full provenance chain

Output is available as JSON (`tools/output/{session}/profiles/{member_id}.json`) or HTML.

## Limitations and Scope

This is a model, not an official record. It:
- **Is not** connected to the state's payroll system
- **Does not** account for voluntary stipend refusal (some members decline stipends)
- **Does not** model mid-session role changes (uses roster as of session start)
- **May contain** mapping errors where scraped data is ambiguous

The project aims for accuracy but is an independent reconstruction of statutory rules applied to public data. Use it as a research tool and cross-reference with official records when precision matters.

## Contributing

Contributions are welcome:
- Improve scraping robustness
- Add historical sessions
- Refine role or committee catalogs
- Extend validation checks
- Build new visualizations in `tools/`

Open an issue or submit a PR.


