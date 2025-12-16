"""Output writers for various formats"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def write_json(data: Any, path: Path, indent: int = 2) -> None:
    """Write data to JSON file with pretty formatting"""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=indent, ensure_ascii=False)
    try:
        print(f"[OK] Wrote {path}")
    except UnicodeEncodeError:
        print(f"[OK] Wrote {path}")


def write_json_compact(data: Any, path: Path) -> None:
    """Write data to JSON file in compact format"""
    write_json(data, path, indent=None)
