#!/usr/bin/env python3
"""Cross-platform PDF helper for office-pdf."""

from __future__ import annotations

import argparse
import json
import math
import os
import sys
from pathlib import Path


def require(module_name: str, install_name: str | None = None):
    try:
        return __import__(module_name)
    except ImportError as exc:
        package = install_name or module_name
        raise SystemExit(f"Missing dependency `{package}`. Install it with: python -m pip install {package}") from exc


def write_json(path: str | None, data: dict) -> None:
    text = json.dumps(data, ensure_ascii=False, indent=2)
    if path:
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        Path(path).write_text(text, encoding="utf-8")
    print(text)


def command_inspect(args: argparse.Namespace) -> int:
    pypdf = require("pypdf")
    reader = pypdf.PdfReader(args.input)
    pages = []
    for index, page in enumerate(reader.pages, 1):
        box = page.mediabox
        width = float(box.width)
        height = float(box.height)
        try:
            text = page.extract_text() or ""
        except Exception:
            text = ""
        pages.append({
            "page": index,
            "width_pt": round(width, 2),
            "height_pt": round(height, 2),
            "rotation": int(page.get("/Rotate", 0)),
            "text_chars": len(text),
        })

    fields = []
    try:
        raw_fields = reader.get_fields() or {}
        for name, field in raw_fields.items():
            fields.append({
                "name": str(name),
                "type": str(field.get("/FT", "")),
                "value": str(field.get("/V", "")) if field.get("/V") is not None else "",
            })
    except Exception:
        fields = []

    metadata = {}
    if reader.metadata:
        metadata = {str(k): str(v) for k, v in reader.metadata.items() if v is not None}

    result = {
        "status": "ok",
        "input": str(args.input),
        "encrypted": bool(reader.is_encrypted),
        "page_count": len(reader.pages),
        "metadata": metadata,
        "pages": pages,
        "form_field_count": len(fields),
        "form_fields": fields,
    }
    write_json(args.out, result)
    return 0


def command_render(args: argparse.Namespace) -> int:
    fitz = require("fitz", "PyMuPDF")
    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    doc = fitz.open(args.input)
    rendered = []
    try:
        start = max(args.start, 1)
        end = min(args.end or doc.page_count, doc.page_count)
        for page_number in range(start, end + 1):
            page = doc.load_page(page_number - 1)
            matrix = fitz.Matrix(args.dpi / 72.0, args.dpi / 72.0)
            pix = page.get_pixmap(matrix=matrix, alpha=False)
            target = outdir / f"page-{page_number:03d}.png"
            pix.save(target)
            rendered.append(str(target))
    finally:
        doc.close()
    write_json(args.report, {
        "status": "ok",
        "input": str(args.input),
        "dpi": args.dpi,
        "rendered": rendered,
    })
    return 0


def command_extract(args: argparse.Namespace) -> int:
    output_parts = []
    try:
        pdfplumber = require("pdfplumber")
        with pdfplumber.open(args.input) as pdf:
            for index, page in enumerate(pdf.pages, 1):
                text = page.extract_text() or ""
                output_parts.append(f"\n--- Page {index} ---\n{text}\n")
    except SystemExit:
        pypdf = require("pypdf")
        reader = pypdf.PdfReader(args.input)
        for index, page in enumerate(reader.pages, 1):
            text = page.extract_text() or ""
            output_parts.append(f"\n--- Page {index} ---\n{text}\n")

    text = "".join(output_parts).strip() + "\n"
    if args.out:
        Path(args.out).parent.mkdir(parents=True, exist_ok=True)
        Path(args.out).write_text(text, encoding="utf-8")
    else:
        print(text)
    return 0


def command_merge(args: argparse.Namespace) -> int:
    pypdf = require("pypdf")
    writer = pypdf.PdfWriter()
    for input_path in args.inputs:
        reader = pypdf.PdfReader(input_path)
        for page in reader.pages:
            writer.add_page(page)
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    with open(args.out, "wb") as handle:
        writer.write(handle)
    write_json(args.report, {"status": "ok", "out": args.out, "inputs": args.inputs})
    return 0


def _truthy(value: object) -> bool:
    return str(value).strip().lower() in {"1", "true", "yes", "on"}


def command_fill(args: argparse.Namespace) -> int:
    pypdf = require("pypdf")
    from pypdf.generic import BooleanObject, NameObject

    data = json.loads(Path(args.values).read_text(encoding="utf-8"))
    reader = pypdf.PdfReader(args.input)
    writer = pypdf.PdfWriter()
    writer.clone_document_from_reader(reader)

    acroform = writer._root_object.get("/AcroForm")  # type: ignore[attr-defined]
    if acroform:
        acroform.update({NameObject("/NeedAppearances"): BooleanObject(True)})

    for page in writer.pages:
        writer.update_page_form_field_values(page, {
            key: "Yes" if isinstance(value, bool) and _truthy(value) else str(value)
            for key, value in data.items()
        })

    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    with open(args.out, "wb") as handle:
        writer.write(handle)
    write_json(args.report, {"status": "ok", "out": args.out, "field_count": len(data)})
    return 0


