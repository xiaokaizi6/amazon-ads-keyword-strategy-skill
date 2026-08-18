#!/usr/bin/env python3
"""Verify portable originals and coverage counts for the 108-source pack."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--skill-root", type=Path, required=True)
    args = parser.parse_args()
    root = args.skill_root.resolve()
    rows: list[dict[str, Any]] = [
        json.loads(line)
        for line in args.manifest.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    source_ids = [str(row.get("source_id", "")) for row in rows]
    type_counts = Counter(str(row.get("source_type", "")) for row in rows)
    errors: list[str] = []
    if len(rows) != 108:
        errors.append(f"expected 108 rows, found {len(rows)}")
    if len(set(source_ids)) != len(source_ids):
        errors.append("source_id values are not unique")
    if type_counts != Counter({"project_corpus": 100, "user_document": 8}):
        errors.append(f"unexpected source_type counts: {dict(type_counts)}")
    for row in rows:
        relative = str(row.get("portable_asset_path", ""))
        target = (root / relative).resolve()
        if not relative or root not in target.parents or not target.is_file():
            errors.append(f"{row.get('source_id')}: missing or unsafe asset path")
            continue
        expected = str(row.get("portable_content_sha256", "")).lower()
        if sha256(target) != expected:
            errors.append(f"{row.get('source_id')}: SHA-256 mismatch")
    print(f"Portable manifest rows: {len(rows)}")
    print(f"Source-type counts: {dict(type_counts)}")
    print(f"Integrity errors: {len(errors)}")
    for error in errors:
        print(f"- {error}")
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
