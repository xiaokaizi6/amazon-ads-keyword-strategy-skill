"""Build source manifests and claim-level validation coverage reports.

The command is intentionally conservative: it inventories source files and
validates a user/Codex-authored atomic-claim JSONL file, but it never infers
that a claim is true or false from text alone.

Default inputs and outputs:

  source directory: data/raw/amazon_ads_articles
  manifest: data/processed/amazon_ads_skill/source_manifest.jsonl
  claim review: data/processed/amazon_ads_skill/claim_review.jsonl
  report: data/processed/amazon_ads_skill/source_validation_report.md

Use ``--no-project-corpus --source-file <path>`` for a later user-supplied
batch.  A claim file is optional; without it the report is ``NOT_READY`` and
the claim-review output is not created.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter
from datetime import date
from pathlib import Path
from typing import Any, Iterable


DEFAULT_SOURCE_DIR = Path("data/raw/amazon_ads_articles")
DEFAULT_MANIFEST_OUTPUT = Path("data/processed/amazon_ads_skill/source_manifest.jsonl")
DEFAULT_CLAIM_OUTPUT = Path("data/processed/amazon_ads_skill/claim_review.jsonl")
DEFAULT_REPORT_OUTPUT = Path("data/processed/amazon_ads_skill/source_validation_report.md")

TEXT_EXTENSIONS = {
    ".csv",
    ".json",
    ".jsonl",
    ".md",
    ".rst",
    ".text",
    ".txt",
    ".tsv",
    ".yaml",
    ".yml",
}

CLAIM_STATUSES = {
    "supported",
    "confirmed_error",
    "outdated",
    "unsupported",
    "context_dependent",
    "disputed",
    "unresolved",
}

REQUIRED_CLAIM_FIELDS = {
    "claim_id",
    "source_id",
    "source_location",
    "evidence_quote",
    "normalized_claim",
    "claim_type",
    "status",
    "confidence",
    "checked_source_ids",
    "supporting_evidence",
    "opposing_evidence",
    "missing_evidence",
    "verification_test",
    "reviewed_at",
}


def parse_args() -> argparse.Namespace:
    """Parse the source-review CLI."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--source-dir",
        action="append",
        type=Path,
        help="Directory to inventory recursively; may be repeated.",
    )
    parser.add_argument(
        "--source-file",
        action="append",
        type=Path,
        help="Individual file to inventory; may be repeated.",
    )
    parser.add_argument(
        "--no-project-corpus",
        action="store_true",
        help="Do not include data/raw/amazon_ads_articles by default.",
    )
    parser.add_argument("--claims-file", type=Path, help="Atomic claim JSONL to review.")
    parser.add_argument("--manifest-output", type=Path, default=DEFAULT_MANIFEST_OUTPUT)
    parser.add_argument("--claim-output", type=Path, default=DEFAULT_CLAIM_OUTPUT)
    parser.add_argument("--report-output", type=Path, default=DEFAULT_REPORT_OUTPUT)
    parser.add_argument("--source-type", default="user_document")
    parser.add_argument("--marketplace", default="unknown")
    parser.add_argument("--ad-product", action="append", default=[])
    parser.add_argument("--product-stage", action="append", default=[])
    parser.add_argument("--first-party", action="store_true")
    parser.add_argument("--acquired-date", default=date.today().isoformat())
    return parser.parse_args()


def sha256_file(path: Path) -> str:
    """Return a streaming SHA-256 for a source file."""
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_text(path: Path) -> tuple[str | None, list[str]]:
    """Read text sources with BOM-tolerant and GB18030 fallbacks."""
    if path.suffix.lower() not in TEXT_EXTENSIONS:
        return None, [f"binary_or_unsupported_extension:{path.suffix.lower() or '<none>'}"]
    raw = path.read_bytes()
    if not raw:
        return "", ["empty_file"]
    for encoding in ("utf-8-sig", "utf-8", "gb18030"):
        try:
            return raw.decode(encoding), []
        except UnicodeDecodeError:
            continue
    return None, ["decode_failed_utf8_utf8sig_gb18030"]


def title_from_text(text: str | None, fallback: str) -> str:
    """Extract the first Markdown heading or use the file name."""
    if text:
        for line in text.splitlines():
            match = re.match(r"^\s{0,3}#{1,6}\s+(.+?)\s*$", line)
            if match:
                return match.group(1).strip()[:240]
    return fallback


def stable_source_id(path: Path, digest: str) -> str:
    """Create a stable ID without embedding an absolute machine path."""
    try:
        location = path.resolve().relative_to(Path.cwd().resolve()).as_posix()
    except ValueError:
        location = path.resolve().as_posix()
    seed = f"{location}\0{digest}".encode("utf-8")
    return f"SRC-{hashlib.sha1(seed).hexdigest()[:12]}"


def evidence_cluster(digest: str) -> str:
    """Group byte-identical files as one evidence cluster."""
    return f"EC-{digest[:12]}"


