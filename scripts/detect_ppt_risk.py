#!/usr/bin/env python3
"""Detect rolling concept-only windows in a visual beat manifest."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


DEFAULT_CONCEPT_TYPES = {"concept card", "static motion page", "concept motion"}


def norm(value: str) -> str:
    return " ".join(value.replace("_", " ").replace("-", " ").lower().split())


def load_beats(path: Path) -> list[dict]:
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    beats = data.get("beats", data) if isinstance(data, dict) else data
    if not isinstance(beats, list) or not beats:
        raise ValueError("manifest must contain a non-empty beat list")
    parsed = []
    for index, beat in enumerate(beats):
        try:
            start = float(beat["start"])
            end = float(beat["end"])
            visual_type = norm(str(beat["visual_type"]))
        except (KeyError, TypeError, ValueError) as exc:
            raise ValueError(f"invalid beat at index {index}: {exc}") from exc
        if end <= start:
            raise ValueError(f"beat {index} must have end > start")
        parsed.append({"start": start, "end": end, "visual_type": visual_type, "id": beat.get("id", index)})
    return parsed


def detect(beats: list[dict], window: float, step: float, concept_types: set[str]) -> list[dict]:
    start = min(b["start"] for b in beats)
    finish = max(b["end"] for b in beats)
    raw = []
    t = start
    while t + window <= finish + 1e-6:
        end = t + window
        overlaps = [b for b in beats if b["end"] > t and b["start"] < end]
        coverage = sum(max(0.0, min(end, b["end"]) - max(t, b["start"])) for b in overlaps)
        types = {b["visual_type"] for b in overlaps}
        if coverage >= window * 0.9 and types and types.issubset(concept_types):
            raw.append({"start": round(t, 3), "end": round(end, 3), "visual_types": sorted(types)})
        t += step

    merged: list[dict] = []
    for risk in raw:
        if merged and risk["start"] <= merged[-1]["end"] + step + 1e-6:
            merged[-1]["end"] = risk["end"]
            merged[-1]["visual_types"] = sorted(set(merged[-1]["visual_types"]) | set(risk["visual_types"]))
        else:
            merged.append(risk)
    return merged


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--window", type=float, default=10.0)
    parser.add_argument("--step", type=float, default=1.0)
    parser.add_argument("--concept-type", action="append", dest="concept_types")
    parser.add_argument("--report", type=Path)
    parser.add_argument("--fail-on-risk", action="store_true")
    args = parser.parse_args()

    try:
        beats = load_beats(args.manifest)
        concept_types = {norm(v) for v in (args.concept_types or DEFAULT_CONCEPT_TYPES)}
        risks = detect(beats, args.window, args.step, concept_types)
        result = {
            "pass": not risks,
            "manifest": str(args.manifest),
            "window_seconds": args.window,
            "step_seconds": args.step,
            "risk_count": len(risks),
            "risks": risks,
            "note": "PPT_RISK requires semantic review; visual types are not an equal-ratio quota.",
        }
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        result = {"pass": False, "errors": [str(exc)], "risks": []}

    output = json.dumps(result, ensure_ascii=False, indent=2)
    print(output)
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(output + "\n", encoding="utf-8")
    if result.get("errors"):
        return 2
    return 1 if args.fail_on_risk and result.get("risks") else 0


if __name__ == "__main__":
    sys.exit(main())
