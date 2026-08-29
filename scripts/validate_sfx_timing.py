#!/usr/bin/env python3
"""Validate SFX-to-motion timing, including impact and pen-down intervals."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def classify(delta_ms: float, pass_ms: float, warn_ms: float) -> str:
    if delta_ms <= pass_ms:
        return "PASS"
    if delta_ms <= warn_ms:
        return "WARN"
    return "FAIL"


def validate(data: dict) -> dict:
    events = data.get("events", [])
    errors, warnings, rows = [], [], []
    if not events:
        errors.append("manifest must contain at least one SFX event")
    for index, event in enumerate(events):
        eid = str(event.get("id", index))
        kind = str(event.get("type", "")).upper()
        pass_ms = float(event.get("pass_ms", data.get("pass_ms", 80)))
        warn_ms = float(event.get("warn_ms", data.get("warn_ms", 150)))
        status, deltas, event_errors = "PASS", [], []
        if kind == "DRAW":
            required = ("motion_start", "motion_end", "sfx_start", "sfx_end")
            if any(field not in event for field in required):
                event_errors.append("DRAW requires motion_start/end and sfx_start/end")
            else:
                deltas = [abs(float(event["sfx_start"]) - float(event["motion_start"])) * 1000,
                          abs(float(event["sfx_end"]) - float(event["motion_end"])) * 1000]
        elif kind in {"MOTION", "IMPACT", "COMEDY", "REVEAL"}:
            if "impact_time" not in event or "sfx_time" not in event:
                event_errors.append(f"{kind or 'event'} requires impact_time and sfx_time")
            else:
                deltas = [abs(float(event["sfx_time"]) - float(event["impact_time"])) * 1000]
        else:
            event_errors.append(f"unsupported SFX type: {kind}")
        if event_errors:
            status = "FAIL"
        elif deltas:
            status = max((classify(value, pass_ms, warn_ms) for value in deltas),
                         key={"PASS": 0, "WARN": 1, "FAIL": 2}.get)
        if status == "FAIL":
            errors.append(f"{eid}: timing exceeds tolerance or manifest is invalid")
        elif status == "WARN":
            warnings.append(f"{eid}: timing delta is perceptually reviewable")
        rows.append({"id": eid, "type": kind, "status": status,
                     "delta_ms": [round(value, 3) for value in deltas], "errors": event_errors,
                     "pass_ms": pass_ms, "warn_ms": warn_ms})
    return {
        "pass": not errors, "event_count": len(events), "errors": errors, "warnings": warnings, "events": rows,
        "automated_scope": "declared impact/draw timestamps and per-event tolerances",
        "human_review_required": ["perceived transient onset", "dialogue masking", "comedy strength", "licensed-source suitability"],
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
