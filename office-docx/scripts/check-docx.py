#!/usr/bin/env python3
"""Validate .docx structure and count paragraphs, tables, images."""

import json
import sys
import zipfile
import xml.etree.ElementTree as ET


def check_docx(path: str) -> dict:
    """Open docx as ZIP and extract structural counts."""
    try:
        with zipfile.ZipFile(path, "r") as zf:
            if "word/document.xml" not in zf.namelist():
                return {"valid": False, "error": "word/document.xml not found"}

            # Parse document.xml for paragraphs and tables
            ns = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
            tree = ET.fromstring(zf.read("word/document.xml"))
            paragraphs = len(tree.findall(".//" + "{%s}p" % ns["w"]))
            tables = len(tree.findall(".//" + "{%s}tbl" % ns["w"]))

            # Count images from relationship file
            images = 0
            rels_path = "word/_rels/document.xml.rels"
            if rels_path in zf.namelist():
                rels_ns = {
                    "r": "http://schemas.openxmlformats.org/package/2006/relationships"
                }
                rels_tree = ET.fromstring(zf.read(rels_path))
                image_type = (
                    "http://schemas.openxmlformats.org/officeDocument/2006/"
                    "relationships/image"
                )
                for rel in rels_tree.findall("{%s}Relationship" % rels_ns["r"]):
                    if rel.get("Type") == image_type:
                        images += 1

            return {
                "valid": True,
                "paragraphs": paragraphs,
                "tables": tables,
                "images": images,
            }

    except zipfile.BadZipFile:
        return {"valid": False, "error": "Not a valid ZIP/docx file"}
    except Exception as e:
        return {"valid": False, "error": str(e)}


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"valid": False, "error": "Usage: check-docx.py <file>"}))
        sys.exit(1)

    result = check_docx(sys.argv[1])
    print(json.dumps(result))
    sys.exit(0 if result["valid"] else 1)
