"""Generate HTML viewer from JSON profiles"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from jinja2 import Template


def load_all_profiles(session_dir: Path) -> list[dict]:
    """Load all member profile JSONs"""
    profiles_dir = session_dir / "profiles"
    profiles = []
    for profile_file in sorted(profiles_dir.glob("*.json")):
        with profile_file.open('r', encoding='utf-8') as f:
            profiles.append(json.load(f))
    return profiles


def load_summary_stats(session_dir: Path) -> dict:
    """Load summary statistics"""
    stats_file = session_dir / "reports" / "summary_stats.json"
    with stats_file.open('r', encoding='utf-8') as f:
        return json.load(f)


def load_validation_report(session_dir: Path) -> dict:
    """Load validation report"""
    val_file = session_dir / "reports" / "validation_report.json"
    with val_file.open('r', encoding='utf-8') as f:
        return json.load(f)


def generate_html_viewer(
    session_id: str,
    output_dir: Path = Path("tools/output")
) -> Path:
    """Generate HTML viewer for a session"""
    session_dir = output_dir / session_id
    if not session_dir.exists():
        raise ValueError(f"Session directory not found: {session_dir}")
    print(f"Loading data for session {session_id}...")
    profiles = load_all_profiles(session_dir)
    stats = load_summary_stats(session_dir)
    validation = load_validation_report(session_dir)
    print(f"Loaded {len(profiles)} member profiles")
    template_path = Path(__file__).parent / "template.html"
    with template_path.open('r', encoding='utf-8') as f:
        template = Template(f.read())
    print("Rendering HTML...")
    html = template.render(
        session_id=session_id,
        profiles=profiles,
        stats=stats,
        validation=validation,
        profiles_json=json.dumps(profiles, separators=(',', ':')),
        stats_json=json.dumps(stats, separators=(',', ':'))
    )
    output_file = session_dir / "viewer.html"
    with output_file.open('w', encoding='utf-8') as f:
        f.write(html)
    print(f"\n[SUCCESS] HTML viewer generated: {output_file.absolute()}")
    return output_file


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate HTML viewer for legislative compensation data"
    )
    parser.add_argument(
        "session_id",
        help="Session ID, e.g. 2025-2026"
    )
    parser.add_argument(
        "--output-dir",
        default="tools/output",
        help="Output directory (default: tools/output)"
    )
    args = parser.parse_args()
    output_dir = Path(args.output_dir)
    generate_html_viewer(args.session_id, output_dir)


if __name__ == "__main__":
    main()