def _draw_header_footer(canvas, doc, title: str, accent, muted) -> None:
    canvas.saveState()
    width, height = doc.pagesize
    canvas.setStrokeColor(accent)
    canvas.setLineWidth(1.2)
    canvas.line(doc.leftMargin, height - 46, width - doc.rightMargin, height - 46)
    canvas.setFillColor(muted)
    canvas.setFont("Helvetica", 7.5)
    canvas.drawString(doc.leftMargin, height - 39, title.upper())
    canvas.drawRightString(width - doc.rightMargin, 26, f"Page {doc.page}")
    canvas.restoreState()


def _bar_chart_drawing(values: list[tuple[str, float]], accent, width: float, height: float):
    from reportlab.graphics.shapes import Drawing, Rect, String, Line
    from reportlab.lib.colors import HexColor

    drawing = Drawing(width, height)
    max_value = max(v for _, v in values) or 1
    left = 36
    bottom = 24
    chart_width = width - 52
    chart_height = height - 46
    bar_gap = 12
    bar_width = (chart_width - bar_gap * (len(values) - 1)) / len(values)
    drawing.add(Line(left, bottom, left + chart_width, bottom, strokeColor=HexColor("#CBD5E1"), strokeWidth=0.8))
    for index, (label, value) in enumerate(values):
        bar_h = chart_height * (value / max_value)
        x = left + index * (bar_width + bar_gap)
        drawing.add(Rect(x, bottom, bar_width, bar_h, fillColor=accent, strokeColor=accent))
        drawing.add(String(x + bar_width / 2, 8, label, textAnchor="middle", fontName="Helvetica", fontSize=7, fillColor=HexColor("#475569")))
        drawing.add(String(x + bar_width / 2, bottom + bar_h + 5, str(int(value)), textAnchor="middle", fontName="Helvetica-Bold", fontSize=7.5, fillColor=HexColor("#334155")))
    return drawing


