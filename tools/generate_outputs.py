"""Generate all analysis outputs for a session"""

from __future__ import annotations

import argparse
from pathlib import Path

from data.session_loader import load_session
from tools.member_profile import generate_member_profile
from tools.session_report import generate_session_report
from tools.writers import write_json


def generate_all_outputs(
    session_id: str, output_dir: Path, verbose: bool = False
) -> None:
    """Generate all outputs for a session"""
    print(f"Loading session {session_id}...")
    loaded = load_session(Path("data/sessions"), session_id)
    session = loaded.session
    session_output = output_dir / session_id
    profiles_dir = session_output / "profiles"
    reports_dir = session_output / "reports"
    print(f"\nGenerating outputs for {len(loaded.members)} members...")
    print("\n1. Generating member profiles...")
    for i, member in enumerate(loaded.members.values(), 1):
        profile = generate_member_profile(member, session, session_id)
        output_path = profiles_dir / f"{member.member_id}.json"
        write_json(profile.to_dict(), output_path)
        if verbose or i % 20 == 0:
            print(f"   Generated {i}/{len(loaded.members)} profiles...")
    print(f"   [OK] Completed {len(loaded.members)} member profiles")
    print("\n2. Generating session report...")
    report = generate_session_report(loaded)
    write_json(report.to_dict(), reports_dir / "full_session.json")
    write_json(report.summary_statistics, reports_dir / "summary_stats.json")
    write_json(report.validation_summary, reports_dir / "validation_report.json")
    print("   [OK] Completed session report")
    print(f"\n{'='*60}")
    print("[SUCCESS] All outputs generated successfully!")
    print(f"\nOutput location: {session_output.absolute()}")
    print("\nGenerated:")
    prof_rel = profiles_dir.relative_to(output_dir)
    print(f"  - {len(loaded.members)} member profiles in {prof_rel}/")
    rep_rel = reports_dir.relative_to(output_dir)
    print(f"  - Session report in {rep_rel}/")
    print("\nValidation:")
    cat_err = report.validation_summary["catalog_errors"]
    sess_err = report.validation_summary["session_errors"]
    dist_err = report.validation_summary["distance_errors"]
    cat_warn = report.validation_summary["catalog_warnings"]
    sess_warn = report.validation_summary["session_warnings"]
    dist_warn = report.validation_summary["distance_warnings"]
    print(f"  - Errors: {cat_err + sess_err + dist_err}")
    print(f"  - Warnings: {cat_warn + sess_warn + dist_warn}")
    if cat_err + sess_err + dist_err > 0:
        val_path = reports_dir / "validation_report.json"
        print(f"\n[WARNING] Check {val_path} for details")
    print(f"{'='*60}\n")


def main() -> None:
    """Generate end-to-end JSON analysis packets"""
    parser = argparse.ArgumentParser(
        description="Generate JSON analysis outputs for legislative session"
    )
    parser.add_argument("session_id", help="Session ID, e.g. 2025-2026")
    parser.add_argument(
        "--output-dir",
        default="docs/",
        help="Output directory (default: docs/)",
    )
    parser.add_argument("--verbose", action="store_true", help="Show detailed progress")
    args = parser.parse_args()
    output_dir = Path(args.output_dir)
    generate_all_outputs(args.session_id, output_dir, args.verbose)


if __name__ == "__main__":
    main()
