"""Generate HTML viewer from JSON profiles"""

from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path

from jinja2 import Template
import markdown  # type: ignore

from version import __version__
from tools.html_viewer.sections import sections


def load_all_profiles(session_dir: Path) -> list[dict]:
    """Load all member profile JSONs"""
    profiles_dir = session_dir / "profiles"
    profiles = []
    for profile_file in sorted(profiles_dir.glob("*.json")):
        with profile_file.open("r", encoding="utf-8") as f:
            profiles.append(json.load(f))
    return profiles


def load_summary_stats(session_dir: Path) -> dict:
    """Load summary statistics"""
    stats_file = session_dir / "reports" / "summary_stats.json"
    with stats_file.open("r", encoding="utf-8") as f:
        return json.load(f)


def load_validation_report(session_dir: Path) -> dict:
    """Load validation report"""
    val_file = session_dir / "reports" / "validation_report.json"
    with val_file.open("r", encoding="utf-8") as f:
        return json.load(f)


def convert_sections_to_html() -> list[dict[str, str]]:
    """Convert markdown sections to HTML with title as H2"""
    html_sections = []
    for title, content in sections.items():
        html_content = markdown.markdown(content.strip())
        # Prepend the section title as an H2 header
        full_content = f"<h2>{title}</h2>\n{html_content}"
        html_sections.append({"title": title, "content": full_content})

    # Add changelog as the last section
    changelog_path = Path(__file__).parent.parent.parent / "CHANGELOG.md"
    if changelog_path.exists():
        with changelog_path.open("r", encoding="utf-8") as f:
            changelog_content = f.read()
        # Convert markdown to HTML (already includes H1 "Changelog")
        changelog_html = markdown.markdown(changelog_content.strip())
        html_sections.append({"title": "Changelog", "content": changelog_html})

    return html_sections


def generate_html_viewer(
    session_id: str, output_dir: Path = Path("tools/output")
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
    with template_path.open("r", encoding="utf-8") as f:
        template = Template(f.read())
    print("Rendering HTML...")
    html_sections = convert_sections_to_html()
    generated_on = datetime.now().strftime("%B %d, %Y at %I:%M %p")
    html = template.render(
        session_id=session_id,
        profiles=profiles,
        stats=stats,
        validation=validation,
        profiles_json=json.dumps(profiles, separators=(",", ":")),
        stats_json=json.dumps(stats, separators=(",", ":")),
        version=__version__,
        html_sections=html_sections,
        github_url="https://github.com/arbowl/ma-legislature-stipends/",
        generated_on=generated_on,
    )
    output_file = Path("docs/") / "index.html"
    with output_file.open("w", encoding="utf-8") as f:
        f.write(html)
    print(f"\n[SUCCESS] HTML viewer generated: {output_file.absolute()}")
    return output_file


def main() -> None:
    """Generates the HTML page for workshop purposes"""
    parser = argparse.ArgumentParser(
        description="Generate HTML viewer for legislative compensation data"
    )
    parser.add_argument("session_id", help="Session ID, e.g. 2025-2026")
    parser.add_argument(
        "--output-dir",
        default="tools/output",
        help="Output directory (default: tools/output)",
    )
    args = parser.parse_args()
    output_dir = Path(args.output_dir)
    generate_html_viewer(args.session_id, output_dir)


if __name__ == "__main__":
    main()
