#!/usr/bin/env python3
"""Validate skills/manifest.json against the Skill schema.

Usage:
    python3 validate_skills_manifest.py [path/to/skills]

Defaults to "skills" in the current directory. Checks manifest.json parses,
every entry has the required fields with correct types/enums, slugs and
indexCodes are unique, and every entry's `slug` has a matching
skills/<slug>/SKILL.md on disk. Exits non-zero if any check fails, printing
every problem found (not just the first).
"""
import json
import re
import sys
from pathlib import Path

REQUIRED_STRING_FIELDS = ["slug", "name", "indexCode", "category", "summary", "whenToUse"]
REQUIRED_ARRAY_FIELDS = ["inputs", "outputs", "relatedArtifacts", "tags"]
VALID_CATEGORIES = {"Research", "Operations", "Market", "Product", "AI"}
SLUG_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
INDEX_CODE_RE = re.compile(r"^SKILL-\d{3}$")


def main():
    skills_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("skills")
    manifest_path = skills_dir / "manifest.json"

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

        for field in REQUIRED_ARRAY_FIELDS:
            if field not in entry:
                errors.append(f"{label}: missing required field '{field}'")
            elif not isinstance(entry[field], list) or not all(isinstance(v, str) for v in entry[field]):
                errors.append(f"{label}: '{field}' must be an array of strings")

        slug = entry.get("slug")
        if isinstance(slug, str):
            if not SLUG_RE.match(slug):
                errors.append(f"{label}: slug '{slug}' must be kebab-case ([a-z0-9-])")
            slugs.setdefault(slug, []).append(i)

            skill_md = skills_dir / slug / "SKILL.md"
            if not skill_md.exists():
                errors.append(f"{label}: {skill_md} not found (every skill needs a real SKILL.md folder)")

        category = entry.get("category")
        if category is not None and category not in VALID_CATEGORIES:
            errors.append(f"{label}: category '{category}' must be one of {sorted(VALID_CATEGORIES)}")

        index_code = entry.get("indexCode")
        if isinstance(index_code, str):
            if not INDEX_CODE_RE.match(index_code):
                errors.append(f"{label}: indexCode '{index_code}' must match SKILL-NNN (e.g. SKILL-001)")
            index_codes.setdefault(index_code, []).append(i)

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
