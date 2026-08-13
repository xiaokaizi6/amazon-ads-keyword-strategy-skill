from __future__ import annotations

import hashlib
import json
import re
import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
R = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
X = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
REL = "http://schemas.openxmlformats.org/package/2006/relationships"
NSW = {"w": W, "r": R}
NSX = {"x": X}


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def docx_text(path: Path, out: Path) -> dict:
    with zipfile.ZipFile(path) as z:
        names = z.namelist()
        root = ET.fromstring(z.read("word/document.xml"))
        lines: list[str] = []
        paragraphs = 0
        tables = 0
        # Preserve document order at block level.
        body = root.find(f"{{{W}}}body")
        for block in list(body or []):
            if block.tag == f"{{{W}}}p":
                text = "".join(t.text or "" for t in block.findall(".//w:t", NSW)).strip()
                if text:
                    paragraphs += 1
                    lines.append(text)
            elif block.tag == f"{{{W}}}tbl":
                tables += 1
                lines.append(f"[TABLE {tables}]")
                for tr in block.findall("./w:tr", NSW):
                    row = []
                    for tc in tr.findall("./w:tc", NSW):
                        row.append(" ".join("".join(t.text or "" for t in p.findall(".//w:t", NSW)).strip() for p in tc.findall("./w:p", NSW)).strip())
                    if any(row):
                        lines.append(" || ".join(row))
        # Include headers/footers/footnotes as separate labeled sections when present.
        for name in sorted(names):
            if name.startswith("word/header") or name.startswith("word/footer") or name in {"word/footnotes.xml", "word/endnotes.xml"}:
                try:
                    extra = ET.fromstring(z.read(name))
                except Exception:
                    continue
                texts = ["".join(t.text or "" for t in p.findall(".//w:t", NSW)).strip() for p in extra.findall(".//w:p", NSW)]
                texts = [t for t in texts if t]
                if texts:
                    lines.append(f"[{name}]")
                    lines.extend(texts)
        out.write_text("\n".join(lines), encoding="utf-8")
        return {
            "file": str(path),
            "sha256": digest(path),
            "bytes": path.stat().st_size,
            "paragraphs": paragraphs,
            "tables": tables,
            "chars": sum(len(x) for x in lines),
            "media": len([n for n in names if n.startswith("word/media/")]),
            "output": str(out),
        }


def col_num(ref: str) -> int:
    letters = re.match(r"[A-Z]+", ref or "")
    if not letters:
        return 0
    n = 0
    for c in letters.group(0):
        n = n * 26 + ord(c) - 64
    return n


def xlsx_text(path: Path, out: Path) -> dict:
    with zipfile.ZipFile(path) as z:
        names = z.namelist()
        shared: list[str] = []
        if "xl/sharedStrings.xml" in names:
            root = ET.fromstring(z.read("xl/sharedStrings.xml"))
            for si in root.findall("x:si", NSX):
                shared.append("".join(t.text or "" for t in si.findall(".//x:t", NSX)))
        wb = ET.fromstring(z.read("xl/workbook.xml"))
        rels = ET.fromstring(z.read("xl/_rels/workbook.xml.rels"))
        rid_to_target = {r.attrib["Id"]: r.attrib["Target"] for r in rels}
        rows_out: list[str] = []
        sheets_meta = []
        for sheet in wb.findall("x:sheets/x:sheet", NSX):
            name = sheet.attrib.get("name", "")
            rid = sheet.attrib.get(f"{{{R}}}id")
            target = rid_to_target.get(rid, "")
            if not target.startswith("/"):
                target = "xl/" + target.lstrip("xl/")
            if target not in names:
                target = "xl/worksheets/" + Path(target).name
            root = ET.fromstring(z.read(target))
            sheet_rows = root.findall(".//x:sheetData/x:row", NSX)
            max_col = 0
            count = 0
            rows_out.append(f"[SHEET {name}]")
            for row in sheet_rows:
                vals = {}
                for cell in row.findall("x:c", NSX):
                    ref = cell.attrib.get("r", "")
                    idx = col_num(ref)
                    max_col = max(max_col, idx)
                    typ = cell.attrib.get("t")
                    v = cell.find("x:v", NSX)
                    value = "" if v is None else (v.text or "")
                    if typ == "s" and value.isdigit() and int(value) < len(shared):
                        value = shared[int(value)]
                    elif typ == "inlineStr":
                        value = "".join(t.text or "" for t in cell.findall(".//x:t", NSX))
                    f = cell.find("x:f", NSX)
                    if f is not None and f.text:
                        value = f"={f.text} -> {value}"
                    vals[idx] = value
                if vals:
                    count += 1
                    rows_out.append("\t".join(vals.get(i, "") for i in range(1, max_col + 1)))
            sheets_meta.append({"name": name, "rows": count, "max_col": max_col})
        out.write_text("\n".join(rows_out), encoding="utf-8")
        return {
            "file": str(path),
            "sha256": digest(path),
            "bytes": path.stat().st_size,
            "sheets": sheets_meta,
            "shared_strings": len(shared),
            "output": str(out),
        }


def main() -> None:
    root = Path(r"C:\Users\liuya\Downloads")
    files = [
        root / "亚马逊专题课-进阶广告诊断有优化全指导-文字整理版 (1).docx",
        root / "新品推广基础推广动作及流程(1).xlsx",
        root / "2025亚马逊划线价运营玩法.docx",
        root / "亚马逊折扣+促销说明.xlsx",
        root / "亚马逊广告报告高效分析和优化-Word版 (1).docx",
    ]
    outdir = Path("tmp/source_extracts")
    outdir.mkdir(parents=True, exist_ok=True)
    meta = []
    for p in files:
        stem = p.stem.replace(" ", "_")
        if p.suffix.lower() == ".docx":
            meta.append(docx_text(p, outdir / f"{stem}.txt"))
        else:
            meta.append(xlsx_text(p, outdir / f"{stem}.txt"))
    print(json.dumps(meta, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