def iter_source_paths(
    source_dirs: Iterable[Path], source_files: Iterable[Path]
) -> list[Path]:
    """Collect existing files once, preserving deterministic order."""
    paths: dict[str, Path] = {}
    for directory in source_dirs:
        if not directory.is_dir():
            raise FileNotFoundError(f"Source directory does not exist: {directory}")
        for path in directory.rglob("*"):
            if path.is_file():
                paths[str(path.resolve()).lower()] = path
    for path in source_files:
        if not path.is_file():
            raise FileNotFoundError(f"Source file does not exist: {path}")
        paths[str(path.resolve()).lower()] = path
    return sorted(paths.values(), key=lambda item: str(item).lower())


def build_manifest(paths: list[Path], args: argparse.Namespace) -> list[dict[str, Any]]:
    """Create source records while preserving readability limitations."""
    records: list[dict[str, Any]] = []
    for path in paths:
        digest = sha256_file(path)
        text, issues = read_text(path)
        records.append(
            {
                "source_id": stable_source_id(path, digest),
                "file_name": path.name,
                "file_path": path.as_posix(),
                "title": title_from_text(text, path.stem),
                "author_or_org": "unknown",
                "published_date": "",
                "acquired_date": args.acquired_date,
                "version": "",
                "source_type": args.source_type,
                "marketplace": args.marketplace,
                "ad_products": list(args.ad_product),
                "product_stages": list(args.product_stage),
                "is_first_party": bool(args.first_party),
                "evidence_cluster": evidence_cluster(digest),
                "content_sha256": digest,
                "byte_count": path.stat().st_size,
                "extension": path.suffix.lower(),
                "readable": text is not None,
                "readability_issues": issues,
                "included_in_scope": True,
            }
        )
    return records


