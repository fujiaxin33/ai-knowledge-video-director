#!/usr/bin/env python3
"""Validate structured draw-on progression and Hand-tip/reveal-front alignment."""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path


ALLOWED_INSTANT_INTENTS = {"comedy impact", "surprise", "error mark", "explosion", "sudden prop", "visual punch"}
MODE_ALIASES = {
    "true draw": "true_stroke", "true_draw": "true_stroke", "mask draw": "progressive_mask",
    "mask_draw": "progressive_mask", "hand reveal": "hand_reveal", "hand_reveal": "hand_reveal",
    "assembly build": "assembly_build", "transform": "transform", "comedy pop": "instant_pop",
    "comedy_pop": "instant_pop",
}


def validate(data: dict) -> dict:
    errors, warnings, rows = [], [], []
    tolerance = float(data.get("max_tip_distance", 40.0))
    sequences = data.get("sequences", [])
    if not sequences:
        errors.append("manifest must contain at least one draw sequence")
    for index, seq in enumerate(sequences):
        sid = str(seq.get("id", index))
        mode = str(seq.get("mode", "")).lower()
        mode = MODE_ALIASES.get(mode, mode)
        start, end = seq.get("start"), seq.get("end")
        seq_errors, seq_warnings = [], []
        if not isinstance(start, (int, float)) or not isinstance(end, (int, float)) or end <= start:
            seq_errors.append("start/end must define a positive duration")
        if mode == "instant_pop":
            intent = str(seq.get("intent", "")).lower()
            if intent not in ALLOWED_INSTANT_INTENTS:
                seq_errors.append("instant_pop lacks an allowed impact intent")
        elif mode not in {"true_stroke", "progressive_mask", "assembly_build", "hand_reveal", "transform"}:
            seq_errors.append(f"unsupported draw mode: {mode}")

        if seq.get("high_quality_asset") and not seq.get("final_quality_preserved"):
            seq_errors.append("high-quality asset is not declared preserved in the final state")
        stages = seq.get("becoming_stages")
        if seq.get("live_drawing") and (not isinstance(stages, list) or len(stages) < 2):
            seq_errors.append("live drawing requires at least two meaningful becoming stages")
        if all(key in seq for key in ("voice_start", "voice_end", "draw_start", "draw_end")):
            vs, ve = float(seq["voice_start"]), float(seq["voice_end"])
            ds, de = float(seq["draw_start"]), float(seq["draw_end"])
            if ve <= vs or de <= ds or min(ve, de) <= max(vs, ds):
                seq_errors.append("draw and related voice must overlap with positive duration")

        samples = seq.get("samples", [])
        if mode != "instant_pop" and len(samples) < 3:
            seq_errors.append("progressive draw requires at least three samples")
        last_reveal = -1.0
        for sample_index, sample in enumerate(samples):
            reveal = sample.get("reveal")
            if not isinstance(reveal, (int, float)) or not 0 <= reveal <= 1:
                seq_errors.append(f"sample {sample_index}: reveal must be within 0..1")
                continue
            if reveal + 1e-6 < last_reveal:
                seq_errors.append(f"sample {sample_index}: reveal is not monotonic")
            active = reveal > last_reveal + 1e-6 and 0.01 < reveal < .99
            if active and not sample.get("hand_present"):
                seq_errors.append(f"sample {sample_index}: active reveal has no Hand")
            if active and sample.get("hand_moving") is False and not sample.get("autonomous_effect"):
                seq_errors.append(f"sample {sample_index}: reveal continues after Hand stops")
            hand, front = sample.get("hand_tip"), sample.get("reveal_front")
            if active and (not isinstance(hand, list) or not isinstance(front, list) or len(hand) != 2 or len(front) != 2):
                seq_errors.append(f"sample {sample_index}: Hand tip and reveal front are required")
            elif active:
                distance = math.dist([float(hand[0]), float(hand[1])], [float(front[0]), float(front[1])])
                if distance > tolerance:
                    seq_errors.append(f"sample {sample_index}: Hand/front distance {distance:.1f}px > {tolerance:.1f}px")
            last_reveal = reveal
        if samples:
            if float(samples[0].get("reveal", 1)) > .15:
                if seq.get("live_drawing"):
                    seq_errors.append("live-drawing final state is already present at the start")
                else:
                    seq_warnings.append("first sample already reveals more than 15%")
            if float(samples[-1].get("reveal", 0)) < .90:
                seq_errors.append("final sample is not substantially complete")
        errors.extend(f"{sid}: {message}" for message in seq_errors)
        warnings.extend(f"{sid}: {message}" for message in seq_warnings)
        rows.append({"id": sid, "mode": mode, "pass": not seq_errors,
                     "errors": seq_errors, "warnings": seq_warnings})
    return {
        "pass": not errors, "sequence_count": len(sequences), "errors": errors, "warnings": warnings,
        "sequences": rows,
        "automated_scope": "structured timing, voice/draw overlap, becoming states, asset preservation, reveal monotonicity, Hand motion, tip/front distance, and instant-pop intent",
        "human_review_required": ["stroke naturalness", "Hand acting purpose", "semantic part order", "mask-edge quality", "whether an instant punch is tasteful"],
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
