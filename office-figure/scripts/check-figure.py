#!/usr/bin/env python3
"""Validate figure files (PNG, SVG, .drawio) via magic bytes and structure."""

import json
import os
import struct
import sys
import xml.etree.ElementTree as ET


def check_png(path: str) -> dict:
    """Validate PNG magic bytes and read dimensions from IHDR chunk."""
    with open(path, "rb") as f:
        header = f.read(8)
        if header != b"\x89PNG\r\n\x1a\n":
            return {"valid": False, "error": "Invalid PNG magic bytes"}

        # IHDR is always the first chunk after the 8-byte signature
        # Chunk layout: 4-byte length, 4-byte type, data, 4-byte CRC
        chunk_length = struct.unpack(">I", f.read(4))[0]
        chunk_type = f.read(4)
        if chunk_type != b"IHDR":
            return {"valid": False, "error": "First chunk is not IHDR"}

        width, height = struct.unpack(">II", f.read(8))

    return {"valid": True, "format": "png", "size": [width, height]}


def check_svg(path: str) -> dict:
    """Validate SVG by checking for <svg> root element."""
    try:
        tree = ET.parse(path)
        root = tree.getroot()
        # Strip namespace for comparison
        tag = root.tag.split("}")[-1] if "}" in root.tag else root.tag
        if tag != "svg":
            return {"valid": False, "error": "Root element is not <svg>"}

        width = root.get("width", "unknown")
        height = root.get("height", "unknown")
        return {"valid": True, "format": "svg", "width": width, "height": height}

    except ET.ParseError as e:
        return {"valid": False, "error": f"XML parse error: {e}"}


def check_drawio(path: str) -> dict:
    """Validate .drawio by checking for <mxfile> or <mxGraphModel> root."""
    try:
        tree = ET.parse(path)
        root = tree.getroot()
        tag = root.tag.split("}")[-1] if "}" in root.tag else root.tag
        if tag not in ("mxfile", "mxGraphModel"):
            return {
                "valid": False,
                "error": f"Root element is <{tag}>, expected <mxfile> or <mxGraphModel>",
            }

        # Count diagrams/pages if mxfile
        pages = len(root.findall("diagram")) if tag == "mxfile" else 1
        return {"valid": True, "format": "drawio", "pages": pages}

    except ET.ParseError as e:
        return {"valid": False, "error": f"XML parse error: {e}"}


def check_figure(path: str) -> dict:
    """Detect format from extension and validate accordingly."""
    ext = os.path.splitext(path)[1].lower()

    if ext == ".png":
        return check_png(path)
    elif ext == ".svg":
        return check_svg(path)
    elif ext == ".drawio":
        return check_drawio(path)
    else:
        # Fallback: try magic bytes detection
        with open(path, "rb") as f:
            magic = f.read(8)
        if magic[:4] == b"\x89PNG":
            return check_png(path)
        return {"valid": False, "error": f"Unsupported extension: {ext}"}


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"valid": False, "error": "Usage: check-figure.py <file>"}))
        sys.exit(1)

    path = sys.argv[1]
    if not os.path.isfile(path):
        result = {"valid": False, "error": f"File not found: {path}"}
    else:
        result = check_figure(path)

    print(json.dumps(result))
    sys.exit(0 if result["valid"] else 1)