def write_jsonl(path: Path, records: Iterable[dict[str, Any]]) -> None:
    """Write one JSON object per line."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for record in records:
            handle.write(json.dumps(record, ensure_ascii=False, separators=(",", ":")) + "\n")


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    """Load JSONL objects and fail with a line-specific error."""
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8-sig") as handle:
        for line_number, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            try:
                value = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"Invalid JSON at {path}:{line_number}: {exc}") from exc
            if not isinstance(value, dict):
                raise ValueError(f"JSONL record at {path}:{line_number} is not an object")
            rows.append(value)
    return rows


def as_ref_ids(value: Any) -> list[str]:
    """Extract source IDs from string or object reference arrays."""
    if not isinstance(value, list):
        return []
    result: list[str] = []
    for item in value:
        if isinstance(item, str) and item:
            result.append(item)
        elif isinstance(item, dict) and isinstance(item.get("source_id"), str):
            result.append(item["source_id"])
    return sorted(set(result))


def validate_claims(
    claims: list[dict[str, Any]], manifest: list[dict[str, Any]]
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """Validate claim contracts and calculate honest source coverage."""
    manifest_ids = {record["source_id"] for record in manifest}
    readable_ids = {record["source_id"] for record in manifest if record.get("readable")}
    reviewed: list[dict[str, Any]] = []
    checked_ids: set[str] = set()
    errors = 0

    for claim in claims:
        missing_fields = sorted(REQUIRED_CLAIM_FIELDS - set(claim))
        source_id = claim.get("source_id", "")
        references = sorted(
            set(
                [source_id]
                + as_ref_ids(claim.get("checked_source_ids"))
                + as_ref_ids(claim.get("supporting_evidence"))
                + as_ref_ids(claim.get("opposing_evidence"))
            )
        )
        checked_ids.update(item for item in references if item in manifest_ids)
        row = dict(claim)
        row["checked_source_ids"] = references
        row["validation_errors"] = []
        if missing_fields:
            row["validation_errors"].append(
                {"code": "missing_fields", "fields": missing_fields}
            )
        if source_id not in manifest_ids:
            row["validation_errors"].append(
                {"code": "unknown_source_id", "source_id": source_id}
            )
        if claim.get("status") not in CLAIM_STATUSES:
            row["validation_errors"].append(
                {"code": "invalid_status", "status": claim.get("status")}
            )
        if claim.get("status") == "confirmed_error" and not (
            claim.get("opposing_evidence") and claim.get("verification_test")
        ):
            row["validation_errors"].append(
                {
                    "code": "confirmed_error_requires_direct_counterevidence",
                    "message": "需要 opposing_evidence 和 verification_test。",
                }
            )
        if claim.get("status") in {"disputed", "context_dependent", "unresolved"} and not (
            claim.get("missing_evidence") or claim.get("verification_test")
        ):
            row["validation_errors"].append(
                {
                    "code": "uncertainty_requires_next_check",
                    "message": "不确定或冲突主张必须记录缺失证据或验证测试。",
                }
            )
        row["coverage"] = {
            "source_id_known": source_id in manifest_ids,
            "checked_source_ids_known": [item for item in references if item in manifest_ids],
            "unreadable_source_ids": [item for item in references if item not in readable_ids and item in manifest_ids],
            "status": "covered" if source_id in manifest_ids and references else "uncovered",
        }
        if row["validation_errors"]:
            errors += len(row["validation_errors"])
        reviewed.append(row)

    unreviewed_ids = sorted(manifest_ids - checked_ids)
    unreadable_ids = sorted(manifest_ids - readable_ids)
    coverage = {
        "scope_source_count": len(manifest_ids),
        "claim_count": len(reviewed),
        "checked_source_count": len(checked_ids),
        "unreviewed_source_count": len(unreviewed_ids),
        "unreviewed_source_ids": unreviewed_ids,
        "unreadable_source_count": len(unreadable_ids),
        "unreadable_source_ids": unreadable_ids,
        "validation_error_count": errors,
        "status": (
            "FAIL"
            if errors
            else "PASS"
            if reviewed and not unreviewed_ids and not unreadable_ids
            else "PARTIAL"
        ),
    }
    return reviewed, coverage


def write_report(
    path: Path,
    manifest: list[dict[str, Any]],
    claims: list[dict[str, Any]],
    coverage: dict[str, Any],
    claims_file: Path | None,
) -> None:
    """Write a Markdown report that never overstates review coverage."""
    source_types = Counter(record.get("source_type", "unknown") for record in manifest)
    lines = [
        "# Source Validation Report",
        "",
        f"- Scope source count: {coverage['scope_source_count']}",
        f"- Readable source count: {sum(1 for record in manifest if record.get('readable'))}",
        f"- Claim count: {coverage['claim_count']}",
        f"- Checked source count: {coverage['checked_source_count']}",
        f"- Validation errors: {coverage['validation_error_count']}",
        f"- Status: **{coverage['status'] if claims_file else 'NOT_READY'}**",
        "",
        "## Source Types",
        "",
    ]
    lines.extend(f"- {key}: {value}" for key, value in sorted(source_types.items()))
    lines.extend(["", "## Review Inputs", ""])
    lines.append(f"- Claims file: `{claims_file.as_posix()}`" if claims_file else "- Claims file: NOT RUN")
    lines.append("- Claim review is not a text-only truth classifier; statuses require explicit evidence references.")
    lines.extend(["", "## Coverage", ""])
    if coverage["unreviewed_source_ids"]:
        lines.append(f"- Unreviewed source IDs: {', '.join(coverage['unreviewed_source_ids'][:50])}")
    else:
        lines.append("- Unreviewed source IDs: none")
    if coverage["unreadable_source_ids"]:
        lines.append(f"- Unreadable source IDs: {', '.join(coverage['unreadable_source_ids'][:50])}")
    else:
        lines.append("- Unreadable source IDs: none")
    lines.extend(["", "## Claim Status Counts", ""])
    status_counts = Counter(claim.get("status", "invalid") for claim in claims)
    lines.extend(f"- {key}: {value}" for key, value in sorted(status_counts.items()))
    if not claims_file:
        lines.extend(
            [
                "",
                "No claim file was supplied. The manifest is an inventory only; no claim has been verified.",
            ]
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    """Inventory sources and optionally validate claims."""
    args = parse_args()
    source_dirs = list(args.source_dir or [])
    if not args.no_project_corpus and not source_dirs and not args.source_file:
        source_dirs = [DEFAULT_SOURCE_DIR]
    source_files = list(args.source_file or [])
    paths = iter_source_paths(source_dirs, source_files)
    if not paths:
        raise ValueError("No source files found; provide --source-dir or --source-file")

    manifest = build_manifest(paths, args)
    write_jsonl(args.manifest_output, manifest)
    claims: list[dict[str, Any]] = []
    coverage = {
        "scope_source_count": len(manifest),
        "claim_count": 0,
        "checked_source_count": 0,
        "unreviewed_source_count": len(manifest),
        "unreviewed_source_ids": [record["source_id"] for record in manifest],
        "unreadable_source_count": sum(1 for record in manifest if not record.get("readable")),
        "unreadable_source_ids": [record["source_id"] for record in manifest if not record.get("readable")],
        "validation_error_count": 0,
        "status": "NOT_READY",
    }
    if args.claims_file:
        claims = load_jsonl(args.claims_file)
        claims, coverage = validate_claims(claims, manifest)
        write_jsonl(args.claim_output, claims)
    write_report(args.report_output, manifest, claims, coverage, args.claims_file)
    print(f"Wrote {len(manifest)} source records to {args.manifest_output}")
    if args.claims_file:
        print(f"Wrote {len(claims)} claim reviews to {args.claim_output}")
    else:
        print("Claim review not run: no --claims-file supplied")
    print(f"Wrote source validation report to {args.report_output}")
    return 0 if coverage["status"] in {"PASS", "PARTIAL", "NOT_READY"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
