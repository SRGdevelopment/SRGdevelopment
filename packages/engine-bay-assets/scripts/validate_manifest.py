#!/usr/bin/env python3
"""Validate an engine-bay asset manifest without third-party dependencies."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

VALID_UNITS = {"meter", "millimeter", "centimeter", "inch"}
VALID_UP_AXIS = {"Y", "Z"}
PART_ID_PATTERN = re.compile(r"^[a-z0-9_\-]+$")


def require(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def is_vector3(value: Any) -> bool:
    return isinstance(value, list) and len(value) == 3 and all(isinstance(item, (int, float)) for item in value)


def validate_manifest(path: Path) -> list[str]:
    errors: list[str] = []
    try:
        manifest = json.loads(path.read_text())
    except json.JSONDecodeError as exc:
        return [f"Invalid JSON: {exc}"]

    required = [
        "manifest_version",
        "assembly_id",
        "revision",
        "units",
        "up_axis",
        "model_url",
        "draco_compressed",
        "meshopt_compressed",
        "texture_format",
        "lods",
        "parts",
    ]
    for key in required:
        require(key in manifest, f"Missing top-level key: {key}", errors)

    require(manifest.get("units") in VALID_UNITS, "units must be meter, millimeter, centimeter, or inch", errors)
    require(manifest.get("up_axis") in VALID_UP_AXIS, "up_axis must be Y or Z", errors)
    require(isinstance(manifest.get("model_url"), str) and bool(manifest.get("model_url")), "model_url must be a non-empty string", errors)
    require(isinstance(manifest.get("lods"), list), "lods must be an array", errors)
    require(isinstance(manifest.get("parts"), list) and len(manifest.get("parts", [])) > 0, "parts must be a non-empty array", errors)

    seen_ids: set[str] = set()
    for index, part in enumerate(manifest.get("parts", [])):
        prefix = f"parts[{index}]"
        require(isinstance(part, dict), f"{prefix} must be an object", errors)
        if not isinstance(part, dict):
            continue
        part_id = part.get("id")
        require(isinstance(part_id, str) and bool(PART_ID_PATTERN.match(part_id)), f"{prefix}.id must be slug-like", errors)
        require(part_id not in seen_ids, f"Duplicate part id: {part_id}", errors)
        if isinstance(part_id, str):
            seen_ids.add(part_id)
        for key in ["name", "sku", "oem_number", "category", "documentation_url"]:
            require(isinstance(part.get(key), str) and bool(part.get(key)), f"{prefix}.{key} must be a non-empty string", errors)
        require(is_vector3(part.get("position")), f"{prefix}.position must be a 3-number vector", errors)
        require(is_vector3(part.get("exploded_offset")), f"{prefix}.exploded_offset must be a 3-number vector", errors)
        require(isinstance(part.get("bounding_radius"), (int, float)) and part.get("bounding_radius", 0) > 0, f"{prefix}.bounding_radius must be > 0", errors)
        if part.get("parent_id") is not None:
            require(isinstance(part.get("parent_id"), str), f"{prefix}.parent_id must be string or null", errors)

    for index, part in enumerate(manifest.get("parts", [])):
        if isinstance(part, dict) and part.get("parent_id"):
            require(part["parent_id"] in seen_ids, f"parts[{index}].parent_id references unknown part", errors)

    return errors


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: validate_manifest.py <manifest.json>", file=sys.stderr)
        return 2
    path = Path(sys.argv[1])
    errors = validate_manifest(path)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(f"Manifest valid: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
