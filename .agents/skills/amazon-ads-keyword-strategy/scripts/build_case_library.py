"""Build the case library from normalized Amazon ads strategy records.

Input path: data/processed/amazon_ads_skill/normalized_records.jsonl
Output path: data/processed/amazon_ads_skill/case_library.jsonl

CLI arguments:
  --input-file: JSONL normalized records path.
  --output-file: JSONL case library path.
The implementation is shared with ``normalize_records.py`` so the full
normalization pipeline and this focused rebuild command cannot drift apart.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from normalize_records import (
    attach_cases_and_diagnostics,
    attach_counterexamples,
    build_case_library,
    build_rule_groups,
    load_jsonl,
    write_jsonl,
)


DEFAULT_INPUT_FILE = Path("data/processed/amazon_ads_skill/normalized_records.jsonl")
DEFAULT_OUTPUT_FILE = Path("data/processed/amazon_ads_skill/case_library.jsonl")


def parse_args() -> argparse.Namespace:
    """Parse CLI arguments."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-file", type=Path, default=DEFAULT_INPUT_FILE)
    parser.add_argument("--output-file", type=Path, default=DEFAULT_OUTPUT_FILE)
    return parser.parse_args()


def main() -> int:
    """Run case library building."""
    args = parse_args()
    records = load_jsonl(args.input_file)
    if not records:
        raise ValueError(f"No normalized records found in {args.input_file}")

    merged_rules = build_rule_groups(records)
    attach_counterexamples(
        merged_rules,
        [record for record in records if record.get("record_type") == "counterexample"],
    )
    cases = build_case_library(records)
    attach_cases_and_diagnostics(merged_rules, cases, records)
    write_jsonl(args.output_file, cases)
    print(f"Wrote {len(cases)} cases to {args.output_file}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
