#!/usr/bin/env python3
"""Validate the office-skills repository structure and scan for obvious secrets."""

from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path


SECRET_PATTERNS = [
    (re.compile(r"sk-[a-zA-Z0-9_-]{20,}"), "OpenAI-style API key"),
    (re.compile(r"AKIA[0-9A-Z]{16}"), "AWS access key"),
    (re.compile(r"Bearer\s+[a-zA-Z0-9_\-.]{50,}"), "Hardcoded bearer token"),
]

SCAN_EXTENSIONS = {
    ".cs",
    ".csproj",
    ".drawio",
    ".example",
    ".ini",
    ".js",
    ".json",
    ".md",
    ".mjs",
    ".ps1",
    ".py",
    ".sh",
    ".tex",
    ".toml",
    ".txt",
    ".yaml",
    ".yml",
}

SKIP_DIRS = {
    ".git",
    ".venv",
    "__pycache__",
    "bin",
    "generated",
    "node_modules",
    "obj",
    "out",
    "temp",
    "tmp",
    "venv",
}

SKIP_FILES = {
    ".env",
    "env.conf",
    "office-skills.local.env",
    "settings.local.json",
}

COMMUNITY_LANES = ("good", "corrections", "anti-patterns")


def extract_frontmatter(text: str) -> str | None:
    stripped = text.lstrip("\ufeff")
    if not stripped.startswith("---"):
        return None
    end = stripped.find("---", 3)
    if end == -1:
        return None
    return stripped[3:end]


def parse_frontmatter_fields(frontmatter: str) -> dict[str, str]:
    fields: dict[str, str] = {}
    lines = frontmatter.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if not line.strip() or line.strip().startswith("#"):
            i += 1
            continue
        match = re.match(r"^([a-zA-Z_][a-zA-Z0-9_]*)\s*:\s*(.*)", line)
        if not match:
            i += 1
            continue
        key = match.group(1)
        rest = match.group(2).strip()
        if rest in ("|", ">", "|+", "|-", ">+", ">-"):
            block_lines = []
            i += 1
            while i < len(lines) and (
                lines[i].startswith("  ") or lines[i].startswith("\t") or lines[i].strip() == ""
            ):
                block_lines.append(lines[i])
                i += 1
            fields[key] = "\n".join(block_lines).strip()
            continue
        fields[key] = rest.strip("\"'")
        i += 1
    return fields


def iter_skill_dirs(base_path: Path) -> list[Path]:
    return sorted(
        path for path in base_path.iterdir()
        if path.is_dir() and path.name.startswith("office-") and (path / "SKILL.md").exists()
    )


def validate_skill(skill_dir: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    skill_md = skill_dir / "SKILL.md"

    content = skill_md.read_text(encoding="utf-8-sig", errors="ignore")
    frontmatter = extract_frontmatter(content)
    if frontmatter is None:
        errors.append("SKILL.md has no valid YAML frontmatter")
        return errors, warnings

    fields = parse_frontmatter_fields(frontmatter)
    name = fields.get("name", "").strip()
    description = fields.get("description", "").strip()

    if not name:
        errors.append("Missing required field: name")
    elif name != skill_dir.name:
        errors.append(f"name '{name}' does not match directory name '{skill_dir.name}'")

    if not description:
        errors.append("Missing required field: description")

    if not (skill_dir / "agents" / "openai.yaml").exists():
        warnings.append("Missing recommended agents/openai.yaml")

    community_dir = skill_dir / "examples" / "community"
    if not (community_dir / "README.md").exists():
        errors.append("Missing examples/community/README.md")
    for lane in COMMUNITY_LANES:
        if not (community_dir / lane).is_dir():
            errors.append(f"Missing examples/community/{lane}/")

    previews_dir = skill_dir / "assets" / "previews"
    if previews_dir.exists() and any(previews_dir.rglob("*")):
        errors.append("Rendered previews belong in examples/, not assets/previews/")

    env_dir = skill_dir / "assets" / "env"
    if env_dir.exists():
        public_env_files = [path for path in env_dir.rglob("*") if path.is_file() and path.name != "env.conf"]
        if public_env_files:
            errors.append("Per-skill env examples are not allowed; use config/office-skills.local.env.example")

    return errors, warnings


def should_scan_file(path: Path) -> bool:
    if path.name in SKIP_FILES:
        return False
    if path.suffix not in SCAN_EXTENSIONS:
        return False
    return not any(part in SKIP_DIRS or part.startswith(".git") for part in path.parts)


def scan_secrets(base_path: Path) -> list[str]:
    findings: list[str] = []
    for root, dirs, files in os.walk(base_path):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for filename in files:
            path = Path(root) / filename
            rel = path.relative_to(base_path)
            if not should_scan_file(rel):
                continue
            text = path.read_text(encoding="utf-8", errors="ignore")
            for line_no, line in enumerate(text.splitlines(), 1):
                for pattern, description in SECRET_PATTERNS:
                    match = pattern.search(line)
                    if match:
                        findings.append(f"{rel}:{line_no} potential {description}: {match.group(0)[:24]}...")
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate office-skills repository")
    parser.add_argument("--path", default=".", help="Repository root to scan")
    args = parser.parse_args()

    base_path = Path(args.path).resolve()
    skill_dirs = iter_skill_dirs(base_path)
    if not skill_dirs:
        print("No top-level office-* skill directories found.")
        return 1

    total_errors = 0
    total_warnings = 0

    print(f"\nValidating {len(skill_dirs)} office skill(s)...\n")
    for skill_dir in skill_dirs:
        errors, warnings = validate_skill(skill_dir)
        status = "FAIL" if errors else "WARN" if warnings else "PASS"
        print(f"  [{status}]  {skill_dir.relative_to(base_path)}")
        for error in errors:
            print(f"           ERROR  {error}")
        for warning in warnings:
            print(f"           WARN   {warning}")
        total_errors += len(errors)
        total_warnings += len(warnings)

    secret_findings = scan_secrets(base_path)
    for finding in secret_findings:
        print(f"  [FAIL]  {finding}")
    total_errors += len(secret_findings)

    print()
    if total_errors:
        print(f"  {total_errors} error(s), {total_warnings} warning(s)")
        print("  Validation FAILED.\n")
        return 1
    if total_warnings:
        print(f"  0 errors, {total_warnings} warning(s)")
        print("  Validation PASSED.\n")
        return 0
    print("  All checks passed.\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
