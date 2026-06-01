"""Normalize extracted Amazon ads strategy records.

Input path: data/processed/amazon_ads_skill/extracted_records.jsonl
Output path: data/processed/amazon_ads_skill/normalized_records.jsonl

CLI arguments:
  --input-file: JSONL extracted records path.
  --output-file: JSONL normalized records path.
"""

from __future__ import annotations

import argparse
from pathlib import Path


DEFAULT_INPUT_FILE = Path("data/processed/amazon_ads_skill/extracted_records.jsonl")
DEFAULT_OUTPUT_FILE = Path("data/processed/amazon_ads_skill/normalized_records.jsonl")


def parse_args() -> argparse.Namespace:
    """Parse CLI arguments."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-file", type=Path, default=DEFAULT_INPUT_FILE)
    parser.add_argument("--output-file", type=Path, default=DEFAULT_OUTPUT_FILE)
    return parser.parse_args()


def main() -> int:
    """Run record normalization."""
    parse_args()
    raise NotImplementedError("Future phase will implement record normalization.")


if __name__ == "__main__":
    raise SystemExit(main())

