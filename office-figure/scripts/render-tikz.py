#!/usr/bin/env python
"""Compile a TikZ/PGFPlots file with local Tectonic and render PNG preview."""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
from pathlib import Path

import fitz


def find_repo_root(start: Path) -> Path:
    for path in [start, *start.parents]:
        if (path / "office-figure" / "SKILL.md").exists():
            return path
        if path.name == "office-figure" and (path / "SKILL.md").exists():
            return path.parent
        if (path / "AGENTS" / "office-skills" / "office-figure").exists():
            return path
    return start


def find_default_tectonic(tex_path: Path) -> Path | None:
    env_tool = os.environ.get("OFFICE_SKILLS_TECTONIC")
    if env_tool:
        return Path(env_tool)

    path_tool = shutil.which("tectonic")
    if path_tool:
        return Path(path_tool)

    for start in (tex_path.parent, Path.cwd().resolve()):
        root = find_repo_root(start)
        for candidate in (
            root / "office-figure" / "tools" / "tectonic" / "tectonic",
            root / "office-figure" / "tools" / "tectonic" / "tectonic.exe",
            root / "tools" / "tectonic" / "tectonic",
            root / "tools" / "tectonic" / "tectonic.exe",
        ):
            if candidate.exists():
                return candidate
    return None


def render_pdf(pdf_path: Path, png_path: Path, dpi: int, page_number: int) -> None:
    doc = fitz.open(pdf_path)
    try:
        page_index = page_number - 1
        if page_index < 0 or page_index >= doc.page_count:
            raise SystemExit(f"PDF has {doc.page_count} pages; page {page_number} is unavailable")
        page = doc.load_page(page_index)
        matrix = fitz.Matrix(dpi / 72.0, dpi / 72.0)
        pix = page.get_pixmap(matrix=matrix, alpha=False)
        png_path.parent.mkdir(parents=True, exist_ok=True)
        pix.save(png_path)
    finally:
        doc.close()


def main() -> int:
    parser = argparse.ArgumentParser(description="Compile TikZ to PDF and PNG.")
    parser.add_argument("tex", type=Path, help="Input .tex file")
    parser.add_argument("--outdir", type=Path, help="Compilation output directory")
    parser.add_argument("--png", type=Path, help="PNG output path")
    parser.add_argument("--dpi", type=int, default=300, help="PNG render DPI")
    parser.add_argument("--page", type=int, default=1, help="1-based PDF page number")
    parser.add_argument("--tectonic", type=Path, help="Path to Tectonic executable")
    parser.add_argument("--quiet", action="store_true", help="Do not pass --print to Tectonic")
    args = parser.parse_args()

    tex_path = args.tex.resolve()
    if not tex_path.exists():
        raise SystemExit(f"Missing input: {tex_path}")

    tectonic = args.tectonic or find_default_tectonic(tex_path)
    if not tectonic or not tectonic.exists():
        raise SystemExit("Missing Tectonic executable. Install `tectonic` in PATH or pass --tectonic.")

    outdir = (args.outdir or tex_path.parent).resolve()
    outdir.mkdir(parents=True, exist_ok=True)

    command = [str(tectonic), "-X", "compile"]
    if not args.quiet:
        command.append("--print")
    command.extend(["--outdir", str(outdir), str(tex_path)])
    subprocess.run(command, check=True)

    pdf_path = outdir / tex_path.with_suffix(".pdf").name
    if not pdf_path.exists():
        raise SystemExit(f"Tectonic did not create expected PDF: {pdf_path}")

    png_path = (args.png or pdf_path.with_suffix(".png")).resolve()
    render_pdf(pdf_path, png_path, args.dpi, args.page)
    print(png_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
