#!/usr/bin/env python3
"""Validate a structured voice/visual contract without claiming semantic vision."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def validate(data: dict) -> dict:
    beats = data.get("beats", [])
    errors, warnings, rows = [], [], []
    if not beats:
        errors.append("manifest must contain at least one beat")
    for index, beat in enumerate(beats):
        bid = str(beat.get("id", index))
        beat_errors, beat_warnings = [], []
        required = ("voice_start", "voice_end", "visual_start", "visual_end", "intended_meaning")
        if any(field not in beat for field in required):
            beat_errors.append("missing required voice/visual fields")
        else:
            vs, ve = float(beat["voice_start"]), float(beat["voice_end"])
            xs, xe = float(beat["visual_start"]), float(beat["visual_end"])
            if ve <= vs or xe <= xs:
                beat_errors.append("voice and visual spans must have positive duration")
            lead = xs - vs
            if lead < -.20:
                beat_errors.append(f"visual starts {-lead * 1000:.0f}ms too early")
            elif lead > .30:
                beat_errors.append(f"visual starts {lead * 1000:.0f}ms late")
            elif lead > .20:
                beat_warnings.append(f"visual start lag is {lead * 1000:.0f}ms")
            if xe < ve - .15:
                beat_errors.append("visual exits before the spoken meaning finishes")
            next_voice = beat.get("next_voice_start")
            if next_voice is not None and xe > float(next_voice) + .30:
                beat_errors.append("old visual persists after the next voice beat")
            if "reveal_time" in beat:
                if "keyword_start" not in beat or "keyword_end" not in beat:
                    beat_errors.append("reveal_time requires keyword_start and keyword_end")
                else:
                    reveal = float(beat["reveal_time"])
                    ks, ke = float(beat["keyword_start"]), float(beat["keyword_end"])
                    if reveal < ks - .20 or reveal > ke + .20:
                        beat_errors.append("reveal completion is outside the keyword contract")
                    elif reveal < ks or reveal > ke:
                        beat_warnings.append("reveal completion uses the allowed anticipation/lag margin")
        if not str(beat.get("visual_event", "")).strip():
            beat_errors.append("visual_event is required")
        voice_facts, visual_facts = beat.get("voice_facts"), beat.get("visual_facts")
        if voice_facts is not None or visual_facts is not None:
            if not isinstance(voice_facts, dict) or not isinstance(visual_facts, dict):
                beat_errors.append("voice_facts and visual_facts must both be objects")
            else:
                for key in ("counts", "numbers", "terms", "names", "brands", "polarity", "relations"):
                    if voice_facts.get(key, {}) != visual_facts.get(key, {}):
                        beat_errors.append(f"semantic mismatch in {key}")
        errors.extend(f"{bid}: {message}" for message in beat_errors)
        warnings.extend(f"{bid}: {message}" for message in beat_warnings)
        rows.append({"id": bid, "status": "FAIL" if beat_errors else ("WARN" if beat_warnings else "PASS"),
                     "errors": beat_errors, "warnings": beat_warnings})
    return {
        "pass": not errors, "beat_count": len(beats), "errors": errors, "warnings": warnings, "beats": rows,
        "automated_scope": "voice/visual spans, next-beat persistence, keyword/reveal timing, and declared fact equality",
        "human_review_required": ["undeclared semantic equivalence", "whether anticipation feels natural"],
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
