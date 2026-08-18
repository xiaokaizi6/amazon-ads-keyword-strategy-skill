#!/usr/bin/env python3
"""Build a portable source manifest from an existing reviewed batch manifest.

The source manifest remains the record of original acquisition paths.  This
tool adds an asset-relative copy location and verifies it by SHA-256, so a
desktop installation can retrieve the same original files without relying on
the author's Downloads folder or the repository's data/raw directory.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if line.strip():
            value = json.loads(line)
            if not isinstance(value, dict):
                raise ValueError(f"{path}:{number} is not a JSON object")
            rows.append(value)
    return rows


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-manifest", type=Path, required=True)
    parser.add_argument("--skill-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    skill_root = args.skill_root.resolve()
    source_root = skill_root / "assets" / "source_materials"
    if not source_root.is_dir():
        raise SystemExit(f"source assets directory not found: {source_root}")

    candidates: dict[str, list[Path]] = {}
    for path in sorted(source_root.rglob("*")):
        if path.is_file():
            candidates.setdefault(sha256(path), []).append(path)

    output_rows: list[dict[str, Any]] = []
    missing: list[str] = []
    ambiguous: list[str] = []
    for source in load_jsonl(args.source_manifest):
        expected_hash = str(source.get("content_sha256", "")).lower()
        matches = candidates.get(expected_hash, [])
        if len(matches) != 1:
            (missing if not matches else ambiguous).append(str(source.get("source_id")))
            continue
        asset = matches[0]
        row = dict(source)
        row["original_file_path"] = source.get("file_path")
        row["portable_asset_path"] = asset.relative_to(skill_root).as_posix()
        row["portable_byte_count"] = asset.stat().st_size
        row["portable_content_sha256"] = expected_hash
        row["portable_integrity"] = "verified"
        output_rows.append(row)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8", newline="\n") as handle:
        for row in output_rows:
            handle.write(json.dumps(row, ensure_ascii=False, separators=(",", ":")) + "\n")

    print(f"Sources in input: {len(load_jsonl(args.source_manifest))}")
    print(f"Portable sources verified: {len(output_rows)}")
    print(f"Missing source assets: {','.join(missing) if missing else 'none'}")
    print(f"Ambiguous source assets: {','.join(ambiguous) if ambiguous else 'none'}")
    return 0 if not missing and not ambiguous and len(output_rows) else 1


if __name__ == "__main__":
    raise SystemExit(main())
