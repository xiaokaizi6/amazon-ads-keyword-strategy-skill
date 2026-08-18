#!/usr/bin/env python3
"""OCR embedded DOCX/XLSX media into page-traceable JSONL without altering originals."""

from __future__ import annotations

import argparse
import hashlib
import json
import tempfile
import zipfile
from datetime import date
from pathlib import Path

from rapidocr_onnxruntime import RapidOCR


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def ordered_media(archive: zipfile.ZipFile) -> list[zipfile.ZipInfo]:
    return sorted(
        [
            entry
            for entry in archive.infolist()
            if not entry.is_dir() and entry.filename.startswith(("word/media/", "xl/media/"))
        ],
        key=lambda entry: entry.filename.lower(),
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--source-id", required=True)
    parser.add_argument("--reviewed-at", default=date.today().isoformat())
    parser.add_argument("--media-start", type=int, default=1, help="1-based first embedded media item")
    parser.add_argument("--media-end", type=int, help="1-based inclusive last embedded media item")
    parser.add_argument("--append", action="store_true", help="append selected records to output")
    args = parser.parse_args()

    source_hash = sha256(args.source)
    engine = RapidOCR()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(args.source) as archive, args.output.open("a" if args.append else "w", encoding="utf-8", newline="\n") as handle, tempfile.TemporaryDirectory() as temp_dir:
        temp_root = Path(temp_dir)
        media = ordered_media(archive)
        if args.media_start < 1:
            raise ValueError("--media-start must be at least 1")
        media_end = args.media_end or len(media)
        if media_end < args.media_start or media_end > len(media):
            raise ValueError(f"invalid media range {args.media_start}-{media_end}; source has {len(media)} items")
        selected = list(enumerate(media[args.media_start - 1 : media_end], start=args.media_start))
        for index, entry in selected:
            media_path = temp_root / Path(entry.filename).name
            media_path.write_bytes(archive.read(entry))
            try:
                result, elapsed = engine(str(media_path))
                lines = [
                    {"text": str(item[1]), "confidence": round(float(item[2]), 6), "bbox": item[0]}
                    for item in (result or [])
                    if len(item) >= 3 and str(item[1]).strip()
                ]
                review_status = "machine_ocr_derived_not_source_authority"
                ocr_error = None
            except Exception as error:  # Preserve an addressable record for non-raster Office media.
                elapsed = []
                lines = []
                review_status = "embedded_media_not_machine_ocr_readable_refer_to_original"
                ocr_error = f"{type(error).__name__}: {error}"
            record = {
                "record_id": f"{args.source_id}-MEDIA-{index:03d}",
                "source_id": args.source_id,
                "source_location": f"Embedded Office media {index:03d}: {entry.filename}",
                "content_type": "embedded_image_ocr",
                "media_path_in_source": entry.filename,
                "content": "\n".join(line["text"] for line in lines),
                "ocr_lines": lines,
                "mean_confidence": round(sum(line["confidence"] for line in lines) / len(lines), 6) if lines else None,
                "ocr_elapsed_seconds": [round(float(value), 6) for value in elapsed],
                "source_sha256": source_hash,
                "reviewed_at": args.reviewed_at,
                "review_status": review_status,
                "ocr_error": ocr_error,
            }
            handle.write(json.dumps(record, ensure_ascii=False, separators=(",", ":")) + "\n")
    print(f"OCRed {len(selected)} embedded media files to {args.output}")


if __name__ == "__main__":
    main()
