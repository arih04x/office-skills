#!/usr/bin/env python3
"""Validate .pptx structure and count slides."""

import json
import re
import sys
import zipfile
import xml.etree.ElementTree as ET


def check_pptx(path: str) -> dict:
    """Open pptx as ZIP and count slides."""
    try:
        with zipfile.ZipFile(path, "r") as zf:
            if "ppt/presentation.xml" not in zf.namelist():
                return {"valid": False, "error": "ppt/presentation.xml not found"}

            # Count slide entries matching ppt/slides/slide<N>.xml
            slide_pattern = re.compile(r"^ppt/slides/slide\d+\.xml$")
            slides = sum(
                1 for name in zf.namelist() if slide_pattern.match(name)
            )

            return {"valid": True, "slides": slides}

    except zipfile.BadZipFile:
        return {"valid": False, "error": "Not a valid ZIP/pptx file"}
    except Exception as e:
        return {"valid": False, "error": str(e)}


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"valid": False, "error": "Usage: check-pptx.py <file>"}))
        sys.exit(1)

    result = check_pptx(sys.argv[1])
    print(json.dumps(result))
    sys.exit(0 if result["valid"] else 1)
