"""Validate generated Amazon ads skill outputs.

Input paths:
  data/processed/amazon_ads_skill/articles_index.jsonl
  data/processed/amazon_ads_skill/article_sections.jsonl
  data/processed/amazon_ads_skill/extracted_records.jsonl
  data/processed/amazon_ads_skill/normalized_records.jsonl
  data/processed/amazon_ads_skill/merged_rules.jsonl
  data/processed/amazon_ads_skill/case_library.jsonl

Output path: data/processed/amazon_ads_skill/validation_report.md

CLI arguments:
  --processed-dir: processed output directory.
  --output-file: validation report path.
"""

from __future__ import annotations

import argparse
from pathlib import Path


DEFAULT_PROCESSED_DIR = Path("data/processed/amazon_ads_skill")
DEFAULT_OUTPUT_FILE = Path("data/processed/amazon_ads_skill/validation_report.md")


def parse_args() -> argparse.Namespace:
    """Parse CLI arguments."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--processed-dir", type=Path, default=DEFAULT_PROCESSED_DIR)
    parser.add_argument("--output-file", type=Path, default=DEFAULT_OUTPUT_FILE)
    return parser.parse_args()


def main() -> int:
    """Run output validation."""
    parse_args()
    raise NotImplementedError("Future phase will implement output validation.")


if __name__ == "__main__":
    raise SystemExit(main())

