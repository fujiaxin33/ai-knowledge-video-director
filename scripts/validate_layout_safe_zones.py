#!/usr/bin/env python3
"""Check layout elements against explicit final-canvas safe zones."""

import argparse
import json
import sys
from pathlib import Path


def r(item):
    return tuple(item[k] for k in ("x", "y", "width", "height"))


def overlap(a, b):
    ax, ay, aw, ah = a
    bx, by, bw, bh = b
    return ax < bx + bw and ax + aw > bx and ay < by + bh and ay + ah > by


def active(a, b):
    return max(a.get("start_frame", 0), b.get("start_frame", 0)) <= min(
        a.get("end_frame", 10**12), b.get("end_frame", 10**12)
    )


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("manifest", type=Path)
    ap.add_argument("--report", type=Path)
    args = ap.parse_args()
    data = json.loads(args.manifest.read_text(encoding="utf-8"))
    width, height = data["canvas"]["width"], data["canvas"]["height"]
    elements = data.get("layout_elements", [])
    zones = {z["id"]: z for z in data.get("safe_zones", [])}
    errors = []

    for item in elements + list(zones.values()):
        try:
            x, y, w, h = r(item)
            if any(not isinstance(v, int) for v in (x, y, w, h)):
                errors.append(f"{item.get('id')}: rectangle must use integer pixels")
            if x < 0 or y < 0 or w <= 0 or h <= 0 or x + w > width or y + h > height:
                errors.append(f"{item.get('id')}: rectangle outside canvas")
        except Exception:
            errors.append(f"{item.get('id', '<unnamed>')}: invalid rectangle")

    for item in elements:
        for zid in item.get("avoid_safe_zones", []):
            zone = zones.get(zid)
            if zone is None:
                errors.append(f"{item.get('id')}: unknown safe zone {zid}")
            elif active(item, zone) and overlap(r(item), r(zone)):
                errors.append(f"{item.get('id')}: overlaps safe zone {zid}")

    by_id = {x.get("id"): x for x in elements + list(zones.values())}
    for pair in data.get("forbidden_pairs", []):
        if len(pair) != 2 or pair[0] not in by_id or pair[1] not in by_id:
            errors.append(f"invalid forbidden pair: {pair}")
            continue
        a, b = by_id[pair[0]], by_id[pair[1]]
        if active(a, b) and overlap(r(a), r(b)):
            errors.append(f"forbidden overlap: {pair[0]} × {pair[1]}")

    result = {"pass": not errors, "errors": errors, "element_count": len(elements)}
    output = json.dumps(result, ensure_ascii=False, indent=2)
    print(output)
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(output + "\n", encoding="utf-8")
    return 0 if result["pass"] else 1


if __name__ == "__main__":
    sys.exit(main())

