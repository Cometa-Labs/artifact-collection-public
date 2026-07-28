#!/usr/bin/env python3
"""Validate documents/manifest.json against the Artifact schema.

Usage:
    python3 validate_manifest.py [path/to/documents]

Defaults to "documents" in the current directory. Checks manifest.json parses,
every entry has the required fields with correct types/enums, slugs and
indexCodes are unique, dates are well-formed, and every referenced `file`
exists as a sibling in the documents/ folder. Exits non-zero if any check
fails, printing every problem found (not just the first).
"""
import json
import re
import sys
from pathlib import Path

REQUIRED_STRING_FIELDS = ["slug", "title", "eyebrow", "summary", "file", "date", "type", "indexCode", "status", "agentUse"]
VALID_TYPES = {"Report", "Model", "Calculator", "Map", "Product"}
VALID_STATUSES = {"Reference", "Active", "Exploratory"}
SLUG_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
INDEX_CODE_RE = re.compile(r"^[A-Z]+-\d{3}$")


def main():
    docs_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("documents")
    manifest_path = docs_dir / "manifest.json"

    if not manifest_path.exists():
        print(f"ERROR: {manifest_path} does not exist")
        sys.exit(1)

    try:
        manifest = json.loads(manifest_path.read_text())
    except json.JSONDecodeError as e:
        print(f"ERROR: {manifest_path} is not valid JSON: {e}")
        sys.exit(1)

    if not isinstance(manifest, list):
        print(f"ERROR: {manifest_path} must be a JSON array at the top level")
        sys.exit(1)

    errors = []
    slugs = {}
    index_codes = {}

    for i, entry in enumerate(manifest):
        label = f"entry[{i}]" + (f" (slug={entry.get('slug')!r})" if isinstance(entry, dict) and "slug" in entry else "")

        if not isinstance(entry, dict):
            errors.append(f"{label}: not a JSON object")
            continue

        for field in REQUIRED_STRING_FIELDS:
            if field not in entry:
                errors.append(f"{label}: missing required field '{field}'")
            elif not isinstance(entry[field], str) or not entry[field].strip():
                errors.append(f"{label}: '{field}' must be a non-empty string")

        if "tags" not in entry:
            errors.append(f"{label}: missing required field 'tags'")
        elif not isinstance(entry["tags"], list) or not all(isinstance(t, str) for t in entry["tags"]):
            errors.append(f"{label}: 'tags' must be an array of strings")

        slug = entry.get("slug")
        if isinstance(slug, str):
            if not SLUG_RE.match(slug):
                errors.append(f"{label}: slug '{slug}' must be kebab-case ([a-z0-9-])")
            slugs.setdefault(slug, []).append(i)

        date = entry.get("date")
        if isinstance(date, str) and not DATE_RE.match(date):
            errors.append(f"{label}: date '{date}' must match YYYY-MM-DD")

        artifact_type = entry.get("type")
        if artifact_type is not None and artifact_type not in VALID_TYPES:
            errors.append(f"{label}: type '{artifact_type}' must be one of {sorted(VALID_TYPES)}")

        status = entry.get("status")
        if status is not None and status not in VALID_STATUSES:
            errors.append(f"{label}: status '{status}' must be one of {sorted(VALID_STATUSES)}")

        index_code = entry.get("indexCode")
        if isinstance(index_code, str):
            if not INDEX_CODE_RE.match(index_code):
                errors.append(f"{label}: indexCode '{index_code}' must match PREFIX-NNN (e.g. OPS-001)")
            index_codes.setdefault(index_code, []).append(i)

        file_name = entry.get("file")
        if isinstance(file_name, str):
            if "/" in file_name or "\\" in file_name:
                errors.append(f"{label}: file '{file_name}' must be a bare filename, no path")
            elif not (docs_dir / file_name).exists():
                errors.append(f"{label}: file '{file_name}' not found in {docs_dir}/")

    for slug, indices in slugs.items():
        if len(indices) > 1:
            errors.append(f"duplicate slug '{slug}' used by entries {indices}")

    for code, indices in index_codes.items():
        if len(indices) > 1:
            errors.append(f"duplicate indexCode '{code}' used by entries {indices}")

    if errors:
        print(f"FAILED: {len(errors)} problem(s) in {manifest_path}\n")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)

    print(f"OK: {manifest_path} — {len(manifest)} entries, all valid")


if __name__ == "__main__":
    main()
