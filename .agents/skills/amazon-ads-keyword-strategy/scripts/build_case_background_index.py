#!/usr/bin/env python3
"""Merge source-preserving case records into one searchable background index."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, action="append", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    cases: list[dict[str, object]] = []
    seen: set[str] = set()
    for path in args.input:
        for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
            if not line.strip():
                continue
            record = json.loads(line)
            case_id = str(record.get("case_id", ""))
            if not case_id:
                raise ValueError(f"{path}:{line_number} has no case_id")
            if case_id in seen:
                raise ValueError(f"duplicate case_id {case_id} in {path}:{line_number}")
            seen.add(case_id)
            record["retrieval_source_artifact"] = path.as_posix()
            record["retrieval_status"] = "source_preserving_case_record"
            cases.append(record)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8", newline="\n") as handle:
        for record in cases:
            handle.write(json.dumps(record, ensure_ascii=False, separators=(",", ":")) + "\n")
    print(f"Wrote {len(cases)} unique case records to {args.output}")


if __name__ == "__main__":
    main()
