#!/usr/bin/env python3
"""Validate semantic single-line whiteboard captions and declared safe-zone geometry."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def inside(rect: tuple[float, float, float, float], zone: tuple[float, float, float, float]) -> bool:
    x, y, w, h = rect
    zx, zy, zw, zh = zone
    return x >= zx and y >= zy and x + w <= zx + zw and y + h <= zy + zh


def validate(data: dict) -> dict:
    captions = sorted(data.get("captions", []), key=lambda item: float(item.get("start", 0)))
    errors, warnings, rows = [], [], []
    recommended = int(data.get("recommended_characters", 16))
    hard_limit = int(data.get("hard_limit_characters", 22))
    canvas = data.get("canvas", {})
    safe = data.get("safe_zone", {})
    zone = (float(safe.get("x", 0)), float(safe.get("y", 0)), float(safe.get("width", canvas.get("width", 0))),
            float(safe.get("height", canvas.get("height", 0))))
    if not captions:
        errors.append("manifest must contain at least one caption")
    previous = None
    for index, caption in enumerate(captions):
        cid = str(caption.get("id", index))
        text = str(caption.get("text", "")).strip()
        item_errors, item_warnings = [], []
        start, end = float(caption.get("start", 0)), float(caption.get("end", 0))
        if end <= start:
            item_errors.append("caption duration must be positive")
        if not text:
            item_errors.append("caption text is empty")
        if "\n" in text or int(caption.get("line_count", 1)) != 1:
            item_errors.append("whiteboard caption must be one line")
        if len(text) > hard_limit:
            item_errors.append(f"caption length {len(text)} exceeds hard candidate limit {hard_limit}")
        elif len(text) > recommended:
            item_warnings.append(f"caption length {len(text)} exceeds recommended {recommended}")
        if not caption.get("semantic", False):
            item_warnings.append("caption is not declared semantic/compressed")
        if all(field in caption for field in ("x", "y", "width", "height")):
            rect = tuple(float(caption[field]) for field in ("x", "y", "width", "height"))
            if not inside(rect, zone):
                item_errors.append("caption box leaves the declared safe zone")
            if canvas.get("width") and canvas.get("height"):
                area_ratio = rect[2] * rect[3] / (float(canvas["width"]) * float(canvas["height"]))
                if area_ratio > .12:
                    item_warnings.append("caption box area may dominate the whiteboard")
        else:
            item_warnings.append("caption geometry is missing; safe-zone check is incomplete")
        if previous is not None:
            if start < float(previous["end"]):
                item_errors.append("caption overlaps the previous caption")
            if text == str(previous.get("text", "")).strip():
                item_warnings.append("caption repeats the previous semantic line")
        errors.extend(f"{cid}: {message}" for message in item_errors)
        warnings.extend(f"{cid}: {message}" for message in item_warnings)
        rows.append({"id": cid, "status": "FAIL" if item_errors else ("WARN" if item_warnings else "PASS"),
                     "errors": item_errors, "warnings": item_warnings})
        previous = caption
    return {
        "pass": not errors, "caption_count": len(captions), "errors": errors, "warnings": warnings,
        "captions": rows,
        "automated_scope": "line count, length candidates, temporal overlap/repetition, declared safe-zone geometry and area",
        "human_review_required": ["semantic compression", "visual priority", "face/Hand/story collision", "reading rhythm"],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    try:
        result = validate(json.loads(args.manifest.read_text(encoding="utf-8-sig")))
    except (OSError, ValueError, TypeError, json.JSONDecodeError) as exc:
        result = {"pass": False, "errors": [str(exc)], "warnings": []}
    output = json.dumps(result, ensure_ascii=False, indent=2)
    print(output)
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(output + "\n", encoding="utf-8")
    return 0 if result.get("pass") else 1


if __name__ == "__main__":
    sys.exit(main())
