#!/usr/bin/env python3
"""Validate semantic annotation geometry on a final video canvas."""

import argparse
import json
import math
import sys
from pathlib import Path


def rect(item):
    return tuple(item[k] for k in ("x", "y", "width", "height"))


def inside(inner, outer):
    ix, iy, iw, ih = inner
    ox, oy, ow, oh = outer
    return ix >= ox and iy >= oy and ix + iw <= ox + ow and iy + ih <= oy + oh


def overlaps(a, b):
    ax, ay, aw, ah = a
    bx, by, bw, bh = b
    return ax < bx + bw and ax + aw > bx and ay < by + bh and ay + ah > by


def active_overlap(a, b):
    return max(a.get("start_frame", 0), b.get("start_frame", 0)) <= min(
        a.get("end_frame", 10**12), b.get("end_frame", 10**12)
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    data = json.loads(args.manifest.read_text(encoding="utf-8"))
    canvas = (0, 0, data["canvas"]["width"], data["canvas"]["height"])
    zones = {z["id"]: z for z in data.get("safe_zones", [])}
    errors, warnings = [], []

    for ann in data.get("annotations", []):
        aid = ann.get("id", "<unnamed>")
        for field in ("start_frame", "end_frame"):
            if not isinstance(ann.get(field), int):
                errors.append(f"{aid}: {field} must be an integer")
        if ann.get("start_frame", 0) > ann.get("end_frame", -1):
            errors.append(f"{aid}: start_frame is after end_frame")
        for name in ("target", "annotation"):
            try:
                r = rect(ann[name])
            except Exception:
                errors.append(f"{aid}: missing valid {name} rectangle")
                continue
            if any(not isinstance(v, int) for v in r):
                errors.append(f"{aid}: {name} coordinates must be integer pixels")
            if r[2] <= 0 or r[3] <= 0 or not inside(r, canvas):
                errors.append(f"{aid}: {name} is invalid or outside canvas: {r}")

        if "target" not in ann or "annotation" not in ann:
            continue
        target, mark = rect(ann["target"]), rect(ann["annotation"])
        kind = ann.get("kind", "box")
        if kind == "box":
            if not inside(target, mark):
                errors.append(f"{aid}: box does not fully contain semantic target")
            else:
                tx, ty, tw, th = target
                mx, my, mw, mh = mark
                pads = (tx - mx, ty - my, mx + mw - tx - tw, my + mh - ty - th)
                declared = ann.get("padding")
                if declared is not None and any(abs(p - declared) > 4 for p in pads):
                    errors.append(f"{aid}: box padding {pads} is not aligned to declared {declared}px")
                if min(pads) < 8 or max(pads) > 20:
                    errors.append(f"{aid}: box padding {pads} must stay within 8–20px")
        elif kind == "underline":
            tx, ty, tw, th = target
            mx, my, mw, mh = mark
            if abs(mx - tx) > 8 or abs(mw - tw) > 16:
                errors.append(f"{aid}: underline does not span the target text")
            if not (ty + th - 6 <= my <= ty + th + 14):
                errors.append(f"{aid}: underline is not anchored to target baseline")
            if mh > 12:
                warnings.append(f"{aid}: underline is visually heavy ({mh}px)")

        for zid in ann.get("avoid_safe_zones", []):
            zone = zones.get(zid)
            if zone is None:
                errors.append(f"{aid}: unknown safe zone {zid}")
            elif active_overlap(ann, zone) and overlaps(mark, rect(zone)):
                errors.append(f"{aid}: annotation overlaps safe zone {zid}")
        if not ann.get("semantic_target") or not ann.get("why_now"):
            errors.append(f"{aid}: semantic_target and why_now are required")

    result = {"pass": not errors, "errors": errors, "warnings": warnings,
              "annotation_count": len(data.get("annotations", []))}
    output = json.dumps(result, ensure_ascii=False, indent=2)
    print(output)
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(output + "\n", encoding="utf-8")
    return 0 if result["pass"] else 1


if __name__ == "__main__":
    sys.exit(main())

