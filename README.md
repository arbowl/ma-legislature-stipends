![Tests](https://github.com/arbowl/ma-legislature-stipends/workflows/Tests/badge.svg)
![Quick Check](https://github.com/arbowl/ma-legislature-stipends/workflows/Quick%20Check/badge.svg)
[![Webpage Status](https://api.netlify.com/api/v1/badges/b0472686-0ddc-4dfe-88f9-8cff86262188/deploy-status)](https://app.netlify.com/projects/comforting-frangipane-e58c06/deploys)

https://BeaconHillStipends.org/

# **Massachusetts Legislature Compensation Model**

This project builds a **fully reproducible, transparent model** of annual compensation for members of the Massachusetts General Court. It encodes the statutory logic behind:

* **Leadership stipends** and **committee stipends** (M.G.L. c.3 §9B)
* **Travel/distance expenses** (M.G.L. c.3 §9C)
* **Base salary adjustments** (Article CXVIII of the Massachusetts Constitution)
* The statute’s **caps and constraints**, including:

  * At most **one paid committee chair**
  * At most **two paid stipend-bearing positions** per member

The goal is to provide an auditable, data-driven system capable of computing compensation for any legislative session using publicly available information.

---

## **What This Project Does**

### **1. Scrapes public legislative data**

The toolkit automatically retrieves:

* The list of all House and Senate members
* Their districts, parties, and profile identifiers
* Leadership positions
* Committee assignments
* Committee metadata and identifiers

All scraped data is stored in a structured, human-readable JSON format.

### **2. Normalizes everything into a clean internal model**

The Legislature’s website is inconsistent in formatting names, roles, and committees.
The pipeline:

* Standardizes member records
* Maps committee assignments to a canonical, session-independent catalog
* Identifies which roles correspond to statutory stipend categories
* Enforces chamber-appropriate distinctions (House vs Senate vs Joint)

This results in session datasets that the stipend calculator can rely on without ambiguity.

### **3. Computes stipends under M.G.L. c.3 §9B**

The model reproduces the statute’s stipend structure, including:

* Presiding officers
* Floor leaders
* Assistant leaders
* Committee chairs / vice chairs / ranking minority members
* Baseline statutory tiers (80k, 65k, 60k, 50k, etc.)
* Session-specific adjustments (e.g., biennial increases)

It also performs **statutory selection**, choosing the highest-paying lawful combination when a member holds more than two stipend-bearing roles.

### **4. Computes travel expenses under M.G.L. c.3 §9C**

Distance to the State House is derived from official district geographic centroids.

The model assigns:

* **$15,000** for members living within 50 miles of the State House
* **$20,000** for members living more than 50 miles away

These totals are integrated into the final compensation output.

### **5. Produces transparent, per-member compensation breakdowns**

For each member and each session, the system outputs:

* Base salary
* Stipends earned (and which were discarded due to statutory caps)
* Travel allowance
* Total annual compensation
* Provenance: where each figure came from, and why

This makes the model suitable for research, journalism, policy analysis, and auditing.

---

## **How the Pipeline Works (Conceptually)**

1. **Scrape**

   * Pull raw data from the Legislature’s website.

2. **Normalize**

   * Clean district names, roles, committees.
   * Match scraped data to the canonical internal catalogs.
   * Write session-specific `members.json` and `roles.json`.

3. **Enrich**

   * Add geographic distances.
   * Apply session-specific stipend adjustment factors.

4. **Compute**

   * Run the compensation engine for the session.
   * Apply statutory rules, caps, and adjustments.

5. **Output**

   * Per-member totals with explanations and audit trails.

---

## **What This Project Is *Not***

* It is **not** a tool that modifies or updates any official state records.
* It is **not** an authoritative statement of legislative compensation.

  * It is an *open model*, based on public information and statutory interpretation.
* It is **not** intended for real-time or operational payroll use.

  * It is a research-grade simulation.

---

## **How to Use the Project**

1. **Prepare a session**
   Run the scrape + normalization pipeline for the desired legislative session.

2. **Inspect the generated session files**
   Session data lives under:

   ```
   data/sessions/<session_id>/
       members.json
       roles.json
       base_salary.json
       stipend_adjustment_9b.json
   ```

3. **Run the compensation calculator**
   Use the CLI or library call to compute totals for all members.

4. **Review the results**
   The output includes:

   * Stipend components
   * Which roles counted or were excluded
   * Travel allowance
   * Total compensation with detailed provenance

---

## **Why This Project Exists**

Massachusetts’ legislative compensation system is:

* Complex
* Distributed across multiple laws
* Partially reported
* Lacking a canonical, machine-readable source

This project fills that gap by creating an open, rigorously structured model that anyone can inspect, audit, reproduce, and build upon.

---

## **Contributions and Extensions**

The system is built to be extensible:

* Add new sessions
* Refine role catalogs
* Improve scraping and normalization
* Update stipend adjustments as new data becomes available
* Extend distance modeling with additional geographic sources
* Produce richer public reports

PRs and issues are welcome.

