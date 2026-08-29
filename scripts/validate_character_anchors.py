#!/usr/bin/env python3
"""Validate character pose-swap anchors, scale continuity, and temporal uniqueness."""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path


def validate(data: dict) -> dict:
    characters = data.get("characters", [])
    errors, warnings, rows = [], [], []
    max_jump = float(data.get("max_anchor_jump_px", 32))
    max_scale = float(data.get("max_scale_jump", .08))
    if not characters:
        errors.append("manifest must contain at least one character")
    for index, character in enumerate(characters):
        cid = str(character.get("id", index))
        states = sorted(character.get("states", []), key=lambda state: float(state.get("time", 0)))
        char_errors, char_warnings = [], []
        if len(states) < 2:
            char_errors.append("character needs at least two states for an anchor comparison")
        previous = None
        for state_index, state in enumerate(states):
            if int(state.get("visible_count", 1)) != 1 and not state.get("intentional_duplicate"):
                char_errors.append(f"state {state_index}: more than one temporal character state is visible")
            if state.get("mirrored") and state.get("contains_text_or_directional_prop"):
                char_errors.append(f"state {state_index}: mirrored text/logo/directional prop")
            required = ("anchor_x", "anchor_y", "scale")
            if any(field not in state for field in required):
                char_errors.append(f"state {state_index}: missing anchor/scale")
                continue
            if previous is not None and not state.get("intentional_translation"):
                distance = math.dist([float(previous["anchor_x"]), float(previous["anchor_y"])],
                                     [float(state["anchor_x"]), float(state["anchor_y"])])
                scale_delta = abs(float(state["scale"]) - float(previous["scale"]))
                local_jump = float(state.get("max_anchor_jump_px", max_jump))
                local_scale = float(state.get("max_scale_jump", max_scale))
                if distance > local_jump:
                    char_errors.append(f"state {state_index}: anchor jump {distance:.1f}px > {local_jump:.1f}px")
                if scale_delta > local_scale:
                    char_errors.append(f"state {state_index}: scale jump {scale_delta:.3f} > {local_scale:.3f}")
            if not state.get("full_silhouette", True) and not state.get("intentional_occlusion"):
                char_errors.append(f"state {state_index}: unintended partial silhouette")
            previous = state
        errors.extend(f"{cid}: {message}" for message in char_errors)
        warnings.extend(f"{cid}: {message}" for message in char_warnings)
        rows.append({"id": cid, "pass": not char_errors, "errors": char_errors, "warnings": char_warnings})
    return {
        "pass": not errors, "character_count": len(characters), "errors": errors, "warnings": warnings,
        "characters": rows,
        "automated_scope": "declared base-anchor/scale deltas, temporal state count, silhouette and mirror flags",
        "human_review_required": ["visual identity continuity", "actual feet/base alignment", "face/gesture safety", "intentional occlusion"],
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