def command_create_demo(args: argparse.Namespace) -> int:
    reportlab = require("reportlab")
    from reportlab.lib import colors
    from reportlab.lib.colors import HexColor
    from reportlab.lib.enums import TA_JUSTIFY
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
    from reportlab.platypus import (
        SimpleDocTemplate,
        Paragraph,
        Spacer,
        Table,
        TableStyle,
        KeepTogether,
        HRFlowable,
    )

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    title = args.title
    accent = HexColor(args.accent)
    dark = HexColor("#172033")
    muted = HexColor("#64748B")
    light = HexColor("#EEF6F4")

    doc = SimpleDocTemplate(
        str(out),
        pagesize=A4,
        rightMargin=54,
        leftMargin=54,
        topMargin=72,
        bottomMargin=54,
        title=title,
        author="ARIHOAX Office",
    )
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle("DeckTitle", fontName="Helvetica-Bold", fontSize=25, leading=30, textColor=dark, spaceAfter=8))
    styles.add(ParagraphStyle("Subtle", fontName="Helvetica", fontSize=9, leading=13, textColor=muted, spaceAfter=20))
    styles.add(ParagraphStyle("H1x", fontName="Helvetica-Bold", fontSize=15, leading=19, textColor=dark, spaceBefore=14, spaceAfter=6))
    styles.add(ParagraphStyle("BodyX", fontName="Times-Roman", fontSize=10.2, leading=16, textColor=HexColor("#1F2937"), alignment=TA_JUSTIFY, spaceAfter=8))
    styles.add(ParagraphStyle("Callout", fontName="Helvetica-Bold", fontSize=10, leading=14, textColor=dark, backColor=light, borderColor=accent, borderWidth=0, leftIndent=0, rightIndent=0, spaceBefore=8, spaceAfter=8))
    styles.add(ParagraphStyle("Caption", fontName="Helvetica", fontSize=8.2, leading=11, textColor=muted, alignment=1, spaceAfter=10))

    story = [
        Paragraph(title, styles["DeckTitle"]),
        Paragraph("Cross-platform PDF creation, inspection, extraction, form filling, merging, and rendered visual QA.", styles["Subtle"]),
        HRFlowable(width="100%", thickness=1.4, color=accent, spaceAfter=14),
        Paragraph("What this demonstrates", styles["H1x"]),
        Paragraph("This searchable PDF was generated with a pure Python pipeline. The same helper can inspect an existing PDF, render pages to PNG for visual QA, extract text, merge files, and fill form fields while preserving the source file.", styles["BodyX"]),
        Paragraph("Validation is part of the workflow, not an afterthought: every layout-sensitive PDF should be rendered to images and reviewed for clipping, missing glyphs, blank pages, and table overflow.", styles["BodyX"]),
    ]

    callout_table = Table(
        [[Paragraph("Quality gate: inspect the PDF structure, render the pages, then report both the final PDF and the preview artifacts.", styles["Callout"])]],
        colWidths=[doc.width],
    )
    callout_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), light),
        ("LINEBEFORE", (0, 0), (0, -1), 4, accent),
        ("LEFTPADDING", (0, 0), (-1, -1), 14),
        ("RIGHTPADDING", (0, 0), (-1, -1), 12),
        ("TOPPADDING", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
    ]))
    story.append(callout_table)

    story.extend([
        Paragraph("Capability matrix", styles["H1x"]),
    ])
    table_data = [
        ["Route", "Purpose", "Default tool"],
        ["CREATE", "Generate polished searchable PDFs", "ReportLab"],
        ["INSPECT", "Read pages, metadata, fields, text counts", "pypdf"],
        ["RENDER", "Create PNG previews for visual QA", "PyMuPDF"],
        ["EXTRACT", "Review text content", "pdfplumber / pypdf"],
        ["FILL", "Write form field values", "pypdf"],
        ["MERGE", "Combine source PDFs safely", "pypdf"],
    ]
    tbl = Table(table_data, colWidths=[78, 250, 120])
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), accent),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 8.8),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, HexColor("#F8FAFC")]),
        ("GRID", (0, 0), (-1, -1), 0.35, HexColor("#CBD5E1")),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(tbl)
    story.append(Spacer(1, 16))
    story.append(Paragraph("Rendered QA coverage", styles["H1x"]))
    story.append(_bar_chart_drawing([
        ("Create", 92),
        ("Inspect", 88),
        ("Render", 96),
        ("Extract", 82),
        ("Fill", 78),
    ], accent, doc.width, 150))
    story.append(Paragraph("Figure 1: Example capability coverage shown as a generated vector chart.", styles["Caption"]))
    story.append(Paragraph("Practical rule: when a PDF is important enough to deliver, it is important enough to render and inspect. This is the main difference between a casual PDF script and a reusable Office PDF skill.", styles["BodyX"]))

    doc.build(
        story,
        onFirstPage=lambda canvas, d: _draw_header_footer(canvas, d, title, accent, muted),
        onLaterPages=lambda canvas, d: _draw_header_footer(canvas, d, title, accent, muted),
    )
    write_json(args.report, {"status": "ok", "out": str(out), "size_bytes": out.stat().st_size})
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="office-pdf toolkit")
    sub = parser.add_subparsers(dest="command", required=True)

    inspect_p = sub.add_parser("inspect", help="Inspect structure, metadata, pages, and form fields")
    inspect_p.add_argument("--input", required=True)
    inspect_p.add_argument("--out")
    inspect_p.set_defaults(func=command_inspect)

    render_p = sub.add_parser("render", help="Render PDF pages to PNG with PyMuPDF")
    render_p.add_argument("--input", required=True)
    render_p.add_argument("--outdir", required=True)
    render_p.add_argument("--dpi", type=int, default=160)
    render_p.add_argument("--start", type=int, default=1)
    render_p.add_argument("--end", type=int)
    render_p.add_argument("--report")
    render_p.set_defaults(func=command_render)

    extract_p = sub.add_parser("extract", help="Extract text")
    extract_p.add_argument("--input", required=True)
    extract_p.add_argument("--out")
    extract_p.set_defaults(func=command_extract)

    merge_p = sub.add_parser("merge", help="Merge PDFs")
    merge_p.add_argument("--out", required=True)
    merge_p.add_argument("--report")
    merge_p.add_argument("inputs", nargs="+")
    merge_p.set_defaults(func=command_merge)

    fill_p = sub.add_parser("fill", help="Fill PDF form fields from a JSON file")
    fill_p.add_argument("--input", required=True)
    fill_p.add_argument("--out", required=True)
    fill_p.add_argument("--values", required=True)
    fill_p.add_argument("--report")
    fill_p.set_defaults(func=command_fill)

    demo_p = sub.add_parser("create-demo", help="Create a polished demo PDF")
    demo_p.add_argument("--out", required=True)
    demo_p.add_argument("--title", default="Office PDF Capability Sheet")
    demo_p.add_argument("--accent", default="#1F766E")
    demo_p.add_argument("--report")
    demo_p.set_defaults(func=command_create_demo)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
