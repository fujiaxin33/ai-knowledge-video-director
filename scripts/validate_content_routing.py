#!/usr/bin/env python3
"""Validate declared primary mode and optional storytelling layers against explicit traits."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def expected_route(case: dict) -> tuple[str, set[str]]:
    primary = "STANDARD" if case.get("real_screen_primary") or case.get("formal_enterprise") else (
        "WHITEBOARD_STORYTELLING" if case.get("drawn_story_world") else "STANDARD")
    layers = set()
    if (case.get("cultural_punch_helpful") or case.get("internet_language_requested")) and not (
            case.get("no_humor") or case.get("formal_enterprise")):
        layers.add("INTERNET_NATIVE_STORYTELLING")
    if case.get("draw_while_talking") and not case.get("finished_frame_required"):
        layers.add("LIVE_DRAWING_STORYTELLING")
    return primary, layers


def validate(data: dict) -> dict:
    errors, rows = [], []
    cases = data.get("cases", [])
    if not cases:
        errors.append("routing manifest must contain cases")
    for index, case in enumerate(cases):
        cid = str(case.get("id", index))
        primary, layers = expected_route(case)
        actual_primary = str(case.get("route", {}).get("primary_mode", "")).upper()
        actual_layers = {str(value).upper() for value in case.get("route", {}).get("layers", [])}
        item = []
        if actual_primary != primary:
            item.append(f"primary mode {actual_primary or '<empty>'} != {primary}")
        if actual_layers != layers:
            item.append(f"layers {sorted(actual_layers)} != {sorted(layers)}")
        errors.extend(f"{cid}: {message}" for message in item)
        rows.append({"id": cid, "expected_primary": primary, "expected_layers": sorted(layers), "pass": not item})
    return {"pass": not errors, "errors": errors, "cases": rows,
            "note": "Platform alone never enables internet-native; explicit audience/content traits do."}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    try:
        result = validate(json.loads(args.manifest.read_text(encoding="utf-8-sig")))
    except (OSError, ValueError, TypeError, json.JSONDecodeError) as exc:
        result = {"pass": False, "errors": [str(exc)]}
    output = json.dumps(result, ensure_ascii=False, indent=2)
    print(output)
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(output + "\n", encoding="utf-8")
    return 0 if result.get("pass") else 1


if __name__ == "__main__":
    sys.exit(main())
